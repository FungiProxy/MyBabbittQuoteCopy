# UI Refactor Guide

_Last updated: {{DATE}}_

This document outlines the planned refactor of the PySide6 user‐interface layer. The goal is to improve maintainability, performance, and accessibility without changing existing business logic.

## 1 Objectives
- Break large monolithic widgets into composable components
- Adopt a Model–View–Controller (MVC) or Model–View–ViewModel (MVVM) structure
- Ensure all widgets are keyboard‐navigable and screen‐reader friendly
- Isolate long‐running DB operations in background threads
- Provide unit-test hooks for critical UI behaviors

## 2 Current Pain Points
| File | Approx. LOC | Issues |
| --- | --- | --- |
| `product_selection_dialog.py` | 600+ | Mixed UI + business logic, large `if/else` branches |
| `specifications_tab.py` | 700+ | Handles validation, DB lookups, and widget creation in one place |

## 3 Refactor Roadmap
1. Create `src/ui/components/` sub-package for reusable widgets (e.g., `OptionSelector`, `PriceLabel`).
2. Extract logic in `specifications_tab.py` into:
   - `SpecificationController` (handles state, validation, DB calls)
   - `SpecificationView` (pure widgets/layout)
3. Split `product_selection_dialog.py` into:
   - `ProductSelectionDialog` (controller)
   - `ProductSearchPanel`, `VariantTable`, `OptionSidebar` (views)
4. Introduce central `UiEventBus` (Qt signals) for inter-component communication.
5. Add `tests/ui/` for widget smoke tests using `pytest-qt`.

## 4 Accessibility Checklist
- [ ] All focusable controls reachable via <Tab>
- [ ] Labels associated with inputs (`setAccessibleName`, `setBuddy`/`for=`)
- [ ] High-contrast stylesheet toggle in Settings
- [ ] Minimum 4.5:1 color contrast ratio

## 5 Performance Enhancements
- Replace `QTableWidget` with `QTableView` + `QAbstractTableModel` for large datasets
- Use `QThreadPool` + `QRunnable` for price look-ups
- Debounce expensive signal handlers (see `utils/debounce.py`)

## 6 Timeline
| Stage | Task | Owner | ETA |
| --- | --- | --- | --- |
| Phase 1 | Component extraction | — | 1 week |
| Phase 2 | Controller/View split | — | 1 week |
| Phase 3 | Accessibility polish | — | 3 days |
| Phase 4 | Performance tuning & tests | — | 1 week |

> After each phase, run the full test suite and perform a manual exploratory test to catch regressions.
