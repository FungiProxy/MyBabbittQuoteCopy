-- Update standard lengths for Halar material
-- Correct standard lengths: 6, 10, 12, 18, 24, 36, 48, 60, 72, 84, 96

-- First, let's see what's currently in the table
SELECT 'Current standard lengths for Halar:' as info;
SELECT material_code, length FROM standard_lengths WHERE material_code = 'H' ORDER BY length;

-- Clear existing standard lengths for Halar
DELETE FROM standard_lengths WHERE material_code = 'H';

-- Insert the correct standard lengths
INSERT INTO standard_lengths (material_code, length) VALUES 
('H', 6.0),
('H', 10.0),
('H', 12.0),
('H', 18.0),
('H', 24.0),
('H', 36.0),
('H', 48.0),
('H', 60.0),
('H', 72.0),
('H', 84.0),
('H', 96.0);

-- Verify the complete list
SELECT 'Updated standard lengths for Halar:' as info;
SELECT material_code, length FROM standard_lengths WHERE material_code = 'H' ORDER BY length;

-- Expected result should be: 6, 10, 12, 18, 24, 36, 48, 60, 72, 84, 96 