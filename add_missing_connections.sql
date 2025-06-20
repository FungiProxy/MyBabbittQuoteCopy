-- Add missing connection options based on price list
-- These options are referenced in the price list but missing from the database

-- Add missing connection options for LS8000, LS8000/2, LT9000, FS10000
INSERT INTO options (name, description, price, price_type, category, product_families, choices, adders) VALUES
('Connection Type', 'Primary connection type selection', 0.0, 'fixed', 'Connections', 'LS8000,LS8000/2,LT9000,FS10000', 
 '["NPT", "Flange", "Tri-clamp"]', '{"NPT": 0, "Flange": 0, "Tri-clamp": 0}'),
('NPT Size', 'NPT connection size selection', 0.0, 'fixed', 'Connections', 'LS8000,LS8000/2,LT9000,FS10000', 
 '["3/4\"", "1\""]', '{"3/4\"": 0, "1\"": 0}'),
('Flange Type', 'Flange type selection', 0.0, 'fixed', 'Connections', 'LS8000,LS8000/2,LT9000,FS10000', 
 '["150#", "300#"]', '{"150#": 0, "300#": 0}'),
('Flange Size', 'Flange size selection', 0.0, 'fixed', 'Connections', 'LS8000,LS8000/2,LT9000,FS10000', 
 '["1\"", "1-1/2\"", "2\"", "3\"", "4\""]', '{"1\"": 0, "1-1/2\"": 0, "2\"": 0, "3\"": 0, "4\"": 0}'),
('Tri-clamp', 'Tri-clamp selection', 0.0, 'fixed', 'Connections', 'LS8000,LS8000/2,LT9000,FS10000', 
 '["1-1/2\" Tri-clamp Process Connection", "1-1/2\" Tri-clamp Spud", "2\" Tri-clamp Process Connection", "2\" Tri-clamp Spud"]', 
 '{"1-1/2\" Tri-clamp Process Connection": 280.0, "1-1/2\" Tri-clamp Spud": 170.0, "2\" Tri-clamp Process Connection": 330.0, "2\" Tri-clamp Spud": 220.0}'),
('Insulator', 'Insulator material selection', 0.0, 'fixed', 'Connections', 'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500', 
 '["Delrin", "Teflon", "PEEK", "Ceramic"]', '{"Delrin": 0, "Teflon": 40, "PEEK": 340, "Ceramic": 470}');

-- Now populate the product_family_options table for these new options
-- For LS8000 (family_id = 6)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 6, id, 1 FROM options WHERE name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator') 
AND product_families LIKE '%LS8000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 6);

-- For LS8000/2 (family_id = 7)  
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 7, id, 1 FROM options WHERE name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator') 
AND product_families LIKE '%LS8000/2%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 7);

-- For LT9000 (family_id = 8)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 8, id, 1 FROM options WHERE name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator') 
AND product_families LIKE '%LT9000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 8);

-- For FS10000 (family_id = 9)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 9, id, 1 FROM options WHERE name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator') 
AND product_families LIKE '%FS10000%'
AND id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = 9);

-- For all other families (1-5, 10-11) - add insulator option
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT pf.id, o.id, 1 
FROM product_families pf, options o 
WHERE o.name = 'Insulator' 
AND pf.id IN (1,2,3,4,5,10,11)
AND o.product_families LIKE '%LS2000%'
AND o.id NOT IN (SELECT option_id FROM product_family_options WHERE product_family_id = pf.id); 