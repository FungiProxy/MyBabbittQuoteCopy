# AGENT REVIEW GUIDE

## Overview
This document is intended for agents or developers reviewing the MyBabbittQuoteCopy codebase. It provides a high-level understanding of the application's architecture, data flow, and practical tips for efficiently locating and understanding key mechanics and operations.

---

## 1. Application Purpose
MyBabbittQuoteCopy is a quoting and configuration tool for industrial products (e.g., level switches). It allows users to select a product family, configure options (materials, connections, voltages, etc.), and generate quotes with accurate pricing, including adders for special materials, lengths, and exotic metals.

---

## 2. Core Architecture
- **Backend:** Python, SQLAlchemy ORM, SQLite (quotes.db)
- **Frontend/UI:** PySide6 (Qt), modular dialogs and widgets
- **Data:** Seeded via JSON/CSV and Python scripts, with options and materials stored in the database

---

## 3. Key Components & Where to Find Them

### Data Model & Database
- **Models:** `src/core/models/` (e.g., `option.py`, `material.py`, `exotic_metal_option.py`)
- **Database:** `data/quotes.db` (main), CSV/JSON in `data/` for seeding

### Service Layer
- **Business Logic:** `src/core/services/`
  - `product_service.py` (fetches options, applies business rules)
  - `configuration_service.py` (handles configuration logic)


### UI Layer
- **Dialogs:** `src/ui/product_selection_dialog_improved.py`, `src/ui/main_window.py`
- **Components:** `src/ui/components/`, `src/ui/views/`
- **Helpers/Utils:** `src/ui/helpers/`, `src/ui/utils/`

---

## 4. How the Application Works (Data Flow)
1. **Startup:** Loads product families and options from the database.
2. **Product Selection:** User selects a product family (left side of UI).
3. **Option Configuration:** UI fetches all available options for the selected family (right side), including materials, connections, voltages, etc.
4. **Dynamic Option Rendering:** Only options with valid `choices` are rendered. Adders and pricing are shown for each selection.
5. **Quote Generation:** Final configuration is priced and saved as a quote.

---

## 5. Key Mechanics & Where to Find Them
- **Material/Exotic Metal Handling:**
  - Data: `data/materials.csv`, `data/temp/options.csv`
  - Model: `src/core/models/material.py`, `src/core/models/option.py`
  - Service: `product_service.py` (filters, adders), `configuration_service.py`
  - UI: `product_selection_dialog_improved.py` (dynamic rendering)
- **Length Adders:**
  - Logic: `product_service.py`, see memory: adder is applied at threshold and every full 12" after
- **Option Filtering:**
  - Service: `get_additional_options` in `ProductService` (filters by family, excludes as needed)
- **UI Rendering:**
  - Only renders options with non-empty `choices` (see always_applied_workspace_rules)

---

## 6. Debugging & Extension Tips
- **Check Data Consistency:**
  - Ensure `choices` and `adders` are JSON (not stringified) in the DB.
  - Use scripts in `extra/` and `scripts/` to audit or patch data.
- **Trace Data Flow:**
  - Start from UI event (e.g., selection change) → service call → model/data fetch.
- **Add New Options/Materials:**
  - Update seed files and/or use migration scripts.
  - Reseed or patch the DB as needed.
- **UI Issues:**
  - Use debug prints in `_build_dynamic_options` in `product_selection_dialog_improved.py`.
- **Testing:**
  - See `tests/` and `extra/test_*` scripts for integration/unit tests.

---

## 7. Finding Code for Specific Operations
- **Material Option Logic:**
  - Search for "Material" in `src/core/services/` and `src/ui/`
- **Exotic Metal Adders:**
  - Search for "exotic" or codes "A", "HC", "HB", "TT" in models, services, and data
- **Quote Saving:**
  - See `src/core/services/quote_service.py` (if present) or `main.py`
- **UI Event Handling:**
  - Look for signal/slot connections in `main_window.py` and dialogs

---

## 8. Business Rules & Conventions
- See always_applied_workspace_rules in `.rules` for enforced conventions
- Product configuration UI: left = product family, right = all options for that family
- Use SQLAlchemy JSON columns for `choices`/`adders` in `Option`
- Drop/recreate tables and reseed if schema changes

---

## 9. Useful Scripts
- `extra/check_exotic_metals_db.py`: Audit exotic metal presence
- `extra/add_exotic_metal_codes.py`: Patch DB with exotic metals
- `extra/integrate_exotic_metals.py`: Migrate exotic metals to unified material option
- `scripts/` and `extra/`: Many one-off data and audit scripts

---

## 10. Contact & Further Help
- See `docs/` for architecture, UI, and database guides
- `docs/START_HERE.md` for onboarding
- For business logic, see `docs/database_refactor_plan.md` and `docs/ui_refactor_guide.md`

---

*This guide should help any agent or developer quickly orient themselves and efficiently review or extend the application.* 