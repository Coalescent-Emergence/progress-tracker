# Kerrigan Roadmap

**Consolidated (detailed-first)**

Last Updated: February 12, 2026

## Executive Summary

Kerrigan is a privacy-first conversation intelligence platform for healthcare, focused on HIPAA-compliant transcription, summarization, and in-session assistance for therapists and clinicians. This roadmap consolidates the short- and medium-term release plan, prioritizing the detailed roadmap where conflicts exist.

- Project status: Planning → MVP development
- MVP timeline: ~3 months (Months 1–3) targeting Q2 2026
- High-level goal: Authenticated audio upload → reliable transcription pipeline → audit logging

---

## One-Page Snapshot

- Target MVP duration: 12–16 weeks (3 months)
- Team (planning): ~6 FTE for full product; solo-dev MVP is acceptable for initial build
- Key MVP deliverables: Authentication, audio upload, Whisper-STT integration, job lifecycle, audit logs
- Success metrics (MVP): 10 concurrent users, p95 API latency <100ms, >80% test coverage, zero critical vulnerabilities

---

## Phases & Timeline

Phase 1 — Foundation & Security (Weeks 1-10 / Months 0-1)
- Infrastructure (DB, S3, local dev stack)
- Auth: JWT-based auth, password hashing, refresh tokens
- Core API/handlers and CI/CD pipeline
- Docker Compose local environment and migrations
- Gate: Security checklist and readiness for integration

Phase 2 — Core Features (Weeks 11-22 / Months 1-2)
- Transcription engine integration (Whisper-STT batch)
- Audio upload endpoints, job creation, status polling
- Transcription storage and retrieval
- Audit logging for PHI access
- Gate: End-to-end integration tests successful

Phase 3 — Hardening & Integration (Weeks 23-30 / Months 2-3)
- Admin APIs (user management), password reset, email verification (V1 scope)
- Monitoring, metrics (Prometheus), error tracking (Sentry)
- Perform security and compliance hardening
- Gate: Security hardening review

Phase 4 — Launch Prep & Pilot (Weeks 31-36 / Months 3+)
- QA and load testing
- Documentation, onboarding materials for pilot sites
- Beta pilot program with 5–10 sites
- Gate: Launch approval and BAA in place

Notes: The detailed roadmap recommends a 28–36 week program for a full product with a 6–8 FTE team; the MVP timeline here represents the minimal path for early validation.

---

## Release Targets and Key Features

### MVP (Months 1–3) — Foundation (Must-haves)
- User registration and JWT authentication (HS256 for MVP)
- Audio upload via REST API (multipart), supported formats WAV/MP3/FLAC/M4A/OGG
- Whisper-STT batch integration for transcription processing
- Job orchestration and status tracking (pending/processing/completed/failed)
- Transcription retrieval (JSON, plain text; SRT/VTT planned)
- HIPAA-compliant audit logging (audit_logs table, retention policy)
- Docker Compose local deployment
- CI: Lint, tests, coverage enforcement (>80%), security scan

### V1.0 (Months 4–6) — Production Hardening
- Admin API (user & system management)
- Password reset and email verification
- Role-Based Access Control (RBAC): Admin, Provider, Viewer
- API versioning strategy (e.g., `/api/v1/`)
- Kubernetes deployment (Helm chart), read replicas, backups
- Observability: Prometheus metrics, Grafana dashboards, tracing (OpenTelemetry)
- Success metrics: 100 concurrent users, p95 <50ms, 99.9% uptime

### V1.1 (Months 7–9) — Real-Time Features
- WebSocket streaming for live transcription
- Partial/intermediate transcription results streaming
- Real-time dashboard for job and system monitoring
- Transcription editing and custom vocabularies
- Infrastructure: Redis for sessions/WS, HPA for scaling
- Success metrics: <2s first partial result, 500 concurrent WS connections

### V2.0 (Months 10–12) — Enterprise Features
- Organization accounts (multi-tenancy) and team collaboration
- Advanced semantic search (full-text + vector search)
- Export formats (PDF, DOCX, SRT) and webhooks
- API keys for programmatic access; multi-region deployment
- Database sharding or distributed Postgres options

### V2.1+ (Year 2) — AI & Intelligence
- Speaker diarization, sentiment analysis, summarization, medical entity extraction
- Local/hardened LLM (PicoClaw) for clinical safety or fallback to cloud LLM
- Model-serving infra (KServe/TorchServe) and GPU clusters

---

## Prioritization Framework

Features prioritized with RICE: Reach × Impact × Confidence / Effort.
Use RICE for backlog prioritization and to decide what moves from Tier 2 → Tier 1.

---

## Dependencies & Risks (Consolidated)

- Whisper-STT availability: retry and queueing mitigations; SLA expected
- PostgreSQL single point: add read replicas and backups in V1.0
- S3 vendor lock-in: use S3-compatible APIs (MinIO dev) for portability
- Compliance risk: engage counsel early, enforce audit logging and retention
- Scope creep: phase gates and strict change control

Top risks: Transcription accuracy (<95%), PicoClaw hardening delays, Teams API limits, HIPAA audit failures, scope creep — mitigations and owners included in detailed roadmap.

---

## Technical Debt & Maintenance

Ongoing work:
- Weekly dependency updates and vulnerability scans
- Monthly performance reviews and DB optimization
- Maintain ADRs and documentation
- Quarterly refactor sprints (15% allocation)

---

## Success Metrics & KPIs (Consolidated)

Product & Usage
- DAU/WAU targets (MVP: DAU 5 / WAU 10)
- Transcriptions per user (MVP ~3/week)

System
- API latency: p50/p95/p99 targets per endpoint (see `docs/metrics.md`)
- Uptime targets: MVP 99% → V1.0 99.9%

Security & Compliance
- Audit log coverage: 100% of PHI access
- Retention: MVP 90 days; production 7 years (policy)

Code Quality
- Coverage target: ≥80% (enforced in CI)
- Cyclomatic complexity limits and linting via `golangci-lint`

---

## Budget & Resource Estimates (From detailed roadmap)

Rough estimate for full product (6 FTE over ~8 months): $1.0–1.2M (includes infra, audits, legal). For MVP with solo dev, cost is significantly lower—detailed budgetary planning required if pursuing hiring.

---

## Deferred / Rejected Items

Deferred (not for next 12 months): Mobile apps, on-premise, video transcription, live translation.
Rejected: Blockchain for audit logs, GraphQL (for now), serverless for long-running jobs.

---

## Launch & Pilot Plan

- Pilot cohort: onboard 5–10 pilot sites during Phase 4
- Pilot acceptance criteria: functionality, security audit results, therapist satisfaction ≥4/5
- Go/No-Go gate: BAA signed, zero critical security items

---

## Next Actions (Immediate)

1. Finalize MVP acceptance criteria and owners
2. Staff/assign critical roles (Tech Lead, PM, Compliance contact)
3. Begin Phase 1 tasks: infra, auth, local dev stack
4. Use AI agents to decompose top-priority stories (`ai:clarify`, `ai:decompose`)

---

## AI Agent Assistance

- Use `ai:clarify` to refine feature ideas into MVP stories
- Use `ai:decompose` for task breakdowns and file-level suggestions
- Use Architecture Guardian on PRs to flag ADR conflicts

---

**Document History**: Consolidated from `roadmap_basic.md` and `roadmap_detailed.md` (detailed version preferred where conflicting).  
**Maintainer**: Kerrigan tech lead (TBD)
