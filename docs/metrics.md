# Kerrigan Metrics & KPIs

**Success measurement and operational health indicators**

Last Updated: February 12, 2026

## Product Metrics

### User Engagement

| Metric | Definition | Target (MVP) | Target (V1.0) |
|--------|-----------|--------------|---------------|
| **Daily Active Users (DAU)** | Unique users with ≥1 API call per day | 5 | 50 |
| **Weekly Active Users (WAU)** | Unique users with ≥1 API call per week | 10 | 100 |
| **Transcriptions per User** | Avg transcriptions per user per week | 3 | 10 |
| **User Retention (7-day)** | % users who return within 7 days of first use | 40% | 60% |
| **Time to First Transcription** | Median time from registration to first transcription | <5 min | <2 min |

### Business Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| **Transcription Success Rate** | % of jobs that complete successfully | >95% |
| **Median Transcription Time** | Time from upload to completed result | <30s |
| **Average Audio Duration** | Median uploaded audio file length | ~5 min |
| **Storage Growth** | Audio storage increase per month | (Tracked, no target) |

---

## System Performance

### API Latency

| Endpoint | Target p50 | Target p95 | Target p99 |
|----------|-----------|-----------|-----------|
| `POST /auth/login` | <20ms | <100ms | <200ms |
| `POST /audio/upload` (↑ file) | <500ms | <2s | <5s |
| `GET /jobs/:id` | <10ms | <50ms | <100ms |
| `GET /transcriptions/:id` | <20ms | <100ms | <200ms |

**Measurement**: Log request duration in middleware, aggregate in Prometheus (post-MVP)

### Throughput

| Metric | Target (MVP) | Target (V1.0) |
|--------|--------------|---------------|
| **Requests per second (RPS)** | 10 | 100 |
| **Concurrent users** | 10 | 100 |
| **Audio uploads per hour** | 20 | 200 |
| **Transcriptions per hour** | 20 | 200 |

### Availability & Reliability

| Metric | Target (MVP) | Target (V1.0) |
|--------|--------------|---------------|
| **Uptime** | 99% | 99.9% |
| **Mean Time Between Failures (MTBF)** | >7 days | >30 days |
| **Mean Time To Recovery (MTTR)** | <1 hour | <15 minutes |
| **Error Rate** (5xx responses) | <1% | <0.1% |

---

## Code Quality

### Test Coverage

| Category | Target |
|----------|--------|
| **Overall Coverage** | >80% |
| **Business Logic (services)** | >90% |
| **HTTP Handlers** | >75% |
| **Repositories** | >85% |
| **Middleware** | >70% |

**Measurement**: `go test ./... -coverprofile=coverage.out`

### Code Complexity

| Metric | Target |
|--------|--------|
| **Cyclomatic Complexity** | <10 per function |
| **Max Function Lines** | <50 lines |
| **Max File Lines** | <500 lines |

**Enforcement**: `golangci-lint` with `gocyclo` and `gofmt`

---

## Security & Compliance

### HIPAA Audit Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| **Audit Log Coverage** | % of PHI access events logged | 100% |
| **Audit Log Retention** | Days of logs retained | 90 days (MVP), 7 years (prod) |
| **Failed Auth Attempts** | Failed logins per user per day | <5 (rate limit trigger) |
| **Password Reset Attempts** | Password resets per user per week | <3 |

### Security Vulnerabilities

| Metric | Target |
|--------|--------|
| **Critical Vulnerabilities** | 0 in production |
| **High Vulnerabilities** | Fix within 7 days |
| **Medium Vulnerabilities** | Fix within 30 days |
| **Dependency Updates** | Check weekly, update monthly |

**Measurement**: `go list -m -u all`, GitHub Dependabot alerts

---

## Development Velocity

### Sprint Metrics (Solo Developer + AI)

