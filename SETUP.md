# GitHub Pages Deployment Setup

This repository automatically syncs the MVP tracker from the source repository and deploys it to GitHub Pages.

## Initial Setup

### 1. Configure GitHub Pages

1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: **GitHub Actions**
3. Save the settings

### 2. Create Personal Access Token (PAT)

To allow this repository to pull files from the private Kerrigan repository, you need to create a Personal Access Token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "Progress Tracker Sync"
4. Set expiration as needed
5. Select the following scopes:
   - `repo` (Full control of private repositories)
6. Click "Generate token"
7. **Copy the token immediately** (you won't be able to see it again)

### 3. Add the Token as a Repository Secret

1. Go to this repository's Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `SOURCE_REPO_TOKEN`
4. Value: Paste the PAT you created
5. Click "Add secret"

### 4. Configure Permissions

1. Go to repository Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click "Save"

## Workflow Triggers

The deployment workflow runs in the following scenarios:

1. **Manual trigger**: Go to Actions → Deploy MVP Tracker to GitHub Pages → Run workflow
2. **Scheduled**: Automatically runs daily at midnight UTC
3. **Repository dispatch**: Can be triggered from the source repository when changes are made

## Triggering from Source Repository

To set up automatic deployment when the MVP tracker is updated in the Kerrigan repository:

1. In the Kerrigan repository, create a workflow file `.github/workflows/trigger-deploy.yml`:

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
            -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
            https://api.github.com/repos/Coalescent-Emergence/progress-tracker/dispatches \
            -d '{"event_type":"deploy"}'
```

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
- Verify that `SOURCE_REPO_TOKEN` secret is set correctly
- Ensure the PAT has `repo` scope
- Check that the PAT hasn't expired

### No files are synced
- Check the paths in the workflow file match the actual location in the source repository
- Review the workflow logs to see what files were found

### Deploy succeeds but site shows 404
- Verify that `docs/index.html` exists after sync
- Check GitHub Pages settings are configured correctly
- Wait a few minutes for the deployment to propagate
