"""
Improved Product Configuration Dialog with better UI/UX
File: src/ui/product_selection_dialog_improved.py

🟢 15 min implementation - Replace existing product_selection_dialog.py
"""

import logging
from typing import Dict, List, Optional
from src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper


from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QFrame,
    QScrollArea, QWidget, QGroupBox, QSpacerItem, QSizePolicy,
    QListWidget, QListWidgetItem, QMessageBox, QProgressBar,
    QButtonGroup, QRadioButton
)
from PySide6.QtGui import QFont, QPixmap, QPalette
from PySide6.QtCore import QIntValidator

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService

logger = logging.getLogger(__name__)


class ModernOptionWidget(QFrame):
    """Individual option widget with modern styling and pricing display."""
    
    option_changed = Signal(str, str)  # option_name, value
    
    def __init__(self, option_name: str, choices: list, adders: dict, parent=None):
        super().__init__(parent)
                # Apply configuration dialog fixes
                ConfigurationDialogHelper.apply_dialog_fixes(self)

        self.option_name = option_name
        self.choices = choices
        self.adders = adders
        
        self.setFrameStyle(QFrame.Box)
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
                box-shadow: 0 2px 8px rgba(44, 62, 80, 0.1);
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
    
    def __init__(self, product_service: ProductService, product_to_edit=None, parent=None):
        super().__init__(parent)
                # Apply configuration dialog fixes
                ConfigurationDialogHelper.apply_dialog_fixes(self)

        self.product_service = product_service
        self.config_service = ConfigurationService()
        self.db = SessionLocal()
        self.product_to_edit = product_to_edit
        self.quantity = 1
        self.option_widgets = {}
        
        self.setWindowTitle("Configure Product" if product_to_edit else "Select & Configure Product")
        self.setModal(True)
        self.resize(1200, 800)
        
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
        """Create modern right panel for configuration."""
        panel = QFrame()
        panel.setStyleSheet("QFrame { background-color: #f8f9fa; }")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header area
        header_layout = QHBoxLayout()
        
        self.config_title = QLabel("Select a Product")
        self.config_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #2C3E50;
        """)
        header_layout.addWidget(self.config_title)
        
        header_layout.addStretch()
        
        # Progress indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #e9ecef;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #28A745;
                border-radius: 3px;
            }
        """)
        self.progress_bar.hide()
        header_layout.addWidget(self.progress_bar)
        
        layout.addLayout(header_layout)
        
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
        layout.addWidget(scroll_area)
        
        # Bottom action area
        self._create_bottom_actions(layout)
        
        return panel
    
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
        """Show improved configuration options for the selected product."""
        logger.debug(f"Showing improved config for: {product['name']}")
        
        # Clear existing config
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.option_widgets.clear()
        
        # Update header
        self.config_title.setText(f"Configure {product['name']}")
        self.progress_bar.setValue(25)
        self.progress_bar.show()
        
        # Create configuration sections
        self._create_core_options_section(product)
        self._create_additional_options_sections(product)
        self._create_probe_length_section(product)
        
        # Add stretch at bottom
        self.config_layout.addStretch()
        
        # Set defaults and update pricing
        self._set_default_values(product.get("name", ""))
        self._update_total_price()
        
        self.add_button.setEnabled(True)
        self.progress_bar.setValue(100)
    
    def _create_core_options_section(self, product):
        """Create core options (Voltage, Material) in a modern grid layout."""
        group = QGroupBox("Core Configuration")
        
        # Use grid layout for compact display
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)
        grid_layout.setContentsMargins(16, 20, 16, 16)
        
        row = 0
        col = 0
        
        # Get core options (Voltage, Material)
        core_options = ["Voltage", "Material"]
        
        for option_name in core_options:
            try:
                choices = self.product_service.get_option_choices(self.db, product["name"], option_name)
                adders = self.product_service.get_option_adders(self.db, product["name"], option_name)
                
                if choices:
                    option_widget = ModernOptionWidget(option_name, choices, adders)
                    option_widget.option_changed.connect(self._on_option_changed)
                    self.option_widgets[option_name] = option_widget
                    
                    grid_layout.addWidget(option_widget, row, col)
                    
                    col += 1
                    if col >= 2:  # Max 2 columns
                        col = 0
                        row += 1
                        
            except Exception as e:
                logger.error(f"Error creating core option {option_name}: {e}")
        
        group.setLayout(grid_layout)
        self.config_layout.addWidget(group)
    
    def _create_additional_options_sections(self, product):
        """Create additional options grouped by category."""
        try:
            all_options = self.product_service.get_additional_options(self.db, product["name"])
            
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
    
    def _create_probe_length_section(self, product):
        """Create probe length section with modern input controls."""
        group = QGroupBox("Probe Length")
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(16)
        
        # Spinner for common lengths
        spinner_container = QFrame()
        spinner_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        spinner_layout = QVBoxLayout(spinner_container)
        
        spinner_label = QLabel("Standard Length")
        spinner_label.setStyleSheet("font-weight: 500; color: #2C3E50; margin-bottom: 4px;")
        spinner_layout.addWidget(spinner_label)
        
        probe_length_spin = QSpinBox()
        probe_length_spin.setRange(1, 120)
        probe_length_spin.setSuffix('"')
        probe_length_spin.setValue(product.get("base_length", 10))
        probe_length_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        spinner_layout.addWidget(probe_length_spin)
        
        layout.addWidget(spinner_container)
        
        # Manual input for custom lengths
        manual_container = QFrame()
        manual_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        manual_layout = QVBoxLayout(manual_container)
        
        manual_label = QLabel("Custom Length")
        manual_label.setStyleSheet("font-weight: 500; color: #2C3E50; margin-bottom: 4px;")
        manual_layout.addWidget(manual_label)
        
        probe_length_edit = QLineEdit()
        probe_length_edit.setPlaceholderText("Enter custom length")
        probe_length_edit.setText(str(probe_length_spin.value()))
        probe_length_edit.setValidator(QIntValidator(1, 120))
        probe_length_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
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
    
    # Keep existing methods for data handling...
    def _load_product_list(self):
        """Load product list (existing implementation)."""
        try:
            products = self.product_service.get_products(self.db)
            self.products = products
            self._populate_product_list()
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")
    
    def _populate_product_list(self, filter_text=""):
        """Populate product list with optional filtering."""
        self.product_list.clear()
        filtered_products = [
            p for p in self.products 
            if filter_text.lower() in p["name"].lower()
        ]
        
        for product in filtered_products:
            item = QListWidgetItem(f"{product['name']}")
            item.setData(Qt.UserRole, product)
            self.product_list.addItem(item)
    
    def _filter_products(self, text):
        """Filter products based on search text."""
        self._populate_product_list(text)
    
    def _on_product_selected(self):
        """Handle product selection."""
        items = self.product_list.selectedItems()
        if not items:
            return
        
        product_data = items[0].data(Qt.UserRole)
        try:
            self.config_service.start_configuration(
                product_family_id=product_data["id"],
                product_family_name=product_data["name"],
                base_product_info=product_data,
            )
            self._show_product_config(product_data)
        except Exception as e:
            logger.error(f"Error starting configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to configure product: {e}")
    
    def _on_option_changed(self, option_name: str, value):
        """Handle option change."""
        try:
            self.config_service.update_option(option_name, value)
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
            config = self.config_service.get_current_configuration()
            if config:
                base_price = config.get('base_price', 0)
                total_price = config.get('final_price', 0)
                
                self.base_price_label.setText(f"Base Price: ${base_price:.2f}")
                final_total = total_price * self.quantity
                self.total_price_label.setText(f"Total: ${final_total:.2f}")
        except Exception as e:
            logger.error(f"Error updating price: {e}")
    
    def _set_default_values(self, family_name: str):
        """Set default values for the product family."""
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
            config = self.config_service.get_current_configuration()
            if config:
                config['quantity'] = self.quantity
                self.product_added.emit(config)
                self.accept()
        except Exception as e:
            logger.error(f"Error adding to quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add to quote: {e}")
    
    def _load_product_for_editing(self):
        """Load product for editing (existing implementation)."""
        if self.product_to_edit:
            # Implementation for editing existing product
            pass
    
    def closeEvent(self, event):
        """Clean up resources on close."""
        if hasattr(self, 'db') and self.db:
            self.db.close()
        super().closeEvent(event)