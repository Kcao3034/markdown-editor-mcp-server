# Implementation Plan - Fix Smithery Build

The Smithery build is failing. We need to ensure the build environment is clean and correctly configured.

## Proposed Changes

### Docker Configuration
1.  **Create `.dockerignore`**: Exclude `.git`, `tests`, and cache directories to reduce build context size and prevent potential conflicts.

### Smithery Configuration
2.  **Update `smithery.yaml`**:
    *   Review `install` section. It currently requests an editable install (`-e .`) which might be problematic in some CI/build environments that expect a static artifact.
    *   Ensure `run` configuration aligns with the installed package.

### Package Configuration
3.  **Verify `pyproject.toml`**: Ensure it correctly identifies packages so `pip install .` works reliably.

## Verification Plan

1.  Run `docker build .` to verify container build locally.
2.  Verify `smithery.yaml` aligns with standard MCP server configurations (if documentation or patterns are available).
