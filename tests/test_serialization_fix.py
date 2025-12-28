"""Tests to verify that read-only tools return actual JSON data, not static messages.

This test verifies the fix for the serialization bug in v0.1.5 where
list_directory, get_document_structure, search_text, get_context, and read_element
returned only static messages like "Structure extracted" instead of actual data.
"""

import asyncio
import json
import tempfile
from pathlib import Path

import pytest

from markdown_editor.server import call_tool, list_tools


@pytest.fixture
def temp_md_file():
    """Create a temporary markdown file for testing."""
    content = """# Test Document

This is a test paragraph with some searchable text.

## Section One

First section content here.

## Section Two

Second section content with unique phrase.
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as f:
        f.write(content)
        return f.name


@pytest.fixture
def cleanup_file(temp_md_file):
    """Clean up temporary file after test."""
    yield temp_md_file
    Path(temp_md_file).unlink(missing_ok=True)


class TestSerializationFix:
    """Tests for the serialization bug fix."""

    @pytest.mark.asyncio
    async def test_list_directory_returns_json(self):
        """list_directory should return JSON with items array, not 'N files found'."""
        result = await call_tool("list_directory", {"path": "."})
        
        assert "content" in result
        assert len(result["content"]) > 0
        text = result["content"][0].text
        
        # Should be valid JSON, not a static message
        parsed = json.loads(text)
        assert "items" in parsed
        assert isinstance(parsed["items"], list)

    @pytest.mark.asyncio
    async def test_get_document_structure_returns_json(self, cleanup_file):
        """get_document_structure should return JSON with structure, not 'Structure extracted'."""
        result = await call_tool(
            "get_document_structure", {"file_path": cleanup_file}
        )
        
        assert "content" in result
        text = result["content"][0].text
        
        # Should NOT be just "Structure extracted"
        assert text != "Structure extracted"
        
        # Should be valid JSON with structure data
        parsed = json.loads(text)
        assert "structure" in parsed

    @pytest.mark.asyncio
    async def test_search_text_returns_json(self, cleanup_file):
        """search_text should return JSON with results, not 'Found X matches'."""
        result = await call_tool(
            "search_text", 
            {"file_path": cleanup_file, "query": "searchable"}
        )
        
        assert "content" in result
        text = result["content"][0].text
        
        # Should NOT be just "Found X matches"
        assert not text.startswith("Found")
        
        # Should be valid JSON with results
        parsed = json.loads(text)
        assert "results" in parsed
        assert "count" in parsed

    @pytest.mark.asyncio
    async def test_get_context_returns_json(self, cleanup_file):
        """get_context should return JSON with context data, not 'Context extracted'."""
        result = await call_tool(
            "get_context",
            {"file_path": cleanup_file, "path": "Test Document"}
        )
        
        assert "content" in result
        text = result["content"][0].text
        
        # Should NOT be just "Context extracted"
        assert text != "Context extracted"
        
        # Should be valid JSON
        parsed = json.loads(text)
        # Should have context-related fields (target, before, after or error)
        assert isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_read_element_returns_json(self, cleanup_file):
        """read_element should return JSON with element data, not 'Element read'."""
        result = await call_tool(
            "read_element",
            {"file_path": cleanup_file, "path": "Test Document"}
        )
        
        assert "content" in result
        text = result["content"][0].text
        
        # Should NOT be just "Element read"
        assert text != "Element read"
        
        # Should be valid JSON
        parsed = json.loads(text)
        assert isinstance(parsed, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
