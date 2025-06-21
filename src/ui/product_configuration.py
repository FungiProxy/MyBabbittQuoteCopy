"""
Product Configuration Widget

A comprehensive product configuration widget that integrates with the existing
product service and configuration service to provide a working product configuration
interface.
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QPushButton,
    QFrame,
    QScrollArea,
    QGroupBox,
    QButtonGroup,
    QRadioButton,
    QCheckBox,
    QLineEdit,
    QMessageBox,
)

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from src.ui.theme.babbitt_theme import BabbittTheme

logger = logging.getLogger(__name__)


class ProductConfigurationWidget(QWidget):
    """
    Product configuration widget that provides a working interface for
    configuring Babbitt International products.
    
    Features:
    - Dynamic option loading from database
    - Real-time pricing updates
    - Material and voltage selection
    - Additional options configuration
    - Length-based pricing
    - Professional styling
    """
    
    configuration_changed = Signal(dict)  # Emitted when configuration changes
    
    def __init__(self, product_data: Optional[Dict] = None, parent=None):
        super().__init__(parent)
        self.product_data = product_data or {}
        self.db = SessionLocal()
        self.product_service = ProductService()
        self.config_service = ConfigurationService(self.db, self.product_service)
        
        # Configuration state
        self.current_config = {}
        self.available_options = {}
        self.option_widgets = {}
        
        # Base price from product data
        self.base_price = self.product_data.get('base_price', 0.0)
        
        self._setup_ui()
        self._load_product_configuration()
        
    def __del__(self):
        """Clean up database connection."""
        if hasattr(self, 'db') and self.db:
            self.db.close()
    
    def _setup_ui(self):
        """Set up the main UI layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("Configure Product")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title)
        
        # Scrollable configuration area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.config_container = QWidget()
        self.config_layout = QVBoxLayout(self.config_container)
        self.config_layout.setSpacing(16)
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(self.config_container)
        main_layout.addWidget(scroll_area)
        
        # Price summary
        self.price_widget = self._create_price_summary()
        main_layout.addWidget(self.price_widget)
        
        # Add to Quote button
        self.add_button = QPushButton("Add to Quote")
        self.add_button.setStyleSheet(BabbittTheme.get_button_style())
        self.add_button.clicked.connect(self._on_add_to_quote)
        self.add_button.setMinimumHeight(45)
        main_layout.addWidget(self.add_button)
        
        # Apply theme styling
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
    
    def _create_price_summary(self) -> QFrame:
        """Create the price summary widget."""
        price_card = QFrame()
        price_card.setObjectName("card")
        price_card.setStyleSheet("""
            QFrame#card {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(price_card)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Price Summary")
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        layout.addWidget(title)
        
        # Price breakdown
        self.price_breakdown = QLabel()
        self.price_breakdown.setWordWrap(True)
        self.price_breakdown.setStyleSheet("color: #2c3e50; font-size: 14px;")
        layout.addWidget(self.price_breakdown)
        
        # Total
        self.total_label = QLabel()
        self.total_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #ea580c;
            padding: 8px 12px;
            background-color: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 6px;
        """)
        layout.addWidget(self.total_label)
        
        return price_card
    
    def _load_product_configuration(self):
        """Load and display product configuration options."""
        if not self.product_data:
            logger.warning("No product data provided for configuration")
            return
        
        family_name = self.product_data.get('family_name', self.product_data.get('name', ''))
        if not family_name:
            logger.warning("No product family name found in product data")
            return
        
        try:
            # Start configuration session
            self.config_service.start_configuration(
                product_family_id=self.product_data.get('id', 1),
                product_family_name=family_name,
                base_product_info=self.product_data
            )
            
            # Load available options
            self.available_options = self.product_service.get_additional_options(self.db, family_name)
            
            # Create configuration sections
            self._create_core_options_section()
            self._create_additional_options_sections()
            self._create_quantity_section()
            
            # Update pricing
            self._update_price_display()
            
        except Exception as e:
            logger.error(f"Error loading product configuration: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to load product configuration: {e}")
    
    def _create_core_options_section(self):
        """Create core options section (Material, Voltage)."""
        group = QGroupBox("Core Configuration")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                color: #2C3E50;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                background-color: white;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 20, 16, 16)
        
        # Material selection
        material_options = [opt for opt in self.available_options if opt.get('category') == 'Material']
        if material_options:
            self.material_combo = QComboBox()
            self.material_combo.setStyleSheet("""
                QComboBox {
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    padding: 8px;
                    min-height: 20px;
                    background-color: white;
                }
                QComboBox:focus {
                    border-color: #2C3E50;
                }
            """)
            
            material_option = material_options[0]
            choices = material_option.get('choices', [])
            adders = material_option.get('adders', {})
            
            for choice in choices:
                if isinstance(choice, dict):
                    display_name = choice.get('display_name', choice.get('code', ''))
                    code = choice.get('code', '')
                else:
                    display_name = str(choice)
                    code = str(choice)
                
                price_adder = adders.get(code, 0)
                if price_adder > 0:
                    display_name += f" (+${price_adder:.2f})"
                
                self.material_combo.addItem(display_name, code)
            
            self.material_combo.currentIndexChanged.connect(self._on_material_changed)
            layout.addRow("Material:", self.material_combo)
            self.option_widgets['Material'] = self.material_combo
        
        # Voltage selection
        voltage_options = [opt for opt in self.available_options if opt.get('category') == 'Voltage']
        if voltage_options:
            self.voltage_combo = QComboBox()
            self.voltage_combo.setStyleSheet("""
                QComboBox {
                    border: 1px solid #ced4da;
                    border-radius: 4px;
                    padding: 8px;
                    min-height: 20px;
                    background-color: white;
                }
                QComboBox:focus {
                    border-color: #2C3E50;
                }
            """)
            
            voltage_option = voltage_options[0]
            choices = voltage_option.get('choices', [])
            adders = voltage_option.get('adders', {})
            
            for choice in choices:
                price_adder = adders.get(choice, 0)
                display_name = str(choice)
                if price_adder > 0:
                    display_name += f" (+${price_adder:.2f})"
                
                self.voltage_combo.addItem(display_name, choice)
            
            self.voltage_combo.currentIndexChanged.connect(self._on_voltage_changed)
            layout.addRow("Voltage:", self.voltage_combo)
            self.option_widgets['Voltage'] = self.voltage_combo
        
        self.config_layout.addWidget(group)
    
    def _create_additional_options_sections(self):
        """Create sections for additional options grouped by category."""
        # Group options by category
        options_by_category = {}
        for option in self.available_options:
            category = option.get('category', 'Other')
            if category not in ['Material', 'Voltage']:  # Skip core options
                if category not in options_by_category:
                    options_by_category[category] = []
                options_by_category[category].append(option)
        
        # Create section for each category
        for category, options in options_by_category.items():
            group = QGroupBox(category)
            group.setStyleSheet("""
                QGroupBox {
                    font-weight: 600;
                    color: #2C3E50;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    margin-top: 12px;
                    padding-top: 8px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 8px;
                    background-color: white;
                }
            """)
            
            layout = QFormLayout(group)
            layout.setSpacing(12)
            layout.setContentsMargins(16, 20, 16, 16)
            
            for option in options:
                self._create_option_widget(option, layout)
            
            self.config_layout.addWidget(group)
    
    def _create_option_widget(self, option: Dict, layout: QFormLayout):
        """Create a widget for a specific option."""
        option_name = option.get('name', '')
        choices = option.get('choices', [])
        adders = option.get('adders', {})
        
        if not choices:
            return
        
        if len(choices) <= 4:
            # Use radio buttons for few choices
            widget = self._create_radio_group(option_name, choices, adders)
        else:
            # Use dropdown for many choices
            widget = self._create_dropdown(option_name, choices, adders)
        
        layout.addRow(f"{option_name}:", widget)
        self.option_widgets[option_name] = widget
    
    def _create_radio_group(self, option_name: str, choices: List, adders: Dict) -> QWidget:
        """Create a radio button group for an option."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        button_group = QButtonGroup()
        
        for i, choice in enumerate(choices):
            if isinstance(choice, dict):
                display_name = choice.get('display_name', choice.get('code', ''))
                code = choice.get('code', '')
            else:
                display_name = str(choice)
                code = str(choice)
            
            price_adder = adders.get(code, 0)
            if price_adder > 0:
                display_name += f" (+${price_adder:.2f})"
            
            radio = QRadioButton(display_name)
            radio.setProperty("choice_code", code)
            radio.setProperty("option_name", option_name)
            
            button_group.addButton(radio, i)
            layout.addWidget(radio)
            
            if i == 0:  # Select first option by default
                radio.setChecked(True)
        
        button_group.buttonClicked.connect(self._on_radio_changed)
        return container
    
    def _create_dropdown(self, option_name: str, choices: List, adders: Dict) -> QComboBox:
        """Create a dropdown for an option."""
        combo = QComboBox()
        combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                min-height: 20px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #2C3E50;
            }
        """)
        
        for choice in choices:
            if isinstance(choice, dict):
                display_name = choice.get('display_name', choice.get('code', ''))
                code = choice.get('code', '')
            else:
                display_name = str(choice)
                code = str(choice)
            
            price_adder = adders.get(code, 0)
            if price_adder > 0:
                display_name += f" (+${price_adder:.2f})"
            
            combo.addItem(display_name, code)
        
        combo.setProperty("option_name", option_name)
        combo.currentIndexChanged.connect(self._on_dropdown_changed)
        return combo
    
    def _create_quantity_section(self):
        """Create quantity selection section."""
        group = QGroupBox("Quantity")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                color: #2C3E50;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                background-color: white;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 20, 16, 16)
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(999)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setStyleSheet("""
            QSpinBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                min-height: 20px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #2C3E50;
            }
        """)
        self.quantity_spin.valueChanged.connect(self._on_quantity_changed)
        layout.addRow("Quantity:", self.quantity_spin)
        
        self.config_layout.addWidget(group)
    
    def _on_material_changed(self):
        """Handle material selection change."""
        if hasattr(self, 'material_combo'):
            value = self.material_combo.currentData()
            self.config_service.set_option("Material", value)
            self._update_price_display()
    
    def _on_voltage_changed(self):
        """Handle voltage selection change."""
        if hasattr(self, 'voltage_combo'):
            value = self.voltage_combo.currentData()
            self.config_service.set_option("Voltage", value)
            self._update_price_display()
    
    def _on_radio_changed(self, button):
        """Handle radio button change."""
        option_name = button.property("option_name")
        value = button.property("choice_code")
        self.config_service.set_option(option_name, value)
        self._update_price_display()
    
    def _on_dropdown_changed(self):
        """Handle dropdown change."""
        sender = self.sender()
        if sender:
            option_name = sender.property("option_name")
            value = sender.currentData()
            self.config_service.set_option(option_name, value)
            self._update_price_display()
    
    def _on_quantity_changed(self, quantity: int):
        """Handle quantity change."""
        self._update_price_display()
    
    def _update_price_display(self):
        """Update the price display with current configuration."""
        try:
            # Get current configuration
            config = self.config_service.get_current_configuration()
            if not config:
                return
            
            # Calculate pricing
            unit_price = config.get('final_price', self.base_price)
            quantity = self.quantity_spin.value()
            total_price = unit_price * quantity
            
            # Build price breakdown
            breakdown = [f"Base Price: ${self.base_price:.2f}"]
            
            # Add option costs
            selected_options = config.get('selected_options', {})
            for option_name, value in selected_options.items():
                if option_name in ['Material', 'Voltage']:
                    # Get price adder for this option
                    for opt in self.available_options:
                        if opt.get('name') == option_name:
                            adders = opt.get('adders', {})
                            price_adder = adders.get(value, 0)
                            if price_adder > 0:
                                breakdown.append(f"{option_name}: +${price_adder:.2f}")
                            break
            
            # Update display
            self.price_breakdown.setText("\n".join(breakdown))
            
            if quantity > 1:
                self.total_label.setText(f"Unit Price: ${unit_price:.2f}\nQuantity: {quantity}\nTotal: ${total_price:.2f}")
            else:
                self.total_label.setText(f"Total: ${total_price:.2f}")
            
            # Update current config
            self.current_config = {
                'unit_price': unit_price,
                'quantity': quantity,
                'total_price': total_price,
                'selected_options': selected_options
            }
            
        except Exception as e:
            logger.error(f"Error updating price display: {e}", exc_info=True)
    
    def _on_add_to_quote(self):
        """Handle add to quote button click."""
        config_summary = self.get_configuration_summary()
        self.configuration_changed.emit(config_summary)
    
    def get_configuration_summary(self) -> Dict:
        """Get configuration summary for quote generation."""
        config = self.config_service.get_current_configuration()
        if not config:
            return {}
        
        # Build readable configuration description
        description_parts = [self.product_data.get('name', 'Product')]
        
        selected_options = config.get('selected_options', {})
        for option_name, value in selected_options.items():
            if option_name in ['Material', 'Voltage']:
                description_parts.append(f"{option_name}: {value}")
        
        return {
            'product': self.product_data.get('name', 'Product'),
            'description': ", ".join(description_parts),
            'configuration': self.current_config,
            'unit_price': self.current_config.get('unit_price', 0),
            'quantity': self.current_config.get('quantity', 1),
            'total_price': self.current_config.get('total_price', 0)
        } 