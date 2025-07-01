# Quote Template Placeholder Reference

This document provides a comprehensive reference for all available placeholders that can be used in quote templates.

## Customer Information
- `{{cust_name}}` - Customer name
- `{{cust_company}}` - Customer company name
- `{{cust_contact}}` - Contact person name
- `{{cust_phone}}` - Phone number
- `{{cust_email}}` - Email address
- `{{cust_ref}}` - Customer reference number
- `{{cust_addr}}` - Street address
- `{{cust_city}}` - City
- `{{cust_state}}` - State/Province
- `{{cust_zip}}` - ZIP/Postal code
- `{{cust_country}}` - Country (defaults to USA)

## Shipping Information
- `{{ship_name}}` - Shipping contact name
- `{{ship_company}}` - Shipping company name
- `{{ship_addr}}` - Shipping address
- `{{ship_city}}` - Shipping city
- `{{ship_state}}` - Shipping state
- `{{ship_zip}}` - Shipping ZIP code
- `{{ship_country}}` - Shipping country
- `{{delivery_notes}}` - Delivery instructions

## Quote Information
- `{{quote_num}}` - Quote number
- `{{quote_date}}` - Quote date (YYYY-MM-DD)
- `{{exp_date}}` - Expiration date
- `{{quote_status}}` - Quote status (Draft, Sent, etc.)
- `{{project}}` - Project name
- `{{notes}}` - General notes
- `{{special}}` - Special instructions

## Sales Representative
- `{{sales_name}}` - Sales rep name
- `{{sales_phone}}` - Sales rep phone
- `{{sales_email}}` - Sales rep email

## Pricing Information
- `{{subtotal}}` - Subtotal amount
- `{{tax_rate}}` - Tax rate percentage
- `{{tax_amt}}` - Tax amount
- `{{ship_cost}}` - Shipping cost
- `{{discount}}` - Discount amount
- `{{total}}` - Total price

## Company Information
- `{{company}}` - Company name
- `{{tagline}}` - Company tagline
- `{{comp_addr}}` - Company address
- `{{comp_phone}}` - Company phone
- `{{comp_email}}` - Company email
- `{{comp_web}}` - Company website

## Terms and Conditions
- `{{pay_terms}}` - Payment terms
- `{{pay_method}}` - Payment method
- `{{del_terms}}` - Delivery terms
- `{{warranty}}` - Warranty period
- `{{validity}}` - Quote validity period
- `{{restock}}` - Restocking fee
- `{{ship_method}}` - Shipping method

## Product Family Information
- `{{family}}` - Product family name
- `{{family_desc}}` - Product family description
- `{{insulator_desc}}` - Insulator description
- `{{housing_desc}}` - Housing description

## Technical Specifications
- `{{mat_note}}` - Material-specific notes
- `{{pressure}}` - Pressure rating
- `{{temp_range}}` - Temperature range
- `{{chem_comp}}` - Chemical compatibility
- `{{app_note}}` - Application notes
- `{{install}}` - Installation notes
- `{{maintenance}}` - Maintenance notes
- `{{length_notes}}` - Length-specific pricing notes
- `{{app_notes}}` - Application notes (detailed)
- `{{tech_specs}}` - Technical specifications
- `{{mat_notes}}` - Material notes (detailed)
- `{{safety}}` - Safety notes

## Individual Product Information (Up to 10 Products)

### Product 1
- `{{p1_name}}` - Product name
- `{{p1_desc}}` - Product description
- `{{p1_model}}` - Model number
- `{{p1_specs}}` - Product specifications
- `{{p1_opts}}` - Selected options
- `{{p1_mat}}` - Material (with display name)
- `{{p1_volt}}` - Voltage
- `{{p1_len}}` - Length with inches symbol
- `{{p1_conn}}` - Connection type
- `{{p1_connmat}}` - Connection material (with display name)
- `{{p1_insmat}}` - Insulator material (with display name)
- `{{p1_qty}}` - Quantity
- `{{p1_price}}` - Unit price
- `{{p1_total}}` - Total price for this item

### Product 2
- `{{p2_name}}` - Product name
- `{{p2_desc}}` - Product description
- `{{p2_model}}` - Model number
- `{{p2_specs}}` - Product specifications
- `{{p2_opts}}` - Selected options
- `{{p2_mat}}` - Material (with display name)
- `{{p2_volt}}` - Voltage
- `{{p2_len}}` - Length with inches symbol
- `{{p2_conn}}` - Connection type
- `{{p2_connmat}}` - Connection material (with display name)
- `{{p2_insmat}}` - Insulator material (with display name)
- `{{p2_qty}}` - Quantity
- `{{p2_price}}` - Unit price
- `{{p2_total}}` - Total price for this item

### Product 3-10
Same pattern as above, replacing the number (e.g., `{{p3_name}}`, `{{p4_mat}}`, etc.)

## Material Display Names

### Connection Materials
- S → 316SS
- A → Alloy 20
- HC → Hastelloy C-276
- HB → Hastelloy B
- TT → Titanium

### Insulator Materials
- TEF → Teflon
- DEL → Delrin
- PK → PEEK
- U → UHMWPE
- CER → Ceramic

## Length Pricing Notes
The following notes are automatically generated based on materials in the quote:

- **S (316SS)**: "For longer probes please add $45.00 per foot"
- **H (Halar)**: "For longer probes please add $110.00 per foot"
- **U (UHMWPE)**: "For longer probes please add $40.00 per inch"
- **T (Titanium)**: "For longer probes please add $50.00 per inch"
- **CPVC**: "For longer probes please add $50.00 per inch"

## Usage Examples

### Basic Quote Header
```
Quote #{{quote_num}}
Date: {{quote_date}}
Customer: {{cust_name}}
Company: {{cust_company}}
```

### Product Line Item
```
{{p1_qty}} x {{p1_name}} - {{p1_model}}
Material: {{p1_mat}}
Length: {{p1_len}}
Connection: {{p1_conn}} {{p1_connmat}}
Insulator: {{p1_insmat}}
Unit Price: {{p1_price}}
Total: {{p1_total}}
```

### Technical Notes Section
```
Technical Specifications:
{{tech_specs}}

Material Notes:
{{mat_notes}}

Length Pricing Notes:
{{length_notes}}
```

## Notes
- All placeholders are case-sensitive
- Placeholders that don't have data will be replaced with empty strings
- Currency values are automatically formatted with dollar signs and commas
- Dates are formatted as YYYY-MM-DD
- Product placeholders (p1-p10) are only populated if products exist in the quote 