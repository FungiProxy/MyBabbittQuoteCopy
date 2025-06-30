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
from src.ui.theme import COLORS, FONTS, SPACING, RADIUS, get_button_style


class CustomerSelectionDialog(QDialog):
    """Dialog to select an existing customer from a list."""
    
    customer_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Customer")
        self.setMinimumSize(1300, 700)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['2xl'], SPACING['2xl'], SPACING['2xl'], SPACING['2xl'])
        layout.setSpacing(SPACING['lg'])

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
        
        # Apply modern styling
        self._apply_modern_styling()
        
    def _apply_modern_styling(self):
        """Apply modern styling to the dialog."""
        # Dialog background
        dialog_style = f"""
        QDialog {{
            background-color: {COLORS['bg_secondary']};
            border-radius: {RADIUS['lg']}px;
        }}
        """
        
        # Button styling
        button_style = f"""
        QDialogButtonBox QPushButton {{
            background-color: {COLORS['primary']};
            color: white;
            border: none;
            border-radius: {RADIUS['md']}px;
            padding: {SPACING['md']}px {SPACING['2xl']}px;
            font-weight: {FONTS['weights']['semibold']};
            font-size: {FONTS['sizes']['base']}px;
            font-family: {FONTS['family']};
            min-height: 20px;
        }}
        QDialogButtonBox QPushButton:hover {{
            background-color: {COLORS['primary_hover']};
        }}
        QDialogButtonBox QPushButton:pressed {{
            background-color: {COLORS['primary_pressed']};
        }}
        QDialogButtonBox QPushButton[text="Cancel"] {{
            background-color: {COLORS['secondary']};
            color: {COLORS['text_secondary']};
            border: 2px solid {COLORS['border_light']};
        }}
        QDialogButtonBox QPushButton[text="Cancel"]:hover {{
            background-color: {COLORS['secondary_hover']};
            border-color: {COLORS['border_medium']};
        }}
        """
        
        # Combine styles
        combined_style = dialog_style + button_style
        self.setStyleSheet(combined_style)
        
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