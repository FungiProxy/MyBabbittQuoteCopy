from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame,
    QDateEdit, QFormLayout, QSizePolicy, QSpacerItem,
    QDialog, QScrollArea, QGridLayout, QListWidget, QListWidgetItem, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QDate, Signal, QSize
from PySide6.QtGui import QColor, QFont
from src.ui.product_selection_dialog import ProductSelectionDialog
from src.core.services.product_service import ProductService
from src.ui.spare_parts_tab import SparePartsTab
import uuid
from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService
from src.ui.quote_selection_dialog import QuoteSelectionDialog
import logging
from src.core.services.export_service import QuoteExportService

logger = logging.getLogger(__name__)

class PhoneNumberInput(QLineEdit):
    """Custom input field for phone numbers with automatic formatting."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("(xxx) xxx-xxxx")
        self.textChanged.connect(self._format_phone_number)
        self._previous_text = ""
        
    def _format_phone_number(self, text):
        """Format the phone number as the user types."""
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, text))
        
        # Don't process if the text is being deleted
        if len(digits) < len(self._previous_text.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')):
            self._previous_text = text
            return
            
        # Format based on number of digits
        if len(digits) <= 3:
            formatted = digits
        elif len(digits) <= 6:
            formatted = f"({digits[:3]}) {digits[3:]}"
        else:
            # Ensure we only take up to 10 digits
            digits = digits[:10]
            formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            
        # Only update if the formatting would change
        if formatted != text:
            # Store cursor position
            cursor_pos = self.cursorPosition()
            # Calculate how many characters were added before cursor
            added_before_cursor = len([c for c in formatted[:cursor_pos] if c not in text[:cursor_pos]])
            
            # Update text
            self.setText(formatted)
            # Restore cursor position, accounting for added formatting characters
            self.setCursorPosition(cursor_pos + added_before_cursor)
            
        self._previous_text = formatted

class QuoteItemWidget(QWidget):
    """Custom widget for displaying a single item in the quote list."""
    remove_item = Signal(str)
    edit_item = Signal(str)

    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product_id = product.get("id")
        self.product = product
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        part_number = self.product.get("part_number", "N/A")
        qty = self.product.get("quantity", 1)
        
        # Calculate price
        base_price = self.product.get('base_price', 0)
        options_price = sum(op.get('price', 0) for op in self.product.get('options', []))
        total_price = (base_price + options_price) * qty

        item_label = QLabel(f"<b>{part_number}</b> (Qty: {qty})")
        item_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        price_label = QLabel(f"<b>${total_price:,.2f}</b>")
        price_label.setFixedWidth(120)
        price_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setFixedSize(60, 28)
        self.edit_btn.clicked.connect(lambda: self.edit_item.emit(self.product_id))

        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setFixedSize(60, 28)
        self.remove_btn.setStyleSheet("background-color: #f44336; color: white;")
        self.remove_btn.clicked.connect(lambda: self.remove_item.emit(self.product_id))

        layout.addWidget(item_label)
        layout.addStretch()
        layout.addWidget(price_label)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.remove_btn)

class ItemDetailsWidget(QWidget):
    """A widget to display the details (options) of a quote item."""
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 10, 20, 10)
        
        details_label = QLabel("<b>Complete Configuration:</b>")
        self.main_layout.addWidget(details_label)

        for option in self.product.get("options", []):
            if option.get("selected"):
                row_layout = QHBoxLayout()
                row_layout.setSpacing(10)

                name = option.get('name', 'Option')
                value = option.get('selected', 'N/A')
                price_adder = option.get('price', 0)
                
                option_label = QLabel(f"{name}: <b>{value}</b>")
                price_label = QLabel(f"+${price_adder:,.2f}")
                
                row_layout.addWidget(option_label)
                row_layout.addWidget(price_label)
                row_layout.addStretch() # Push widgets to the left

                self.main_layout.addLayout(row_layout)
        
        self.main_layout.addStretch()
        self.setStyleSheet("background-color: #f7f7f7; border-radius: 4px;")

class QuoteCreationPage(QWidget):
    """
    Single-page Quote Creation UI matching the new design.
    Customer info and quote summary at the top, quote items below.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.products = []  # Store added products
        self.expanded_item_row = -1
        self.init_ui()

    def init_ui(self):
        # Main scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        # Header: Title and actions
        header_layout = QHBoxLayout()
        title_label = QLabel("Quote Builder")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.load_quote_btn = QPushButton("Load Quote")
        self.save_quote_btn = QPushButton("Save Quote")
        self.print_btn = QPushButton("Print")
        self.export_btn = QPushButton("Export")
        header_layout.addWidget(self.load_quote_btn)
        header_layout.addWidget(self.save_quote_btn)
        header_layout.addWidget(self.print_btn)
        header_layout.addWidget(self.export_btn)
        self.main_layout.addLayout(header_layout)

        # Top section: Customer Info (left) | Quote Summary (right)
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        # Customer Info Card - More compact
        customer_card = QFrame()
        customer_card.setObjectName("customerCard")
        customer_card.setStyleSheet("""
            QFrame#customerCard { background: white; border-radius: 6px; border: 1px solid #e0e0e0; }
            QLineEdit, QDateEdit { padding: 5px; border: 1px solid #ccc; border-radius: 4px; font-size: 13px; }
            QLineEdit:focus, QDateEdit:focus { border: 1px solid #007AFF; }
        """)
        customer_layout = QVBoxLayout(customer_card)
        customer_layout.setContentsMargins(12, 12, 12, 12)
        customer_layout.setSpacing(8)
        
        customer_title = QLabel("Customer Information")
        customer_title.setStyleSheet("font-size: 15px; font-weight: bold;")
        customer_layout.addWidget(customer_title)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(8)
        form_layout.setLabelAlignment(Qt.AlignLeft)

        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Full Name")
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Company Name")
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.customer_name)
        name_layout.addWidget(self.company_name)
        form_layout.addRow("Customer:", name_layout)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email Address")
        self.phone = PhoneNumberInput()
        contact_layout = QHBoxLayout()
        contact_layout.addWidget(self.email)
        contact_layout.addWidget(self.phone)
        form_layout.addRow("Contact:", contact_layout)

        self.quote_reference = QLineEdit("BQ-2025-6800")
        self.quote_reference.setReadOnly(True)
        self.quote_date = QDateEdit(QDate.currentDate())
        self.quote_date.setCalendarPopup(True)
        self.expiration_date = QDateEdit(QDate.currentDate().addDays(30))
        self.expiration_date.setCalendarPopup(True)
        details_layout = QHBoxLayout()
        details_layout.addWidget(self.quote_date)
        details_layout.addWidget(self.expiration_date)
        form_layout.addRow("Dates:", details_layout)
        form_layout.addRow("Reference:", self.quote_reference)

        customer_layout.addLayout(form_layout)
        top_layout.addWidget(customer_card, 3)

        # Quote Summary Card - More compact
        summary_card = QFrame()
        summary_card.setObjectName("summaryCard")
        summary_card.setStyleSheet("QFrame#summaryCard { background: white; border-radius: 6px; border: 1px solid #e0e0e0; }")
        summary_layout = QVBoxLayout(summary_card)
        summary_layout.setContentsMargins(12, 12, 12, 12)
        summary_layout.setSpacing(8)

        summary_title = QLabel("Quote Summary")
        summary_title.setStyleSheet("font-size: 15px; font-weight: bold;")
        summary_layout.addWidget(summary_title)
        
        self.summary_grid = QGridLayout()
        self.summary_grid.setSpacing(6)
        
        style = "font-size: 13px;"
        self.items_label = QLabel("Items:")
        self.items_label.setStyleSheet(style)
        self.items_value = QLabel("0")
        self.items_value.setStyleSheet(style)
        self.subtotal_label = QLabel("Subtotal:")
        self.subtotal_label.setStyleSheet(style)
        self.subtotal_value = QLabel("$0.00")
        self.subtotal_value.setStyleSheet(style)
        self.total_label = QLabel("Total:")
        self.total_label.setStyleSheet(f"{style} font-weight: bold;")
        self.total_value = QLabel("$0.00")
        self.total_value.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.summary_grid.addWidget(self.items_label, 0, 0)
        self.summary_grid.addWidget(self.items_value, 0, 1, Qt.AlignRight)
        self.summary_grid.addWidget(self.subtotal_label, 1, 0)
        self.summary_grid.addWidget(self.subtotal_value, 1, 1, Qt.AlignRight)
        self.summary_grid.addWidget(self.total_label, 2, 0)
        self.summary_grid.addWidget(self.total_value, 2, 1, Qt.AlignRight)

        summary_layout.addLayout(self.summary_grid)
        summary_layout.addStretch()
        top_layout.addWidget(summary_card, 2)
        self.main_layout.addLayout(top_layout)
        
        # Quote Items Section
        items_card = QFrame()
        items_card.setObjectName("itemsCard")
        items_card.setStyleSheet("""
            QFrame#itemsCard { background: white; border-radius: 6px; border: 1px solid #e0e0e0; }
            QListWidget { border: none; font-size: 13px; }
        """)
        items_layout = QVBoxLayout(items_card)
        items_layout.setContentsMargins(12, 12, 12, 12)
        items_layout.setSpacing(10)

        items_header = QHBoxLayout()
        items_title = QLabel("Quote Items")
        items_title.setStyleSheet("font-size: 15px; font-weight: bold;")
        items_header.addWidget(items_title)
        items_header.addStretch()
        self.add_spare_parts_btn = QPushButton("Add Spare Part")
        self.add_product_btn = QPushButton("Add Item")
        items_header.addWidget(self.add_spare_parts_btn)
        items_header.addWidget(self.add_product_btn)
        items_layout.addLayout(items_header)

        self.items_list = QListWidget()
        self.items_list.setStyleSheet("QListWidget::item { border-bottom: 1px solid #eee; }")
        self.items_list.setMinimumHeight(300)
        self.items_list.itemClicked.connect(self._on_item_clicked)
        items_layout.addWidget(self.items_list)
        
        self.main_layout.addWidget(items_card, 1)

        # Footer
        footer_layout = QHBoxLayout()
        footer_left = QLabel("Babbitt International Inc.")
        footer_right = QLabel("© 2025 All rights reserved")
        footer_layout.addWidget(footer_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_right)
        self.main_layout.addLayout(footer_layout)

        scroll_area.setWidget(container)
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll_area)
        
        self.add_product_btn.clicked.connect(self.open_product_dialog)
        self.add_spare_parts_btn.clicked.connect(self.open_spare_parts_dialog)
        self.save_quote_btn.clicked.connect(self.save_quote)
        self.load_quote_btn.clicked.connect(self.open_load_quote_dialog)
        self.print_btn.clicked.connect(self.print_quote)
        self.export_btn.clicked.connect(self.export_quote)
        
        self.update_items_list()

    def open_load_quote_dialog(self):
        dialog = QuoteSelectionDialog(self)
        if dialog.exec():
            quote_id = dialog.selected_quote_id
            if quote_id:
                self.load_quote(quote_id)

    def load_quote(self, quote_id):
        db = SessionLocal()
        try:
            quote_data = QuoteService.get_full_quote_details(db, quote_id)
            if not quote_data:
                QMessageBox.warning(self, "Error", "Could not find quote details.")
                return

            # Populate customer info
            customer = quote_data.get("customer", {})
            self.customer_name.setText(customer.get("name"))
            self.company_name.setText(customer.get("company"))
            self.email.setText(customer.get("email"))
            self.phone.setText(customer.get("phone"))

            # Populate products
            self.products = quote_data.get("products", [])
            self.update_items_list()
            self.update_summary()

            # Populate other quote details
            self.quote_reference.setText(quote_data.get("quote_number"))
            self.quote_date.setDate(QDate.fromString(quote_data.get("date_created").isoformat(), Qt.ISODate))
            if quote_data.get("expiration_date"):
                self.expiration_date.setDate(QDate.fromString(quote_data.get("expiration_date").isoformat(), Qt.ISODate))
            
            QMessageBox.information(self, "Quote Loaded", f"Quote {quote_data.get('quote_number')} loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading quote: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"An error occurred while loading the quote: {e}")
        finally:
            db.close()

    def save_quote(self):
        """
        Gather all data from the UI and save the quote to the database.
        """
        customer_data = {
            "name": self.customer_name.text(),
            "company": self.company_name.text(),
            "email": self.email.text(),
            "phone": self.phone.text(),
        }

        if not customer_data["name"] or not customer_data["email"]:
            QMessageBox.warning(self, "Missing Information", "Customer name and email are required.")
            return

        if not self.products:
            QMessageBox.warning(self, "No Items", "Cannot save a quote with no items.")
            return

        quote_details = { "notes": "" }

        db = SessionLocal()
        try:
            quote = QuoteService.create_quote_with_items(
                db=db,
                customer_data=customer_data,
                products_data=self.products,
                quote_details=quote_details
            )
            QMessageBox.information(self, "Quote Saved", f"Quote {quote.quote_number} has been saved successfully.")
            # Clear form after saving
            self.products = []
            self.customer_name.clear()
            self.company_name.clear()
            self.email.clear()
            self.phone.clear()
            self.update_items_list()
            self.update_summary()
        except Exception as e:
            logger.error(f"Failed to save quote: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to save quote: {e}")
        finally:
            db.close()

    def open_product_dialog(self):
        dialog = ProductSelectionDialog(product_service=ProductService(), parent=self)
        if dialog.exec():
            product = dialog.selected_product
            if product:
                product['id'] = str(uuid.uuid4()) # Assign a unique ID
                self.products.append(product)
                self.update_items_list()
                self.update_summary()

    def open_spare_parts_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Spare Parts")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(dialog)
        spare_parts_tab = SparePartsTab(parent=dialog)
        layout.addWidget(spare_parts_tab)
        
        # Connect the part_selected signal
        spare_parts_tab.part_selected.connect(self.add_spare_part_to_quote)
        spare_parts_tab.part_selected.connect(dialog.accept)  # Close dialog when part is selected
        
        dialog.exec()

    def add_spare_part_to_quote(self, part_info):
        """Add a spare part to the quote."""
        part_info['id'] = str(uuid.uuid4()) # Assign a unique ID
        self.products.append(part_info)
        self.update_items_list()
        self.update_summary()

    def update_items_list(self):
        """Populate the list of quote items with custom widgets."""
        self.items_list.clear()
        self.expanded_item_row = -1
        
        if not self.products:
            placeholder_item = QListWidgetItem("No items have been added to the quote yet.")
            placeholder_item.setTextAlignment(Qt.AlignCenter)
            
            font = placeholder_item.font()
            font.setItalic(True)
            placeholder_item.setFont(font)
            
            flags = placeholder_item.flags()
            flags &= ~Qt.ItemIsSelectable
            flags &= ~Qt.ItemIsEnabled
            placeholder_item.setFlags(flags)
            
            placeholder_item.setForeground(QColor("gray"))

            self.items_list.addItem(placeholder_item)
            return

        for product in self.products:
            item_widget = QuoteItemWidget(product)
            item_widget.remove_item.connect(self._remove_product)
            item_widget.edit_item.connect(self._edit_product)
            
            list_item = QListWidgetItem(self.items_list)
            list_item.setSizeHint(item_widget.sizeHint())
            # Store product_id in the item itself for easy access
            list_item.setData(Qt.UserRole, product['id'])
            
            self.items_list.addItem(list_item)
            self.items_list.setItemWidget(list_item, item_widget)


    def _remove_product(self, product_id):
        """Remove a product from the quote."""
        if self.expanded_item_row != -1:
            self.items_list.takeItem(self.expanded_item_row + 1)
            self.expanded_item_row = -1

        self.products = [p for p in self.products if p.get('id') != product_id]
        self.update_items_list()
        self.update_summary()

    def _edit_product(self, product_id):
        """Opens the product selection dialog to edit an existing item."""
        if self.expanded_item_row != -1:
            self.items_list.takeItem(self.expanded_item_row + 1)
            self.expanded_item_row = -1
            
        product_to_edit = next((p for p in self.products if p.get('id') == product_id), None)
        if not product_to_edit:
            return

        dialog = ProductSelectionDialog(
            product_service=ProductService(), 
            parent=self, 
            product_to_edit=product_to_edit
        )

        if dialog.exec():
            updated_product = dialog.get_selected_product_data()
            if updated_product:
                # Find the index of the old product and replace it
                for i, p in enumerate(self.products):
                    if p.get('id') == product_id:
                        self.products[i] = updated_product
                        break
                self.update_items_list()
                self.update_summary()


    def _on_item_clicked(self, item):
        """Show or hide details for the clicked quote item."""
        if not item.data(Qt.UserRole): # Clicked on details or placeholder
            return

        selected_row = self.items_list.row(item)

        # If a details widget is already open, remove it
        if self.expanded_item_row != -1:
            self.items_list.takeItem(self.expanded_item_row + 1)
            # If the user re-clicked the same item, just collapse it
            if selected_row == self.expanded_item_row:
                self.expanded_item_row = -1
                return
            # Adjust selected_row if the removed item was above the current selection
            if self.expanded_item_row < selected_row:
                selected_row -= 1

        product_id = item.data(Qt.UserRole)
        product = next((p for p in self.products if p.get('id') == product_id), None)

        # Don't show details if product has no options with selections
        if not product or not any(o.get('selected') for o in product.get("options", [])):
            self.expanded_item_row = -1
            return
            
        # Create and insert the details widget
        details_widget = ItemDetailsWidget(product)
        details_item = QListWidgetItem()
        details_item.setSizeHint(details_widget.sizeHint())
        details_item.setFlags(details_item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
        
        self.items_list.insertItem(selected_row + 1, details_item)
        self.items_list.setItemWidget(details_item, details_widget)
        
        self.expanded_item_row = selected_row


    def update_summary(self):
        """Update the quote summary details."""
        items_count = len(self.products)
        subtotal = 0.0
        for product in self.products:
            base_price = product.get('base_price', 0)
            options_price = sum(op.get('price', 0) for op in product.get('options', []) if op.get('price'))
            qty = product.get('quantity', 1)
            price = (base_price + options_price) * qty
            subtotal += price
        
        total = subtotal

        self.items_value.setText(str(items_count))
        self.subtotal_value.setText(f"${subtotal:,.2f}")
        self.total_value.setText(f"${total:,.2f}")

    def print_quote(self):
        # Implementation of print_quote method
        pass

    def export_quote(self):
        """Handles the export of the current quote to a Word document."""
        try:
            # Get the current quote details
            quote_details = self.get_current_quote_details()
            if not quote_details:
                QMessageBox.warning(self, "No Quote", "Please create or load a quote first.")
                return

            customer_name = quote_details['customer']['name'].replace(" ", "_")
            quote_number = quote_details['quote']['quote_number']
            default_filename = f"Quote_{quote_number}_{customer_name}.docx"

            # For now, we assume a template exists at this path.
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

    def get_current_quote_details(self):
        """Get the current quote details for export."""
        try:
            # Get customer info
            customer_info = {
                'name': self.customer_name.text(),
                'company': self.company_name.text(),
                'email': self.email.text(),
                'phone': self.phone.text()
            }

            # Get quote info
            quote_info = {
                'quote_number': self.quote_reference.text(),
                'date': self.quote_date.date().toString("yyyy-MM-dd"),
                'expiration_date': self.expiration_date.date().toString("yyyy-MM-dd")
            }

            # Get line items
            line_items = []
            for i in range(self.items_list.count()):
                item = self.items_list.itemWidget(self.items_list.item(i))
                if isinstance(item, QuoteItemWidget):
                    line_items.append({
                        'part_number': item.product.get('part_number', 'N/A'),
                        'description': item.product.get('description', 'N/A'),
                        'quantity': item.product.get('quantity', 1),
                        'price': item.product.get('base_price', 0) + sum(op.get('price', 0) for op in item.product.get('options', []))
                    })

            return {
                'customer': customer_info,
                'quote': quote_info,
                'line_items': line_items
            }
        except Exception as e:
            logger.error(f"Error getting quote details: {e}", exc_info=True)
            return None