| Metric | Definition | Target |
|--------|-----------|--------|
| **Story Points per Week** | Avg story points completed | 5-7 SP |
| **Cycle Time** | Issue opened → PR merged | <3 days |
| **PR Merge Time** | PR created → merged | <1 day |
| **Build Time** | CI pipeline duration (test + build) | <5 minutes |

### AI Agent Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| **AI Suggestions Accepted** | % of AI-generated code/ADRs used | >50% |
| **Agent Invocations** | AI agent triggers per week | 5-10 |
| **Agent Accuracy** | % of agent outputs requiring minimal edits | >70% |

**Tracked For**:
- MVP Clarifier (story generation)
- Technical Decomposer (task breakdown)
- Architecture Guardian (ADR violation detection)

---

## Operational Metrics

### Database

| Metric | Target |
|--------|--------|
| **Query Latency (p95)** | <50ms |
| **Connection Pool Utilization** | <80% |
| **Active Connections** | <20 (of 25 max) |
| **Slow Queries** (>1s) | <1% of queries |
| **Database Size** | Monitor growth, no hard limit MVP |

### Object Storage (S3)

| Metric | Target |
|--------|--------|
| **Upload Success Rate** | >99% |
| **Download Latency (p95)** | <500ms |
| **Storage Used** | Monitor, no limit MVP |
| **Monthly Bandwidth** | Monitor for cost optimization |

### External Services

| Metric | Target |
|--------|--------|
| **Whisper-STT Availability** | >99% |
| **Whisper-STT Latency (p95)** | <30s for 5min audio |
| **Whisper-STT Error Rate** | <2% |

---

## Cost Metrics (Post-MVP)

| Metric | Definition | Est. Month 1 |
|--------|-----------|--------------|
| **AWS/GCP Bill** | Total cloud spend | $50 |
| **Cost per Transcription** | Total cost / transcriptions | $0.10 |
| **Database Costs** | PostgreSQL hosting | $15 |
| **Storage Costs** | S3/GCS audio storage | $5 |
| **Compute Costs** | Kubernetes nodes | $30 |

**Optimization Target**: <$0.05 per transcription by V1.0

---

## Monitoring Stack

### MVP (Lightweight)
- **Logs**: Structured JSON logs to stdout, view with `docker logs`
- **Metrics**: Manual calculation from logs and DB queries
- **Alerts**: None (manual monitoring)

### V1.0 (Production)
- **Logs**: Loki or CloudWatch Logs
- **Metrics**: Prometheus scraping `/metrics` endpoint
- **Dashboards**: Grafana with pre-built dashboards
- **Alerts**: PagerDuty for critical issues (uptime <99%, error rate >1%)
- **Tracing**: OpenTelemetry for distributed tracing

---

## Dashboard Examples

### Grafana Dashboard (V1.0+)

**Panel 1**: API Request Rate (RPS)  
**Panel 2**: API Latency (p50, p95, p99)  
**Panel 3**: Error Rate (4xx, 5xx)  
**Panel 4**: Transcription Job Status (pending, processing, completed, failed)  
**Panel 5**: Database Connection Pool Utilization  
**Panel 6**: Memory and CPU Usage  

---

## Reporting Cadence

| Report | Frequency | Audience | Format |
|--------|-----------|----------|--------|
| **Daily Health Check** | Daily | Solo dev | Terminal/dashboard |
| **Weekly Sprint Review** | Weekly | Solo dev + stakeholders | GitHub issue |
| **Monthly Product Metrics** | Monthly | Internal | Spreadsheet/doc |
| **Quarterly OKR Review** | Quarterly | Company | Presentation |

---

**Related Documents**:
- [MVP Scope](./mvp.md) - MVP success criteria
- [Roadmap](./roadmap.md) - Long-term targets
- [Architecture](./architecture.md) - Performance targets

**AI Agent Assistance**:
- Track AI agent accuracy and usage in `metrics.md` updates
- Use Metrics to validate ADR decisions (e.g., latency < target?)
