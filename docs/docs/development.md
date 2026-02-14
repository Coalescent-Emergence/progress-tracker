# Kerrigan Development Guide

**Local setup, testing, debugging, and contribution workflow**

Last Updated: February 12, 2026

---

## Prerequisites

### Required
- **Go**: 1.23 or later ([installation guide](https://go.dev/doc/install))
- **Docker**: 20.10+ and Docker Compose v2 ([Docker Desktop](https://www.docker.com/products/docker-desktop/))
- **Git**: 2.30+ ([download](https://git-scm.com/downloads))

### Recommended
- **VSCode** with Go extension (`golang.go`)
- **Delve** debugger: `go install github.com/go-delve/delve/cmd/dlv@latest`
- **Air** live reload: `go install github.com/cosmtrek/air@latest`
- **golangci-lint**: `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest`

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Coalescent-Emergence/Kerrigan.git
cd Kerrigan
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your local settings (defaults usually work)
```

**Key Variables**:
```env
SERVER_PORT=8080
DATABASE_URL=postgres://kerrigan:password@localhost:5432/kerrigan?sslmode=disable
JWT_SECRET=your-secret-key-here-change-in-production
S3_ENDPOINT=http://localhost:9000  # MinIO
```

### 3. Start Dependencies (Docker Compose)

```bash
docker compose up -d
```

This starts:
- **PostgreSQL** (port 5432)
- **MinIO** (port 9000, console: 9001)
- **Redis** (port 6379, optional for V1.0+)

**Verify**:
```bash
docker compose ps
# All services should show "Up"
```

### 4. Run Database Migrations

```bash
# TODO: Add migrate command when migrations/ created
# Example: make migrate-up
```

### 5. Install Go Dependencies

```bash
go mod download
```

### 6. Run Server

**Option A**: Direct run
```bash
go run cmd/server/main.go
```

**Option B**: With Air (live reload)
```bash
air
# Watches files, auto-rebuilds on save
```

**Verify**:
```bash
curl http://localhost:8080/api/health
# Should return: {"status":"healthy",...}
```

---

## Project Structure

```
Kerrigan/
├── cmd/
│   └── server/
│       └── main.go           # Application entrypoint
├── internal/                 # Private application code
│   ├── config/               # Configuration loading
│   ├── api/
│   │   ├── handlers/         # HTTP request handlers
│   │   ├── middleware/       # Auth, logging, rate limiting
│   │   └── router/           # Chi router setup
│   ├── service/              # Business logic layer
│   │   ├── auth.go
│   │   ├── audio.go
│   │   └── transcription.go
│   ├── repository/           # Database access layer
│   │   └── postgres/
│   │       ├── user.go
│   │       └── audio.go
│   └── models/               # Domain models (User, AudioFile, etc.)
├── migrations/               # SQL migration files
│   ├── 000001_create_users_table.up.sql
│   └── 000001_create_users_table.down.sql
├── tests/
│   ├── integration/          # API integration tests
│   └── mocks/                # Mock implementations
├── scripts/
│   ├── build.sh              # Build binary
│   └── test.sh               # Run all tests
├── docs/                     # Documentation
├── go.mod                    # Dependencies
├── go.sum                    # Dependency checksums
├── .env.example              # Environment template
├── docker-compose.yml        # Local dev services
└── Dockerfile                # Production image
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/add-audio-upload
```

**Branch Naming**:
- `feature/`: New features
- `fix/`: Bug fixes
- `refactor/`: Code improvements
- `docs/`: Documentation updates

### 2. Write Tests (TDD)

Create test before implementation:

```go
// tests/integration/audio_upload_test.go
func TestAudioUpload_Success(t *testing.T) {
    // Setup test server
    app := setupTestApp(t)
    defer app.Cleanup()
    
    // Create test user and get token
    token := app.CreateTestUser("test@example.com")
    
    // Prepare test audio file
    audioData := loadTestAudio("test-5min.wav")
    
    // Make request
    resp := app.UploadAudio(token, audioData)
    
    // Assertions
    assert.Equal(t, http.StatusAccepted, resp.StatusCode)
    
    var result map[string]interface{}
    json.Unmarshal(resp.Body, &result)
    assert.NotEmpty(t, result["audio_id"])
    assert.Equal(t, "uploaded", result["status"])
}
```

Run test (should fail):
```bash
go test ./tests/integration -run TestAudioUpload_Success
```

### 3. Implement Feature

```go
// internal/api/handlers/audio.go
func (h *AudioHandler) Upload(w http.ResponseWriter, r *http.Request) {
    // Parse multipart form
    file, header, err := r.FormFile("file")
    if err != nil {
        respondError(w, http.StatusBadRequest, "Missing file")
        return
    }
    defer file.Close()
    
    // Extract user from context (set by auth middleware)
    userID := r.Context().Value("user_id").(string)
    
    // Call service layer
    audio, err := h.audioService.Upload(r.Context(), userID, file, header)
    if err != nil {
        respondError(w, http.StatusInternalServerError, err.Error())
        return
    }
    
    respondJSON(w, http.StatusAccepted, audio)
}
```

### 4. Run Tests

```bash
# Run all tests
go test ./...

# Run with coverage
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out

# Run specific package
go test ./internal/service -v
```

### 5. Lint Code

```bash
golangci-lint run

# Auto-fix some issues
golangci-lint run --fix
```

**Common Issues**:
- `errcheck`: Unchecked errors → add `if err != nil { ... }`
- `gofmt`: Formatting → run `go fmt ./...`
- `gosec`: Security → review and fix or add `// nolint:gosec` with justification

### 6. Commit & Push

```bash
git add .
git commit -m "feat: add audio file upload endpoint"
git push origin feature/add-audio-upload
```

**Commit Message Format** (Conventional Commits):
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `test:` Add/update tests
- `docs:` Documentation
- `chore:` Tooling/dependencies

### 7. Create Pull Request

Open PR on GitHub, request review from AI agents:
1. Add label `type:feature` (triggers MVP Clarifier if needed)
2. Architecture Guardian auto-runs (checks ADRs)
3. CI runs tests and linter
4. Merge after passing checks

---

## Testing

### Unit Tests

Test individual functions in isolation:

```go
// internal/service/auth_test.go
func TestAuthService_ValidatePassword(t *testing.T) {
    svc := NewAuthService(nil) // No DB needed for this test
    
    tests := []struct {
        name     string
        password string
        wantErr  bool
    }{
        {"valid password", "SecureP@ss1", false},
        {"too short", "Pass1!", true},
        {"no uppercase", "secure@ss1", true},
        {"no number", "SecureP@ss", true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := svc.ValidatePassword(tt.password)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

### Integration Tests

Test full HTTP request/response cycle:

```go
// tests/integration/auth_test.go
func TestLogin_Success(t *testing.T) {
    app := setupTestApp(t)
    defer app.Cleanup()
    
    // Register user
    app.RegisterUser("test@example.com", "Password123!")
    
    // Login
    body := `{"email":"test@example.com","password":"Password123!"}`
    req := httptest.NewRequest("POST", "/api/auth/login", strings.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    
    w := httptest.NewRecorder()
    app.Router.ServeHTTP(w, req)
    
    assert.Equal(t, http.StatusOK, w.Code)
    
    var resp map[string]interface{}
    json.Unmarshal(w.Body.Bytes(), &resp)
    assert.NotEmpty(t, resp["access_token"])
    assert.NotEmpty(t, resp["refresh_token"])
}
```

### Test Database Setup

Use Docker for test database:

```go
// tests/integration/setup.go
func setupTestApp(t *testing.T) *TestApp {
    // Start test DB container
    db := startTestPostgres(t)
    
    // Run migrations
    runMigrations(db)
    
    // Create app with test dependencies
    app := &TestApp{
        DB:     db,
        Router: setupRouter(db),
    }
    
    return app
}

func (app *TestApp) Cleanup() {
    app.DB.Close()
    stopTestPostgres()
}
```

---

## Debugging

### VSCode Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Kerrigan",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}/cmd/server",
      "env": {
        "DATABASE_URL": "postgres://kerrigan:password@localhost:5432/kerrigan?sslmode=disable",
        "JWT_SECRET": "test-secret"
      },
      "args": []
    },
    {
      "name": "Debug Test",
      "type": "go",
      "request": "launch",
      "mode": "test",
      "program": "${workspaceFolder}/internal/service",
      "args": ["-test.run", "TestAuthService_Login"]
    }
  ]
}
```

**Usage**:
1. Set breakpoints in code
2. Press `F5` to start debugging
3. Use Debug Console to inspect variables

### Delve CLI

```bash
# Debug application
dlv debug cmd/server/main.go

# Debug specific test
dlv test ./internal/service -- -test.run TestAuthService_Login
```

**Delve Commands**:
- `b main.go:25` - Set breakpoint at line 25
- `c` - Continue execution
- `n` - Next line
- `s` - Step into function
- `p variable` - Print variable value
- `q` - Quit

---

## Database Management

### Migrations

```bash
# Create new migration
migrate create -ext sql -dir migrations -seq add_audio_files_table

# Apply migrations
migrate -path migrations -database "postgres://user:pass@localhost:5432/kerrigan?sslmode=disable" up

# Rollback last migration
migrate -path migrations -database "..." down 1
```

### Seed Data (Development)

```bash
# TODO: Create seed script
# scripts/seed.sh
```

### Database Console

```bash
# Connect to local DB
docker exec -it kerrigan-postgres psql -U kerrigan -d kerrigan

# List tables
\dt

# Describe table
\d users

# Run query
SELECT * FROM users LIMIT 10;
```

---

## Local Service Testing

### MinIO (S3 Alternative)

**Web Console**: http://localhost:9001  
**Credentials**: `minioadmin` / `minioadmin`

**Create Bucket**:
```bash
# Install MinIO client
brew install minio/stable/mc  # macOS
# or download from: https://min.io/docs/minio/linux/reference/minio-mc.html

# Configure
mc alias set local http://localhost:9000 minioadmin minioadmin

# Create bucket
mc mb local/kerrigan-audio
```

### Whisper-STT Mock (MVP)

For MVP, mock Whisper-STT responses:

```go
// internal/service/transcription.go
func (s *TranscriptionService) mockWhisperCall(audioURL string) (string, error) {
    // Return fake transcription for testing
    return "This is a mocked transcription result.", nil
}
```

**V1.0+**: Deploy actual Whisper-STT microservice

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill process
kill -9 <PID>
```

### Docker Compose Issues

```bash
# Rebuild containers
docker compose down -v
docker compose up --build -d

# View logs
docker compose logs -f postgres
```

### Database Connection Refused

1. Check PostgreSQL is running: `docker compose ps`
2. Verify connection string in `.env`
3. Check firewall/antivirus blocking port 5432

### Tests Failing

```bash
# Clean test cache
go clean -testcache

# Run tests with verbose output
go test ./... -v

# Run specific test
go test ./internal/service -run TestAuthService_Login -v
```

---

## Performance Profiling

### CPU Profiling

```go
import _ "net/http/pprof"

// In main.go:
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

**Capture profile**:
```bash
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

### Memory Profiling

```bash
go tool pprof http://localhost:6060/debug/pprof/heap
```

**Analyze**:
```
(pprof) top10      # Top 10 allocations
(pprof) list funcName  # Show source code
(pprof) web        # Open in browser (requires Graphviz)
```

---

## AI Agent Development Workflow

1. **Create Issue**: Describe feature/bug
2. **Add Label**: `ai:clarify` to generate stories
3. **Review Stories**: AI generates MVP-scoped stories
4. **Add Label**: `ai:decompose` for task breakdown
5. **Implement**: Follow task list
6. **Create PR**: Architecture Guardian auto-reviews
7. **Merge**: Celebrate! 🎉

**Example**:
```
Issue: "Add password reset functionality"
Label: ai:clarify
AI Output: 3 stories (email verification, reset token, password update)
Label: ai:decompose (on story)
AI Output: 8 tasks with dependencies
```

---

**Related Documents**:
- [Architecture](./architecture.md) - System design
- [API Documentation](./api.md) - Endpoint specs
- [Contributing Guidelines](../.github/CONTRIBUTING.md) - PR workflow
- [Repository Setup](../.github/docs/REPOSITORY_SETUP.md) - CI/CD setup

**Next Steps**:
- Implement authentication handlers
- Write integration tests
- Set up CI/CD pipeline
