"""
Working Product Selection Dialog

A simplified but functional product selection and configuration dialog
that integrates with the existing services and provides a working
product configuration interface.
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QFrame,
    QScrollArea, QWidget, QGroupBox, QListWidget, QListWidgetItem, 
    QMessageBox, QProgressBar, QButtonGroup, QRadioButton
)
from PySide6.QtGui import QFont, QIntValidator

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialIntegration

logger = logging.getLogger(__name__)


class WorkingProductSelectionDialog(QDialog):
    """
    Working product selection dialog with simplified but functional interface.
    
    Features:
    - Product family selection
    - Material and voltage configuration
    - Real-time pricing updates
    - Quantity selection
    - Professional styling
    """
    
    product_added = Signal(dict)
    
    def __init__(self, product_service: ProductService, parent=None, product_to_edit=None):
        super().__init__(parent)
        self.product_service = product_service
        self.db = SessionLocal()
        self.config_service = ConfigurationService(self.db, self.product_service)
        self.product_to_edit = product_to_edit
        self.quantity = 1
        self.option_widgets = {}
        
        self.setWindowTitle("Configure Product" if product_to_edit else "Select & Configure Product")
        self.setModal(True)
        self.resize(1000, 700)
        
        # Apply industrial theme integration
        BabbittIndustrialIntegration.setup_dialog(self, "large")
        
        self._setup_ui()
        
        if product_to_edit:
            self._load_product_for_editing()
        else:
            self._load_product_list()
    
    def _setup_ui(self):
        """Setup the UI layout."""
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
        """Create left panel for product selection."""
        panel = QFrame()
        panel.setStyleSheet("QFrame { background-color: #f8f9fa; }")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header
        header_label = QLabel("Select Product Family")
        header_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 16px;
        """)
        layout.addWidget(header_label)
        
        # Product list
        self.product_list = QListWidget()
        self.product_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: white;
                padding: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f8f9fa;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)
        self.product_list.itemClicked.connect(self._on_product_selected)
        layout.addWidget(self.product_list)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Create right panel for configuration."""
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
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.config_container = QWidget()
        self.config_layout = QVBoxLayout(self.config_container)
        self.config_layout.setSpacing(16)
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(self.config_container)
        layout.addWidget(scroll_area)
        
        # Bottom actions
        self._create_bottom_actions(layout)
        
        return panel
    
    def _create_bottom_actions(self, parent_layout):
        """Create bottom action buttons."""
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
        
        # Price display
        price_layout = QHBoxLayout()
        
        self.base_price_label = QLabel("Base Price: $0.00")
        self.base_price_label.setStyleSheet("font-weight: 600; color: #2C3E50;")
        price_layout.addWidget(self.base_price_label)
        
        price_layout.addStretch()
        
        self.total_price_label = QLabel("Total: $0.00")
        self.total_price_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #ea580c;
            padding: 8px 12px;
            background-color: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 6px;
        """)
        price_layout.addWidget(self.total_price_label)
        
        layout.addLayout(price_layout)
        
        # Button layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: white;
                color: #6c757d;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #adb5bd;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # Add to Quote button
        self.add_button = QPushButton("Add to Quote")
        self.add_button.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                background-color: #28A745;
                color: white;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._on_add_to_quote)
        button_layout.addWidget(self.add_button)
        
        bottom_layout.addLayout(button_layout)
        layout.addLayout(bottom_layout)
        
        parent_layout.addWidget(actions_frame)
    
    def _load_product_list(self):
        """Load product list."""
        try:
            # Get product families
            families = self.product_service.get_product_families(self.db)
            self.products = families
            self._populate_product_list()
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")
    
    def _populate_product_list(self, filter_text=""):
        """Populate the product list."""
        self.product_list.clear()
        try:
            for product in self.products:
                if filter_text.lower() in product.get('name', '').lower():
                    item = QListWidgetItem(product.get('name', ''))
                    item.setData(Qt.ItemDataRole.UserRole, product)
                    self.product_list.addItem(item)
        except Exception as e:
            logger.error(f"Error populating product list: {e}", exc_info=True)
    
    def _on_product_selected(self):
        """Handle product selection."""
        items = self.product_list.selectedItems()
        if not items:
            return
        
        product_data = items[0].data(Qt.ItemDataRole.UserRole)
        try:
            # Start configuration
            self.config_service.start_configuration(
                product_family_id=product_data.get('id', 1),
                product_family_name=product_data.get('name', ''),
                base_product_info=product_data,
            )
            self._show_product_config(product_data)
        except Exception as e:
            logger.error(f"Error starting configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to configure product: {e}")
    
    def _show_product_config(self, product):
        """Show configuration options for the selected product."""
        logger.debug(f"Showing config for: {product.get('name', '')}")
        
        # Clear existing config
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.option_widgets.clear()
        
        # Update header
        self.config_title.setText(f"Configure {product.get('name', '')}")
        self.progress_bar.setValue(25)
        self.progress_bar.show()
        
        # Create configuration sections
        self._create_core_options_section(product)
        self._create_quantity_section()
        
        # Set defaults and update pricing
        self._set_default_values(product.get('name', ''))
        self._update_total_price()
        
        self.add_button.setEnabled(True)
        self.progress_bar.setValue(100)
    
    def _create_core_options_section(self, product):
        """Create core options (Material, Voltage)."""
        group = QGroupBox("Core Configuration")
        
        layout = QFormLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 20, 16, 16)
        
        # Material selection
        try:
            materials = self.product_service.get_available_materials_for_product(self.db, product.get('name', ''))
            if materials:
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
                
                material_option = materials[0]
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
        except Exception as e:
            logger.error(f"Error creating material options: {e}")
        
        # Voltage selection
        try:
            voltages = self.product_service.get_available_voltages(self.db, product.get('name', ''))
            if voltages:
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
                
                for voltage in voltages:
                    self.voltage_combo.addItem(str(voltage), voltage)
                
                self.voltage_combo.currentIndexChanged.connect(self._on_voltage_changed)
                layout.addRow("Voltage:", self.voltage_combo)
                self.option_widgets['Voltage'] = self.voltage_combo
        except Exception as e:
            logger.error(f"Error creating voltage options: {e}")
        
        self.config_layout.addWidget(group)
    
    def _create_quantity_section(self):
        """Create quantity selection section."""
        group = QGroupBox("Quantity")
        
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
            self._update_total_price()
    
    def _on_voltage_changed(self):
        """Handle voltage selection change."""
        if hasattr(self, 'voltage_combo'):
            value = self.voltage_combo.currentData()
            self.config_service.set_option("Voltage", value)
            self._update_total_price()
    
    def _on_quantity_changed(self, quantity: int):
        """Handle quantity change."""
        self.quantity = quantity
        self._update_total_price()
    
    def _update_total_price(self):
        """Update price display."""
        try:
            if self.config_service.current_config:
                base_price = self.config_service.current_config.base_product.get('base_price', 0)
                total_price = self.config_service.get_final_price()
                
                self.base_price_label.setText(f"Base Price: ${base_price:.2f}")
                final_total = total_price * self.quantity
                self.total_price_label.setText(f"Total: ${final_total:.2f}")
        except Exception as e:
            logger.error(f"Error updating price: {e}")
    
    def _set_default_values(self, family_name: str):
        """Set default values for the product family."""
        default_configs = {
            "LS2000": {"Voltage": "115VAC", "Material": "S"},
            "LS1000": {"Voltage": "24VDC", "Material": "S"},
            "LS6000": {"Voltage": "115VAC", "Material": "S"},
            "LS7000": {"Voltage": "115VAC", "Material": "S"},
            "LS8000": {"Voltage": "115VAC", "Material": "S"},
        }
        
        defaults = default_configs.get(family_name, {})
        
        for option_name, default_value in defaults.items():
            widget = self.option_widgets.get(option_name)
            if widget and hasattr(widget, 'findText'):
                # For combo boxes
                index = widget.findText(default_value)
                if index >= 0:
                    widget.setCurrentIndex(index)
                    self._on_option_changed(option_name, default_value)
    
    def _on_option_changed(self, option_name: str, value):
        """Handle option change."""
        try:
            self.config_service.set_option(option_name, value)
            self._update_total_price()
        except Exception as e:
            logger.error(f"Error updating option {option_name}: {e}")
    
    def _on_add_to_quote(self):
        """Handle add to quote action."""
        try:
            if self.config_service.current_config:
                config = {
                    'product': self.config_service.current_config.product_family_name,
                    'description': self.config_service.get_final_description(),
                    'unit_price': self.config_service.get_final_price(),
                    'quantity': self.quantity,
                    'total_price': self.config_service.get_final_price() * self.quantity,
                    'configuration': self.config_service.current_config.selected_options
                }
                self.product_added.emit(config)
                self.accept()
        except Exception as e:
            logger.error(f"Error adding to quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add to quote: {e}")
    
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
        """Apply enhanced styling to form elements."""
        # Make buttons more prominent
        if hasattr(self, 'add_button'):
            self.add_button.setMinimumHeight(40) 