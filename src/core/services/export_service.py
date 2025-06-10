"""
Service for exporting quote data to different file formats.
"""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import logging
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch

logger = logging.getLogger(__name__)

class QuotePDFGenerator:
    """
    Handles the logic for creating a professional-looking PDF quote.
    """
    def __init__(self, company_info, terms_and_conditions):
        self.company_info = company_info
        self.terms_and_conditions = terms_and_conditions
        self.styles = self._setup_styles()

    def _setup_styles(self):
        """Initializes styles for the PDF document."""
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Header', fontSize=18, alignment=TA_CENTER, spaceBottom=20))
        styles.add(ParagraphStyle(name='SubHeader', fontSize=12, alignment=TA_LEFT, spaceBottom=10))
        styles.add(ParagraphStyle(name='Body', fontSize=10, alignment=TA_LEFT, leading=14))
        styles.add(ParagraphStyle(name='RightAlign', fontSize=10, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Footer', fontSize=8, alignment=TA_CENTER, textColor=colors.grey))
        return styles

    def generate_pdf_quote(self, quote_details, output_path):
        """Generates the complete PDF quote and saves it to a file."""
        try:
            doc = SimpleDocTemplate(output_path,
                                    rightMargin=inch/2, leftMargin=inch/2,
                                    topMargin=inch/2, bottomMargin=inch/2)

            story = []

            self._add_header(story, quote_details)
            self._add_customer_info(story, quote_details)
            self._add_line_items_table(story, quote_details)
            self._add_summary(story, quote_details)
            self._add_footer(story)

            doc.build(story)
            logger.info(f"PDF quote generated successfully at {output_path}")

        except Exception as e:
            logger.error(f"Error generating PDF quote: {e}", exc_info=True)
            raise

    def _add_header(self, story, quote_details):
        """Adds the header section with company and quote details."""
        story.append(Paragraph("Quote", self.styles['Header']))
        
        header_data = [
            [Paragraph(self.company_info['name'], self.styles['Body']), Paragraph(f"<b>Quote #:</b> {quote_details.get('quote_number', 'N/A')}", self.styles['RightAlign'])],
            [Paragraph(self.company_info['address'], self.styles['Body']), Paragraph(f"<b>Date:</b> {quote_details.get('date_created', 'N/A')}", self.styles['RightAlign'])],
            [Paragraph(self.company_info['contact'], self.styles['Body']), '']
        ]
        
        table = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('SPAN', (0, 2), (0, 2)), # Span company contact info
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.25*inch))

    def _add_customer_info(self, story, quote_details):
        """Adds the customer information section."""
        customer = quote_details.get('customer', {})
        story.append(Paragraph("<b>Bill To:</b>", self.styles['SubHeader']))
        
        customer_details = f"""
        {customer.get('name', 'N/A')}<br/>
        {customer.get('address', 'N/A')}
        """
        story.append(Paragraph(customer_details, self.styles['Body']))
        story.append(Spacer(1, 0.25*inch))

    def _add_line_items_table(self, story, quote_details):
        """Creates and adds the line items table."""
        table_data = [
            ["Part Number", "Description", "Qty", "Unit Price", "Total Price"]
        ]
        
        for item in quote_details.get('line_items', []):
            quantity = item.get('quantity', 1)
            unit_price = item.get('price', 0)
            total_price = quantity * unit_price
            
            table_data.append([
                item.get('part_number', 'N/A'),
                Paragraph(item.get('description', 'N/A'), self.styles['Body']),
                str(quantity),
                f"${unit_price:,.2f}",
                f"${total_price:,.2f}"
            ])

        table = Table(table_data, colWidths=[1*inch, 3.5*inch, 0.5*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.25*inch))
        
    def _add_summary(self, story, quote_details):
        """Adds the quote summary (subtotal, tax, total)."""
        subtotal = quote_details.get('total_price', 0)
        # Assuming tax is not included yet. Add tax calculation if needed.
        tax = 0.0 
        total = subtotal + tax
        
        summary_data = [
            ["Subtotal:", f"${subtotal:,.2f}"],
            ["Tax (0%):", f"${tax:,.2f}"],
            ["<b>Total:</b>", f"<b>${total:,.2f}</b>"],
        ]

        summary_table = Table(summary_data, colWidths=[1*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.white), # No visible grid
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ]))

        # Wrap summary table in another table to align it to the right
        align_table = Table([[summary_table]], colWidths=[7*inch])
        align_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'RIGHT')]))

        story.append(align_table)
        story.append(Spacer(1, 0.25*inch))
        
    def _add_footer(self, story):
        """Adds the terms and conditions footer."""
        story.append(Paragraph("Terms and Conditions", self.styles['SubHeader']))
        story.append(Paragraph(self.terms_and_conditions.replace('\n', '<br/>'), self.styles['Body']))


class QuoteExportService:
    """
    Handles the logic for exporting a quote to a Word or PDF document.
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

    def generate_pdf_document(self, quote_details, output_path):
        """
        Generates a .pdf file from quote data.
        """
        # These would typically come from a config file or database
        company_info = {
            "name": "Your Company Name",
            "address": "123 Main Street, Anytown, USA 12345",
            "contact": "Email: contact@yourcompany.com | Phone: (123) 456-7890"
        }
        terms_and_conditions = "1. All invoices are due upon receipt.\n2. Please make all checks payable to Your Company Name.\n3. Prices are valid for 30 days."

        try:
            pdf_generator = QuotePDFGenerator(company_info, terms_and_conditions)
            pdf_generator.generate_pdf_quote(quote_details, output_path)
            logger.info(f"PDF generation initiated for {output_path}")
        except Exception as e:
            logger.error(f"Failed to initiate PDF generation: {e}", exc_info=True)
            raise
