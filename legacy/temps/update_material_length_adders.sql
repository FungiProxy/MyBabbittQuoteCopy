-- SQL script to update materials table with correct length adders
-- Based on materials.csv data

-- Update 316 Stainless Steel (S) - per foot pricing
UPDATE materials SET 
    length_adder_per_inch = 0.0,
    length_adder_per_foot = 45.0,
    has_nonstandard_length_surcharge = 0,
    nonstandard_length_surcharge = 0.0
WHERE code = 'S';

-- Update Halar Coated (H) - per foot pricing with nonstandard surcharge
UPDATE materials SET 
    length_adder_per_inch = 0.0,
    length_adder_per_foot = 110.0,
    has_nonstandard_length_surcharge = 1,
    nonstandard_length_surcharge = 300.0
WHERE code = 'H';

-- Update Teflon Sleeve (TS) - per foot pricing
UPDATE materials SET 
    length_adder_per_inch = 0.0,
    length_adder_per_foot = 110.0,
    has_nonstandard_length_surcharge = 0,
    nonstandard_length_surcharge = 0.0
WHERE code = 'TS';

-- Update UHMWPE Blind End (U) - per inch pricing
UPDATE materials SET 
    length_adder_per_inch = 40.0,
    length_adder_per_foot = 0.0,
    has_nonstandard_length_surcharge = 0,
    nonstandard_length_surcharge = 0.0
WHERE code = 'U';

-- Update Teflon Blind End (T) - per inch pricing
UPDATE materials SET 
    length_adder_per_inch = 50.0,
    length_adder_per_foot = 0.0,
    has_nonstandard_length_surcharge = 0,
    nonstandard_length_surcharge = 0.0
WHERE code = 'T';

-- Update Cable (C) - per foot pricing
UPDATE materials SET 
    length_adder_per_inch = 0.0,
    length_adder_per_foot = 45.0,
    has_nonstandard_length_surcharge = 0,
    nonstandard_length_surcharge = 0.0
WHERE code = 'C';

-- Update CPVC Blind End (CPVC) - per inch pricing
UPDATE materials SET 
    length_adder_per_inch = 50.0,
    length_adder_per_foot = 0.0,
    has_nonstandard_length_surcharge = 0,
    nonstandard_length_surcharge = 0.0
WHERE code = 'CPVC';

-- Update exotic metals (A, HB, HC, TT) - no length adders
UPDATE materials SET 
    length_adder_per_inch = 0.0,
    length_adder_per_foot = 0.0,
    has_nonstandard_length_surcharge = 0,
    nonstandard_length_surcharge = 0.0
WHERE code IN ('A', 'HB', 'HC', 'TT');

-- Verify the updates
SELECT 
    code,
    name,
    base_length,
    length_adder_per_inch,
    length_adder_per_foot,
    has_nonstandard_length_surcharge,
    nonstandard_length_surcharge
FROM materials
ORDER BY code; 