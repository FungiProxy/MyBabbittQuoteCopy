-- Add process_connection_material column to base_models table
-- Note: SQLite doesn't support ADD COLUMN in ALTER TABLE, so we need to recreate the table
-- This is a simplified approach - you may need to handle this differently in your database
-- For now, we'll assume the column exists or will be added manually

-- If you need to add the column manually in DB Browser:
-- 1. Open the database in DB Browser for SQLite
-- 2. Go to "Database Structure" tab
-- 3. Right-click on base_models table
-- 4. Select "Modify Table"
-- 5. Add a new column: process_connection_material (TEXT)

-- Insert Connection Material option into options table
INSERT INTO options (
    name,
    description,
    price,
    price_type,
    category,
    excluded_products,
    product_families,
    choices,
    adders,
    rules
) VALUES (
    'Connection Material',
    'Process connection material selection',
    0.0,
    'fixed',
    'Connections',
    NULL,
    'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000',
    '[{"code": "S", "display_name": "S - 316 Stainless Steel"}, {"code": "A", "display_name": "A - Alloy 20"}, {"code": "HB", "display_name": "HB - Hastelloy-B"}, {"code": "HC", "display_name": "HC - Hastelloy-C-276"}, {"code": "TT", "display_name": "TT - Titanium"}]',
    '{"S": 0, "A": 0, "HB": 0, "HC": 0, "TT": 0}',
    NULL
);

-- Set default value for all base models except LS7500, LS8500, and TRAN-EX
UPDATE base_models
SET process_connection_material = 'S'
WHERE model_number NOT LIKE 'LS7500%' 
  AND model_number NOT LIKE 'LS8500%' 
  AND model_number NOT LIKE 'TRAN-EX%'; 