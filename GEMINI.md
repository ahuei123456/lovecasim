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

## Current Status
- The codebase mimics "vibe coding" style: monolithic files, loose scripts in root, mixed responsibilities.
- **Immediate Goal:** Clean up root directory, organize scripts, and document architecture.
