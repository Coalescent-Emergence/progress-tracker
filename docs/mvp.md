# Kerrigan MVP Scope

**Last Updated**: February 12, 2026  
**Target Launch**: ~3 months from start  
**Team**: Solo developer + AI agents

---

## 📊 Track Our Progress

**[View Live MVP Progress Dashboard →](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)**

See real-time updates on all MVP tasks, milestones, and completion status. The dashboard automatically tracks progress from GitHub Issues and provides:
- Overall completion percentage
- Visual progress indicators
- Task breakdown by milestone
- Priority and effort estimates

For a quick text summary, see [MVP_STATUS.md](../MVP_STATUS.md)

---

## MVP Definition

Kerrigan's MVP is the **minimum backend infrastructure** needed to support basic healthcare transcription workflow:

1. User can register and authenticate
2. User can upload audio files
3. System orchestrates audio transcription via Whisper service
4. User can retrieve transcription results
5. All actions are audit logged for SOC2/HIPAA compliance

## Success Criteria

### Functional

- [ ] User registration and login working (email/password, JWT-based)
- [ ] Audio upload endpoint accepts common formats (.mp3, .wav, .m4a)
- [ ] Backend successfully submits jobs to Whisper-STT service
- [ ] Transcription results retrievable via API
- [ ] Basic error handling (invalid auth, file format errors, service timeouts)

### Non-Functional

- [ ] API latency < 100ms p95 for authenticated requests (excluding transcription)
- [ ] Test coverage > 80% for core business logic
- [ ] Audit logs capture all authentication and data access events
- [ ] Can handle 10 concurrent users without degradation
- [ ] Zero critical security vulnerabilities (per `go list -m -u all` and manual review)

### Operational

- [ ] Docker deployment working with docker-compose
- [ ] Database migrations automated
- [ ] Basic monitoring/logging in place (stdout logs, structured JSON)
- [ ] Can deploy new version with < 5 minutes downtime (manual for MVP)

## Out of Scope for MVP

**Explicitly deferred to post-MVP**:

- ❌ Password reset flow (users contact admin for password reset)
- ❌ Email verification (assume trusted user base initially)
- ❌ Real-time streaming transcription (batch processing only)
- ❌ Multi-factor authentication
- ❌ Role-based access control (RBAC) - all users have same permissions
- ❌ Advanced search/filtering of transcriptions
- ❌ Webhooks or event notifications
- ❌ API versioning (v1 implicit, no versioning yet)
- ❌ GraphQL endpoint (REST only)
- ❌ Auto-scaling infrastructure
- ❌ Comprehensive monitoring (Prometheus/Grafana)

## 3-Month Milestone Breakdown

### Month 1: Foundation (Weeks 1-4)

**Goal**: Authentication and core infrastructure

- Week 1: Project setup, database schema, migrations
- Week 2: User registration and login (JWT authentication)
- Week 3: JWT middleware, protected endpoint pattern, audit logging
- Week 4: Integration tests for auth flow, CI/CD pipeline

**Deliverable**: Users can register, login, and access protected `/api/health` endpoint

### Month 2: Core Functionality (Weeks 5-8)

**Goal**: Audio processing workflow

- Week 5: Audio upload endpoint, S3 storage integration
- Week 6: Whisper-STT service integration (job submission)
- Week 7: Job status polling, transcription result retrieval
- Week 8: Error handling, retry logic, integration tests

**Deliverable**: End-to-end audio upload → transcription → retrieval working

### Month 3: Polish & Launch Prep (Weeks 9-12)

**Goal**: Production readiness

- Week 9: Performance optimization (database indexing, caching)
- Week 10: Security audit, dependency updates, test coverage gaps
- Week 11: Docker deployment, database backup strategy
- Week 12: Documentation, deployment guide, final testing

**Deliverable**: Production-ready Kerrigan backend deployed and accessible to UI

## MVP User Stories

| ID | Story | Priority | Complexity | Owner |
|----|-------|----------|------------|-------|
| AUTH-1 | User can register with email/password | P0 | M | Solo dev |
| AUTH-2 | User can login and receive JWT | P0 | M | Solo dev |
| AUTH-3 | User can refresh JWT using refresh token | P0 | S | Solo dev |
| UPLOAD-1 | User can upload audio file via API | P0 | M | Solo dev |
| UPLOAD-2 | System validates audio format and size | P0 | S | Solo dev |
| TRANS-1 | System submits transcription job to Whisper | P0 | M | Solo dev |
| TRANS-2 | User can check transcription job status | P0 | S | Solo dev |
| TRANS-3 | User can retrieve completed transcription | P0 | M | Solo dev |
| AUDIT-1 | All auth events logged for compliance | P0 | M | Solo dev |
| AUDIT-2 | All data access logged for compliance | P0 | S | Solo dev |

**Total Story Points**: ~22 (assuming S=2, M=5, L=13)

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Whisper service latency unexpectedly high | Medium | High | Implement timeout + retry logic, benchmark early |
| Solo developer knowledge gaps in Go | Low | Medium | Leverage AI agents for code generation/review |
| Database schema changes mid-MVP | Medium | Medium | Use migration framework from day 1 |
| Security vulnerability discovered late | Low | Critical | Weekly `go list -m -u all`, dependency updates |
| MVP scope creep | High | Medium | Strict adherence to out-of-scope list, use ADRs |

## Acceptance Testing Plan

End-to-end test scenario:

1. **Register**: `POST /auth/register` with valid email/password → 201
2. **Login**: `POST /auth/login` with credentials → 200 + JWT
3. **Upload**: `POST /audio/upload` with JWT + .mp3 file → 202 + job ID
4. **Poll**: `GET /jobs/{id}` with JWT → 200 + status:"processing"
5. **Retrieve**: After ~30s, `GET /transcriptions/{id}` with JWT → 200 + text result
6. **Audit**: Verify audit log contains all 5 events with timestamps and user ID

**Pass Criteria**: All 6 steps complete without errors, p95 latency < 100ms (excluding Whisper processing)

## MVP Metrics

Track these metrics during MVP development:

- **Velocity**: Story points completed per week (target: ~5-7 SP/week)
- **Test Coverage**: % of code covered by tests (target: >80%)
- **Build Time**: CI pipeline duration (target: <5 minutes)
- **API Latency**: p50/p95/p99 for each endpoint (target: p95 < 100ms)
- **Error Rate**: % of API requests returning 5xx (target: <1%)

## Post-MVP Roadmap Teaser

After MVP launch, next priorities (see [roadmap.md](./roadmap.md) for details):

1. **Admin Panel**: User management, transcription review
2. **Real-time Streaming**: WebSocket-based live transcription
3. **Multi-tenancy**: Organization accounts, RBAC
4. **Advanced Features**: Search, tagging, custom vocabulary
5. **Infrastructure**: Auto-scaling, Kubernetes, monitoring

---

**Related Documents**:
- [Architecture](./architecture.md) - System design and C4 diagrams
- [Tech Stack](./tech-stack.md) - Technology choices and rationale
- [Roadmap](./roadmap.md) - Long-term feature planning
- [ADRs](./decisions/) - Architectural decision records

**AI Agent Assistance**:
- Use `ai:clarify` label to refine MVP features
- Use `ai:decompose` label to break stories into implementation tasks
- Use `ai:generate` label to create additional user stories
