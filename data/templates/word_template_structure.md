# Professional Word Document Quote Template Structure
## Complete Design Guide for quote_template.docx

### Document Settings
- **Page Size**: Letter (8.5" x 11")
- **Margins**: Top: 1", Bottom: 1", Left: 1", Right: 1"
- **Font**: Arial or Calibri for body text
- **Line Spacing**: 1.15 for body text

---

## HEADER SECTION

### Company Header (Top of Page)
**Format**: Center-aligned, Company colors background

```
[COMPANY LOGO PLACEHOLDER - Insert your logo here]

{{company_name}}
{{company_tagline}}

{{company_address}}
Phone: {{company_phone}} | Email: {{company_email}}
Website: {{company_website}}
```

**Formatting Instructions:**
- Company name: Font size 18pt, Bold, Color: #002347 (Professional Blue)
- Tagline: Font size 12pt, Italic, Color: #666666
- Address/contact: Font size 10pt, Regular, Color: #333333

---

## DOCUMENT TITLE SECTION

```
QUOTATION

Quote #: {{quote_number}}
Date: {{quote_date}}
Valid Until: {{expiration_date}}
```

**Formatting Instructions:**
- "QUOTATION": Font size 24pt, Bold, Center-aligned, Color: #002347
- Quote details: Font size 12pt, Right-aligned, in a bordered box

---

## CUSTOMER INFORMATION SECTION

### Bill To / Ship To (Two-column layout)

**Left Column - Bill To:**
```
BILL TO:
{{customer_name}}
{{customer_company}}
{{customer_address}}
{{customer_city}}, {{customer_state}} {{customer_zip}}
{{customer_country}}

Contact: {{customer_contact_name}}
Phone: {{customer_phone}}
Email: {{customer_email}}
```

**Right Column - Ship To:**
```
SHIP TO:
{{shipping_name}}
{{shipping_company}}
{{shipping_address}}
{{shipping_city}}, {{shipping_state}} {{shipping_zip}}
{{shipping_country}}

Delivery Notes: {{delivery_instructions}}
```

**Formatting Instructions:**
- Section headers ("BILL TO:", "SHIP TO:"): Font size 12pt, Bold, Color: #002347
- Content: Font size 11pt, Regular, Color: #333333
- Use table structure with no borders for alignment

---

## QUOTE DETAILS SECTION

```
Project: {{project_name}}
Reference: {{customer_reference}}
Sales Representative: {{sales_rep_name}}
Payment Terms: {{payment_terms}}
Delivery Terms: {{delivery_terms}}
```

