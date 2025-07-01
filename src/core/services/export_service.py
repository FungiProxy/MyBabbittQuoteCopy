"""
Enhanced Service for exporting quotes to different formats (PDF, Word, etc.).
Supports comprehensive placeholder system for professional quote generation.
"""

import os
import json
from datetime import datetime, timedelta
from docx import Document
from scripts.word_template_generator import create_quote_template, generate_quote_from_template
import logging

logger = logging.getLogger(__name__)

# Map material codes to display names (expand as needed)
MATERIAL_DISPLAY_NAMES = {
    "S": "Stainless Steel",
    "H": "HALAR",
    "TS": "Teflon Sleeve",
    "U": "UHMWPE",
    "T": "Teflon",
    "C": "Cable",
    "A": "Alloy 20",
    "HC": "Hastelloy C-276",
    "HB": "Hastelloy B",
    "TT": "Titanium",
    # Add more as needed
}

# Map connection material codes to display names
CONNECTION_MATERIAL_DISPLAY_NAMES = {
    "S": "316SS",
    "A": "Alloy 20",
    "HC": "Hastelloy C-276", 
    "HB": "Hastelloy B",
    "TT": "Titanium",
}

# Map insulator material codes to display names
INSULATOR_MATERIAL_DISPLAY_NAMES = {
    "TEF": "Teflon",
    "DEL": "Delrin", 
    "PK": "PEEK",
    "U": "UHMWPE",
    "CER": "Ceramic",
}

# Material-specific notes for longer probes
MATERIAL_LENGTH_NOTES = {
    "S": "For longer probes please add $45.00 per foot",
    "H": "For longer probes please add $110.00 per foot", 
    "U": "For longer probes please add $40.00 per inch",
    "T": "For longer probes please add $50.00 per inch",
    "CPVC": "For longer probes please add $50.00 per inch",
}

# Company information - customize for your business
COMPANY_INFO = {
    "company_name": "Babbitt International",
    "company_tagline": "Level Controls & Systems",
    "company_address": "123 Business Ave, Houston, TX 77001",
    "company_phone": "(555) 987-6543",
    "company_email": "quotes@babbitt.com",
    "company_website": "www.babbittinternational.com"
}

# Default terms and conditions
DEFAULT_TERMS = {
    "payment_terms": "Net 30 days",
    "payment_method": "Check, Credit Card, Wire Transfer",
    "delivery_terms": "FCA Factory, Houston, TX",
    "warranty_period": "12 months",
    "quote_validity_period": "30 days",
    "restocking_fee": "15%",
    "shipping_method": "Ground Freight"
}

