# GitHub Pages Deployment Setup

This repository automatically syncs the MVP tracker from the source repository and deploys it to GitHub Pages.

## Initial Setup

### 1. Configure GitHub Pages

1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: **GitHub Actions**
3. Save the settings

### 2. Configure Permissions

1. Go to repository Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click "Save"

### 3. Configure Access to Kerrigan Repository

Since the Kerrigan repository is private, you need to provide authentication to access it:

1. Create a Personal Access Token (PAT):
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a descriptive name like "Progress Tracker - Kerrigan Access"
   - Select the `repo` scope (for full repository access)
   - Set an appropriate expiration (90 days recommended for security)
   - Click "Generate token"
   - **Important**: Copy the token immediately - you won't be able to see it again!

2. Add the token as a repository secret:
   - Go to this repository's Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `KERRIGAN_ACCESS_TOKEN`
   - Value: Paste the PAT you just created
   - Click "Add secret"

**Note**: The workflow will fall back to using `GITHUB_TOKEN` if `KERRIGAN_ACCESS_TOKEN` is not set, but this will only work if your organization allows the Actions `GITHUB_TOKEN` to access other organization repositories. If you see "Not Found" errors when trying to checkout the Kerrigan repository, you must configure the `KERRIGAN_ACCESS_TOKEN` secret.

## Workflow Triggers

The deployment workflow runs in the following scenarios:

1. **Manual trigger**: Go to Actions → Deploy MVP Tracker to GitHub Pages → Run workflow
2. **Scheduled**: Automatically runs daily at midnight UTC
3. **Repository dispatch**: Can be triggered from the source repository when changes are made

## Triggering from Source Repository

To set up automatic deployment when the MVP tracker is updated in the Kerrigan repository:

1. Create a Personal Access Token (PAT) with `repo` scope for triggering workflows
2. Add it as a secret named `TRIGGER_TOKEN` in the Kerrigan repository
3. In the Kerrigan repository, create a workflow file `.github/workflows/trigger-deploy.yml`:

```yaml
name: Trigger Progress Tracker Deployment

on:
  push:
    paths:
      - 'mvp-tracker/**'  # Adjust path to where MVP tracker files are located
      - 'progress-tracker/**'
  workflow_dispatch:

jobs:
  trigger-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger deployment in progress-tracker repository
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Authorization: token ${{ secrets.TRIGGER_TOKEN }}" \
            https://api.github.com/repos/Coalescent-Emergence/progress-tracker/dispatches \
            -d '{"event_type":"deploy"}'
```

**Note**: The `TRIGGER_TOKEN` must be a Personal Access Token with `repo` scope. The default `GITHUB_TOKEN` cannot trigger workflows in other repositories.

## File Structure

After sync, the repository will have:
- `docs/` - Contains the MVP tracker files deployed to GitHub Pages
- `.github/workflows/deploy.yml` - The deployment workflow

## Customizing File Paths

If the MVP tracker files are in a different location in the Kerrigan repository, edit `.github/workflows/deploy.yml` and update the paths in the "Copy MVP tracker files" step.

Common locations to check:
- `mvp-tracker/`
- `docs/mvp-tracker/`
- `progress-tracker/`
- `mvp-tracker.html` (single file)

## Viewing the Deployed Site

Once deployed, the site will be available at:
`https://coalescent-emergence.github.io/progress-tracker/`

## Troubleshooting

### Workflow fails with "Resource not accessible by integration"
- Check that workflow permissions are set to "Read and write permissions"
- Verify that Pages is set to deploy from "GitHub Actions"

### Sync fails with authentication errors
- Verify that the repository has proper org permissions to access Kerrigan
- Check workflow permissions are set to "Read and write permissions"

### No files are synced
- Check the paths in the workflow file match the actual location in the source repository
- Review the workflow logs to see what files were found

### Deploy succeeds but site shows 404
- Verify that `docs/index.html` exists after sync
- Check GitHub Pages settings are configured correctly
- Wait a few minutes for the deployment to propagate

## Sparse checkout from Kerrigan (implementation notes)

This repository's deployment workflow uses a git sparse-checkout to fetch only the minimal static files required for the MVP tracker from the private `Coalescent-Emergence/Kerrigan` repository.

- **Authentication**: The workflow uses `KERRIGAN_ACCESS_TOKEN` (a Personal Access Token stored as a repository secret) to authenticate to the Kerrigan repo. If this secret is not configured, it falls back to `GITHUB_TOKEN`, which will only work if your organization allows the Actions token to access other organization repositories. See [Configure Access to Kerrigan Repository](#3-configure-access-to-kerrigan-repository) for setup instructions.
- **Whitelist**: only these paths are fetched and copied into `docs/`:
  - `docs/mvp-tracker.html`
  - `docs/index.html`
  - `docs/_config.yml`
  - `MVP_STATUS.md`
  - `docs/TRACKER_SETUP.md`
  - `docs/README.md`
  - `docs/mvp.md`
  - `GITHUB_PAGES_SETUP.md`
  - `README.md`

- **Allowed extensions copied**: `.html`, `.css`, `.js`, `.svg`, `.png`, `.jpg`, `.jpeg`, `.webp`, `.woff2`, `.ico`, `.json`, `.md`.

- **Security**: the workflow explicitly rejects any files outside the whitelist and will skip files with disallowed extensions. Server-side code, `.env*` files, private keys, or other sensitive content are never fetched or copied.

If you need to change the sparse paths, edit `.github/workflows/deploy.yml` and update the `.git/info/sparse-checkout` entries accordingly.
