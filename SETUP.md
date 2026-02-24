# Progress Tracker — Setup & Operations

This repository hosts the MVP launch-readiness dashboard at
`https://coalescent-emergence.github.io/progress-tracker/`.

Progress data is fetched automatically from the GitHub API (Projects v2 preferred, Issues API
fallback) and the dashboard is rebuilt on every change. No manual updates needed once configured.

---

## Quick-Start Checklist

- [ ] Configure GitHub Pages (see §1)
- [ ] Set workflow permissions (see §2)
- [ ] Add `TRACKER_DATA_TOKEN` secret (see §3)
- [ ] Set `GH_PROJECT_NUMBER` variable if using Projects v2 (see §4)
- [ ] Configure the control-plane relay (see §5)
- [ ] Install trigger workflow in Kerrigan (see §6)
- [ ] Run the first manual deploy (see §7)

---

## 1. Configure GitHub Pages

1. Go to **Settings → Pages**
2. Under "Build and deployment" → Source: **GitHub Actions**
3. Save

## 2. Workflow Permissions

1. **Settings → Actions → General → Workflow permissions**
2. Select **"Read and write permissions"**
3. Check **"Allow GitHub Actions to create and approve pull requests"**
4. Save

## 3. TRACKER_DATA_TOKEN (required for private repos)

Create a PAT with the following scopes, then add it as a repository secret:

| Scope         | Why                                        |
|---------------|--------------------------------------------|
| `repo`        | Read issues from private Kerrigan repo     |
| `read:org`    | Needed for Projects v2 GraphQL             |
| `read:project`| Read Projects v2 board items               |

**Creating the secret:**

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate token with scopes above; set 1-year expiration
3. This repo → Settings → Secrets and variables → Actions → **New repository secret**
   - Name: `TRACKER_DATA_TOKEN`
   - Value: the token

> **Note:** If this secret is not set, the workflow falls back to `GITHUB_TOKEN`. That only works
> if your org policy allows the default token to access other organisation repos.

## 4. GH_PROJECT_NUMBER (optional but recommended)

Setting this enables **GitHub Projects v2** mode, which provides the richest data:

1. Find your project number: go to `https://github.com/orgs/Coalescent-Emergence/projects`, open
   the project — the URL contains `/projects/N`.
2. This repo → Settings → Secrets and variables → Actions → Variables tab →
   **New repository variable**
   - Name: `GH_PROJECT_NUMBER`
   - Value: `<N>` (the number from the URL)

**Without this variable** the generator falls back to Issues API with milestone or title-prefix grouping
(works with the existing Kerrigan T1–T9 issue naming convention).

### Required project fields for full Projects v2 support

| Field Name   | Type          | Values used by generator            |
|--------------|---------------|-------------------------------------|
| `Item Type`  | Single Select | `initiative`, `delivery`            |
| `Initiative` | Text / Number | The initiative issue number or title |

Run `mvp-control-plane/scripts/bootstrap-project-schema.sh` to create these fields.

## 5. Control-Plane Relay (mvp-control-plane)

The relay workflow at `mvp-control-plane/.github/workflows/relay-progress-update.yml`
forwards `progress-update-request` dispatches to this repo.

Add a secret to **mvp-control-plane**:
- Name: `TRACKER_DISPATCH_TOKEN`
- Value: PAT with `repo` scope on `Coalescent-Emergence/progress-tracker`

## 6. Kerrigan Trigger Workflow

The workflow at `Kerrigan/.github/workflows/trigger-progress-tracker.yml` fires on issue events
and dispatches to mvp-control-plane.

Add a secret to **Kerrigan**:
- Name: `MVPCP_DISPATCH_TOKEN`
- Value: PAT with `repo` scope on `Coalescent-Emergence/mvp-control-plane`

For adding more repos, see `mvp-control-plane/docs/guides/progress-tracker-integration.md`.

## 7. First Deploy

Trigger a manual run:
**Actions → Deploy MVP Tracker to GitHub Pages → Run workflow**

After ~1–2 minutes the dashboard will be live at:
`https://coalescent-emergence.github.io/progress-tracker/mvp-tracker.html`

---

## Event Flow (summary)

```
Kerrigan issue event
  → trigger-progress-tracker.yml (Kerrigan)
  → mvp-control-plane relay-progress-update.yml
  → progress-tracker deploy.yml
  → generate_mvp_data.py (GitHub API)
  → docs/data/mvp-data.json committed
  → GitHub Pages deploy
  → dashboard live
```

Update also fires automatically on the daily schedule (`0 6 * * *` UTC).

---

## Data File Schema

`docs/data/mvp-data.json` is the generated snapshot. Shape:

```json
{
  "generated_at": "2026-02-18T06:00:00Z",
  "source": "github-issues-title-prefix",
  "repo": "Coalescent-Emergence/Kerrigan",
  "project_title": "",
  "overall": {
    "total_initiatives": 9,
    "total_items": 9,
    "closed_items": 1,
    "percent_complete": 11
  },
  "initiatives": [
    {
      "number": 4,
      "title": "T1 — Capture Verification (capture shim)",
      "url": "https://github.com/Coalescent-Emergence/Kerrigan/issues/4",
      "status": "completed",
      "labels": [{"name": "p1"}, {"name": "type:feature"}],
      "total": 1,
      "closed": 1,
      "percent": 100,
      "children": [
        {"number": 4, "title": "T1 — ...", "state": "closed", "url": "..."}
      ]
    }
  ]
}
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Workflow fails: "Resource not accessible" | Permissions not set to read/write | See §2 |
| No data / all 0% | Token lacks `repo` or `read:project` scope | See §3 |
| Generator falls back to Issues API despite project set | `GH_PROJECT_NUMBER` not set or wrong | See §4 |
| Dispatch from Kerrigan not firing | `MVPCP_DISPATCH_TOKEN` secret missing | See §6 |
| Dashboard shows stale data | Browser cache — add `?v=` param or hard-refresh | n/a |
