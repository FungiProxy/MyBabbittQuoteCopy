"""
Service for exporting quotes to different formats (PDF, Word, etc.).
"""

import os
from docx import Document
from scripts.word_template_generator import create_quote_template, generate_quote_from_template
import logging

logger = logging.getLogger(__name__)

class QuoteExportService:
    """Service to handle exporting quote data to various document formats."""

    def __init__(self, template_path="data/templates/quote_template.docx"):
        self.template_path = template_path
        # Ensure the template exists
        if not os.path.exists(self.template_path):
            logger.info("Word template not found. Creating a new one...")
            create_quote_template()

    def generate_word_document(self, quote_data, output_path):
        """
        Generates a Word document from quote data using a template.
        """
        # The generate_quote_from_template function expects a simple dict
        # The quote_data is already in the right format.
        
        # The `generate_quote_from_template` function handles the file generation
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