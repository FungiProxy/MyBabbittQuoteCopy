"""
Improved Product Configuration Dialog with better UI/UX
File: src/ui/product_selection_dialog_improved.py

🟢 15 min implementation - Replace existing product_selection_dialog.py
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QEvent
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QFrame,
    QScrollArea, QWidget, QGroupBox, QSpacerItem, QSizePolicy,
    QListWidget, QListWidgetItem, QMessageBox, QProgressBar,
    QButtonGroup, QRadioButton, QCheckBox, QDoubleSpinBox
)
from PySide6.QtGui import QFont, QPixmap, QPalette, QIntValidator, QKeyEvent

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.ui.theme.babbitt_theme import BabbittTheme

logger = logging.getLogger(__name__)


class ConnectionOptionsWidget(QFrame):
    """A dedicated widget to handle the complexity of connection options."""
    
    option_changed = Signal(str, object)  # Emits option name and selected value
    
    def __init__(self, family_name: str, product_service: ProductService, parent=None):
        super().__init__(parent)
        self.family_name = family_name
        self.product_service = product_service
        self.sub_option_widgets: Dict[str, QWidget] = {}
        
        self.setFrameStyle(QFrame.Shape.NoFrame)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Build the UI for connection options."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        
        # Fetch all connection-related options for this product family
        all_options = self.product_service.get_additional_options(self.family_name)
        all_connection_options = [opt for opt in all_options if opt.get("category") == "Connections"]

        # Create the primary connection type dropdown
        connection_type_option = next((opt for opt in all_connection_options if opt['name'] == 'Connection Type'), None)
        
        if not connection_type_option:
            # If no primary selector, don't build anything
            return
            
        self.type_combo = self._create_option_widget("Connection Type", connection_type_option)
        self.main_layout.addWidget(self.type_combo)
        self.type_combo.option_changed.connect(self._on_connection_type_changed)

        # Container for sub-options that will be shown/hidden
        self.sub_options_container = QWidget()
        self.sub_options_layout = QVBoxLayout(self.sub_options_container)
        self.sub_options_layout.setContentsMargins(0, 10, 0, 0)
        self.sub_options_layout.setSpacing(10)
        self.main_layout.addWidget(self.sub_options_container)

        # Create all possible sub-option widgets and hide them initially
        self._create_sub_option_widgets(all_connection_options)
        
        # Trigger the initial state based on the default connection type
        self._on_connection_type_changed()

    def _create_option_widget(self, name: str, option_data: Dict) -> "ModernOptionWidget":
        """Factory for creating a standard option widget."""
        widget = ModernOptionWidget(
            option_name=name,
            choices=option_data.get("choices", []),
            adders=option_data.get("adders", {}),
            widget_type='combobox'
        )
        widget.option_changed.connect(
            lambda opt_name, value: self.option_changed.emit(opt_name, value)
        )
        return widget

    def _create_sub_option_widgets(self, options: List[Dict]):
        """Create and store all potential sub-option widgets."""
        sub_option_map = {
            "NPT": ["NPT Size"],
            "Flange": ["Flange Size", "Flange Type"],
            "Tri-clamp": ["Tri-clamp"]
        }

        for conn_type, sub_names in sub_option_map.items():
            for name in sub_names:
                option_data = next((opt for opt in options if opt['name'] == name), None)
                if option_data:
                    widget = self._create_option_widget(name, option_data)
                    self.sub_options_layout.addWidget(widget)
                    widget.hide()
                    self.sub_option_widgets[name] = widget

    def _on_connection_type_changed(self):
        """Show/hide sub-options based on the selected connection type."""
        selected_type = ""
        if isinstance(self.type_combo, ModernOptionWidget):
            selected_type = self.type_combo.get_current_value()
        
        self.option_changed.emit("Connection Type", selected_type)

        sub_option_map = {
            "NPT": ["NPT Size"],
            "Flange": ["Flange Size", "Flange Type"],
            "Tri-clamp": ["Tri-clamp"]
        }

        # Hide all sub-options first
        for widget in self.sub_option_widgets.values():
            widget.hide()

        # Show the relevant ones
        if selected_type in sub_option_map:
            for name in sub_option_map[selected_type]:
                if name in self.sub_option_widgets:
                    widget = self.sub_option_widgets[name]
                    widget.show()
                    # Emit its default value so the config service is aware of it
                    if isinstance(widget, ModernOptionWidget):
                        self.option_changed.emit(name, widget.get_current_value())
    
    def get_current_configuration(self) -> Dict[str, str]:
        """Get all selected values from this widget."""
        config = {}
        if isinstance(self.type_combo, ModernOptionWidget):
            config["Connection Type"] = self.type_combo.get_current_value()
        
        selected_type = config.get("Connection Type", "")
        sub_option_map = {
            "NPT": ["NPT Size"],
            "Flange": ["Flange Size", "Flange Type"],
            "Tri-clamp": ["Tri-clamp"]
        }
        
        if selected_type in sub_option_map:
            for name in sub_option_map[selected_type]:
                if name in self.sub_option_widgets:
                    widget = self.sub_option_widgets[name]
                    if isinstance(widget, ModernOptionWidget):
                        config[name] = widget.get_current_value()
                    
        return config


class ModernOptionWidget(QFrame):
    """Individual option widget with modern styling and pricing display."""
    
    option_changed = Signal(str, str)  # option_name, value
    
    def __init__(self, option_name: str, choices: list, adders: dict, widget_type: str = 'default', parent=None):
        super().__init__(parent)
        self.option_name = option_name
        self.choices = choices
        self.adders = adders
        self.widget_type = widget_type
        self.exotic_metals = ["A", "HB", "HC", "TT"]  # Exotic metal codes
        self.manual_adder_input = None  # Will hold the manual adder input widget
        
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet("""
            ModernOptionWidget {
                background-color: #ffffff;
                border: 1px solid #e0e4e7;
                border-radius: 8px;
                margin: 4px;
                padding: 12px;
            }
            ModernOptionWidget:hover {
                border-color: #2C3E50;
            }
        """)
        
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
        
        # Create appropriate input widget based on type or number of choices
        if self.widget_type == 'combobox':
            self.input_widget = self._create_compact_dropdown()
        elif self.widget_type == 'radio':
            self.input_widget = self._create_radio_group()
        else:  # 'default' behavior
            if len(self.choices) <= 4:
                # Use radio buttons for few choices
                self.input_widget = self._create_radio_group()
            else:
                # Use compact dropdown for many choices
                self.input_widget = self._create_compact_dropdown()
        
        layout.addWidget(self.input_widget)
        
        # Create manual adder input for exotic metals (initially hidden)
        if self.option_name == "Material":
            self.manual_adder_input = self._create_manual_adder_input()
            layout.addWidget(self.manual_adder_input)
            self.manual_adder_input.hide()
        
        # Price indicator
        self.price_label = QLabel("")
        self.price_label.setStyleSheet("""
            color: #28A745; 
            font-weight: 600; 
            font-size: 10px;
            margin-top: 4px;
        """)
        layout.addWidget(self.price_label)
    
    def _create_manual_adder_input(self) -> QWidget:
        """Create manual adder input widget for exotic metals."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 8, 0, 0)
        
        # Label
        label = QLabel("Manual Adder ($):")
        label.setStyleSheet("""
            color: #6C757D;
            font-size: 10px;
            font-weight: 500;
        """)
        layout.addWidget(label)
        
        # Input field
        self.adder_spinbox = QSpinBox()
        self.adder_spinbox.setMinimum(0)
        self.adder_spinbox.setMaximum(9999)
        self.adder_spinbox.setValue(0)
        self.adder_spinbox.setStyleSheet("""
            QSpinBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 4px 6px;
                min-height: 20px;
                max-height: 24px;
                font-size: 10px;
                background-color: white;
            }
            QSpinBox:focus {
                border-color: #2C3E50;
            }
        """)
        self.adder_spinbox.valueChanged.connect(self._on_manual_adder_changed)
        layout.addWidget(self.adder_spinbox)
        
        # Add stretch to push everything to the left
        layout.addStretch()
        
        return container
    
    def _on_manual_adder_changed(self, value: int):
        """Handle manual adder value change."""
        # Update the adders dictionary with the manual value
        current_choice = self._get_current_choice()
        if current_choice in self.exotic_metals:
            if isinstance(self.adders, dict):
                self.adders[current_choice] = value
            self._update_price_display(current_choice)
            # Emit the option change with the current choice
            self.option_changed.emit(self.option_name, current_choice)
    
    def _get_current_choice(self) -> str:
        """Get the currently selected choice."""
        if hasattr(self, 'button_group') and self.button_group:
            button = self.button_group.checkedButton()
            if button:
                return button.property("choice_code")
        elif hasattr(self, 'input_widget') and isinstance(self.input_widget, QComboBox):
            return self.input_widget.currentData()
        return ""
    
    def _check_and_show_exotic_metal_input(self, choice: str):
        """Check if choice is exotic metal and show/hide manual input accordingly."""
        if self.manual_adder_input and self.option_name == "Material":
            if choice in self.exotic_metals:
                self.manual_adder_input.show()
                # Set the current manual adder value
                current_adder = self.adders.get(choice, 0) if isinstance(self.adders, dict) else 0
                self.adder_spinbox.setValue(current_adder)
            else:
                self.manual_adder_input.hide()
    
    def _create_radio_group(self) -> QWidget:
        """Create radio button group for few options."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.button_group = QButtonGroup()
        
        default_idx = self._get_default_choice_index()
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
            
            if i == default_idx:
                radio.setChecked(True)
                # Check if this is an exotic metal and show input if needed
                self._check_and_show_exotic_metal_input(code)
        
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
        if not self.choices:
             return combo

        if isinstance(self.choices[0], dict):
            # Handle list of dicts like [{'code': 'S', 'display_name': '...'}, ...]
            for choice in self.choices:
                code = choice.get("code", "")
                display_name = choice.get("display_name", code)
                combo.addItem(display_name, code)
        else:
            # Handle list of strings
            for choice in self.choices:
                combo.addItem(str(choice), str(choice))
        
        default_idx = self._get_default_choice_index()
        if default_idx != -1:
            combo.setCurrentIndex(default_idx)
            # Check if this is an exotic metal and show input if needed
            default_choice = combo.currentData()
            self._check_and_show_exotic_metal_input(default_choice)

        combo.currentIndexChanged.connect(self._on_dropdown_changed)
        return combo
    
    def _on_radio_changed(self, button):
        """Handle radio button change."""
        code = button.property("choice_code")
        self._check_and_show_exotic_metal_input(code)
        self._update_price_display(code)
        self.option_changed.emit(self.option_name, code)
    
    def _on_dropdown_changed(self):
        """Handle dropdown change."""
        combo_box = self.sender()
        if isinstance(combo_box, QComboBox):
            code = combo_box.currentData()
            self._check_and_show_exotic_metal_input(code)
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
    
    def _get_default_choice_index(self) -> int:
        """Find the index of the default choice, prioritizing zero-cost options."""
        if not self.choices:
            return -1
            
        # Priority 1: Find a choice with a price adder of 0.
        if isinstance(self.adders, dict):
            for i, choice_data in enumerate(self.choices):
                code = choice_data.get("code") if isinstance(choice_data, dict) else choice_data
                if self.adders.get(code, -1) == 0:
                    return i

        # Priority 2: Find a choice that contains common default keywords.
        for i, choice_data in enumerate(self.choices):
            display_name = choice_data.get("display_name", "") if isinstance(choice_data, dict) else choice_data
            if any(keyword in display_name.lower() for keyword in ["standard", "viton", "npt"]):
                return i
                
        # Fallback to the first item if no better default is found.
        return 0

    def get_current_value(self) -> str:
        """Get the currently selected value."""
        if hasattr(self, 'button_group') and self.button_group:
            button = self.button_group.checkedButton()
            if button:
                return button.property("choice_code")
        elif hasattr(self, 'input_widget') and isinstance(self.input_widget, QComboBox):
            return self.input_widget.currentData()
        return ""
    
    def get_manual_adder_value(self) -> int:
        """Get the current manual adder value for exotic metals."""
        if self.manual_adder_input and hasattr(self, 'adder_spinbox'):
            return self.adder_spinbox.value()
        return 0
    
    def get_current_adder_value(self) -> int:
        """Get the current adder value (including manual adder for exotic metals)."""
        current_choice = self.get_current_value()
        if current_choice in self.exotic_metals:
            return self.get_manual_adder_value()
        else:
            return self.adders.get(current_choice, 0) if isinstance(self.adders, dict) else 0


class ImprovedProductSelectionDialog(QDialog):
    """
    Improved product selection dialog with modern UI/UX.
    
    🟢 Features:
    - Compact, visually appealing option widgets
    - Clear visual hierarchy and spacing
    - Real-time pricing feedback
    - Better categorization and grouping
    - Responsive layout for different screen sizes
    """
    
    product_added = Signal(dict)
    
    def __init__(self, product_service, parent=None, product_to_edit=None):
        """Initialize with enhanced styling."""
        super().__init__(parent)
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        self.product_service = product_service
        self.db = SessionLocal()
        # self.config_service = ConfigurationService(db=self.db, product_service=self.product_service)
        self.product_to_edit = product_to_edit
        self.quantity = 1
        self.option_widgets = {}
        self.current_product = None
        self.selected_options = {}

        # Enhance the dialog appearance
        self.setWindowTitle("Configure Product - Babbitt International")
        self.resize(1000, 700)  # Slightly larger for better usability
        self.setModal(True)
        
        # Apply modern styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
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
        
        self._setup_ui()
        
        if product_to_edit:
            self._load_product_for_editing()
        else:
            self._load_product_list()
        
        # Apply modern UI integration enhancements
        from src.ui.utils.ui_integration import QuickMigrationHelper
        QuickMigrationHelper.fix_oversized_dropdowns(self)
        QuickMigrationHelper.modernize_existing_dialog(self)
        
        # Apply Babbitt theme to this dialog
        self.setStyleSheet(BabbittTheme.get_dialog_stylesheet())
    
    def _setup_ui(self):
        """Setup the improved UI layout."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel - Product selection
        self.left_panel = self._create_left_panel()
        main_layout.addWidget(self.left_panel, 1)
        
        # Right panel - Configuration
        self.right_panel = self._create_right_panel()
        main_layout.addWidget(self.right_panel, 2)
        
        # Apply enhanced form styling
        self._enhance_form_styling()
    
    def _create_left_panel(self) -> QWidget:
        """Create modern left panel for product selection."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 1px solid #e9ecef;
            }
        """)
        panel.setFixedWidth(300)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header
        header = QLabel("Select Product")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 8px;
        """)
        layout.addWidget(header)
        
        # Search/Filter (placeholder for now)
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search products...")
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                font-size: 14px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #2C3E50;
                background-color: white;
            }
        """)
        layout.addWidget(search_input)
        
        # Product list
        self.product_list = QListWidget()
        self.product_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e9ecef;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #e9ecef;
                background-color: white;
                margin: 2px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
            QListWidget::item:selected {
                background-color: #2C3E50;
                color: white;
            }
        """)
        layout.addWidget(self.product_list)
        
        # Connect signals
        search_input.textChanged.connect(self._filter_products)
        self.product_list.itemSelectionChanged.connect(self._on_product_selected)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Creates the main configuration area on the right."""
        right_container = QWidget()
        container_layout = QVBoxLayout(right_container)
        container_layout.setContentsMargins(20, 10, 20, 10)

        # Title
        self.config_title = QLabel("Select a Product to Begin")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setWeight(QFont.Weight.Bold)
        self.config_title.setFont(title_font)
        self.config_title.setStyleSheet("color: #2C3E50; margin-bottom: 10px;")
        container_layout.addWidget(self.config_title)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        container_layout.addWidget(self.progress_bar)

        # Scroll Area for options
        self.config_area = QScrollArea()
        self.config_area.setWidgetResizable(True)
        self.config_area.setStyleSheet("background-color: transparent; border: none;")
        self.config_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.config_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)
        self.config_layout.setContentsMargins(5, 5, 5, 5)
        self.config_layout.setSpacing(15)
        
        self.config_area.setWidget(self.config_widget)
        container_layout.addWidget(self.config_area)

        # Add the bottom actions/pricing summary
        self._create_bottom_actions(container_layout)

        return right_container
    
    def _create_bottom_actions(self, parent_layout):
        """Create bottom action buttons with pricing."""
        actions_frame = QFrame()
        actions_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(actions_frame)
        layout.setSpacing(12)
        
        # Pricing summary
        pricing_layout = QHBoxLayout()
        
        self.base_price_label = QLabel("Base Price: $0.00")
        self.base_price_label.setStyleSheet("font-size: 14px; color: #6C757D;")
        pricing_layout.addWidget(self.base_price_label)
        
        pricing_layout.addStretch()
        
        self.total_price_label = QLabel("Total: $0.00")
        self.total_price_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
        """)
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
        self.quantity_spinner.setStyleSheet("""
            QSpinBox {
                padding: 6px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        self.quantity_spinner.valueChanged.connect(self._on_quantity_changed)
        qty_layout.addWidget(self.quantity_spinner)
        
        bottom_layout.addLayout(qty_layout)
        bottom_layout.addStretch()
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border: 1px solid #6C757D;
                border-radius: 6px;
                background-color: white;
                color: #6C757D;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.add_button = QPushButton("Add to Quote")
        self.add_button.setStyleSheet("""
            QPushButton {
                padding: 10px 24px;
                border: none;
                border-radius: 6px;
                background-color: #2C3E50;
                color: white;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:disabled {
                background-color: #6C757D;
            }
        """)
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._on_add_to_quote)
        button_layout.addWidget(self.add_button)
        
        bottom_layout.addLayout(button_layout)
        layout.addLayout(bottom_layout)
        
        parent_layout.addWidget(actions_frame)
    
    def _show_product_config(self, product):
        """Show the configuration options for the selected product."""
        # Clear previous configuration
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.option_widgets = {}

        self.current_product = product
        self.config_title.setText(f"Configure {product.name}")

        # 1. Start with a clean slate for selected options
        self.selected_options = {}

        # 2. Additional & Probe Length Options (in specified order)
        self._create_ordered_options_sections(product)

        # Add a spacer to push everything to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.config_layout.addSpacerItem(spacer)
        
        # This seems to be the right place to call this
        self._set_default_values(product.name)
        self._update_total_price()
        self.add_button.setEnabled(True)

    def _create_ordered_options_sections(self, product):
        """
        Creates all dynamic option sections in the user-defined order:
        1. Voltage
        2. Material
        3. Probe Length
        4. Connection Options
        5. All others
        """
        all_options = self.product_service.get_additional_options(product.name)
        if not all_options:
            logger.warning(f"No additional options found for {product.name}")
            return

        options_by_category: Dict[str, List] = {}
        for option_data in all_options:
            category = option_data.get("category", "General")

            # Dynamically rename "Accessories" to "Extra Options" for display purposes
            if category == "Accessories":
                category = "Extra Options"

            # We no longer need a separate core options section
            if category == "Core":
                category = "General"

            if category not in options_by_category:
                options_by_category[category] = []
            options_by_category[category].append(option_data)

        def create_category_section(category_name):
            options = options_by_category.get(category_name)
            if not options:
                return

            if category_name == "Connections":
                # Use the specialized widget for connections
                conn_widget = ConnectionOptionsWidget(product.name, self.product_service)
                conn_widget.option_changed.connect(self._on_option_changed)
                group_box = QGroupBox(category_name)
                layout = QVBoxLayout(group_box)
                layout.addWidget(conn_widget)
                self.config_layout.addWidget(group_box)
                self.option_widgets["Connections"] = conn_widget # Store the main widget
                # Set initial connection values
                initial_config = conn_widget.get_current_configuration()
                for opt_name, value in initial_config.items():
                    self.selected_options[opt_name] = value
                return

            group_box = QGroupBox(category_name)
            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(10)

            # Determine widget type for this category
            widget_type = 'default'
            if category_name == "Voltages":
                widget_type = 'combobox'
            elif 'material' in category_name.lower():
                widget_type = 'combobox'

            for option in options:
                option_name = option.get("name")
                choices = option.get("choices", [])
                adders = option.get("adders", {})
                
                if not choices or not isinstance(choices, list):
                    logger.warning(f"Skipping option '{option_name}' in '{category_name}' due to invalid choices.")
                    continue

                option_widget = ModernOptionWidget(option_name, choices, adders, widget_type=widget_type)
                option_widget.option_changed.connect(self._on_option_changed)
                group_layout.addWidget(option_widget)
                self.option_widgets[option_name] = option_widget
                # Store the default value
                self.selected_options[option_name] = option_widget.get_current_value()

            self.config_layout.addWidget(group_box)

        # Separate material categories for ordering
        all_material_categories = sorted([cat for cat in options_by_category if "material" in cat.lower()])
        main_material_categories = [cat for cat in all_material_categories if "o-ring" not in cat.lower()]
        
        # Define the display order
        priority_order = (
            ["Voltages"] + 
            main_material_categories + 
            ["Probe Length", "Connections", "O-ring Material"]
        )
        
        rendered_categories = set()

        for category in priority_order:
            if category == "Probe Length":
                # Special handling for Probe Length section
                self._create_probe_length_section(product)
                rendered_categories.add("Probe Length") # Mark as "rendered"
            elif category == "Connections":
                # Handled separately to ensure it's a single block
                create_category_section("Connections")
                rendered_categories.add("Connections")
            else:
                if category in options_by_category:
                    create_category_section(category)
                    rendered_categories.add(category)

        # Render remaining categories, sorted for consistent ordering
        remaining_keys = sorted([key for key in options_by_category.keys() if key not in rendered_categories])
        for category in remaining_keys:
            create_category_section(category)
    
    def _create_probe_length_section(self, product):
        """Create the specialized probe length input section."""
        # This section is now enabled for all products.
        group_box = QGroupBox("Probe Length")
        layout = QHBoxLayout(group_box)
        layout.setSpacing(12)
        
        # Use a sensible default since the DB doesn't store one per family
        default_length = 10.0

        # Use QDoubleSpinBox for decimal increments
        probe_length_spinner = QDoubleSpinBox()
        probe_length_spinner.setRange(1.0, 200.0)
        probe_length_spinner.setSingleStep(0.5)
        probe_length_spinner.setDecimals(1)
        probe_length_spinner.setValue(default_length)
        probe_length_spinner.setSuffix(" in.")
        probe_length_spinner.setMinimumWidth(100)
        probe_length_spinner.setStyleSheet("""
            QDoubleSpinBox { 
                padding: 6px; 
                border: 1px solid #ced4da; 
                border-radius: 4px;
            }
        """)

        self.probe_length_edit = QLineEdit(str(default_length))
        self.probe_length_edit.setValidator(QIntValidator(1, 999))
        self.probe_length_edit.installEventFilter(self) # Intercept key presses
        self.option_widgets["Probe Length Edit"] = self.probe_length_edit
        
        layout.addWidget(QLabel("Length:"))
        layout.addWidget(probe_length_spinner)
        layout.addWidget(QLabel("Custom:"))
        layout.addWidget(self.probe_length_edit)
        layout.addStretch()

        self.option_widgets["Probe Length"] = probe_length_spinner
        group_box.setLayout(layout)
        self.config_layout.addWidget(group_box)

        # Sync logic
        def sync_probe_length_widgets():
            # Sync spinner to edit - QDoubleSpinBox emits valueChanged(float)
            probe_length_spinner.valueChanged.connect(
                lambda val: self.probe_length_edit.setText(f"{val:.1f}")
            )
            
            # Sync edit to spinner
            def update_spinner(text):
                try:
                    # Use float to handle decimals from the line edit
                    val = float(text)
                    if probe_length_spinner.minimum() <= val <= probe_length_spinner.maximum():
                        # Block signals to prevent feedback loop
                        probe_length_spinner.blockSignals(True)
                        probe_length_spinner.setValue(val)
                        probe_length_spinner.blockSignals(False)
                        self._on_option_changed("Probe Length", val)
                except ValueError:
                    pass  # Ignore non-numeric input

            self.probe_length_edit.textChanged.connect(update_spinner)

        sync_probe_length_widgets()
        
        # Emit the initial default value
        self._on_option_changed("Probe Length", default_length)
    
    def _load_product_list(self):
        """Load product list from the service."""
        try:
            families = self.product_service.get_product_families(self.db)
            self._populate_product_list(families)
        except Exception as e:
            logger.error(f"Error loading product families: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", "Could not load product families from the database.")
    
    def _populate_product_list(self, families: List[Dict], filter_text: str = ""):
        """Populate the product list, optionally filtering."""
        self.product_list.clear()
        
        filtered_families = [
            f for f in families
            if filter_text.lower() in f.get('name', '').lower() or
               filter_text.lower() in f.get('description', '').lower()
        ]

        for family in filtered_families:
            item = QListWidgetItem(f"{family['name']}")
            item.setToolTip(family.get('description', 'No description available.'))
            item.setData(Qt.ItemDataRole.UserRole, family)
            self.product_list.addItem(item)
    
    def _filter_products(self, text):
        """Filter products based on search text."""
        try:
            families = self.product_service.get_product_families(self.db)
            self._populate_product_list(families, text)
        except Exception as e:
            logger.error(f"Error filtering products: {e}", exc_info=True)
    
    def _on_product_selected(self):
        """Handle product selection from the list."""
        selected_items = self.product_list.selectedItems()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        family_name = selected_item.text()
        
        # We need the full object, not just a dict
        product_family_obj = self.product_service.get_product_family_by_name(family_name)
        
        if not product_family_obj:
            QMessageBox.critical(self, "Error", f"Could not find product data for {family_name}.")
            return

        self._show_product_config(product_family_obj)
        
        self.config_area.setVisible(True)

    def _on_option_changed(self, option_name: str, value):
        """Handle option change."""
        self.selected_options[option_name] = value
        self._update_total_price()
    
    def _on_quantity_changed(self, quantity: int):
        """Handle quantity change."""
        self.quantity = quantity
        self._update_total_price()
    
    def _update_total_price(self):
        """Update price display."""
        if not self.current_product:
            return

        base_price = self.current_product.base_model.base_price if self.current_product.base_model else 0.0
        
        # Calculate adders from selected options
        total_adder = 0.0
        for option_name, selected_value in self.selected_options.items():
            widget = self.option_widgets.get(option_name)
            if isinstance(widget, ModernOptionWidget):
                # Use the get_current_adder_value method to handle exotic metals
                price_adder = widget.get_current_adder_value()
                total_adder += price_adder
            elif isinstance(widget, ConnectionOptionsWidget):
                # For complex widgets, need to get price from sub-options
                config = widget.get_current_configuration()
                # This part is still tricky, need to implement adder logic in ConnectionOptionsWidget
                # For now, let's assume it works, but we need to implement it.
                pass

        total_price = base_price + total_adder
        
        self.base_price_label.setText(f"Base Price: ${base_price:.2f}")
        final_total = total_price * self.quantity
        self.total_price_label.setText(f"Total: ${final_total:.2f}")

    def _set_default_values(self, family_name: str):
        """Set default options for the selected product family."""
        # This method is now less important, as widgets set their own sensible defaults.
        # We can keep it for product-specific overrides if needed in the future.
        pass
    
    def _on_add_to_quote(self):
        """Handle add to quote action."""
        if not self.current_product:
            QMessageBox.warning(self, "Incomplete Configuration", "Please select a product first.")
            return

        # Build the final configuration dict
        final_config = {
            "product_family": self.current_product.name,
            "quantity": self.quantity,
            "selected_options": self.selected_options,
            "base_price": self.current_product.base_model.base_price if self.current_product.base_model else 0.0,
        }

        # Calculate final price again for safety
        total_price = final_config["base_price"]
        for option_name, selected_value in self.selected_options.items():
             widget = self.option_widgets.get(option_name)
             if isinstance(widget, ModernOptionWidget):
                 # Use the get_current_adder_value method to handle exotic metals
                 total_price += widget.get_current_adder_value()
        
        final_config["total_price"] = total_price * self.quantity
        
        self.product_added.emit(final_config)
        self.accept()
    
    def _load_product_for_editing(self):
        """Load product for editing."""
        if self.product_to_edit:
            # Implementation for editing existing product
            pass
    
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
    
    def eventFilter(self, watched, event: QKeyEvent) -> bool:
        """
        Filter events to catch the Enter key press on the probe length edit.
        """
        if (hasattr(self, 'probe_length_edit') and
            watched == self.probe_length_edit and
            event.type() == QEvent.Type.KeyPress and
            event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)):
            # Event is an Enter press on our target QLineEdit.
            # We clear focus to give a visual cue that input is "done".
            self.probe_length_edit.clearFocus()
            # Return True to signify that we have handled this event and it
            # should not be processed further (i.e., it won't trigger the dialog's default button).
            return True
        
        # For all other events, pass them along to the default implementation.
        return super().eventFilter(watched, event) 