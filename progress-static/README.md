# MVP Progress Tracker Static Page

This static page fetches and displays MVP progress by parsing ProjectV2 issues from the mvp-control-plane repository.

## Usage

1. Open `index.html` in your browser.
2. You must provide a GitHub personal access token (with `repo` and `project` read access) in your browser's localStorage:

   Open the browser console and run:
   ```js
   localStorage.setItem('GITHUB_TOKEN', 'YOUR_TOKEN_HERE');
   ```
   Then refresh the page.

3. The page will show a summary and list of issues from the MVP ProjectV2 board.

## Deployment

- You can deploy this folder (`progress-static/`) to any static web host (GitHub Pages, Netlify, Vercel, S3, etc).
- No server-side code is required.

## Security Note

- Your GitHub token is stored only in your browser's localStorage and never sent to any server except GitHub.
- For public deployments, consider using a backend proxy or GitHub App for secure API access.

---

**Files:**
- `index.html` — Main static page
- `progress.js` — Fetches and renders progress
