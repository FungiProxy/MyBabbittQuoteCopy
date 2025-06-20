-- Add TRAN-EX options for LS8000/2 family
-- TRAN-EX is an extra probe, housing, and transmitter for two-probe applications
-- Base price: $540 for S material, $650 for H material
-- Length adders: S = $45/foot, H = $110/foot

-- Add TRAN-EX option for LS8000/2
INSERT INTO options (name, description, price, price_type, category, product_families, choices, adders) VALUES
('TRAN-EX', 'Extra probe, housing, and transmitter for two-probe applications', 0.0, 'fixed', 'Accessories', 'LS8000/2', 
 '["No", "Yes"]', '{"No": 0, "Yes": 540}');

-- Add TRAN-EX Material option (for when TRAN-EX is selected)
INSERT INTO options (name, description, price, price_type, category, product_families, choices, adders) VALUES
('TRAN-EX Material', 'TRAN-EX probe material selection', 0.0, 'fixed', 'Accessories', 'LS8000/2', 
 '["S", "H"]', '{"S": 0, "H": 110}');

-- Add TRAN-EX Length option (for when TRAN-EX is selected)
-- This will use the standard length adder logic from the configuration service
INSERT INTO options (name, description, price, price_type, category, product_families, choices, adders) VALUES
('TRAN-EX Length', 'TRAN-EX probe length in inches', 0.0, 'per_inch', 'Accessories', 'LS8000/2', 
 '["10", "12", "18", "24", "36", "48", "60", "72", "84", "96", "108", "120"]', 
 '{"10": 0, "12": 0, "18": 0, "24": 0, "36": 0, "48": 0, "60": 0, "72": 0, "84": 0, "96": 0, "108": 0, "120": 0}');

-- Add relationships to product_family_options for LS8000/2 (family_id = 7)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 7, id, 1 FROM options WHERE name IN ('TRAN-EX', 'TRAN-EX Material', 'TRAN-EX Length') 
AND product_families LIKE '%LS8000/2%';

-- Verify the additions
SELECT id, name, product_families, choices, adders FROM options WHERE name LIKE '%TRAN-EX%' ORDER BY id; 