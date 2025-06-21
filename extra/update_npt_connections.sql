-- Update NPT connections based on product family specifications
-- LS2000, LS2100, LS8000, FS10000: 3/4" NPT only
-- LS6000, LS7000, LS7000/2, LT9000: 1" NPT standard, 3/4" optional
-- LS8000/2: 3/4" NPT standard, 1" optional

-- First, let's see current NPT Size options
SELECT id, name, product_families, choices, adders FROM options WHERE name = 'NPT Size';

-- Update NPT Size for LS2000, LS2100, LS8000, FS10000 (3/4" only)
UPDATE options 
SET product_families = 'LS2000,LS2100,LS8000,FS10000',
    choices = '["3/4\""]',
    adders = '{"3/4\"": 0}'
WHERE name = 'NPT Size' AND id = (
    SELECT MIN(id) FROM options WHERE name = 'NPT Size'
);

-- Create new NPT Size option for LS6000, LS7000, LS7000/2, LT9000 (1" standard, 3/4" optional)
INSERT INTO options (name, description, price, price_type, category, product_families, choices, adders) VALUES
('NPT Size', 'NPT connection size selection', 0.0, 'fixed', 'Connections', 'LS6000,LS7000,LS7000/2,LT9000', 
 '["1\"", "3/4\""]', '{"1\"": 0, "3/4\"": 0}');

-- Create new NPT Size option for LS8000/2 (3/4" standard, 1" optional)
INSERT INTO options (name, description, price, price_type, category, product_families, choices, adders) VALUES
('NPT Size', 'NPT connection size selection', 0.0, 'fixed', 'Connections', 'LS8000/2', 
 '["3/4\"", "1\""]', '{"3/4\"": 0, "1\"": 0}');

-- Now update the product_family_options table for these NPT options
-- For LS2000 (family_id = 1)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 1, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LS2000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 1);

-- For LS2100 (family_id = 2)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 2, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LS2100%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 2);

-- For LS6000 (family_id = 3)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 3, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LS6000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 3);

-- For LS7000 (family_id = 4)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 4, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LS7000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 4);

-- For LS7000/2 (family_id = 5)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 5, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LS7000/2%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 5);

-- For LS8000 (family_id = 6)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 6, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LS8000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 6);

-- For LS8000/2 (family_id = 7)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 7, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LS8000/2%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 7);

-- For LT9000 (family_id = 8)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 8, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%LT9000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 8);

-- For FS10000 (family_id = 9)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 9, id, 1 FROM options WHERE name = 'NPT Size' AND product_families LIKE '%FS10000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 9);

-- Verify the updates
SELECT id, name, product_families, choices, adders FROM options WHERE name = 'NPT Size' ORDER BY id; 