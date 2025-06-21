# ui/product_configuration.py
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class BabbittStyles:
    """Centralized styling for quick, uniform appearance"""
    
    # Color scheme based on your current orange accent
    COLORS = {
        'primary_dark': '#2c3e50',      # Dark sidebar (similar to current)
        'primary': '#34495e',           # Lighter dark
        'accent': '#f39c12',            # Orange (keeping your current)
        'accent_hover': '#e67e22',      # Darker orange for hover
        'success': '#27ae60',           # Green for success
        'background': '#ffffff',        # White background
        'card_bg': '#f8f9fa',          # Light gray for cards
        'border': '#dee2e6',           # Border color
        'text_primary': '#2c3e50',     # Dark text
        'text_secondary': '#6c757d'    # Gray text
    }
    
    @staticmethod
    def get_main_window_style():
        """Main window styling"""
        return """
            QMainWindow {
                background-color: #ffffff;
            }
        """
    
    @staticmethod
    def get_sidebar_style():
        """Sidebar navigation styling"""
        return f"""
            QWidget#sidebar {{
                background-color: {BabbittStyles.COLORS['primary_dark']};
                min-width: 220px;
                max-width: 220px;
            }}
            QPushButton#sidebarButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton#sidebarButton:hover {{
                background-color: {BabbittStyles.COLORS['primary']};
                border-left: 4px solid {BabbittStyles.COLORS['accent']};
            }}
            QPushButton#sidebarButton:checked {{
                background-color: {BabbittStyles.COLORS['primary']};
                border-left: 4px solid {BabbittStyles.COLORS['accent']};
            }}
        """
    
    @staticmethod
    def get_card_style():
        """Card container styling"""
        return f"""
            QFrame#card {{
                background-color: {BabbittStyles.COLORS['card_bg']};
                border: 1px solid {BabbittStyles.COLORS['border']};
                border-radius: 8px;
                padding: 16px;
                margin: 8px;
            }}
        """
    
    @staticmethod
    def get_button_style():
        """Primary button styling"""
        return f"""
            QPushButton {{
                background-color: {BabbittStyles.COLORS['accent']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {BabbittStyles.COLORS['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: #d68910;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """
    
    @staticmethod
    def get_input_style():
        """Input field styling"""
        return f"""
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                border: 1px solid {BabbittStyles.COLORS['border']};
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 2px solid {BabbittStyles.COLORS['accent']};
                padding: 7px 11px;
            }}
            QTextEdit {{
                border: 1px solid {BabbittStyles.COLORS['border']};
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }}
        """
    
    @staticmethod
    def get_table_style():
        """Table widget styling"""
        return f"""
            QTableWidget {{
                border: 1px solid {BabbittStyles.COLORS['border']};
                gridline-color: {BabbittStyles.COLORS['border']};
                background-color: white;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: {BabbittStyles.COLORS['accent']};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {BabbittStyles.COLORS['card_bg']};
                padding: 8px;
                border: none;
                font-weight: 600;
            }}
        """

