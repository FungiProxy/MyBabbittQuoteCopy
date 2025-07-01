"""
Service for exporting quotes to different formats (PDF, Word, etc.).
"""

import os
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

class QuoteExportService:
    """Service to handle exporting quote data to various document formats."""

    def __init__(self, product_family):
        # Use one template per product family
        template_name = f"{product_family} Quote Template.docx"
        self.template_path = os.path.join("data", "templates", template_name)
        if not os.path.exists(self.template_path):
            logger.info(f"Word template not found for {product_family}. Creating a new one...")
            create_quote_template()  # Optionally pass product_family for custom creation

    def generate_word_document(self, quote_data, output_path):
        """
        Generates a Word document from quote data using a template.
        """
        # Add material display names to each item for template use
        for item in quote_data.get("items", []):
            material_code = item.get("material")
            item["material_display"] = MATERIAL_DISPLAY_NAMES.get(material_code, material_code or "")

        success = generate_quote_from_template(
            self.template_path,
            output_path,
            quote_data
        )

        if not success:
            raise Exception("Failed to generate Word document.")

class QuotePDFGenerator:
    """Dummy class for PDF generation."""
    def __init__(self, company_info, terms_and_conditions):
        pass

    def generate_pdf_quote(self, quote_data, file_path):
        logger.info(f"Generating PDF for quote {quote_data['quote_number']} at {file_path}")
        # This is a dummy implementation.
        # In a real scenario, you would use a library like reportlab to create a PDF.
        with open(file_path, 'w') as f:
            f.write(f"PDF for quote {quote_data['quote_number']}") 