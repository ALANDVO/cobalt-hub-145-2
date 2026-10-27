# Changelog

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-10-26

### Added
- **Core Context API** - FastAPI backend with context loading functionality
  - `GET /health` - Health check endpoint
  - `POST /context/load` - Load PRODUCT.md and DESIGN.md from project root
  - Configurable custom paths for product and design documents
  - Case-insensitive file discovery in project root and common subdirectories
  - SHA-256 content fingerprinting for staleness detection
  - Proper error handling with descriptive messages

- **React Frontend** - Vite + React + TypeScript frontend
  - Form to input project root and optional custom paths
  - Displays loaded context files with content, SHA-256, and size
  - Shows warnings for missing files
  - Loading state and error handling

- **Testing**
  - 16 backend unit tests (pytest) covering context loading, file discovery, SHA-256 computation
  - 7 frontend component tests (Vitest + Testing Library) covering form rendering, API integration, error states

### Architecture
- Backend: FastAPI 0.115, Pydantic 2.9, Python 3.12
- Frontend: React 18, TypeScript 5.6, Vite 5.4
- Testing: pytest 8.3, Vitest 2.1, Testing Library

### Files Added
```
backend/
├── main.py                 # FastAPI application
├── context_loader.py       # Context loading logic
├── test_context_loader.py  # Unit tests (16 tests)
├── requirements.txt
└── venv/                   # Virtual environment

frontend/
├── src/
│   ├── App.tsx             # Main component
│   ├── App.test.tsx        # Component tests (7 tests)
│   ├── api.ts              # API client
│   ├── main.tsx            # Entry point
│   └── test-setup.ts       # Test setup
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── tsconfig.node.json

feature-plan.json           # Feature tracking
PLAN.md                     # Implementation plan
README.md                   # Documentation
```

### Acceptance Criteria Met
- ✅ FastAPI server starts and serves health endpoint
- ✅ POST `/context/load` accepts project root and returns parsed PRODUCT.md and DESIGN.md
- ✅ Validates file existence and returns structured context with SHA-256
- ✅ React frontend calls the API and displays loaded context
- ✅ All 16 backend tests pass
- ✅ All 7 frontend tests pass
