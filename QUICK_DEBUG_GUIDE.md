# Quick Debug Guide - Model Number & Pricing Issues

## Current Problems

### 1. Model Number Includes Extra Codes
- **Issue**: Model number shows `LS2000-115VAC-S-10"-1""NPT` instead of base `LS2000-115VAC-S-10"`
- **Root Cause**: UI defaults to first choice in dropdown (1" NPT) instead of base model value (3/4" NPT)
- **Fix**: When base model is selected, set all option widgets to base model's actual values

### 2. Price Shows Adders When Should Be Base Price
- **Issue**: Price shows $565 instead of base $455
- **Root Cause**: AccessoryOptionStrategy adds adders even for "No" values
- **Debug Evidence**: 
  ```
  [DEBUG] Accessory: Extra Static Protection, value: No, adders: {'Yes': 30, 'No': 0}
  [DEBUG] Accessory adder applied: Extra Static Protection = 30  // BUG: Should not add 30 for "No"
  ```
- **Fix**: Only add non-zero adders to price

### 3. Insulator Length Key Mismatch
- **Issue**: `[WARNING] No adder found for Insulator Length value: 4`
- **Root Cause**: Code looks for key "4" but adders dict uses "Standard", "6" Extended", etc.
- **Fix**: Map "4" to "Standard" before lookup

## Key Files to Check

1. **UI Default Selection**: `src/ui/product_selection_dialog_modern.py` - `_setup_core_options()`
2. **Accessory Pricing**: `src/core/pricing/strategies/accessory_option_strategy.py`
3. **Insulator Pricing**: `src/core/pricing/strategies/insulator_option_strategy.py`
4. **Model Number Generation**: `src/core/services/configuration_service.py` - `generate_model_number()`

## Debug Output Analysis

The debug shows the flow:
1. User selects LS2000 model
2. UI sets options to first available choices (not base model values)
3. Configuration service compares user choices to base model
4. Since they don't match, extra codes are added to model number
5. Pricing strategies apply adders even for default "No" values

## Quick Fix Priority

1. **HIGH**: Fix UI default selection to use base model values
2. **HIGH**: Fix accessory pricing to not add zero adders  
3. **MEDIUM**: Fix insulator length key mapping

## Base Model Reference
- LS2000 base: `LS2000-115VAC-S-10"` (3/4" NPT, U insulator, 10" probe)
- All options should default to these values when model is selected 