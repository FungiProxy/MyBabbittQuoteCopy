"""
Improved Product Configuration Dialog with better UI/UX
File: src/ui/product_selection_dialog_improved.py

🟢 15 min implementation - Replace existing product_selection_dialog.py
"""

import logging
from typing import Dict, List, Optional, Any
import os

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QEvent, QSize
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QFrame,
    QScrollArea, QWidget, QGroupBox, QSpacerItem, QSizePolicy,
    QListWidget, QListWidgetItem, QMessageBox, QProgressBar,
    QButtonGroup, QRadioButton, QCheckBox, QDoubleSpinBox, QMenu
)
from PySide6.QtGui import QFont, QPixmap, QPalette, QIntValidator, QKeyEvent, QColor

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.core.services.spare_part_service import SparePartService
from src.core.services.pricing_service import PricingService
from src.core.models import ProductFamily, Option
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
        # Exclude insulator options from connection options
        all_connection_options = [opt for opt in all_options if opt.get("category") == "Connections" and not opt.get("name", "").startswith("Insulator")]

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
        """Find the index of the default choice, prioritizing zero-cost options, then lowest adder."""
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
        # Priority 3: Pick the lowest adder
        if isinstance(self.adders, dict) and self.choices:
            min_adder = None
            min_idx = 0
            for i, choice_data in enumerate(self.choices):
                code = choice_data.get("code") if isinstance(choice_data, dict) else choice_data
                adder = self.adders.get(code, None)
                if adder is not None:
                    if min_adder is None or adder < min_adder:
                        min_adder = adder
                        min_idx = i
            return min_idx
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
        self.product_to_edit = product_to_edit
        self.quantity = 1
        self.option_widgets = {}
        self.current_product = None
        self.selected_options = {}
        self.product_image_label = None
        
        self.grid_row = 0
        self.grid_col = 0
        
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
        
        self.pricing_service = PricingService(db=self.db, product_service=self.product_service)
        self.configuration_service = ConfigurationService(db=self.db, product_service=self.product_service)

        self.selected_options: Dict[str, Any] = {}
        self.current_product: Optional[ProductFamily] = None
        self.current_base_model = None
        
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
        
        # Install a global event filter to handle the Enter key.
        self.installEventFilter(self)
    
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
        self.config_layout = QGridLayout(self.config_widget)
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
        self.pricing_layout = QHBoxLayout()
        
        self.base_price_label = QLabel("Base Price: $0.00")
        self.base_price_label.setStyleSheet("font-size: 14px; color: #6C757D;")
        self.pricing_layout.addWidget(self.base_price_label)
        
        self.pricing_layout.addStretch()
        
        self.total_price_label = QLabel("Total: $0.00")
        self.total_price_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
        """)
        self.pricing_layout.addWidget(self.total_price_label)
        
        layout.addLayout(self.pricing_layout)
        
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
    
    def _add_widget_to_grid(self, widget: QWidget, full_width: bool = False):
        """Adds a widget to the configuration grid, handling column and row positioning."""
        if full_width:
            # If we're not in the first column, move to a new row to avoid jagged layout
            if self.grid_col != 0:
                self.grid_row += 1
                self.grid_col = 0
            
            self.config_layout.addWidget(widget, self.grid_row, 0, 1, 2) # Add widget spanning both columns
            self.grid_row += 1 # Move to the next row
        else:
            self.config_layout.addWidget(widget, self.grid_row, self.grid_col)
            self.grid_col += 1
            # If we've filled the second column, move to the next row
            if self.grid_col > 1:
                self.grid_col = 0
                self.grid_row += 1

    def _show_product_config(self, product):
        """Show the configuration options for the selected product."""
        # DEBUG: Print product details to trace base price issues
        try:
            base_model = getattr(product, 'base_model', None)
            base_price = base_model.base_price if base_model else 'N/A'
            model_number = base_model.model_number if base_model else 'N/A'
            print(f"DEBUG: Configuring product: name={getattr(product, 'name', None)}, model_number={model_number}, base_price={base_price}")
        except Exception as e:
            print(f"DEBUG: Error printing product details: {e}")
        # Clear previous configuration
        while self.config_layout.count():
            item = self.config_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()
        
        self.option_widgets = {}

        self.current_product = product
        self.config_title.setText(f"Configure {product.name}")

        # Reset grid layout trackers
        self.grid_row = 0
        self.grid_col = 0

        # 1. Start with a clean slate for selected options
        self.selected_options = {}
        self.selected_spare_parts = {}  # Track selected spare parts (force reset)

        # 2. Additional & Probe Length Options (in specified order)
        self._create_ordered_options_sections(product)

        # 3. Add Spare Parts Section (collapsible)
        spare_parts_widget = self._create_spare_parts_section(product)
        if spare_parts_widget:
            self._add_widget_to_grid(spare_parts_widget, full_width=True)

        # Add a spacer to push everything to the top, spanning all columns
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.config_layout.addItem(spacer, self.grid_row + 1, 0, 1, 2)
        
        # This seems to be the right place to call this
        self._set_default_values(product.name)
        self._update_total_price()
        self.add_button.setEnabled(True)

    def _create_ordered_options_sections(self, product):
        """
        Creates all dynamic option sections in a two-column grid layout.
        """
        all_options = self.product_service.get_additional_options(product.name)
        if not all_options:
            logger.warning(f"No additional options found for {product.name}")
            return

        # --- Data Pre-processing ---
        options_by_category: Dict[str, List] = {}
        # Group all options by their category
        for option_data in all_options:
            category = option_data.get("category", "General")
            if category == "Accessories":
                category = "Extra Options"
            if category not in options_by_category:
                options_by_category[category] = []
            options_by_category[category].append(option_data)

        # Move Insulator options from "Connections" into their own categories for layout purposes
        if "Connections" in options_by_category:
            connection_opts = options_by_category["Connections"]
            insulator_opts = [opt for opt in connection_opts if opt.get("name", "").startswith("Insulator")]
            options_by_category["Connections"] = [opt for opt in connection_opts if not opt.get("name", "").startswith("Insulator")]

            for opt in insulator_opts:
                cat_name = opt.get("name") # e.g., "Insulator Material"
                if cat_name:
                    options_by_category[cat_name] = [opt]

        # --- Widget Creation and Layout ---
        def create_category_widget(category_name):
            """Creates the appropriate QGroupBox or QWidget for a given category."""
            options = options_by_category.get(category_name)
            if not options:
                return None

            # Render Connections in grid format like other options
            if category_name == "Connections":
                widgets = []
                for option in options:
                    option_name = option.get("name")
                    choices = option.get("choices", [])
                    adders = option.get("adders", {})
                    if not choices or not isinstance(choices, list):
                        continue
                    option_widget = ModernOptionWidget(option_name, choices, adders)
                    option_widget.option_changed.connect(self._on_option_changed)
                    self.option_widgets[option_name] = option_widget
                    self.selected_options[option_name] = option_widget.get_current_value()
                    widgets.append(option_widget)
                # Return a QWidget containing all connection widgets in a grid
                group = QWidget()
                grid = QGridLayout(group)
                grid.setSpacing(16)
                grid.setContentsMargins(16, 20, 16, 16)
                row, col = 0, 0
                for w in widgets:
                    grid.addWidget(w, row, col)
                    col += 1
                    if col >= 2:
                        col = 0
                        row += 1
                group.setLayout(grid)
                return group

            # Generic categories get a standard group box
            group_box = QGroupBox(category_name)
            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(10)

            widget_type = 'combobox' if category_name == "Voltages" or 'material' in category_name.lower() or 'Insulator' in category_name else 'default'

            for option in options:
                option_name = option.get("name")
                choices = option.get("choices", [])
                adders = option.get("adders", {})
                
                if not choices or not isinstance(choices, list):
                    continue

                option_widget = ModernOptionWidget(option_name, choices, adders, widget_type=widget_type)
                option_widget.option_changed.connect(self._on_option_changed)
                group_layout.addWidget(option_widget)
                self.option_widgets[option_name] = option_widget
                self.selected_options[option_name] = option_widget.get_current_value()

            return group_box

        # --- Category Ordering and Rendering ---
        all_material_categories = sorted([cat for cat in options_by_category if "material" in cat.lower()])
        main_material_categories = [cat for cat in all_material_categories if "o-ring" not in cat.lower()]
        
        priority_order = (
            ["Voltages"] + 
            main_material_categories + 
            ["Probe Length", "Connections", "Insulator Material", "Insulator Length", "O-ring Material"]
        )
        
        rendered_categories = set()
        
        # Render priority categories first
        for category in priority_order:
            if category not in rendered_categories:
                is_full_width = category in ["Probe Length", "Connections"]
                
                widget = None
                if category == "Probe Length":
                    widget = self._create_probe_length_section(product)
                elif category in options_by_category:
                    widget = create_category_widget(category)
                
                if widget:
                    self._add_widget_to_grid(widget, full_width=is_full_width)
                    rendered_categories.add(category)
        
        # Render remaining categories
        remaining_keys = sorted([key for key in options_by_category.keys() if key not in rendered_categories])
        for category in remaining_keys:
            widget = create_category_widget(category)
            if widget:
                self._add_widget_to_grid(widget, full_width=False)

    def _create_probe_length_section(self, product):
        """Create the specialized probe length input section and return it."""
        group_box = QGroupBox("Probe Length")
        layout = QHBoxLayout(group_box)
        layout.setSpacing(12)

        # Determine initial probe length based on product family and material
        default_length = 10
        family_name = getattr(product, 'name', '')
        material_code = getattr(getattr(product, 'base_model', None), 'material', 'S')
        if family_name == 'FS10000':
            default_length = 6
        elif material_code in ['U', 'T', 'CPVC']:
            default_length = 4
        elif material_code == 'C':
            default_length = 12

        probe_length_spinner = QSpinBox()
        probe_length_spinner.setRange(1, 200)
        probe_length_spinner.setSingleStep(1)
        probe_length_spinner.setValue(default_length)
        probe_length_spinner.setSuffix(" in.")
        probe_length_spinner.setMinimumWidth(100)

        self.probe_length_edit = QLineEdit(str(default_length))
        self.probe_length_edit.setValidator(QIntValidator(1, 999))
        layout.addWidget(probe_length_spinner)
        layout.addWidget(self.probe_length_edit)
        layout.addStretch()

        self.option_widgets["Probe Length"] = probe_length_spinner
        self.option_widgets["Probe Length Edit"] = self.probe_length_edit
        group_box.setLayout(layout)

        def sync_probe_length_widgets():
            probe_length_spinner.valueChanged.connect(
                lambda val: [self.probe_length_edit.setText(str(val)), self._on_option_changed("Probe Length", val)]
            )
            def update_spinner(text):
                try:
                    val = int(text)
                    if 1 <= val <= 200:
                        probe_length_spinner.setValue(val)
                        self._on_option_changed("Probe Length", val)
                except Exception:
                    pass
            self.probe_length_edit.textChanged.connect(update_spinner)
        sync_probe_length_widgets()

        # Emit the initial default value to calculate the initial length adder
        self._on_option_changed("Probe Length", default_length)
        return group_box

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

        # Add regular product families
        for family in filtered_families:
            item = QListWidgetItem(f"{family['name']}")
            item.setToolTip(family.get('description', 'No description available.'))
            item.setData(Qt.ItemDataRole.UserRole, family)
            self.product_list.addItem(item)
        
        # Add Spare Parts as a special family (only if not filtering or if "spare" is in filter)
        if not filter_text or "spare" in filter_text.lower() or "parts" in filter_text.lower():
            # Add a separator
            separator_item = QListWidgetItem()
            separator_item.setFlags(Qt.ItemFlag.NoItemFlags)
            separator_item.setSizeHint(QSize(0, 20))
            self.product_list.addItem(separator_item)
            
            # Add Spare Parts family
            spare_parts_family = {
                'name': 'Spare Parts',
                'description': 'Browse and add spare parts to your quote',
                'is_spare_parts': True
            }
            item = QListWidgetItem("🔧 Spare Parts")
            item.setToolTip("Browse and add spare parts to your quote")
            item.setData(Qt.ItemDataRole.UserRole, spare_parts_family)
            item.setBackground(QColor("#f8f9fa"))
            item.setForeground(QColor("#6c757d"))
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
        family_data = selected_item.data(Qt.ItemDataRole.UserRole)
        
        # Check if this is the special "Spare Parts" selection
        if family_data.get('is_spare_parts'):
            self._show_spare_parts_interface()
            return
        
        family_name = selected_item.text()
        
        # We need the full object, not just a dict
        product_family_obj = self.product_service.get_product_family_by_name(family_name)
        
        if not product_family_obj:
            QMessageBox.critical(self, "Error", f"Could not find product data for {family_name}.")
            return

        self._show_product_config(product_family_obj)
        
        self.config_area.setVisible(True)

    def _show_spare_parts_interface(self):
        """Show the spare parts browsing and selection interface."""
        # Clear the current configuration area
        for i in reversed(range(self.config_layout.count())):
            layout_item = self.config_layout.itemAt(i)
            if layout_item and layout_item.widget():
                child = layout_item.widget()
                if child:
                    child.setParent(None)
        
        # Reset grid layout trackers
        self.grid_row = 0
        self.grid_col = 0
        
        # Update the title
        self.config_title.setText("Spare Parts")
        
        # Reset spare parts selection
        self.selected_spare_parts = {}  # Force reset when switching to spare parts tab
        
        # Create the spare parts interface
        self._create_spare_parts_browsing_interface()
        
        # Show the configuration area
        self.config_area.setVisible(True)
        
        # Disable the add button since we're not configuring a product
        self.add_button.setEnabled(False)

    def _on_option_changed(self, option_name: str, value):
        """Handle option change and update total price."""
        self.selected_options[option_name] = value
        # Special handling for Material change to update Probe Length base
        if option_name == "Material":
            new_material_code = None
            if isinstance(value, dict):
                new_material_code = value.get('code')
            elif isinstance(value, str) and ' - ' in value:
                new_material_code = value.split(' - ')[0]
            elif isinstance(value, str):
                new_material_code = value
            if new_material_code:
                updated_probe_length = 10
                if new_material_code in ['U', 'T', 'CPVC']:
                    updated_probe_length = 4
                elif new_material_code == 'C':
                    updated_probe_length = 12
                if self.current_product and getattr(self.current_product, 'name', None) == 'FS10000':
                    updated_probe_length = 6
                spin_widget = self.option_widgets.get("Probe Length")
                edit_widget = self.option_widgets.get("Probe Length Edit")
                if spin_widget and edit_widget and spin_widget.value() != int(updated_probe_length):
                    spin_widget.setValue(int(updated_probe_length))
                    edit_widget.setText(str(int(updated_probe_length)))
                    self.selected_options["Probe Length"] = updated_probe_length
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
        length_adder = 0.0
        # Get current probe length
        probe_length = self.selected_options.get("Probe Length", 10.0)
        # Get selected material to calculate length adder
        material_widget = self.option_widgets.get("Material")
        selected_material = None
        if material_widget and isinstance(material_widget, ModernOptionWidget):
            material_choice = material_widget.get_current_value()
            if isinstance(material_choice, dict):
                selected_material = material_choice.get('code')
            elif isinstance(material_choice, str) and ' - ' in material_choice:
                selected_material = material_choice.split(' - ')[0]
            elif isinstance(material_choice, str):
                selected_material = material_choice
        if selected_material and probe_length:
            try:
                print(f'DEBUG: Calling calculate_length_price with product_name={self.current_product.name}, selected_material={selected_material}, probe_length={probe_length}')
                length_adder = self.product_service.calculate_length_price(
                    self.current_product.name, 
                    selected_material, 
                    float(probe_length)
                )
                print(f'DEBUG: length_adder returned = {length_adder}')
            except Exception as e:
                logger.warning(f"Error calculating length price: {e}")
                length_adder = 0.0
        # Only include adders for the active connection sub-option
        # Determine selected connection type if present
        selected_connection_type = None
        if 'Connection Type' in self.selected_options:
            selected_connection_type = self.selected_options['Connection Type']
        for option_name, selected_value in self.selected_options.items():
            # If this is a connection sub-option, only include if it matches the selected type
            if option_name in ['NPT Size', 'Flange Size', 'Tri-clamp']:
                if selected_connection_type == 'NPT' and option_name != 'NPT Size':
                    continue
                if selected_connection_type == 'Flange' and option_name != 'Flange Size':
                    continue
                if selected_connection_type == 'Tri-clamp' and option_name != 'Tri-clamp':
                    continue
            widget = self.option_widgets.get(option_name)
            if isinstance(widget, ModernOptionWidget):
                price_adder = widget.get_current_adder_value()
                if price_adder != 0:
                    print(f'DEBUG: option adder: option_name={option_name}, selected_value={selected_value}, price_adder={price_adder}')
                total_adder += price_adder
            elif isinstance(widget, ConnectionOptionsWidget):
                config = widget.get_current_configuration()
                pass
        spare_parts_total = 0.0
        if hasattr(self, 'selected_spare_parts'):
            spare_parts_total = sum(
                data['part'].price * data['quantity'] 
                for data in self.selected_spare_parts.values()
            )
        # DEBUG PRINTS
        print('DEBUG: base_price =', base_price)
        print('DEBUG: total_adder =', total_adder)
        print('DEBUG: length_adder =', length_adder)
        print('DEBUG: spare_parts_total =', spare_parts_total)
        total_price = base_price + total_adder + length_adder + spare_parts_total
        print('DEBUG: total_price =', total_price)
        # Update price display with length adder information
        self.base_price_label.setText(f"Base Price: ${base_price:.2f}")
        
        # Show length adder if applicable
        if length_adder > 0:
            length_info = f"Length Adder: ${length_adder:.2f}"
            if hasattr(self, 'length_adder_label'):
                self.length_adder_label.setText(length_info)
                self.length_adder_label.setVisible(True)
            else:
                # Create length adder label if it doesn't exist
                self.length_adder_label = QLabel(length_info)
                self.length_adder_label.setStyleSheet("""
                    QLabel {
                        font-size: 12px;
                        color: #059669;
                        padding: 4px 8px;
                        background-color: #ecfdf5;
                        border: 1px solid #a7f3d0;
                        border-radius: 4px;
                    }
                """)
                # Add the length adder label to the pricing layout
                if hasattr(self, 'pricing_layout'):
                    self.pricing_layout.addWidget(self.length_adder_label)
        else:
            if hasattr(self, 'length_adder_label'):
                self.length_adder_label.setVisible(False)
        
        # Show spare parts total if applicable
        if spare_parts_total > 0:
            spare_parts_info = f"Spare Parts: ${spare_parts_total:.2f}"
            if hasattr(self, 'spare_parts_total_label'):
                self.spare_parts_total_label.setText(spare_parts_info)
                self.spare_parts_total_label.setVisible(True)
            else:
                # Create spare parts total label if it doesn't exist
                self.spare_parts_total_label = QLabel(spare_parts_info)
                self.spare_parts_total_label.setStyleSheet("""
                    QLabel {
                        font-size: 12px;
                        color: #7c3aed;
                        padding: 4px 8px;
                        background-color: #f3f4f6;
                        border: 1px solid #ddd6fe;
                        border-radius: 4px;
                    }
                """)
                # Add the spare parts total label to the pricing layout
                if hasattr(self, 'pricing_layout'):
                    self.pricing_layout.addWidget(self.spare_parts_total_label)
        else:
            if hasattr(self, 'spare_parts_total_label'):
                self.spare_parts_total_label.setVisible(False)
        
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
            "product_id": self.current_product.base_model.id if self.current_product.base_model else None,
            "product_family": self.current_product.name,
            "quantity": self.quantity,
            "selected_options": self.selected_options,
            "base_price": self.current_product.base_model.base_price if self.current_product.base_model else 0.0,
        }

        # Add spare parts to configuration
        if hasattr(self, 'selected_spare_parts') and self.selected_spare_parts:
            final_config["spare_parts"] = [
                {
                    "part_number": data['part'].part_number,
                    "name": data['part'].name,
                    "quantity": data['quantity'],
                    "unit_price": data['part'].price,
                    "total_price": data['part'].price * data['quantity']
                }
                for data in self.selected_spare_parts.values()
            ]
        else:
            final_config["spare_parts"] = []

        # Calculate final price again for safety
        total_price = final_config["base_price"]
        
        # Add option adders
        for option_name, selected_value in self.selected_options.items():
             widget = self.option_widgets.get(option_name)
             if isinstance(widget, ModernOptionWidget):
                 # Use the get_current_adder_value method to handle exotic metals
                 total_price += widget.get_current_adder_value()
        
        # Add length adder
        probe_length = self.selected_options.get("Probe Length", 10.0)
        material_widget = self.option_widgets.get("Material")
        if material_widget and isinstance(material_widget, ModernOptionWidget):
            material_choice = material_widget.get_current_value()
            selected_material = None
            if isinstance(material_choice, dict):
                selected_material = material_choice.get('code')
            elif isinstance(material_choice, str) and ' - ' in material_choice:
                selected_material = material_choice.split(' - ')[0]
            elif isinstance(material_choice, str):
                selected_material = material_choice
            
            if selected_material and probe_length:
                try:
                    print(f'DEBUG: Calling calculate_length_price with product_name={self.current_product.name}, selected_material={selected_material}, probe_length={probe_length}')
                    length_adder = self.product_service.calculate_length_price(
                        self.current_product.name, 
                        selected_material, 
                        float(probe_length)
                    )
                    print(f'DEBUG: length_adder returned = {length_adder}')
                except Exception as e:
                    logger.warning(f"Error calculating length price: {e}")
                    length_adder = 0.0
        
        # Add spare parts total
        spare_parts_total = 0.0
        if hasattr(self, 'selected_spare_parts'):
            spare_parts_total = sum(
                data['part'].price * data['quantity'] 
                for data in self.selected_spare_parts.values()
            )
        
        total_price += spare_parts_total
        
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
        Globally filter for the Enter key to prevent accidental dialog closure.
        If the key is pressed on a QLineEdit, clear focus as a UX cue.
        """
        # We are only interested in KeyPress events.
        if event.type() != QEvent.Type.KeyPress:
            return super().eventFilter(watched, event)

        # Check if the key is Enter or Return.
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # If the event originated from a QLineEdit, clear its focus.
            if isinstance(watched, QLineEdit):
                watched.clearFocus()

            # Return True to signify that we have handled this event.
            # This prevents the event from being processed further, which stops
            # it from triggering the dialog's default button (i.e., accept()).
            return True
        
        # For all other events, let the default implementation handle them.
        return super().eventFilter(watched, event)

    def _update_product_image(self, product_family):
        """Update the product image based on the selected product family."""
        if not self.product_image_label:
            return
            
        image_path = self.product_service.get_product_image_path(product_family)
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.product_image_label.setPixmap(pixmap.scaled(
                self.product_image_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.product_image_label.setText("Image not available")

    def _create_product_image_section(self):
        """Creates the section for displaying the product image."""

    def _create_spare_parts_section(self, product):
        """Creates the spare parts section for the selected product."""
        # Get spare parts for this product family
        spare_parts = SparePartService.get_spare_parts_by_family(self.db, product.name)
        
        if not spare_parts:
            return None  # Don't show section if no spare parts available
        
        # Create collapsible group box
        group_box = QGroupBox("Spare Parts")
        group_box.setCheckable(True)
        group_box.setChecked(False)  # Start collapsed
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e4e7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2C3E50;
            }
            QGroupBox:checked {
                border-color: #2C3E50;
            }
        """)
        
        # Main layout for the group box
        main_layout = QVBoxLayout(group_box)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 20, 16, 16)
        
        # Summary label (shown when collapsed)
        self.spare_parts_summary = QLabel("0 spare parts selected")
        self.spare_parts_summary.setStyleSheet("""
            QLabel {
                color: #6C757D;
                font-size: 12px;
                font-weight: normal;
                padding: 4px 8px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        """)
        main_layout.addWidget(self.spare_parts_summary)
        
        # Content widget (shown when expanded)
        self.spare_parts_content = QWidget()
        content_layout = QVBoxLayout(self.spare_parts_content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-weight: 500; color: #2C3E50;")
        search_layout.addWidget(search_label)
        
        self.spare_parts_search = QLineEdit()
        self.spare_parts_search.setPlaceholderText("Search by part number or name...")
        self.spare_parts_search.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2C3E50;
            }
        """)
        search_layout.addWidget(self.spare_parts_search)
        content_layout.addLayout(search_layout)
        
        # Spare parts list
        self.spare_parts_list = QListWidget()
        self.spare_parts_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e9ecef;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #2C3E50;
            }
        """)
        self.spare_parts_list.setMaximumHeight(200)
        content_layout.addWidget(self.spare_parts_list)
        
        # Selected spare parts display
        self.selected_spare_parts_list = QListWidget()
        self.selected_spare_parts_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #d1ecf1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #e9ecef;
            }
        """)
        self.selected_spare_parts_list.setMaximumHeight(120)
        content_layout.addWidget(self.selected_spare_parts_list)
        
        # Add the content widget to main layout
        main_layout.addWidget(self.spare_parts_content)
        
        # Initially hide content (collapsed state)
        self.spare_parts_content.setVisible(False)
        
        # Connect signals
        group_box.toggled.connect(self._on_spare_parts_toggled)
        self.spare_parts_search.textChanged.connect(self._filter_spare_parts)
        self.spare_parts_list.itemDoubleClicked.connect(self._add_spare_part)
        
        # Add context menu for selected spare parts
        self.selected_spare_parts_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.selected_spare_parts_list.customContextMenuRequested.connect(self._show_spare_parts_context_menu)
        
        # Populate spare parts
        self._populate_spare_parts_list(spare_parts)
        
        return group_box
    
    def _on_spare_parts_toggled(self, checked):
        """Handle spare parts section toggle (expand/collapse)."""
        self.spare_parts_content.setVisible(checked)
        if checked:
            self.spare_parts_summary.setVisible(False)
        else:
            self.spare_parts_summary.setVisible(True)
            self._update_spare_parts_summary()
    
    def _populate_spare_parts_list(self, spare_parts):
        """Populate the spare parts list."""
        self.spare_parts_list.clear()
        self.all_spare_parts = spare_parts  # Store for filtering
        
        for part in spare_parts:
            item = QListWidgetItem()
            item.setText(f"{part.part_number} - {part.name} (${part.price:.2f})")
            item.setData(Qt.ItemDataRole.UserRole, part)
            item.setToolTip(f"Part Number: {part.part_number}\nName: {part.name}\nPrice: ${part.price:.2f}\n\nDouble-click to add")
            self.spare_parts_list.addItem(item)
    
    def _filter_spare_parts(self, search_text):
        """Filter spare parts based on search text."""
        for i in range(self.spare_parts_list.count()):
            item = self.spare_parts_list.item(i)
            part = item.data(Qt.ItemDataRole.UserRole)
            
            # Check if search text matches part number or name
            matches = (
                search_text.lower() in part.part_number.lower() or
                search_text.lower() in part.name.lower()
            )
            
            item.setHidden(not matches)
    
    def _add_spare_part(self, item):
        """Add a spare part to the selected list."""
        part = item.data(Qt.ItemDataRole.UserRole)
        part_key = part.part_number
        
        # Check if already selected
        if part_key in self.selected_spare_parts:
            # Increment quantity
            self.selected_spare_parts[part_key]['quantity'] += 1
        else:
            # Add new part
            self.selected_spare_parts[part_key] = {
                'part': part,
                'quantity': 1
            }
        
        self._update_selected_spare_parts_display()
        self._update_spare_parts_summary()
        self._update_total_price()
    
    def _update_selected_spare_parts_display(self):
        """Update the display of selected spare parts."""
        self.selected_spare_parts_list.clear()
        
        for part_key, data in self.selected_spare_parts.items():
            part = data['part']
            quantity = data['quantity']
            total_price = part.price * quantity
            
            item = QListWidgetItem()
            item.setText(f"{part.name} x{quantity} = ${total_price:.2f}")
            item.setData(Qt.ItemDataRole.UserRole, part_key)
            
            # Add remove button or context menu
            item.setToolTip(f"Part: {part.part_number}\nQuantity: {quantity}\nPrice: ${part.price:.2f}\nTotal: ${total_price:.2f}\n\nRight-click to remove")
            
            self.selected_spare_parts_list.addItem(item)
    
    def _update_spare_parts_summary(self):
        """Update the summary text for spare parts."""
        total_parts = sum(data['quantity'] for data in self.selected_spare_parts.values())
        total_price = sum(data['part'].price * data['quantity'] for data in self.selected_spare_parts.values())
        
        if total_parts == 0:
            self.spare_parts_summary.setText("0 spare parts selected")
        else:
            self.spare_parts_summary.setText(f"{total_parts} spare parts selected - ${total_price:.2f}")
    
    def _remove_spare_part(self, part_key):
        """Remove a spare part from the selected list."""
        if part_key in self.selected_spare_parts:
            del self.selected_spare_parts[part_key]
            self._update_selected_spare_parts_display()
            self._update_spare_parts_summary()
            self._update_total_price()

    def _show_spare_parts_context_menu(self, position):
        """Show context menu for selected spare parts."""
        item = self.selected_spare_parts_list.itemAt(position)
        if item:
            part_key = item.data(Qt.ItemDataRole.UserRole)
            menu = QMenu()
            remove_action = menu.addAction("Remove")
            remove_action.triggered.connect(lambda: self._remove_spare_part(part_key))
            menu.exec(self.selected_spare_parts_list.mapToGlobal(position))

    def _create_spare_parts_browsing_interface(self):
        """Create the main spare parts browsing interface."""
        # Initialize selected spare parts if not already done
        if not hasattr(self, 'selected_spare_parts'):
            self.selected_spare_parts = {}
        
        # Get all spare parts from all families
        all_spare_parts = SparePartService.get_all_spare_parts(self.db)
        
        # Group spare parts by product family
        spare_parts_by_family = {}
        for part in all_spare_parts:
            family_name = part.product_family.name
            if family_name not in spare_parts_by_family:
                spare_parts_by_family[family_name] = []
            spare_parts_by_family[family_name].append(part)
        
        # Create the main interface
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("Browse and Add Spare Parts")
        header_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(header_label)
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-weight: 500; color: #2C3E50;")
        search_layout.addWidget(search_label)
        
        self.spare_parts_search = QLineEdit()
        self.spare_parts_search.setPlaceholderText("Search by part number, name, or family...")
        self.spare_parts_search.setStyleSheet("""
            QLineEdit {
                padding: 10px 12px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2C3E50;
            }
        """)
        search_layout.addWidget(self.spare_parts_search)
        main_layout.addLayout(search_layout)
        
        # Create scrollable area for spare parts
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Add spare parts grouped by family
        for family_name in sorted(spare_parts_by_family.keys()):
            family_parts = spare_parts_by_family[family_name]
            
            # Create family group
            family_group = QGroupBox(family_name)
            family_group.setStyleSheet("""
                QGroupBox {
                    font-weight: 600;
                    color: #2C3E50;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 8px;
                    background-color: white;
                }
            """)
            
            family_layout = QVBoxLayout(family_group)
            family_layout.setSpacing(8)
            
            # Add spare parts for this family
            for part in family_parts:
                part_widget = self._create_spare_part_widget(part)
                family_layout.addWidget(part_widget)
            
            scroll_layout.addWidget(family_group)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # Add the main widget to the grid
        self._add_widget_to_grid(main_widget, full_width=True)
        
        # Connect search functionality
        self.spare_parts_search.textChanged.connect(self._filter_spare_parts_browsing)
        
        # Store reference to all spare parts for filtering
        self.all_spare_parts_browsing = all_spare_parts
        self.spare_parts_by_family = spare_parts_by_family

    def _create_spare_part_widget(self, part):
        """Create a widget for displaying a single spare part."""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 8px;
            }
            QFrame:hover {
                background-color: #e9ecef;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Part info
        info_layout = QVBoxLayout()
        part_name = QLabel(part.name)
        part_name.setStyleSheet("font-weight: 500; color: #2C3E50;")
        info_layout.addWidget(part_name)
        
        part_details = QLabel(f"Part #: {part.part_number} | ${part.price:.2f}")
        part_details.setStyleSheet("font-size: 12px; color: #6c757d;")
        info_layout.addWidget(part_details)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Add to quote button
        add_button = QPushButton("Add to Quote")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_button.clicked.connect(lambda: self._add_spare_part_to_quote(part))
        layout.addWidget(add_button)
        
        return widget

    def _add_spare_part_to_quote(self, part):
        """Add a spare part directly to the quote."""
        # Create a spare part configuration
        spare_part_config = {
            "type": "spare_part",
            "part_number": part.part_number,
            "name": part.name,
            "price": part.price,
            "quantity": 1,
            "product_family": part.product_family.name
        }
        
        # Emit the signal to add to quote
        self.product_added.emit(spare_part_config)
        
        # Show confirmation
        QMessageBox.information(
            self, 
            "Spare Part Added", 
            f"Added {part.name} to your quote.\nPrice: ${part.price:.2f}"
        )

    def _filter_spare_parts_browsing(self, search_text):
        """Filter spare parts in the browsing interface."""
        if not hasattr(self, 'all_spare_parts_browsing'):
            return
        
        # This is a simplified filter - in a full implementation,
        # you'd want to hide/show the family groups and parts
        # For now, we'll just log the search
        logger.info(f"Searching spare parts: {search_text}")