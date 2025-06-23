from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDialog,
    QMessageBox,
    QHeaderView,
    QTextEdit,
    QSplitter,
    QScrollArea,
)
from src.ui.dialogs.customer_dialog import CustomerDialog
from src.core.database import SessionLocal
from src.core.services.customer_service import CustomerService

"""
Customers Page for the Babbitt Quote Generator.

This module defines the customers management interface for the quote generator.
It provides functionality to:
- View list of customers
- Add new customers
- Edit existing customers
- View customer details and history
"""

class CustomersPage(QWidget):
    """
    Customers management page for the quote generator.

    This page allows users to manage customer information including:
    - Viewing customer list
    - Adding new customers
    - Editing customer details
    - Viewing customer quote history
    """

    def __init__(self, parent=None):
        """Initialize the CustomersPage."""
        super().__init__(parent)
        self.selected_customer_id = None
        self.init_ui()

    def init_ui(self):
        """Set up the UI components."""
        # Main layout
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side (Table)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(16) # Add spacing
        
        # Top section with search and add customer
        top_layout = QHBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search customers...")
        self.search_bar.setFixedWidth(300)
        top_layout.addWidget(self.search_bar)

        top_layout.addStretch()

        # Add Customer button
        self.add_customer_btn = QPushButton("+ Add Customer")
        self.add_customer_btn.setProperty("class", "primary")
        top_layout.addWidget(self.add_customer_btn)

        left_layout.addLayout(top_layout)

        # Customers table
        self.customers_table = QTableWidget()
        self.customers_table.setObjectName("customersTable")
        self.customers_table.setColumnCount(4)
        self.customers_table.setHorizontalHeaderLabels(["Name", "Company", "Email", "Phone"])
        header = self.customers_table.horizontalHeader()

        # Left align headers and add separators
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setStyleSheet("QHeaderView::section { border-right: 1px solid #d0d0d0; padding-left: 5px; }")

        # Set more balanced resize modes and initial widths
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.customers_table.setColumnWidth(0, 250)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.customers_table.setColumnWidth(1, 150)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.customers_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.customers_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.customers_table.setShowGrid(False)
        self.customers_table.verticalHeader().setVisible(False)
        self.customers_table.verticalHeader().setDefaultSectionSize(45) # Set row height
        left_layout.addWidget(self.customers_table)
        
        splitter.addWidget(left_widget)

        # Right side (Details Panel)
        details_panel = self._create_details_panel()
        splitter.addWidget(details_panel)
        
        splitter.setSizes([1050, 350]) # Adjust initial sizes
        main_layout.addWidget(splitter)

        # Connect signals
        self.search_bar.textChanged.connect(self._filter_customers)
        self.add_customer_btn.clicked.connect(self._add_customer)
        self.customers_table.itemSelectionChanged.connect(self._on_customer_selected)
        self.edit_customer_btn.clicked.connect(self._handle_edit_customer)
        self.delete_customer_btn.clicked.connect(self._handle_delete_customer)
        self._filter_customers() # Initial load

    def _create_details_panel(self):
        """Create the redesigned panel to display customer details."""
        details_card = QFrame()
        details_card.setObjectName("detailsCard")
        
        card_layout = QVBoxLayout(details_card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(20)
        
        # Details Header
        header_title = QLabel("Customer Details")
        header_title.setObjectName("detailsTitle")
        card_layout.addWidget(header_title)

        # Scroll Area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("detailsScrollArea")
        
        scroll_content = QWidget()
        scroll_content.setObjectName("detailsScrollContent")
        self.details_layout = QVBoxLayout(scroll_content)
        self.details_layout.setContentsMargins(0, 8, 0, 8)
        self.details_layout.setSpacing(24)

        # Create detail fields
        self.details_name = self._add_detail_to_layout("Name")
        self.details_company = self._add_detail_to_layout("Company")
        self.details_email = self._add_detail_to_layout("Email")
        self.details_phone = self._add_detail_to_layout("Phone")
        
        # Create and add the notes widget separately to ensure correct typing
        notes_label = QLabel("Notes")
        notes_label.setObjectName("detailLabel")
        self.details_notes = QTextEdit()
        self.details_notes.setReadOnly(True)
        self.details_notes.setObjectName("detailValueNotes")
        self.details_notes.setFixedHeight(120)

        notes_container = QWidget()
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(4)
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.details_notes)
        self.details_layout.addWidget(notes_container)
        
        self.details_layout.addStretch()
        
        self.scroll_area = scroll_area
        
        scroll_area.setWidget(scroll_content)
        card_layout.addWidget(scroll_area)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.edit_customer_btn = QPushButton("Edit")
        self.edit_customer_btn.setProperty("class", "secondary")
        self.edit_customer_btn.setEnabled(False)
        button_layout.addWidget(self.edit_customer_btn)

        self.delete_customer_btn = QPushButton("Delete")
        self.delete_customer_btn.setProperty("class", "danger")
        self.delete_customer_btn.setEnabled(False)
        button_layout.addWidget(self.delete_customer_btn)
        
        button_layout.addStretch()
        
        card_layout.addLayout(button_layout)
        
        # Placeholder for when no customer is selected
        self.no_customer_selected_label = self._create_placeholder()
        card_layout.addWidget(self.no_customer_selected_label)

        return details_card

    def _add_detail_to_layout(self, label_text, is_multiline=False):
        """Helper to create and add a detail widget to the layout."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        label = QLabel(label_text)
        label.setObjectName("detailLabel")
        
        if is_multiline:
            value_widget = QTextEdit()
            value_widget.setReadOnly(True)
            value_widget.setObjectName("detailValueNotes")
            value_widget.setFixedHeight(120)
        else:
            value_widget = QLabel("—")
            value_widget.setObjectName("detailValue")
            value_widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addWidget(label)
        layout.addWidget(value_widget)
        
        self.details_layout.addWidget(widget)
        return value_widget

    def _create_placeholder(self):
        """Create a placeholder widget for when no customer is selected."""
        placeholder = QWidget()
        placeholder.setObjectName("detailsPlaceholder")
        
        layout = QVBoxLayout(placeholder)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon = QLabel("👤")
        icon.setObjectName("placeholderIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        text = QLabel("Select a customer")
        text.setObjectName("placeholderText")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtext = QLabel("Details will be shown here.")
        subtext.setObjectName("placeholderSubtext")
        subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(text)
        layout.addWidget(subtext)
        
        return placeholder

    def _on_customer_selected(self):
        """Handle customer selection from the table."""
        selected_items = self.customers_table.selectedItems()
        
        if selected_items:
            row = selected_items[0].row()
            customer_id_item = self.customers_table.item(row, 0)
            if customer_id_item:
                self.selected_customer_id = customer_id_item.data(Qt.ItemDataRole.UserRole)
                self.edit_customer_btn.setEnabled(True)
                self.delete_customer_btn.setEnabled(True)
                self._update_details_panel(self.selected_customer_id)
            else:
                self.selected_customer_id = None
                self.edit_customer_btn.setEnabled(False)
                self.delete_customer_btn.setEnabled(False)
                self._clear_details_panel()
        else:
            self.selected_customer_id = None
            self.edit_customer_btn.setEnabled(False)
            self.delete_customer_btn.setEnabled(False)
            self._clear_details_panel()

    def _clear_details_panel(self):
        """Clear the details panel and show a placeholder."""
        self.no_customer_selected_label.setVisible(True)
        self.scroll_area.setVisible(False)
        self.details_name.setText("—")
        self.details_company.setText("—")
        self.details_email.setText("—")
        self.details_phone.setText("—")
        self.details_notes.setPlainText("")

    def _update_details_panel(self, customer_id):
        """Fetch and display customer details."""
        self.no_customer_selected_label.setVisible(False)
        self.scroll_area.setVisible(True)
        with SessionLocal() as db:
            customer = CustomerService.get_customer(db, customer_id)
            if customer:
                self.details_name.setText(customer.name)
                self.details_company.setText(customer.company)
                self.details_email.setText(customer.email)
                self.details_phone.setText(customer.phone)
                self.details_notes.setPlainText(customer.notes or "")
            else:
                self._clear_details_panel()

    def _filter_customers(self):
        """Filter customers based on search text."""
        search_text = self.search_bar.text().lower()
        self.customers_table.setRowCount(0)

        with SessionLocal() as db:
            customers = CustomerService.search_customers(db, search_text)
            for row_position, customer in enumerate(customers):
                self.customers_table.insertRow(row_position)

                # Store customer ID in the first item's data
                name_item = QTableWidgetItem(str(customer.name))
                name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                name_item.setData(Qt.ItemDataRole.UserRole, customer.id)
                self.customers_table.setItem(row_position, 0, name_item)

                company_item = QTableWidgetItem(str(customer.company) if customer.company is not None else "")
                company_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.customers_table.setItem(row_position, 1, company_item)

                email_item = QTableWidgetItem(str(customer.email) if customer.email is not None else "")
                email_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.customers_table.setItem(row_position, 2, email_item)

                phone_item = QTableWidgetItem(str(customer.phone) if customer.phone is not None else "")
                phone_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.customers_table.setItem(row_position, 3, phone_item)

        if self.customers_table.rowCount() > 0:
            self.customers_table.selectRow(0)

        # Force the details panel to update based on the current selection state.
        # This is more reliable than depending on the itemSelectionChanged signal
        # to be emitted after programmatically selecting a row.
        self._on_customer_selected()

    def _add_customer(self):
        """Open a dialog to add a new customer."""
        dialog = CustomerDialog(parent=self)
        if dialog.exec():
            self._filter_customers()

    def _handle_edit_customer(self):
        """Handle edit customer button click."""
        if self.selected_customer_id:
            self._edit_customer(self.selected_customer_id)

    def _handle_delete_customer(self):
        """Handle delete customer button click."""
        if self.selected_customer_id:
            self._delete_customer(self.selected_customer_id)

    def _edit_customer(self, customer_id):
        """Open a dialog to edit the customer with the given ID."""
        dialog = CustomerDialog(customer_id=customer_id, parent=self)
        if dialog.exec():
            self._filter_customers()

    def _delete_customer(self, customer_id):
        """Delete the customer with the given ID."""
        reply = QMessageBox.warning(
            self,
            "Delete Customer",
            "Are you sure you want to delete this customer?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            with SessionLocal() as db:
                if CustomerService.delete_customer(db, customer_id):
                    self._filter_customers()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete customer.")
