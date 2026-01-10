# Refactor Engine Architecture, Type Safety, and Test Infrastructure

## Summary
This PR implements a significant architectural overhaul of the game engine, transitioning from runtime parsing to a build-time compilation model. It also enforces strict type safety using Pydantic and Mypy, refactors the test suite to use centralized fixtures, and cleans up technical debt by reorganizing the codebase structure.

## Key Changes

### 🏗️ Architecture & Compilation
- **New Compiler Module**: Created `compiler/` to handle card parsing at build time.
- **Build-Time Processing**: Implemented `compiler/main.py` ("Phase 7") to compile raw `cards.json` into optimized `items.json` / `cards_compiled.json`.
- **Pydantic Models**: Defined strict data models for Cards and Abilities in `engine/models/`, replacing ad-hoc dictionaries.
- **Data Loader Update**: Updated `CardDataLoader` to consume pre-compiled data, improving startup robustness.

### 🔧 Refactoring & Cleanup
- **Directory Restructure**: Separated code into clear domains: `engine/`, `backend/`, `compiler/`, and `tests/`.
- **Legacy Removal**: Deleted the facade `engine/game/ability.py` and consolidated imports to `engine.models.*`.
- **Test Organization**:
    - Centralized shared fixtures and steps in `engine/tests/conftest.py`.
    - Removed fragile star imports (`from ... import *`) in test files.
    - Moved parser tests to `compiler/tests/`.

### 🛡️ Type Safety & Quality
- **Mypy Compliance**: Achieved passing `mypy` checks (strict mode) across `engine/` and `compiler/`.
    - Fixed type errors in `game_state.py` (e.g., `.group` vs `.groups` attribute access).
    - Updated test data to match strict Pydantic models (e.g., using `Group` enums instead of strings).
- **Tooling**:
    - Configured `pre-commit` hooks with `ruff` and `mypy`.
    - Enabled `pydantic.mypy` plugin for correct type inference.

## Breaking Changes
- **Build Step Required**: Running the game engine now requires the compiled card data. Run `uv run compiler/main.py` before starting the server or running tests.

## Verification
- **Tests**: `uv run pytest` passes (imports resolving correctly via `conftest.py`).
- **Linting**: `ruff` checks pass.
- **Type Checking**: `mypy` checks pass.
