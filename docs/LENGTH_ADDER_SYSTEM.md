# Length Adder System

## Overview

The length adder system provides a flexible, database-driven approach to calculating length-based pricing for different product families and materials. This system replaces the previous hard-coded logic with configurable rules stored in the database.

## Database Schema

### length_adder_rules Table

```sql
CREATE TABLE length_adder_rules (
    id INTEGER NOT NULL,
    product_family VARCHAR NOT NULL,
    material_code VARCHAR NOT NULL,
    adder_type VARCHAR NOT NULL,
    first_threshold FLOAT NOT NULL,
    adder_amount FLOAT NOT NULL,
    description TEXT,
    PRIMARY KEY (id)
);
```

**Fields:**
- `product_family`: Product family identifier (e.g., "LS2000", "FS10000")
- `material_code`: Material code (e.g., "S", "H", "U", "T", "TS", "CPVC")
- `adder_type`: Type of adder calculation ("per_foot" or "per_inch")
- `first_threshold`: Length in inches where the first adder is applied
- `adder_amount`: Amount to add per unit (foot or inch)
- `description`: Human-readable description of the rule

## Pricing Rules

### Per-Foot Adders

For materials with `adder_type = 'per_foot'`:
- **Most product families**: First adder applied at 24 inches
- **FS10000**: First adder applied at 18 inches (special case)
- **Calculation**: `(length - first_threshold) / 12 * adder_amount`

**Examples:**
- LS2000 S material at 36": `(36 - 24) / 12 * 45 = 1 * 45 = $45`
- LS2000 H material at 48": `(48 - 24) / 12 * 110 = 2 * 110 = $220`
- FS10000 S material at 30": `(30 - 18) / 12 * 45 = 1 * 45 = $45`

### Per-Inch Adders

For materials with `adder_type = 'per_inch'`:
- **Base length**: Usually 4 inches for U, T, CPVC materials
- **Calculation**: `(length - first_threshold) * adder_amount`

**Examples:**
- LS2000 U material at 8": `(8 - 4) * 40 = 4 * 40 = $160`
- LS2000 T material at 10": `(10 - 4) * 50 = 6 * 50 = $300`
- LS6000 CPVC material at 8": `(8 - 4) * 50 = 4 * 50 = $200`

## Material-Specific Rules

### Standard Materials (S, H, TS, C)
- **Adder Type**: per_foot
- **First Threshold**: 24" (except FS10000 at 18")
- **Amounts**: 
  - S, C: $45/foot
  - H, TS: $110/foot

### Blind End Materials (U, T, CPVC)
- **Adder Type**: per_inch
- **First Threshold**: 4"
- **Amounts**:
  - U: $40/inch
  - T: $50/inch
  - CPVC: $50/inch

### Exotic Metals (A, HB, HC, TT)
- **No length adders**: These materials don't have length-based pricing

## Implementation

### Pricing Strategy

The `ExtraLengthStrategy` class in `src/core/pricing/strategies.py` queries the database for applicable rules and calculates the appropriate adder.

### Service Methods

The `ProductService` class provides:
- `calculate_length_price()`: Calculate adder for specific length/material combination
- `get_length_adder_rules()`: Retrieve rules from database

### Migration

Use the migration script `migrations/versions/add_length_adder_rules_table.py` to add the table and seed data to existing databases.

## Benefits

1. **Flexibility**: Easy to modify thresholds and amounts without code changes
2. **Maintainability**: All rules in one place, clearly documented
3. **Extensibility**: Easy to add new product families or materials
4. **Consistency**: Centralized logic prevents inconsistencies
5. **Auditability**: Clear record of pricing rules in database

## Testing

Run `test_length_adder_rules.py` to verify the system works correctly with various scenarios.

## Future Enhancements

Potential improvements:
- Add support for more complex pricing models
- Include seasonal or volume-based pricing
- Add rule versioning for historical tracking
- Create admin interface for rule management 