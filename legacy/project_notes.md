# Project Notes

_Last updated: {{DATE}}_

## Purpose
This file provides design notes, architectural decisions, open questions, and implementation context for the MyBabbittQuote project. It is intended for both human contributors and AI agents (including Cursor AI) to support onboarding, planning, and ongoing development.

---

## Project Overview
MyBabbittQuote is a domain-driven quote generator for Babbitt International products. It features a modular UI, robust business logic for pricing and quoting, and planned export capabilities. The project is structured for maintainability, extensibility, and testability.

---

## Current Project State
- **Action Plan:** Maintained in `ACTION_PLAN.md` (see for prioritized tasks and next steps)
- **Onboarding:** `README.md` and `START_HERE.md` provide clear instructions for new contributors and agents
- **Core Logic:** Pricing, quoting, and product models are implemented and tested
- **UI:** Functional, modular, but some files are large and need refactoring; dynamic options and accessibility improvements planned
- **Testing:** Present, but needs centralization and more coverage; UI tests planned
- **Documentation:** Improved, but more docstrings and usage examples needed
- **Export:** Structure present, full PDF export in progress

---

## Key Design Decisions
- **Domain-Driven Design:** Code is organized by domain (core, ui, export, utils)
- **Separation of Concerns:** Business logic, UI, and data access are separated for maintainability
- **Extensibility:** Models and services are designed to support future product and pricing rule changes
- **Testing:** Integration and business logic tests are prioritized; UI tests planned
- **Configuration:** Hardcoded pricing rules are being migrated to config files or the database

---

## Open Questions & Ideas
- How to best handle dynamic product options (e.g., flange types, cable lengths) in the UI?
- Should all pricing rules be moved to the database/config files for easier updates?
- What is the best approach for user authentication/authorization if multi-user support is needed?
- How to structure admin tools for managing products, materials, and pricing rules?
- What are the accessibility requirements for the UI?
- How to categorize and manage specialized, customer-specific, or legacy products?
- Should spare parts be a separate high-level category in the UI and database?

---

## Implementation Details
### Database
- SQLAlchemy models handle complex pricing rules and relationships
- Pre-populated database approach for product catalog
- Standard SQLite database for easy deployment
- Alembic used for migrations

### Pricing Logic
- Material-specific pricing (S, H, U, T materials)
- Length-based calculations (per inch/foot)
- Non-standard length surcharges (for H material)
- Option compatibility with product families
- Some rules still hardcoded; migration to config/DB ongoing

### UI
- PySide6-based tabbed interface: product selection, specifications, quote summary, spare parts
- Signals/slots for inter-component communication
- Needs refactoring for large files and more modular widgets
- Dynamic dropdowns/radio buttons for product-specific options planned
- Accessibility and input validation improvements planned

### Export
- Structure for PDF export present in `src/export/`
- Decoupling export logic from UI is planned for CLI/API support

---

## Recent Improvements
- Added `ACTION_PLAN.md` for clear, prioritized project planning
- Updated `README.md` for comprehensive onboarding
- Created `START_HERE.md` pointer file for new contributors and agents
- Ensured `project_notes.md` is visible to Cursor AI and all contributors
- Improved project structure and documentation

---

## Resources
- **Action Plan:** See `ACTION_PLAN.md`
- **Onboarding:** See `README.md` and `START_HERE.md`
- **Design Notes:** This file
- **Database/Business Logic:** See `src/core/`
- **UI:** See `src/ui/`
- **Export:** See `src/export/`
- **Data:** See `data/` for price lists and additional info

---

## Command Reference
```bash
# Initialize database
python scripts/create_db.py

# Test database structure
python scripts/test_db.py

# Test pricing logic
python scripts/test_pricing.py

# Query database contents
python scripts/query_db.py
```

---

## How to Use This File
- Add new design decisions, questions, or ideas as they arise
- Update this file after major changes or architectural decisions
- Use this as a reference for onboarding, planning, and code reviews

## My Babbitt Quote Generator - Personal Notes

<!-- This file is for personal notes and is ignored by git and cursor agents -->

## Project Status

### Completed
- Database schema design and implementation
- Pricing model with complex rules
- Database utilities and helpers
- Initial data seeding

