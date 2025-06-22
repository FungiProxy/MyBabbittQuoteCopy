"""
Export functionality integration for the quote creation page.
Add this to your quote_creation_redesign.py
"""

import os
from datetime import datetime
from PySide6.QtWidgets import QFileDialog, QMessageBox
from src.core.services.export_service import QuoteExportService, QuotePDFGenerator
import logging

logger = logging.getLogger(__name__)


class ExportMixin:
    """Mixin class to add export functionality to QuoteCreationPage."""
    
    def _init_export_actions(self):
        """Initialize export action connections."""
        # Connect export buttons from the actions panel
        if hasattr(self, 'generate_pdf_btn'):
            self.generate_pdf_btn.clicked.connect(self._export_to_pdf)
        if hasattr(self, 'generate_word_btn'):
            self.generate_word_btn.clicked.connect(self._export_to_word)
        if hasattr(self, 'save_draft_btn'):
            self.save_draft_btn.clicked.connect(self._save_draft)
        if hasattr(self, 'send_quote_btn'):
            self.send_quote_btn.clicked.connect(self._send_quote)
    
    def _prepare_quote_data(self):
        """Prepare quote data for export."""
        # Get customer info
        customer_data = {
            'name': self.company_name_edit.text() or 'N/A',
            'contact_person': self.contact_person_edit.text() or 'N/A',
            'email': self.email_edit.text() or 'N/A',
            'phone': self.phone_edit.text() or 'N/A',
            'address': '',  # Add if you have address fields
            'notes': self.notes_edit.toPlainText() or ''
        }
        
        # Get quote items
        items = []
        total_price = 0.0
        
        for i in range(self.items_table.rowCount()):
            # Skip empty rows
            product_item = self.items_table.item(i, 0)
            if not product_item:
                continue
                
            product = product_item.text()
            config_item = self.items_table.item(i, 1)
            qty_item = self.items_table.item(i, 2)
            price_item = self.items_table.item(i, 3)
            total_item = self.items_table.item(i, 4)
            
            configuration = config_item.text() if config_item else ''
            quantity = int(qty_item.text()) if qty_item and qty_item.text().isdigit() else 1
            unit_price = float(price_item.text().replace('$', '').replace(',', '')) if price_item else 0.0
            line_total = float(total_item.text().replace('$', '').replace(',', '')) if total_item else 0.0
            
            items.append({
                'product': product,
                'configuration': configuration,
                'quantity': quantity,
                'unit_price': unit_price,
                'total': line_total
            })
            
            total_price += line_total
        
        # Get application notes for the products
        application_notes = self._get_application_notes(items)
        
        # Prepare complete quote data
        quote_data = {
            'quote_number': self._generate_quote_number(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'customer': customer_data,
            'customer_name': customer_data['name'],
            'contact_person': customer_data['contact_person'],
            'subject': f"{items[0]['product']} Level Transmitter" if items else "Quote",
            'items': items,
            'total_price': total_price,
            'application_notes': application_notes,
            'sales_person_name': 'John Nichelosi',  # Get from settings/user profile
            'sales_person_phone': '(713) 467-4438',
            'sales_person_email': 'John@babbitt.us',
            'company_info': {
                'name': 'Babbitt International',
                'address': 'Houston, TX',
                'contact': 'Email: sales@babbittinternational.com | Phone: (713) 467-4438',
            },
            'terms_and_conditions': (
                '1. All prices are in USD.\n'
                '2. Terms: Net 30 days W.A.C. or CC\n'
                '3. Prices are valid for 30 days.\n'
                '4. Delivery: FCA Factory, Houston, TX'
            )
        }
        
        return quote_data
    
    def _get_application_notes(self, items):
        """Get application notes based on products."""
        # Default LT9000 application notes from the price list
        lt9000_notes = """THE LT 9000 IS DESIGNED TO BE USED IN ELECTRICALLY CONDUCTIVE LIQUIDS THAT DO NOT LEAVE A RESIDUE ON THE PROBE. A wet electrically conductive coating will give an indication of level at the highest point that there is a continuous coating from the surface of the fluid.

For proper operation, the LT 9000 must be grounded to the fluid. In non-metallic tanks, extra grounding provisions may be necessary. It is good engineering practice to provide a separate independent high-level alarm in critical applications, rather than using a set point based on the 4-20mA output."""
        
        # Check if any LT9000 products in the quote
        for item in items:
            if 'LT9000' in item['product']:
                return lt9000_notes
        
        # Default notes for other products
        return "Please refer to product manual for detailed application notes and installation instructions."
    
    def _generate_quote_number(self):
        """Generate a unique quote number."""
        # Format: Q-YYYY-MMDD-XXX
        date_str = datetime.now().strftime('%Y-%m%d')
        # In production, get the last number from database
        sequence = 1  
        return f"Q-{date_str}-{sequence:03d}"
    
    def _export_to_pdf(self):
        """Export quote to PDF."""
        try:
            quote_data = self._prepare_quote_data()
            
            if not quote_data['items']:
                QMessageBox.warning(self, "Warning", "No items in quote to export!")
                return
            
            # Get save location
            default_filename = f"Quote_{quote_data['quote_number']}_{quote_data['customer_name'].replace(' ', '_')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Quote as PDF",
                default_filename,
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
            
            # Generate PDF
            pdf_generator = QuotePDFGenerator(
                quote_data['company_info'],
                quote_data['terms_and_conditions']
            )
            pdf_generator.generate_pdf_quote(quote_data, file_path)
            
            QMessageBox.information(self, "Success", f"Quote exported to:\n{file_path}")
            
        except Exception as e:
            logger.error(f"Error exporting to PDF: {e}")
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF: {str(e)}")
    
    def _export_to_word(self):
        """Export quote to Word document."""
        try:
            quote_data = self._prepare_quote_data()
            
            if not quote_data['items']:
                QMessageBox.warning(self, "Warning", "No items in quote to export!")
                return
            
            # Get save location
            default_filename = f"Quote_{quote_data['quote_number']}_{quote_data['customer_name'].replace(' ', '_')}.docx"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Quote as Word Document",
                default_filename,
                "Word Documents (*.docx)"
            )
            
            if not file_path:
                return
            
            # Check if template exists
            template_path = "data/templates/quote_template.docx"
            if not os.path.exists(template_path):
                # Create template if it doesn't exist
                from scripts.word_template_generator import create_quote_template
                create_quote_template()
            
            # Generate Word document
            exporter = QuoteExportService(template_path)
            exporter.generate_word_document(quote_data, file_path)
            
            QMessageBox.information(self, "Success", f"Quote exported to:\n{file_path}")
            
        except Exception as e:
            logger.error(f"Error exporting to Word: {e}")
            QMessageBox.critical(self, "Export Error", f"Failed to export Word document: {str(e)}")
    
    def _save_draft(self):
        """Save quote as draft."""
        try:
            # In production, save to database
            quote_data = self._prepare_quote_data()
            quote_data['status'] = 'DRAFT'
            
            # For now, just show success message
            QMessageBox.information(
                self, 
                "Draft Saved", 
                f"Quote {quote_data['quote_number']} saved as draft!"
            )
            
        except Exception as e:
            logger.error(f"Error saving draft: {e}")
            QMessageBox.critical(self, "Save Error", f"Failed to save draft: {str(e)}")
    
    def _send_quote(self):
        """Send quote via email."""
        try:
            quote_data = self._prepare_quote_data()
            
            if not quote_data['customer']['email']:
                QMessageBox.warning(
                    self, 
                    "Missing Email", 
                    "Customer email is required to send quote!"
                )
                return
            
            # In production, implement email sending
            # For now, export to PDF and show message
            temp_path = f"temp_quote_{quote_data['quote_number']}.pdf"
            pdf_generator = QuotePDFGenerator(
                quote_data['company_info'],
                quote_data['terms_and_conditions']
            )
            pdf_generator.generate_pdf_quote(quote_data, temp_path)
            
            QMessageBox.information(
                self,
                "Quote Ready",
                f"Quote is ready to send to:\n{quote_data['customer']['email']}\n\n"
                f"PDF saved to: {temp_path}"
            )
            
        except Exception as e:
            logger.error(f"Error sending quote: {e}")
            QMessageBox.critical(self, "Send Error", f"Failed to send quote: {str(e)}")


# Add to QuoteCreationPage class in quote_creation_redesign.py:
# 
# class QuoteCreationPage(QWidget, ExportMixin):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.init_ui()
#         self._init_export_actions()  # Add this line
