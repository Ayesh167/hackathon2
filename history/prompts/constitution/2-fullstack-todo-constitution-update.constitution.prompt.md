---
id: 2
title: "Fullstack Todo Constitution Update"
stage: "constitution"
date_iso: "2026-02-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-app"
branch: "master"
user: "Ayesha shafi"
command: "/sp.constitution Title: Full-Stack Todo Web Application Master Constitution"
labels: ["constitution", "governance", "spec-kit-plus"]
spec: null
ticket: null
adr: null
pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
prompt_text: |
  Title: Full-Stack Todo Web Application Master Constitution

  Purpose:
  Define governance, rules, responsibilities, skills, workflow, and technical standards for building the Todo Full-Stack Web Application using Spec-Kit Plus, Claude Code, and Agentic Dev Stack. This constitution ensures all agents, skills, specs, frontend, backend, API, database, and authentication work in a coordinated, hackathon-ready manner.

  Scope:
  Applies to the entire project:
  - /specs
  - /frontend
  - /backend
  - /agents
  - CLAUDE.md files
  - Environment configuration
  - Docker / deployment setup

  ---

  ## 1. Agents and Responsibilities

  All agents listed below **must follow CLAUDE.md rules** and the specifications in `/specs`.
  All skills must be deterministic, reusable, and reference specs.

  1. **Spec Architect**
     - Owns all specification writing in `/specs`
     - Defines features, API endpoints, database schema, UI components
     - Maintains spec integrity and approves any updates
     - Skills:
       - Write/Update Feature Specs
       - Write/Update API Specs
       - Write/Update Database Schema
       - Write/Update UI Specs

  2. **Planner Agent**
     - Converts specs into actionable development plans
     - Breaks plan into tasks for backend, frontend, and auth
     - Ensures task dependencies are respected
     - Skills:
       - Generate Development Plan
       - Task Breakdown
       - Phase & Dependency Mapping

  3. **Backend Engineer**
     - Implements FastAPI backend
     - Uses SQLModel for ORM
     - Integrates Neon PostgreSQL
     - Implements all REST API endpoints as per specs
     - Enforces JWT authentication and user isolation
     - Skills:
       - Create/Read/Update/Delete Task APIs
       - Toggle Task Completion
       - Validate JWT Token
       - Filter Tasks by Authenticated User
       - Handle API Errors per spec

  4. **Frontend Engineer**
     - Implements Next.js frontend (App Router)
     - TypeScript + Tailwind CSS
     - Integrates with Better Auth for login/signup
     - Calls backend APIs via `/lib/api.ts`
     - Implements responsive UI
     - Skills:
       - Display Tasks List
       - Task CRUD UI
       - Attach JWT to API Requests
       - Responsive Page Layout
       - Authentication Integration

  5. **Auth & Security Agent**
     - Configures Better Auth to issue JWT tokens
     - Verifies JWT in backend for every request
     - Ensures user isolation and token expiry
     - Reports violations to Reviewer
     - Skills:
       - Issue JWT Tokens
       - Validate JWT Tokens
       - Enforce User Isolation
       - Security Compliance Checks

  6. **Reviewer Agent**
     - Validates that implementation complies with specs
     - Checks frontend, backend, auth, and database
     - Reports missing features or errors
     - Approves deployment readiness
     - Skills:
       - Spec Compliance Validation
       - Feature Coverage Audit
       - Security Audit
       - Phase Readiness Approval

  ---

  ## 2. Workflow Rules

  - Follow **Agentic Dev Stack**:
    `Spec → Plan → Task Breakdown → Implement via Agents → Review → Iterate`
  - No manual coding outside agent skills
  - Agents communicate via `/agents/*/CLAUDE.md`, `/specs`, and plans
  - Skills are **self-contained**; outputs of one skill feed into another
  - Reviewer agent is **final authority** for spec compliance

  ---

  ## 3. Spec-Kit Plus Rules

  - All features, APIs, database schema, and UI components must be referenced via `@specs/...`
  - CLAUDE.md files in root, frontend, backend, and agents define operational rules
  - Changes to specs must be approved by Spec Architect
  - Agents may not implement functionality outside the approved specs

  ---

  ## 4. Backend Rules

  - FastAPI under `/backend`
  - SQLModel ORM only
  - Neon PostgreSQL for persistent storage
  - REST API endpoints:
    - GET /api/{user_id}/tasks
    - POST /api/{user_id}/tasks
    - GET /api/{user_id}/tasks/{id}
    - PUT /api/{user_id}/tasks/{id}
    - DELETE /api/{user_id}/tasks/{id}
    - PATCH /api/{user_id}/tasks/{id}/complete
  - All routes must:
    - Require JWT token in `Authorization` header
    - Return 401 Unauthorized if token missing/invalid
    - Filter all queries by authenticated user
  - Connection string and JWT secret come from environment variables:
    - `DATABASE_URL`
    - `BETTER_AUTH_SECRET`

  ---

  ## 5. Frontend Rules

  - Next.js 16+ (App Router) with TypeScript
  - Tailwind CSS for styling
  - Server components by default; client components for interactivity
  - `/lib/api.ts` used for all backend calls
  - JWT attached to all API requests
  - Better Auth login/signup integrated
  - Responsive UI components according to specs

  ---

  ## 6. Authentication & Security

  - Better Auth issues JWT tokens
  - Frontend includes token in `Authorization: Bearer <token>`
  - Backend verifies JWT using `BETTER_AUTH_SECRET`
  - Only authenticated users can access tasks
  - User cannot access/modify other users' tasks
  - JWT tokens expire automatically (e.g., 7 days)
  - All security violations are reported to Reviewer agent

  ---

  ## 7. Monorepo Organization
  hackathon-todo/
  ├── .spec-kit/
  │ └── config.yaml
  ├── specs/
  │ ├── overview.md
  │ ├── architecture.md
  │ ├── features/
  │ │ ├── task-crud.md
  │ │ ├── authentication.md
  │ │ └── chatbot.md
  │ ├── api/
  │ │ ├── rest-endpoints.md
  │ │ └── mcp-tools.md
  │ ├── database/
  │ │ └── schema.md
  │ └── ui/
  │ ├── components.md
  │ └── pages.md
  ├── frontend/
  │ └── CLAUDE.md
  ├── backend/
  │ └── CLAUDE.md
  ├── agents/
  │ ├── spec-architect/
  │ ├── planner-agent/
  │ ├── backend-engineer/
  │ ├── frontend-engineer/
  │ ├── auth-security-agent/
  │ └── reviewer-agent/
  ├── docker-compose.yml
  ├── CLAUDE.md
  └── README.md

  ---


  ## 8. Review & Validation


  - Reviewer agent confirms:
    - All REST APIs match spec
    - Frontend displays tasks correctly per user
    - JWT authentication works and user isolation enforced
    - Spec compliance for all features
    - Project is hackathon-ready


  ---


  ## 9. Constraints


  - No human coding outside agent skills
  - All implementation references `/specs` via `@specs/...`
  - Agents must follow CLAUDE.md rules
  - Security and auth rules are mandatory
  - Workflow must be deterministic and reproducible


  ---


  ### Outcome


  - Full-stack Todo Web App implemented via agents and skills
  - Multi-user support with JWT authentication
  - Spec-driven, secure, maintainable, hackathon-ready
