# Kerrigan Documentation & MVP Tracker

This directory contains the Kerrigan project documentation and the MVP Progress Tracker.

## 📊 MVP Progress Tracker

**[View Live Tracker →](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)**

The MVP tracker is a non-technical friendly dashboard that shows real-time progress on all MVP tasks.

### Files
- **`mvp-tracker.html`** - Interactive dashboard (main tracker page)
- **`index.html`** - Redirect page to the tracker
- **`_config.yml`** - Jekyll/GitHub Pages configuration

### GitHub Pages Setup

This site is automatically deployed to GitHub Pages via GitHub Actions:

**Workflow**: `.github/workflows/deploy-pages.yml`
- Triggers on push to `main` branch when files in `/docs` change
- Automatically deploys the tracker to GitHub Pages
- No manual intervention needed

**Setup Steps**:
1. Go to [Repository Settings → Pages](https://github.com/Coalescent-Emergence/Kerrigan/settings/pages)
2. Under "Build and deployment" → **Source**: Select "GitHub Actions"
3. Save and wait for deployment

**Access**:
- Tracker: https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html
- Redirect: https://coalescent-emergence.github.io/Kerrigan/

### Local Development

To test the tracker locally:

```bash
cd docs
python3 -m http.server 8000
# Visit http://localhost:8000/mvp-tracker.html
```

## 📖 Documentation

### Project Documentation
- **`mvp.md`** - MVP scope and requirements
- **`architecture.md`** - System architecture and design
- **`api.md`** - API documentation
- **`roadmap.md`** - Product roadmap
- **`tech-stack.md`** - Technology choices
- **`development.md`** - Development guidelines
- **`metrics.md`** - Success metrics and KPIs

### Setup & Configuration
- **`TRACKER_SETUP.md`** - Detailed tracker setup instructions
- **`decisions/`** - Architecture Decision Records (ADRs)

---

**Note**: The MVP tracker automatically pulls data from GitHub Issues API. No manual updates needed - progress is always current!
