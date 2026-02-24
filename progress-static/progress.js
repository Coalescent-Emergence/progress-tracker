// progress.js
// Fetches and displays MVP progress from GitHub ProjectV2 issues

const OWNER = 'Coalescent-Emergence';
const REPO = 'mvp-control-plane';
const PROJECT_NUMBER = 1; // Adjust if not Project #1

async function fetchProjectV2Issues() {
  // GitHub GraphQL API endpoint
  const endpoint = 'https://api.github.com/graphql';
  // You must provide a GitHub token with read access to the repo as GITHUB_TOKEN in localStorage
  const token = localStorage.getItem('GITHUB_TOKEN');
  if (!token) {
    document.getElementById('progress-summary').textContent = 'GitHub token not found. Please set GITHUB_TOKEN in localStorage.';
    return null;
  }

  // GraphQL query for ProjectV2 items
  const query = `
    query($owner: String!, $repo: String!, $projectNumber: Int!, $first: Int!) {
      repository(owner: $owner, name: $repo) {
        projectV2(number: $projectNumber) {
          items(first: $first) {
            nodes {
              content {
                ... on Issue {
                  number
                  title
                  url
                  state
                  labels(first: 10) { nodes { name } }
                }
              }
            }
          }
        }
      }
    }
  `;

  const variables = {
    owner: OWNER,
    repo: REPO,
    projectNumber: PROJECT_NUMBER,
    first: 100
  };

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ query, variables })
  });

  if (!res.ok) {
    document.getElementById('progress-summary').textContent = 'Failed to fetch project data.';
    return null;
  }
  const data = await res.json();
  return data?.data?.repository?.projectV2?.items?.nodes || [];
}

function summarizeProgress(issues) {
  const total = issues.length;
  const closed = issues.filter(i => i.content && i.content.state === 'CLOSED').length;
  return { total, closed, percent: total ? Math.round((closed / total) * 100) : 0 };
}

function renderProgress(issues) {
  const summary = summarizeProgress(issues);
  document.getElementById('progress-summary').innerHTML =
    `<strong>${summary.closed}</strong> of <strong>${summary.total}</strong> issues closed (<strong>${summary.percent}%</strong> complete)`;

  const list = document.getElementById('issue-list');
  list.innerHTML = '';
  issues.forEach(i => {
    if (!i.content) return;
    const li = document.createElement('li');
    li.className = 'issue';
    li.innerHTML = `
      <a href="${i.content.url}" target="_blank">#${i.content.number}: ${i.content.title}</a>
      <span class="status-${i.content.state.toLowerCase()}" style="float:right;">${i.content.state}</span>
      <div>Labels: ${(i.content.labels.nodes.map(l => l.name).join(', ') || 'None')}</div>
    `;
    list.appendChild(li);
  });
}

async function main() {
  const issues = await fetchProjectV2Issues();
  if (issues) renderProgress(issues);
}

main();
