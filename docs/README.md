# Kerrigan

**Backend API gateway and workflow orchestration for the Coalescent-Emergence healthcare transcription platform.**

![Status](https://img.shields.io/badge/status-MVP%20Development-yellow)
![Go Version](https://img.shields.io/badge/go-1.23+-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)

## 📊 MVP Progress Tracker

**[View Live MVP Progress Dashboard →](https://coalescent-emergence.github.io/Kerrigan/mvp-tracker.html)**

Real-time tracking of all MVP tasks, milestones, and completion status. Non-technical friendly dashboard showing:
- Overall completion percentage
- 60-day timeline with 3 phases (Foundation, Core Features, Launch)
- Priority and effort indicators for each task
- Automatic updates from GitHub Issues

## Overview

Kerrigan is the central backend service for the Coalescent-Emergence platform, providing:

- **Authentication & Authorization**: JWT-based user authentication, session management
- **API Gateway**: Unified REST API for UI and external clients
- **Workflow Orchestration**: Coordinates requests between UI, Whisper-STT, and MCP servers
- **Audit Logging**: SOC2/HIPAA-compliant audit trail for all data access
- **Data Management**: PostgreSQL database for users, metadata, and transcription records

## Architecture

Kerrigan follows a **layered service architecture** where it acts as the orchestration layer:

```
UI → Kerrigan (this repo) → Services (Whisper-STT, MCP-*)
                ↓
            PostgreSQL
```

See [docs/architecture.md](./docs/architecture.md) for detailed C4 diagrams and component breakdown.

**Key Design Decisions** (ADRs):
- [Organization: Multi-Repo Architecture](https://github.com/Coalescent-Emergence/.github/blob/main/docs/decisions/0001-multi-repo-architecture.md)
- [Organization: Layered Service Architecture](https://github.com/Coalescent-Emergence/.github/blob/main/docs/decisions/0003-layered-service-architecture.md)
- [Kerrigan: Go as Backend Language](./docs/decisions/0001-go-backend-language.md)

## Quick Start

### Prerequisites

- **Go 1.23+**: [Download](https://go.dev/dl/)
- **PostgreSQL 15+**: [Installation guide](https://www.postgresql.org/download/)
- **Docker** (optional): For running PostgreSQL and services locally

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/Coalescent-Emergence/Kerrigan.git
cd Kerrigan

# Install dependencies
go mod download

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations (coming soon)
# make migrate-up

# Run tests
go test ./... -v

# Start development server
go run cmd/server/main.go
```

Server will start on `http://localhost:8080` by default.

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | HTTP server port | `8080` | No |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://localhost/kerrigan` | Yes |
| `JWT_SECRET` | Secret key for JWT signing (HS256) | - | Yes |
| `LOG_LEVEL` | Logging level (debug, info, warn, error) | `info` | No |
| `WHISPER_SERVICE_URL` | Whisper-STT service endpoint | - | Yes |

See `.env.example` for complete list.

## Project Structure

```
Kerrigan/
├── cmd/
│   └── server/          # Application entrypoint
│       └── main.go
├── internal/            # Private application code
│   ├── auth/            # Authentication (JWT, sessions)
│   ├── api/             # HTTP handlers and routing
│   ├── service/         # Business logic
│   ├── repository/      # Data access layer
│   ├── middleware/      # HTTP middleware (auth, logging, CORS)
│   └── config/          # Configuration management
├── pkg/                 # Public reusable packages (if any)
├── api/                 # API specifications
│   └── openapi.yaml     # OpenAPI/Swagger spec
├── migrations/          # Database migration files
├── tests/               # Integration and E2E tests
│   └── integration/
├── scripts/             # Build and deployment scripts
│   ├── build.sh
│   └── test.sh
├── docs/                # Documentation
│   ├── architecture.md
│   ├── api.md
│   ├── development.md
│   └── decisions/       # Architecture Decision Records (ADRs)
├── .github/
│   └── workflows/       # CI/CD workflows
│       └── ci.yml
├── go.mod               # Go module dependencies
├── go.sum
├── .env.example         # Example environment configuration
├── .gitignore
├── LICENSE
└── README.md            # This file
```

## Development Workflow

### Branch Strategy

- **`main`**: Production-ready code, **protected branch** requiring PR
- **`dev`**: Integration branch (optional for MVP, can develop directly from feature branches)
- **`feature/<issue>-name`**: Feature branches, always create from latest `main`

**Branch Protection Settings** (for `main`):
- ✅ Require pull request before merging
  - Required approvals: 1 (or 0 for solo dev initially)
  - Dismiss stale approvals when new commits pushed
- ✅ Require status checks to pass before merging
  - Required checks: `lint`, `test`, `build` (from CI workflow)
  - Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ❌ Allow force pushes (disabled)
- ❌ Allow deletions (disabled)

See [.github/REPOSITORY_SETTINGS.md](https://github.com/Coalescent-Emergence/.github/blob/main/REPOSITORY_SETTINGS.md) for complete setup instructions.

Example workflow:
```bash
git checkout main
git pull origin main
git checkout -b feature/15-jwt-authentication
# ... make changes ...
git push origin feature/15-jwt-authentication
# Open PR on GitHub (CI runs automatically)
# AI agents review automatically (Architecture Guardian)
# After approval and green checks, merge via "Squash and merge"
```

### Pull Request Process

1. **Create issue** first (required by [pr-validation workflow](https://github.com/Coalescent-Emergence/.github/blob/main/workflows/pr-validation.yml))
2. **Create feature branch** from `main`
3. **Implement changes** with tests
4. **Open PR** linking issue with "Closes #15" in description
5. **AI agents** automatically review (Architecture Guardian, Refactor Auditor if applicable)
6. **Human review** and address feedback
7. **Merge** via squash merge (preferred for clean history)

See [.github/CONTRIBUTING.md](https://github.com/Coalescent-Emergence/.github/blob/main/CONTRIBUTING.md) for complete workflow.

### Testing

```bash
# Run all tests
go test ./... -v

# Run with coverage
go test ./... -v -race -coverprofile=coverage.out
go tool cover -html=coverage.out  # View coverage in browser

# Run specific package tests
go test ./internal/auth -v

# Run integration tests
go test ./tests/integration -v

# Run tests with live reload (using gow)
go install github.com/mitranim/gow@latest
gow test ./... -v
```

**Coverage Target**: 80%+ for production code (enforced in CI)

### Linting

```bash
# Install golangci-lint
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Run linter
golangci-lint run ./...

# Fix auto-fixable issues
golangci-lint run --fix ./...
```

## API Documentation

- **OpenAPI Spec**: [api/openapi.yaml](./api/openapi.yaml)
- **API Guide**: [docs/api.md](./docs/api.md)

### Core Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Create new user account |
| `POST` | `/auth/login` | Login and receive JWT |
| `POST` | `/auth/refresh` | Refresh JWT using refresh token |
| `POST` | `/audio/upload` | Upload audio file for transcription |
| `GET` | `/jobs/:id` | Get transcription job status |
| `GET` | `/transcriptions/:id` | Retrieve transcription results |

All endpoints except `/auth/*` require `Authorization: Bearer <jwt>` header.

## Deployment

**Current**: Manual deployment (MVP)
**Future**: Automated CI/CD pipeline (see [docs/deployment.md](./docs/deployment.md))

```bash
# Build production binary
./scripts/build.sh

# Run binary
./bin/kerrigan

# Docker deployment (coming soon)
docker build -t kerrigan:latest .
docker run -p 8080:8080 --env-file .env kerrigan:latest
```

## Contributing

This repository follows the organization-wide contribution guidelines:

- [CONTRIBUTING.md](https://github.com/Coalescent-Emergence/.github/blob/main/CONTRIBUTING.md) - Workflow and processes
- [AI_PLAYBOOK.md](https://github.com/Coalescent-Emergence/.github/blob/main/AI_PLAYBOOK.md) - AI agent usage
- [LABELS.md](https://github.com/Coalescent-Emergence/.github/blob/main/LABELS.md) - Issue/PR label taxonomy

### AI Agent Assistance

Kerrigan inherits organization-wide AI agents:

- **MVP Clarifier** (`ai:clarify`): Break down ideas into MVP stories
- **Story Generator** (`ai:generate`): Create atomic user stories
- **Technical Decomposer** (`ai:decompose`): Generate implementation tasks
- **Architecture Guardian** (auto): Reviews PRs against ADRs
- **Refactor Auditor** (`type:refactor`): Analyzes refactor safety

See [AI_PLAYBOOK.md](https://github.com/Coalescent-Emergence/.github/blob/main/AI_PLAYBOOK.md) for details.

## Security

- **Secrets**: Never commit secrets. Use environment variables or secret management service.
- **Dependencies**: Run `go list -m -u all` regularly to check for vulnerabilities.
- **Audit Logging**: All data access logged for SOC2/HIPAA compliance.
- **Security Policy**: See [.github/SECURITY.md](https://github.com/Coalescent-Emergence/.github/blob/main/SECURITY.md)

**Report vulnerabilities** to: security@coalescent-emergence.com (or per [SECURITY.md](https://github.com/Coalescent-Emergence/.github/blob/main/SECURITY.md))

## License

Proprietary and confidential. Unauthorized copying or distribution is strictly prohibited.

See [LICENSE](./LICENSE) for details.

## Links

- **Organization**: [Coalescent-Emergence](https://github.com/Coalescent-Emergence)
- **Organization Governance**: [.github Repository](https://github.com/Coalescent-Emergence/.github)
- **Related Repositories**:
  - [UI](https://github.com/Coalescent-Emergence/UI) - Web frontend (to be created)
  - [Whisper-STT](https://github.com/Coalescent-Emergence/Whisper-STT) - Transcription service (to be created)
- **Architecture Decisions**: [docs/decisions/](./docs/decisions/)

## Support

- **Issues**: [GitHub Issues](https://github.com/Coalescent-Emergence/Kerrigan/issues)
- **Documentation**: [docs/](./docs/)
- **Roadmap**: [docs/roadmap.md](./docs/roadmap.md)
