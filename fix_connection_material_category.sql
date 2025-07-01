-- Fix the category of Connection Material option
UPDATE options 
SET category = 'Connections' 
WHERE name = 'Connection Material' AND category = 'Connection Material'; 