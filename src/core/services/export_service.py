"""
Service for exporting quote data to different file formats.
"""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import logging

logger = logging.getLogger(__name__)

class QuoteExportService:
    """
    Handles the logic for exporting a quote to a Word document.
    """
    def __init__(self, template_path):
        self.template_path = template_path

    def _replace_placeholder(self, paragraph, placeholder, value):
        """
        Replaces a placeholder in a paragraph with a given value, preserving style.
        """
        if placeholder in paragraph.text:
            inline = paragraph.runs
            # Replace the placeholder and keep the original style
            for i in range(len(inline)):
                if placeholder in inline[i].text:
                    text = inline[i].text.replace(placeholder, str(value))
                    inline[i].text = text
                    logger.debug(f"Replaced '{placeholder}' with '{value}'")
                    return
            # Fallback if the placeholder is split across runs
            paragraph.text = paragraph.text.replace(placeholder, str(value))
            logger.debug(f"Replaced '{placeholder}' with '{value}' (fallback)")

    def generate_word_document(self, quote_details, output_path):
        """
        Generates a .docx file from a template and quote data.
        """
        try:
            document = Document(self.template_path)
            
            placeholders = {
                "{{quote_number}}": quote_details.get('quote_number', 'N/A'),
                "{{customer_name}}": quote_details.get('customer', {}).get('name', 'N/A'),
                "{{customer_address}}": quote_details.get('customer', {}).get('address', 'N/A'),
                "{{date_created}}": quote_details.get('date_created', 'N/A'),
                "{{total_price}}": f"${quote_details.get('total_price', 0):,.2f}",
            }

            # Replace placeholders in paragraphs
            for paragraph in document.paragraphs:
                for key, value in placeholders.items():
                    self._replace_placeholder(paragraph, key, value)
            
            # Replace placeholders in tables (e.g., header/footer)
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            for key, value in placeholders.items():
                                self._replace_placeholder(paragraph, key, value)

            # Find the line items table and populate it
            # We assume the placeholder "{{line_items_table}}" is in a cell by itself
            # where we want to insert the line items.
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if "{{line_items_table}}" in cell.text:
                            cell.text = "" # Clear the placeholder
                            line_items_table = cell.add_table(rows=1, cols=4)
                            line_items_table.style = 'Table Grid'
                            hdr_cells = line_items_table.rows[0].cells
                            hdr_cells[0].text = 'Part Number'
                            hdr_cells[1].text = 'Description'
                            hdr_cells[2].text = 'Qty'
                            hdr_cells[3].text = 'Price'

                            for item in quote_details.get('line_items', []):
                                row_cells = line_items_table.add_row().cells
                                row_cells[0].text = item.get('part_number', 'N/A')
                                row_cells[1].text = item.get('description', 'N/A')
                                row_cells[2].text = str(item.get('quantity', 1))
                                row_cells[3].text = f"${item.get('price', 0):,.2f}"
                                
                            logger.info("Successfully populated line items table.")
                            break # Exit loops once table is found and populated

            document.save(output_path)
            logger.info(f"Word document generated successfully at {output_path}")

        except FileNotFoundError:
            logger.error(f"Template file not found at {self.template_path}")
            raise
        except Exception as e:
            logger.error(f"Error generating Word document: {e}", exc_info=True)
            raise
