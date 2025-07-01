# Export Template System - Quick Reference

## 🚀 Getting Started

### 1. Available Placeholders
All placeholders use the format: `{{placeholder_name}}`

### 2. Core Placeholder Categories

#### Customer Information
- `{{customer_name}}` - Customer's full name
- `{{customer_company}}` - Company name
- `{{customer_phone}}` - Phone number
- `{{customer_email}}` - Email address
- `{{customer_address}}` - Street address
- `{{customer_city}}`, `{{customer_state}}`, `{{customer_zip}}` - Address components

#### Quote Information
- `{{quote_number}}` - Unique quote identifier
- `{{quote_date}}` - Quote creation date
- `{{expiration_date}}` - Quote expiration date
- `{{total_price}}` - Final total amount
- `{{subtotal}}` - Subtotal before tax/shipping

#### Company Information
- `{{company_name}}` - Your company name
- `{{company_tagline}}` - Company tagline
- `{{company_address}}` - Company address
- `{{company_phone}}` - Company phone
- `{{company_email}}` - Company email

#### Product Information (for each line item)
- `{{product_1_name}}` - First product name
- `{{product_1_model}}` - Model number
- `{{product_1_material}}` - Material (Stainless Steel, HALAR, etc.)
- `{{product_1_connection_material}}` - Connection material (316SS, Alloy 20, etc.)
- `{{product_1_quantity}}` - Quantity
- `{{product_1_unit_price}}` - Unit price
- `{{product_1_total}}` - Line total

#### Technical Specifications
- `{{technical_specs}}` - Auto-generated technical specifications
- `{{material_notes}}` - Material-specific information
- `{{application_notes}}` - Application-specific notes
- `{{installation_notes}}` - Installation instructions
- `{{maintenance_notes}}` - Maintenance requirements

## 📝 Template Creation

### 1. Create Word Template
1. Open Microsoft Word
2. Create your document layout
3. Insert placeholders where you want data to appear
4. Save as `.docx` in `data/templates/` directory

### 2. Example Template Structure
```
{{company_name}}
{{company_tagline}}

QUOTATION
Quote #: {{quote_number}}
Date: {{quote_date}}

Customer: {{customer_name}}
Company: {{customer_company}}

{{line_items_table}}

Total: {{total_price}}
```

## ⚙️ Configuration

### 1. Company Information
Edit `data/templates/export_config.json`:
```json
{
  "company_info": {
    "company_name": "Your Company Name",
    "company_tagline": "Your Tagline",
    "company_address": "Your Address",
    "company_phone": "Your Phone",
    "company_email": "Your Email"
  }
}
```

### 2. Default Terms
```json
{
  "default_terms": {
    "payment_terms": "Net 30 days",
    "delivery_terms": "FCA Factory",
    "warranty_period": "12 months"
  }
}
```

## 🔧 Usage in Code

### 1. Basic Export
```python
from src.core.services.export_service import QuoteExportService

# Create export service
exporter = QuoteExportService()

# Prepare quote data
quote_data = {
    "quote_number": "Q-2024-0001",
    "customer": {
        "name": "John Smith",
        "company": "Acme Industries"
    },
    "items": [
        {
            "product": "LS2000 Level Sensor",
            "model_number": "LS2000-115VAC-S-24",
            "quantity": 2,
            "unit_price": 425.00
        }
    ]
}

# Generate Word document
exporter.generate_word_document(quote_data, "output.docx")
```

### 2. PDF Export
```python
from src.core.services.export_service import QuotePDFGenerator

pdf_generator = QuotePDFGenerator()
pdf_generator.generate_pdf_quote(quote_data, "output.pdf")
```

### 3. Email Generation
```python
from src.core.services.export_service import QuoteEmailGenerator

email_generator = QuoteEmailGenerator()
email_content = email_generator.generate_email_content(quote_data)
```

## 📋 Data Structure

### Quote Data Format
```python
quote_data = {
    "quote_number": "Q-2024-0001",
    "quote_date": "2024-01-15",
    "customer": {
        "name": "John Smith",
        "company": "Acme Industries",
        "phone": "(555) 123-4567",
        "email": "john@acme.com",
        "address": "123 Main St",
        "city": "Houston",
        "state": "TX",
        "zip": "77001"
    },
    "shipping": {
        "name": "John Smith",
        "company": "Acme Industries",
        "address": "456 Warehouse Blvd",
        "city": "Houston",
        "state": "TX",
        "zip": "77002"
    },
    "items": [
        {
            "product": "LS2000 Level Sensor",
            "product_family": "LS2000",
            "model_number": "LS2000-115VAC-S-24",
            "description": "High-temperature level sensor",
            "material": "S",
            "voltage": "115VAC",
            "length": 24,
            "quantity": 2,
            "unit_price": 425.00,
            "total_price": 850.00,
            "configuration": {
                "Connection Type": "NPT",
                "NPT Size": "1.5\"",
                "Extra Static Protection": True
            }
        }
    ],
    "subtotal": 850.00,
    "tax_rate": 8.25,
    "tax_amount": 70.13,
    "total_price": 920.13
}
```

## 🎨 Styling

### 1. Word Template Styling
- Use professional fonts (Arial, Calibri)
- Apply consistent spacing
- Use company colors for headers
- Include company logo if desired

### 2. PDF Styling
- Configure in `export_config.json` under `pdf_settings`
- Set page size, margins, fonts, colors
- Use professional color scheme

## 🔍 Troubleshooting

### Common Issues

1. **Placeholders not replaced**
   - Check placeholder syntax: `{{placeholder_name}}`
   - Ensure no spaces in placeholder names
   - Verify data is available in quote_data

2. **Template not found**
   - Check file path in `data/templates/`
   - Ensure file extension is `.docx`
   - Verify file permissions

3. **Formatting issues**
   - Check Word template formatting
   - Ensure placeholders are in single text runs
   - Test with sample data

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check template data
template_data = exporter._prepare_template_data(quote_data)
print(json.dumps(template_data, indent=2))
```

## 📚 Additional Resources

- **Full Placeholder Reference**: `data/templates/placeholder_reference.md`
- **Sample Template**: `data/templates/sample_quote_template.docx`
- **Configuration**: `data/templates/export_config.json`
- **Export Service**: `src/core/services/export_service.py`

## 🚀 Next Steps

1. **Customize Company Information** in `export_config.json`
2. **Create Your Template** using the sample as reference
3. **Test with Sample Data** to verify placeholders work
4. **Integrate with UI** for user-friendly export
5. **Add PDF Generation** using ReportLab or similar
6. **Implement Email Integration** for direct quote sending 