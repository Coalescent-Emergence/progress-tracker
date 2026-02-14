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
