# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-context-api

## Roadmap

### core-context-api — Core Context API - PRODUCT.md/DESIGN.md loading and validation

Status: done

Acceptance:
- FastAPI server starts and serves health endpoint
- POST /context/load accepts project root and returns parsed PRODUCT.md and DESIGN.md
- Validates file existence and returns structured context
- React frontend can call the API and display loaded context

Implementation: `backend/main.py`, `backend/context_loader.py`, `frontend/src/App.tsx`, `frontend/src/api.ts`

Tests: `backend/test_context_loader.py`, `frontend/src/App.test.tsx`

### browser-extension-copy-issues — Browser Extension - Copy All Issues (Issue #829)

Status: planned

Acceptance:
- Extension popup has 'Copy all issues' button after scan
- Copied output includes page URL, total findings, each issue's name/explanation/selector/guidance
- Confirmation toast shown on successful copy

Implementation: `extension/popup.ts`, `extension/manifest.json`

Tests: `extension/test_copy_issues.ts`

### gitignore-init-cleanup — Gitignore guidance and clean command (Issue #834)

Status: planned

Acceptance:
- /init suggests .gitignore entries for .impeccable/
- /clean command removes stale generated files
- Works with worktrees

Implementation: `backend/commands/init.py`, `backend/commands/clean.py`

Tests: `backend/test_init_clean.py`

### design-sidecar-fingerprint — Design sidecar fingerprint validation (Issue #846)

Status: planned

Acceptance:
- SHA-256 of DESIGN.md stored in sidecar on generation
- Staleness check compares content fingerprint, not mtime
- Legacy sidecars without fingerprint marked 'unverified' not 'stale'

Implementation: `backend/context_loader.py`, `backend/staleness.py`

Tests: `backend/test_staleness.py`

### configurable-context-paths — Configurable PRODUCT.md/DESIGN.md paths (Issue #1022)

Status: planned

Acceptance:
- contextFiles.config with independent product/design paths
- Shared resolver across context, live, and design tooling
- Path validation with clear errors, backward compatible

Implementation: `backend/config.py`, `backend/context_resolver.py`

Tests: `backend/test_config_resolver.py`

### rtl-audit-physical-properties — Audit: flag physical CSS properties on RTL pages (Issue #1113)

Status: planned

Acceptance:
- New Internationalization audit section (6th dimension)
- Flags margin/padding/border/text-align/float/left/right on dir=rtl
- Informational on LTR pages, score rescales from /20 to /24

Implementation: `backend/audit/rtl_check.py`, `backend/audit/scoring.py`

Tests: `backend/test_rtl_audit.py`

