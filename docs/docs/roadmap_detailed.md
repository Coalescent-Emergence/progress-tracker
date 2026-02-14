KERRIGAN MVP - Executive Summary & Quick Reference
Project: Intelligent Conversation Intelligence Platform for Healthcare
 Codenamed: Kerrigan
 Status: Planning Phase
 Document Date: February 12, 2026

One-Page Project Overview
What is Kerrigan?
Kerrigan is a privacy-first conversation intelligence platform that helps therapists and mental health professionals enhance their clinical documentation and care delivery. It automatically:
Records and transcribes therapy sessions from Microsoft Teams calls or uploaded audio
Summarizes conversations intelligently (both extractive and abstractive)
Provides real-time AI consultation through an in-session chat assistant
Suggests evidence-based interventions using retrieval-augmented generation (RAG)
Maintains absolute confidentiality with 100% local data retention and HIPAA compliance
Why Build Kerrigan Now?
Therapist burden: Documentation takes 10-15 minutes per 50-minute session
Quality at scale: AI-powered notes help standardize care quality
Privacy imperative: Healthcare data is increasingly attacked; local-first architecture eliminates cloud risks
Market opportunity: $4.2B mental health software market; few truly HIPAA-compliant AI solutions exist

Key Numbers
Metric
Value
Total Duration
28-36 weeks (6-8.5 months)
Team Size
6 FTE (5 full-time, 1 part-time)
Core Phases
4 (Foundation, Core Features, Hardening, Launch)
Gate Reviews
4 major milestones with approval gates
Target Transcription Accuracy
≥95% on clinical audio
Chat Response Time
<1s first token, <5s full response
System Uptime Target
≥99.5%
Concurrent Sessions Supported
5+ per server


MVP Feature Set
Tier 1: MVP Launch Critical (Must Have)
Audio File Transcription - Upload audio files → automatic transcription with speaker identification and PII masking
Teams Call Recording - Automatic Teams call capture, retrieval, and transcription
Conversation Summarization - Dual-mode summarization (extractive + AI-powered abstractive)
Real-Time Chat Interface - In-session AI assistant with context-aware responses
Local Data Retention - 100% local storage, AES-256 encryption, zero cloud PII
HIPAA Compliance - Audit logging, access control, secure deletion, BAA-ready
Tier 2: High Priority (If Schedule Permits)
RAG-enhanced therapeutic interventions
Session history and semantic search
Custom intervention library for clinics
Tier 3: Future Versions
Mobile apps (iOS/Android)
Zoom/Google Meet integration
EHR integration (Epic, Cerner)
Real-time co-therapist collaboration

Timeline at a Glance
Phase 1: Foundation & Security           (Weeks 1-10, ~8-10 weeks)
├─ Infrastructure setup
├─ PicoClaw hardening (AI safety)
├─ Frontend foundation
└─ [GATE: Security Audit]

Phase 2: Core Features                   (Weeks 11-22, ~10-12 weeks)
├─ Transcription engine
├─ Teams integration
├─ Real-time transcript buffer
├─ Summarization module
├─ Chat interface
└─ [GATE: End-to-End Integration Test]

Phase 3: Hardening & Integration         (Weeks 23-30, ~6-8 weeks)
├─ RAG therapeutic interventions
├─ HIPAA compliance hardening
├─ Data lifecycle management
├─ Performance optimization
└─ [GATE: Security Hardening Review]

Phase 4: Testing & Launch Prep           (Weeks 31-36, ~4-6 weeks)
├─ QA and load testing
├─ Documentation
├─ Beta pilot program
├─ Production deployment readiness
└─ [GATE: Launch Approval]

MVP LAUNCH ✓


Technology Stack (Summary)
Layer
Technology
AI/LLM
PicoClaw (hardened for clinical safety)
Transcription
Whisper (local, 99% accurate)
Backend
Go + Chi (API), Python FastAPI (ML)
Frontend
React 18 + TypeScript + Tailwind CSS
Database
SQLite (local) + Chroma (vector DB)
Embeddings
Sentence Transformers (local)
Deployment
Docker + Kubernetes
Security
AES-256 encryption, local key derivation, audit logging

Core Principle: Everything runs locally. Zero cloud transmission of PII.

Why This Approach Works
1. Local-First Architecture
Pro: Maximum privacy, HIPAA-compliant by design, no cloud vendor lock-in
Con: Higher infrastructure cost for clients; limited scalability
Decision: Privacy > Scale for MVP. Scale horizontally (multiple servers) later
2. Hardened PicoClaw Instead of Cloud LLM
Pro: Zero API costs, complete data sovereignty, deterministic safety
Con: Requires ML engineering effort; may need fallback to cloud if safety hardening fails
Decision: Worth the effort for privacy-first positioning. Have OpenAI API as fallback.
3. Teams First (Not Zoom/Meet)
Pro: ~85% of enterprise healthcare uses Teams; mature API
Con: Limits addressable market initially
Decision: Do one integration really well. Others can follow post-launch.
4. Strict Phase Gates
Pro: Prevents scope creep, ensures security testing happens, maintains stakeholder alignment
Con: Requires disciplined change management
Decision: Non-negotiable for a healthcare compliance project.

