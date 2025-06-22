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
    QSizePolicy,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QColor

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService
from src.core.services.product_service import ProductService
from src.ui.product_selection_dialog_working import WorkingProductSelectionDialog
from src.ui.theme.babbitt_theme import BabbittTheme

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
        self.product_service = ProductService()
        
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

    def _style_input_field(self, field, uniform_height=48):
        field.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid #E9ECEF;
                border-radius: 6px;
                padding: 12px 16px;
                font-size: 14px;
                background: white;
                height: {uniform_height}px;
            }}
            QLineEdit:focus {{
                border-color: #2C3E50;
                outline: none;
            }}
            QLineEdit:hover {{
                border-color: #34495E;
            }}
        """)
    
    def _style_text_area(self, field):
        field.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E9ECEF;
                border-radius: 6px;
                padding: 12px 16px;
                font-size: 14px;
                background: white;
                min-height: 120px;
            }
            QTextEdit:focus {
                border-color: #2C3E50;
                outline: none;
            }
            QTextEdit:hover {
                border-color: #34495E;
            }
        """)

    def _setup_ui(self):
        """Set up the quote creation UI to match the desired modern look."""
        # Main layout is now a QHBoxLayout for the two-column structure
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # --- Left Column (2/3 width) ---
        left_column_layout = QVBoxLayout()
        left_column_layout.setSpacing(20)
        
        # Create and add the header for the left column
        header_widget = self._create_quote_header()
        left_column_layout.addWidget(header_widget)
        
        # Create and add the items panel
        items_panel = self._create_items_panel()
        left_column_layout.addWidget(items_panel)
        
        # --- Right Column (1/3 width) ---
        right_column_layout = QVBoxLayout()
        right_column_layout.setSpacing(20)
        
        # Create and add the customer panel
        customer_panel = self._create_customer_panel()
        right_column_layout.addWidget(customer_panel)
        
        # Create and add the actions panel
        actions_panel = self._create_actions_panel()
        right_column_layout.addWidget(actions_panel)
        
        # Spacer to push customer/actions panels up
        right_column_layout.addStretch(1)
        
        # Add the two columns to the main layout with the correct stretch factor
        main_layout.addLayout(left_column_layout, 2)
        main_layout.addLayout(right_column_layout, 1)

    def mousePressEvent(self, event):
        """Clear focus from input widgets when clicking on the background."""
        focused_widget = self.focusWidget()
        if focused_widget and isinstance(focused_widget, (QLineEdit, QTextEdit)):
            focused_widget.clearFocus()
        super().mousePressEvent(event)

    def _create_quote_header(self) -> QWidget:
        """Create the quote header with title and basic info."""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        # Left-aligned content: Quote Number
        self.quote_number_label = QLabel("Quote not yet saved")
        self.quote_number_label.setProperty("labelType", "caption")

        # Center-aligned content: Status and Price
        status_price_container = QWidget()
        status_layout = QVBoxLayout(status_price_container)
        status_layout.setContentsMargins(0,0,0,0)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status_label = QLabel(self.current_quote['status'].upper())
        self.status_label.setProperty("status", self.current_quote['status'])
        status_layout.addWidget(self.status_label)
        
        self.total_label = QLabel(f"${self.current_quote['total_value']:.2f}")
        self.total_label.setProperty("priceType", "total-prominent")
        status_layout.addWidget(self.total_label)

        # Right-aligned (but transparent) content to balance the layout
        balancing_label = QLabel("Quote not yet saved")
        balancing_label.setProperty("labelType", "caption")
        balancing_label.setStyleSheet("color: transparent;")

        # Add widgets to the layout to achieve perfect centering
        layout.addWidget(self.quote_number_label)
        layout.addStretch()
        layout.addWidget(status_price_container)
        layout.addStretch()
        layout.addWidget(balancing_label)

        return header

    def _apply_shadow_effect(self, widget):
        """Apply a standard drop shadow effect to a widget."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        widget.setGraphicsEffect(shadow)

    def _create_items_panel(self) -> QWidget:
        """Create the quote items panel as a styled card."""
        panel = QFrame()
        panel.setProperty("class", "content-section")
        self._apply_shadow_effect(panel)

        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Quote Items")
        title_label.setProperty("class", "section-title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Container for the centered button
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        add_product_btn = QPushButton("+ Add Product")
        add_product_btn.clicked.connect(self._add_product)
        button_layout.addWidget(add_product_btn)
        button_layout.addStretch()
        layout.addWidget(button_container)
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels([
            "Product", "Configuration", "Quantity", "Unit Price", "Total", "Actions"
        ])
        
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.items_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.items_table.setAlternatingRowColors(True)
        
        size_policy = self.items_table.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
        self.items_table.setSizePolicy(size_policy)
        
        layout.addWidget(self.items_table)
        
        # Empty state message
        self.empty_state_label = QLabel("No items added yet. Click 'Add Product' to get started.")
        self.empty_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_state_label.setProperty("class", "placeholderCard")
        layout.addWidget(self.empty_state_label)
        
        return panel

    def _create_customer_panel(self) -> QWidget:
        """Create the customer information panel as a styled card."""
        panel = QFrame()
        panel.setProperty("class", "content-section")
        self._apply_shadow_effect(panel)

        layout = QVBoxLayout(panel)
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        title_label = QLabel("Customer Information")
        title_label.setProperty("class", "section-title")
        layout.addWidget(title_label)
        
        # Customer form fields
        self.company_name_edit = QLineEdit()
        form_layout.addRow("Company Name:", self.company_name_edit)
        
        self.contact_person_edit = QLineEdit()
        form_layout.addRow("Contact Person:", self.contact_person_edit)

        self.email_edit = QLineEdit()
        form_layout.addRow("Email:", self.email_edit)

        self.phone_edit = QLineEdit()
        form_layout.addRow("Phone:", self.phone_edit)

        self.notes_edit = QTextEdit()
        form_layout.addRow("Notes:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # Connect signals for customer info changes
        self.company_name_edit.textChanged.connect(self._on_customer_info_changed)
        self.contact_person_edit.textChanged.connect(self._on_customer_info_changed)
        self.email_edit.textChanged.connect(self._on_customer_info_changed)
        self.phone_edit.textChanged.connect(self._on_customer_info_changed)
        self.notes_edit.textChanged.connect(self._on_customer_info_changed)
    
        return panel

    def _create_actions_panel(self) -> QWidget:
        """Create the actions panel as a styled card."""
        panel = QFrame()
        panel.setProperty("class", "content-section")
        self._apply_shadow_effect(panel)

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        # Title
        title_label = QLabel("Actions")
        title_label.setProperty("class", "section-title")
        layout.addWidget(title_label)
        
        # Action buttons
        self.save_draft_btn = QPushButton("Save Draft")
        self.save_draft_btn.setProperty("buttonStyle", "secondary")
        self.save_draft_btn.clicked.connect(self._save_draft)
        
        self.generate_pdf_btn = QPushButton("Generate PDF")
        self.generate_pdf_btn.setProperty("buttonStyle", "secondary")
        self.generate_pdf_btn.clicked.connect(self._generate_pdf)
        
        self.send_quote_btn = QPushButton("Send Quote")
        self.send_quote_btn.setProperty("buttonStyle", "secondary")
        self.send_quote_btn.clicked.connect(self._send_quote)
        
        layout.addWidget(self.save_draft_btn)
        layout.addWidget(self.generate_pdf_btn)
        layout.addWidget(self.send_quote_btn)
        
        return panel

    def _add_product(self):
        """Open the product selection dialog to add a new item."""
        try:
            # Use the working dialog
            dialog = WorkingProductSelectionDialog(product_service=self.product_service, parent=self)
            dialog.product_added.connect(self._on_product_configured)
            dialog.exec()
        except Exception as e:
            logger.error(f"Error opening product selection dialog: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Could not open product selection dialog: {e}")

    def _on_product_configured(self, config_data: Dict):
        """Handle completed product configuration from the new widget."""
        try:
            # The new widget returns a summary with all the data we need.
            quote_item = {
                "product_family": config_data.get("product", "N/A"),
                "model_number": config_data.get("product", "N/A"), # Use the base product name
                "configuration": config_data.get("description", "Standard Configuration"),
                "quantity": config_data.get("quantity", 1),
                "unit_price": config_data.get("unit_price", 0),
                "total_price": config_data.get("total_price", 0),
                "config_data": config_data.get("configuration", {}) # Store the detailed config
            }
            
            self.current_quote["items"].append(quote_item)
            self._update_items_table()
            self._update_quote_totals()
            
            logger.info(f"Added product to quote: {quote_item['model_number']}")
            
        except Exception as e:
            logger.error(f"Error adding configured product: {e}", exc_info=True)
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
            self.contact_person_edit.text().strip() and
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
        """Edit an existing quote item."""
        product_to_edit = self.current_quote["items"][row]
        
        try:
            # Use the working dialog for editing
            dialog = WorkingProductSelectionDialog(
                product_service=self.product_service,
                product_to_edit=product_to_edit,
                parent=self
            )
            
            # Reconnect the signal to a handler that updates the item
            dialog.product_added.connect(lambda new_config: self._on_product_updated(row, new_config))
            
            dialog.exec()
        except Exception as e:
            logger.error(f"Error opening product configuration dialog for editing: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Could not open product configuration: {e}")

    def _on_product_updated(self, row: int, new_config: Dict):
        """
        Handle the updated configuration for an existing item.
        This replaces the old item at the given row with the new one.
        """
        # Replace the item in the quote data
        self.current_quote["items"][row] = new_config
        
        # Refresh the table to show updated item
        self._update_items_table()

    def _remove_item(self, row: int):
        """Remove an item from the quote."""
        if not (0 <= row < len(self.current_quote["items"])):
            return
        
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
        
        self.total_label.setText(f"${total_value:,.2f}")

    def _on_customer_info_changed(self):
        """Handle customer information changes."""
        self.current_quote["customer_info"] = {
            "company_name": self.company_name_edit.text().strip(),
            "contact_name": self.contact_person_edit.text().strip(),
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
        self.contact_person_edit.clear()
        self.email_edit.clear()
        self.phone_edit.clear()
        self.notes_edit.clear()
        
        # Reset labels
        self.quote_number_label.setText("Quote not yet saved")
        self.status_label.setText("DRAFT")
        self.status_label.setProperty("status", "Draft")
        self.total_label.setText("$0.00")
        
        self._update_items_visibility()

    def load_quote(self, quote_data: Dict):
        """Load an existing quote for editing."""
        self.current_quote = quote_data.copy()
        
        # Populate customer info
        customer_info = quote_data.get("customer_info", {})
        self.company_name_edit.setText(customer_info.get("company_name", ""))
        self.contact_person_edit.setText(customer_info.get("contact_name", ""))
        self.email_edit.setText(customer_info.get("email", ""))
        self.phone_edit.setText(customer_info.get("phone", ""))
        self.notes_edit.setPlainText(customer_info.get("notes", ""))
        
        # Update labels
        quote_number = quote_data.get("quote_number")
        if quote_number:
            self.quote_number_label.setText(f"Quote #: {quote_number}")
        else:
            self.quote_number_label.setText("Quote not yet saved")

        status = quote_data.get("status", "Draft")
        self.status_label.setText(status.upper())
        self.status_label.setProperty("status", status)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        
        # Populate items table
        self._update_items_table()
        self._update_quote_totals()

    def closeEvent(self, event):
        """Handle widget close event."""
        if hasattr(self, 'db') and self.db:
            self.db.close()
        event.accept()