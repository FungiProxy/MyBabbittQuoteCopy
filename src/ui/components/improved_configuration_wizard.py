"""
Improved Product Configuration Dialog with better UI/UX
File: src/ui/components/improved_configuration_wizard.py

🟢 15 min implementation - Enhanced version of configuration_wizard.py
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QFrame,
    QScrollArea, QWidget, QGroupBox, QSpacerItem, QSizePolicy,
    QListWidget, QListWidgetItem, QMessageBox, QProgressBar,
    QButtonGroup, QRadioButton
)
from PySide6.QtGui import QFont, QPixmap, QPalette, QIntValidator

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.utils.ui_integration import QuickMigrationHelper, ModernWidgetFactory

logger = logging.getLogger(__name__)


class ModernOptionWidget(QFrame):
    """Individual option widget with modern styling and pricing display."""
    
    option_changed = Signal(str, str)  # option_name, value
    
    def __init__(self, option_name: str, choices: list, adders: dict, parent=None):
        super().__init__(parent)
        self.option_name = option_name
        self.choices = choices
        self.adders = adders
        
        self.setProperty("card", True)
        self.setProperty("interactive", True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the modern UI for this option."""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Option title
        title_label = QLabel(self.option_name)
        title_font = QFont()
        title_font.setWeight(QFont.Weight.Medium)
        title_font.setPointSize(11)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2C3E50; margin-bottom: 4px;")
        layout.addWidget(title_label)
        
        # Create appropriate input widget
        if len(self.choices) <= 4:
            # Use radio buttons for few choices
            self.input_widget = self._create_radio_group()
        else:
            # Use compact dropdown for many choices
            self.input_widget = self._create_compact_dropdown()
        
        layout.addWidget(self.input_widget)
        
        # Price indicator
        self.price_label = QLabel("")
        self.price_label.setStyleSheet("""
            color: #28A745; 
            font-weight: 600; 
            font-size: 10px;
            margin-top: 4px;
        """)
        layout.addWidget(self.price_label)
    
    def _create_radio_group(self) -> QWidget:
        """Create radio button group for few options."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.button_group = QButtonGroup()
        
        for i, choice in enumerate(self.choices):
            code = choice if isinstance(choice, str) else choice.get("code", "")
            display_name = choice if isinstance(choice, str) else choice.get("display_name", code)
            
            radio = QRadioButton(display_name)
            radio.setProperty("choice_code", code)
            
            # Style radio buttons
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 10px;
                    padding: 4px;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            
            self.button_group.addButton(radio, i)
            layout.addWidget(radio)
            
            if i == 0:  # Select first option by default
                radio.setChecked(True)
        
        self.button_group.buttonClicked.connect(self._on_radio_changed)
        return container
    
    def _create_compact_dropdown(self) -> QComboBox:
        """Create compact dropdown for many options."""
        combo = QComboBox()
        combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px 8px;
                min-height: 20px;
                max-height: 32px;
                font-size: 11px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #2C3E50;
            }
            QComboBox::drop-down {
                width: 20px;
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        
        # Handle different choice formats
        if isinstance(self.choices[0], dict):
            codes = [choice.get("code", "") for choice in self.choices]
            display_names = {choice.get("code", ""): choice.get("display_name", "") for choice in self.choices}
        else:
            codes = self.choices
            display_names = {code: code for code in codes}
        
        # Add items
        for code in codes:
            display_name = display_names.get(code, code)
            combo.addItem(display_name, code)
        
        combo.currentIndexChanged.connect(self._on_dropdown_changed)
        return combo
    
    def _on_radio_changed(self, button):
        """Handle radio button change."""
        code = button.property("choice_code")
        self._update_price_display(code)
        self.option_changed.emit(self.option_name, code)
    
    def _on_dropdown_changed(self):
        """Handle dropdown change."""
        code = self.input_widget.currentData()
        self._update_price_display(code)
        self.option_changed.emit(self.option_name, code)
    
    def _update_price_display(self, code: str):
        """Update the price display for selected option."""
        price_adder = self.adders.get(code, 0) if isinstance(self.adders, dict) else 0
        if price_adder > 0:
            self.price_label.setText(f"+${price_adder:.2f}")
            self.price_label.setStyleSheet("color: #28A745; font-weight: 600; font-size: 10px; margin-top: 4px;")
        elif price_adder < 0:
            self.price_label.setText(f"${price_adder:.2f}")
            self.price_label.setStyleSheet("color: #DC3545; font-weight: 600; font-size: 10px; margin-top: 4px;")
        else:
            self.price_label.setText("Standard")
            self.price_label.setStyleSheet("color: #6C757D; font-weight: 400; font-size: 10px; margin-top: 4px;")
    
    def get_current_value(self) -> str:
        """Get currently selected value."""
        if hasattr(self, 'button_group'):
            # Radio button group
            checked_button = self.button_group.checkedButton()
            return checked_button.property("choice_code") if checked_button else ""
        else:
            # Dropdown
            return self.input_widget.currentData() or ""
    
    def set_default_value(self, value: str):
        """Set default value for the widget."""
        if hasattr(self, 'button_group'):
            # Radio button group
            for button in self.button_group.buttons():
                if button.property("choice_code") == value:
                    button.setChecked(True)
                    self._on_radio_changed(button)
                    break
        else:
            # Dropdown
            index = self.input_widget.findData(value)
            if index >= 0:
                self.input_widget.setCurrentIndex(index)
                self._on_dropdown_changed()


class ImprovedConfigurationWizard(QDialog):
    """
    Improved product configuration dialog with modern UI/UX.
    
    🟢 Features:
    - Compact, visually appealing option widgets
    - Clear visual hierarchy and spacing
    - Real-time pricing feedback
    - Better categorization and grouping
    - Responsive layout for different screen sizes
    """
    
    product_added = Signal(dict)
    
    def __init__(self, product_data: Dict, parent=None):
        super().__init__(parent)
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        self.product_data = product_data
        self.db = SessionLocal()
        self.product_service = ProductService()
        self.config_service = ConfigurationService(self.db, self.product_service)
        self.quantity = 1
        self.option_widgets = {}
        
        self.setWindowTitle(f"Configure {product_data.get('name', 'Product')}")
        self.setModal(True)         
        self.resize(1200, 800)
        
        self._setup_ui()
        self._load_product_config()
        self._set_default_values()
        
        # Apply modern UI integration enhancements
        QuickMigrationHelper.fix_oversized_dropdowns(self)
        QuickMigrationHelper.modernize_existing_dialog(self)
    
    def _setup_ui(self):
        """Setup the improved UI layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header area
        header_layout = QHBoxLayout()
        
        self.config_title = ModernWidgetFactory.create_title_label(f"Configure {self.product_data.get('name', 'Product')}")
        header_layout.addWidget(self.config_title)
        
        header_layout.addStretch()
        
        # Progress indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.hide()
        header_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(header_layout)
        
        # Scrollable configuration area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.config_container = QWidget()
        self.config_layout = QVBoxLayout(self.config_container)
        self.config_layout.setSpacing(16)
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(self.config_container)
        main_layout.addWidget(scroll_area)
        
        # Bottom action area
        self._create_bottom_actions(main_layout)
        
        # Apply enhanced form styling
        self._enhance_form_styling()
    
    def _create_bottom_actions(self, parent_layout):
        """Create bottom action buttons with pricing."""
        actions_frame = QFrame()
        actions_frame.setProperty("card", True)
        actions_frame.setProperty("elevated", True)
        
        layout = QVBoxLayout(actions_frame)
        layout.setSpacing(12)
        
        # Pricing summary
        pricing_layout = QHBoxLayout()
        
        self.base_price_label = ModernWidgetFactory.create_price_label(0.0, "base")
        pricing_layout.addWidget(QLabel("Base Price:"))
        pricing_layout.addWidget(self.base_price_label)
        
        pricing_layout.addStretch()
        
        self.total_price_label = ModernWidgetFactory.create_price_label(0.0, "total")
        pricing_layout.addWidget(QLabel("Total:"))
        pricing_layout.addWidget(self.total_price_label)
        
        layout.addLayout(pricing_layout)
        
        # Quantity and actions
        bottom_layout = QHBoxLayout()
        
        # Quantity
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("Qty:"))
        
        self.quantity_spinner = QSpinBox()
        self.quantity_spinner.setRange(1, 999)
        self.quantity_spinner.setValue(1)
        self.quantity_spinner.setFixedWidth(80)
        self.quantity_spinner.valueChanged.connect(self._on_quantity_changed)
        qty_layout.addWidget(self.quantity_spinner)
        
        bottom_layout.addLayout(qty_layout)
        bottom_layout.addStretch()
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = ModernWidgetFactory.create_secondary_button("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.add_button = ModernWidgetFactory.create_primary_button("Add to Quote")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._on_add_to_quote)
        button_layout.addWidget(self.add_button)
        
        bottom_layout.addLayout(button_layout)
        layout.addLayout(bottom_layout)
        
        parent_layout.addWidget(actions_frame)
    
    def _load_product_config(self):
        """Load and display product configuration options."""
        logger.debug(f"Loading config for: {self.product_data['name']}")
        
        # Update header
        self.progress_bar.setValue(25)
        self.progress_bar.show()
        
        # Create configuration sections
        self._create_core_options_section()
        self._create_additional_options_sections()
        self._create_probe_length_section()
        
        # Add stretch at bottom
        self.config_layout.addStretch()
        
        # Set defaults and update pricing
        self._set_default_values()
        self._update_total_price()
        
        self.add_button.setEnabled(True)
        self.progress_bar.setValue(100)
    
    def _create_core_options_section(self):
        """Create core options (Voltage, Material) in a modern grid layout."""
        group = QGroupBox("Core Configuration")
        
        # Use grid layout for compact display
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)
        grid_layout.setContentsMargins(16, 20, 16, 16)
        
        row = 0
        col = 0
        
        # Get core options (Voltage, Material)
        try:
            # Materials
            materials = self.product_service.get_available_materials_for_product(self.db, self.product_data["name"])
            if materials:
                # Assuming the first material option contains the choices
                mat_option = materials[0]
                option_widget = ModernOptionWidget("Material", mat_option['choices'], mat_option['adders'])
                option_widget.option_changed.connect(self._on_option_changed)
                self.option_widgets["Material"] = option_widget
                grid_layout.addWidget(option_widget, row, col)
                col += 1

            # Voltages
            voltages = self.product_service.get_available_voltages(self.db, self.product_data["name"])
            if voltages:
                # Voltage options don't typically have adders from this view
                option_widget = ModernOptionWidget("Voltage", voltages, {})
                option_widget.option_changed.connect(self._on_option_changed)
                self.option_widgets["Voltage"] = option_widget
                grid_layout.addWidget(option_widget, row, col)
                col += 1
                        
        except Exception as e:
            logger.error(f"Error creating core option: {e}")
        
        group.setLayout(grid_layout)
        self.config_layout.addWidget(group)
    
    def _create_additional_options_sections(self):
        """Create additional options grouped by category."""
        try:
            all_options = self.product_service.get_additional_options(self.db, self.product_data["name"])
            
            # Group by category
            options_by_category = {}
            for option in all_options:
                category = option.get("category", "Other")
                if category not in ["Material", "Voltage"]:  # Skip core options
                    if category not in options_by_category:
                        options_by_category[category] = []
                    options_by_category[category].append(option)
            
            # Create section for each category
            for category, options in options_by_category.items():
                if not options:
                    continue
                    
                group = QGroupBox(category)
                grid_layout = QGridLayout()
                grid_layout.setSpacing(16)
                grid_layout.setContentsMargins(16, 20, 16, 16)
                
                row = 0
                col = 0
                
                for option in options:
                    option_name = option.get("name", "Unknown")
                    choices = option.get("choices", [])
                    adders = option.get("adders", {})
                    
                    if choices:
                        option_widget = ModernOptionWidget(option_name, choices, adders)
                        option_widget.option_changed.connect(self._on_option_changed)
                        self.option_widgets[option_name] = option_widget
                        
                        grid_layout.addWidget(option_widget, row, col)
                        
                        col += 1
                        if col >= 2:  # Max 2 columns
                            col = 0
                            row += 1
                
                if grid_layout.count() > 0:
                    group.setLayout(grid_layout)
                    self.config_layout.addWidget(group)
                    
        except Exception as e:
            logger.error(f"Error creating additional options: {e}")
    
    def _create_probe_length_section(self):
        """Create probe length section with modern input controls."""
        group = QGroupBox("Probe Length")
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(16)
        
        # Spinner for common lengths
        spinner_container = QFrame()
        spinner_container.setProperty("card", True)
        spinner_layout = QVBoxLayout(spinner_container)
        
        spinner_label = QLabel("Standard Length")
        spinner_label.setStyleSheet("font-weight: 500; color: #2C3E50; margin-bottom: 4px;")
        spinner_layout.addWidget(spinner_label)
        
        probe_length_spin = QSpinBox()
        probe_length_spin.setRange(1, 120)
        probe_length_spin.setSuffix('"')
        probe_length_spin.setValue(self.product_data.get("base_length", 10))
        spinner_layout.addWidget(probe_length_spin)
        
        layout.addWidget(spinner_container)
        
        # Manual input for custom lengths
        manual_container = QFrame()
        manual_container.setProperty("card", True)
        manual_layout = QVBoxLayout(manual_container)
        
        manual_label = QLabel("Custom Length")
        manual_label.setStyleSheet("font-weight: 500; color: #2C3E50; margin-bottom: 4px;")
        manual_layout.addWidget(manual_label)
        
        probe_length_edit = QLineEdit()
        probe_length_edit.setPlaceholderText("Enter custom length")
        probe_length_edit.setText(str(probe_length_spin.value()))
        probe_length_edit.setValidator(QIntValidator(1, 120))
        manual_layout.addWidget(probe_length_edit)
        
        layout.addWidget(manual_container)
        layout.addStretch()
        
        # Connect probe length widgets
        def sync_probe_length_widgets():
            # Sync spinner to edit
            probe_length_edit.textChanged.connect(
                lambda text: probe_length_spin.setValue(int(text)) if text.isdigit() and 1 <= int(text) <= 120 else None
            )
            # Sync edit to spinner
            probe_length_spin.valueChanged.connect(
                lambda value: probe_length_edit.setText(str(value))
            )
            # Trigger configuration update
            probe_length_spin.valueChanged.connect(
                lambda value: self._on_option_changed("Probe Length", value)
            )
        
        sync_probe_length_widgets()
        
        # Store widgets for access
        self.option_widgets["Probe Length Spin"] = probe_length_spin
        self.option_widgets["Probe Length Edit"] = probe_length_edit
        
        group.setLayout(layout)
        self.config_layout.addWidget(group)
    
    def _on_option_changed(self, option_name: str, value):
        """Handle option change."""
        try:
            self.config_service.set_option(option_name, value)
            self._update_total_price()
            self.progress_bar.setValue(min(100, self.progress_bar.value() + 5))
        except Exception as e:
            logger.error(f"Error updating option {option_name}: {e}")
    
    def _on_quantity_changed(self, quantity: int):
        """Handle quantity change."""
        self.quantity = quantity
        self._update_total_price()
    
    def _update_total_price(self):
        """Update price display."""
        try:
            config = self.config_service.current_config
            if config:
                base_price = config.base_product.get('base_price', 0.0)
                total_price = config.final_price
                
                self.base_price_label.setText(f"Base Price: ${base_price:.2f}")
                final_total = total_price * self.quantity
                self.total_price_label.setText(f"Total: ${final_total:.2f}")
        except Exception as e:
            logger.error(f"Error updating price: {e}")
    
    def _set_default_values(self):
        """Set default values for the product family."""
        family_name = self.product_data.get("name", "")
        default_configs = {
            "LS2000": {"Voltage": "115VAC", "Material": "S", "Probe Length": 10},
            "LS2100": {"Voltage": "24VDC", "Material": "S", "Probe Length": 10},
            "LS6000": {"Voltage": "115VAC", "Material": "S", "Probe Length": 10},
            "LS7000": {"Voltage": "115VAC", "Material": "S", "Probe Length": 10},
            "LS7000/2": {"Voltage": "115VAC", "Material": "H", "Probe Length": 10},
            "LS8000": {"Voltage": "115VAC", "Material": "S", "Probe Length": 10},
            "LS8000/2": {"Voltage": "115VAC", "Material": "H", "Probe Length": 10},
            "LT9000": {"Voltage": "115VAC", "Material": "H", "Probe Length": 10},
            "FS10000": {"Voltage": "115VAC", "Material": "S", "Probe Length": 6},
            "LS7500": {"Voltage": "115VAC", "Material": "S", "Probe Length": 10},
        }
        
        defaults = default_configs.get(family_name, {})
        
        for option_name, default_value in defaults.items():
            if option_name == "Probe Length":
                # Handle probe length widgets
                spin_widget = self.option_widgets.get("Probe Length Spin")
                edit_widget = self.option_widgets.get("Probe Length Edit")
                if spin_widget and edit_widget:
                    spin_widget.setValue(default_value)
                    edit_widget.setText(str(default_value))
                    self._on_option_changed("Probe Length", default_value)
            else:
                # Handle modern option widgets
                widget = self.option_widgets.get(option_name)
                if widget and hasattr(widget, 'set_default_value'):
                    widget.set_default_value(default_value)
                    self._on_option_changed(option_name, default_value)
    
    def _on_add_to_quote(self):
        """Handle add to quote action."""
        try:
            config = self.config_service.current_config
            if config:
                config_dict = {
                    "product_family_name": config.product_family_name,
                    "model_number": config.model_number,
                    "final_price": config.final_price,
                    "quantity": self.quantity,
                    "selected_options": config.selected_options,
                }
                self.product_added.emit(config_dict)
                self.accept()
        except Exception as e:
            logger.error(f"Error adding to quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add to quote: {e}")
    
    def closeEvent(self, event):
        """Clean up resources on close."""
        if hasattr(self, 'db') and self.db:
            self.db.close()
        super().closeEvent(event)
    
    def _enhance_form_styling(self):
        """Apply enhanced styling to form elements for better usability."""
        # This method makes the interface more user-friendly
        
        # Make buttons more prominent
        if hasattr(self, 'add_button'):
            self.add_button.setProperty("class", "primary")
            self.add_button.setText("Add to Quote")
            self.add_button.setMinimumHeight(40)
        
        # Enhance quantity controls
        if hasattr(self, 'quantity_spinner'):
            self.quantity_spinner.setMinimumHeight(36)
            self.quantity_spinner.setMinimum(1)
            self.quantity_spinner.setMaximum(999)
        
        # Make total price more prominent
        if hasattr(self, 'total_price_label'):
            self.total_price_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: 700;
                    color: #ea580c;
                    padding: 8px 12px;
                    background-color: #fff7ed;
                    border: 1px solid #fed7aa;
                    border-radius: 6px;
                }
            """) 