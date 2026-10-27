"""Context loading and parsing for PRODUCT.md and DESIGN.md."""
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
import hashlib


class ContextLoadRequest(BaseModel):
    """Request to load context files."""
    project_root: str = Field(..., description="Absolute or relative path to project root")
    product_path: Optional[str] = Field(None, description="Custom path to PRODUCT.md (relative to project_root)")
    design_path: Optional[str] = Field(None, description="Custom path to DESIGN.md (relative to project_root)")


class ContextFile(BaseModel):
    """A loaded context file."""
    path: str
    content: str
    sha256: str
    size_bytes: int


class ContextLoadResponse(BaseModel):
    """Response with loaded context files."""
    project_root: str
    product: Optional[ContextFile] = None
    design: Optional[ContextFile] = None
    warnings: list[str] = []


def _read_file(path: Path) -> ContextFile:
    """Read a file and compute its SHA-256."""
    content = path.read_text(encoding="utf-8")
    # Normalize line endings for consistent hashing
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    sha256 = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return ContextFile(
        path=str(path),
        content=content,
        sha256=sha256,
        size_bytes=len(content.encode("utf-8")),
    )


def _find_file(project_root: Path, custom_path: Optional[str], default_names: list[str]) -> Optional[Path]:
    """Find a context file, trying custom path first, then defaults."""
    if custom_path:
        candidate = (project_root / custom_path).resolve()
        if candidate.exists() and candidate.is_file():
            return candidate
        # Custom path specified but not found - don't fall back to defaults
        return None

    # Try default names in project root (case-insensitive)
    for name in default_names:
        candidate = (project_root / name).resolve()
        if candidate.exists() and candidate.is_file():
            return candidate
        # Case-insensitive fallback in project root
        try:
            for entry in project_root.iterdir():
                if entry.is_file() and entry.name.lower() == name.lower():
                    return entry.resolve()
        except OSError:
            pass

    # Try in common subdirectories
    subdirs = ["docs", "governance/context", "docs/brand", "design", "context"]
    for subdir in subdirs:
        subdir_path = (project_root / subdir).resolve()
        if not subdir_path.exists() or not subdir_path.is_dir():
            continue
        for name in default_names:
            candidate = (subdir_path / name).resolve()
            if candidate.exists() and candidate.is_file():
                return candidate
            # Case-insensitive fallback in subdirectory
            try:
                for entry in subdir_path.iterdir():
                    if entry.is_file() and entry.name.lower() == name.lower():
                        return entry.resolve()
            except OSError:
                pass

    return None


def load_context(request: ContextLoadRequest) -> ContextLoadResponse:
    """
    Load PRODUCT.md and DESIGN.md from project root.

    Args:
        request: ContextLoadRequest with project_root and optional custom paths

    Returns:
        ContextLoadResponse with loaded files or None if not found

    Raises:
        FileNotFoundError: If project_root doesn't exist
        ValueError: If custom path specified but file not found
    """
    project_root = Path(request.project_root).resolve()

    if not project_root.exists():
        raise FileNotFoundError(f"Project root not found: {project_root}")

    if not project_root.is_dir():
        raise ValueError(f"Project root is not a directory: {project_root}")

    warnings = []

    # Load PRODUCT.md
    product_path = _find_file(project_root, request.product_path, ["PRODUCT.md", "product.md", "Product.md"])
    product_file = None
    if product_path:
        product_file = _read_file(product_path)
    elif request.product_path:
        raise ValueError(f"Custom product path not found: {request.product_path}")
    else:
        warnings.append("PRODUCT.md not found in project root or common locations")

    # Load DESIGN.md
    design_path = _find_file(project_root, request.design_path, ["DESIGN.md", "design.md", "Design.md"])
    design_file = None
    if design_path:
        design_file = _read_file(design_path)
    elif request.design_path:
        raise ValueError(f"Custom design path not found: {request.design_path}")
    else:
        warnings.append("DESIGN.md not found in project root or common locations")

    return ContextLoadResponse(
        project_root=str(project_root),
        product=product_file,
        design=design_file,
        warnings=warnings,
    )
