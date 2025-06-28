"""
V0 Product Selection Dialog - Modern UI with Existing Business Logic
Combines v0ui design with existing product configuration and pricing services
"""

import logging
from typing import Dict, Optional

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                               QListWidget, QListWidgetItem, QPushButton, QTabWidget,
                               QComboBox, QSpinBox, QFormLayout, QFrame, QScrollArea,
                               QMessageBox, QGroupBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

# Import existing business logic (unchanged)
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

logger = logging.getLogger(__name__)


class ModernButton(QPushButton):
    """Modern button component"""
    
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style(button_type)
    
    def _apply_style(self, button_type):
        if button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
                QPushButton:pressed {
                    background-color: #1e40af;
                }
            """)
        elif button_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f8fafc;
                    color: #475569;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                    border-color: #cbd5e1;
                }
                QPushButton:pressed {
                    background-color: #e2e8f0;
                }
            """)


class ModernLineEdit(QWidget):
    """Modern input with search styling"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        from PySide6.QtWidgets import QLineEdit
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(44)
        self.input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #cbd5e1;
            }
        """)
        layout.addWidget(self.input)
    
    @property
    def textChanged(self):
        return self.input.textChanged
    
    def text(self):
        return self.input.text()


class V0ProductSelectionDialog(QDialog):
    """
    Modern product selection dialog combining v0ui design with existing services.
    Preserves all business logic while providing modern interface.
    """
    
    product_added = Signal(dict)
    
    def __init__(self, product_service: ProductService = None, parent=None, product_to_edit=None):
        super().__init__(parent)
        
        # Initialize services (existing business logic)
        self.product_service = product_service or ProductService()
        self.db = SessionLocal()
        self.config_service = ConfigurationService(self.db, self.product_service)
        self.product_to_edit = product_to_edit
        self.quantity = 1
        self.option_widgets = {}
        self.selected_product = None
        
        self.setWindowTitle("Configure Product - Babbitt International")
        self.setModal(True)
        self.resize(900, 600)
        
        # Apply modern styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QGroupBox {
                font-weight: 600;
                color: #1e293b;
                border: 2px solid #e2e8f0;
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
        self._load_products()
        
        if product_to_edit:
            self._load_product_for_editing()
    
    def _setup_ui(self):
        """Setup modern UI layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header_label = QLabel("Select a Product to Begin")
        header_label.setFont(QFont("Segoe UI", 18, QFont.Weight.SemiBold))
        header_label.setStyleSheet("color: #1e293b;")
        layout.addWidget(header_label)
        
        # Main content
        main_layout = QHBoxLayout()
        
        # Left panel - Product list
        left_panel = self._create_product_list_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel - Configuration
        right_panel = self._create_configuration_panel()
        main_layout.addWidget(right_panel, 2)
        
        layout.addLayout(main_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = ModernButton("Cancel", "secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.add_btn = ModernButton("Add to Quote", "primary")
        self.add_btn.clicked.connect(self._on_add_to_quote)
        self.add_btn.setEnabled(False)
        button_layout.addWidget(self.add_btn)
        
        layout.addLayout(button_layout)
    
    def _create_product_list_panel(self):
        """Create modern product list panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Search
        search_input = ModernLineEdit("Search products...")
        search_input.textChanged.connect(self._filter_products)
        layout.addWidget(search_input)
        
        # Product list
        self.product_list = QListWidget()
        self.product_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f1f5f9;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #f8fafc;
            }
        """)
        self.product_list.currentItemChanged.connect(self._on_product_selected)
        layout.addWidget(self.product_list)
        
        return panel
    
    def _create_configuration_panel(self):
        """Create modern configuration panel"""
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Configuration title
        self.config_label = QLabel("Configure Product")
        self.config_label.setFont(QFont("Segoe UI", 16, QFont.Weight.SemiBold))
        self.config_label.setStyleSheet("color: #1e293b;")
        layout.addWidget(self.config_label)
        
        # Tabs for configuration sections
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3b82f6;
            }
        """)
        
        # Create empty tabs initially
        material_tab = QWidget()
        voltage_tab = QWidget()
        length_tab = QWidget()
        
        self.tabs.addTab(material_tab, "Material")
        self.tabs.addTab(voltage_tab, "Voltage") 
        self.tabs.addTab(length_tab, "Probe Length")
        
        layout.addWidget(self.tabs)
        
        # Pricing section
        pricing_widget = self._create_pricing_widget()
        layout.addWidget(pricing_widget)
        
        return panel
    
    def _create_pricing_widget(self):
        """Create modern pricing display"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        self.base_price_label = QLabel("Base Price: $0.00")
        self.base_price_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.base_price_label)
        
        layout.addStretch()
        
        qty_label = QLabel("Qty:")
        layout.addWidget(qty_label)
        
        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setValue(1)
        self.qty_spin.setStyleSheet("""
            QSpinBox {
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 8px;
                min-width: 60px;
            }
        """)
        self.qty_spin.valueChanged.connect(self._update_total)
        layout.addWidget(self.qty_spin)
        
        layout.addStretch()
        
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #059669;")
        layout.addWidget(self.total_label)
        
        return widget
    
    def _load_products(self):
        """Load products using existing service"""
        try:
            # Use existing product service (unchanged business logic)
            families = self.product_service.get_product_families(self.db)
            self._populate_product_list(families)
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")
    
    def _populate_product_list(self, families, filter_text=""):
        """Populate product list with families"""
        self.product_list.clear()
        for family in families:
            if filter_text.lower() in family.name.lower():
                item = QListWidgetItem(family.name)
                item.setData(Qt.ItemDataRole.UserRole, family)
                self.product_list.addItem(item)
    
    def _filter_products(self, text):
        """Filter products based on search"""
        try:
            families = self.product_service.get_product_families(self.db)
            self._populate_product_list(families, text)
        except Exception as e:
            logger.error(f"Error filtering products: {e}")
    
    def _on_product_selected(self, current, previous):
        """Handle product selection using existing services"""
        if not current:
            return
        
        family = current.data(Qt.ItemDataRole.UserRole)
        self.selected_product = family
        
        # Update configuration using existing service
        try:
            self.config_service.start_configuration(
                product_family_id=family.id,
                product_family_name=family.name,
                base_product_info={"name": family.name, "id": family.id}
            )
            
            self._update_configuration_ui(family)
            self.add_btn.setEnabled(True)
            
        except Exception as e:
            logger.error(f"Error configuring product: {e}")
            QMessageBox.critical(self, "Error", f"Failed to configure product: {e}")
    
    def _update_configuration_ui(self, family):
        """Update configuration UI with product options"""
        self.config_label.setText(f"Configure {family.name}")
        
        # Update pricing
        base_price = getattr(family.base_model, 'base_price', 0.0) if family.base_model else 0.0
        self.base_price_label.setText(f"Base Price: ${base_price:.2f}")
        self._update_total()
        
        # Load options into tabs (simplified for demo)
        try:
            # Get material options
            materials = self.product_service.get_available_materials_for_product(self.db, family.name)
            if materials:
                self._populate_material_tab(materials[0])
                
        except Exception as e:
            logger.error(f"Error loading options: {e}")
    
    def _populate_material_tab(self, material_option):
        """Populate material tab with options"""
        material_tab = self.tabs.widget(0)
        
        # Clear existing layout
        if material_tab.layout():
            widget = QWidget()
            material_tab.setParent(None)
            self.tabs.removeTab(0)
            self.tabs.insertTab(0, widget, "Material")
            material_tab = widget
        
        layout = QFormLayout(material_tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 20, 16, 16)
        
        # Material combo
        material_combo = QComboBox()
        material_combo.setMinimumHeight(44)
        material_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #2563eb;
            }
            QComboBox:hover {
                border-color: #cbd5e1;
            }
        """)
        
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
            
            material_combo.addItem(display_name, code)
        
        material_combo.currentIndexChanged.connect(self._update_total)
        layout.addRow("Material:", material_combo)
        
        self.option_widgets["Material"] = material_combo
    
    def _update_total(self):
        """Update total price"""
        try:
            base_price = 0.0
            if self.selected_product and self.selected_product.base_model:
                base_price = self.selected_product.base_model.base_price
            
            quantity = self.qty_spin.value()
            total = base_price * quantity
            
            self.total_label.setText(f"Total: ${total:.2f}")
            
        except Exception as e:
            logger.error(f"Error updating total: {e}")
    
    def _on_add_to_quote(self):
        """Add configured product to quote using existing service"""
        if not self.selected_product:
            QMessageBox.warning(self, "Warning", "Please select a product first.")
            return
        
        try:
            # Get configuration from service (existing business logic)
            config = self.config_service.get_current_configuration()
            if config:
                config['quantity'] = self.qty_spin.value()
                self.product_added.emit(config)
                self.accept()
            else:
                QMessageBox.warning(self, "Warning", "No configuration available.")
                
        except Exception as e:
            logger.error(f"Error adding to quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add to quote: {e}")
    
    def _load_product_for_editing(self):
        """Load product for editing (existing functionality)"""
        if self.product_to_edit:
            # Implementation for editing existing product
            pass
    
    def closeEvent(self, event):
        """Clean up resources"""
        if hasattr(self, 'db') and self.db:
            self.db.close()
        super().closeEvent(event) 