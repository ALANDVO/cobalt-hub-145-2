"""Tests for context_loader module."""
import tempfile
import os
from pathlib import Path
import pytest

from context_loader import load_context, ContextLoadRequest, _read_file, _find_file


class TestReadFile:
    """Tests for _read_file function."""

    def test_read_file_computes_sha256(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\nContent here.")
            temp_path = Path(f.name)

        try:
            result = _read_file(temp_path)
            assert result.path == str(temp_path)
            assert result.content == "# Test\n\nContent here."
            assert result.size_bytes > 0
            assert len(result.sha256) == 64  # SHA-256 hex length
            # Verify it's a valid hex string
            int(result.sha256, 16)
        finally:
            temp_path.unlink()

    def test_read_file_normalizes_line_endings(self):
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".md", delete=False) as f:
            f.write(b"# Test\r\nContent\r\nEnd\r")
            temp_path = Path(f.name)

        try:
            result = _read_file(temp_path)
            # Content should have normalized line endings
            assert "\r" not in result.content
            assert result.content == "# Test\nContent\nEnd\n"
        finally:
            temp_path.unlink()

    def test_read_file_consistent_hash(self):
        """Same content should produce same hash regardless of line endings."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, newline="") as f1:
            f1.write("# Test\nContent\n")
            path1 = Path(f1.name)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, newline="") as f2:
            f2.write("# Test\r\nContent\r\n")
            path2 = Path(f2.name)

        try:
            result1 = _read_file(path1)
            result2 = _read_file(path2)
            assert result1.sha256 == result2.sha256
        finally:
            path1.unlink()
            path2.unlink()


class TestFindFile:
    """Tests for _find_file function."""

    def test_find_custom_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            custom = root / "custom" / "product.md"
            custom.parent.mkdir(parents=True)
            custom.write_text("# Custom Product")

            result = _find_file(root, "custom/product.md", ["PRODUCT.md"])
            assert result == custom.resolve()

    def test_find_custom_path_not_found_returns_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            result = _find_file(root, "nonexistent.md", ["PRODUCT.md"])
            assert result is None

    def test_find_default_in_root(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "PRODUCT.md").write_text("# Product")

            result = _find_file(root, None, ["PRODUCT.md"])
            assert result == (root / "PRODUCT.md").resolve()

    def test_find_default_case_insensitive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "product.md").write_text("# Product")

            result = _find_file(root, None, ["PRODUCT.md"])
            assert result == (root / "product.md").resolve()

    def test_find_in_subdirectory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "docs" / "brand" / "design.md").parent.mkdir(parents=True)
            (root / "docs" / "brand" / "design.md").write_text("# Design")

            result = _find_file(root, None, ["DESIGN.md"])
            assert result == (root / "docs" / "brand" / "design.md").resolve()

    def test_find_not_found_returns_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            result = _find_file(root, None, ["PRODUCT.md"])
            assert result is None


class TestLoadContext:
    """Tests for load_context function."""

    def test_load_both_files_from_root(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "PRODUCT.md").write_text("# Product\n\nProduct description.")
            (root / "DESIGN.md").write_text("# Design\n\nDesign description.")

            request = ContextLoadRequest(project_root=str(root))
            result = load_context(request)

            assert result.project_root == str(root.resolve())
            assert result.product is not None
            assert result.product.content == "# Product\n\nProduct description."
            assert result.design is not None
            assert result.design.content == "# Design\n\nDesign description."
            assert len(result.warnings) == 0

    def test_load_with_custom_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "governance" / "context" / "product.md").parent.mkdir(parents=True)
            (root / "governance" / "context" / "product.md").write_text("# Custom Product")
            (root / "docs" / "brand" / "design.md").parent.mkdir(parents=True)
            (root / "docs" / "brand" / "design.md").write_text("# Custom Design")

            request = ContextLoadRequest(
                project_root=str(root),
                product_path="governance/context/product.md",
                design_path="docs/brand/design.md",
            )
            result = load_context(request)

            assert result.product is not None
            assert result.product.content == "# Custom Product"
            assert result.design is not None
            assert result.design.content == "# Custom Design"

    def test_custom_path_not_found_raises_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            request = ContextLoadRequest(
                project_root=str(root),
                product_path="nonexistent.md",
            )
            with pytest.raises(ValueError, match="Custom product path not found"):
                load_context(request)

    def test_project_root_not_found_raises_error(self):
        request = ContextLoadRequest(project_root="/nonexistent/path")
        with pytest.raises(FileNotFoundError, match="Project root not found"):
            load_context(request)

    def test_project_root_not_dir_raises_error(self):
        with tempfile.NamedTemporaryFile() as f:
            request = ContextLoadRequest(project_root=f.name)
            with pytest.raises(ValueError, match="not a directory"):
                load_context(request)

    def test_missing_files_produces_warnings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "PRODUCT.md").write_text("# Product")

            request = ContextLoadRequest(project_root=str(root))
            result = load_context(request)

            assert result.product is not None
            assert result.design is None
            assert len(result.warnings) == 1
            assert "DESIGN.md not found" in result.warnings[0]

    def test_sha256_in_response(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "PRODUCT.md").write_text("# Product")

            request = ContextLoadRequest(project_root=str(root))
            result = load_context(request)

            assert result.product is not None
            assert len(result.product.sha256) == 64
            # Verify it's valid hex
            int(result.product.sha256, 16)
