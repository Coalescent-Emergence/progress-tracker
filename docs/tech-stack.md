# Kerrigan Technology Stack

**Backend Technology Choices and Rationale**

Last Updated: February 12, 2026

## Core Technology: Go 1.23+

**Decision**: Use Go as the primary programming language for Kerrigan backend.

**Rationale** (see [ADR-0001](./decisions/0001-go-backend-language.md) for details):
- **Performance**: Native concurrency with goroutines for handling multiple service calls
- **Type Safety**: Strong static typing reduces runtime errors
- **Deployment**: Single binary simplifies Docker deployment (no runtime dependencies)
- **Ecosystem**: Excellent libraries for HTTP servers, PostgreSQL, JWT, S3
- **Team Expertise**: Solo developer has strong Go experience

**Alternatives Considered**: TypeScript/Node.js (good but slower, less suitable for high-concurrency orchestration), Python (excellent for ML but slower for API gateway)

---

## HTTP Framework: Chi v5

**Package**: `github.com/go-chi/chi/v5`

**Why Chi**:
- Lightweight, idiomatic Go (no magic, just `http.Handler` interface)
- Middleware composition model matches our layered architecture
- Fast routing (trie-based, minimal allocations)
- Well-documented, stable (v5 released 2021, mature)

**Alternatives**: Echo (good but more opinionated), Gin (faster but less idiomatic), stdlib `http.ServeMux` (too basic for middleware needs)

**Usage Example**:
```go
r := chi.NewRouter()
r.Use(middleware.Logger)
r.Use(middleware.Recoverer)

r.Route("/api", func(r chi.Router) {
    r.Use(AuthMiddleware) // Protected routes
    r.Get("/health", healthHandler)
})
```

---

## Database: PostgreSQL 15+

**Why PostgreSQL**:
- **HIPAA Compliance**: Mature audit logging, row-level security (future)
- **JSON Support**: `jsonb` type for flexible metadata storage
- **Full-Text Search**: Built-in support for transcription search (post-MVP)
- **Reliability**: ACID transactions, proven at scale
- **UUID Support**: Native `uuid` type for primary keys

**Alternatives**: MySQL (less JSON support), MongoDB (NoSQL overkill), SQLite (not production-grade)

**Driver**: `github.com/jackc/pgx/v5` (fastest Go PostgreSQL driver, better than database/sql)

---

## Authentication: JWT (HS256)

**Packages**:
- `github.com/golang-jwt/jwt/v5` for JWT generation/validation
- `golang.org/x/crypto/bcrypt` for password hashing

**JWT Strategy**:
- **Access Token**: 15-minute expiry, HS256 signed
- **Refresh Token**: 7-day expiry, stored hashed in database
- **Claims**: `user_id`, `email`, `issued_at`, `expires_at`

**Why HS256 (symmetric)**:
- Simpler key management for MVP (single secret)
- Faster validation (~1-2ms vs ~10-20ms for RS256)
- Sufficient when only Kerrigan validates tokens

**Post-MVP Migration to RS256**:
- If services need independent token validation (without shared secret)
- Transition path: dual-signing period, then deprecate HS256

---

## Object Storage: S3-Compatible (MinIO → AWS S3)

**Package**: `github.com/minio/minio-go/v7`

**Why S3**:
- **Scalability**: Handles TB+ of audio files without DB bloat
- **Cost-Effective**: Cheaper than DB storage for large files
- **Durability**: 99.999999999% durability (AWS S3)
- **Encryption**: At-rest encryption for HIPAA compliance

**Dev**: MinIO (local Docker container, S3-compatible API)  
**Prod**: AWS S3 or GCP Cloud Storage

---

## Testing

### Unit Testing: testify

**Package**: `github.com/stretchr/testify`

**Why testify**:
- `assert` package for readable assertions
- `mock` package for interface mocking
- `suite` package for test fixtures

**Example**:
```go
func TestUserService_Create(t *testing.T) {
    mockRepo := new(MockUserRepository)
    mockRepo.On("Create", mock.Anything).Return(nil)
    
    svc := NewUserService(mockRepo)
    err := svc.CreateUser("test@example.com", "password")
    
    assert.NoError(t, err)
    mockRepo.AssertExpectations(t)
}
```

