# Cursor Rules: Product Configuration UI

## Data Model & Database
- Always use SQLAlchemy's `JSON` column type for fields like `choices` and `adders` in the `Option` model to ensure proper serialization and deserialization.
- If the schema changes, drop and recreate the affected tables, then reseed to avoid stale or incorrectly formatted data.
- When seeding options, ensure each option includes all required fields: `name`, `description`, `price`, `price_type`, `category`, `choices` (list), and `adders` (dict).

## Service Layer
- The `get_additional_options` method in `ProductService` **must** return `choices` and `adders` for each option, not just basic fields. This is required for the UI to render configuration controls.
- Always filter out options where the product family is in `excluded_products`.

## UI/UX (ProductSelectionDialog)
- Only render option labels and widgets if `choices` is a valid, non-empty list. This prevents extra or orphaned labels from appearing in the UI.
- Use debug prints in `_build_dynamic_options` to verify the structure of `all_options` if options are not rendering as expected.
- The right-hand side of the product configuration should always show all available options and configurable selections for the selected product family, with correct pricing adders.

## Debugging & Maintenance
- If options do not appear in the UI, check:
  1. The database table schema (should be JSON for `choices`/`adders`).
  2. The data in the table (should be lists/dicts, not strings).
  3. The output of `get_additional_options` (should include all needed fields).
  4. The UI logic (should skip options with no valid choices).
- Use targeted debug prints to quickly isolate data flow or rendering issues.

## General
- When making changes to the data model or service layer, always test the full flow: seed data → fetch in service → render in UI.
- Keep seeding scripts up to date with the latest required fields and formats.
- Document any non-obvious business rules or UI behaviors in this rules file for future maintainers. 