BEGIN TRANSACTION;
DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
DROP TABLE IF EXISTS "base_models";
CREATE TABLE "base_models" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"model_number"	VARCHAR NOT NULL,
	"description"	TEXT NOT NULL,
	"base_price"	FLOAT NOT NULL,
	"base_length"	FLOAT NOT NULL,
	"voltage"	VARCHAR NOT NULL,
	"material"	VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "cable_length_options";
CREATE TABLE "cable_length_options" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"length"	FLOAT NOT NULL,
	"price"	FLOAT,
	"is_available"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "connection_options";
CREATE TABLE "connection_options" (
	"id"	INTEGER NOT NULL,
	"type"	VARCHAR NOT NULL,
	"rating"	VARCHAR,
	"size"	VARCHAR NOT NULL,
	"price"	FLOAT,
	"product_family_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "customers";
CREATE TABLE "customers" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR NOT NULL,
	"company"	VARCHAR,
	"email"	VARCHAR,
	"phone"	VARCHAR,
	"address"	VARCHAR,
	"city"	VARCHAR,
	"state"	VARCHAR,
	"zip_code"	VARCHAR,
	"notes"	VARCHAR,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "exotic_metal_options";
CREATE TABLE "exotic_metal_options" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"metal_type"	VARCHAR NOT NULL,
	"price"	FLOAT,
	"is_available"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "housing_type_options";
CREATE TABLE "housing_type_options" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"housing_type_id"	INTEGER NOT NULL,
	"price"	FLOAT,
	"is_available"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("housing_type_id") REFERENCES "housing_types"("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "housing_types";
CREATE TABLE "housing_types" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR NOT NULL,
	"description"	VARCHAR,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
DROP TABLE IF EXISTS "material_availability";
CREATE TABLE "material_availability" (
	"id"	INTEGER NOT NULL,
	"material_code"	VARCHAR NOT NULL,
	"product_type"	VARCHAR NOT NULL,
	"is_available"	BOOLEAN,
	"notes"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("material_code") REFERENCES "materials"("code")
);
DROP TABLE IF EXISTS "material_options";
CREATE TABLE "material_options" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"material_code"	VARCHAR NOT NULL,
	"display_name"	VARCHAR NOT NULL,
	"base_price"	FLOAT,
	"is_available"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "materials";
CREATE TABLE "materials" (
	"id"	INTEGER NOT NULL,
	"code"	VARCHAR NOT NULL,
	"name"	VARCHAR NOT NULL,
	"description"	TEXT,
	"base_length"	FLOAT NOT NULL,
	"length_adder_per_inch"	FLOAT,
	"length_adder_per_foot"	FLOAT,
	"has_nonstandard_length_surcharge"	BOOLEAN,
	"nonstandard_length_surcharge"	FLOAT,
	"base_price_adder"	FLOAT,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "o_ring_material_options";
CREATE TABLE "o_ring_material_options" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"material_type"	VARCHAR NOT NULL,
	"price"	FLOAT,
	"is_available"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "options";
CREATE TABLE "options" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR NOT NULL,
	"description"	TEXT,
	"price"	FLOAT NOT NULL,
	"price_type"	VARCHAR,
	"category"	VARCHAR,
	"excluded_products"	VARCHAR,
	"product_families"	VARCHAR,
	"choices"	JSON,
	"adders"	JSON,
	"rules"	JSON,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "probe_length_options";
CREATE TABLE "probe_length_options" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"length"	FLOAT NOT NULL,
	"price"	FLOAT,
	"is_available"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "product_families";
CREATE TABLE "product_families" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR NOT NULL,
	"description"	TEXT,
	"category"	VARCHAR,
	"base_model_number"	VARCHAR,
	"base_price"	FLOAT,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "product_family_options";
CREATE TABLE "product_family_options" (
	"product_family_id"	INTEGER NOT NULL,
	"option_id"	INTEGER NOT NULL,
	"is_available"	INTEGER,
	"family_specific_price"	FLOAT,
	"notes"	TEXT,
	PRIMARY KEY("product_family_id","option_id"),
	FOREIGN KEY("option_id") REFERENCES "options"("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "products";
CREATE TABLE "products" (
	"id"	INTEGER NOT NULL,
	"model_number"	VARCHAR NOT NULL,
	"description"	TEXT,
	"category"	VARCHAR,
	"base_price"	FLOAT NOT NULL,
	"base_length"	FLOAT,
	"voltage"	VARCHAR,
	"material"	VARCHAR,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "quote_item_options";
CREATE TABLE "quote_item_options" (
	"id"	INTEGER NOT NULL,
	"quote_item_id"	INTEGER NOT NULL,
	"option_id"	INTEGER NOT NULL,
	"quantity"	INTEGER,
	"price"	FLOAT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("option_id") REFERENCES "options"("id"),
	FOREIGN KEY("quote_item_id") REFERENCES "quote_items"("id")
);
DROP TABLE IF EXISTS "quote_items";
CREATE TABLE "quote_items" (
	"id"	INTEGER NOT NULL,
	"quote_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER,
	"unit_price"	FLOAT NOT NULL,
	"length"	FLOAT,
	"material"	VARCHAR,
	"voltage"	VARCHAR,
	"description"	TEXT,
	"discount_percent"	FLOAT,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_id") REFERENCES "product_variants"("id"),
	FOREIGN KEY("quote_id") REFERENCES "quotes"("id")
);
DROP TABLE IF EXISTS "quotes";
CREATE TABLE "quotes" (
	"id"	INTEGER NOT NULL,
	"quote_number"	VARCHAR NOT NULL,
	"customer_id"	INTEGER NOT NULL,
	"date_created"	DATETIME,
	"expiration_date"	DATETIME,
	"status"	VARCHAR,
	"notes"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("customer_id") REFERENCES "customers"("id")
);
DROP TABLE IF EXISTS "spare_parts";
CREATE TABLE "spare_parts" (
	"id"	INTEGER NOT NULL,
	"part_number"	VARCHAR NOT NULL,
	"name"	VARCHAR NOT NULL,
	"description"	TEXT,
	"price"	FLOAT NOT NULL,
	"product_family_id"	INTEGER,
	"category"	VARCHAR,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
DROP TABLE IF EXISTS "standard_lengths";
CREATE TABLE "standard_lengths" (
	"id"	INTEGER NOT NULL,
	"material_code"	VARCHAR NOT NULL,
	"length"	FLOAT NOT NULL,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "voltage_options";
CREATE TABLE "voltage_options" (
	"id"	INTEGER NOT NULL,
	"product_family_id"	INTEGER NOT NULL,
	"voltage"	VARCHAR NOT NULL,
	"is_available"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_family_id") REFERENCES "product_families"("id")
);
INSERT INTO "alembic_version" ("version_num") VALUES ('806ecdc3a65b');
INSERT INTO "housing_types" ("id","name","description") VALUES (1,'Standard','Standard housing');
INSERT INTO "housing_types" ("id","name","description") VALUES (2,'Explosion Proof','Explosion proof housing');
INSERT INTO "housing_types" ("id","name","description") VALUES (3,'Weatherproof','Weatherproof housing');
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (1,'S','316 Stainless Steel','Standard 316SS probe',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (2,'H','Halar Coated','Halar coated probe',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (3,'TS','Teflon Sleeve','Teflon sleeve probe',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (4,'U','UHMWPE Blind End','UHMWPE blind end probe',4.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (5,'T','Teflon Blind End','Teflon blind end probe',4.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (6,'C','Cable','Cable probe',12.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (7,'CPVC','CPVC Blind End','CPVC blind end probe',4.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (8,'A','Alloy 20','Exotic metal',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (9,'HB','Hastelloy-B','Exotic metal',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (10,'HC','Hastelloy-C-276','Exotic metal',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "materials" ("id","code","name","description","base_length","length_adder_per_inch","length_adder_per_foot","has_nonstandard_length_surcharge","nonstandard_length_surcharge","base_price_adder") VALUES (11,'TT','Titanium','Exotic metal',10.0,0.0,0.0,0,0.0,0.0);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (1,'NEMA 4 Enclosure','10" x 8" x 4" NEMA 4 metal enclosure for receiver',0.0,'fixed','Accessories',NULL,'LS8000/2','["Yes", "No"]','{"Yes": 420, "No": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (2,'GRK Exp Proof Enclosure','GRK explosion proof enclosure for receiver (2 each, NPT 3/4" conduit entries)',0.0,'fixed','Accessories',NULL,'LS8000',NULL,NULL,NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (11,'O-Rings','O-Ring material selection',0.0,'fixed','O-ring Material',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["Viton", "Silicon", "Buna-N", "EPDM", "PTFE", "Kalrez"]','{"Viton": 0, "Silicon": 0, "Buna-N": 0, "EPDM": 0, "PTFE": 0, "Kalrez": 295}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (13,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS2000','["115VAC", "24VDC"]','{"115VAC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (14,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS2100','["24VDC"]','{"24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (15,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS6000','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (16,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS7000','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (17,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS7000/2','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (18,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS8000','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (19,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS8000/2','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (20,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LT9000','["115VAC", "230VAC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (21,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'FS10000','["115VAC", "230VAC"]','{"115VAC": 0, "230VAC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (22,'Voltage','Supply voltage selection',0.0,'fixed','Voltages',NULL,'LS7500,LS8500','["115VAC", "230VAC", "12VDC", "24VDC"]','{"115VAC": 0, "230VAC": 0, "12VDC": 0, "24VDC": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (23,'Connection Type','Primary connection type selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["NPT", "Flange", "Tri-clamp"]','{"NPT": 0, "Flange": 0, "Tri-clamp": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (24,'NPT Size','NPT connection size selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100','["3/4\""]','{"3/4\"": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (25,'NPT Size','NPT connection size selection',0.0,'fixed','Connections',NULL,'LS6000,LS7000','["1\"", "3/4\""]','{"1\"": 0, "3/4\"": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (26,'Flange Type','Flange type selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["150#", "300#"]','{"150#": 0, "300#": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (27,'Flange Size','Flange size selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["1\"", "1-1/2\"", "2\"", "3\"", "4\""]','{"1\"": 0, "1-1/2\"": 0, "2\"": 0, "3\"": 0, "4\"": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (28,'Tri-clamp','Tri-clamp selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["1-1/2\" Tri-clamp Process Connection", "1-1/2\" Tri-clamp Spud", "2\" Tri-clamp Process Connection", "2\" Tri-clamp Spud"]','{"1-1/2\" Tri-clamp Process Connection": 280.0, "1-1/2\" Tri-clamp Spud": 170.0, "2\" Tri-clamp Process Connection": 330.0, "2\" Tri-clamp Spud": 220.0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (29,'Insulator','Insulator material selection',0.0,'fixed','Connections',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500','["Delrin", "Teflon", "PEEK", "Ceramic"]','{"Delrin": 0, "Teflon": 40, "PEEK": 340, "Ceramic": 470}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (30,'Extra Static Protection','Additional static protection for plastic pellets and resins',0.0,'fixed','Accessories',NULL,'LS2000','["Yes", "No"]','{"Yes": 30, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (31,'Bent Probe','Bent probe configuration',0.0,'fixed','Accessories',NULL,'LS2000,LS2100,LS6000,LS7000,LS8000','["Yes", "No"]','{"Yes": 50, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (32,'Stainless Steel Tag','Stainless steel identification tag',0.0,'fixed','Accessories',NULL,'LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000','["Yes", "No"]','{"Yes": 30, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (33,'3/4" Diameter Probe','3/4" diameter probe x 10"',0.0,'fixed','Accessories',NULL,'LS6000,LS7000','["Yes", "No"]','{"Yes": 175, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (34,'Twisted Shielded Pair','22 AWG, twisted shielded pair',0.0,'per_unit','Accessories',NULL,'LS8000,LS8000/2','["Yes", "No"]','{"Yes": 0.7, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (35,'NEMA 4 Enclosure','8" x 6" x 3.5" NEMA 4 metal enclosure for receiver',0.0,'fixed','Accessories',NULL,'LS8000','["Yes", "No"]','{"Yes": 245, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (36,'Additional Coaxial Cable','Additional coaxial cable',0.0,'per_unit','Accessories',NULL,'FS10000','["Yes", "No"]','{"Yes": 6.0, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (37,'GRK Exp Proof Enclosure','GRK explosion proof enclosure for receiver (2 each, 3/4" conduit entries)',0.0,'fixed','Accessories',NULL,'LS8000/2,FS10000','["Yes", "No"]','{"Yes": 1030, "No": 0}',NULL);
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (38,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS2000','["S", "H", "TS", "U", "T", "C", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (39,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS2100','["S", "H", "TS", "U", "T", "C", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (40,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS6000','["S", "H", "TS", "U", "T", "C", "CPVC", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "CPVC": 400, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (41,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS7000','["S", "H", "TS", "U", "T", "C", "CPVC", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "U": 20, "T": 60, "C": 80, "CPVC": 400, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (42,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS7000/2','["H", "TS", "A", "HC", "HB", "TT"]','{"H": 0, "TS": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (43,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS8000','["S", "H", "TS", "C", "A", "HC", "HB", "TT"]','{"S": 0, "H": 110, "TS": 110, "C": 80, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (44,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS8000/2','["H", "TS", "A", "HC", "HB", "TT"]','{"H": 0, "TS": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (45,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LT9000','["H", "TS", "A", "HC", "HB", "TT"]','{"H": 0, "TS": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (46,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'FS10000','["S", "A", "HC", "HB", "TT"]','{"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (47,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS7500','["S", "A", "HC", "HB", "TT"]','{"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "options" ("id","name","description","price","price_type","category","excluded_products","product_families","choices","adders","rules") VALUES (48,'Material','Probe material selection (including exotic metals)',0.0,'fixed','Material',NULL,'LS8500','["S", "A", "HC", "HB", "TT"]','{"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0}','null');
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (1,'LS2000','LS2000 Level Switch','Point Level Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (2,'LS2100','LS2100 Level Switch','Point Level Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (3,'LS6000','LS6000 Level Switch','Point Level Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (4,'LS7000','LS7000 Level Switch','Point Level Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (5,'LS7000/2','LS7000/2 Level Switch','Multi-Point Level Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (6,'LS8000','LS8000 Level Switch','Point Level Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (7,'LS8000/2','LS8000/2 Level Switch','Multi-Point Level Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (8,'LT9000','LT9000 Level Switch','Continuous Level Transmitter',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (9,'FS10000','FS10000 Level Switch','Flow Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (10,'LS7500','LS7500 Integral Flange Sensor','Presence/Absence Switch',NULL,NULL);
INSERT INTO "product_families" ("id","name","description","category","base_model_number","base_price") VALUES (11,'LS8500','LS8500 Remote Mount Flange Sensor','Presence/Absence Switch',NULL,NULL);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (1,'H',6.0);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (2,'H',12.0);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (3,'H',18.0);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (4,'H',24.0);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (5,'H',36.0);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (6,'H',48.0);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (7,'H',60.0);
INSERT INTO "standard_lengths" ("id","material_code","length") VALUES (8,'H',72.0);
DROP INDEX IF EXISTS "ix_base_models_id";
CREATE INDEX "ix_base_models_id" ON "base_models" (
	"id"
);
DROP INDEX IF EXISTS "ix_base_models_model_number";
CREATE UNIQUE INDEX "ix_base_models_model_number" ON "base_models" (
	"model_number"
);
DROP INDEX IF EXISTS "ix_customers_id";
CREATE INDEX "ix_customers_id" ON "customers" (
	"id"
);
DROP INDEX IF EXISTS "ix_customers_name";
CREATE INDEX "ix_customers_name" ON "customers" (
	"name"
);
DROP INDEX IF EXISTS "ix_material_availability_id";
CREATE INDEX "ix_material_availability_id" ON "material_availability" (
	"id"
);
DROP INDEX IF EXISTS "ix_material_availability_material_code";
CREATE INDEX "ix_material_availability_material_code" ON "material_availability" (
	"material_code"
);
DROP INDEX IF EXISTS "ix_material_availability_product_type";
CREATE INDEX "ix_material_availability_product_type" ON "material_availability" (
	"product_type"
);
DROP INDEX IF EXISTS "ix_materials_code";
CREATE UNIQUE INDEX "ix_materials_code" ON "materials" (
	"code"
);
DROP INDEX IF EXISTS "ix_materials_id";
CREATE INDEX "ix_materials_id" ON "materials" (
	"id"
);
DROP INDEX IF EXISTS "ix_options_category";
CREATE INDEX "ix_options_category" ON "options" (
	"category"
);
DROP INDEX IF EXISTS "ix_options_id";
CREATE INDEX "ix_options_id" ON "options" (
	"id"
);
DROP INDEX IF EXISTS "ix_options_name";
CREATE INDEX "ix_options_name" ON "options" (
	"name"
);
DROP INDEX IF EXISTS "ix_product_families_category";
CREATE INDEX "ix_product_families_category" ON "product_families" (
	"category"
);
DROP INDEX IF EXISTS "ix_product_families_id";
CREATE INDEX "ix_product_families_id" ON "product_families" (
	"id"
);
DROP INDEX IF EXISTS "ix_product_families_name";
CREATE INDEX "ix_product_families_name" ON "product_families" (
	"name"
);
DROP INDEX IF EXISTS "ix_products_category";
CREATE INDEX "ix_products_category" ON "products" (
	"category"
);
DROP INDEX IF EXISTS "ix_products_id";
CREATE INDEX "ix_products_id" ON "products" (
	"id"
);
DROP INDEX IF EXISTS "ix_products_model_number";
CREATE INDEX "ix_products_model_number" ON "products" (
	"model_number"
);
DROP INDEX IF EXISTS "ix_quote_item_options_id";
CREATE INDEX "ix_quote_item_options_id" ON "quote_item_options" (
	"id"
);
DROP INDEX IF EXISTS "ix_quote_items_id";
CREATE INDEX "ix_quote_items_id" ON "quote_items" (
	"id"
);
DROP INDEX IF EXISTS "ix_quotes_id";
CREATE INDEX "ix_quotes_id" ON "quotes" (
	"id"
);
DROP INDEX IF EXISTS "ix_quotes_quote_number";
CREATE UNIQUE INDEX "ix_quotes_quote_number" ON "quotes" (
	"quote_number"
);
DROP INDEX IF EXISTS "ix_spare_parts_category";
CREATE INDEX "ix_spare_parts_category" ON "spare_parts" (
	"category"
);
DROP INDEX IF EXISTS "ix_spare_parts_id";
CREATE INDEX "ix_spare_parts_id" ON "spare_parts" (
	"id"
);
DROP INDEX IF EXISTS "ix_spare_parts_part_number";
CREATE INDEX "ix_spare_parts_part_number" ON "spare_parts" (
	"part_number"
);
DROP INDEX IF EXISTS "ix_standard_lengths_id";
CREATE INDEX "ix_standard_lengths_id" ON "standard_lengths" (
	"id"
);
DROP INDEX IF EXISTS "ix_standard_lengths_material_code";
CREATE INDEX "ix_standard_lengths_material_code" ON "standard_lengths" (
	"material_code"
);
COMMIT;
