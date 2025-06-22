from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
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
        self.init_ui()

    def init_ui(self):
        """Set up the UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

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
        self.add_customer_btn.setObjectName("primaryButton")
        top_layout.addWidget(self.add_customer_btn)

        main_layout.addLayout(top_layout)

        # Customers list section
        customers_card = QFrame()
        customers_card.setObjectName("customersCard")

        customers_layout = QVBoxLayout(customers_card)
        customers_layout.setContentsMargins(12, 12, 12, 12)
        customers_layout.setSpacing(10)

        # Customers list header
        header_layout = QHBoxLayout()
        header_title = QLabel("Customers")
        header_title.setStyleSheet("font-size: 15px; font-weight: bold;")
        header_layout.addWidget(header_title)
        header_layout.addStretch()

        customers_layout.addLayout(header_layout)

        # Customers table
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(5)
        self.customers_table.setHorizontalHeaderLabels(["Name", "Company", "Email", "Phone", "Actions"])
        header = self.customers_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.customers_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        customers_layout.addWidget(self.customers_table)

        main_layout.addWidget(customers_card)

        # Footer
        footer_layout = QHBoxLayout()
        footer_left = QLabel("Babbitt International Inc.")
        footer_right = QLabel("© 2025 All rights reserved")
        footer_layout.addWidget(footer_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_right)
        main_layout.addLayout(footer_layout)

        # Connect signals
        self.search_bar.textChanged.connect(self._filter_customers)
        self.add_customer_btn.clicked.connect(self._add_customer)
        self._filter_customers() # Initial load

    def _filter_customers(self):
        """Filter customers based on search text."""
        search_term = self.search_bar.text()
        
        with SessionLocal() as db:
            customers = CustomerService.search_customers(db, search_term)
            self.customers_table.setRowCount(0) # Clear table
            for row, customer in enumerate(customers):
                self.customers_table.insertRow(row)

                # Store customer ID in the first item's data
                name_item = QTableWidgetItem(str(customer.name))
                name_item.setData(Qt.ItemDataRole.UserRole, customer.id)
                self.customers_table.setItem(row, 0, name_item)

                self.customers_table.setItem(row, 1, QTableWidgetItem(str(customer.company or "")))
                self.customers_table.setItem(row, 2, QTableWidgetItem(str(customer.email or "")))
                self.customers_table.setItem(row, 3, QTableWidgetItem(str(customer.phone or "")))

                # Actions buttons
                edit_btn = QPushButton("Edit")
                delete_btn = QPushButton("Delete")
                edit_btn.clicked.connect(lambda _, r=row: self._edit_customer(r))
                delete_btn.clicked.connect(lambda _, r=row: self._delete_customer(r))

                actions_layout = QHBoxLayout()
                actions_layout.addWidget(edit_btn)
                actions_layout.addWidget(delete_btn)
                actions_layout.setContentsMargins(0, 0, 0, 0)
                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)

                self.customers_table.setCellWidget(row, 4, actions_widget)
                self.customers_table.setRowHeight(row, 40)

    def _add_customer(self):
        """Handle add customer button click."""
        dialog = CustomerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._filter_customers()

    def _edit_customer(self, row):
        item = self.customers_table.item(row, 0)
        if not item:
            return
        customer_id = item.data(Qt.ItemDataRole.UserRole)

        dialog = CustomerDialog(self, customer_id=customer_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._filter_customers()

    def _delete_customer(self, row):
        item = self.customers_table.item(row, 0)
        if not item:
            return
        customer_id = item.data(Qt.ItemDataRole.UserRole)
        customer_name = item.text()

        reply = QMessageBox.question(
            self,
            "Delete Customer",
            f"Are you sure you want to delete {customer_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            with SessionLocal() as db:
                success = CustomerService.delete_customer(db, customer_id)
                if success:
                    QMessageBox.information(self, "Success", f"{customer_name} has been deleted.")
                    self._filter_customers()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete {customer_name}.")
