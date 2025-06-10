"""
Dialog for selecting an existing quote to load.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QFrame, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal
from src.core.services.quote_service import QuoteService
from src.core.services.export_service import QuoteExportService
from src.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

class QuoteSelectionDialog(QDialog):
    """
    A dialog that lists existing quotes and allows the user to select one.
    """
    quote_deleted = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load Quote")
        self.setMinimumSize(600, 400)
        self.selected_quote_id = None
        self.init_ui()
        self.populate_quotes()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.quote_list = QListWidget()
        self.quote_list.itemDoubleClicked.connect(self.accept)
        main_layout.addWidget(self.quote_list)

        button_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_quote)
        self.delete_btn.setEnabled(False) # Disabled by default
        
        button_layout.addStretch()
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(button_layout)
        
        self.quote_list.itemSelectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        """Enable/disable delete button based on selection."""
        self.delete_btn.setEnabled(len(self.quote_list.selectedItems()) > 0)

    def populate_quotes(self):
        self.quote_list.clear()
        db = SessionLocal()
        try:
            # This method will be re-added in the next step
            quotes = QuoteService.get_all_quotes_summary(db)
            if not quotes:
                self.quote_list.addItem("No quotes found.")
                return

            for quote in quotes:
                item_text = f"Quote {quote['quote_number']} - {quote['customer_name']} - ${quote['total']:,.2f} ({quote['date_created']})"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, quote['id'])
                self.quote_list.addItem(item)
        except Exception as e:
            logger.error(f"Error populating quotes: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", "Could not load quotes from the database.")
        finally:
            db.close()

    def delete_quote(self):
        selected_items = self.quote_list.selectedItems()
        if not selected_items:
            return

        quote_id = selected_items[0].data(Qt.UserRole)
        item_text = selected_items[0].text()

        reply = QMessageBox.question(
            self,
            "Delete Quote",
            f"Are you sure you want to delete this quote?\n\n{item_text}\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            db = SessionLocal()
            try:
                success = QuoteService.delete_quote(db, quote_id)
                if success:
                    QMessageBox.information(self, "Success", "Quote deleted successfully.")
                    self.quote_deleted.emit()
                    # Refresh the list
                    self.populate_quotes()
                else:
                    QMessageBox.warning(self, "Error", "Could not find the quote to delete.")
            except Exception as e:
                logger.error(f"Error deleting quote: {e}", exc_info=True)
                QMessageBox.critical(self, "Error", f"An error occurred while deleting the quote: {e}")
            finally:
                db.close()

    def export_quote(self):
        selected_items = self.quote_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a quote to export.")
            return

        quote_id = selected_items[0].data(Qt.UserRole)
        db = SessionLocal()
        try:
            quote_details = QuoteService.get_quote_details(db, quote_id)
            if not quote_details:
                QMessageBox.critical(self, "Error", "Could not find quote details.")
                return

            customer_name = quote_details['customer']['name'].replace(" ", "_")
            quote_number = quote_details['quote_number']
            default_filename = f"Quote_{quote_number}_{customer_name}.docx"

            # For now, we assume a template exists at this path.
            # We will create this template next.
            template_path = "data/templates/quote_template.docx"

            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Quote", default_filename, "Word Documents (*.docx)"
            )

            if save_path:
                exporter = QuoteExportService(template_path)
                exporter.generate_word_document(quote_details, save_path)
                QMessageBox.information(self, "Success", f"Quote successfully exported to {save_path}")

        except Exception as e:
            logger.error(f"Error exporting quote: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Could not export quote: {e}")
        finally:
            db.close()

    def accept(self):
        selected_items = self.quote_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a quote to load.")
            return
        self.selected_quote_id = selected_items[0].data(Qt.UserRole)
        super().accept() 