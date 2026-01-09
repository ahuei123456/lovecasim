# Lovecasim Project Context

## Overview
This project is a web-based implementation of the "Love Live! School Idol Collection" Trading Card Game (TCG). It features a Python/Flask backend and a vanilla HTML/JS frontend.

## Architecture

### Backend
- **Framework:** Flask (`server.py` is the entry point).
- **Core Logic:** Located in `game/`. `GameState` manages the flow, while `CardDataLoader` loads card definitions.
- **AI/Simulation:** `headless_runner.py` appears to be for AI agent simulation or training.
- **Data:** JSON files in `data/` drive the card database (`cards.json`) and rules (`rule_map.json`).

### Frontend
- **Tech Stack:** Vanilla HTML/JS, with some Vue.js references (`deck_builder_vue.html`).
- **Assets:** Served from `web_ui/`, `css/`, `js/`, and `img/`.
- **Entry Points:** Several HTML files in root (`deck_viewer.html`, `interactive_deck_viewer.html`).

## Key Directories
| Directory | Purpose |
|O---|---|
| `game/` | Core game logic (State, Player, Card models). |
| `web_ui/` | Static assets for the game interface. |
| `docs/` | Detailed documentation on game rules, ability coverage, and analysis. |
| `data/` | JSON data files for cards and rules. |
| `tools/` | Utility scripts (likely for data extraction/maintenance). |
| `tests/` | Python test files. |

## Development Guidelines
- **Run Server:** `uv run server.py`
- **Testing:** `uv run python -m pytest`
- **Style:** Python: **Ruff** (User preference). JS: Keep as is for now.
- **Deployment:** Heroku (`Procfile` present), but currently "as is".
- **Architecture Strategy:**
    - Phase 1: Cleanup root directory.
    - Phase 2: Separate into `frontend/`, `backend/`, and `engine/`.

## Test Architecture (New)
- **Framework:** `pytest` + `pytest-bdd`
- **Location:** `engine/tests/`
- **Features:** `engine/tests/features/*.feature` (Gherkin syntax)
- **Step Definitions:** `engine/tests/steps/test_*_steps.py`
- **Status:** 
    - Core properties (Mechanics, Conditions, Deck Ops, Energy) migrated to BDD.
    - Legacy logic tests (`test_score4*`, `test_rules`) still exist but need migration or fixing.
- **Running Tests:** `uv run pytest engine/tests`

## Engine Quirks & Learnings
- **GameState.member_db/live_db:** These are **Class Variables**, not instance variables. Tests must handle them carefully (resetting them or mocking at class level).
- **Action IDs:**
    - **Color Select:** 580-585 (Pink, Red, Yellow, Green, Blue, Purple)
    - **Target Opponent:** 600-602 (Stage Slots)
- **Conditions:** `GROUP_FILTER` logic was fixed to correctly handle context-based filtering (e.g., "revealed card is Aqours").
- **Arrays:** `tapped_energy` is a fixed-size NumPy array (typically 100), not a list.

## Development Guidelines
