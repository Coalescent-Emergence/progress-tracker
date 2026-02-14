# Kerrigan MVP Status

**Last Updated**: Auto-generated from GitHub Issues

> **[📊 View Interactive Dashboard](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)** - For the best experience, use the live dashboard which auto-updates from GitHub Issues.

## Quick Summary

This document provides a snapshot of MVP progress. For real-time status, see the interactive dashboard above.

### Overall Progress

Based on GitHub Issues tracking:
- **Total MVP Tasks**: Tracked via GitHub Issues
- **Status**: See [Issues Board](https://github.com/Coalescent-Emergence/Kerrigan/issues)
- **Timeline**: 60 days (see sections below)

### How to Track Progress

1. **For Non-Technical Users**: Use the **[Interactive Dashboard](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)**
   - Visual progress bars and percentages
   - Color-coded task status
   - Organized by milestones
   - Auto-refreshes from GitHub

2. **For Technical Users**: View **[GitHub Issues](https://github.com/Coalescent-Emergence/Kerrigan/issues)**
   - Filter by labels (p0, p1, p2 for priority)
   - Track specific tasks and discussions
   - See detailed acceptance criteria

## MVP Milestones

### Phase 1: Foundation (Days 1-20)
**Goal**: Infrastructure & security setup

**Key Deliverables**:
- Infrastructure & security setup
- PicoClaw hardening (minimal)
- Basic frontend (single therapist, single session)
- Transcription engine (Whisper integration)
- Teams integration basics

**Progress**: Track in [Interactive Dashboard](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)

### Phase 2: Core Features (Days 21-50)
**Goal**: Transcription, real-time features, and hardening

**Key Deliverables**:
- Real-time transcript buffer + indexing
- Chat interface with transcript context
- Basic summarization
- Security hardening & encryption
- HIPAA audit logging & documentation
- Performance optimization & bug fixes

**Progress**: Track in [Interactive Dashboard](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)

### Phase 3: Launch (Days 51-60)
**Goal**: Testing, refinement, and deployment

**Key Deliverables**:
- Pilot testing (1-2 therapists)
- Bug fixes & final refinements
- Production deployment & launch

**Progress**: Track in [Interactive Dashboard](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)

## Understanding Task Labels

Tasks in the tracker use the following label system:

### Priority
- **P0** (Blocker): Critical path items that block other work
- **P1** (High): Important features needed for MVP
- **P2** (Medium): Nice-to-have features for MVP
- **P3** (Low): Post-MVP features

### Effort
- **S** (Small): < 4 hours, single file changes
- **M** (Medium): 1-2 days, multiple files
- **L** (Large): 3+ days, cross-cutting changes

### Status
- **✅ Completed**: Issue is closed, work is done
- **⬜ Pending**: Issue is open, work in progress or not started

## How Progress is Calculated

The tracker automatically:
1. Fetches all issues from the GitHub repository
2. Categorizes them by milestone based on labels and task numbers
3. Calculates completion percentage: `(Closed Issues / Total Issues) × 100`
4. Updates every 5 minutes when viewing the interactive dashboard

## For Stakeholders

**Want to know where we are?**
- Visit the **[Interactive Dashboard](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)**
- Look at the overall progress percentage
- Check which milestone we're currently in
- See how many tasks are completed vs. remaining

**Have questions?**
- Review [MVP Scope Documentation](./docs/mvp.md) for detailed requirements
- Check [Roadmap](./docs/roadmap.md) for long-term planning
- See [Architecture](./docs/architecture.md) for technical design

## Technical Details

### How It Works

The MVP tracker is built as a static HTML page that:
- Uses GitHub's public API to fetch issue data
- Requires no backend infrastructure
- Can be hosted on GitHub Pages
- Auto-categorizes issues into milestones
- Provides a clean, non-technical friendly interface

### File Location
- Interactive Dashboard: `/docs/mvp-tracker.html`
- This Document: `/MVP_STATUS.md`

### Updating

The tracker updates automatically - no manual intervention needed:
- Dashboard pulls live data from GitHub Issues API
- Progress reflects real issue status (open/closed)
- New issues are automatically included
- Closed issues are marked as completed

---

**Quick Links**:
- [📊 Interactive Dashboard](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)
- [📋 GitHub Issues](https://github.com/Coalescent-Emergence/Kerrigan/issues)
- [📖 MVP Documentation](./docs/mvp.md)
- [🗺️ Roadmap](./docs/roadmap.md)
