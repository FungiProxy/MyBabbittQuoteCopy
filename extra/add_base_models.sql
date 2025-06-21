-- SQL script to add base models for all product families
-- This script inserts the base model configurations for each product family

INSERT INTO "base_models" ("id", "product_family_id", "model_number", "description", "base_price", "base_length", "voltage", "material") VALUES 
(1, 1, 'LS2000-115VAC-S-10"', 'LS2000 Level Switch - Base Configuration', 425.0, 10.0, '115VAC', 'S'),
(2, 2, 'LS2100-24VDC-S-10"', 'LS2100 Level Switch - Base Configuration', 460.0, 10.0, '24VDC', 'S'),
(3, 3, 'LS6000-115VAC-S-10"', 'LS6000 Level Switch - Base Configuration', 550.0, 10.0, '115VAC', 'S'),
(4, 4, 'LS7000-115VAC-S-10"', 'LS7000 Level Switch - Base Configuration', 680.0, 10.0, '115VAC', 'S'),
(5, 5, 'LS7000/2-115VAC-H-10"', 'LS7000/2 Level Switch - Base Configuration', 770.0, 10.0, '115VAC', 'H'),
(6, 6, 'LS8000-115VAC-S-10"', 'LS8000 Level Switch - Base Configuration', 715.0, 10.0, '115VAC', 'S'),
(7, 7, 'LS8000/2-115VAC-H-10"', 'LS8000/2 Level Switch - Base Configuration', 850.0, 10.0, '115VAC', 'H'),
(8, 8, 'LT9000-115VAC-H-10"', 'LT9000 Level Transmitter - Base Configuration', 855.0, 10.0, '115VAC', 'H'),
(9, 9, 'FS10000-115VAC-S-6"', 'FS10000 Flow Switch - Base Configuration', 1885.0, 6.0, '115VAC', 'S'),
(10, 10, 'LS7500-BASE', 'LS7500 Presence/Absence Switch - Base Configuration', 0.0, 10.0, '115VAC', 'S'),
(11, 11, 'LS8500-BASE', 'LS8500 Presence/Absence Switch - Base Configuration', 0.0, 10.0, '115VAC', 'S');

-- Verify the insertions
SELECT 
    bm.id,
    pf.name as product_family,
    bm.model_number,
    bm.description,
    bm.base_price,
    bm.base_length,
    bm.voltage,
    bm.material
FROM base_models bm
JOIN product_families pf ON bm.product_family_id = pf.id
ORDER BY bm.id; 