### HTTP Testing: httptest

**Package**: stdlib `net/http/httptest`

**Why httptest**:
- Built into Go standard library
- Test HTTP handlers without starting server
- Record responses for assertion

---

## Linting & Code Quality

**Tool**: `golangci-lint`

**Enabled Linters**:
- `errcheck`: Ensure errors are checked
- `govet`: Static analysis
- `staticcheck`: Advanced static analysis
- `gosec`: Security vulnerabilities
- `gofmt`: Formatting
- `goimports`: Import organization

**CI Integration**: Runs on every PR via [.github/workflows/ci.yml](../.github/workflows/ci.yml)

---

## Rate Limiting: golang.org/x/time/rate

**Package**: `golang.org/x/time/rate`

**Why x/time/rate**:
- Token bucket algorithm (smooth rate limiting)
- Per-IP limiting in middleware
- Low overhead (goroutine-safe)

**Configuration**: 60 requests/minute per IP for `/auth/*` endpoints

---

## Logging: slog (Go 1.21+)

**Package**: stdlib `log/slog`

**Why slog**:
- Native structured logging (JSON format)
- Performance-optimized (zero-alloc in hot paths)
- Leveled logging (DEBUG, INFO, WARN, ERROR)

**Example**:
```go
slog.Info("User registered", 
    "user_id", userID, 
    "email", email,
    "ip", req.RemoteAddr)
```

**Post-MVP**: Consider [zerolog](https://github.com/rs/zerolog) if slog performance insufficient

---

## Database Migrations

**Tool**: `github.com/golang-migrate/migrate/v4`

**Why migrate**:
- SQL-based migrations (no DSL, direct SQL)
- CLI and Go API
- Supports rollback
- Version tracking in DB

**Migration Files**:
```
migrations/
├── 000001_create_users_table.up.sql
├── 000001_create_users_table.down.sql
├── 000002_create_audio_files_table.up.sql
└── 000002_create_audio_files_table.down.sql
```

---

## Configuration: Environment Variables

**Package**: `github.com/kelseyhightower/envconfig` (optional)

**Why env vars**:
- 12-Factor App compliance
- Kubernetes/Docker-friendly
- No config file management

**Validation**: Fail fast on startup if required vars missing

---

## Development Tools

### Live Reload: Air

**Tool**: `github.com/cosmtrek/air`

**Why Air**:
- Watches files, rebuilds on change
- Faster development iteration

**Usage**:
```bash
air
# Watches Go files, recompiles and restarts on save
```

### Debugging: Delve

**Tool**: `github.com/go-delve/delve`

**Why Delve**:
- Go-specific debugger (better than GDB)
- VSCode integration

---

## Dependency Management

**Strategy**: Direct dependencies in `go.mod`, vendor if needed

**Update Process**:
1. Weekly: `go list -m -u all` to check for updates
2. Monthly: Update non-breaking minor versions
3. Security patches: Immediate update

**Vulnerability Scanning**: `go list -m -json all | nancy sleuth` (Sonatype Nancy)

---

## Build & CI/CD

**Build Tool**: `go build` (no need for Make unless multi-step)

**CI**: GitHub Actions with Go 1.23 setup  
**Coverage**: `go test ./... -coverprofile=coverage.out`  
**Target**: >80% coverage for production code

**Docker**:
```dockerfile
FROM golang:1.23-alpine AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o kerrigan cmd/server/main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /app
COPY --from=builder /build/kerrigan .
CMD ["./kerrigan"]
```

---

## Future Considerations (Post-MVP)

### gRPC

If service-to-service communication needs better performance:
- `google.golang.org/grpc`
- `google.golang.org/protobuf`

### GraphQL

If UI needs flexible querying:
- `github.com/99designs/gqlgen`

### Message Queue

If async processing scales beyond HTTP:
- Redis Streams (lightweight)
- RabbitMQ or Kafka (heavier)

### Observability

**Metrics**: Prometheus with `github.com/prometheus/client_golang`  
**Tracing**: OpenTelemetry with `go.opentelemetry.io/otel`

---

**Related Documents**:
- [ADR-0001: Go as Backend Language](./decisions/0001-go-backend-language.md)
- [Architecture](./architecture.md)
- [Development Guide](./development.md)
