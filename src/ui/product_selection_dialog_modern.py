"""
Modern Product Selection Dialog

A modernized version of the product selection dialog using the new
modern UI components for consistent styling and enhanced UX.
"""

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, Signal, QObject, QEvent
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QWidget, QGroupBox, QListWidget, 
    QListWidgetItem, QMessageBox, QProgressBar, QButtonGroup, QRadioButton,
    QTextEdit, QPushButton, QComboBox, QSpinBox, QCheckBox, QLineEdit
)
from PySide6.QtGui import QFont

# Import our modern components
from .components import (
    ModernButton, ModernLineEdit, ModernTextEdit, ModernComboBox,
    ModernSpinBox, ModernCheckBox, ModernRadioButton,
    Card, PriceDisplay, LoadingSpinner, EmptyState
)

# Import standard Qt widgets as fallback
from PySide6.QtWidgets import QComboBox, QSpinBox

from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.ui.theme.babbitt_theme import BabbittTheme
from src.core.config.material_defaults import get_material_default_length

logger = logging.getLogger(__name__)


class EnterKeyFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            return True  # Ignore Enter/Return key
        return super().eventFilter(obj, event)


class ModernProductSelectionDialog(QDialog):
    """
    Modern product selection dialog using the new UI components.
    
    Features:
    - Product family selection
    - Material and voltage configuration using modern form components
    - Real-time pricing updates with modern price display
    - Quantity selection with modern spin box
    - Professional styling with modern components
    """
    
    product_added = Signal(dict)
    
    def __init__(self, product_service: ProductService, parent=None, product_to_edit=None):
        super().__init__(parent)
        self.product_service = product_service
        self.db = SessionLocal()
        self.product_to_edit = product_to_edit
        self.quantity = 1
        self.option_widgets = {}
        self.enter_key_filter = EnterKeyFilter()
        
        # Add flag to track model changes that need probe length reset
        self._pending_model_change = None
        self._model_changed_during_setup = False
        self._pending_model_base_length = None
        
        # Initialize configuration service
        self.config_service = ConfigurationService(self.db, self.product_service)
        
        # Setup UI
        self._setup_ui()
        
        # Connect signals after UI is set up
        self.product_list.itemSelectionChanged.connect(self._on_product_selected)
        self.add_button.clicked.connect(self._on_add_to_quote)
        self.installEventFilter(self.enter_key_filter)
        
        # Load product list
        self._load_product_list()
        
        # Set window properties
        self.setWindowTitle("Product Selection")
        self.setModal(True)
        self.resize(1000, 900)
        
        # Apply Babbitt theme
        self.setStyleSheet(BabbittTheme.get_dialog_stylesheet())
    
    def _setup_ui(self):
        """Setup the UI layout."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # Left panel - Product selection (narrower)
        self.left_panel = self._create_left_panel()
        self.left_panel.setFixedWidth(220)  # Narrowed from default
        main_layout.addWidget(self.left_panel, 0)
        
        # Right panel - Configuration
        self.right_panel = self._create_right_panel()
        main_layout.addWidget(self.right_panel, 1)
        
        # Apply enhanced form styling
        self._enhance_form_styling()
    
    def _create_left_panel(self) -> QWidget:
        """Create left panel for product selection."""
        panel = QFrame()
        panel.setStyleSheet("QFrame { background-color: #f8f9fa; border-radius: 12px; }")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)  # Increased margins
        layout.setSpacing(20)  # Increased spacing
        
        # Header
        header_label = QLabel("Select Product Family")
        header_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #2C3E50;
            margin-bottom: 8px;
        """)
        layout.addWidget(header_label)
        
        # Product list
        self.product_list = QListWidget()
        self.product_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
                padding: 12px;
                margin-top: 8px;
            }
            QListWidget::item {
                padding: 16px;
                border-bottom: 1px solid #f8f9fa;
                border-radius: 6px;
                margin: 2px 0px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                border: 2px solid #1976d2;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
                border: 1px solid #dee2e6;
            }
        """)
        self.product_list.itemClicked.connect(self._on_product_selected)
        layout.addWidget(self.product_list)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Create right panel for configuration."""
        panel = QFrame()
        panel.setStyleSheet("QFrame { background-color: #f8f9fa; border-radius: 12px; }")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header area with total price
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Model number label (dynamic)
        self.model_number_label = QLabel("")
        self.model_number_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #222;')
        header_layout.addWidget(self.model_number_label)
        
        header_layout.addStretch()
        
        # Total price display
        self.total_price_display = QLabel("Total: $0.00")
        self.total_price_display.setStyleSheet('font-size: 18px; font-weight: bold; background: #e6f0fa; border-radius: 8px; padding: 8px 18px; color: #2563eb;')
        header_layout.addWidget(self.total_price_display)
        
        layout.addLayout(header_layout)
        
        # Scrollable configuration area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #dee2e6;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #adb5bd;
            }
        """)
        
        self.config_container = QWidget()
        self.config_layout = QVBoxLayout(self.config_container)
        self.config_layout.setSpacing(16)
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(self.config_container)
        layout.addWidget(scroll_area)

        # --- Add action buttons directly at the bottom ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: 2px solid #6c757d;
                border-radius: 6px;
                background-color: white;
                color: #6c757d;
                font-weight: 600;
                font-size: 14px;
                min-height: 32px;
                max-height: 32px;
            }
            QPushButton:hover {
                background-color: #6c757d;
                color: white;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        # Add to Quote button
        self.add_button = QPushButton("Add to Quote")
        self.add_button.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                background-color: #007bff;
                color: white;
                font-weight: 600;
                font-size: 14px;
                min-height: 32px;
                max-height: 32px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
        """)
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._on_add_to_quote)
        button_layout.addWidget(self.add_button)
        layout.addLayout(button_layout)
        # --- End action buttons ---

        return panel
    
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
        """Populate the product list, filtering out base model duplicates."""
        self.product_list.clear()
        try:
            # Only include entries where the description does NOT contain 'Base Model'
            filtered_products = [
                product for product in self.products
                if 'Base Model' not in (product.get('description') or '')
            ]
            for product in filtered_products:
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
        print(f"[DEBUG] Product selected: {product_data}")
        selected_name = product_data.get('name', '')

        # PATCH: Special handling for TRAN-EX family
        if selected_name == "TRAN-EX":
            # Hardcode the correct model number for TRAN-EX
            base_product_info = self.db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
            if base_product_info:
                print(f"[PATCH] Using TRAN-EX base product: {base_product_info.model_number} (ID: {base_product_info.id})")
                # Convert SQLAlchemy object to dict for compatibility
                product_data = {
                    'id': base_product_info.id,
                    'name': selected_name,
                    'model_number': base_product_info.model_number,
                    'description': base_product_info.description,
                    'category': base_product_info.category,
                    'base_price': base_product_info.base_price,
                    'base_length': getattr(base_product_info, 'base_length', 10),
                    'voltage': getattr(base_product_info, 'voltage', '115VAC'),
                    'material': getattr(base_product_info, 'material', 'S'),
                }
            else:
                print("[PATCH] TRAN-EX base product not found!")
        else:
            base_product_info = self.product_service.get_base_product_for_family(self.db, selected_name)
            if base_product_info:
                print(f"[DEBUG] Base product info: {base_product_info}")
                product_data = base_product_info
            else:
                print(f"[WARNING] No base product found for {selected_name}, using family info")

        # Set flag for model change and store the base length
        self._model_changed_during_setup = True
        self._pending_model_base_length = product_data.get('base_length', 10)
        print(f"[DEBUG] Model changed, base length will be reset to: {self._pending_model_base_length}")

        try:
            # Get the first valid material code for this product
            materials = self.product_service.get_available_materials_for_product(self.db, selected_name)
            if materials and materials[0].get('choices'):
                first_material = None
                choices = materials[0]['choices']
                if isinstance(choices[0], dict) and 'code' in choices[0]:
                    first_material = choices[0]['code']
                elif isinstance(choices[0], str):
                    first_material = choices[0]
            else:
                first_material = None
            selected_options = {'material': first_material} if first_material else {}
            print(f"[DEBUG] Passing selected_options to start_configuration: {selected_options}")
            self.config_service.start_configuration(
                product_family_id=product_data.get('id', 1),
                product_family_name=selected_name,
                base_product_info=product_data,
                selected_options=selected_options,
            )
            self._show_product_config(product_data)
        except Exception as e:
            import traceback
            print(f"[DEBUG] Exception in _on_product_selected: {e}")
            print(traceback.format_exc())
            logger.error(f"Error starting configuration: {e}")
            raise  # Ensure the exception is not swallowed
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
        self._update_model_number_label()
        core_options = []
        seen_option_names = set()
        try:
            print(f"[DEBUG] Gathering core options for: {product.get('name', '')}")
            # Voltage - skip for TRAN-EX since it has no voltage options
            if product.get('name') != 'TRAN-EX':
                voltages = self.product_service.get_available_voltages(self.db, product.get('name', ''))
                print(f"[DEBUG] Voltages for {product.get('name', '')}: {voltages}")
                if voltages:
                    core_options.append({
                        'name': 'Voltage',
                        'choices': voltages,
                        'adders': {},
                        'category': 'Electrical',
                    })
                    seen_option_names.add('Voltage')
            else:
                print(f"[DEBUG] Skipping voltage for TRAN-EX - no voltage options")
            # Material
            materials = self.product_service.get_available_materials_for_product(self.db, product.get('name', ''))
            print(f"[DEBUG] Materials for {product.get('name', '')}: {materials}")
            if materials:
                material_option = materials[0]
                # Set default to first available material code if present
                choices = material_option.get('choices', [])
                if choices and isinstance(choices[0], dict) and 'code' in choices[0]:
                    material_option['default'] = choices[0]['code']
                elif choices and isinstance(choices[0], str):
                    material_option['default'] = choices[0]
                material_option['category'] = 'Material'
                if product.get('name') == 'TRAN-EX':
                    material_option['type'] = 'dropdown'
                core_options.append(material_option)
                seen_option_names.add('Material')
            # Special handling for TRAN-EX (fixed material)
            elif product.get('name') == 'TRAN-EX':
                core_options.append({
                    'name': 'Material',
                    'choices': ['S', 'H'],
                    'adders': {},
                    'category': 'Material',
                    'default': 'S',
                    'type': 'dropdown',
                })
                seen_option_names.add('Material')
            # Probe Length (always present unless already in options)
            if 'Probe Length' not in seen_option_names:
                base_length = product.get('base_length', 10)
                core_options.append({
                    'name': 'Probe Length',
                    'type': 'numeric',
                    'default': base_length,
                    'category': 'Mechanical',
                    'min': 1,
                    'max': 200,
                })
                seen_option_names.add('Probe Length')
        except Exception as e:
            print(f"[ERROR] Exception gathering core options for {product.get('name', '')}: {e}")
            import traceback
            print(traceback.format_exc())
            self._show_error_message(f"Error gathering core options: {e}")
            return
        # Additional options
        try:
            print(f"[DEBUG] Gathering additional options for: {product.get('name', '')}")
            additional_options = self.product_service.get_additional_options(self.db, product.get('name', ''))
            print(f"[DEBUG] Additional options: {additional_options}")
        except Exception as e:
            print(f"[ERROR] Exception gathering additional options for {product.get('name', '')}: {e}")
            import traceback
            print(traceback.format_exc())
            self._show_error_message(f"Error gathering additional options: {e}")
            additional_options = []
        quantity_option = {'name': 'Quantity', 'choices': None, 'type': 'numeric', 'category': 'General'}
        all_options = core_options[:]
        for opt in additional_options:
            if opt.get('name') not in seen_option_names:
                all_options.append(opt)
                seen_option_names.add(opt.get('name'))
        all_options.append(quantity_option)
        ordered_core_names = ['Voltage', 'Material', 'Probe Length']
        ordered_core = [opt for name in ordered_core_names for opt in all_options if opt.get('name') == name]
        rest = [opt for opt in all_options if opt.get('name') not in ordered_core_names]
        all_options = ordered_core + rest
        options_by_category = {}
        for option in all_options:
            cat = option.get('category', 'Other') or 'Other'
            if cat not in options_by_category:
                options_by_category[cat] = []
            options_by_category[cat].append(option)
        try:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            container = QWidget()
            vbox = QVBoxLayout(container)
            vbox.setSpacing(16)
            vbox.setContentsMargins(8, 8, 8, 8)
            default_values_to_set = []
            for opt in ordered_core:
                form = QFormLayout()
                form.setSpacing(10)
                form.setContentsMargins(8, 8, 8, 8)
                widget = self._create_dynamic_option_widget(opt, force_dropdown=False)
                if widget:
                    label = QLabel(opt.get('name', ''))
                    label.setStyleSheet('font-weight: 500; color: #2C3E50;')
                    form.addRow(label, widget)
                    if opt.get('name') in ['Probe Length', 'Voltage', 'Material']:
                        default_val = opt.get('default')
                        if default_val is not None:
                            default_values_to_set.append((opt.get('name'), default_val, widget))
                group = QGroupBox(opt.get('category', 'Other'))
                group.setStyleSheet('font-weight: bold; font-size: 15px;')
                group.setLayout(form)
                vbox.addWidget(group)
            # Remove Insulator options from Connections and prepare for Insulator section
            insulator_material_option = None
            insulator_length_option = None
            if 'Connections' in options_by_category:
                new_conn_opts = []
                for opt in options_by_category['Connections']:
                    if opt.get('name') == 'Insulator Material':
                        insulator_material_option = opt
                    elif opt.get('name') == 'Insulator Length':
                        insulator_length_option = opt
                    else:
                        new_conn_opts.append(opt)
                options_by_category['Connections'] = new_conn_opts
            # Render all sections as before, but insert Insulator section right after Connections
            for cat, opts in options_by_category.items():
                opts = [opt for opt in opts if opt.get('name') not in ordered_core_names]
                if not opts:
                    continue
                group = QGroupBox(cat)
                group.setStyleSheet('font-weight: bold; font-size: 15px;')
                if cat == 'Connections':
                    # Define combo_style for use in this block
                    combo_style = """
                        QComboBox {
                            border: 1px solid #ced4da;
                            border-radius: 4px;
                            padding: 8px;
                            min-height: 32px;
                            background-color: white;
                        }
                        QComboBox:focus {
                            border-color: #2C3E50;
                        }
                    """
                    # --- New: Dynamic Connection Type/Sub-options Workflow ---
                    form = QFormLayout()
                    form.setSpacing(10)
                    form.setContentsMargins(8, 8, 8, 8)

                    # Find the Connection Type option
                    connection_type_option = next((o for o in opts if o.get('name') == 'Connection Type'), None)
                    sub_option_map = {
                        'NPT': ['NPT Size'],
                        'Flange': ['Flange Size', 'Flange Type'],
                        'Tri-clamp': ['Tri-clamp']
                    }
                    # Create Connection Type dropdown
                    if connection_type_option:
                        conn_type_combo = QComboBox()
                        conn_type_combo.setFixedWidth(200)
                        conn_type_combo.setMinimumHeight(32)
                        conn_type_combo.setStyleSheet(combo_style)
                        conn_type_choices = connection_type_option.get('choices', [])
                        for choice in conn_type_choices:
                            display_name = choice.get('display_name', choice.get('code', str(choice))) if isinstance(choice, dict) else str(choice)
                            code = choice.get('code', str(choice)) if isinstance(choice, dict) else str(choice)
                            conn_type_combo.addItem(display_name, code)
                        form.addRow(QLabel('Connection Type'), conn_type_combo)
                    else:
                        conn_type_combo = None

                    # Prepare sub-option widgets (all as dropdowns)
                    sub_option_widgets = {}
                    for sub_opt in opts:
                        name = sub_opt.get('name')
                        if name == 'Connection Type':
                            continue
                        choices = sub_opt.get('choices', [])
                        adders = sub_opt.get('adders', {})
                        combo = QComboBox()
                        combo.setFixedWidth(200)
                        combo.setMinimumHeight(32)
                        combo.setStyleSheet(combo_style)
                        if choices and isinstance(choices[0], dict):
                            for choice in choices:
                                display_name = choice.get('display_name', choice.get('code', str(choice)))
                                code = choice.get('code', str(choice))
                                combo.addItem(display_name, code)
                        elif choices:
                            for choice in choices:
                                combo.addItem(str(choice), str(choice))
                        sub_option_widgets[name] = combo
                        form.addRow(QLabel(name), combo)
                        combo.hide()

                    def on_conn_type_changed(idx):
                        selected_type = conn_type_combo.currentData() if conn_type_combo else ''
                        if not isinstance(selected_type, str):
                            selected_type = str(selected_type) if selected_type is not None else ''
                        # Hide all sub-options first
                        for w in sub_option_widgets.values():
                            w.hide()
                        # Show only relevant sub-options
                        if selected_type in sub_option_map:
                            for name in sub_option_map[selected_type]:
                                if name in sub_option_widgets:
                                    sub_option_widgets[name].show()
                    if conn_type_combo:
                        conn_type_combo.currentIndexChanged.connect(on_conn_type_changed)
                        # Show sub-options for default selection
                        on_conn_type_changed(conn_type_combo.currentIndex())
                    group.setLayout(form)
                    vbox.addWidget(group)
                    # Insert Insulator section immediately after Connections
                    if insulator_material_option or insulator_length_option:
                        ins_group = QGroupBox('Insulator')
                        ins_group.setStyleSheet('font-weight: bold; font-size: 15px;')
                        ins_form = QFormLayout()
                        ins_form.setSpacing(10)
                        ins_form.setContentsMargins(8, 8, 8, 8)
                        if insulator_material_option:
                            widget = self._create_dynamic_option_widget(insulator_material_option, force_dropdown=True)
                            if widget:
                                label = QLabel(insulator_material_option.get('name', ''))
                                label.setStyleSheet('font-weight: 500; color: #2C3E50;')
                                ins_form.addRow(label, widget)
                        if insulator_length_option:
                            widget = self._create_dynamic_option_widget(insulator_length_option, force_dropdown=True)
                            if widget:
                                label = QLabel(insulator_length_option.get('name', ''))
                                label.setStyleSheet('font-weight: 500; color: #2C3E50;')
                                ins_form.addRow(label, widget)
                        ins_group.setLayout(ins_form)
                        vbox.addWidget(ins_group)
                else:
                    form = QFormLayout()
                    form.setSpacing(10)
                    form.setContentsMargins(8, 8, 8, 8)
                    for option in opts:
                        # Special handling for Accessories: single checkbox per option
                        if cat == 'Accessories':
                            name = option.get('name', '')
                            cb = QCheckBox()
                            cb.setChecked(False)  # Default to No
                            cb.stateChanged.connect(lambda state, n=name: self._on_option_changed(n, bool(state)))
                            self.option_widgets[name] = cb
                            label = QLabel(name)
                            label.setStyleSheet('font-weight: 500; color: #2C3E50;')
                            form.addRow(label, cb)
                        else:
                            widget = self._create_dynamic_option_widget(option, cat)
                            if widget:
                                label = QLabel(option.get('name', ''))
                                label.setStyleSheet('font-weight: 500; color: #2C3E50;')
                                form.addRow(label, widget)
                    group.setLayout(form)
                    vbox.addWidget(group)
            vbox.addStretch()
            scroll.setWidget(container)
            while self.config_layout.count():
                child = self.config_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self.config_layout.addWidget(scroll)
            self._set_default_values(product.get('name', ''))
            for name, value, widget in default_values_to_set:
                if hasattr(widget, 'setValue'):
                    widget.setValue(value)
                elif hasattr(widget, 'setCurrentIndex'):
                    idx = widget.findData(value)
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
                self._on_option_changed(name, value)
            self._update_total_price()
            self.add_button.setEnabled(True)
            
            # Handle any deferred changes after all widgets are created
            self._handle_deferred_changes()
            
        except Exception as e:
            print(f"[ERROR] Exception rendering config UI for {product.get('name', '')}: {e}")
            import traceback
            print(traceback.format_exc())
            self._show_error_message(f"Error rendering config UI: {e}")

    def _create_dynamic_option_widget(self, option, force_dropdown=False):
        """Create the appropriate widget for an option based on its data."""
        print(f"[DEBUG] _create_dynamic_option_widget called for option: {option.get('name')}")
        print(f"[DEBUG] Option dict: {option}")
        print(f"[DEBUG] opt_type: {option.get('type')}")
        name = option.get('name', '')
        choices = option.get('choices', None)
        adders = option.get('adders', {})
        opt_type = option.get('type', None)
        combo_style = """
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                min-height: 32px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #2C3E50;
            }
        """
        spin_style = """
            QSpinBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                min-height: 32px;
                background-color: white;
                font-size: 14px;
            }
            QSpinBox:focus {
                border-color: #2C3E50;
            }
        """
        # Force dropdown if type is explicitly set to 'dropdown'
        if opt_type == 'dropdown' and choices:
            combo = QComboBox()
            combo.setFixedWidth(200)
            combo.setMinimumHeight(32)
            combo.setStyleSheet(combo_style)
            if isinstance(choices[0], dict):
                for choice in choices:
                    display_name = choice.get('display_name', choice.get('code', str(choice)))
                    code = str(choice.get('code', str(choice)))
                    combo.addItem(display_name, code)
            else:
                for choice in choices:
                    combo.addItem(str(choice), str(choice))
            combo.currentIndexChanged.connect(lambda idx, n=name, c=combo: self._on_option_changed(n, str(c.currentData())))
            self.option_widgets[name] = combo
            return combo
        # Probe Length (always numeric input)
        if name == 'Probe Length':
            spin = QSpinBox()
            spin.setFixedWidth(120)
            spin.setMinimumHeight(32)
            spin.setMaximumHeight(32)
            spin.setStyleSheet(spin_style)
            spin.setMinimum(option.get('min', 1))
            spin.setMaximum(200)
            spin.setSingleStep(1)
            default = option.get('default', 10)
            spin.setValue(default)
            spin.valueChanged.connect(lambda val, n=name: self._on_option_changed(n, val))
            # Prevent Enter from closing dialog
            spin.installEventFilter(self.enter_key_filter)
            # Store the widget in option_widgets so it can be found later
            self.option_widgets[name] = spin
            return spin
        # Quantity (special case)
        if name == 'Quantity':
            spin = QSpinBox()
            spin.setFixedWidth(120)
            spin.setMinimumHeight(32)
            spin.setMaximumHeight(32)
            spin.setStyleSheet(spin_style)
            spin.setMinimum(1)
            spin.setMaximum(999)
            spin.setSingleStep(1)
            spin.setValue(self.quantity)
            spin.valueChanged.connect(self._on_quantity_changed)
            self.quantity_spin = spin
            # Prevent Enter from closing dialog
            spin.installEventFilter(self.enter_key_filter)
            return spin
        # Voltage: always render as dropdown
        if name == 'Voltage' and choices:
            combo = QComboBox()
            combo.setFixedWidth(200)
            combo.setMinimumHeight(32)
            combo.setStyleSheet(combo_style)
            if isinstance(choices[0], dict):
                for choice in choices:
                    display_name = choice.get('display_name', choice.get('code', str(choice)))
                    code = str(choice.get('code', str(choice)))
                    combo.addItem(display_name, code)
            else:
                for choice in choices:
                    combo.addItem(str(choice), str(choice))
            combo.currentIndexChanged.connect(lambda idx, n=name, c=combo: self._on_option_changed(n, str(c.currentData())))
            self.option_widgets[name] = combo
            return combo
        # Boolean (checkbox)
        if choices and all(isinstance(c, bool) for c in choices) and set(choices) == {True, False}:
            cb = QCheckBox()
            cb.stateChanged.connect(lambda state, n=name: self._on_option_changed(n, bool(state)))
            self.option_widgets[name] = cb
            return cb
        # Radio buttons (2-4 choices)
        if choices and 2 <= len(choices) <= 4:
            group = QWidget()
            layout = QHBoxLayout(group)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(8)
            button_group = QButtonGroup(group)
            for i, choice in enumerate(choices):
                if isinstance(choice, dict):
                    display_name = choice.get('display_name', choice.get('code', str(choice)))
                    code = str(choice.get('code', str(choice)))
                else:
                    display_name = str(choice)
                    code = str(choice)
                radio = QRadioButton(display_name)
                radio.setProperty('choice_code', code)
                button_group.addButton(radio, i)
                layout.addWidget(radio)
                if i == 0:
                    radio.setChecked(True)
            button_group.buttonClicked.connect(lambda btn, n=name: self._on_option_changed(n, str(btn.property('choice_code'))))
            self.option_widgets[name] = button_group
            return group
        # Dropdown (more than 4 choices)
        if choices and len(choices) > 4:
            combo = QComboBox()
            combo.setFixedWidth(200)
            combo.setMinimumHeight(32)
            combo.setStyleSheet(combo_style)
            if isinstance(choices[0], dict):
                for choice in choices:
                    display_name = choice.get('display_name', choice.get('code', str(choice)))
                    code = str(choice.get('code', str(choice)))
                    combo.addItem(display_name, code)
            else:
                for choice in choices:
                    combo.addItem(str(choice), str(choice))
            combo.currentIndexChanged.connect(lambda idx, n=name, c=combo: self._on_option_changed(n, str(c.currentData())))
            self.option_widgets[name] = combo
            return combo
        # Freeform text (fallback)
        if opt_type == 'text':
            line = QLineEdit()
            line.setMinimumHeight(32)
            line.textChanged.connect(lambda text, n=name: self._on_option_changed(n, text))
            self.option_widgets[name] = line
            return line
        return None
    
    def _on_quantity_changed(self):
        """Handle quantity selection change."""
        if hasattr(self, 'quantity_spin'):
            value = self.quantity_spin.value()
            self.quantity = value
            self._update_total_price()
            self._update_model_number_label()
    
    def _on_option_changed(self, option_name: str, value):
        """Handle option change."""
        try:
            print(f"[DEBUG] UI _on_option_changed: {option_name} = {value} (type: {type(value)})")
            
            # Check if this is a material change
            if option_name == 'Material':
                print(f"[DEBUG] Material changed to: {value}")
                
                # Get the default length for this material
                material_default_length = get_material_default_length(value)
                print(f"[DEBUG] Material default length for {value}: {material_default_length}")
                
                # Immediately reset the probe length to the material's default
                self._reset_probe_length_to_material_default(material_default_length)
            
            self.config_service.set_option(option_name, value)
            print(f"[DEBUG] UI _on_option_changed: selected_options after set: {self.config_service.current_config.selected_options if self.config_service.current_config else None}")
            self._update_total_price()
            self._update_model_number_label()
        except Exception as e:
            import traceback
            print(f"[DEBUG] Exception in _on_option_changed: {e}")
            print(traceback.format_exc())
            logger.error(f"Error updating option {option_name}: {e}")
    
    def _handle_deferred_changes(self):
        """Handle material and model changes that were deferred during setup."""
        # Process any deferred model change
        if self._pending_model_base_length is not None and self._model_changed_during_setup:
            print(f"[DEBUG] Processing deferred model change, resetting probe length to: {self._pending_model_base_length}")
            self._reset_probe_length_to_specific_base(self._pending_model_base_length)
            self._model_changed_during_setup = False
            self._pending_model_base_length = None
    
    def _reset_probe_length_to_base(self):
        """Reset the probe length to the base length for the current product."""
        try:
            if not self.config_service.current_config:
                print("[DEBUG] No current configuration, cannot reset probe length")
                return
            
            # Get the base length from the current product
            base_length = self.config_service.current_config.base_product.get('base_length', 10)
            print(f"[DEBUG] Resetting probe length to base length: {base_length}")
            
            # Find the probe length widget and update it
            probe_length_widget = self.option_widgets.get('Probe Length')
            if probe_length_widget and hasattr(probe_length_widget, 'setValue'):
                print(f"[DEBUG] Updating probe length widget to: {base_length}")
                probe_length_widget.setValue(base_length)
                # Update the configuration service
                self.config_service.set_option('Probe Length', base_length)
                print(f"[DEBUG] Probe length reset to base length: {base_length}")
            else:
                print(f"[DEBUG] Probe length widget not found or not a spin box")
                
        except Exception as e:
            print(f"[DEBUG] Error resetting probe length: {e}")
            import traceback
            traceback.print_exc()
    
    def _reset_probe_length_to_specific_base(self, base_length):
        """Reset the probe length to a specific base length value."""
        try:
            print(f"[DEBUG] Resetting probe length to specific base length: {base_length}")
            
            # Find the probe length widget and update it
            probe_length_widget = self.option_widgets.get('Probe Length')
            if probe_length_widget and hasattr(probe_length_widget, 'setValue'):
                print(f"[DEBUG] Updating probe length widget to: {base_length}")
                probe_length_widget.setValue(base_length)
                # Update the configuration service
                self.config_service.set_option('Probe Length', base_length)
                print(f"[DEBUG] Probe length reset to specific base length: {base_length}")
            else:
                print(f"[DEBUG] Probe length widget not found or not a spin box")
                
        except Exception as e:
            print(f"[DEBUG] Error resetting probe length to specific base: {e}")
            import traceback
            traceback.print_exc()
    
    def _reset_probe_length_to_material_default(self, material_default_length):
        """Reset the probe length to the default length for the given material."""
        try:
            print(f"[DEBUG] Resetting probe length to material default: {material_default_length}")
            print(f"[DEBUG] Available option widgets: {list(self.option_widgets.keys())}")
            
            # Find the probe length widget and update it
            probe_length_widget = self.option_widgets.get('Probe Length')
            print(f"[DEBUG] Probe length widget found: {probe_length_widget}")
            
            if probe_length_widget and hasattr(probe_length_widget, 'setValue'):
                print(f"[DEBUG] Updating probe length widget to material default: {material_default_length}")
                probe_length_widget.setValue(material_default_length)
                # Update the configuration service
                self.config_service.set_option('Probe Length', material_default_length)
                print(f"[DEBUG] Probe length reset to material default: {material_default_length}")
            else:
                print(f"[DEBUG] Probe length widget not found or not a spin box")
                print(f"[DEBUG] Widget type: {type(probe_length_widget) if probe_length_widget else 'None'}")
                print(f"[DEBUG] Has setValue: {hasattr(probe_length_widget, 'setValue') if probe_length_widget else False}")
                
        except Exception as e:
            print(f"[DEBUG] Error resetting probe length to material default: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_total_price(self):
        """Update price display using modern PriceDisplay component in header only."""
        try:
            if self.config_service.current_config:
                total_price = self.config_service.get_final_price() * self.quantity
                self.total_price_display.setText(f"Total: ${total_price:.2f}")
        except Exception as e:
            logger.error(f"Error updating price: {e}")
    
    def _set_default_values(self, family_name: str):
        """Set default values for the product family, only if valid for the current product."""
        print(f"[DEBUG] UI _set_default_values called for family: {family_name}")
        default_configs = {
            "LS2000": {"Voltage": "115VAC", "Material": "S"},
            "LS2100": {"Voltage": "115VAC", "Material": "S"},
            "LS1000": {"Voltage": "24VDC", "Material": "S"},
            "LS6000": {"Voltage": "115VAC", "Material": "S"},
            "LS7000": {"Voltage": "115VAC", "Material": "S"},
            "LS7000/2": {"Voltage": "115VAC", "Material": "S"},
            "LS7500": {"Voltage": "115VAC", "Material": "S"},
            "LS8000": {"Voltage": "115VAC", "Material": "S"},
            "LS8500": {"Voltage": "115VAC", "Material": "S"},
            "LT9000": {"Voltage": "115VAC", "Material": "S"},
            "FS10000": {"Voltage": "115VAC", "Material": "S"},
        }
        defaults = default_configs.get(family_name, {})
        for option_name, default_value in defaults.items():
            widget = self.option_widgets.get(option_name)
            print(f"[DEBUG] UI _set_default_values: {option_name} = {default_value} (type: {type(default_value)})")
            if widget:
                # For combo boxes
                if isinstance(widget, QComboBox):
                    idx = widget.findData(default_value)
                    if idx >= 0:
                        print(f"[DEBUG] Setting QComboBox {option_name} to index {idx} (value: {default_value})")
                        widget.setCurrentIndex(idx)
                        self._on_option_changed(option_name, default_value)
                # For radio button groups
                elif isinstance(widget, QButtonGroup):
                    for btn in widget.buttons():
                        if btn.property('choice_code') == default_value:
                            print(f"[DEBUG] Setting QButtonGroup {option_name} to {default_value}")
                            btn.setChecked(True)
                            self._on_option_changed(option_name, default_value)
                            break
    
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
        # Modern components handle their own styling
        pass

    def _update_model_number_label(self):
        if self.config_service.current_config:
            model_number = self.config_service.generate_model_number()
            self.model_number_label.setText(model_number)
        else:
            self.model_number_label.setText("")

    def _show_error_message(self, message):
        # Clear the config layout and show an error message
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        error_label = QLabel(message)
        error_label.setStyleSheet('color: red; font-weight: bold; font-size: 16px;')
        self.config_layout.addWidget(error_label)

    def _update_price(self):
        """Update the total price based on current selections."""
        try:
            if not self.config_service.current_config:
                return

            # Get current selections
            selected_options = self.config_service.current_config.selected_options
            print(f"[DEBUG] _update_price() - selected_options: {selected_options}")
            
            # Check for U or T materials specifically
            material = selected_options.get('Material')
            length = selected_options.get('Length')
            if material in ['U', 'T'] and material and length:
                print(f"[DEBUG] U/T MATERIAL DETECTED - Material: {material}, Length: {length}")
                
                # Get product family for length adder calculation
                product_family = self.config_service.current_config.product_family_name
                print(f"[DEBUG] Product family for length adder: {product_family}")
                
                # Calculate length adder manually to verify
                if product_family:
                    try:
                        length_adder = self.product_service.calculate_length_price(
                            product_family, str(material), float(length)
                        )
                        print(f"[DEBUG] Manual length adder calculation: ${length_adder:.2f}")
                    except Exception as e:
                        print(f"[DEBUG] Error calculating length adder: {e}")

            # Calculate price using configuration service
            price = self.config_service.get_final_price()
            print(f"[DEBUG] Final calculated price: ${price:.2f}")
            
            # Update price display
            self.total_price_display.setText(f"Total: ${price:.2f}")
            
        except Exception as e:
            print(f"[DEBUG] Error in _update_price: {e}")
            import traceback
            traceback.print_exc() 