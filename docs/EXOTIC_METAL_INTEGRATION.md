# Exotic Metal Integration Implementation

## Overview

This document describes the implementation of exotic metals integration into the material dropdown with manual override pricing functionality.

## What Was Implemented

### 1. Database Changes
- **Integrated exotic metals into material options**: All four exotic metals (Alloy 20, Hastelloy-C-276, Hastelloy-B, Titanium) are now available in the material dropdown for all product families
- **Removed separate exotic metal options**: The standalone "Exotic Metal" category options have been removed since exotic metals are now part of the material selection
- **Manual override pricing**: All exotic metals have $0 adders in the database, indicating they require manual override pricing

### 2. UI Changes
- **Material dropdown enhancement**: The material dropdown now includes exotic metals with "(Consult Factory)" label
- **Manual override field**: When an exotic metal is selected, a "Manual Override Price" field appears allowing users to enter a custom price adder
- **Dynamic visibility**: The manual override field only appears when exotic metals are selected and is hidden for standard materials

### 3. Pricing Logic
- **Configuration service updates**: Added handling for "Exotic Metal Override" option in pricing calculations
- **Manual override application**: The manual override value is added to the final price when an exotic metal is selected
- **Per-configuration pricing**: Each configuration can have its own exotic metal price, not affecting future configurations

## Technical Implementation Details

### Database Structure
```sql
-- Material options now include exotic metals
choices: ["S", "H", "TS", "U", "T", "C", "Alloy 20", "Hastelloy-C-276", "Hastelloy-B", "Titanium"]
adders: {
    "S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80,
    "Alloy 20": 0, "Hastelloy-C-276": 0, "Hastelloy-B": 0, "Titanium": 0
}
```

### UI Components
- **Material ComboBox**: Enhanced to include exotic metals with "(Consult Factory)" suffix
- **Manual Override Layout**: QHBoxLayout containing label and input field
- **Dynamic Visibility**: Controlled by `_handle_exotic_metal_override()` method

### Pricing Integration
```python
# In ConfigurationService._update_price()
if option_name == "Exotic Metal Override":
    override_value = self._to_float(selected_value)
    if override_value > 0:
        final_price += override_value
```

## Benefits of This Approach

### 1. **Unified Interface**
- All materials (standard and exotic) are in one dropdown
- Consistent user experience across all product families
- No need to navigate between different option categories

### 2. **Flexible Pricing**
- Manual override allows for custom pricing per configuration
- No global price changes affecting other configurations
- Supports "Consult Factory" pricing model

### 3. **Data Integrity**
- Exotic metals are treated as materials in the data model
- Consistent with existing material handling patterns
- Simplified database structure

### 4. **User Experience**
- Clear indication that exotic metals require factory consultation
- Immediate price feedback when override is entered
- Intuitive workflow for sales team

## Usage Instructions

### For Users
1. Select a product family
2. Choose material from dropdown (exotic metals show "(Consult Factory)")
3. If exotic metal is selected, enter manual override price
4. Price updates automatically with override applied

### For Developers
1. Exotic metals are identified by checking if material value is in exotic metals list
2. Manual override is stored as "Exotic Metal Override" option
3. Pricing calculation includes override value when present

## Files Modified

### Core Files
- `src/ui/product_selection_dialog.py`: UI integration and manual override handling
- `src/core/services/configuration_service.py`: Pricing logic for exotic metal overrides
- `scripts/data/config/materials.py`: Database configuration updates

### Scripts
- `scripts/update_materials_with_exotic_metals.py`: Database migration script
- `test_exotic_metal_integration.py`: Verification script

## Testing

The implementation has been tested to verify:
- ✅ Exotic metals appear in material dropdown for all product families
- ✅ Manual override field appears when exotic metals are selected
- ✅ Manual override field is hidden for standard materials
- ✅ Pricing calculations include manual override values
- ✅ Separate exotic metal options have been removed
- ✅ All exotic metals have $0 adders (manual override only)

## Future Considerations

1. **Validation**: Could add validation to ensure manual override prices are reasonable
2. **History**: Could track exotic metal pricing history for reference
3. **Approval Workflow**: Could add approval process for exotic metal configurations
4. **Reporting**: Could add reporting on exotic metal usage and pricing

## Conclusion

The exotic metal integration provides a clean, unified interface for material selection while maintaining the flexibility needed for custom pricing. The manual override approach ensures that each configuration can have its own pricing without affecting global settings. 