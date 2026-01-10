# Lovecasim Project Context

## Overview
This project is a web-based implementation of the "Love Live! School Idol Collection" Trading Card Game (TCG).

## Architecture
The project follows a modular architecture separating the game engine, backend server, and frontend assets.

- **Engine** (`engine/`): Core game logic, state management, and data models. Type-safe and fully tested.
- **Backend** (`server.py`): Flask server exposing the game via API.
- **Frontend** (`web_ui/`): Vanilla HTML/JS interface.
- **Compiler** (`compiler/`): Utilities for processing raw card data into `cards_compiled.json`.

## Key Directories
| Directory | Purpose |
|O---|---|
| `engine/game/` | Game state, logic, and turn orchestration. |
| `engine/models/` | Pydantic models for Cards, Effects, and Actions. |
| `engine/tests/` | Comprehensive test suite (Pytest + BDD). |
| `data/` | JSON data source (`cards.json`, `rule_map.json`, `cards_compiled.json`). |
| `web_ui/` | Static assets (CSS, JS, Images). |

## Development Standards

### Static Analysis
We enforce high code quality using pre-commit hooks.
- **Linting & Formatting:** `ruff` (replaces black/isort/flake8).
- **Type Checking:** `mypy` (strict mode compliant).
- **Automation:** `pre-commit` runs these checks on every commit.

**Commands:**
```bash
# Run all checks
uv run pre-commit run --all-files

# Manual checks
uv run ruff check .
uv run mypy .
```

### Testing
Tests are run using **Pytest**, though some legacy tests still utilize `unittest.TestCase`.

- **Run all tests:** `uv run pytest`
- **New Tests:** MUST use strict `pytest` style (fixtures, functions), NOT `unittest.TestCase`.
- **Structure:**
    - `engine/tests/features/`: BDD tests (Gherkin syntax).
    - `engine/tests/steps/`: BDD step definitions.
    - `engine/tests/cards/`: Card ability verification.
    - `engine/tests/mechanics/`: Core mechanics (Energy, Turns, Zones).
    - `engine/tests/logic/`: Game rules and scoring logic.
    - `engine/tests/scenarios/`: Complex integration scenarios.
    - `engine/tests/data/`: Data integrity and loading tests.

## Logic Quirks & Learnings
- **Pre-compiled Data:** The engine now relies on `cards_compiled.json` for performance and consistency.
- **GameState Class Vars:** `member_db` and `live_db` are class-level for memory efficiency; tests must handle this.
- **Conditionals:** `GROUP_FILTER` checks prioritize `context` (e.g., revealed card) over global state.
- **Arrays:** `tapped_energy` is a fixed-size NumPy array.
- **Action IDs:**
    - **Color Select:** 580-585 (Pink, Red, Yellow, Green, Blue, Purple)
    - **Target Opponent:** 600-602 (Stage Slots)
