# progress-tracker

MVP progress tracker - Deployed to GitHub Pages

This repository automatically syncs and deploys the MVP tracker from the source repository to GitHub Pages.

## Quick Links

- 🌐 **Live Site**: https://coalescent-emergence.github.io/progress-tracker/
- 📋 **Setup Guide**: See [SETUP.md](SETUP.md) for configuration instructions
- 💡 **Recommendations**: See [RECOMMENDATIONS.md](RECOMMENDATIONS.md) for improvement suggestions
- 🔄 **Workflow Status**: Check the [Actions tab](../../actions) for deployment status

## How it Works

This repository uses GitHub Actions to:
1. Pull MVP tracker files from the source repository (Kerrigan) using sparse checkout
2. Generate a JSON file of issues from the GitHub API
3. Deploy them to GitHub Pages automatically

**Note**: Access to the private Kerrigan repository requires configuring a `KERRIGAN_ACCESS_TOKEN` secret. See [SETUP.md](SETUP.md) for detailed setup instructions.

## Label Conventions

The tracker categorizes issues based on labels:
- **Priority**: `p0` (critical), `p1` (high), `p2` (medium), `p3` (low)
- **Effort**: `effort:S` (small), `effort:M` (medium), `effort:L` (large)
- **Type**: `type:feature`, `type:infra`, etc.

Issues are automatically organized into phases based on their titles and labels.
