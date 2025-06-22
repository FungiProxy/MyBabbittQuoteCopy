"""
Customer dialog for adding and editing customers.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QMessageBox,
)
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.core.database import SessionLocal
from src.core.models import Customer
from src.core.services.customer_service import CustomerService
logger = logging.getLogger(__name__)


class CustomerDialog(QDialog):
    """Dialog for adding or editing customer information."""
    
    customer_saved = Signal(dict)  # Emits customer data when saved
    
    def __init__(self, parent=None, customer_id=None):
        """Initialize the customer dialog.
        
        Args:
            parent: Parent widget
            customer_id: ID of customer to edit (None for new customer)
        """
        super().__init__(parent)
        self.customer_id = customer_id
        self.is_edit_mode = customer_id is not None
        
        self.setWindowTitle("Edit Customer" if self.is_edit_mode else "Add Customer")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self._init_ui()
        
        if self.is_edit_mode:
            self._load_customer_data()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Contact Name (required)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Required")
        form_layout.addRow("Contact Name*:", self.name_edit)
        
        # Company Name
        self.company_edit = QLineEdit()
        form_layout.addRow("Company:", self.company_edit)
        
        # Email
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("email@example.com")
        form_layout.addRow("Email:", self.email_edit)
        
        # Phone
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("(555) 123-4567")
        form_layout.addRow("Phone:", self.phone_edit)
        
        # Address
        self.address_edit = QLineEdit()
        form_layout.addRow("Address:", self.address_edit)
        
        # City
        self.city_edit = QLineEdit()
        form_layout.addRow("City:", self.city_edit)
        
        # State
        self.state_edit = QLineEdit()
        self.state_edit.setMaxLength(2)
        self.state_edit.setPlaceholderText("TX")
        form_layout.addRow("State:", self.state_edit)
        
        # Zip Code
        self.zip_edit = QLineEdit()
        self.zip_edit.setPlaceholderText("12345")
        form_layout.addRow("Zip Code:", self.zip_edit)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        form_layout.addRow("Notes:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._save_customer)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
        # Apply styling
        self._apply_styling()
    
    def _apply_styling(self):
        """Apply consistent styling to the dialog."""
        style = """
        QDialog {
            background-color: #f5f5f5;
        }
        QLineEdit, QTextEdit {
            padding: 8px;
            border: 1px solid #e0e4e7;
            border-radius: 4px;
            background-color: white;
            font-size: 13px;
        }
        QLineEdit:focus, QTextEdit:focus {
            border-color: #2C3E50;
        }
        QLabel {
            font-size: 13px;
            color: #333;
        }
        """
        self.setStyleSheet(style)
    
    def _load_customer_data(self):
        """Load existing customer data for editing."""
        try:
            with SessionLocal() as db:
                customer = CustomerService.get_customer(db, self.customer_id)
                if customer:
                    self.name_edit.setText(customer.name or "")
                    self.company_edit.setText(customer.company or "")
                    self.email_edit.setText(customer.email or "")
                    self.phone_edit.setText(customer.phone or "")
                    self.address_edit.setText(customer.address or "")
                    self.city_edit.setText(customer.city or "")
                    self.state_edit.setText(customer.state or "")
                    self.zip_edit.setText(customer.zip_code or "")
                    self.notes_edit.setPlainText(customer.notes or "")
                else:
                    QMessageBox.warning(self, "Error", "Customer not found")
                    self.reject()
        except Exception as e:
            logger.error(f"Error loading customer: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load customer: {str(e)}")
            self.reject()
    
    def _save_customer(self):
        """Save the customer data."""
        # Validate required fields
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Contact name is required")
            self.name_edit.setFocus()
            return
        
        try:
            with SessionLocal() as db:
                customer_data = {
                    "name": self.name_edit.text().strip(),
                    "company": self.company_edit.text().strip() or None,
                    "email": self.email_edit.text().strip() or None,
                    "phone": self.phone_edit.text().strip() or None,
                    "address": self.address_edit.text().strip() or None,
                    "city": self.city_edit.text().strip() or None,
                    "state": self.state_edit.text().strip().upper() or None,
                    "zip_code": self.zip_edit.text().strip() or None,
                    "notes": self.notes_edit.toPlainText().strip() or None,
                }
                
                if self.is_edit_mode:
                    # Update existing customer
                    customer = CustomerService.update_customer(
                        db, self.customer_id, customer_data
                    )
                else:
                    # Create new customer
                    customer = CustomerService.create_customer(db, **customer_data)
                
                # Emit signal with customer data
                self.customer_saved.emit({
                    "id": customer.id,
                    "name": customer.name,
                    "company": customer.company,
                    "email": customer.email,
                    "phone": customer.phone,
                })
                
                self.accept()
                
        except SQLAlchemyError as e:
            logger.error(f"Database error saving customer: {e}")
            QMessageBox.critical(self, "Database Error", 
                               "Failed to save customer. Please try again.")
        except Exception as e:
            logger.error(f"Error saving customer: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save customer: {str(e)}")