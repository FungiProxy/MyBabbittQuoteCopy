# Database Refactoring Plan: Consolidating Product Options

## 1. Executive Summary (TL;DR)

The current database design, where every possible product configuration is a separate row in `product_variants`, is the primary blocker to completing the application. It's impossible to build the required dynamic UI and pricing logic on top of this structure.

This document proposes a plan to refactor the database by **replacing the numerous, separate option tables (e.g., `materials`, `material_options`, `connections`, `connection_options`) with a single, unified `options` table and a link table.**

This change is not just a "nice-to-have" improvement for the future; it is a **necessary prerequisite** to make the application functional. It will simplify the data, unblock UI development, and enable the flexible pricing logic described in the `price_list.txt`.

---

## 2. The Current Problem: "Permutation Explosion"

The recent database audit revealed the core issue:

*   **Massive Data Redundancy:** The `product_variants` table has **662 rows**, while the price list only defines around **27 base models**. The extra rows are permutations of the same product with different options (e.g., `LS7000` with every possible voltage, material, and connection combination).
*   **Static and Inflexible:** The application needs to calculate price adders like `*add $45/foot`. This is impossible when a 10" probe and a 12" probe are stored as two completely separate products with fixed prices.
*   **Impossible UI Logic:** The user interface cannot present a dropdown with 320+ nearly identical options for a single product like the `LS8500`. The user needs to select "Material", "Voltage", and "Probe Length" from distinct controls.

### "Before" Structure:

The current structure requires a pair of tables for every single option type, which is complex and difficult to manage.

```
┌──────────────────┐      ┌────────────────────────┐
│    materials     │      │    material_options    │
├──────────────────┤      ├────────────────────────┤
│ id, name, etc.   │──────│ product_family_id, ... │
└──────────────────┘      └────────────────────────┘

┌──────────────────┐      ┌────────────────────────┐
│   connections    │      │   connection_options   │
├──────────────────┤      ├────────────────────────┤
│ id, name, etc.   │──────│ product_family_id, ... │
└──────────────────┘      └────────────────────────┘

┌──────────────────┐      ┌────────────────────────┐
│   accessories    │      │  accessory_options     │
├──────────────────┤      ├────────────────────────┤
│ id, name, etc.   │──────│ product_family_id, ... │
└──────────────────┘      └────────────────────────┘

(... and so on for every option category)
```

---

## 3. The Proposed Solution: A Unified `options` Table

We will replace the scattered option tables with a single, elegant `options` table. A `category` column will distinguish between different types of options (e.g., 'Material', 'Connection', 'Voltage').

A single many-to-many join table, `product_family_options`, will link these options to the relevant product families.

### New `options` Table Definition:

| Column Name   | Data Type | Description                                          | Example                             |
| ------------- | --------- | ---------------------------------------------------- | ----------------------------------- |
| `id`          | Integer   | Primary Key                                          | 101                                 |
| `name`        | String    | The display name of the option                       | 'Stainless Steel'                   |
| `category`    | String    | **The key to this design.** Groups options.          | 'Material', 'Connection', 'Voltage' |
| `price_type`  | String    | How the price is applied ('fixed', 'per_foot', etc.) | 'fixed'                             |
| `price`       | Float     | The cost or cost adder for the option.               | 40.00                               |
| `description` | Text      | Additional details for the option.                   | 'Standard 316SS Probe'              |

### "After" Structure:

This new model is much cleaner, more powerful, and easier to extend.

```
┌──────────────────┐      ┌────────────────────────┐      ┌──────────────────┐
│ product_families │      │ product_family_options │      │      options     │
├──────────────────┤      ├────────────────────────┤      ├──────────────────┤
│ id (PK)          │      │ product_family_id (FK) │      │ id (PK)          │
│ name             │◀─────│ option_id (FK)         │─────▶│ name             │
└──────────────────┘      └────────────────────────┘      │ category         │
                                                          │ price, etc.      │
                                                          └──────────────────┘
```

---

## 4. Benefits of the New Structure

1.  **Enables Dynamic UI:** The UI can query for all options where `category='Material'` and populate a "Material" dropdown for the user.
2.  **Enables Dynamic Pricing:** The application can easily calculate costs. `Base Price + Price of selected Material + (Price of Probe * length)`.
3.  **Reduces Data:** The `product_variants` table will shrink dramatically to only include base models. The 662 variants become ~27 base products.
4.  **Simplifies Maintenance:** To add a new option (e.g., a new "Cable Type"), we just add new rows to the `options` table. No new tables or database schema changes are required.
5.  **Future-Proofs the System:** This scalable model can handle any new product families or option types you add in the future without requiring another major refactor.

---

## 5. High-Level Migration Plan

This refactor can be performed systematically with a dedicated script.

### ✅ Step 1: Define New Models (COMPLETED)
Create the SQLAlchemy models for `Option` and the `product_family_options` association in `src/core/models/`.

**Status:** ✅ **COMPLETED**
- Created `Option` model with JSON columns for `choices`, `adders`, and `rules`
- Model supports all required fields: `name`, `description`, `price`, `price_type`, `category`, `product_families`, `excluded_products`

### ✅ Step 2: Create Migration Script (COMPLETED)
Create a new script, `scripts/migrate_to_unified_options.py`.

**Status:** ✅ **COMPLETED**
- Created comprehensive migration script that handles all option types
- Successfully migrated data from legacy tables to unified `options` table
- **Migration Results:**
  - **66 total options** created across **9 categories**
  - **Materials:** 7 options
  - **Voltages:** 6 options  
  - **Connections:** 22 options
  - **Accessories:** 3 options
  - **Housing Types:** 8 options
  - **Insulators:** 7 options
  - **Exotic Metals:** 4 options
  - **O-Ring Materials:** 6 options
  - **Probe Modifications:** 3 options
- All options include structured `choices` and `adders` data for dynamic UI configuration

### 🔄 Step 3: Populate the New Tables (COMPLETED)
The script will read from the old `materials` table and insert each row into the new `options` table with `category='Material'`.
It will then read `material_options` to create the links in `product_family_options`.
Repeat this process for `connections`, `accessories`, `voltages`, etc.

**Status:** ✅ **COMPLETED**
- All legacy option data has been successfully migrated
- Product family associations preserved via `product_families` field
- Pricing information and compatibility rules maintained

### ⏳ Step 4: Clean Up (PENDING)
Once the migration is verified, the old, redundant tables can be dropped from the database.

**Status:** ⏳ **PENDING**
- Legacy option tables still exist but are no longer used
- Can be safely dropped after verification that new system works correctly

### ⏳ Step 5: Refactor Services (PENDING)
Update the `ProductService` to fetch data from these new, unified tables instead of the old ones.

**Status:** ⏳ **PENDING**
- Need to update `ProductService.get_additional_options()` method
- Update UI components to use new unified options structure
- Test that dynamic configuration works correctly 