# MyBabbittQuote UI Redesign Action Plan

This document outlines the plan, progress, and rationale for integrating the new user interface into the MyBabbittQuote application.

## 1. Overview

The goal of this initiative is to replace the existing user interface with a modern, professionally designed, and more user-friendly version. The new design introduces a centralized theme, a step-by-step product configuration wizard, and a streamlined quote creation process.

This plan will serve as a living document to track our progress and ensure a smooth, maintainable integration.

## 2. Current Status

- **[In Progress]** Initial project plan and documentation created.
- **[DONE]** New UI files (`main_window_redesign.py`, `dashboard_redesign.py`, etc.) need to be moved to their correct locations in the `src/` directory.
- **[DONE]** Hardcoded styles within the new UI components need to be refactored to use the central `BabbittTheme`.
- **[To Do]** The new `ConfigurationWizard` needs to be integrated with the existing `ProductService` and `ConfigurationService` to ensure consistent business logic.
- **[To Do]** The application's entry point (`main.py`) needs to be updated to launch the new `MainWindowRedesign`.
- **[To Do]** A full end-to-end testing pass is required to validate the new user flow.
- **[To Do]** All service layer calls and signal/slot connections need to be verified to ensure data flows correctly between the new UI and the backend.
- **[To Do]** The old, now-unused UI files should be identified and removed from the project.

## 3. Action Plan & Rationale

Here is the step-by-step plan for the integration. Each step is designed to ensure the final implementation is robust, maintainable, and consistent with the existing application architecture.

### Step 1: Organize New UI Files (Done)
- **Status:** Complete
- **Rationale:** Proper file organization is essential for maintainability. This step moves the new UI components into the existing `src/ui` structure, making them a formal part of the application.

### Step 2: Refactor Hardcoded Styles (Done)
- **Status:** Complete
- **Rationale:** Removing inline `setStyleSheet` calls and centralizing them in `babbitt_theme.py` is critical for a consistent and maintainable UI. This ensures that future style changes can be made in one place. It also improves code readability by separating style from logic.

### Step 3: Update Application Entry Point (Done)
- **Status:** Complete
- **Rationale:** This step officially activates the new UI by pointing the main application entry point to `MainWindowRedesign`. The application will now launch with the new interface.

### Step 4: Full System & Data Flow Verification
- **Status:** Mostly Complete
- **Rationale:** With the new UI in place, we must conduct a full end-to-end test. This involves creating a quote from start to finish, ensuring that all data from the configuration wizard is correctly passed to the quote, saved to the database, and reflected accurately in the dashboard. This validates that all signal/slot connections and service layer interactions are working as expected.
- **Progress:** The new UI is successfully launching and displaying. The main components (dashboard, navigation, quote creation) are functional. Minor issues remain with pricing calculations in the configuration wizard, but the core user interface is working correctly.

### Step 5: Cleanup Old UI Files
- **Status:** To Do
- **Rationale:** This step involves identifying and removing the old, now-unused UI files from the project.

## 4. File Mappings

This section will track the location of the new UI files.

| Original Location (`data/ui_redesign/`)      | New Location (`src/`)                     | Status      |
| -------------------------------------------- | ----------------------------------------- | ----------- |
| `babbitt_theme.py`                           | `ui/theme/babbitt_theme.py`               | **Done**    |
| `main_window_redesign.py`                    | `ui/main_window_redesign.py`              | **Done**    |
| `dashboard_redesign.py`                      | `ui/views/dashboard_redesign.py`          | **Done**    |
| `quote_creation_redesign.py`                 | `ui/views/quote_creation_redesign.py`     | **Done**    |
| `product_selection_redesign.py`              | `ui/components/product_selection_redesign.py` | **Done**    |
| `configuration_wizard.py`                    | `ui/components/configuration_wizard.py`     | **Done**    |

## 5. Next Steps

- **Task:** Verify all service layer calls and signal/slot connections to ensure data flows correctly between the new UI and the backend.
- **Rationale:** This step ensures that the new UI interacts correctly with the backend services and that data flows between the two seamlessly.

---
*This document will be updated as we complete each step.*