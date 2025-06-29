# TRAN-EX Reconfiguration Plan

## Overview
This document describes the process and rationale for reconfiguring the TRAN-EX option as a separate product family, rather than as an accessory or dynamic option under LS8000/2.

---

## Background
- **TRAN-EX** is a special configuration related to the LS8000/2 family.
- When selected, it requires a unique set of options and pricing rules (notably, voltage is not configurable).
- Treating TRAN-EX as a separate product family simplifies UI logic, pricing, and future maintenance.

---

## Key Changes

### 1. Database
- Add a new product family: `TRAN-EX`
- Copy relevant options from LS8000/2, **excluding voltage**
- Set up unique pricing rules (base price + $540 adder, etc.)
- Update seeding scripts to include TRAN-EX options

### 2. UI/UX
- TRAN-EX appears as a selectable product family in the product selection dialog
- When TRAN-EX is selected:
  - Show all standard options except voltage
  - Use the same material and length options as LS8000/2
  - Apply TRAN-EX-specific pricing logic

### 3. Business Logic
- Pricing engine recognizes TRAN-EX as a distinct family
- No voltage selection for TRAN-EX
- All other configuration and adders work as for LS8000/2, unless otherwise specified

### 4. Migration/Transition
- Remove TRAN-EX as an accessory or dynamic option from LS8000/2, if present
- Update documentation and training materials for sales/support

---

## Implementation Steps
1. **Database**
   - Add TRAN-EX to `product_families`
   - Seed options for TRAN-EX (copy from LS8000/2, remove voltage)
   - Add/adjust pricing rules

2. **UI**
   - Update product selection dialog to include TRAN-EX
   - Ensure configuration dialog hides voltage for TRAN-EX

3. **Testing**
   - Verify TRAN-EX can be quoted/configured independently
   - Confirm pricing and options match requirements

4. **Documentation**
   - Update user and admin guides to reflect new workflow

---

## Rationale
- **Simplicity:** Reduces conditional logic in UI and pricing code
- **Maintainability:** Easier to update TRAN-EX options/rules in the future
- **Clarity:** Users see TRAN-EX as a distinct product, reducing confusion 