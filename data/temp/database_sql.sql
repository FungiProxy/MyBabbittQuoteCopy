BEGIN TRANSACTION;
DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
DROP TABLE IF EXISTS "base_models";
CREATE TABLE base_models (
	id INTEGER NOT NULL, 
	product_family_id INTEGER NOT NULL, 
	model_number VARCHAR NOT NULL, 
	description TEXT NOT NULL, 
	base_price FLOAT NOT NULL, 
	base_length FLOAT NOT NULL, 
	voltage VARCHAR NOT NULL, 
	material VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id)
);
DROP TABLE IF EXISTS "cable_length_options";
CREATE TABLE cable_length_options (
	id INTEGER NOT NULL, 
	product_family_id INTEGER NOT NULL, 
	length FLOAT NOT NULL, 
	price FLOAT, 
	is_available INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id)
);
DROP TABLE IF EXISTS "connection_options";
CREATE TABLE connection_options (
	id INTEGER NOT NULL, 
	type VARCHAR NOT NULL, 
	rating VARCHAR, 
	size VARCHAR NOT NULL, 
	price FLOAT, 
	product_family_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id)
);
DROP TABLE IF EXISTS "customers";
CREATE TABLE customers (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	company VARCHAR, 
	email VARCHAR, 
	phone VARCHAR, 
	address VARCHAR, 
	city VARCHAR, 
	state VARCHAR, 
	zip_code VARCHAR, 
	notes VARCHAR, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS "housing_type_options";
CREATE TABLE housing_type_options (
	id INTEGER NOT NULL, 
	product_family_id INTEGER NOT NULL, 
	housing_type_id INTEGER NOT NULL, 
	price FLOAT, 
	is_available INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id), 
	FOREIGN KEY(housing_type_id) REFERENCES housing_types (id)
);
DROP TABLE IF EXISTS "housing_types";
CREATE TABLE housing_types (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
DROP TABLE IF EXISTS "length_adder_rules";
CREATE TABLE length_adder_rules (
	id INTEGER NOT NULL, 
	product_family VARCHAR NOT NULL, 
	material_code VARCHAR NOT NULL, 
	adder_type VARCHAR NOT NULL, 
	first_threshold FLOAT NOT NULL, 
	adder_amount FLOAT NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS "material_availability";
CREATE TABLE material_availability (
	id INTEGER NOT NULL, 
	material_code VARCHAR NOT NULL, 
	product_type VARCHAR NOT NULL, 
	is_available BOOLEAN, 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(material_code) REFERENCES materials (code)
);
DROP TABLE IF EXISTS "material_options";
CREATE TABLE material_options (
	id INTEGER NOT NULL, 
	product_family_id INTEGER NOT NULL, 
	material_code VARCHAR NOT NULL, 
	display_name VARCHAR NOT NULL, 
	base_price FLOAT, 
	is_available INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id)
);
DROP TABLE IF EXISTS "materials";
CREATE TABLE materials (
	id INTEGER NOT NULL, 
	code VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	description TEXT, 
	base_length FLOAT NOT NULL, 
	length_adder_per_inch FLOAT, 
	length_adder_per_foot FLOAT, 
	has_nonstandard_length_surcharge BOOLEAN, 
	nonstandard_length_surcharge FLOAT, 
	base_price_adder FLOAT, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS "o_ring_material_options";
CREATE TABLE o_ring_material_options (
	id INTEGER NOT NULL, 
	product_family_id INTEGER NOT NULL, 
	material_type VARCHAR NOT NULL, 
	price FLOAT, 
	is_available INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id)
);
DROP TABLE IF EXISTS "options";
CREATE TABLE options (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description TEXT, 
	price FLOAT NOT NULL, 
	price_type VARCHAR, 
	category VARCHAR, 
	excluded_products VARCHAR, 
	product_families VARCHAR, 
	choices JSON, 
	adders JSON, 
	rules JSON, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS "product_families";
CREATE TABLE product_families (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description TEXT, 
	category VARCHAR, 
	base_model_number VARCHAR, 
	base_price FLOAT, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS "product_family_options";
CREATE TABLE product_family_options (
	product_family_id INTEGER NOT NULL, 
	option_id INTEGER NOT NULL, 
	is_available INTEGER, 
	family_specific_price FLOAT, 
	notes TEXT, 
	PRIMARY KEY (product_family_id, option_id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id), 
	FOREIGN KEY(option_id) REFERENCES options (id)
);
DROP TABLE IF EXISTS "products";
CREATE TABLE products (
	id INTEGER NOT NULL, 
	model_number VARCHAR NOT NULL, 
	description TEXT, 
	category VARCHAR, 
	base_price FLOAT NOT NULL, 
	base_length FLOAT, 
	voltage VARCHAR, 
	material VARCHAR, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS "quote_item_options";
CREATE TABLE quote_item_options (
	id INTEGER NOT NULL, 
	quote_item_id INTEGER NOT NULL, 
	option_id INTEGER NOT NULL, 
	quantity INTEGER, 
	price FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(quote_item_id) REFERENCES quote_items (id), 
	FOREIGN KEY(option_id) REFERENCES options (id)
);
DROP TABLE IF EXISTS "quote_items";
CREATE TABLE quote_items (
	id INTEGER NOT NULL, 
	quote_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER, 
	unit_price FLOAT NOT NULL, 
	length FLOAT, 
	material VARCHAR, 
	voltage VARCHAR, 
	description TEXT, 
	discount_percent FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(quote_id) REFERENCES quotes (id), 
	FOREIGN KEY(product_id) REFERENCES product_variants (id)
);
DROP TABLE IF EXISTS "quotes";
CREATE TABLE quotes (
	id INTEGER NOT NULL, 
	quote_number VARCHAR NOT NULL, 
	customer_id INTEGER NOT NULL, 
	date_created DATETIME, 
	expiration_date DATETIME, 
	status VARCHAR, 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES customers (id)
);
DROP TABLE IF EXISTS "spare_parts";
CREATE TABLE spare_parts (
	id INTEGER NOT NULL, 
	part_number VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	description TEXT, 
	price FLOAT NOT NULL, 
	product_family_id INTEGER, 
	category VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id)
);
DROP TABLE IF EXISTS "standard_lengths";
CREATE TABLE standard_lengths (
	id INTEGER NOT NULL, 
	material_code VARCHAR NOT NULL, 
	length FLOAT NOT NULL, 
	PRIMARY KEY (id)
);
DROP TABLE IF EXISTS "voltage_options";
CREATE TABLE voltage_options (
	id INTEGER NOT NULL, 
	product_family_id INTEGER NOT NULL, 
	voltage VARCHAR NOT NULL, 
	is_available INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_family_id) REFERENCES product_families (id)
);
INSERT INTO "alembic_version" ("version_num") VALUES ('add_length_adder_rules');
INSERT INTO "base_models" ("id","product_family_id","model_number","description","base_price","base_length","voltage","material") VALUES (1,1,'LS2000-115VAC-S-10"','LS2000 Level Switch - Base Configuration',425.0,10.0,'115VAC','S'),
 (2,2,'LS2100-24VDC-S-10"','LS2100 Level Switch - Base Configuration',460.0,10.0,'24VDC','S'),
 (3,3,'LS6000-115VAC-S-10"','LS6000 Level Switch - Base Configuration',550.0,10.0,'115VAC','S'),
 (4,4,'LS7000-115VAC-S-10"','LS7000 Level Switch - Base Configuration',680.0,10.0,'115VAC','S'),
 (5,5,'LS7000/2-115VAC-H-10"','LS7000/2 Level Switch - Base Configuration',770.0,10.0,'115VAC','H'),
 (6,6,'LS8000-115VAC-S-10"','LS8000 Level Switch - Base Configuration',715.0,10.0,'115VAC','S'),
 (7,7,'LS8000/2-115VAC-H-10"','LS8000/2 Level Switch - Base Configuration',850.0,10.0,'115VAC','H'),
 (8,8,'LT9000-115VAC-H-10"','LT9000 Level Transmitter - Base Configuration',855.0,10.0,'115VAC','H'),
 (9,9,'FS10000-115VAC-S-6"','FS10000 Flow Switch - Base Configuration',1885.0,6.0,'115VAC','S'),
 (10,10,'LS7500-BASE','LS7500 Presence/Absence Switch - Base Configuration',0.0,10.0,'115VAC','S'),
 (11,11,'LS8500-BASE','LS8500 Presence/Absence Switch - Base Configuration',0.0,10.0,'115VAC','S');
INSERT INTO "housing_types" ("id","name","description") VALUES (1,'Standard','Standard housing'),
 (2,'Explosion Proof','Explosion proof housing'),
 (3,'Weatherproof','Weatherproof housing');
INSERT INTO "length_adder_rules" ("id","product_family","material_code","adder_type","first_threshold","adder_amount","description") VALUES (1,'LS2000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (2,'LS2000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (3,'LS2000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (4,'LS2000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (5,'LS2100','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (6,'LS2100','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (7,'LS2100','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (8,'LS2100','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (9,'LS6000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (10,'LS6000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (11,'LS6000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (12,'LS6000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (13,'LS7000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (14,'LS7000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (15,'LS7000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (16,'LS7000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (17,'LS7000/2','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (18,'LS7000/2','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (19,'LS8000','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (20,'LS8000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (21,'LS8000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (22,'LS8000','C','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (23,'LS8000/2','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (24,'LS8000/2','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (25,'LT9000','H','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (26,'LT9000','TS','per_foot',24.0,110.0,'$110 per foot starting at 24"'),
 (27,'LS7500','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (28,'LS8500','S','per_foot',24.0,45.0,'$45 per foot starting at 24"'),
 (29,'FS10000','S','per_foot',18.0,45.0,'$45 per foot starting at 18"'),
 (30,'LS2000','U','per_inch',4.0,40.0,'$40 per inch starting at 4"'),
 (31,'LS2000','T','per_inch',4.0,50.0,'$50 per inch starting at 4"'),
 (32,'LS2100','U','per_inch',4.0,40.0,'$40 per inch starting at 4"'),
 (33,'LS2100','T','per_inch',4.0,50.0,'$50 per inch starting at 4"'),
 (34,'LS6000','CPVC','per_inch',5.0,50.0,'$50 per inch starting at 5"'),
 (35,'LS7000','CPVC','per_inch',5.0,50.0,'$50 per inch starting at 5"');
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (1,'S','316 Stainless Steel','Standard 316SS probe',10.0,0.0,45.0,0,0.0,0.0),
 (2,'H','Halar Coated','Halar coated probe',10.0,0.0,110.0,1,300.0,0.0),
 (3,'TS','Teflon Sleeve','Teflon sleeve probe',10.0,0.0,110.0,0,0.0,0.0),
 (4,'U','UHMWPE Blind End','UHMWPE blind end probe',4.0,40.0,0.0,0,0.0,0.0),
 (5,'T','Teflon Blind End','Teflon blind end probe',4.0,50.0,0.0,0,0.0,0.0),
 (6,'C','Cable','Cable probe',12.0,0.0,45.0,0,0.0,0.0),
 (7,'CPVC','CPVC Blind End','CPVC blind end probe',4.0,50.0,0.0,0,0.0,0.0),
 (8,'A','Alloy 20','Exotic metal',10.0,0.0,0.0,0,0.0,0.0),
 (9,'HB','Hastelloy-B','Exotic metal',10.0,0.0,0.0,0,0.0,0.0),
 (10,'HC','Hastelloy-C-276','Exotic metal',10.0,0.0,0.0,0,0.0,0.0),
 (11,'TT','Titanium','Exotic metal',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (1,'NEMA 4 Enclosure','10" x 8" x 4" NEMA 4 metal enclosure for receiver',0.0,'fixed','Accessories',NULL,'LS8000/2','["Yes", "No"]','{"Yes": 420, "No": 0}',NULL),
 (2,'GRK Exp Proof Enclosure','GRK explosion proof enclosure for receiver (2 each, NPT 3/4" conduit entries)',0.0,'fixed','Accessories',NULL,'LS8000',NULL,NULL,NULL),
 (11,'O-Rings','O-Ring material selection',0.0,'fixed','O-ring Material',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["Viton", "Silicon", "Buna-N", "EPDM", "PTFE", "Kalrez"]','{"Viton": 0, "Silicon": 0, "Buna-N": 0, "EPDM": 0, "PTFE": 0, "Kalrez": 295}',NULL),
 (13,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS2000','["115VAC", "24VDC"]','{"115VAC": 0, "24VDC": 0}',NULL),
 (14,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS2100','["24VDC"]','{"24VDC": 0}',NULL),
 (15,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS6000','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL),
 (16,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS7000','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL),
 (17,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS7000/2','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL),
 (18,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS8000','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL),
 (19,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS8000/2','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL),
 (20,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LT9000','["115VAC", "230VAC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "24VDC": 0}',NULL),
 (21,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'FS10000','["115VAC", "230VAC"]','{"115VAC": 0, "230VAC": 0}',NULL),
 (22,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS7500,LS8500','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL),
 (23,'Connection Type','Primary connection type selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["NPT", "Flange", "Tri-clamp"]','{"NPT": 0, "Flange": 0, "Tri-clamp": 0}',NULL),
 (24,'NPT Size','NPT connection size selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS8000,FS10000','["3/4\""]','{"3/4\"": 0}',NULL),
 (26,'Flange Type','Flange type selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["150#", "300#"]','{"150#": 0, "300#": 0}',NULL),
 (27,'Flange Size','Flange size selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["1\"", "1-1/2\"", "2\"", "3\"", "4\""]','{"1\"": 0, "1-1/2\"": 0, "2\"": 0, "3\"": 0, "4\"": 0}',NULL),
 (28,'Tri-clamp','Tri-clamp selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["1-1/2\" Tri-clamp Process Connection", "1-1/2\" Tri-clamp Spud", "2\" Tri-clamp Process Connection", "2\" Tri-clamp Spud"]','{"1-1/2\" Tri-clamp Process Connection": 280.0, "1-1/2\" Tri-clamp Spud": 170.0, "2\" Tri-clamp Process Connection": 330.0, "2\" Tri-clamp Spud": 220.0}',NULL),
 (29,'Insulator Material','Insulator material selection (standard vs optional materials)',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["Standard", "Teflon Upgrade", "PEEK", "Ceramic"]','{"Standard": 0, "Teflon Upgrade": 40, "PEEK": 340, "Ceramic": 470}',NULL),
 (30,'Extra Static Protection','Additional static protection for plastic pellets and resins',0.0,'fixed','Accessories',NULL,'LS2000','["Yes", "No"]','{"Yes": 30, "No": 0}',NULL),
 (31,'Bent Probe','Bent probe configuration',0.0,'fixed','Accessories',NULL,'LS2000,LS2100,LS6000,LS7000,LS8000','["Yes", "No"]','{"Yes": 50, "No": 0}',NULL),
 (32,'Stainless Steel Tag','Stainless steel identification tag',0.0,'fixed','Accessories',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000','["Yes", "No"]','{"Yes": 30, "No": 0}',NULL),
 (33,'3/4" Diameter Probe','3/4" diameter probe x 10"',0.0,'fixed','Accessories',NULL,'LS6000,LS7000','["Yes", "No"]','{"Yes": 175, "No": 0}',NULL),
 (34,'Twisted Shielded Pair','22 AWG, twisted shielded pair',0.0,'per_unit','Accessories',NULL,'LS8000,LS8000/2','["Yes", "No"]','{"Yes": 0.7, "No": 0}',NULL),
 (35,'NEMA 4 Enclosure','8" x 6" x 3.5" NEMA 4 metal enclosure for receiver',0.0,'fixed','Accessories',NULL,'LS8000','["Yes", "No"]','{"Yes": 245, "No": 0}',NULL),
 (36,'Additional Coaxial Cable','Additional coaxial cable',0.0,'per_unit','Accessories',NULL,'FS10000','["Yes", "No"]','{"Yes": 6.0, "No": 0}',NULL),
 (37,'GRK Exp Proof Enclosure','GRK explosion proof enclosure for receiver (2 each, 3/4" conduit entries)',0.0,'fixed','Accessories',NULL,'LS8000/2,FS10000','["Yes", "No"]','{"Yes": 1030, "No": 0}',NULL),
 (38,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS2000','["S", "H", "TS", "U", "T", "C", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (39,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS2100','["S", "H", "TS", "U", "T", "C", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (40,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS6000','["S", "H", "TS", "U", "T", "C", "CPVC", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "CPVC": 400, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (41,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS7000','["S", "H", "TS", "U", "T", "C", "CPVC", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "CPVC": 400, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (42,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS7000/2','["H", "TS", "A", "HC", "HB", "TT"]','{"H": 0, "TS": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (43,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS8000','["S", "H", "TS", "U", "T", "C", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (44,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS8000/2','["H", "TS", "A", "HC", "HB", "TT"]','{"H": 0, "TS": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (45,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LT9000','["H", "TS", "A", "HC", "HB", "TT"]','{"H": 0, "TS": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (46,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'FS10000','["S", "A", "HC", "HB", "TT"]','{"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (47,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS7500','["S", "A", "HC", "HB", "TT"]','{"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (48,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS8500','["S", "A", "HC", "HB", "TT"]','{"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}',NULL),
 (49,'NPT Size','NPT connection size selection',0.0,'fixed','Connections',NULL,'LS6000,LS7000,LS7000/2,LT9000','["1\"", "3/4\""]','{"1\"": 0, "3/4\"": 0}',NULL),
 (50,'NPT Size','NPT connection size selection',0.0,'fixed','Connections',NULL,'LS8000/2','["3/4\"", "1\""]','{"3/4\"": 0, "1\"": 0}',NULL),
 (51,'Insulator Length','Insulator length selection (standard vs extended lengths)',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["Standard", "6\" Extended", "8\" Extended", "10\" Extended", "12\" Extended"]','{"Standard": 0, "6\" Extended": 150, "8\" Extended": 200, "10\" Extended": 250, "12\" Extended": 300}',NULL),
 (52,'TRAN-EX','Extra probe, housing, and transmitter for two-probe applications',0.0,'fixed','Accessories',NULL,'LS8000/2','["No", "Yes"]','{"No": 0, "Yes": 540}',NULL),
 (53,'TRAN-EX Material','TRAN-EX probe material selection',0.0,'fixed','Accessories',NULL,'LS8000/2','["S", "H"]','{"S": 0, "H": 110}',NULL),
 (54,'TRAN-EX Length','TRAN-EX probe length in inches',0.0,'per_inch','Accessories',NULL,'LS8000/2','["10", "12", "18", "24", "36", "48", "60", "72", "84", "96", "108", "120"]','{"10": 0, "12": 0, "18": 0, "24": 0, "36": 0, "48": 0, "60": 0, "72": 0, "84": 0, "96": 0, "108": 0, "120": 0}',NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (1,'LS2000','LS2000 Level Switch','Point Level Switch',NULL,NULL),
 (2,'LS2100','LS2100 Level Switch','Point Level Switch',NULL,NULL),
 (3,'LS6000','LS6000 Level Switch','Point Level Switch',NULL,NULL),
 (4,'LS7000','LS7000 Level Switch','Point Level Switch',NULL,NULL),
 (5,'LS7000/2','LS7000/2 Level Switch','Multi-Point Level Switch',NULL,NULL),
 (6,'LS8000','LS8000 Level Switch','Point Level Switch',NULL,NULL),
 (7,'LS8000/2','LS8000/2 Level Switch','Multi-Point Level Switch',NULL,NULL),
 (8,'LT9000','LT9000 Level Switch','Continuous Level Transmitter',NULL,NULL),
 (9,'FS10000','FS10000 Level Switch','Flow Switch',NULL,NULL),
 (10,'LS7500','LS7500 Integral Flange Sensor','Presence/Absence Switch',NULL,NULL),
 (11,'LS8500','LS8500 Remote Mount Flange Sensor','Presence/Absence Switch',NULL,NULL);
INSERT INTO "product_family_options" ("product_family_id","option_id","is_available","family_specific_price","notes") VALUES (7,1,1,NULL,NULL),
 (6,2,1,NULL,NULL),
 (1,11,1,NULL,NULL),
 (2,11,1,NULL,NULL),
 (3,11,1,NULL,NULL),
 (4,11,1,NULL,NULL),
 (5,11,1,NULL,NULL),
 (6,11,1,NULL,NULL),
 (7,11,1,NULL,NULL),
 (8,11,1,NULL,NULL),
 (9,11,1,NULL,NULL),
 (10,11,1,NULL,NULL),
 (11,11,1,NULL,NULL),
 (1,13,1,NULL,NULL),
 (2,14,1,NULL,NULL),
 (3,15,1,NULL,NULL),
 (4,16,1,NULL,NULL),
 (5,17,1,NULL,NULL),
 (6,18,1,NULL,NULL),
 (7,19,1,NULL,NULL),
 (8,20,1,NULL,NULL),
 (9,21,1,NULL,NULL),
 (10,22,1,NULL,NULL),
 (11,22,1,NULL,NULL),
 (1,23,1,NULL,NULL),
 (2,23,1,NULL,NULL),
 (3,23,1,NULL,NULL),
 (4,23,1,NULL,NULL),
 (5,23,1,NULL,NULL),
 (6,23,1,NULL,NULL),
 (7,23,1,NULL,NULL),
 (8,23,1,NULL,NULL),
 (9,23,1,NULL,NULL),
 (10,23,1,NULL,NULL),
 (11,23,1,NULL,NULL),
 (1,24,1,NULL,NULL),
 (2,24,1,NULL,NULL),
 (1,26,1,NULL,NULL),
 (2,26,1,NULL,NULL),
 (3,26,1,NULL,NULL),
 (4,26,1,NULL,NULL),
 (5,26,1,NULL,NULL),
 (6,26,1,NULL,NULL),
 (7,26,1,NULL,NULL),
 (8,26,1,NULL,NULL),
 (9,26,1,NULL,NULL),
 (10,26,1,NULL,NULL),
 (11,26,1,NULL,NULL),
 (1,27,1,NULL,NULL),
 (2,27,1,NULL,NULL),
 (3,27,1,NULL,NULL),
 (4,27,1,NULL,NULL),
 (5,27,1,NULL,NULL),
 (6,27,1,NULL,NULL),
 (7,27,1,NULL,NULL),
 (8,27,1,NULL,NULL),
 (9,27,1,NULL,NULL),
 (10,27,1,NULL,NULL),
 (11,27,1,NULL,NULL),
 (1,28,1,NULL,NULL),
 (2,28,1,NULL,NULL),
 (3,28,1,NULL,NULL),
 (4,28,1,NULL,NULL),
 (5,28,1,NULL,NULL),
 (6,28,1,NULL,NULL),
 (7,28,1,NULL,NULL),
 (8,28,1,NULL,NULL),
 (9,28,1,NULL,NULL),
 (10,28,1,NULL,NULL),
 (11,28,1,NULL,NULL),
 (1,30,1,NULL,NULL),
 (1,31,1,NULL,NULL),
 (2,31,1,NULL,NULL),
 (3,31,1,NULL,NULL),
 (4,31,1,NULL,NULL),
 (6,31,1,NULL,NULL),
 (1,32,1,NULL,NULL),
 (2,32,1,NULL,NULL),
 (3,32,1,NULL,NULL),
 (4,32,1,NULL,NULL),
 (5,32,1,NULL,NULL),
 (6,32,1,NULL,NULL),
 (7,32,1,NULL,NULL),
 (8,32,1,NULL,NULL),
 (3,33,1,NULL,NULL),
 (4,33,1,NULL,NULL),
 (6,34,1,NULL,NULL),
 (7,34,1,NULL,NULL),
 (6,35,1,NULL,NULL),
 (9,36,1,NULL,NULL),
 (7,37,1,NULL,NULL),
 (9,37,1,NULL,NULL),
 (1,38,1,NULL,NULL),
 (2,39,1,NULL,NULL),
 (3,40,1,NULL,NULL),
 (4,41,1,NULL,NULL),
 (5,42,1,NULL,NULL),
 (6,43,1,NULL,NULL),
 (7,44,1,NULL,NULL),
 (8,45,1,NULL,NULL),
 (9,46,1,NULL,NULL),
 (10,47,1,NULL,NULL),
 (11,48,1,NULL,NULL),
 (3,49,1,NULL,NULL),
 (4,49,1,NULL,NULL),
 (5,49,1,NULL,NULL),
 (6,24,1,NULL,NULL),
 (6,50,1,NULL,NULL),
 (7,50,1,NULL,NULL),
 (8,49,1,NULL,NULL),
 (9,24,1,NULL,NULL),
 (1,29,1,NULL,NULL),
 (2,29,1,NULL,NULL),
 (3,29,1,NULL,NULL),
 (4,29,1,NULL,NULL),
 (5,29,1,NULL,NULL),
 (6,29,1,NULL,NULL),
 (7,29,1,NULL,NULL),
 (8,29,1,NULL,NULL),
 (9,29,1,NULL,NULL),
 (10,29,1,NULL,NULL),
 (11,29,1,NULL,NULL),
 (1,51,1,NULL,NULL),
 (2,51,1,NULL,NULL),
 (3,51,1,NULL,NULL),
 (4,51,1,NULL,NULL),
 (5,51,1,NULL,NULL),
 (6,51,1,NULL,NULL),
 (7,51,1,NULL,NULL),
 (8,51,1,NULL,NULL),
 (9,51,1,NULL,NULL),
 (10,51,1,NULL,NULL),
 (11,51,1,NULL,NULL),
 (7,52,1,NULL,NULL),
 (7,54,1,NULL,NULL),
 (7,53,1,NULL,NULL);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (1,'H',6.0),
 (11,'H',10.0),
 (2,'H',12.0),
 (3,'H',18.0),
 (4,'H',24.0),
 (5,'H',36.0),
 (6,'H',48.0),
 (7,'H',60.0),
 (8,'H',72.0),
 (9,'H',84.0),
 (10,'H',96.0);
DROP INDEX IF EXISTS "ix_base_models_id";
CREATE INDEX ix_base_models_id ON base_models (id);
DROP INDEX IF EXISTS "ix_base_models_model_number";
CREATE UNIQUE INDEX ix_base_models_model_number ON base_models (model_number);
DROP INDEX IF EXISTS "ix_customers_id";
CREATE INDEX ix_customers_id ON customers (id);
DROP INDEX IF EXISTS "ix_customers_name";
CREATE INDEX ix_customers_name ON customers (name);
DROP INDEX IF EXISTS "ix_material_availability_id";
CREATE INDEX ix_material_availability_id ON material_availability (id);
DROP INDEX IF EXISTS "ix_material_availability_material_code";
CREATE INDEX ix_material_availability_material_code ON material_availability (material_code);
DROP INDEX IF EXISTS "ix_material_availability_product_type";
CREATE INDEX ix_material_availability_product_type ON material_availability (product_type);
DROP INDEX IF EXISTS "ix_materials_code";
CREATE UNIQUE INDEX ix_materials_code ON materials (code);
DROP INDEX IF EXISTS "ix_materials_id";
CREATE INDEX ix_materials_id ON materials (id);
DROP INDEX IF EXISTS "ix_options_category";
CREATE INDEX ix_options_category ON options (category);
DROP INDEX IF EXISTS "ix_options_id";
CREATE INDEX ix_options_id ON options (id);
DROP INDEX IF EXISTS "ix_options_name";
CREATE INDEX ix_options_name ON options (name);
DROP INDEX IF EXISTS "ix_product_families_category";
CREATE INDEX ix_product_families_category ON product_families (category);
DROP INDEX IF EXISTS "ix_product_families_id";
CREATE INDEX ix_product_families_id ON product_families (id);
DROP INDEX IF EXISTS "ix_product_families_name";
CREATE INDEX ix_product_families_name ON product_families (name);
DROP INDEX IF EXISTS "ix_products_category";
CREATE INDEX ix_products_category ON products (category);
DROP INDEX IF EXISTS "ix_products_id";
CREATE INDEX ix_products_id ON products (id);
DROP INDEX IF EXISTS "ix_products_model_number";
CREATE INDEX ix_products_model_number ON products (model_number);
DROP INDEX IF EXISTS "ix_quote_item_options_id";
CREATE INDEX ix_quote_item_options_id ON quote_item_options (id);
DROP INDEX IF EXISTS "ix_quote_items_id";
CREATE INDEX ix_quote_items_id ON quote_items (id);
DROP INDEX IF EXISTS "ix_quotes_id";
CREATE INDEX ix_quotes_id ON quotes (id);
DROP INDEX IF EXISTS "ix_quotes_quote_number";
CREATE UNIQUE INDEX ix_quotes_quote_number ON quotes (quote_number);
DROP INDEX IF EXISTS "ix_spare_parts_category";
CREATE INDEX ix_spare_parts_category ON spare_parts (category);
DROP INDEX IF EXISTS "ix_spare_parts_id";
CREATE INDEX ix_spare_parts_id ON spare_parts (id);
DROP INDEX IF EXISTS "ix_spare_parts_part_number";
CREATE INDEX ix_spare_parts_part_number ON spare_parts (part_number);
DROP INDEX IF EXISTS "ix_standard_lengths_id";
CREATE INDEX ix_standard_lengths_id ON standard_lengths (id);
DROP INDEX IF EXISTS "ix_standard_lengths_material_code";
CREATE INDEX ix_standard_lengths_material_code ON standard_lengths (material_code);
COMMIT;
