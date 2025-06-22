"""
UI Polish fixes and integration updates.
Apply these changes to your existing files.
"""

# 1. Update main_window.py to properly integrate customers page
# Add this to your MainWindow.__init__ method after creating the pages:

def update_main_window_init():
    """Add customer functionality to main window."""
    return '''
    # In MainWindow.__init__, add after creating pages:
    
    # Import the customer dialog at the top
    from src.ui.dialogs.customer_dialog import CustomerDialog
    
    # Connect customer selection in quote page
    if hasattr(self.quote_page, 'select_customer_btn'):
        self.quote_page.select_customer_btn.clicked.connect(self._select_customer_for_quote)
    '''

# 2. Add customer selection dialog
def create_customer_selection_dialog():
    """Customer selection dialog for quotes."""
    return '''
# Add to src/ui/dialogs/customer_selection_dialog.py

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
    QLineEdit, QPushButton, QLabel, QListWidgetItem,
    QDialogButtonBox
)
from src.core.database import SessionLocal
from src.core.services.customer_service import CustomerService

class CustomerSelectionDialog(QDialog):
    """Dialog for selecting a customer for a quote."""
    
    customer_selected = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Customer")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        self._init_ui()
        self._load_customers()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search customers...")
        self.search_edit.textChanged.connect(self._filter_customers)
        search_layout.addWidget(self.search_edit)
        
        # New customer button
        new_btn = QPushButton("+ New Customer")
        new_btn.clicked.connect(self._add_new_customer)
        search_layout.addWidget(new_btn)
        
        layout.addLayout(search_layout)
        
        # Customer list
        self.customer_list = QListWidget()
        self.customer_list.itemDoubleClicked.connect(self._select_customer)
        layout.addWidget(self.customer_list)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_ok_clicked)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _load_customers(self):
        """Load all customers."""
        with SessionLocal() as db:
            customers = CustomerService.get_all_customers(db)
            self._populate_list(customers)
    
    def _populate_list(self, customers):
        """Populate the customer list."""
        self.customer_list.clear()
        for customer in customers:
            item = QListWidgetItem(f"{customer.name} - {customer.company or 'No Company'}")
            item.setData(Qt.ItemDataRole.UserRole, {
                'id': customer.id,
                'name': customer.name,
                'company': customer.company,
                'email': customer.email,
                'phone': customer.phone
            })
            self.customer_list.addItem(item)
    
    def _filter_customers(self, text):
        """Filter customers based on search text."""
        with SessionLocal() as db:
            if text:
                customers = CustomerService.search_customers(db, text)
            else:
                customers = CustomerService.get_all_customers(db)
            self._populate_list(customers)
    
    def _add_new_customer(self):
        """Open dialog to add new customer."""
        from src.ui.dialogs.customer_dialog import CustomerDialog
        dialog = CustomerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_customers()
    
    def _select_customer(self, item):
        """Handle double-click selection."""
        self.customer_selected.emit(item.data(Qt.ItemDataRole.UserRole))
        self.accept()
    
    def _on_ok_clicked(self):
        """Handle OK button click."""
        current = self.customer_list.currentItem()
        if current:
            self._select_customer(current)
'''

# 3. Update dashboard to show real data
def update_dashboard_stats():
    """Fix dashboard to show real statistics."""
    return '''
# Update src/ui/views/dashboard_redesign.py in _get_dashboard_stats method:

def _get_dashboard_stats(self, db) -> Dict:
    """Get dashboard statistics."""
    try:
        from src.core.models import Quote, Customer
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Get current month start
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        
        # Total quotes this month
        total_quotes = db.query(func.count(Quote.id)).filter(
            Quote.created_at >= month_start
        ).scalar() or 0
        
        # Total pending value
        total_value = db.query(func.sum(Quote.total_price)).filter(
            Quote.status.in_(['DRAFT', 'SENT'])
        ).scalar() or 0.0
        
        # Active customers (customers with quotes in last 90 days)
        ninety_days_ago = now - timedelta(days=90)
        active_customers = db.query(func.count(func.distinct(Quote.customer_id))).filter(
            Quote.created_at >= ninety_days_ago
        ).scalar() or 0
        
        return {
            'total_quotes': total_quotes,
            'total_value': float(total_value),
            'active_customers': active_customers
        }
        
    except Exception as e:
        logger.error(f'Error getting dashboard stats: {e}')
        return {
            'total_quotes': 0,
            'total_value': 0.0,
            'active_customers': 0
        }
'''