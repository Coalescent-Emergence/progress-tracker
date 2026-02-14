# Kerrigan Roadmap

**Long-term feature planning and release schedule**

Last Updated: February 12, 2026

## MVP (Months 1-3) - Foundation

**Target**: Q2 2026  
**Goal**: Basic authentication and transcription workflow

### Features
- ✅ User registration and JWT authentication
- ✅ Audio file upload via REST API
- ✅ Whisper-STT service integration (batch processing)
- ✅ Transcription job status and result retrieval
- ✅ HIPAA-compliant audit logging
- ✅ Docker deployment with docker-compose

### Success Metrics
- 10 concurrent users supported
- <100ms p95 API latency
- >80% test coverage
- Zero critical security vulnerabilities

**Status**: In development (see [mvp.md](./mvp.md))

---

## V1.0 (Months 4-6) - Production Hardening

**Target**: Q3 2026  
**Goal**: Production-ready with basic admin capabilities

### Features
- **Admin Panel API**: User management, system health monitoring
- **Password Reset**: Email-based password recovery
- **Email Verification**: Verify user email addresses on registration
- **Role-Based Access Control (RBAC)**: Admin, Provider, Viewer roles
- **Transcription History**: List all user transcriptions with filtering
- **API Versioning**: `/api/v1/` prefix, deprecation strategy
- **Kubernetes Deployment**: Helm chart for K8s deployment

### Infrastructure
- Prometheus metrics collection
- Grafana dashboards for monitoring
- Sentry error tracking
- Database backup automation

### Success Metrics
- 100 concurrent users
- <50ms p95 API latency
- 99.9% uptime
- <1% error rate

---

## V1.1 (Months 7-9) - Real-Time Features

**Target**: Q4 2026  
**Goal**: Live transcription streaming

### Features
- **WebSocket Streaming**: Real-time audio upload + transcription
- **Partial Results**: Stream intermediate transcription chunks
- **Live Dashboard**: Real-time job monitoring for admins
- **Transcription Editing**: Correct/annotate transcriptions via API
- **Custom Vocabulary**: User-provided vocabulary for better accuracy

### Infrastructure
- Redis for WebSocket session management
- Horizontal pod auto-scaling (HPA)
- CDN for static assets

### Success Metrics
- <2s latency for first transcription chunk
- 500 concurrent WebSocket connections
- 99.95% uptime

---

## V2.0 (Months 10-12) - Enterprise Features

**Target**: Q1 2027  
**Goal**: Multi-tenancy and advanced features

### Features
- **Organization Accounts**: Multi-user organizations with shared transcriptions
- **Team Collaboration**: Share transcriptions within org
- **Advanced Search**: Full-text search across all transcriptions
- **Tagging & Metadata**: Custom tags and metadata on transcriptions
- **Export Formats**: PDF, DOCX, SRT, VTT export
- **Webhooks**: Event notifications (transcription completed, etc.)
- **API Keys**: Alternative auth method for programmatic access

### Infrastructure
- Multi-region deployment (US, EU for GDPR)
- Database sharding by organization
- Object storage tiering (hot/cold data)

### Success Metrics
- 1000+ concurrent users
- Support for 100+ organizations
- <5s p95 search query time

---

## V2.1+ (Year 2) - AI & Intelligence

**Target**: Beyond Q1 2027  
**Goal**: AI-powered features and integrations

### Potential Features
- **Speaker Diarization**: Identify and label different speakers
- **Sentiment Analysis**: Detect tone/sentiment in transcriptions
- **Automatic Summarization**: Generate summaries of long transcriptions
- **Medical Entity Recognition**: Extract medical terms, diagnoses, medications
- **Multi-Language Support**: Transcription in 50+ languages
- **Voice Biometrics**: Speaker verification for security

### Infrastructure
- GPU cluster for ML workloads
- Model serving infrastructure (KServe, TorchServe)
- Feature store for ML features

---

## Feature Prioritization Framework

Features are prioritized using **RICE scoring**:

**RICE = (Reach × Impact × Confidence) / Effort**

- **Reach**: How many users affected (1-10)
- **Impact**: Value delivered (1-3: low/med/high)
- **Confidence**: Certainty of impact (0-100%)
- **Effort**: Person-weeks to ship

**Example** (Real-time streaming):
- Reach: 8 (most users will use)
- Impact: 3 (high value, key differentiator)
- Confidence: 70% (some technical unknowns)
- Effort: 8 person-weeks
- **RICE** = (8 × 3 × 0.7) / 8 = **2.1**

---

## Technical Debt & Maintenance

Ongoing tasks across all versions:

- **Security**: Weekly dependency updates, quarterly security audits
- **Performance**: Monthly performance reviews, DB query optimization
- **Documentation**: Keep ADRs and docs up to date
- **Testing**: Maintain >80% coverage, add E2E tests
- **Refactoring**: Address tech debt quarterly (15% sprint allocation)

---

## Architecture Evolution

### V1.0 → V2.0 Transitions

| Component | MVP | V1.0 | V2.0 |
|-----------|-----|------|------|
| **Auth** | JWT HS256 | JWT RS256 (distributed) | OAuth 2.0 + OIDC |
| **Storage** | Single S3 bucket | Regional buckets | Multi-region + CDN |
| **Database** | Single PostgreSQL | Read replicas | Sharded by organization |
| **Caching** | None | Redis (sessions) | Redis Cluster (distributed) |
| **Deployment** | Docker Compose | Kubernetes (single region) | Multi-region K8s |
| **Monitoring** | Logs only | Prometheus + Grafana | Full observability (traces) |

---

## Dependencies & Risks

| Dependency | Risk | Mitigation |
|-----------|------|------------|
| **Whisper-STT** | Service downtime blocks transcriptions | Implement retry + queue, SLA with 99.9% uptime |
| **PostgreSQL** | Single point of failure | Add read replicas (V1.0), automated backups |
| **S3 Storage** | Vendor lock-in | Use S3-compatible API (easy migration) |
| **Go Ecosystem** | Breaking changes in dependencies | Pin versions, test before upgrading |

---

## Deferred/Rejected Features

**Deferred** (not planned for next 12 months):
- ❌ Mobile apps (native iOS/Android) - Web-first strategy
- ❌ On-premise deployment - Cloud-only initially
- ❌ Video transcription - Audio only for simplicity
- ❌ Live translation - Transcription only, translation later

**Rejected** (decided against):
- ❌ Blockchain for audit logging - Overkill, DB sufficient for HIPAA
- ❌ GraphQL API - REST adequate for current UI needs
- ❌ Serverless architecture - Long-running jobs unsuitable for Lambda

---

**Related Documents**:
- [MVP Scope](./mvp.md) - Immediate priorities
- [Architecture](./architecture.md) - Technical design
- [Metrics](./metrics.md) - Success measurement
- [ADRs](./decisions/) - Architectural decisions

**AI Agent Assistance**:
- Use `ai:clarify` to refine feature ideas into MVP stories
- Use `type:architecture` + `ai:generate-adr` for major feature additions