class QuoteExportService:
    """Enhanced service to handle exporting quote data to various document formats."""

    def __init__(self, product_family=None):
        self.product_family = product_family
        # Template path will be determined when generating the document
        self.template_path = None
            
    def _determine_template_path(self, quote_data):
        """Determine the appropriate template path based on quote data."""
        print(f"🔍 DETERMINING TEMPLATE PATH for quote: {quote_data.get('quote_number', 'Unknown')}")
        logger.info(f"Determining template path for quote data: {quote_data.get('quote_number', 'Unknown')}")
        
        # If product_family was specified in constructor, use it
        if self.product_family:
            template_name = f"{self.product_family} Quote Template.docx"
            template_path = os.path.join("data", "templates", template_name)
            print(f"🎯 Using specified product family: {self.product_family}")
            logger.info(f"Using specified product family: {self.product_family}")
            if os.path.exists(template_path):
                print(f"✅ Found template for specified family: {template_path}")
                logger.info(f"Found template for specified family: {template_path}")
                return template_path
        
        # Otherwise, try to determine from quote items
        items = quote_data.get("items", [])
        print(f"📦 Processing {len(items)} items for template selection")
        logger.info(f"Processing {len(items)} items for template selection")
        if items:
            # Get the most common product family from items
            families = {}
            for i, item in enumerate(items):
                print(f"📋 Item {i+1}: {item}")
                logger.info(f"Item {i+1}: {item}")
                # Check multiple possible field names for product family
                family = (item.get("product_family", "") or 
                         item.get("product", "") or 
                         item.get("name", ""))
                print(f"🏷️  Item {i+1} family: '{family}'")
                logger.info(f"Item {i+1} family: '{family}'")
                if family and family != "N/A":
                    families[family] = families.get(family, 0) + 1
            
            if families:
                # Use the most common family
                most_common_family = max(families.keys(), key=lambda k: families[k])
                print(f"🎯 Detected product family: {most_common_family}")
                logger.info(f"Detected product family: {most_common_family}")
                template_name = f"{most_common_family} Quote Template.docx"
                template_path = os.path.join("data", "templates", template_name)
                print(f"🔍 Looking for template: {template_path}")
                logger.info(f"Looking for template: {template_path}")
                if os.path.exists(template_path):
                    print(f"✅ Found template: {template_path}")
                    logger.info(f"Found template: {template_path}")
                    return template_path
                else:
                    print(f"❌ Template not found: {template_path}")
                    logger.warning(f"Template not found: {template_path}")
                    # List available templates for debugging
                    template_dir = os.path.join("data", "templates")
                    if os.path.exists(template_dir):
                        available_templates = [f for f in os.listdir(template_dir) if f.endswith('.docx')]
                        print(f"📁 Available templates: {available_templates}")
                        logger.info(f"Available templates: {available_templates}")
        
        # Fallback to default template
        default_template = os.path.join("data", "templates", "quote_template.docx")
        print(f"🔄 Falling back to default template: {default_template}")
        logger.info(f"Falling back to default template: {default_template}")
        if not os.path.exists(default_template):
            print(f"⚠️  Default template not found. Creating a new one...")
            logger.info(f"Default template not found. Creating a new one...")
            create_quote_template()
        return default_template

    def generate_word_document(self, quote_data, output_path):
        """
        Generates a Word document from quote data using a template with comprehensive placeholders.
        """
        print(f"🚀 GENERATING WORD DOCUMENT")
        print(f"📁 Output path: {output_path}")
        
        # Determine the appropriate template path
        self.template_path = self._determine_template_path(quote_data)
        print(f"📄 Using template: {self.template_path}")
        logger.info(f"Using template: {self.template_path}")
        
        # Prepare comprehensive data dictionary with all placeholders
        template_data = self._prepare_template_data(quote_data)
        
        # Add material display names to each item for template use
        for item in template_data.get("items", []):
            material_code = item.get("material")
            item["material_display"] = MATERIAL_DISPLAY_NAMES.get(material_code, material_code or "")

        success = generate_quote_from_template(
            self.template_path,
            output_path,
            template_data
        )

        if not success:
            raise Exception("Failed to generate Word document.")
        
        logger.info(f"Word document generated successfully: {output_path}")
        return True

    def _prepare_template_data(self, quote_data):
        """
        Prepare comprehensive template data with all available placeholders.
        """
        template_data = {}
        
        # Add company information
        template_data.update({
            "company": COMPANY_INFO["company_name"],
            "tagline": COMPANY_INFO["company_tagline"],
            "comp_addr": COMPANY_INFO["company_address"],
            "comp_phone": COMPANY_INFO["company_phone"],
            "comp_email": COMPANY_INFO["company_email"],
            "comp_web": COMPANY_INFO["company_website"],
        })
        
        # Add default terms
        template_data.update({
            "pay_terms": DEFAULT_TERMS["payment_terms"],
            "pay_method": DEFAULT_TERMS["payment_method"],
            "del_terms": DEFAULT_TERMS["delivery_terms"],
            "warranty": DEFAULT_TERMS["warranty_period"],
            "validity": DEFAULT_TERMS["quote_validity_period"],
            "restock": DEFAULT_TERMS["restocking_fee"],
            "ship_method": DEFAULT_TERMS["shipping_method"],
        })
        
        # Add current date/time information
        now = datetime.now()
        template_data.update({
            "current_date": now.strftime("%Y-%m-%d"),
            "current_time": now.strftime("%H:%M:%S"),
            "quote_created_date": now.strftime("%Y-%m-%d"),
            "quote_expires_date": (now + timedelta(days=30)).strftime("%Y-%m-%d")
        })
        
        # Add customer information - handle both customer object and direct fields
        customer = quote_data.get("customer", {})
        if not customer and isinstance(customer, dict):
            # If no customer object, try to get customer info from direct fields
            customer = {
                "name": quote_data.get("customer_name", ""),
                "company": quote_data.get("customer_company", ""),
                "contact_name": quote_data.get("contact_person", ""),
                "phone": quote_data.get("customer_phone", ""),
                "email": quote_data.get("customer_email", ""),
                "reference": quote_data.get("customer_ref", ""),
                "address": quote_data.get("customer_address", ""),
                "city": quote_data.get("customer_city", ""),
                "state": quote_data.get("customer_state", ""),
                "zip": quote_data.get("customer_zip", ""),
                "country": quote_data.get("customer_country", "USA"),
            }
        
        template_data.update({
            "cust_name": customer.get("name", ""),
            "cust_company": customer.get("company", ""),
            "cust_contact": customer.get("contact_name", ""),
            "cust_phone": customer.get("phone", ""),
            "cust_email": customer.get("email", ""),
            "cust_ref": customer.get("reference", ""),
            "cust_addr": customer.get("address", ""),
            "cust_city": customer.get("city", ""),
            "cust_state": customer.get("state", ""),
            "cust_zip": customer.get("zip", ""),
            "cust_country": customer.get("country", "USA"),
        })
        
        # Add shipping information (use customer info if not specified)
        shipping = quote_data.get("shipping", {})
        template_data.update({
            "ship_name": shipping.get("name", customer.get("name", "")),
            "ship_company": shipping.get("company", customer.get("company", "")),
            "ship_addr": shipping.get("address", customer.get("address", "")),
            "ship_city": shipping.get("city", customer.get("city", "")),
            "ship_state": shipping.get("state", customer.get("state", "")),
            "ship_zip": shipping.get("zip", customer.get("zip", "")),
            "ship_country": shipping.get("country", customer.get("country", "USA")),
            "delivery_notes": shipping.get("instructions", ""),
        })
        
        # Add quote information
        template_data.update({
            "quote_num": quote_data.get("quote_number", ""),
            "quote_date": quote_data.get("quote_date", now.strftime("%Y-%m-%d")),
            "exp_date": quote_data.get("expiration_date", (now + timedelta(days=30)).strftime("%Y-%m-%d")),
            "quote_status": quote_data.get("status", "Draft"),
            "project": quote_data.get("project_name", ""),
            "notes": quote_data.get("notes", ""),
            "special": quote_data.get("special_instructions", ""),
        })
        
        # Add sales representative information
        sales_rep = quote_data.get("sales_rep", {})
        template_data.update({
            "sales_name": sales_rep.get("name", "Sales Representative"),
            "sales_phone": sales_rep.get("phone", COMPANY_INFO["company_phone"]),
            "sales_email": sales_rep.get("email", COMPANY_INFO["company_email"]),
        })
        
        # Add pricing information
        template_data.update({
            "subtotal": self._format_currency(quote_data.get("subtotal", 0)),
            "tax_rate": f"{quote_data.get('tax_rate', 0):.2f}%",
            "tax_amt": self._format_currency(quote_data.get("tax_amount", 0)),
            "ship_cost": self._format_currency(quote_data.get("shipping_cost", 0)),
            "discount": self._format_currency(quote_data.get("discount_amount", 0)),
            "total": self._format_currency(quote_data.get("total_price", 0)),
        })
        
        # Add product information
        items = quote_data.get("items", [])
        template_data["items"] = items
        template_data["line_items_count"] = len(items)
        
        # Add individual product placeholders (up to 10 products)
        for i, item in enumerate(items[:10], 1):
            # Extract configuration data - handle both new and legacy formats
            config_data = item.get("config_data", {})
            legacy_config = item.get("configuration", {})
            
            # Use config_data if available, otherwise fall back to legacy configuration
            if isinstance(config_data, dict) and config_data:
                configuration = config_data
            elif isinstance(legacy_config, dict) and legacy_config:
                configuration = legacy_config
            else:
                configuration = {}
            
            # Extract specific fields from configuration
            voltage = configuration.get("Voltage", "")
            material = configuration.get("Material", "")
            connection_type = configuration.get("Connection Type", "")
            connection_material = configuration.get("Connection Material", "")
            insulator_material = configuration.get("Insulator Material", "")
            length = configuration.get("Probe Length", "")
            
            # Fallback to direct item fields if not in configuration
            if not voltage:
                voltage = item.get("voltage", "")
            if not material:
                material = item.get("material", "")
            if not length:
                length = item.get("length", "")
            
            template_data.update({
                f"p{i}_name": item.get("model_number", item.get("product", "")),
                f"p{i}_desc": item.get("description", ""),
                f"p{i}_model": item.get("model_number", ""),
                f"p{i}_specs": self._format_product_specs(item),
                f"p{i}_opts": self._format_product_options(item),
                f"p{i}_mat": MATERIAL_DISPLAY_NAMES.get(material, material),
                f"p{i}_volt": voltage,
                f"p{i}_len": f"{length}\"" if length else "",
                f"p{i}_conn": connection_type,
                f"p{i}_connmat": self._format_connection_material(item),
                f"p{i}_insmat": self._format_insulator_material(item),
                f"p{i}_qty": str(item.get("quantity", 1)),
                f"p{i}_price": self._format_currency(item.get("unit_price", 0)),
                f"p{i}_total": self._format_currency(item.get("total_price", 0)),
            })
        
        # Add product family information
        if items:
            first_item = items[0]
            # Try multiple possible field names for product family
            product_family = (first_item.get("product_family", "") or 
                            first_item.get("product", "") or 
                            first_item.get("name", ""))
            
            # If still empty, try to extract from product name
            if not product_family:
                product_name = first_item.get("product", "")
                if product_name and "-" in product_name:
                    # Extract family from product name like "LS2000-24DC-H-36"-12"TEFINS"
                    product_family = product_name.split("-")[0]
            
            template_data.update({
                "family": product_family,
                "family_desc": self._get_product_family_description(product_family),
                "insulator_desc": self._get_insulator_description(product_family),
                "housing_desc": self._get_housing_description(product_family),
            })
        
        # Add technical specifications
        template_data.update({
            "mat_note": self._generate_material_notes(items),
            "pressure": self._get_pressure_rating(items),
            "temp_range": self._get_temperature_range(items),
            "chem_comp": self._get_chemical_compatibility(items),
            "app_note": self._generate_application_notes(items),
            "install": self._generate_installation_notes(items),
            "maintenance": self._generate_maintenance_notes(items),
            "length_notes": self._generate_length_notes(items),
        })
        
        # Add special dynamic content
        template_data.update({
            "app_notes": self._generate_application_notes(items),
            "tech_specs": self._generate_technical_specs(items),
            "mat_notes": self._generate_material_notes(items),
            "safety": self._generate_safety_notes(items),
        })
        
        # Add formatting placeholders
        template_data.update({
            "currency_symbol": "$",
            "currency_code": "USD",
            "number_format": "1,234.56",
            "percentage_format": "8.25%",
        })
        
        # Add document meta information
        template_data.update({
            "document_type": "Quote",
            "document_version": "1.0",
        })
        
        return template_data

    def _format_currency(self, amount):
        """Format amount as currency string."""
        if amount is None:
            return "$0.00"
        return f"${amount:.2f}"

    def _format_product_specs(self, item):
        """Format product specifications as a readable string."""
        specs = []
        
        # Extract configuration data - handle both new and legacy formats
        config_data = item.get("config_data", {})
        legacy_config = item.get("configuration", {})
        
        # Use config_data if available, otherwise fall back to legacy configuration
        if isinstance(config_data, dict) and config_data:
            configuration = config_data
        elif isinstance(legacy_config, dict) and legacy_config:
            configuration = legacy_config
        else:
            configuration = {}
        
        # Extract specific fields from configuration
        length = configuration.get("Probe Length", "")
        voltage = configuration.get("Voltage", "")
        material = configuration.get("Material", "")
        
        # Fallback to direct item fields if not in configuration
        if not length:
            length = item.get("length", "")
        if not voltage:
            voltage = item.get("voltage", "")
        if not material:
            material = item.get("material", "")
        
        if length:
            specs.append(f"{length}\" probe")
        if voltage:
            specs.append(voltage)
        if material:
            material_display = MATERIAL_DISPLAY_NAMES.get(material, material)
            specs.append(material_display)
        
        return ", ".join(specs)

    def _format_product_options(self, item):
        """Format product options as a readable string."""
        # Check for options in config_data (new format)
        config_data = item.get("config_data", {})
        if isinstance(config_data, dict) and config_data:
            options = config_data
        else:
            # Fallback to legacy configuration format
            options = item.get("configuration", {})
        
        if not options:
            return ""
        
        # Handle case where configuration is a string (legacy format)
        if isinstance(options, str):
            return options
        
        # Handle case where configuration is a dictionary
        option_list = []
        for key, value in options.items():
            if value and value not in [True, False]:
                option_list.append(f"{key}: {value}")
            elif value is True:
                option_list.append(key)
        
        return ", ".join(option_list)

    def _format_connection_material(self, item):
        """Format connection material with proper display names."""
        # Check for connection material in config_data (new format)
        config_data = item.get("config_data", {})
        if isinstance(config_data, dict):
            connection_material = config_data.get("Connection Material", "")
            if connection_material:
                return CONNECTION_MATERIAL_DISPLAY_NAMES.get(connection_material, connection_material)
        
        # Check for connection material in configuration (legacy format)
        config = item.get("configuration", {})
        if isinstance(config, dict):
            connection_material = config.get("Connection Material", "")
            if connection_material:
                return CONNECTION_MATERIAL_DISPLAY_NAMES.get(connection_material, connection_material)
        
        # Fallback to checking if it's stored directly in the item
        connection_material = item.get("connection_material", "")
        if connection_material:
            return CONNECTION_MATERIAL_DISPLAY_NAMES.get(connection_material, connection_material)
        
        return ""

    def _format_insulator_material(self, item):
        """Format insulator material with proper display names."""
        # Check for insulator material in config_data (new format)
        config_data = item.get("config_data", {})
        if isinstance(config_data, dict):
            insulator_material = config_data.get("Insulator Material", "")
            if insulator_material:
                return INSULATOR_MATERIAL_DISPLAY_NAMES.get(insulator_material, insulator_material)
        
        # Check for insulator material in configuration (legacy format)
        config = item.get("configuration", {})
        if isinstance(config, dict):
            insulator_material = config.get("Insulator Material", "")
            if insulator_material:
                return INSULATOR_MATERIAL_DISPLAY_NAMES.get(insulator_material, insulator_material)
        
        # Fallback to checking if it's stored directly in the item
        insulator_material = item.get("insulator_material", "")
        if insulator_material:
            return INSULATOR_MATERIAL_DISPLAY_NAMES.get(insulator_material, insulator_material)
        
        return ""

    def _get_product_family_description(self, product_family):
        """Get product family description."""
        descriptions = {
            "LS2000": "High-temperature level sensors",
            "LS2100": "Enhanced level sensors for extreme environments",
            "LS6000": "Continuous service level sensors",
            "LS7000": "Explosion-proof level sensors",
            "LS8000": "Industrial transmitter level sensors",
            "FS10000": "Float switch level sensors",
            "LT9000": "Level transmitter sensors",
        }
        return descriptions.get(product_family, "Level sensor")

    def _get_insulator_description(self, product_family):
        """Get insulator description for product family."""
        descriptions = {
            "LS2000": "High-temperature ceramic insulator, rated to 500°F",
            "LS2100": "Enhanced ceramic insulator with improved thermal characteristics",
            "LS6000": "Continuous service ceramic insulator, rated to 600°F",
            "LS7000": "Advanced ceramic insulator with extended temperature range",
            "LS8000": "Industrial transmitter ceramic insulator, rated to 700°F",
            "FS10000": "Standard ceramic insulator, rated to 450°F",
            "LT9000": "Level transmitter ceramic insulator",
        }
        return descriptions.get(product_family, "Ceramic insulator")

    def _get_housing_description(self, product_family):
        """Get housing description for product family."""
        descriptions = {
            "LS2000": "NEMA 4X, IP65 rated 316 Stainless Steel or HALAR coated enclosure",
            "LS2100": "NEMA 4X, IP67 rated enclosure with enhanced sealing",
            "LS6000": "NEMA 4X, IP68 rated enclosure designed for continuous operation",
            "LS7000": "NEMA 7, explosion-proof enclosure for hazardous locations",
            "LS8000": "NEMA 4X/7 dual-rated enclosure for versatile installation",
            "FS10000": "NEMA 4X, IP65 rated aluminum enclosure",
            "LT9000": "Compact NEMA 4X enclosure designed for space-constrained installations",
        }
        return descriptions.get(product_family, "NEMA 4X enclosure")

    def _generate_material_notes(self, items):
        """Generate material-specific notes based on items."""
        materials = set()
        for item in items:
            material = item.get("material")
            if material:
                materials.add(material)
        
        notes = []
        for material in materials:
            if material == "S":
                notes.append("316 Stainless Steel construction provides excellent corrosion resistance for most industrial applications.")
            elif material == "H":
                notes.append("HALAR (ECTFE) coating provides superior chemical resistance to acids, bases, and organic solvents.")
            elif material == "A":
                notes.append("Alloy 20 construction provides excellent resistance to sulfuric acid and other aggressive chemicals.")
        
        return " ".join(notes)

    def _generate_length_notes(self, items):
        """Generate length-specific notes based on materials in the quote."""
        if not items:
            return ""
        
        materials = set()
        for item in items:
            config = item.get("configuration", {})
            material = config.get("Material", "")
            if material:
                materials.add(material)
        
        notes = []
        for material in sorted(materials):
            if material in MATERIAL_LENGTH_NOTES:
                notes.append(MATERIAL_LENGTH_NOTES[material])
        
        return "\n".join(notes)

    def _get_pressure_rating(self, items):
        """Get pressure rating based on items."""
        # Default pressure rating
        return "1500 PSI continuous operation"

    def _get_temperature_range(self, items):
        """Get temperature range based on items."""
        # Default temperature range
        return "-100°F to 350°F"

    def _get_chemical_compatibility(self, items):
        """Get chemical compatibility based on items."""
        materials = set()
        for item in items:
            material = item.get("material")
            if material:
                materials.add(material)
        
        if "H" in materials:
            return "Superior resistance to acids, bases, and organic solvents"
        elif "S" in materials:
            return "Excellent corrosion resistance for most industrial applications"
        else:
            return "Standard chemical compatibility"

    def _generate_application_notes(self, items):
        """Generate application-specific notes."""
        if not items:
            return ""
        
        # Check for specific applications based on product families
        families = set(item.get("product_family") for item in items)
        
        notes = []
        if "LS7000" in families:
            notes.append("Certified for use in Class I Div 1 and Div 2 hazardous locations.")
        
        if any(item.get("material") == "H" for item in items):
            notes.append("HALAR coating provides superior chemical resistance for aggressive environments.")
        
        if not notes:
            notes.append("Designed for industrial level measurement applications.")
        
        return " ".join(notes)

    def _generate_technical_specs(self, items):
        """Generate technical specifications."""
        if not items:
            return ""
        
        specs = [
            "Temperature Range: -100°F to 350°F",
            "Pressure Rating: 1500 PSI continuous",
            "Electrical Rating: 115VAC or 24VDC",
            "Enclosure Rating: NEMA 4X, IP65",
            "Output Signal: 4-20mA or relay contact",
        ]
        
        return "\n".join(specs)

    def _generate_installation_notes(self, items):
        """Generate installation notes."""
        return "Mount vertically with minimum 1\" clearance from tank wall. Ensure proper grounding for electrical safety."

    def _generate_maintenance_notes(self, items):
        """Generate maintenance notes."""
        return "Annual calibration recommended. Inspect for damage or wear during routine maintenance."

    def _generate_safety_notes(self, items):
        """Generate safety notes."""
        families = set(item.get("product_family") for item in items)
        
        notes = ["Follow all applicable safety codes and regulations."]
        
        if "LS7000" in families:
            notes.append("Explosion-proof installation must be performed by qualified personnel.")
        
        return " ".join(notes)

