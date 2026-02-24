#!/usr/bin/env python3
"""
MVP Progress Data Generator
============================
Queries GitHub Projects v2 (primary) or falls back to the Issues API to produce
a clean JSON snapshot for the progress-tracker dashboard.

Environment variables
---------------------
ORG                 GitHub org name          (default: Coalescent-Emergence)
REPO                Kerrigan repo name       (default: Kerrigan)
TOKEN               GitHub PAT               (required for private repos / Projects v2)
GH_PROJECT_NUMBER   Projects v2 number       (optional; enables Projects v2 mode)
OUTDIR              Output directory         (default: docs/data)

Output: $OUTDIR/mvp-data.json
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

# ─── Config ──────────────────────────────────────────────────────────────────
ORG = os.environ.get("ORG", "Coalescent-Emergence")
REPO = os.environ.get("REPO", "Kerrigan")
TOKEN = os.environ.get("TOKEN", "")
PROJECT_NUMBER_STR = os.environ.get("GH_PROJECT_NUMBER", "")
OUTDIR = os.environ.get("OUTDIR", "docs/data")
OUTFILE = os.path.join(OUTDIR, "mvp-data.json")


# ─── HTTP helpers ─────────────────────────────────────────────────────────────
def gh_request(
    url: str,
    method: str = "GET",
    body: Optional[bytes] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Any:
    headers: Dict[str, str] = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "mvp-progress-generator/2.0",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {detail[:300]}") from exc


def gh_graphql(query: str, variables: Optional[Dict] = None) -> Any:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    result = gh_request(
        "https://api.github.com/graphql",
        method="POST",
        body=payload,
        extra_headers={"Content-Type": "application/json"},
    )
    if "errors" in result:
        raise RuntimeError(f"GraphQL errors: {json.dumps(result['errors'])}")
    return result["data"]


# ─── Projects v2 ─────────────────────────────────────────────────────────────
_PROJECT_ITEMS_QUERY = """
query ($org: String!, $projectNumber: Int!, $cursor: String) {
  organization(login: $org) {
    projectV2(number: $projectNumber) {
      title
      url
      items(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          type
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2Field { name } }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field { ... on ProjectV2Field { name } }
              }
            }
          }
          content {
            ... on Issue {
              number
              title
              state
              url
              labels(first: 10) { nodes { name } }
            }
          }
        }
      }
    }
  }
}
"""


def _field_value(item: Dict, *field_names: str) -> Optional[str]:
    """Return the first matching field value (case-insensitive) from a project item."""
    for node in (item.get("fieldValues") or {}).get("nodes", []):
        if not isinstance(node, dict):
            continue
        field_name_actual = (node.get("field") or {}).get("name", "")
        if field_name_actual.lower() in {fn.lower() for fn in field_names}:
            return node.get("name") or node.get("text") or (
                str(int(node["number"])) if "number" in node else None
            )
    return None


def _fetch_all_project_items(org: str, number: int) -> Tuple[List[Dict], str, str]:
    """Return (items, project_title, project_url)."""
    items: List[Dict] = []
    cursor: Optional[str] = None
    project_title = ""
    project_url = ""
    while True:
        data = gh_graphql(_PROJECT_ITEMS_QUERY, {"org": org, "projectNumber": number, "cursor": cursor})
        proj = data["organization"]["projectV2"]
        project_title = proj.get("title", "")
        project_url = proj.get("url", "")
        page = proj["items"]
        items.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return items, project_title, project_url


def _normalise_state(state: str) -> str:
    return "closed" if state.upper() in ("CLOSED", "MERGED") else "open"


def build_from_project(org: str, project_number: int) -> Dict:
    print(f"[projects-v2] org={org} project=#{project_number}", flush=True)
    raw_items, project_title, project_url = _fetch_all_project_items(org, project_number)

    initiatives: List[Dict] = []
    deliveries: List[Dict] = []

    for item in raw_items:
        content = item.get("content") or {}
        if not content or "number" not in content:
            continue  # draft issue / PR — skip
        item_type_raw = (
            _field_value(item, "Item Type", "item_type", "type", "Type") or ""
        ).lower().strip()
        if item_type_raw in ("initiative", "umbrella", "epic", "milestone"):
            initiatives.append(item)
        else:
            deliveries.append(item)

    if not initiatives:
        print("[projects-v2] No initiative items found; falling back to flat grouping.", flush=True)
        return _build_flat(raw_items, org, project_title, project_url)

    # Build per-initiative records
    records: List[Dict] = []
    for item in initiatives:
        content = item["content"]
        init_number = content["number"]
        init_number_str = str(init_number)
        title = content.get("title", "")
        state = _normalise_state(content.get("state", "OPEN"))
        url = content.get("url", "")
        labels = [{"name": lbl["name"]} for lbl in (content.get("labels") or {}).get("nodes", [])]

        children: List[Dict] = []
        for d in deliveries:
            dc = d.get("content") or {}
            initiative_ref = (
                _field_value(d, "Initiative", "initiative_id", "Parent", "parent") or ""
            ).strip()
            # Match by issue number or title
            if initiative_ref and (initiative_ref == init_number_str or initiative_ref == title):
                children.append({
                    "number": dc.get("number"),
                    "title": dc.get("title", ""),
                    "state": _normalise_state(dc.get("state", "OPEN")),
                    "url": dc.get("url", ""),
                })

        if children:
            total = len(children)
            closed = sum(1 for c in children if c["state"] == "closed")
        else:
            # No linked children recorded — use init's own state
            total = 1
            closed = 1 if state == "closed" else 0

        percent = round(closed / total * 100) if total > 0 else 0
        records.append({
            "number": init_number,
            "title": title,
            "url": url,
            "status": "completed" if percent == 100 else ("in_progress" if percent > 0 else "not_started"),
            "labels": labels,
            "total": total,
            "closed": closed,
            "percent": percent,
            "children": children,
        })

    records.sort(key=lambda r: r.get("number") or 0)

    all_delivery_contents = [
        d.get("content") for d in deliveries if (d.get("content") or {}).get("number")
    ]
    total_all = len(all_delivery_contents) if all_delivery_contents else sum(r["total"] for r in records)
    closed_all = (
        sum(1 for c in all_delivery_contents if _normalise_state(c.get("state", "OPEN")) == "closed")
        if all_delivery_contents
        else sum(r["closed"] for r in records)
    )

    return _make_result(
        source="github-projects-v2",
        org=org,
        repo=REPO,
        project_title=project_title,
        records=records,
        total_all=total_all,
        closed_all=closed_all,
    )


def _build_flat(raw_items: List[Dict], org: str, project_title: str, project_url: str) -> Dict:
    """All project items treated as one group."""
    children: List[Dict] = []
    for item in raw_items:
        content = item.get("content") or {}
        if not content or "number" not in content:
            continue
        children.append({
            "number": content["number"],
            "title": content.get("title", ""),
            "state": _normalise_state(content.get("state", "OPEN")),
            "url": content.get("url", ""),
        })
    total = len(children)
    closed = sum(1 for c in children if c["state"] == "closed")
    percent = round(closed / total * 100) if total > 0 else 0
    record = {
        "number": 0,
        "title": project_title or "MVP Delivery",
        "url": project_url or f"https://github.com/orgs/{org}/projects",
        "status": "completed" if percent == 100 else ("in_progress" if percent > 0 else "not_started"),
        "labels": [],
        "total": total,
        "closed": closed,
        "percent": percent,
        "children": children,
    }
    return _make_result(
        source="github-projects-v2-flat",
        org=org,
        repo=REPO,
        project_title=project_title,
        records=[record],
        total_all=total,
        closed_all=closed,
    )


# ─── REST Issues fallback ─────────────────────────────────────────────────────
def _fetch_all_issues(owner: str, repo: str) -> List[Dict]:
    issues: List[Dict] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{owner}/{repo}/issues"
            f"?state=all&per_page=100&page={page}"
        )
        page_data = gh_request(url)
        if not isinstance(page_data, list) or not page_data:
            break
        for issue in page_data:
            if issue.get("pull_request"):
                continue
            issues.append(issue)
        page += 1
    return issues


def _label_name(label: Any) -> str:
    if isinstance(label, dict):
        return label.get("name", "")
    return str(label)


_INITIATIVE_LABELS = frozenset({
    "type:initiative", "type:epic", "type:umbrella",
    "initiative", "epic", "umbrella",
})


def build_from_issues(owner: str, repo: str) -> Dict:
    print(f"[issues-api] owner={owner} repo={repo}", flush=True)
    raw_issues = _fetch_all_issues(owner, repo)
    if not raw_issues:
        return _make_result(
            source="github-issues-empty",
            org=owner, repo=repo, project_title="",
            records=[], total_all=0, closed_all=0,
        )

    # 1. Try initiative labels
    initiative_issues = [
        i for i in raw_issues
        if any(_label_name(l).lower() in _INITIATIVE_LABELS for l in (i.get("labels") or []))
    ]
    if initiative_issues:
        print(f"[issues-api] Found {len(initiative_issues)} initiative-labeled issues", flush=True)
        return _build_from_initiative_issues(initiative_issues, raw_issues, owner, repo)

    # 2. Try milestones
    milestones: Dict[int, Dict] = {}
    for issue in raw_issues:
        ms = issue.get("milestone")
        if ms and ms.get("number"):
            ms_num = ms["number"]
            if ms_num not in milestones:
                milestones[ms_num] = {"milestone": ms, "issues": []}
            milestones[ms_num]["issues"].append(issue)
    if milestones:
        print(f"[issues-api] Grouping by {len(milestones)} milestones", flush=True)
        return _build_from_milestones(milestones, raw_issues, owner, repo)

    # 3. Title-prefix grouping (Kerrigan T1..T9 style)
    print("[issues-api] Falling back to title-prefix grouping", flush=True)
    return _build_from_title_prefix(raw_issues, owner, repo)


def _build_from_initiative_issues(
    initiative_issues: List[Dict], all_issues: List[Dict], owner: str, repo: str
) -> Dict:
    initiative_numbers = {i["number"] for i in initiative_issues}
    children_map: Dict[int, List[Dict]] = {i["number"]: [] for i in initiative_issues}
    unassigned: List[Dict] = []

    child_issues = [i for i in all_issues if i["number"] not in initiative_numbers]
    for child in child_issues:
        body = child.get("body") or ""
        assigned = False
        for init in initiative_issues:
            if f"#{init['number']}" in body:
                children_map[init["number"]].append(child)
                assigned = True
                break
        if not assigned:
            unassigned.append(child)

    records: List[Dict] = []
    for init in sorted(initiative_issues, key=lambda x: x["number"]):
        children = children_map.get(init["number"], [])
        labels = [{"name": _label_name(l)} for l in (init.get("labels") or [])]
        if children:
            total = len(children)
            closed = sum(1 for c in children if c.get("state") == "closed")
        else:
            total = 1
            closed = 1 if init.get("state") == "closed" else 0
        percent = round(closed / total * 100) if total > 0 else 0
        records.append({
            "number": init["number"],
            "title": init.get("title", ""),
            "url": init.get("html_url", ""),
            "status": "completed" if percent == 100 else ("in_progress" if percent > 0 else "not_started"),
            "labels": labels,
            "total": total,
            "closed": closed,
            "percent": percent,
            "children": [
                {
                    "number": c["number"],
                    "title": c.get("title", ""),
                    "state": c.get("state", "open"),
                    "url": c.get("html_url", ""),
                }
                for c in sorted(children, key=lambda x: x["number"])
            ],
        })

    all_child_items = [c for cs in children_map.values() for c in cs] + unassigned
    total_all = len(all_child_items) if all_child_items else len(initiative_issues)
    closed_all = (
        sum(1 for c in all_child_items if c.get("state") == "closed")
        if all_child_items
        else sum(1 for i in initiative_issues if i.get("state") == "closed")
    )

    return _make_result(
        source="github-issues-initiatives",
        org=owner, repo=repo, project_title="",
        records=records, total_all=total_all, closed_all=closed_all,
    )


def _build_from_milestones(
    milestones: Dict[int, Dict], all_issues: List[Dict], owner: str, repo: str
) -> Dict:
    records: List[Dict] = []
    no_ms = [i for i in all_issues if not i.get("milestone")]
    for ms_num, ms_data in sorted(milestones.items()):
        ms_issues = ms_data["issues"]
        total = len(ms_issues)
        closed = sum(1 for i in ms_issues if i.get("state") == "closed")
        percent = round(closed / total * 100) if total > 0 else 0
        ms = ms_data["milestone"]
        records.append({
            "number": ms.get("number", ms_num),
            "title": ms.get("title", f"Milestone {ms_num}"),
            "url": f"https://github.com/{owner}/{repo}/milestone/{ms_num}",
            "status": "completed" if percent == 100 else ("in_progress" if percent > 0 else "not_started"),
            "labels": [],
            "total": total,
            "closed": closed,
            "percent": percent,
            "children": [
                {
                    "number": i["number"],
                    "title": i.get("title", ""),
                    "state": i.get("state", "open"),
                    "url": i.get("html_url", ""),
                }
                for i in sorted(ms_issues, key=lambda x: x["number"])
            ],
        })
    total_all = sum(r["total"] for r in records) + len(no_ms)
    closed_all = sum(r["closed"] for r in records) + sum(1 for i in no_ms if i.get("state") == "closed")
    return _make_result(
        source="github-issues-milestones",
        org=owner, repo=repo, project_title="",
        records=records, total_all=total_all, closed_all=closed_all,
    )


def _build_from_title_prefix(issues: List[Dict], owner: str, repo: str) -> Dict:
    """Group by title prefix like T1, T2 ... TN; everything else → 'Other'."""
    groups: Dict[str, List[Dict]] = {}
    other: List[Dict] = []
    for issue in issues:
        m = re.match(r"^(T\d+)\b", issue.get("title", ""), re.IGNORECASE)
        if m:
            prefix = m.group(1).upper()
            groups.setdefault(prefix, []).append(issue)
        else:
            other.append(issue)

    records: List[Dict] = []
    for prefix in sorted(groups.keys(), key=lambda p: int(p[1:])):
        group_issues = sorted(groups[prefix], key=lambda x: x["number"])
        total = len(group_issues)
        closed = sum(1 for i in group_issues if i.get("state") == "closed")
        percent = round(closed / total * 100) if total > 0 else 0
        rep = group_issues[0]
        labels = [{"name": _label_name(l)} for l in (rep.get("labels") or [])]
        records.append({
            "number": rep["number"],
            "title": rep.get("title", prefix),
            "url": rep.get("html_url", ""),
            "status": "completed" if percent == 100 else ("in_progress" if percent > 0 else "not_started"),
            "labels": labels,
            "total": total,
            "closed": closed,
            "percent": percent,
            "children": [
                {
                    "number": i["number"],
                    "title": i.get("title", ""),
                    "state": i.get("state", "open"),
                    "url": i.get("html_url", ""),
                }
                for i in group_issues
            ],
        })

    if other:
        total_o = len(other)
        closed_o = sum(1 for i in other if i.get("state") == "closed")
        percent_o = round(closed_o / total_o * 100) if total_o > 0 else 0
        records.append({
            "number": 0,
            "title": "Other Tasks",
            "url": f"https://github.com/{owner}/{repo}/issues",
            "status": "completed" if percent_o == 100 else ("in_progress" if percent_o > 0 else "not_started"),
            "labels": [],
            "total": total_o,
            "closed": closed_o,
            "percent": percent_o,
            "children": [
                {
                    "number": i["number"],
                    "title": i.get("title", ""),
                    "state": i.get("state", "open"),
                    "url": i.get("html_url", ""),
                }
                for i in sorted(other, key=lambda x: x["number"])
            ],
        })

    total_all = sum(r["total"] for r in records)
    closed_all = sum(r["closed"] for r in records)
    return _make_result(
        source="github-issues-title-prefix",
        org=owner, repo=repo, project_title="",
        records=records, total_all=total_all, closed_all=closed_all,
    )


# ─── Result builder ───────────────────────────────────────────────────────────
def _make_result(
    *,
    source: str,
    org: str,
    repo: str,
    project_title: str,
    records: List[Dict],
    total_all: int,
    closed_all: int,
) -> Dict:
    percent = round(closed_all / total_all * 100) if total_all > 0 else 0
    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": source,
        "repo": f"{org}/{repo}",
        "project_title": project_title,
        "overall": {
            "total_initiatives": len([r for r in records if r.get("title") != "Other Tasks"]),
            "total_items": total_all,
            "closed_items": closed_all,
            "percent_complete": percent,
        },
        "initiatives": records,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    os.makedirs(OUTDIR, exist_ok=True)

    data: Optional[Dict] = None

    if PROJECT_NUMBER_STR:
        try:
            proj_num = int(PROJECT_NUMBER_STR)
            data = build_from_project(ORG, proj_num)
            print(f"[ok] Projects v2 source (project #{proj_num})", flush=True)
        except Exception as exc:
            print(
                f"[warn] Projects v2 failed ({exc}); falling back to Issues API",
                file=sys.stderr,
                flush=True,
            )

    if data is None:
        data = build_from_issues(ORG, REPO)
        print("[ok] Issues API source", flush=True)

    with open(OUTFILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    o = data["overall"]
    print(
        f"[ok] Wrote {OUTFILE}\n"
        f"     {o['closed_items']}/{o['total_items']} items closed "
        f"({o['percent_complete']}%) — {len(data['initiatives'])} initiatives",
        flush=True,
    )


if __name__ == "__main__":
    main()