class ProductConfigurationWidget(QWidget):
    """Simplified product configuration for quick implementation"""
    
    configuration_changed = Signal(dict)  # Emits when config changes
    
    def __init__(self):
        super().__init__()
        self.current_config = {}
        self.base_price = 425.00  # LS2000 base price from screenshot
        self.setup_ui()
        
    def setup_ui(self):
        # The main layout for this entire widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area to contain all the config options
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }") # Remove scroll area border

        # A container widget for the scroll area's content
        container_widget = QWidget()
        scroll_area.setWidget(container_widget)
        
        layout = QVBoxLayout(container_widget) # Layout for the container
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Configure Product")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Configuration form
        form_widget = self.create_configuration_form()
        layout.addWidget(form_widget)
        
        # Price summary
        self.price_widget = self.create_price_summary()
        layout.addWidget(self.price_widget)
        
        layout.addStretch()
        
        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)
        
    def create_configuration_form(self):
        """Create the main configuration form"""
        form_card = QFrame()
        form_card.setObjectName("card")
        form_card.setStyleSheet(BabbittStyles.get_card_style())
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Accessories section (from your screenshot)
        accessories_label = QLabel("Accessories")
        accessories_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        form_layout.addRow(accessories_label)
        
        # Extra Static Protection
        self.static_protection = QComboBox()
        self.static_protection.addItems(["No", "Yes (+$125)"])
        self.static_protection.setStyleSheet(BabbittStyles.get_input_style())
        self.static_protection.currentIndexChanged.connect(self.update_configuration)
        form_layout.addRow("Extra Static Protection:", self.static_protection)
        
        # Bent Probe
        self.bent_probe = QComboBox()
        self.bent_probe.addItems(["No", "Yes (+$75)"])
        self.bent_probe.setStyleSheet(BabbittStyles.get_input_style())
        self.bent_probe.currentIndexChanged.connect(self.update_configuration)
        form_layout.addRow("Bent Probe:", self.bent_probe)
        
        # Stainless Steel Tag
        self.ss_tag = QComboBox()
        self.ss_tag.addItems(["No", "Yes (+$25)"])
        self.ss_tag.setStyleSheet(BabbittStyles.get_input_style())
        self.ss_tag.currentIndexChanged.connect(self.update_configuration)
        form_layout.addRow("Stainless Steel Tag:", self.ss_tag)
        
        # Connections section
        connections_label = QLabel("Connections")
        connections_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 16px;")
        form_layout.addRow(connections_label)
        
        # Connection Type
        self.connection_type = QComboBox()
        self.connection_type.addItems(["NPT (Standard)", "BSP (+$50)", "Flanged (+$150)"])
        self.connection_type.setStyleSheet(BabbittStyles.get_input_style())
        self.connection_type.currentIndexChanged.connect(self.update_configuration)
        form_layout.addRow("Connection Type:", self.connection_type)
        
        # NPT Size
        self.npt_size = QComboBox()
        self.npt_size.addItems(["3/4\" (Standard)", "1\" (+$25)", "1.5\" (+$50)", "2\" (+$75)"])
        self.npt_size.setStyleSheet(BabbittStyles.get_input_style())
        self.npt_size.currentIndexChanged.connect(self.update_configuration)
        form_layout.addRow("NPT Size:", self.npt_size)
        
        # Electrical section
        electrical_label = QLabel("Electrical")
        electrical_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 16px;")
        form_layout.addRow(electrical_label)
        
        # Voltage
        self.voltage = QComboBox()
        self.voltage.addItems(["115 VAC (Standard)", "230 VAC", "24 VDC (+$75)"])
        self.voltage.setStyleSheet(BabbittStyles.get_input_style())
        self.voltage.currentIndexChanged.connect(self.update_configuration)
        form_layout.addRow("Supply Voltage:", self.voltage)
        
        # Special Options
        special_label = QLabel("Special Options")
        special_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 16px;")
        form_layout.addRow(special_label)
        
        # Time Delay
        self.time_delay = QCheckBox("Add Time Delay (+$150)")
        self.time_delay.stateChanged.connect(self.update_configuration)
        form_layout.addRow("", self.time_delay)
        
        # High Temperature
        self.high_temp = QCheckBox("High Temperature Option (+$200)")
        self.high_temp.stateChanged.connect(self.update_configuration)
        form_layout.addRow("", self.high_temp)
        
        # Quantity
        quantity_label = QLabel("Quantity")
        quantity_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 16px;")
        form_layout.addRow(quantity_label)
        
        self.quantity = QSpinBox()
        self.quantity.setMinimum(1)
        self.quantity.setMaximum(100)
        self.quantity.setValue(1)
        self.quantity.setStyleSheet(BabbittStyles.get_input_style())
        self.quantity.valueChanged.connect(self.update_configuration)
        form_layout.addRow("Quantity:", self.quantity)
        
        form_card.setLayout(form_layout)
        return form_card
        
    def create_price_summary(self):
        """Create price summary widget"""
        price_card = QFrame()
        price_card.setObjectName("card")
        price_card.setStyleSheet(BabbittStyles.get_card_style() + """
            QFrame#card {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Price Summary")
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        layout.addWidget(title)
        
        # Price breakdown
        self.price_breakdown = QLabel()
        self.price_breakdown.setWordWrap(True)
        layout.addWidget(self.price_breakdown)
        
        # Total
        self.total_label = QLabel()
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-top: 12px;")
        layout.addWidget(self.total_label)
        
        price_card.setLayout(layout)
        
        # Initialize with base price
        self.update_price_display()
        
        return price_card
        
    def update_configuration(self):
        """Update configuration and pricing when any option changes"""
        # Build configuration dictionary
        self.current_config = {
            'base_model': 'LS2000',
            'static_protection': self.static_protection.currentText().startswith("Yes"),
            'bent_probe': self.bent_probe.currentText().startswith("Yes"),
            'ss_tag': self.ss_tag.currentText().startswith("Yes"),
            'connection_type': self.connection_type.currentText(),
            'npt_size': self.npt_size.currentText(),
            'voltage': self.voltage.currentText(),
            'time_delay': self.time_delay.isChecked(),
            'high_temp': self.high_temp.isChecked(),
            'quantity': self.quantity.value()
        }
        
        # Update price display
        self.update_price_display()
        
        # Emit signal for other components
        self.configuration_changed.emit(self.current_config)
        
    def update_price_display(self):
        """Calculate and display updated pricing"""
        # Base price
        unit_price = self.base_price
        breakdown = [f"Base Model (LS2000): ${self.base_price:.2f}"]
        
        # Add accessory costs
        if self.static_protection.currentText().startswith("Yes"):
            unit_price += 125
            breakdown.append("Extra Static Protection: +$125.00")
            
        if self.bent_probe.currentText().startswith("Yes"):
            unit_price += 75
            breakdown.append("Bent Probe: +$75.00")
            
        if self.ss_tag.currentText().startswith("Yes"):
            unit_price += 25
            breakdown.append("Stainless Steel Tag: +$25.00")
            
        # Connection costs
        if "BSP" in self.connection_type.currentText():
            unit_price += 50
            breakdown.append("BSP Connection: +$50.00")
        elif "Flanged" in self.connection_type.currentText():
            unit_price += 150
            breakdown.append("Flanged Connection: +$150.00")
            
        # NPT size costs
        if "1\"" in self.npt_size.currentText() and "1.5\"" not in self.npt_size.currentText():
            unit_price += 25
            breakdown.append("1\" NPT: +$25.00")
        elif "1.5\"" in self.npt_size.currentText():
            unit_price += 50
            breakdown.append("1.5\" NPT: +$50.00")
        elif "2\"" in self.npt_size.currentText():
            unit_price += 75
            breakdown.append("2\" NPT: +$75.00")
            
        # Voltage options
        if "24 VDC" in self.voltage.currentText():
            unit_price += 75
            breakdown.append("24 VDC Power: +$75.00")
            
        # Special options
        if self.time_delay.isChecked():
            unit_price += 150
            breakdown.append("Time Delay: +$150.00")
            
        if self.high_temp.isChecked():
            unit_price += 200
            breakdown.append("High Temperature: +$200.00")
            
        # Calculate total
        quantity = self.quantity.value()
        total = unit_price * quantity
        
        # Update display
        self.price_breakdown.setText("\n".join(breakdown))
        
        if quantity > 1:
            self.total_label.setText(f"Unit Price: ${unit_price:.2f}\nQuantity: {quantity}\nTotal: ${total:.2f}")
        else:
            self.total_label.setText(f"Total: ${total:.2f}")
            
    def get_configuration_summary(self):
        """Get configuration summary for quote generation"""
        config = self.current_config.copy()
        
        # Calculate pricing
        unit_price = self.calculate_unit_price()
        total_price = unit_price * config['quantity']
        
        # Build readable configuration description
        description_parts = ["LS2000 Level Switch"]
        
        if config['static_protection']:
            description_parts.append("Extra Static Protection")
        if config['bent_probe']:
            description_parts.append("Bent Probe")
        if config['ss_tag']:
            description_parts.append("Stainless Steel Tag")
            
        # Create summary
        return {
            'product': 'LS2000',
            'description': ", ".join(description_parts),
            'configuration': config,
            'unit_price': unit_price,
            'quantity': config['quantity'],
            'total_price': total_price
        }
        
    def calculate_unit_price(self):
        """Calculate unit price based on current configuration"""
        price = self.base_price
        
        if self.current_config.get('static_protection'):
            price += 125
        if self.current_config.get('bent_probe'):
            price += 75
        if self.current_config.get('ss_tag'):
            price += 25
            
        # Add other costs based on configuration...
        # (Same logic as update_price_display)
        
        return price