### In Progress
- [ ] Business logic layer
- [ ] UI implementation
- [ ] Export functionality

### In Progress (updated)
- [ ] UI refactor into smaller widgets/components
- [ ] Accessibility & keyboard navigation improvements
- [ ] Export template customization tools

### To Do
- [ ] 
- [ ] 
- [ ] 

## Ideas and Notes
- Create an admin tool
- There should be a more detailed selection for flange types (150# vs 300#) and sizes (1" through 4"), as well as Tri-Clamp connections with different sizing options
- The database models don't appear to have explicit tables for these exotic materials and O-rings
- The existing UI implementation does not include any specific cable length configuration options. The specifications tab has "Extended Probe" as a checkbox, but doesn't have a field specifically for cable length or cable type selection. For remote mounted systems like the LS8000, there should be options to specify the length of the twisted shielded pair cable needed to connect the transmitter to the receiver. For the FS10000, there should be an option to specify additional coaxial cable beyond the standard 15 feet.
- For a complete implementation, the UI should include a dropdown or radio button selection for housing type with options like:
    Standard Housing
    NEMA 4X Stainless Steel Housing
    Explosion Proof - Aluminum
    Explosion Proof - 316 Stainless Steel
    Remote Receiver - NEMA 4 (with size options)
    Remote Receiver - Explosion Proof
The options should be dynamically populated based on the selected product model as not all housing options are available for all products
-

- Standard vs Non-Standard Lengths: The additional info specifies what constitutes "standard lengths" for H material (6, 8, 10, 12, 16, 24, 36, 48, 60, 72 inches), which affects the $300 adder pricing. This categorization of standard lengths might be missing. UPDATE UI WHEN ADDING DROPDOWN MENUS
- Specialized/Custom Product Offerings: The last section of the price list shows special pricing for specific customers/applications (CONTROL SYSTEMS WEST, APPLIED FOR GYSON, AUTOMATION SUPPLY). These might need to be categorized as "customer-specific" or "special application" products.
- Material Compatibility Information: While mentioned in application notes throughout the price list, there's no explicit categorization of which product is best suited for which type of application (conductive liquids, dry materials, etc.).
- Replacement/Legacy Products: The PRESENCE/ABSENCE SWITCHES section notes these are replacement products for Princo P/N's. This category of replacement/legacy products might need to be more explicitly identified.
- Spare Parts: While spare parts are listed under each product, they might benefit from being categorized together as a separate high-level category.

## Questions for Later

- 

## Implementation Details

### Database
- SQLAlchemy models handle complex pricing rules
- Pre-populated database approach for product catalog
- Standard SQLite database for easy deployment

### Pricing Logic
- Material-specific pricing (S, H, U, T materials)
- Length-based calculations (per inch/foot)
- Non-standard length surcharges (for H material)
- Option compatibility with product families

## Test Results

- Database tests confirm schema working correctly
- Pricing tests validate calculations for different configurations
- Query tests confirm data structure

## Resources

- Babbitt International pricing info in data/price_list.txt
- Special pricing rules in data/additional_info.txt

## Command Reference

```bash
# Initialize database
python scripts/create_db.py

# Test database structure
python scripts/test_db.py

# Test pricing logic
python scripts/test_pricing.py

# Query database contents
python scripts/query_db.py


# Transfer agent brain
You are ChatGPT. Your task is to summarize the entire conversation so far into a structured format that allows this context to be carried into a new session and continued seamlessly.

Please output the summary in the following format using markdown:

---

### 📝 Detailed Report

A natural language summary of the conversation's goals, themes, and major insights.

---

### 🗂 Key Topics

- [List 3–7 bullet points summarizing the major discussion themes]

---

### 🚧 Ongoing Projects

Project Name: [Name]

- Goal: [What the user is trying to accomplish]

- Current Status: [Progress made so far]

- Challenges: [Any blockers or complexities]

- Next Steps: [What should happen next]

(Repeat for each project)

---

### 🎯 User Preferences

- [Tone, formatting, workflow style, special instructions the user tends to give]

---

### ✅ Action Items

- [List all actionable follow-ups or tasks that were not yet completed]
```

---

*Last updated: [DATE]* 
