"""
Dialog for selecting an existing customer.
"""
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QDialogButtonBox,
)

from src.ui.views.customers_page import CustomersPage


class CustomerSelectionDialog(QDialog):
    """Dialog to select an existing customer from a list."""
    
    customer_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Customer")
        self.setMinimumSize(1300, 700)

        # Main layout
        layout = QVBoxLayout(self)

        # Customer page widget
        self.customers_page = CustomersPage(self)
        # We need a way to know which customer is selected.
        # The table should have a selection model.
        self.customers_page.customers_table.setSelectionBehavior(self.customers_page.customers_table.SelectionBehavior.SelectRows)
        self.customers_page.customers_table.setSelectionMode(self.customers_page.customers_table.SelectionMode.SingleSelection)
        layout.addWidget(self.customers_page)

        # Dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
    def get_selected_customer_data(self):
        """Returns the data of the selected customer."""
        selected_items = self.customers_page.customers_table.selectedItems()
        if not selected_items:
            return None
        
        row = selected_items[0].row()
        
        # Ensure items exist before accessing them
        id_item = self.customers_page.customers_table.item(row, 0)
        name_item = self.customers_page.customers_table.item(row, 0)
        company_item = self.customers_page.customers_table.item(row, 1)
        email_item = self.customers_page.customers_table.item(row, 2)
        phone_item = self.customers_page.customers_table.item(row, 3)

        if not all([id_item, name_item, company_item, email_item, phone_item]):
            return None

        customer_id = id_item.data(Qt.ItemDataRole.UserRole)
        name = name_item.text()
        company = company_item.text()
        email = email_item.text()
        phone = phone_item.text()

        return {
            "id": customer_id,
            "name": name,
            "company": company,
            "email": email,
            "phone": phone,
        }

    def accept(self):
        """Emit signal and accept the dialog."""
        selected_data = self.get_selected_customer_data()
        if selected_data:
            self.customer_selected.emit(selected_data)
        super().accept() 