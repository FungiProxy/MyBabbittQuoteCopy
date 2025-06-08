from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame,
    QDateEdit, QFormLayout, QSizePolicy, QTableWidget, QTableWidgetItem, QSpacerItem,
    QDialog
)
from PySide6.QtCore import Qt, QDate
from src.ui.product_selection_dialog import ProductSelectionDialog
from src.core.services.product_service import ProductService
from src.ui.spare_parts_tab import SparePartsTab

class QuoteCreationPage(QWidget):
    """
    Single-page Quote Creation UI matching the new design.
    Customer info and quote summary at the top, quote items below.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.products = []  # Store added products
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Header: Title and actions
        header_layout = QHBoxLayout()
        title_label = QLabel("Quote Builder")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.save_quote_btn = QPushButton("\U0001F4BE  Save Quote")
        self.save_quote_btn.setFixedWidth(130)
        header_layout.addWidget(self.save_quote_btn)
        self.print_btn = QPushButton("\U0001F5B6  Print")
        self.print_btn.setFixedWidth(100)
        header_layout.addWidget(self.print_btn)
        self.main_layout.addLayout(header_layout)

        # Top section: Customer Info (left) | Quote Summary (right)
        top_layout = QHBoxLayout()
        # Customer Info Card
        customer_card = QFrame()
        customer_card.setObjectName("customerCard")
        customer_card.setStyleSheet("QFrame#customerCard { background: white; border-radius: 10px; border: 1px solid #e0e0e0; }")
        customer_layout = QVBoxLayout(customer_card)
        customer_layout.setContentsMargins(30, 30, 30, 30)
        customer_layout.setSpacing(10)
        customer_title = QLabel("Customer Information")
        customer_title.setStyleSheet("font-size: 22px; font-weight: bold;")
        customer_layout.addWidget(customer_title)
        customer_desc = QLabel("Enter the customer details for this quote")
        customer_desc.setStyleSheet("color: #888; font-size: 15px;")
        customer_layout.addWidget(customer_desc)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Enter company name")
        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter email address")
        self.quote_reference = QLineEdit("BQ-2025-6800")
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Enter phone number")
        self.quote_date = QDateEdit(QDate.currentDate())
        self.quote_date.setCalendarPopup(True)
        self.expiration_date = QDateEdit(QDate.currentDate().addDays(30))
        self.expiration_date.setCalendarPopup(True)
        # Two-column layout for form fields
        form_row1 = QHBoxLayout()
        form_row1.addWidget(self.customer_name)
        form_row1.addWidget(self.company_name)
        form_layout.addRow("Customer Name", form_row1)
        form_row2 = QHBoxLayout()
        form_row2.addWidget(self.email)
        form_row2.addWidget(self.quote_reference)
        form_layout.addRow("Email", form_row2)
        form_row3 = QHBoxLayout()
        form_row3.addWidget(self.phone)
        form_row3.addWidget(self.quote_date)
        form_row3.addWidget(self.expiration_date)
        form_layout.addRow("Phone", form_row3)
        customer_layout.addLayout(form_layout)
        top_layout.addWidget(customer_card, 2)

        # Quote Summary Card
        summary_card = QFrame()
        summary_card.setObjectName("summaryCard")
        summary_card.setStyleSheet("QFrame#summaryCard { background: white; border-radius: 10px; border: 1px solid #e0e0e0; }")
        summary_layout = QVBoxLayout(summary_card)
        summary_layout.setContentsMargins(30, 30, 30, 30)
        summary_layout.setSpacing(10)
        summary_title = QLabel("Quote Summary")
        summary_title.setStyleSheet("font-size: 22px; font-weight: bold;")
        summary_layout.addWidget(summary_title)
        summary_desc = QLabel("Overview of the current quote")
        summary_desc.setStyleSheet("color: #888; font-size: 15px;")
        summary_layout.addWidget(summary_desc)
        self.items_label = QLabel("Items: 0")
        self.subtotal_label = QLabel("Subtotal: $0.00")
        self.tax_label = QLabel("Tax: Not Included")
        self.total_label = QLabel("<b>Total: $0.00</b>")
        summary_layout.addWidget(self.items_label)
        summary_layout.addWidget(self.subtotal_label)
        summary_layout.addWidget(self.tax_label)
        summary_layout.addWidget(self.total_label)
        summary_layout.addSpacing(10)
        self.finalize_btn = QPushButton("\U0001F4C4  Finalize Quote")
        self.finalize_btn.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 10px 0; border-radius: 6px; font-size: 16px;")
        summary_layout.addWidget(self.finalize_btn)
        top_layout.addWidget(summary_card, 1)
        self.main_layout.addLayout(top_layout)

        # Quote Items Section
        items_card = QFrame()
        items_card.setObjectName("itemsCard")
        items_card.setStyleSheet("QFrame#itemsCard { background: white; border-radius: 10px; border: 1px solid #e0e0e0; }")
        items_layout = QVBoxLayout(items_card)
        items_layout.setContentsMargins(30, 30, 30, 30)
        items_layout.setSpacing(20)
        items_title = QLabel("Quote Items")
        items_title.setStyleSheet("font-size: 22px; font-weight: bold;")
        items_layout.addWidget(items_title)
        items_desc = QLabel("Products and services included in this quote")
        items_desc.setStyleSheet("color: #888; font-size: 15px;")
        items_layout.addWidget(items_desc)
        # Empty state
        self.empty_state_frame = QFrame()
        empty_layout = QVBoxLayout(self.empty_state_frame)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_icon = QLabel("\U0001F4C4")
        empty_icon.setStyleSheet("font-size: 48px; color: #90b4fa; margin-bottom: 10px;")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_icon)
        empty_label = QLabel("No Products Added")
        empty_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 8px;")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_label)
        empty_hint = QLabel('Click the "Add Product" button to start adding products to your quote.')
        empty_hint.setStyleSheet("font-size: 15px; color: #888;")
        empty_hint.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_hint)
        items_layout.addWidget(self.empty_state_frame)
        # Product table (hidden if no products)
        self.items_table = QTableWidget(0, 4)
        self.items_table.setHorizontalHeaderLabels(["Product Name", "Description", "Quantity", "Price"])
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.items_table.setVisible(False)
        items_layout.addWidget(self.items_table)
        # Add Product button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.add_spare_parts_btn = QPushButton("Spare Parts")
        self.add_spare_parts_btn.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 10px 24px; border-radius: 6px; font-size: 16px;")
        self.add_spare_parts_btn.setFixedWidth(160)
        btn_layout.addWidget(self.add_spare_parts_btn)
        
        self.add_product_btn = QPushButton("Items")
        self.add_product_btn.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 10px 24px; border-radius: 6px; font-size: 16px;")
        self.add_product_btn.setFixedWidth(160)
        btn_layout.addWidget(self.add_product_btn)
        items_layout.addLayout(btn_layout)
        self.main_layout.addWidget(items_card)

        # Footer
        footer_layout = QHBoxLayout()
        footer_left = QLabel("Babbitt International Inc.")
        footer_right = QLabel("© 2025 All rights reserved")
        footer_layout.addWidget(footer_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_right)
        self.main_layout.addLayout(footer_layout)

        self.add_product_btn.clicked.connect(self.open_product_dialog)
        self.add_spare_parts_btn.clicked.connect(self.open_spare_parts_dialog)

    def open_product_dialog(self):
        dialog = ProductSelectionDialog(product_service=ProductService(), parent=self)
        if dialog.exec():
            product = dialog.selected_product
            if product:
                self.products.append(product)
                self.update_items_table()
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
        self.products.append(part_info)
        self.update_items_table()
        self.update_summary()

    def update_items_table(self):
        if not self.products:
            self.items_table.setVisible(False)
            self.empty_state_frame.setVisible(True)
            return
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(["Product Name", "Description", "Configuration", "Quantity", "Price"])
        self.items_table.setRowCount(len(self.products))
        for row, product in enumerate(self.products):
            name = product.get("name", "")
            desc = product.get("description", "")
            qty = product.get("quantity", 1)
            # Build configuration summary
            config_summary = ""
            for opt in product.get("options", []):
                if opt.get("selected"):
                    config_summary += f"{opt['name']}: {opt['selected']}\n"
            config_item = QTableWidgetItem(config_summary.strip())
            config_item.setToolTip(config_summary.strip())
            # Calculate price (base + options) if available
            base_price = product.get("base_price", 0)
            options_price = 0
            for opt in product.get("options", []):
                if opt.get("selected") and opt.get("price"):
                    options_price += opt["price"]
            price = base_price + options_price
            self.items_table.setItem(row, 0, QTableWidgetItem(str(name)))
            self.items_table.setItem(row, 1, QTableWidgetItem(str(desc)))
            self.items_table.setItem(row, 2, config_item)
            self.items_table.setItem(row, 3, QTableWidgetItem(str(qty)))
            self.items_table.setItem(row, 4, QTableWidgetItem(f"${price:,.2f}"))
        self.items_table.setVisible(True)
        self.empty_state_frame.setVisible(False)

    def update_summary(self):
        items_count = len(self.products)
        subtotal = 0
        for product in self.products:
            qty = product.get("quantity", 1)
            base_price = product.get("base_price", 0)
            options_price = 0
            for opt in product.get("options", []):
                if "choices" in opt and opt.get("selected") is not None:
                    selected = opt["selected"]
                    for choice in opt["choices"]:
                        if choice["label"] == selected:
                            options_price += choice.get("price", 0)
            price = (base_price + options_price) * qty
            subtotal += price
        self.items_label.setText(f"Items: {items_count}")
        self.subtotal_label.setText(f"Subtotal: ${subtotal:,.2f}")
        self.tax_label.setText("Tax: Not Included")
        self.total_label.setText(f"<b>Total: ${subtotal:,.2f}</b>") 