response_text: |
  Successfully updated the project constitution to reflect the Full-Stack Todo Web Application Master Constitution. The new constitution defines governance, rules, responsibilities, skills, workflow, and technical standards for building the Todo Full-Stack Web Application using Spec-Kit Plus, Claude Code, and Agentic Dev Stack. It includes detailed sections on agent responsibilities, workflow rules, backend/frontend rules, authentication & security requirements, monorepo organization, and review/validation processes. The version was updated from 1.0.0 to 1.1.0 to reflect the addition of comprehensive principles and requirements.
outcome: "Successfully updated constitution with comprehensive agent-based development guidelines"
evaluation: "Constitution now properly defines all 6 agents with their responsibilities, workflow rules, technical standards, and governance procedures as specified in the requirements"
---

# PHR: Full-Stack Todo Web Application Master Constitution Update

## Overview
Updated the project constitution to implement the Full-Stack Todo Web Application Master Constitution as specified.

## Changes Made
1. Replaced the template constitution with the complete implementation-specific constitution
2. Added 6 core principles covering:
   - Agent-Based Development with Spec-Kit Plus
   - Defined Agent Responsibilities and Skills
   - Backend Technical Standards
   - Frontend Technical Standards
   - Authentication & Security Requirements
   - Comprehensive Review & Validation
3. Added additional technical requirements sections
4. Added development workflow sections
5. Updated governance section with comprehensive rules

## Validation
- All 6 agents properly defined with their specific responsibilities
- Technical standards for backend and frontend clearly specified
- Authentication and security requirements detailed
- Workflow rules align with Agentic Dev Stack methodology
- Governance section includes all required constraints
- Version updated from 1.0.0 to 1.1.0 to reflect significant additions