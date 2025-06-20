import logging
import uuid

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QDateEdit,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.quote_service import QuoteService
from src.ui.product_selection_dialog import ProductSelectionDialog
from src.ui.views.quote_selection_dialog import QuoteSelectionDialog

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
        digits = "".join(filter(str.isdigit, text))

        # Don't process if the text is being deleted
        if len(digits) < len(
            self._previous_text.replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "")
        ):
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
            added_before_cursor = len(
                [c for c in formatted[:cursor_pos] if c not in text[:cursor_pos]]
            )

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
        # Use a unique instance ID for each product
        self.instance_id = product.get("instance_id", str(uuid.uuid4()))
        self.product = product
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Get product details with safe defaults
        part_number = self.product.get("part_number", "N/A")
        qty = self.product.get("quantity", 1)

        # Calculate price with safe defaults
        base_price = self.product.get("base_price", 0)
        options = self.product.get("options", [])
        options_price = sum(
            float(op.get("price", 0)) for op in options if isinstance(op, dict)
        )
        total_price = (base_price + options_price) * qty

        # Create labels with proper formatting
        item_label = QLabel(f"<b>{part_number}</b> (Qty: {qty})")
        item_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        price_label = QLabel(f"<b>${total_price:,.2f}</b>")
        price_label.setFixedWidth(120)
        price_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Create buttons
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setFixedSize(60, 28)
        self.edit_btn.clicked.connect(lambda: self.edit_item.emit(self.instance_id))

        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setFixedSize(60, 28)
        self.remove_btn.setStyleSheet("background-color: #f44336; color: white;")
        self.remove_btn.clicked.connect(lambda: self.remove_item.emit(self.instance_id))

        # Add widgets to layout
        layout.addWidget(item_label)
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

                name = option.get("name", "Option")
                value = option.get("selected", "N/A")
                price_adder = option.get("price", 0)

                option_label = QLabel(f"{name}: <b>{value}</b>")
                price_label = QLabel(f"+${price_adder:,.2f}")

                row_layout.addWidget(option_label)
                row_layout.addWidget(price_label)
                row_layout.addStretch()  # Push widgets to the left

                self.main_layout.addLayout(row_layout)

        self.main_layout.addStretch()


