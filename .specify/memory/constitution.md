<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → Full-Stack Todo Web Application Master Constitution
Added sections: Agents and Responsibilities, Workflow Rules, Spec-Kit Plus Rules, Backend Rules, Frontend Rules, Authentication & Security, Monorepo Organization, Review & Validation, Constraints
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Full-Stack Todo Web Application Master Constitution

## Core Principles

### Agent-Based Development with Spec-Kit Plus
All development follows the Agentic Dev Stack methodology: Spec → Plan → Task Breakdown → Implement via Agents → Review → Iterate. No manual coding outside agent skills. All features, APIs, database schema, and UI components must be referenced via `@specs/...`. Changes to specs must be approved by Spec Architect. Agents may not implement functionality outside the approved specs.

### Defined Agent Responsibilities and Skills
Development is coordinated through 6 specialized agents with clearly defined roles: Spec Architect (owns all specification writing), Planner Agent (converts specs to development plans), Backend Engineer (implements FastAPI backend with SQLModel and JWT authentication), Frontend Engineer (implements Next.js frontend with Better Auth integration), Auth & Security Agent (configures JWT tokens and enforces user isolation), and Reviewer Agent (validates spec compliance and deployment readiness). All skills must be deterministic, reusable, and reference specs.

### Backend Technical Standards
Backend implements FastAPI under `/backend` using SQLModel ORM only with Neon PostgreSQL for persistent storage. REST API endpoints include GET/POST/PUT/DELETE/PATCH operations for tasks filtered by authenticated user. All routes require JWT token in `Authorization` header, return 401 Unauthorized if token missing/invalid, and filter queries by authenticated user. Connection string and JWT secret come from environment variables (`DATABASE_URL`, `BETTER_AUTH_SECRET`).

### Frontend Technical Standards
Frontend implements Next.js 16+ (App Router) with TypeScript and Tailwind CSS. Uses server components by default with client components for interactivity. All backend calls use `/lib/api.ts` with JWT attached to requests. Better Auth login/signup integrated with responsive UI components according to specs.

### Authentication & Security Requirements
Better Auth issues JWT tokens that frontend includes in `Authorization: Bearer <token>`. Backend verifies JWT using `BETTER_AUTH_SECRET`. Only authenticated users can access tasks, with user isolation enforced (cannot access/modify other users' tasks). JWT tokens expire automatically (e.g., 7 days). All security violations reported to Reviewer agent.

### Comprehensive Review & Validation
Reviewer agent validates implementation compliance with specs by checking frontend, backend, auth, and database. Confirms all REST APIs match spec, frontend displays tasks correctly per user, JWT authentication works with user isolation enforced, spec compliance for all features, and project is hackathon-ready.

## Additional Technical Requirements

### Workflow Rules
Follow Agentic Dev Stack: Spec → Plan → Task Breakdown → Implement via Agents → Review → Iterate. No manual coding outside agent skills. Agents communicate via `/agents/*/CLAUDE.md`, `/specs`, and plans. Skills are self-contained with outputs of one skill feeding into another. Reviewer agent is final authority for spec compliance.

### Spec-Kit Plus Rules
All features, APIs, database schema, and UI components must be referenced via `@specs/...`. CLAUDE.md files in root, frontend, backend, and agents define operational rules. Changes to specs must be approved by Spec Architect. Agents may not implement functionality outside the approved specs.

### Monorepo Organization
Repository structure follows standardized organization with specs/, frontend/, backend/, agents/, and configuration files organized under a clear hierarchy that supports the agentic development workflow.

## Development Workflow

### Implementation Process
1. Spec Architect creates comprehensive specifications in `/specs`
2. Planner Agent converts specs into actionable development plans
3. Tasks are broken down for backend, frontend, and auth implementation
4. Specialized agents implement according to their defined skills
5. Auth & Security Agent ensures proper authentication and security measures
6. Reviewer Agent validates spec compliance and deployment readiness

### Quality Assurance
All implementations must undergo comprehensive validation by the Reviewer Agent who confirms:
- All REST APIs match spec
- Frontend displays tasks correctly per user
- JWT authentication works and user isolation enforced
- Spec compliance for all features
- Project is hackathon-ready

## Governance

All agents must follow CLAUDE.md rules and the specifications in `/specs`. No human coding outside agent skills is permitted. All implementation references `/specs` via `@specs/...`. Agents must follow CLAUDE.md rules. Security and auth rules are mandatory. Workflow must be deterministic and reproducible. The Reviewer agent has final authority for spec compliance and deployment approval.

**Version**: 1.1.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06