# cobalt-hub-145-alan-vo — Alan Vo

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


The design language that makes your AI harness better at design.

AI/ML developer tools for design-system validation, context management, and browser extension integration.

## Quick Start

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`

- Health check: `GET /health`
- Load context: `POST /context/load`

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173` (proxies API to backend)

### Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## API Reference

### `GET /health`

Returns server health status.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### `POST /context/load`

Load PRODUCT.md and DESIGN.md from a project root.

**Request:**
```json
{
  "project_root": "/path/to/project",
  "product_path": "governance/context/product.md",  // optional
  "design_path": "docs/brand/design.md"             // optional
}
```

**Response:**
```json
{
  "project_root": "/path/to/project",
  "product": {
    "path": "/path/to/project/PRODUCT.md",
    "content": "# Product\n\nDescription...",
    "sha256": "abc123...",
    "size_bytes": 1234
  },
  "design": {
    "path": "/path/to/project/DESIGN.md",
    "content": "# Design\n\nDescription...",
    "sha256": "def456...",
    "size_bytes": 5678
  },
  "warnings": []
}
```

If a file is not found, it will be `null` and a warning will be added to `warnings`.

Custom paths take precedence over auto-discovery. If a custom path is specified but not found, returns 400 error.

## Features

- **Context Loading**: Load PRODUCT.md and DESIGN.md with configurable paths (Issue #1022)
- **Content Fingerprinting**: SHA-256 hashes for staleness detection (Issue #846)
- **Browser Extension**: Copy all detected issues for AI agents (Issue #829)
- **Gitignore Guidance**: Init and clean commands for generated files (Issue #834)
- **RTL Audit**: Flag physical CSS properties on RTL pages (Issue #1113)

## Project Structure

```
cobalt-hub-145-alan-vo/
├── backend/                 # FastAPI backend
│   ├── main.py             # API entry point
│   ├── context_loader.py   # Context loading logic
│   ├── test_context_loader.py
│   └── requirements.txt
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── App.tsx         # Main component
│   │   ├── App.test.tsx    # Component tests
│   │   ├── api.ts          # API client
│   │   └── main.tsx        # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── feature-plan.json       # Feature tracking
└── PLAN.md                 # Implementation plan
```

## Development

See `PLAN.md` for current feature status and roadmap.

Maintainer: Alan Vo <alanvo@gmail.com>
