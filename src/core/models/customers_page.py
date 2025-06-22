"""
Customers Page for the Babbitt Quote Generator - COMPLETE IMPLEMENTATION.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

from src.core.database import SessionLocal
from src.core.services.customer_service import CustomerService
from src.ui.dialogs.customer_dialog import CustomerDialog
from src.utils.logging_setup import logger


class CustomerListItem(QListWidgetItem):
    """Custom list item to store customer data."""
    
    def __init__(self, customer_data):
        """Initialize with customer data."""
        self.customer_data = customer_data
        
        # Format display text
        display_text = customer_data['name']
        if customer_data.get('company'):
            display_text += f" - {customer_data['company']}"
        if customer_data.get('email'):
            display_text += f"\n{customer_data['email']}"
        if customer_data.get('phone'):
            display_text += f" | {customer_data['phone']}"
            
        super().__init__(display_text)


class CustomersPage(QWidget):
    """Customers management page for the quote generator."""

    def __init__(self, parent=None):
        """Initialize the CustomersPage."""
        super().__init__(parent)
        self.search_timer = QTimer()
        self.search_timer.timeout.connect(self._perform_search)
        self.search_timer.setSingleShot(True)
        
        self.init_ui()
        self._load_customers()

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
        self.add_customer_btn.setStyleSheet("""
            QPushButton#primaryButton {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton#primaryButton:hover {
                background-color: #1d4ed8;
            }
        """)
        top_layout.addWidget(self.add_customer_btn)

        main_layout.addLayout(top_layout)

        # Customers list section
        customers_card = QFrame()
        customers_card.setObjectName("customersCard")
        customers_card.setStyleSheet("""
            QFrame#customersCard {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e4e7;
            }
        """)

        customers_layout = QVBoxLayout(customers_card)
        customers_layout.setContentsMargins(20, 20, 20, 20)
        customers_layout.setSpacing(15)

        # Customers list header
        header_layout = QHBoxLayout()
        header_title = QLabel("Customers")
        header_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(header_title)
        header_layout.addStretch()

        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Customers", "Active", "Inactive"])
        self.filter_combo.setMaximumHeight(32)
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 6px 10px;
                border: 1px solid #e0e4e7;
                border-radius: 4px;
                background-color: white;
                font-size: 13px;
            }
        """)
        header_layout.addWidget(self.filter_combo)

        customers_layout.addLayout(header_layout)

        # Customers list
        self.customers_list = QListWidget()
        self.customers_list.setMinimumHeight(400)
        self.customers_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e0e4e7;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)