Critical Success Factors
Technical
✓ PicoClaw hardening - Must achieve deterministic, safe outputs
 ✓ Transcription accuracy - Must hit ≥95% on clinical dialogue
 ✓ Real-time performance - Chat responses <5s or therapists won't use
 ✓ Data encryption - Must withstand security audit scrutiny
Organizational
✓ Executive commitment - 6 FTE for 36 weeks is non-negotiable
 ✓ Security discipline - Phase gates must not be shortcuts
 ✓ Clinical input - Need therapist feedback early and often
 ✓ Compliance engagement - Don't wait until Phase 3 to talk to lawyers
Market
✓ Beta user cohort - Identify 5-10 pilot sites by Week 10
 ✓ Outcome metrics - Define what "success" looks like for early users
 ✓ Go-to-market strategy - Parallel to development, not after launch

Top 5 Risks & Mitigations
#
Risk
Prob
Impact
Mitigation
1
Transcription <95% accuracy
40%
High
Early validation Week 8; have fine-tuning + human-review fallback
2
PicoClaw hardening delays
50%
High
Deep code review Week 2; fallback to cloud LLM API
3
Teams API rate limiting
30%
Medium
Implement backoff/retry; request quota increase Week 2
4
HIPAA audit failures
15%
Critical
Compliance counsel Week 2; weekly checklist; internal audit Week 26
5
Scope creep
70%
Medium
Strict change control; Phase gates only; post-MVP backlog

Mitigation Owner: Project Manager (with escalation to Tech Lead / Compliance Officer)

Resource & Budget Estimate
Personnel
Role
Count
Months
Cost/FTE
Total
Tech Lead
1
8
$200K/yr
$133K
Backend Engineer
2
8
$180K/yr
$240K
ML Engineer
1
8
$200K/yr
$133K
Frontend Engineer
1
8
$160K/yr
$107K
Project Manager
1
8
$150K/yr
$100K
QA Engineer
1
6
$120K/yr
$60K
Subtotal
6 FTE
8 months


$773K

Infrastructure & Tools
Development environment (Docker, Git, CI/CD): $2K
External security audit (penetration testing): $15K
Legal/compliance counsel (FTE equivalent): $30K
Cloud hosting (pilot/testing): $8K
Equipment (MacBooks, server): $40K
Software licenses (as-needed): $5K
Subtotal: $100K
Contingency (15%)
Contingency Reserve: $130K
Total Estimated Budget: $1.0M - $1.2M

Decision Points Needed Now
By Next Week
Executive approval of timeline and budget (Phase 1 commitment: $200K)
Team leads identified (Tech Lead, PM at minimum)
Steering committee formed (Weekly sync starting Week 1)
By Week 2
Compliance counsel engaged (HIPAA roadmap + BAA review)
Beta user cohort recruitment begins (target: identified by Week 10)
PicoClaw technical deep dive scheduled (assess hardening feasibility)
By Week 4
Phase 1 deliverables tracked (Infrastructure, PicoClaw initial results, UI components)
Security audit firm pre-screened (Phase 3 penetration test)
Scope freeze policy documented (change control process)

Success Metrics (What "Done" Looks Like)
For Stakeholders
✓ MVP launches on schedule (Week 36)
✓ Zero critical security findings in final audit
✓ HIPAA BAA signed before launch
✓ 5+ pilot sites onboarded with ≥4/5 satisfaction rating
For Users
✓ Transcription is ≥95% accurate (saves 30% of documentation time)
✓ Chat responses are <5s (feels responsive, not annoying)
✓ Notes are clinically useful (rated ≥4/5 by therapists)
✓ System "just works" (uptime ≥99.5%)
For the Business
✓ Product is defensible (strong IP, HIPAA-first positioning)
✓ Market traction (5+ paying customers identified)
✓ Scalable architecture (ready for subsequent release cycles)
✓ Team retention (6 FTE stays through launch + 8 weeks post-launch)

What Success Looks Like in 12 Months
Month 6 (Week 36): MVP launched to 5 beta sites
 Month 8: 20+ pilot sites live, iterating on Tier 2 features
 Month 10: Revenue-generating customers, scaling to 50+ sessions/month
 Month 12: Established product-market fit, Series A ready (if that's the direction)

Questions for Clarification
Budget ceiling? Is $1.0-1.2M realistic for your organization?
Team availability? Can you commit 6 FTE for 36 weeks starting in 2-3 weeks?
Regulatory strategy? Will Kerrigan be CE-marked (Europe) or FDA-cleared long-term?
Business model? Per-user SaaS, per-organization license, or other?
Scaling approach? Single-instance deployment per customer, or shared infrastructure?

Next Actions (This Week)
[ ] Schedule 30-min executive alignment meeting to approve roadmap
[ ] Identify Tech Lead and Project Manager
[ ] Form steering committee (CEO/CTO, Tech Lead, PM, Finance, Legal)
[ ] Schedule Phase 1 kickoff for Week 1 (with full team + leadership)

Prepared by: [Your Name]
 Date: February 12, 2026
 Approval: ____________________
 Title: ______________

