-- Update insulator options based on price list analysis
-- Standard insulators: Delrin (SS), Teflon (Halar/coatings)
-- Optional insulators: Teflon upgrade, PEEK, Ceramic
-- Length-based pricing: 6", 8", 10", 12"

-- First, let's see current insulator options
SELECT id, name, product_families, choices, adders FROM options WHERE name = 'Insulator';

-- Update the existing insulator option to be more comprehensive
UPDATE options 
SET name = 'Insulator Material',
    description = 'Insulator material selection (standard vs optional materials)',
    choices = '["Standard", "Teflon Upgrade", "PEEK", "Ceramic"]',
    adders = '{"Standard": 0, "Teflon Upgrade": 40, "PEEK": 340, "Ceramic": 470}'
WHERE name = 'Insulator' AND id = (
    SELECT MIN(id) FROM options WHERE name = 'Insulator'
);

-- Create new insulator length option
INSERT INTO options (name, description, price, price_type, category, product_families, choices, adders) VALUES
('Insulator Length', 'Insulator length selection (standard vs extended lengths)', 0.0, 'fixed', 'Connections', 
 'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500', 
 '["Standard", "6\" Extended", "8\" Extended", "10\" Extended", "12\" Extended"]', 
 '{"Standard": 0, "6\" Extended": 150, "8\" Extended": 200, "10\" Extended": 250, "12\" Extended": 300}');

-- Update product_family_options for the updated insulator material option
-- Remove old insulator relationships first
DELETE FROM product_family_options 
WHERE option_id IN (SELECT id FROM options WHERE name = 'Insulator Material');

-- Add new relationships for insulator material (simplified approach)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 1, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS2000%'
UNION ALL
SELECT 2, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS2100%'
UNION ALL
SELECT 3, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS6000%'
UNION ALL
SELECT 4, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS7000%'
UNION ALL
SELECT 5, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS7000/2%'
UNION ALL
SELECT 6, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS8000%'
UNION ALL
SELECT 7, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS8000/2%'
UNION ALL
SELECT 8, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LT9000%'
UNION ALL
SELECT 9, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%FS10000%'
UNION ALL
SELECT 10, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS7500%'
UNION ALL
SELECT 11, id, 1 FROM options WHERE name = 'Insulator Material' AND product_families LIKE '%LS8500%';

-- Add relationships for insulator length (simplified approach)
INSERT INTO product_family_options (product_family_id, option_id, is_available)
SELECT 1, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS2000%'
UNION ALL
SELECT 2, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS2100%'
UNION ALL
SELECT 3, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS6000%'
UNION ALL
SELECT 4, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS7000%'
UNION ALL
SELECT 5, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS7000/2%'
UNION ALL
SELECT 6, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS8000%'
UNION ALL
SELECT 7, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS8000/2%'
UNION ALL
SELECT 8, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LT9000%'
UNION ALL
SELECT 9, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%FS10000%'
UNION ALL
SELECT 10, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS7500%'
UNION ALL
SELECT 11, id, 1 FROM options WHERE name = 'Insulator Length' AND product_families LIKE '%LS8500%';

-- Verify the updates
SELECT id, name, product_families, choices, adders FROM options WHERE name LIKE '%Insulator%' ORDER BY id; 