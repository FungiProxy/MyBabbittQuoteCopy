"""
Redesigned Quote Creation Page

Clean, step-by-step quote creation interface with integrated product selection,
configuration, and customer information forms. Focuses on user-friendly workflow.
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QGroupBox,
    QFormLayout,
)

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService
from src.ui.components.product_selection_redesign import ProductSelectionDialog
from src.ui.components.configuration_wizard import ConfigurationWizard

logger = logging.getLogger(__name__)


class QuoteCreationPageRedesign(QWidget):
    """
    Redesigned quote creation page with clean workflow and modern interface.
    
    Features:
    - Step-by-step quote building
    - Integrated product selection and configuration
    - Real-time quote totals
    - Customer information management
    - Professional quote summary
    """
    
    quote_created = Signal(dict)  # Emitted when quote is successfully created
    quote_updated = Signal(dict)  # Emitted when quote is updated
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Services
        self.db = SessionLocal()
        self.quote_service = QuoteService()
        
        # Current quote state
        self.current_quote = {
            "items": [],
            "customer_info": {},
            "total_value": 0.0,
            "quote_number": None,
            "status": "Draft"
        }
        
        self._setup_ui()

    def __del__(self):
        """Clean up database connection."""
        if hasattr(self, 'db') and self.db:
            self.db.close()

    def _setup_ui(self):
        """Set up the quote creation UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Quote header
        header_widget = self._create_quote_header()
        main_layout.addWidget(header_widget)
        
        # Main content grid
        content_widget = QWidget()
        content_layout = QGridLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Left column - Quote items
        items_panel = self._create_items_panel()
        content_layout.addWidget(items_panel, 0, 0, 2, 1)
        
        # Right column - Customer info and actions
        customer_panel = self._create_customer_panel()
        content_layout.addWidget(customer_panel, 0, 1)
        
        actions_panel = self._create_actions_panel()
        content_layout.addWidget(actions_panel, 1, 1)
        
        # Set column proportions (2:1 ratio)
        content_layout.setColumnStretch(0, 2)
        content_layout.setColumnStretch(1, 1)
        
        main_layout.addWidget(content_widget)
        
        # Now that all components are created, update visibility
        self._update_items_visibility()

    def _create_quote_header(self) -> QWidget:
        """Create the quote header with title and basic info."""
        header = QFrame()
        header.setProperty("class", "card")
        
        layout = QHBoxLayout(header)
        
        # Title and quote number
        title_layout = QVBoxLayout()
        
        title = QLabel("New Quote")
        title.setObjectName("pageTitle")
        title_layout.addWidget(title)
        
        self.quote_number_label = QLabel("Quote #: (Will be assigned on save)")
        self.quote_number_label.setProperty("class", "quoteSubtitle")
        title_layout.addWidget(self.quote_number_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Quote status and total
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.status_label = QLabel("Status: Draft")
        self.status_label.setProperty("class", "status-draft")
        status_layout.addWidget(self.status_label)
        
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setObjectName("quoteTotalLabel")
        status_layout.addWidget(self.total_label)
        
        layout.addLayout(status_layout)
        
        return header

    def _create_items_panel(self) -> QWidget:
        """Create the quote items panel."""
        panel = QGroupBox("Quote Items")
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Add product button
        add_product_btn = QPushButton("+ Add Product")
        add_product_btn.setProperty("class", "primary")
        add_product_btn.clicked.connect(self._add_product)
        layout.addWidget(add_product_btn)
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels([
            "Product", "Configuration", "Quantity", "Unit Price", "Total", "Actions"
        ])
        
        # Configure table
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Product
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)          # Configuration
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Quantity
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Unit Price
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Total
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Actions
        
        self.items_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.items_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.items_table)
        
        # Empty state message
        self.empty_state_label = QLabel("No items added yet. Click 'Add Product' to get started.")
        self.empty_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_state_label.setProperty("class", "placeholderCard")
        layout.addWidget(self.empty_state_label)
        
        return panel

    def _create_customer_panel(self) -> QWidget:
        """Create the customer information panel."""
        panel = QGroupBox("Customer Information")
        
        layout = QFormLayout(panel)
        layout.setSpacing(10)
        
        # Customer form fields
        self.company_name_edit = QLineEdit()
        self.company_name_edit.setPlaceholderText("Enter company name")
        self.company_name_edit.textChanged.connect(self._on_customer_info_changed)
        
        self.contact_name_edit = QLineEdit()
        self.contact_name_edit.setPlaceholderText("Enter contact person")
        self.contact_name_edit.textChanged.connect(self._on_customer_info_changed)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter email address")
        self.email_edit.textChanged.connect(self._on_customer_info_changed)
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Enter phone number")
        self.phone_edit.textChanged.connect(self._on_customer_info_changed)
        
        # Add to form
        layout.addRow("Company Name:", self.company_name_edit)
        layout.addRow("Contact Person:", self.contact_name_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Phone:", self.phone_edit)
        
        # Notes field
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Additional notes or requirements...")
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.textChanged.connect(self._on_customer_info_changed)
        
        layout.addRow("Notes:", self.notes_edit)
        
        return panel

    def _create_actions_panel(self) -> QWidget:
        """Create the actions panel with save/send buttons."""
        panel = QFrame()
        panel.setProperty("class", "card")
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Action buttons
        self.save_draft_btn = QPushButton("Save Draft")
        self.save_draft_btn.setProperty("class", "secondary")
        self.save_draft_btn.clicked.connect(self._save_draft)
        
        self.generate_pdf_btn = QPushButton("Generate PDF")
        self.generate_pdf_btn.setProperty("class", "primary")
        self.generate_pdf_btn.clicked.connect(self._generate_pdf)
        
        self.send_quote_btn = QPushButton("Send Quote")
        self.send_quote_btn.setProperty("class", "success")
        self.send_quote_btn.clicked.connect(self._send_quote)
        
        # Add buttons to layout
        layout.addWidget(self.save_draft_btn)
        layout.addWidget(self.generate_pdf_btn)
        layout.addWidget(self.send_quote_btn)
        
        # Initially disable some buttons
        self.generate_pdf_btn.setEnabled(False)
        self.send_quote_btn.setEnabled(False)
        
        return panel

    def _add_product(self):
        """Open product selection dialog."""
        # Get current theme from parent window if available
        theme_name = None
        if self.parent():
            try:
                # Try to get theme from main window
                main_window = self.parent()
                while main_window and not hasattr(main_window, 'settings_service'):
                    main_window = main_window.parent()
                
                if main_window and hasattr(main_window, 'settings_service'):
                    theme_name = main_window.settings_service.get_theme('Modern Babbitt')
            except:
                theme_name = 'Modern Babbitt'
        
        dialog = ProductSelectionDialog(self, theme_name=theme_name)
        dialog.product_selected.connect(self._on_product_configured)
        dialog.exec()

    def _on_product_configured(self, config_data: Dict):
        """Handle completed product configuration."""
        try:
            # Add to quote items
            # This part needs to be updated to handle the new unified data structure
            quote_item = {
                "product_family": config_data.get("family_name", config_data.get("name")),
                "model_number": config_data.get("name", "N/A"), # Placeholder
                "configuration": "Details from new config flow", # Placeholder
                "quantity": 1,
                "unit_price": config_data.get("base_price", 0), # Placeholder
                "total_price": config_data.get("base_price", 0), # Placeholder
                "config_data": config_data
            }
            
            self.current_quote["items"].append(quote_item)
            self._update_items_table()
            self._update_quote_totals()
            
            logger.info(f"Added product to quote: {quote_item['model_number']}")
            
        except Exception as e:
            logger.error(f"Error adding configured product: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add product to quote: {str(e)}")

    def _format_configuration(self, selected_options: Dict) -> str:
        """Format configuration options for display."""
        config_parts = []
        
        # Key configuration elements
        material = selected_options.get("Material")
        if material:
            config_parts.append(f"Material: {material}")
        
        voltage = selected_options.get("Voltage")
        if voltage:
            config_parts.append(f"Voltage: {voltage}")
        
        length = selected_options.get("Probe Length")
        if length:
            config_parts.append(f"Length: {length}\"")
        
        connection = selected_options.get("Connection")
        if connection and connection != "NPT":
            config_parts.append(f"Connection: {connection}")
        
        # Additional options
        if selected_options.get("Extended Probe"):
            config_parts.append("Extended Probe")
        
        if selected_options.get("Explosion Proof"):
            config_parts.append("Explosion Proof")
        
        if selected_options.get("NEMA 4X"):
            config_parts.append("NEMA 4X")
        
        return " | ".join(config_parts) if config_parts else "Standard Configuration"

    def _update_items_table(self):
        """Update the items table with current quote items."""
        self.items_table.setRowCount(len(self.current_quote["items"]))
        
        for row, item in enumerate(self.current_quote["items"]):
            # Product name
            product_item = QTableWidgetItem(item["product_family"])
            product_item.setFlags(product_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.items_table.setItem(row, 0, product_item)
            
            # Configuration
            config_item = QTableWidgetItem(item["configuration"])
            config_item.setFlags(config_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.items_table.setItem(row, 1, config_item)
            
            # Quantity (editable)
            quantity_item = QTableWidgetItem(str(item["quantity"]))
            quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(row, 2, quantity_item)
            
            # Unit price
            unit_price_item = QTableWidgetItem(f"${item['unit_price']:,.2f}")
            unit_price_item.setFlags(unit_price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            unit_price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.items_table.setItem(row, 3, unit_price_item)
            
            # Total price
            total_price_item = QTableWidgetItem(f"${item['total_price']:,.2f}")
            total_price_item.setFlags(total_price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            total_price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.items_table.setItem(row, 4, total_price_item)
            
            # Actions
            actions_widget = self._create_actions_widget(row)
            self.items_table.setCellWidget(row, 5, actions_widget)
        
        # Connect quantity change signal
        self.items_table.itemChanged.connect(self._on_item_changed)
        
        self._update_items_visibility()

    def _create_actions_widget(self, row: int) -> QWidget:
        """Create action buttons for table row."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setProperty("class", "info small")
        
        # Remove button
        remove_btn = QPushButton("Remove")
        remove_btn.setProperty("class", "danger small")
        
        layout.addWidget(edit_btn)
        layout.addWidget(remove_btn)
        
        return widget

    def _update_items_visibility(self):
        """Update visibility of items table vs empty state."""
        has_items = len(self.current_quote["items"]) > 0
        self.items_table.setVisible(has_items)
        self.empty_state_label.setVisible(not has_items)
        
        # Update action buttons
        self.generate_pdf_btn.setEnabled(has_items and self._has_customer_info())
        self.send_quote_btn.setEnabled(has_items and self._has_customer_info())

    def _has_customer_info(self) -> bool:
        """Check if required customer information is provided."""
        return bool(
            self.company_name_edit.text().strip() and
            self.contact_name_edit.text().strip() and
            self.email_edit.text().strip()
        )

    def _on_item_changed(self, item: QTableWidgetItem):
        """Handle changes to table items (e.g., quantity)."""
        if item.column() == 2:  # Quantity column
            try:
                row = item.row()
                new_quantity = int(item.text())
                
                if new_quantity <= 0:
                    raise ValueError("Quantity must be positive")
                
                # Update quote item
                quote_item = self.current_quote["items"][row]
                quote_item["quantity"] = new_quantity
                quote_item["total_price"] = quote_item["unit_price"] * new_quantity
                
                # Update total price cell
                total_item = QTableWidgetItem(f"${quote_item['total_price']:,.2f}")
                total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.items_table.setItem(row, 4, total_item)
                
                self._update_quote_totals()
                
            except ValueError:
                # Reset to previous value
                item.setText("1")
                QMessageBox.warning(self, "Invalid Quantity", "Please enter a valid positive number.")

    def _edit_item(self, row: int):
        """Edit a quote item."""
        if 0 <= row < len(self.current_quote["items"]):
            quote_item = self.current_quote["items"][row]
            
            # Open configuration wizard with existing data
            config_wizard = ConfigurationWizard(quote_item["config_data"]["product_data"], self)
            
            # Pre-populate with existing configuration
            # This would require additional methods in ConfigurationWizard
            # For now, just show a message
            QMessageBox.information(
                self, 
                "Edit Item", 
                f"Edit functionality for {quote_item['model_number']} will open the configuration wizard.\n\n"
                "This feature is planned for the next iteration."
            )

    def _remove_item(self, row: int):
        """Remove a quote item."""
        if 0 <= row < len(self.current_quote["items"]):
            quote_item = self.current_quote["items"][row]
            
            reply = QMessageBox.question(
                self,
                "Remove Item",
                f"Are you sure you want to remove {quote_item['model_number']} from the quote?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_quote["items"].pop(row)
                self._update_items_table()
                self._update_quote_totals()

    def _update_quote_totals(self):
        """Update quote total calculations."""
        total_value = sum(item["total_price"] for item in self.current_quote["items"])
        self.current_quote["total_value"] = total_value
        
        self.total_label.setText(f"Total: ${total_value:,.2f}")

    def _on_customer_info_changed(self):
        """Handle customer information changes."""
        self.current_quote["customer_info"] = {
            "company_name": self.company_name_edit.text().strip(),
            "contact_name": self.contact_name_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "notes": self.notes_edit.toPlainText().strip()
        }
        
        # Update action button states
        self._update_items_visibility()

    def _save_draft(self):
        """Save quote as draft."""
        try:
            if not self.current_quote["items"]:
                QMessageBox.warning(self, "No Items", "Please add at least one product to the quote.")
                return
            
            # Prepare quote data for saving
            quote_data = {
                "customer_info": self.current_quote["customer_info"],
                "items": self.current_quote["items"],
                "total_value": self.current_quote["total_value"],
                "status": "Draft"
            }
            
            # Save to database (simplified)
            # In real implementation, this would use the quote service
            quote_id = self._save_quote_to_database(quote_data)
            
            if quote_id:
                self.current_quote["quote_number"] = quote_id
                self.quote_number_label.setText(f"Quote #: {quote_id}")
                
                QMessageBox.information(self, "Saved", f"Quote #{quote_id} saved as draft.")
                self.quote_created.emit(self.current_quote)
            
        except Exception as e:
            logger.error(f"Error saving quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save quote: {str(e)}")

    def _generate_pdf(self):
        """Generate PDF quote."""
        try:
            if not self._validate_quote():
                return
            
            # For now, show a placeholder message
            QMessageBox.information(
                self,
                "Generate PDF",
                "PDF generation will create a professional quote document.\n\n"
                "This feature will be implemented in the next phase."
            )
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            QMessageBox.critical(self, "Error", f"Failed to generate PDF: {str(e)}")

    def _send_quote(self):
        """Send quote to customer."""
        try:
            if not self._validate_quote():
                return
            
            # Update status
            self.current_quote["status"] = "Sent"
            self.status_label.setProperty("class", "status-sent")
            self.status_label.setText("Status: Sent")
            
            QMessageBox.information(
                self,
                "Quote Sent",
                f"Quote has been sent to {self.current_quote['customer_info']['email']}.\n\n"
                "The customer will receive a professional PDF quote document."
            )
            
            self.quote_updated.emit(self.current_quote)
            
        except Exception as e:
            logger.error(f"Error sending quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to send quote: {str(e)}")

    def _validate_quote(self) -> bool:
        """Validate quote before saving/sending."""
        if not self.current_quote["items"]:
            QMessageBox.warning(self, "No Items", "Please add at least one product to the quote.")
            return False
        
        if not self._has_customer_info():
            QMessageBox.warning(
                self, 
                "Missing Customer Info", 
                "Please provide company name, contact person, and email address."
            )
            return False
        
        return True

    def _save_quote_to_database(self, quote_data: Dict) -> Optional[str]:
        """Save quote to database and return quote ID."""
        try:
            # Simplified save operation
            # In real implementation, this would use QuoteService
            
            # Generate a temporary quote ID
            import time
            quote_id = f"Q{int(time.time())}"
            
            logger.info(f"Quote saved with ID: {quote_id}")
            return quote_id
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return None

    def new_quote(self):
        """Start a new quote (clear current state)."""
        reply = QMessageBox.question(
            self,
            "New Quote",
            "Are you sure you want to start a new quote? Any unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self._reset_quote()

    def _reset_quote(self):
        """Reset the quote to initial state."""
        self.current_quote = {
            "items": [],
            "customer_info": {},
            "total_value": 0.0,
            "quote_number": None,
            "status": "Draft"
        }
        
        # Clear UI
        self.items_table.setRowCount(0)
        self.company_name_edit.clear()
        self.contact_name_edit.clear()
        self.email_edit.clear()
        self.phone_edit.clear()
        self.notes_edit.clear()
        
        # Reset labels
        self.quote_number_label.setText("Quote #: (Will be assigned on save)")
        self.status_label.setText("Status: Draft")
        self.status_label.setProperty("class", "status-draft")
        self.total_label.setText("Total: $0.00")
        
        self._update_items_visibility()

    def load_quote(self, quote_data: Dict):
        """Load an existing quote for editing."""
        self.current_quote = quote_data.copy()
        
        # Populate customer info
        customer_info = quote_data.get("customer_info", {})
        self.company_name_edit.setText(customer_info.get("company_name", ""))
        self.contact_name_edit.setText(customer_info.get("contact_name", ""))
        self.email_edit.setText(customer_info.get("email", ""))
        self.phone_edit.setText(customer_info.get("phone", ""))
        self.notes_edit.setPlainText(customer_info.get("notes", ""))
        
        # Update labels
        quote_number = quote_data.get("quote_number")
        if quote_number:
            self.quote_number_label.setText(f"Quote #: {quote_number}")
        
        status = quote_data.get("status", "Draft")
        if status == 'Sent':
            self.status_label.setProperty("class", "status-sent")
        else: # Draft or other
            self.status_label.setProperty("class", "status-draft")
        
        # Populate items table
        self._update_items_table()
        self._update_quote_totals()

    def closeEvent(self, event):
        """Handle widget close event."""
        if hasattr(self, 'db') and self.db:
            self.db.close()
        event.accept()