**Formatting Instructions:**
- Font size 11pt, Regular
- Use alternating background colors (#f9f9f9 and white) for each row

---

## LINE ITEMS TABLE

**Table Structure:**
| Item | Product Description | Qty | Unit Price | Total |
|------|-------------------|-----|------------|-------|
| {{line_items_table}} | | | | |

**Sample Table Content:**
```
Item 1: {{product_1_name}}
       {{product_1_description}}
       Model: {{product_1_model}}
       Specifications: {{product_1_specs}}
       Options: {{product_1_options}}

Item 2: {{product_2_name}}
       {{product_2_description}}
       Model: {{product_2_model}}
       Specifications: {{product_2_specs}}
       Options: {{product_2_options}}

[Continue for additional items...]
```

**Table Formatting Instructions:**
- Header row: Background color #002347, Text color white, Font size 12pt, Bold
- Data rows: Alternating colors (#ffffff and #f9f9f9)
- Borders: 1pt solid #cccccc
- Column widths: Item (10%), Description (50%), Qty (10%), Unit Price (15%), Total (15%)
- Numbers: Right-aligned, Currency format for prices

---

## PRICING SUMMARY SECTION

```
                                    Subtotal:    {{subtotal}}
                                    Tax Rate:    {{tax_rate}}%
                                    Tax Amount:  {{tax_amount}}
                                    Shipping:    {{shipping_cost}}
                                    Discount:    {{discount_amount}}
                                    ────────────────────────────
                                    TOTAL:       {{total_price}}
```

**Formatting Instructions:**
- Right-aligned table
- Subtotal lines: Font size 11pt, Regular
- Total line: Font size 14pt, Bold, Background color #002347, Text color white
- Currency format for all amounts

---

## NOTES AND SPECIAL INSTRUCTIONS

```
Notes:
{{quote_notes}}

Special Instructions:
{{special_instructions}}

Delivery Information:
Expected delivery: {{expected_delivery_date}}
Shipping method: {{shipping_method}}
```

**Formatting Instructions:**
- Section headers: Font size 12pt, Bold, Color: #002347
- Content: Font size 11pt, Regular, Line spacing 1.5

---

## TERMS AND CONDITIONS SECTION

```
TERMS AND CONDITIONS

Payment Terms:
• Payment is due within {{payment_terms}} days of invoice date
• {{payment_method}} payments accepted
• Late payments subject to 1.5% monthly service charge

Delivery Terms:
• All prices are FOB shipping point unless otherwise specified
• Delivery dates are estimates and not guaranteed
• Customer is responsible for inspection upon delivery

Warranty:
• Products are covered by manufacturer's standard warranty
• Warranty period: {{warranty_period}}
• Warranty does not cover misuse, abuse, or normal wear

General Terms:
• Prices are valid for {{quote_validity_period}} days from quote date
• Prices subject to change without notice after expiration
• This quote is not an order confirmation
• Acceptance of this quote constitutes agreement to these terms
• Applicable taxes will be added to final invoice

Cancellation Policy:
• Orders may be cancelled within 24 hours of placement
• Custom or special order items are non-cancellable
• Cancellation fees may apply for orders in production

Returns:
• Returns require prior authorization
• Restocking fee: {{restocking_fee}}% applies to standard items
• Custom items are non-returnable
```

**Formatting Instructions:**
- Main header: Font size 14pt, Bold, Color: #002347
- Subheaders: Font size 12pt, Bold, Color: #002347
- Content: Font size 10pt, Regular, Bullet points for lists
- Box border around entire section: 1pt solid #cccccc

---

## FOOTER SECTION

**Page Footer (appears on every page):**
```
{{company_name}} | {{company_address}} | {{company_phone}} | {{company_email}}
Page {{page_number}} of {{total_pages}}

This document contains confidential and proprietary information.
```

**Formatting Instructions:**
- Font size 9pt, Regular, Color: #666666
- Center-aligned
- Border line above footer: 0.5pt solid #cccccc

---

## COMPLETE PLACEHOLDER LIST

### Customer Information
- `{{customer_name}}` - Customer full name
- `{{customer_company}}` - Customer company name
- `{{customer_address}}` - Customer street address
- `{{customer_city}}` - Customer city
- `{{customer_state}}` - Customer state/province
- `{{customer_zip}}` - Customer postal code
- `{{customer_country}}` - Customer country
- `{{customer_contact_name}}` - Primary contact person
- `{{customer_phone}}` - Customer phone number
- `{{customer_email}}` - Customer email address
- `{{customer_reference}}` - Customer reference number

### Shipping Information
- `{{shipping_name}}` - Shipping contact name
- `{{shipping_company}}` - Shipping company name
- `{{shipping_address}}` - Shipping street address
- `{{shipping_city}}` - Shipping city
- `{{shipping_state}}` - Shipping state/province
- `{{shipping_zip}}` - Shipping postal code
- `{{shipping_country}}` - Shipping country
- `{{delivery_instructions}}` - Special delivery instructions

### Quote Information
- `{{quote_number}}` - Unique quote identifier
- `{{quote_date}}` - Quote creation date
- `{{expiration_date}}` - Quote expiration date
- `{{quote_status}}` - Current quote status
- `{{project_name}}` - Project or job name
- `{{quote_notes}}` - Additional notes
- `{{special_instructions}}` - Special handling instructions

### Company Information
- `{{company_name}}` - Your company name
- `{{company_tagline}}` - Company tagline or slogan
- `{{company_address}}` - Company full address
- `{{company_phone}}` - Company phone number
- `{{company_email}}` - Company email address
- `{{company_website}}` - Company website URL

### Product Information
- `{{product_1_name}}` - First product name
- `{{product_1_description}}` - First product description
- `{{product_1_model}}` - First product model number
- `{{product_1_specs}}` - First product specifications
- `{{product_1_options}}` - First product selected options
- `{{line_items_table}}` - Complete line items table

### Pricing Information
- `{{subtotal}}` - Subtotal before tax and shipping
- `{{tax_rate}}` - Tax rate percentage
- `{{tax_amount}}` - Tax amount
- `{{shipping_cost}}` - Shipping cost
- `{{discount_amount}}` - Discount amount
- `{{total_price}}` - Final total amount

### Terms Information
- `{{payment_terms}}` - Payment terms (e.g., "Net 30")
- `{{payment_method}}` - Accepted payment methods
- `{{delivery_terms}}` - Delivery terms
- `{{warranty_period}}` - Warranty period
- `{{quote_validity_period}}` - Quote validity period
- `{{restocking_fee}}` - Restocking fee percentage
- `{{expected_delivery_date}}` - Expected delivery date
- `{{shipping_method}}` - Shipping method

### Document Meta Information
- `{{page_number}}` - Current page number
- `{{total_pages}}` - Total number of pages
- `{{current_date}}` - Today's date
- `{{sales_rep_name}}` - Sales representative name

---

## STEP-BY-STEP CREATION INSTRUCTIONS

### 1. Document Setup
1. Open Microsoft Word
2. Set page margins to 1" on all sides
3. Set default font to Arial 11pt
4. Set line spacing to 1.15

### 2. Create Header
1. Insert header section
2. Add company logo placeholder (Insert > Pictures > placeholder)
3. Type company information with placeholders
4. Format according to specifications above

### 3. Create Main Content
1. Add document title section
2. Create two-column table for customer information
3. Add quote details section
4. Insert line items table with proper formatting
5. Add pricing summary table (right-aligned)
6. Add notes section
7. Add terms and conditions section

### 4. Create Footer
1. Insert footer section
2. Add company information
3. Add page numbering
4. Add confidentiality notice

### 5. Apply Styling
1. Apply color scheme (#002347 for headers, #666666 for secondary text)
2. Set table borders and shading
3. Apply consistent formatting throughout
4. Test placeholder positioning

### 6. Save Template
1. Save as .docx format
2. Name: quote_template.docx
3. Location: data/templates/
4. Test with sample data to verify placeholder positions

---

## PROFESSIONAL STYLING GUIDELINES

### Color Scheme
- **Primary Blue**: #002347 (headers, company name, important text)
- **Secondary Gray**: #666666 (supporting text, footer)
- **Background Gray**: #f9f9f9 (alternating table rows, quote details box)
- **Border Gray**: #cccccc (table borders, section dividers)
- **White**: #ffffff (main background, alternating table rows)

### Typography
- **Headers**: Arial Bold, various sizes (12pt-24pt)
- **Body Text**: Arial Regular, 11pt
- **Footer Text**: Arial Regular, 9pt
- **Table Headers**: Arial Bold, 12pt

### Spacing
- **Section Spacing**: 18pt between major sections
- **Paragraph Spacing**: 6pt after paragraphs
- **Table Cell Padding**: 8pt all around
- **Line Height**: 1.15 for body text, 1.0 for addresses

This template structure provides a professional, comprehensive quote document that maintains brand consistency and includes all necessary business information.
