# Project Action Plan

_Last updated: May 12th, 2025_

## Overview
This file contains the current prioritized action plan for the MyBabbittQuote project. It is intended to help new contributors and AI agents quickly understand the project's status, priorities, and next steps. Please update this file as progress is made or priorities change.

---

## Project State
- **Core business logic:** Implemented (pricing, quoting, models)
- **UI:** Functional, well-documented, but some missing features
- **Testing:** Present, but needs centralization and more coverage
- **Documentation:** Good coverage of core models and UI components
- **Export:** Basic structure present, needs full implementation

---

## Prioritized Action Plan

### 1. Documentation & Onboarding
- [X] Expand `README.md` with project overview, setup, usage, and testing instructions
- [X] Add docstrings to core models
- [X] Complete docstrings for remaining models
- [X] Document UI components and their interactions
  - [X] MainWindow: Tab management and core functionality
  - [X] ProductTab: Product selection interface
  - [X] SpecificationsTab: Product configuration form
  - [X] QuoteTab: Quote management and pricing
  - [X] SparePartsTab: Spare parts catalog and selection
- [ ] Document service layer classes
  - [X] QuoteService
  - [X] ProductService
  - [X] MaterialService
  - [X] CustomerService
- [X] Create developer guide for common tasks
- [X] Add architecture overview diagram
- [X] Document database schema and relationships

### 2. Testing
- [X] Centralize test files in appropriate directories
- [X] Add unit tests for core business logic
- [X] Add integration tests for database operations
- [ ] Add UI component tests
- [ ] Set up CI/CD pipeline
- [ ] Add test coverage reporting
- [ ] Document testing strategy and procedures

### 3. UI Improvements
- [ ] Break large UI files into smaller components
- [ ] Add loading indicators for database operations
- [ ] Improve error handling and user feedback
- [ ] Add form validation
- [ ] Implement undo/redo functionality
- [ ] Add keyboard shortcuts
- [ ] Improve accessibility

### 4. Export Functionality
- [ ] Complete PDF export implementation
- [ ] Add customizable templates
- [ ] Add preview functionality
- [ ] Support multiple export formats
- [ ] Add batch export capability
- [ ] Add email integration

### 5. Database & Performance
- [ ] Optimize database queries
- [ ] Add database indexing
- [ ] Implement caching for frequently accessed data
- [ ] Add database migration scripts
- [ ] Add backup/restore functionality
- [ ] Document database maintenance procedures

### 6. Security
- [ ] Implement user authentication
- [ ] Add role-based access control
- [ ] Add audit logging
- [ ] Implement secure storage for sensitive data
- [ ] Add input validation and sanitization
- [ ] Document security procedures

### 7. Code Organization & Refactoring
- [ ] Refactor large UI files into smaller, focused components or widgets
- [ ] Consider using service classes (not just static methods) for extensibility
- [ ] Ensure all subdirectories have `__init__.py` for explicit package structure

### 8. Business Logic Improvements
- [ ] Move hardcoded pricing rules to configuration files or database tables
- [ ] Add business rule validation (e.g., valid product/material combinations)
- [ ] Optimize database access (profile for N+1 queries, use eager loading, cache expensive lookups)

### 9. Dependency & Build Management
- [ ] Pin dependency versions more strictly in `requirements.txt`
- [ ] Consider using `pip-tools` or `poetry` for dependency management and lock files

### 10. UI/UX Enhancements
- [ ] Use a resource file or stylesheet for consistent UI theming
- [ ] Implement dynamic dropdowns/radio buttons for product-specific options
- [ ] Review UI for accessibility best practices

### 11. Export & Integration
- [ ] Encapsulate all export logic in `src/export/`
- [ ] Decouple export logic from UI to allow CLI or API-triggered exports

### 12. Performance Optimization
- [ ] Profile and optimize slow code paths
- [ ] Ensure frequently queried fields are indexed in the database

### 13. Advanced Enhancements (Optional/Future)
- [ ] Consider using `pydantic` or `dynaconf` for configuration management
- [ ] Add authentication/authorization if multi-user
- [ ] Build admin UI for managing products, materials, and pricing rules

---

## Notes
- Priority order may change based on business needs
- Each task should include appropriate documentation updates
- Consider backwards compatibility when making changes
- Follow established coding standards and patterns

## How to Use This Plan
- Check off items as they are completed.
- Add notes, links to relevant files, or references to issues as needed.
- Update priorities as the project evolves.

## Related Files
- `README.md`: Project overview and setup
- `project_notes.md`: Design notes, ideas, and open questions
- `DECISIONS.md`: Architectural decisions and rationale (if present)

---

Welcome! Start here, and refer to the README for more details. 