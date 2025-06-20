"""
Customers Page for the Babbitt Quote Generator.

This module defines the customers management interface for the quote generator.
It provides functionality to:
- View list of customers
- Add new customers
- Edit existing customers
- View customer details and history
"""

from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


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

        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Customers", "Active", "Inactive"])
        header_layout.addWidget(self.filter_combo)

        customers_layout.addLayout(header_layout)

        # Customers list
        self.customers_list = QListWidget()
        self.customers_list.setMinimumHeight(400)
        customers_layout.addWidget(self.customers_list)

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
        self.filter_combo.currentTextChanged.connect(self._filter_customers)
        self.add_customer_btn.clicked.connect(self._add_customer)
        self.customers_list.itemClicked.connect(self._on_customer_selected)

    def _filter_customers(self):
        """Filter customers based on search text and filter selection."""
        # TODO: Implement customer filtering logic
        pass

    def _add_customer(self):
        """Handle add customer button click."""
        # TODO: Implement add customer dialog
        pass

    def _on_customer_selected(self, item):
        """Handle customer selection from the list."""
        # TODO: Implement customer details view
        pass
