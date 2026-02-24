#!/usr/bin/env node
// fetch-progress.js
// Fetches ProjectV2 issues from GitHub and writes to progress-static/progress.json

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const OWNER = 'Coalescent-Emergence';
const REPO = 'mvp-control-plane';
const PROJECT_NUMBER = 1;
const OUT_PATH = path.join(__dirname, 'progress-static', 'progress.json');

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
if (!GITHUB_TOKEN) {
  console.error('GITHUB_TOKEN not set');
  process.exit(1);
}

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

async function main() {
  const res = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${GITHUB_TOKEN}`
    },
    body: JSON.stringify({
      query,
      variables: {
        owner: OWNER,
        repo: REPO,
        projectNumber: PROJECT_NUMBER,
        first: 100
      }
    })
  });
  if (!res.ok) {
    console.error('GitHub API error:', res.status, await res.text());
    process.exit(1);
  }
  const data = await res.json();
  const issues = data?.data?.repository?.projectV2?.items?.nodes || [];
  fs.writeFileSync(OUT_PATH, JSON.stringify(issues, null, 2));
  console.log(`Wrote ${issues.length} issues to ${OUT_PATH}`);
}

main().catch(e => { console.error(e); process.exit(1); });
