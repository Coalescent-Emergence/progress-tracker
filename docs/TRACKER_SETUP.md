# Setting Up the MVP Status Tracker

This guide explains how to enable and access the MVP Status Tracker for the Kerrigan project.

## Quick Setup (One-Time)

### Option 1: Automated Deployment (Recommended)

GitHub Pages is now configured to deploy automatically via GitHub Actions:

1. Go to the repository settings: https://github.com/Coalescent-Emergence/Kerrigan/settings/pages
2. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
3. The tracker will automatically deploy when changes are pushed to `main`

**Workflow**: The `.github/workflows/deploy-pages.yml` workflow handles deployment automatically.

### Option 2: Manual Deployment from Branch

Alternatively, you can use the traditional branch-based deployment:

1. Go to the repository settings: https://github.com/Coalescent-Emergence/Kerrigan/settings/pages
2. Under "Build and deployment":
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main` and folder `/docs`
3. Click "Save"
4. Wait 1-2 minutes for deployment

### Access the Tracker

Once GitHub Pages is enabled, the tracker will be available at:
**https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html**

Or use the root URL (redirects to tracker):
**https://coalescent-emergence.github.io/Kerrigan/**

## Alternative: Local Viewing

If you don't want to use GitHub Pages, you can view the tracker locally:

1. Open the file directly in your browser:
   ```bash
   open docs/mvp-tracker.html  # macOS
   # or
   xdg-open docs/mvp-tracker.html  # Linux
   # or
   start docs/mvp-tracker.html  # Windows
   ```

2. Or use a local web server:
   ```bash
   cd docs
   python3 -m http.server 8000
   # Then visit http://localhost:8000/mvp-tracker.html
   ```

## How It Works

The MVP tracker is a **static HTML file** that:
- Pulls live data from GitHub Issues API
- Requires no backend or database
- Auto-refreshes every 5 minutes
- Works with any web browser

### Technical Details

- **File**: `/docs/mvp-tracker.html`
- **API**: Uses GitHub's public REST API (`https://api.github.com/repos/Coalescent-Emergence/Kerrigan/issues`)
- **Updates**: Automatic - reflects real-time issue status
- **Hosting**: Can be served from GitHub Pages or any static hosting

## Updating Progress

The tracker automatically updates based on GitHub Issues:

1. **When you close an issue**: Task is marked as completed ✅
2. **When you open an issue**: Task appears in the tracker ⬜
3. **Labels matter**: Priority (p0, p1, p2) and effort (effort:S, effort:M, effort:L) are shown

### Issue Categorization

Issues are automatically sorted into milestones based on:
- Task number in title (T1-T3 → Month 1, T4-T6 → Month 2, T7-T9 → Month 3)
- Keywords in title (auth, audio, deploy, compliance, etc.)
- Labels (area:backend, area:platform, etc.)

## For Non-Technical Users

### Understanding the Dashboard

**Overview Section** (top):
- **Total Progress**: Overall percentage of MVP completion
- **Completed**: Number of finished tasks
- **In Progress**: Number of remaining tasks
- **Total Tasks**: All MVP tasks being tracked

**Progress Bar**:
- Visual representation of completion
- Shows exact number of completed vs. total tasks

**Milestones Section**:
- Groups tasks by phase (Month 1, 2, 3)
- Each milestone shows its status (Completed, In Progress, or Pending)
- Tasks within each milestone show:
  - ✅ = Done
  - ⬜ = Not done yet
  - Priority: How urgent (P0 = most urgent)
  - Effort: How much work (S = small, M = medium, L = large)

## Troubleshooting

### Tracker shows "Error Loading Data"

**Cause**: GitHub API rate limit (60 requests/hour for unauthenticated)

**Solution**: Wait an hour and refresh, or view issues directly at https://github.com/Coalescent-Emergence/Kerrigan/issues

### Tracker not updating

**Solutions**:
1. Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Wait for auto-refresh (occurs every 5 minutes)

### GitHub Pages not working

**Check**:
1. Verify GitHub Pages is enabled in repository settings
2. Ensure deployment branch is set to `main` and folder is `/docs`
3. Wait 1-2 minutes after enabling for initial deployment
4. Check deployment status at: https://github.com/Coalescent-Emergence/Kerrigan/deployments

## Customization

### Changing Milestone Definitions

Edit the `MVP_MILESTONES` object in `/docs/mvp-tracker.html`:

```javascript
const MVP_MILESTONES = {
    'Your Milestone Name': {
        description: 'Description here',
        weeks: 'Weeks X-Y'
    },
    // Add more milestones...
};
```

### Adjusting Categorization Logic

Modify the `categorizeIssue()` function in `/docs/mvp-tracker.html` to change how issues are assigned to milestones.

## Support

- **Technical Issues**: Create an issue at https://github.com/Coalescent-Emergence/Kerrigan/issues
- **Documentation**: See [MVP_STATUS.md](../MVP_STATUS.md) for more details
- **MVP Scope**: See [docs/mvp.md](./mvp.md) for full MVP requirements

---

**Quick Links**:
- [📊 Live Tracker](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html) (after GitHub Pages setup)
- [📋 GitHub Issues](https://github.com/Coalescent-Emergence/Kerrigan/issues)
- [📖 MVP Status](../MVP_STATUS.md)