class QuoteCreationPage(QWidget):
    """
    Single-page Quote Creation UI matching the new design.
    Customer info and quote summary at the top, quote items below.
    """

    quote_loaded = Signal(int)
    quote_deleted = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.products = []
        self.expanded_item_row = -1
        self.current_quote_id = None

        # Initialize services
        self.db = SessionLocal()
        self.product_service = ProductService()
        self.quote_service = QuoteService()

        self.init_ui()

    def __del__(self):
        if self.db:
            self.db.close()

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

        # Customer Info Card
        customer_card = QFrame()
        customer_card.setObjectName("customerCard")
        customer_layout = QVBoxLayout(customer_card)
        customer_layout.setContentsMargins(12, 12, 12, 12)
        customer_layout.setSpacing(8)

        customer_title = QLabel("Customer Information")
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

        self.quote_reference = QLineEdit()
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

        # Quote Summary Card
        summary_card = QFrame()
        summary_card.setObjectName("summaryCard")
        summary_layout = QVBoxLayout(summary_card)
        summary_layout.setContentsMargins(12, 12, 12, 12)
        summary_layout.setSpacing(8)

        summary_title = QLabel("Quote Summary")
        summary_layout.addWidget(summary_title)

        self.summary_grid = QGridLayout()
        self.summary_grid.setSpacing(6)

        style = "font-size: 13px;"
        self.items_label = QLabel("Items:")
        self.items_label.setStyleSheet(style)
        self.items_total_label = QLabel("Subtotal:")
        self.items_total_label.setStyleSheet(style)
        self.total_label = QLabel("Total:")
        self.total_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.items_count = QLabel("0")
        self.items_count.setAlignment(Qt.AlignRight)
        self.items_count.setStyleSheet(style)
        self.items_total_value = QLabel("$0.00")
        self.items_total_value.setAlignment(Qt.AlignRight)
        self.items_total_value.setStyleSheet(style)
        self.total_value = QLabel("$0.00")
        self.total_value.setAlignment(Qt.AlignRight)
        self.total_value.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.summary_grid.addWidget(self.items_label, 0, 0)
        self.summary_grid.addWidget(self.items_count, 0, 1)
        self.summary_grid.addWidget(self.items_total_label, 1, 0)
        self.summary_grid.addWidget(self.items_total_value, 1, 1)
        self.summary_grid.addWidget(self.total_label, 2, 0)
        self.summary_grid.addWidget(self.total_value, 2, 1)

        summary_layout.addLayout(self.summary_grid)
        top_layout.addWidget(summary_card, 2)
        self.main_layout.addLayout(top_layout)

        # Items section
        items_header_layout = QHBoxLayout()
        items_label = QLabel("Quote Items")
        items_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        items_header_layout.addWidget(items_label)
        items_header_layout.addStretch()
        self.add_product_btn = QPushButton("+ Add Product")
        self.add_spare_parts_btn = QPushButton("+ Add Spare Parts")
        items_header_layout.addWidget(self.add_product_btn)
        items_header_layout.addWidget(self.add_spare_parts_btn)
        self.main_layout.addLayout(items_header_layout)

        self.items_list_widget = QListWidget()
        self.items_list_widget.setSpacing(5)
        self.items_list_widget.itemClicked.connect(self._on_item_clicked)
        self.main_layout.addWidget(self.items_list_widget)

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Add notes for the quote...")
        self.main_layout.addWidget(self.notes_input)

        # Connect signals
        self.add_product_btn.clicked.connect(self.open_product_dialog)
        self.add_spare_parts_btn.clicked.connect(self.open_spare_parts_dialog)
        self.save_quote_btn.clicked.connect(self.save_quote)
        self.load_quote_btn.clicked.connect(self.load_quote)
        self.print_btn.clicked.connect(self.print_quote)
        self.export_btn.clicked.connect(self.export_quote)

        self.update_items_list()
        self.update_summary()

        scroll_area.setWidget(container)

        # Set main layout for the page
        page_layout = QVBoxLayout(self)
        page_layout.addWidget(scroll_area)
        page_layout.setContentsMargins(0, 0, 0, 0)

    def load_quote(self):
        """Opens a dialog to select and load an existing quote."""
        dialog = QuoteSelectionDialog(self)
        dialog.quote_deleted.connect(self.quote_deleted.emit)
        if dialog.exec():
            quote_id = dialog.selected_quote_id
            if quote_id:
                self.load_quote_data(quote_id)

    def load_quote_data(self, quote_id):
        """Fetches quote data and updates the UI."""
        self.current_quote_id = quote_id
        try:
            quote_data = QuoteService.get_full_quote_details(
                self.db, self.current_quote_id
            )
            if quote_data:
                self.update_ui_with_quote_data(quote_data)
                QMessageBox.information(
                    self,
                    "Quote Loaded",
                    f"Quote {quote_data.get('quote_number')} loaded successfully.",
                )
                self.quote_loaded.emit(self.current_quote_id)
            else:
                QMessageBox.warning(
                    self, "Load Error", "Could not retrieve quote details."
                )
        except Exception as e:
            logger.error(f"Error loading quote details: {e}", exc_info=True)
            QMessageBox.critical(
                self, "Error", "An error occurred while loading the quote."
            )

    def update_ui_with_quote_data(self, quote_data):
        """Populates the UI fields with data from a loaded quote."""
        customer_info = quote_data.get("customer", {})
        self.customer_name.setText(customer_info.get("name", ""))
        self.company_name.setText(customer_info.get("company", ""))
        self.email.setText(customer_info.get("email", ""))
        self.phone.setText(customer_info.get("phone", ""))

        self.quote_reference.setText(quote_data.get("quote_number", ""))

        created_date = quote_data.get("date_created")
        if created_date:
            self.quote_date.setDate(
                QDate(created_date.year, created_date.month, created_date.day)
            )

        expiration_date = quote_data.get("expiration_date")
        if expiration_date:
            self.expiration_date.setDate(
                QDate(expiration_date.year, expiration_date.month, expiration_date.day)
            )

        self.products.clear()
        for product_data in quote_data.get("products", []):
            self.products.append(product_data)

        self.update_items_list()
        self.update_summary()
        self.notes_input.setText(quote_data.get("notes", ""))

    def save_quote(self):
        """Saves the current quote details to the database."""
        # This is a placeholder for the actual save logic.
        QMessageBox.information(self, "Save", "Save functionality not yet implemented.")

    def open_product_dialog(self):
        """Opens the dialog to add a new product to the quote."""
        dialog = ProductSelectionDialog(self.product_service, self)
        dialog.product_added.connect(self._on_product_added)
        dialog.exec()

    def _on_product_added(self, product_data):
        """Handles the product_added signal from ProductSelectionDialog."""
        # Add a unique instance ID to the product data
        product_data["instance_id"] = str(uuid.uuid4())
        self.products.append(product_data)
        self.update_items_list()
        self.update_summary()

    def open_spare_parts_dialog(self):
        """Opens the dialog to add spare parts to the quote."""
        # This is a placeholder
        QMessageBox.information(
            self, "Spare Parts", "Spare parts dialog not yet implemented."
        )

    def update_items_list(self):
        """Refreshes the list of quote items."""
        self.items_list_widget.clear()
        for i, product in enumerate(self.products):
            item = QListWidgetItem(self.items_list_widget)
            widget = QuoteItemWidget(product)
            widget.remove_item.connect(self._remove_product)
            widget.edit_item.connect(self._edit_product)
            item.setSizeHint(widget.sizeHint())
            self.items_list_widget.addItem(item)
            self.items_list_widget.setItemWidget(item, widget)

            if i == self.expanded_item_row:
                details_widget = ItemDetailsWidget(product)
                details_item = QListWidgetItem(self.items_list_widget)
                details_item.setSizeHint(details_widget.sizeHint())
                self.items_list_widget.addItem(details_item)
                self.items_list_widget.setItemWidget(details_item, details_widget)
                details_item.setFlags(details_item.flags() & ~Qt.ItemIsSelectable)

    def _remove_product(self, instance_id):
        """Removes a product from the quote using its instance ID."""
        self.products = [
            p for p in self.products if p.get("instance_id") != instance_id
        ]
        self.update_items_list()
        self.update_summary()

    def _edit_product(self, instance_id):
        """Opens the product dialog to edit an existing product."""
        product_to_edit = next(
            (p for p in self.products if p.get("instance_id") == instance_id), None
        )
        if not product_to_edit:
            return

        dialog = ProductSelectionDialog(
            self.product_service, self, product_to_edit=product_to_edit
        )
        if dialog.exec():
            updated_product = dialog.get_selected_product_data()
            if updated_product:
                # Preserve the instance ID when updating
                updated_product["instance_id"] = instance_id
                for i, p in enumerate(self.products):
                    if p.get("instance_id") == instance_id:
                        self.products[i] = updated_product
                        break
                self.update_items_list()
                self.update_summary()

    def _on_item_clicked(self, item):
        """Handles clicks on quote items to expand/collapse details."""
        row = self.items_list_widget.row(item)
        if self.expanded_item_row != -1 and row > self.expanded_item_row:
            row -= 1

        if self.expanded_item_row == row:
            self.expanded_item_row = -1
        else:
            self.expanded_item_row = row
        self.update_items_list()

    def update_summary(self):
        """Calculates and updates the quote summary fields."""
        num_items = len(self.products)
        subtotal = sum(
            (
                p.get("base_price", 0)
                + sum(op.get("price", 0) for op in p.get("options", []))
            )
            * p.get("quantity", 1)
            for p in self.products
        )
        total = subtotal

        self.items_count.setText(str(num_items))
        self.items_total_value.setText(f"${subtotal:,.2f}")
        self.total_value.setText(f"${total:,.2f}")

    def print_quote(self):
        """Handles printing the quote."""
        QMessageBox.information(
            self, "Print", "Print functionality not yet implemented."
        )

    def export_quote(self):
        """Handles exporting the quote."""
        QMessageBox.information(
            self, "Export", "Export functionality not yet implemented."
        )

    def get_current_quote_details(self):
        """Constructs a dictionary with the current state of the quote."""
        return {
            "customer": {
                "name": self.customer_name.text(),
                "company": self.company_name.text(),
                "email": self.email.text(),
                "phone": self.phone.text(),
            },
            "products": self.products,
            "quote_number": self.quote_reference.text(),
            "date_created": self.quote_date.date().toPython(),
            "expiration_date": self.expiration_date.date().toPython(),
            "notes": self.notes_input.text(),
        }