class QuotePDFGenerator:
    """Enhanced PDF generator with comprehensive placeholder support."""
    def __init__(self, company_info=None, terms_and_conditions=None):
        self.company_info = company_info or COMPANY_INFO
        self.terms_and_conditions = terms_and_conditions or DEFAULT_TERMS

    def generate_pdf_quote(self, quote_data, file_path):
        """Generate PDF quote with comprehensive placeholder support."""
        logger.info(f"Generating PDF for quote {quote_data.get('quote_number', 'Unknown')} at {file_path}")
        
        # Use the same template data preparation as Word export
        export_service = QuoteExportService()
        template_data = export_service._prepare_template_data(quote_data)
        
        # TODO: Implement actual PDF generation using ReportLab or similar
        # For now, create a simple text file as placeholder
        with open(file_path, 'w') as f:
            f.write(f"PDF Quote: {template_data.get('quote_number', 'Unknown')}\n")
            f.write(f"Customer: {template_data.get('customer_name', '')}\n")
            f.write(f"Total: {template_data.get('total_price', '')}\n")
            f.write(f"Generated: {template_data.get('current_date', '')}\n")
        
        logger.info(f"PDF placeholder created at: {file_path}")
        return True

class QuoteEmailGenerator:
    """Email generator for sending quotes via email."""
    
    def __init__(self, company_info=None):
        self.company_info = company_info or COMPANY_INFO

    def generate_email_content(self, quote_data, template_path=None):
        """Generate email content with quote information."""
        export_service = QuoteExportService()
        template_data = export_service._prepare_template_data(quote_data)
        
        # Default email template
        if not template_path:
            template_path = os.path.join("data", "templates", "email_template.html")
        
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                email_template = f.read()
            
            # Replace placeholders in email template
            for key, value in template_data.items():
                placeholder = f"{{{{{key}}}}}"
                email_template = email_template.replace(placeholder, str(value))
            
            return email_template
        else:
            # Fallback to simple text email
            return self._generate_simple_email(template_data)

    def _generate_simple_email(self, template_data):
        """Generate simple text email as fallback."""
        email_content = f"""
Dear {template_data.get('customer_name', 'Customer')},

Please find attached our quote {template_data.get('quote_number', '')} for your review.

Quote Summary:
- Total Amount: {template_data.get('total_price', '')}
- Valid Until: {template_data.get('expiration_date', '')}

If you have any questions, please don't hesitate to contact us.

Best regards,
{template_data.get('company_name', 'Babbitt International')}
{template_data.get('company_phone', '')}
{template_data.get('company_email', '')}
        """
        return email_content.strip() 