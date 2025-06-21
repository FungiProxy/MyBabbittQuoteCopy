-- Clean up duplicate options in the database
-- Keep the first occurrence of each option and remove duplicates

-- First, let's see what duplicates we have
SELECT name, COUNT(*) as count, GROUP_CONCAT(id) as ids
FROM options 
WHERE name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator')
GROUP BY name
HAVING COUNT(*) > 1;

-- Step 1: Remove product_family_options relationships for duplicate options
-- Keep relationships for the lowest ID option of each name, remove others
DELETE FROM product_family_options 
WHERE option_id IN (
    SELECT o2.id 
    FROM options o1, options o2 
    WHERE o1.name = o2.name 
    AND o1.id < o2.id
    AND o1.name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator')
);

-- Step 2: Now remove the duplicate options
DELETE FROM options 
WHERE id IN (
    SELECT o2.id 
    FROM options o1, options o2 
    WHERE o1.name = o2.name 
    AND o1.id < o2.id
    AND o1.name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator')
);

-- Verify the cleanup
SELECT name, COUNT(*) as count
FROM options 
WHERE name IN ('Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator')
GROUP BY name; 