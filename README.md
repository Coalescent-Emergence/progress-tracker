# progress-tracker

MVP progress tracker - Deployed to GitHub Pages

This repository automatically syncs and deploys the MVP tracker from the source repository to GitHub Pages.

## Quick Links

- 🌐 **Live Site**: https://coalescent-emergence.github.io/progress-tracker/
- 📋 **Setup Guide**: See [SETUP.md](SETUP.md) for configuration instructions
- 🔄 **Workflow Status**: Check the [Actions tab](../../actions) for deployment status

## How it Works

This repository uses GitHub Actions to:
1. Pull MVP tracker files from the source repository (Kerrigan) using sparse checkout
2. Deploy them to GitHub Pages automatically

**Note**: Access to the private Kerrigan repository requires configuring a `KERRIGAN_ACCESS_TOKEN` secret. See [SETUP.md](SETUP.md) for detailed setup instructions.
