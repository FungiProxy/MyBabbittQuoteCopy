"""
Quote Summary Tab for the Babbitt Quote Generator.

This module defines the quote management interface for the quote generator.
It provides a comprehensive view of the quote being built, including:
- Product configuration summary
- Quote items list (products and spare parts)
- Pricing calculations and display
- Customer information collection

The tab serves as the central location for reviewing and finalizing quotes
before they are saved or exported.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QGroupBox, QFormLayout, QSpacerItem,
    QSizePolicy, QPushButton, QTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer
from src.core.database import SessionLocal
from src.core.models.connection_option import ConnectionOption


class QuoteTab(QWidget):
    """
    Quote management tab for the quote generator.
    
    This tab provides a comprehensive interface for managing quotes, including
    product configuration review, pricing calculations, and customer information
    collection. It maintains the current state of the quote and updates
    automatically as changes are made in other tabs.
    
    The tab is organized into sections:
    1. Quote Summary: Shows selected product and configuration
    2. Quote Items: Lists all products and spare parts in the quote
    3. Pricing: Displays calculated prices and totals
    4. Customer Information: Collects customer details
    
    Attributes:
        product_info (dict): Current product information
        specs (dict): Current product specifications
        pricing (dict): Current pricing calculations
        product_summary (QLabel): Label showing selected product
        specs_table (QTableWidget): Table showing product configuration
        items_table (QTableWidget): Table showing quote items
        status_label (QLabel): Label for status messages
        base_price_label (QLabel): Label showing base price
        options_price_label (QLabel): Label showing options price
        total_price_label (QLabel): Label showing total price
        customer_name (QLineEdit): Input for customer name
        contact_name (QLineEdit): Input for contact person
        email (QLineEdit): Input for email address
        phone (QLineEdit): Input for phone number
        notes (QTextEdit): Input for additional notes
    
    Signals:
        customer_updated (dict): Emitted when customer information changes
    """
    
    # Signals
    customer_updated = Signal(dict)  # customer information dictionary
    
    def __init__(self, parent=None):
        """
        Initialize the QuoteTab.
        
        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.init_ui()
        
        # Initialize data structures
        self.product_info = {}
        self.specs = {}
        self.pricing = {
            "base_price": 0.0,
            "options_price": 0.0,
            "total_price": 0.0
        }
    
    def init_ui(self):
        """
        Initialize the UI components.
        
        Sets up the tab's layout with four main sections:
        1. Quote Summary: Product and configuration details
        2. Quote Items: Table of products and spare parts
        3. Pricing: Price breakdown and totals
        4. Customer Information: Form for customer details
        """
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create summary section
        summary_group = QGroupBox("Quote Summary")
        summary_layout = QVBoxLayout()
        
        # Product summary
        self.product_summary = QLabel("No product selected")
        self.product_summary.setStyleSheet("font-weight: bold;")
        self.product_summary.setFont(QFont("Arial", 10))
        summary_layout.addWidget(self.product_summary)
        
        # Configuration summary
        self.specs_table = QTableWidget(0, 2)
        self.specs_table.setHorizontalHeaderLabels(["Configuration Item", "Value"])
        self.specs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.specs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.specs_table.verticalHeader().setVisible(False)
        summary_layout.addWidget(self.specs_table)
        
        summary_group.setLayout(summary_layout)
        main_layout.addWidget(summary_group)

        # Create quote items section
        items_group = QGroupBox("Quote Items")
        items_layout = QVBoxLayout()
        
        # Items table (products and spare parts)
        self.items_table = QTableWidget(0, 4)
        self.items_table.setHorizontalHeaderLabels(["Description", "Quantity", "Unit Price", "Total"])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.items_table.verticalHeader().setVisible(False)
        items_layout.addWidget(self.items_table)
        
        # Status label for notifications
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #08D13F; font-weight: bold;")
        self.status_label.setFont(QFont("Arial", 10))
        items_layout.addWidget(self.status_label)
        
        items_group.setLayout(items_layout)
        main_layout.addWidget(items_group)
        
        # Create pricing section
        pricing_group = QGroupBox("Pricing")
        pricing_layout = QFormLayout()
        
        self.base_price_label = QLabel("$0.00")
        pricing_layout.addRow("Base Price:", self.base_price_label)
        
        self.options_price_label = QLabel("$0.00")
        pricing_layout.addRow("Options:", self.options_price_label)
        
        self.total_price_label = QLabel("$0.00")
        font = QFont()
        font.setBold(True)
        self.total_price_label.setFont(font)
        pricing_layout.addRow("Total Price:", self.total_price_label)
        
        pricing_group.setLayout(pricing_layout)
        main_layout.addWidget(pricing_group)
        
        # Create customer information section
        customer_group = QGroupBox("Customer Information")
        customer_layout = QFormLayout()
        
        self.customer_name = QLineEdit()
        customer_layout.addRow("Customer Name:", self.customer_name)
        
        self.contact_name = QLineEdit()
        customer_layout.addRow("Contact Person:", self.contact_name)
        
        self.email = QLineEdit()
        customer_layout.addRow("Email:", self.email)
        
        self.phone = QLineEdit()
        customer_layout.addRow("Phone:", self.phone)
        
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(100)
        customer_layout.addRow("Notes:", self.notes)
        
        customer_group.setLayout(customer_layout)
        main_layout.addWidget(customer_group)
        
        # Connect signals
        self.customer_name.textChanged.connect(self.on_customer_info_changed)
        self.contact_name.textChanged.connect(self.on_customer_info_changed)
        self.email.textChanged.connect(self.on_customer_info_changed)
        self.phone.textChanged.connect(self.on_customer_info_changed)
        self.notes.textChanged.connect(self.on_customer_info_changed)
        
        # Add spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def update_product_info(self, product_info):
        """
        Update the product information display.
        
        Updates the product summary section with new product information
        and triggers a pricing update.
        
        Args:
            product_info (dict): Dictionary containing product information:
                - model (str): Product model number
                - application (str): Product application
        """
        self.product_info = product_info
        
        # Update product summary label
        model = product_info.get("model", "")
        application = product_info.get("application", "")
        
        if model:
            self.product_summary.setFont(QFont("Arial", 10))
            self.product_summary.setText(f"<b>{model}</b><br>Application: {application}")
        else:
            self.product_summary.setFont(QFont("Arial", 10))
            self.product_summary.setText("No product selected")
        
        # Update pricing
        self.update_pricing()
    
    def update_specifications(self, specs):
        """
        Update the specifications display.
        
        Updates the specifications table with new configuration information,
        organizing specs into logical categories for better readability.
        
        Args:
            specs (dict): Dictionary containing product specifications
        """
        self.specs = specs
        
        # Clear existing specs
        self.specs_table.setRowCount(0)
        
        # Group configuration items by category
        config_categories = {
            "Essential Properties": ["voltage", "material", "material_type", "viscosity"],
            "Dimensions": ["probe_length", "indicator_length", "cable_length"],
            "Connections": ["connection", "mounting"],
            "Material Options": ["exotic_metals", "oring"],
            "Housing": ["housing"],
            "Additional Features": ["high_temp", "extended_probe", "remote_display", "output_type"]
        }
        
        # Add category headers and specs in each category
        for category, spec_keys in config_categories.items():
            category_added = False
            
            for name in spec_keys:
                if name in specs:
                    # Add category header if this is the first spec in the category
                    if not category_added:
                        self._add_category_row(category)
                        category_added = True
                    
                    # Convert internal name to display name
                    display_name = name.replace("_", " ").title()
                    
                    # Format value for display
                    value = specs[name]
                    if isinstance(value, bool):
                        display_value = "Yes" if value else "No"
                    else:
                        display_value = str(value)
                    
                    # Add to table
                    self._add_spec_row(display_name, display_value)
        
        # Update pricing
        self.update_pricing()
    
    def _add_category_row(self, category_name):
        """
        Add a category header row to the specifications table.
        
        Args:
            category_name (str): Name of the category to add
        """
        row = self.specs_table.rowCount()
        self.specs_table.insertRow(row)
        
        category_item = QTableWidgetItem(category_name)
        category_item.setBackground(Qt.lightGray)
        
        font = QFont("Arial", 9)
        font.setBold(True)
        category_item.setFont(font)
        
        # Span both columns
        self.specs_table.setItem(row, 0, category_item)
        self.specs_table.setSpan(row, 0, 1, 2)
    
    def _add_spec_row(self, name, value):
        """
        Add a specification row to the specifications table.
        
        Args:
            name (str): Name of the specification
            value (str): Value of the specification
        """
        row = self.specs_table.rowCount()
        self.specs_table.insertRow(row)
        
        # Add indent to name for better visual hierarchy
        name_item = QTableWidgetItem("    " + name)
        value_item = QTableWidgetItem(value)
        
        font = QFont("Arial", 9)
        name_item.setFont(font)
        value_item.setFont(font)
        
        self.specs_table.setItem(row, 0, name_item)
        self.specs_table.setItem(row, 1, value_item)
    
    def update_pricing(self):
        """
        Update pricing calculations.
        
        Calculates and updates the display of base price, options price,
        and total price based on the current product and specifications.
        This is currently using placeholder calculations and would normally
        integrate with a proper pricing module.
        """
        # Base price based on product model
        base_price = 0.0
        model = self.product_info.get("model", "")
        
        # Set base prices for each model
        model_prices = {
            "LS2000": 800.0,  # General Purpose
            "LS2100": 700.0,  # Loop Powered
            "LS6000": 900.0,  # Heavy Duty
            "LS7000": 1200.0, # Advanced Features
            "LS7000/2": 1500.0, # Dual Point
            "LS8000": 1100.0, # Remote Mounted
            "LS8000/2": 1400.0, # Remote Mounted Dual Point
            "LT9000": 1800.0,  # Level Transmitter
            "FS10000": 950.0   # Flow Switch
        }
        
        # Get base price for the model
        base_model = model.split()[0]  # Get just the model number without description
        base_price = model_prices.get(base_model, 0.0)
        
        # Options price based on specifications
        options_price = 0.0
        
        # Add costs for each option
        for name, value in self.specs.items():
            # Material upgrades
            if name == "material":
                if "Hastelloy" in value:
                    options_price += 400.0
                elif "Aluminum" in value:
                    options_price += 50.0
                
            # Exotic metals
            if name == "exotic_metals":
                if "Titanium" in value:
                    options_price += 600.0
                elif "Monel" in value:
                    options_price += 500.0
            
            # Special O-rings
            if name == "oring":
                if "Kalrez" in value:
                    options_price += 120.0
                elif "PTFE" in value:
                    options_price += 80.0
                elif "EPDM" in value:
                    options_price += 40.0
            
            # Housing options
            if name == "housing":
                if "Explosion-Proof" in value:
                    options_price += 300.0
                elif "Stainless Steel" in value:
                    options_price += 200.0
            
            # Feature options
            if name == "high_temp" and value:
                options_price += 150.0
            elif name == "extended_probe" and value:
                options_price += 100.0
            elif name == "remote_display" and value:
                options_price += 250.0
            
            # Output type options (for transmitters)
            if name == "output_type":
                if "HART" in value:
                    options_price += 300.0
                elif "Modbus RTU" in value:
                    options_price += 250.0
                
            # Length options
            if name == "probe_length" and isinstance(value, (int, float)):
                # Add cost for longer probes
                standard_length = 10  # Standard length is 10" for most models
                if base_model in ["LS2000", "LS2100"] and value > standard_length:
                    options_price += (value - standard_length) * 8.0  # $8 per inch over standard
                elif value > standard_length:
                    options_price += (value - standard_length) * 12.0  # $12 per inch over standard for other models
            
            if name == "cable_length" and isinstance(value, (int, float)):
                # Add cost for longer cables
                standard_cable = 10  # Standard cable length is 10 feet
                if value > standard_cable:
                    options_price += (value - standard_cable) * 5.0  # $5 per foot over standard
        
        # Add connection option price
        db = SessionLocal()
        try:
            connection_type = self.specs.get("connection_type")
            if connection_type == "Flange":
                rating = self.specs.get("flange_rating")
                size = self.specs.get("flange_size")
                option = db.query(ConnectionOption).filter_by(type="Flange", rating=rating, size=size).first()
                if option:
                    options_price += option.price
            elif connection_type == "Tri-Clamp":
                size = self.specs.get("triclamp_size")
                option = db.query(ConnectionOption).filter_by(type="Tri-Clamp", size=size).first()
                if option:
                    options_price += option.price
        finally:
            db.close()
        
        # Calculate total
        total_price = base_price + options_price
        
        # Update pricing data
        self.pricing = {
            "base_price": base_price,
            "options_price": options_price,
            "total_price": total_price
        }
        
        # Update the UI
        self.base_price_label.setText(f"${base_price:.2f}")
        self.options_price_label.setText(f"${options_price:.2f}")
        self.total_price_label.setText(f"${total_price:.2f}")
    
    def on_customer_info_changed(self):
        """Handle changes to customer information."""
        customer_data = {
            "name": self.customer_name.text(),
            "contact": self.contact_name.text(),
            "email": self.email.text(),
            "phone": self.phone.text(),
            "notes": self.notes.toPlainText()
        }
        
        # Emit signal with updated customer info
        self.customer_updated.emit(customer_data)
    
    def get_quote_data(self):
        """Get all data for the current quote."""
        return {
            "product": self.product_info,
            "specifications": self.specs,
            "pricing": self.pricing,
            "customer": {
                "name": self.customer_name.text(),
                "contact": self.contact_name.text(),
                "email": self.email.text(),
                "phone": self.phone.text(),
                "notes": self.notes.toPlainText()
            }
        }

    def add_spare_part_to_quote(self, part_info):
        """Add a spare part or product to the quote."""
        # Check item type (product or spare part)
        item_type = part_info.get('type', 'spare_part')
        
        # Create a description string
        if item_type == 'product':
            description = part_info['description']
            item_name = part_info['name']
            notification_text = f"Added product: {item_name}"
            
            # If it's a product, also update the product summary and specifications
            product_info = {
                "model": part_info['name'],
                "category": part_info['description'].split(' - ')[1] if ' - ' in part_info['description'] else "",
                "application": part_info.get('application', "General Purpose")
            }
            self.update_product_info(product_info)
            
            # Update specifications if they're included
            if 'specifications' in part_info:
                self.update_specifications(part_info['specifications'])
        else:
            description = f"{part_info['name']} - {part_info['part_number']}"
            notification_text = f"Added spare part: {part_info['name']}"
        
        # Create a new row in the quote items table
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        
        # Set the item description and price
        desc_item = QTableWidgetItem(description)
        qty_item = QTableWidgetItem("1")  # Quantity
        unit_price_item = QTableWidgetItem(f"${part_info['price']:.2f}")
        total_price_item = QTableWidgetItem(f"${part_info['price']:.2f}")
        
        # Use standard font to avoid DirectWrite font issues
        font = QFont("Arial", 9)
        desc_item.setFont(font)
        qty_item.setFont(font)
        unit_price_item.setFont(font)
        total_price_item.setFont(font)
        
        self.items_table.setItem(row, 0, desc_item)
        self.items_table.setItem(row, 1, qty_item)
        self.items_table.setItem(row, 2, unit_price_item)
        self.items_table.setItem(row, 3, total_price_item)
        
        # Store part info in the row
        self.items_table.item(row, 0).setData(Qt.UserRole, part_info)
        
        # Update total pricing
        self.update_total_pricing()
        
        # Show a brief notification
        self.status_label.setText(notification_text)
        QTimer.singleShot(3000, lambda: self.status_label.setText(""))

    def update_total_pricing(self):
        """Update total pricing including spare parts."""
        # Calculate base product price from current pricing
        base_price = self.pricing.get("base_price", 0.0)
        options_price = self.pricing.get("options_price", 0.0)
        
        # Calculate additional items price
        items_price = 0.0
        for row in range(self.items_table.rowCount()):
            item_data = self.items_table.item(row, 0).data(Qt.UserRole)
            if item_data:
                quantity = int(self.items_table.item(row, 1).text())
                unit_price = item_data.get("price", 0.0)
                items_price += quantity * unit_price
        
        # Update total price
        total_price = base_price + options_price + items_price
        
        # Update pricing data
        self.pricing["items_price"] = items_price
        self.pricing["total_price"] = total_price
        
        # Update UI with standard fonts
        font = QFont("Arial", 9)
        self.base_price_label.setFont(font)
        self.options_price_label.setFont(font)
        
        bold_font = QFont("Arial", 10)
        bold_font.setBold(True)
        self.total_price_label.setFont(bold_font)
        
        self.base_price_label.setText(f"${base_price:.2f}")
        self.options_price_label.setText(f"${options_price:.2f}")
        self.total_price_label.setText(f"${total_price:.2f}") 