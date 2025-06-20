"""
Customers Page for the Babbitt Quote Generator.

This module defines the customers management interface for the quote generator.
It provides functionality to:
- View list of customers
- Add new customers
- Edit existing customers
- View customer details and history
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.database import SessionLocal
from src.core.services.customer_service import CustomerService

logger = logging.getLogger(__name__)


class CustomersPage(QWidget):
    """
    Customers management page for the quote generator.

    This page allows users to manage customer information including:
    - Viewing customer list
    - Adding new customers
    - Editing customer details
    - Viewing customer quote history
    """

    customer_selected = Signal(dict)  # Emitted when a customer is selected

    def __init__(self, parent=None):
        """Initialize the CustomersPage."""
        super().__init__(parent)
        self.setWindowTitle('Customers')
        self.customer_service = CustomerService()
        self.db = SessionLocal()
        self.customers = []
        self.filtered_customers = []

        self.init_ui()
        self.load_customers()
        
        # Apply modern styling fixes
        self._apply_compact_styling()

    def __del__(self):
        """Clean up database connection."""
        if hasattr(self, 'db') and self.db:
            self.db.close()

    def _apply_compact_styling(self):
        """🔴 CRITICAL: Fix oversized dropdown boxes."""
        # Apply to all combo boxes in the dialog
        for combo in self.findChildren(QComboBox):
            combo.setMaximumHeight(32)
            combo.setMinimumHeight(28) 
            combo.setStyleSheet("""
                QComboBox {
                    padding: 6px 10px;
                    border: 1px solid #e0e4e7;
                    border-radius: 4px;
                    background-color: white;
                    font-size: 13px;
                    max-height: 32px;
                    min-height: 28px;
                }
                QComboBox:focus {
                    border-color: #2C3E50;
                }
                QComboBox::drop-down {
                    width: 20px;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    border: 1px solid #e0e4e7;
                    border-radius: 4px;
                    background-color: white;
                    selection-background-color: #e3f2fd;
                    max-height: 200px;
                }
            """)

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
        self.search_bar.setPlaceholderText('Search customers...')
        self.search_bar.setFixedWidth(300)
        top_layout.addWidget(self.search_bar)

        top_layout.addStretch()

        # Add Customer button
        self.add_customer_btn = QPushButton('+ Add Customer')
        self.add_customer_btn.setObjectName('primaryButton')
        top_layout.addWidget(self.add_customer_btn)

        main_layout.addLayout(top_layout)

        # Customers list section
        customers_card = QFrame()
        customers_card.setObjectName('customersCard')

        customers_layout = QVBoxLayout(customers_card)
        customers_layout.setContentsMargins(12, 12, 12, 12)
        customers_layout.setSpacing(10)

        # Customers list header
        header_layout = QHBoxLayout()
        header_title = QLabel('Customers')
        header_title.setStyleSheet('font-size: 15px; font-weight: bold;')
        header_layout.addWidget(header_title)
        header_layout.addStretch()

        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['All Customers', 'Active', 'Inactive'])
        header_layout.addWidget(self.filter_combo)

        customers_layout.addLayout(header_layout)

        # Customers list
        self.customers_list = QListWidget()
        self.customers_list.setMinimumHeight(400)
        customers_layout.addWidget(self.customers_list)

        main_layout.addWidget(customers_card)

        # Footer
        footer_layout = QHBoxLayout()
        footer_left = QLabel('Babbitt International Inc.')
        footer_left.setStyleSheet('color: #6c757d; font-size: 12px;')
        footer_layout.addWidget(footer_left)

        footer_layout.addStretch()

        footer_right = QLabel('Customer Management System')
        footer_right.setStyleSheet('color: #6c757d; font-size: 12px;')
        footer_layout.addWidget(footer_right)

        main_layout.addLayout(footer_layout)

        # Connect signals
        self.search_bar.textChanged.connect(self.filter_customers)
        self.filter_combo.currentTextChanged.connect(self.filter_customers)
        self.add_customer_btn.clicked.connect(self.add_customer)
        self.customers_list.itemClicked.connect(self.on_customer_selected)

    def load_customers(self):
        """Load customers from the database."""
        try:
            self.customers = self.customer_service.get_all_customers(self.db)
            self.filtered_customers = self.customers.copy()
            self.update_customers_list()
        except Exception as e:
            logger.error(f'Error loading customers: {e}')

    def update_customers_list(self):
        """Update the customers list widget."""
        self.customers_list.clear()

        for customer in self.filtered_customers:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, customer)

            # Create customer display widget
            customer_widget = self.create_customer_widget(customer)
            item.setSizeHint(customer_widget.sizeHint())

            self.customers_list.addItem(item)
            self.customers_list.setItemWidget(item, customer_widget)

    def create_customer_widget(self, customer: Dict) -> QWidget:
        """Create a widget to display customer information."""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 12px;
                margin: 2px;
            }
            QFrame:hover {
                border-color: #2C3E50;
                background-color: #f8f9fa;
            }
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Customer name
        name_label = QLabel(customer.get('name', 'Unknown Customer'))
        name_label.setStyleSheet('font-weight: 600; font-size: 14px; color: #2C3E50;')
        layout.addWidget(name_label)

        # Customer details
        details_layout = QHBoxLayout()
        details_layout.setSpacing(20)

        # Email
        email = customer.get('email', 'No email')
        email_label = QLabel(f'📧 {email}')
        email_label.setStyleSheet('color: #6c757d; font-size: 12px;')
        details_layout.addWidget(email_label)

        # Phone
        phone = customer.get('phone', 'No phone')
        phone_label = QLabel(f'📞 {phone}')
        phone_label.setStyleSheet('color: #6c757d; font-size: 12px;')
        details_layout.addWidget(phone_label)

        # Company
        company = customer.get('company', 'No company')
        company_label = QLabel(f'🏢 {company}')
        company_label.setStyleSheet('color: #6c757d; font-size: 12px;')
        details_layout.addWidget(company_label)

        details_layout.addStretch()
        layout.addLayout(details_layout)

        return widget

    def filter_customers(self):
        """Filter customers based on search text and filter selection."""
        search_text = self.search_bar.text().lower()
        filter_type = self.filter_combo.currentText()

        self.filtered_customers = []

        for customer in self.customers:
            # Apply search filter
            if search_text:
                searchable_text = f"{customer.get('name', '')} {customer.get('email', '')} {customer.get('company', '')}".lower()
                if search_text not in searchable_text:
                    continue

            # Apply type filter
            if filter_type == 'Active' and not customer.get('active', True):
                continue
            elif filter_type == 'Inactive' and customer.get('active', True):
                continue

            self.filtered_customers.append(customer)

        self.update_customers_list()

    def add_customer(self):
        """Add a new customer."""
        # TODO: Implement add customer dialog
        logger.info('Add customer functionality not yet implemented')

    def on_customer_selected(self, item: QListWidgetItem):
        """Handle customer selection."""
        customer = item.data(Qt.UserRole)
        self.customer_selected.emit(customer)
        logger.info(f'Customer selected: {customer.get("name", "Unknown")}')
