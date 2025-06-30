"""
Modern Product Selection Dialog

A modern, professional product selection and configuration dialog
that integrates with the existing business logic and services.
"""

import logging
from typing import Dict, List, Optional, Any

from PySide6.QtCore import Qt, Signal, QTimer, QObject, QEvent
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QFrame,
    QScrollArea, QWidget, QGroupBox, QListWidget, QListWidgetItem,
    QMessageBox, QProgressBar, QSplitter, QTextEdit, QDoubleSpinBox,
    QCheckBox, QRadioButton, QButtonGroup
)
from PySide6.QtGui import QFont, QPalette

# Import existing business logic (unchanged)
from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from src.core.config.material_defaults import get_material_default_length

# Import modern components
from src.ui.components import (
    ModernButton, ModernLineEdit, ModernTextEdit, ModernComboBox,
    ModernSpinBox, ModernCheckBox, ModernRadioButton, PriceDisplay
)

# Import modern theme
from src.ui.theme import COLORS, FONTS, SPACING, RADIUS, get_button_style, get_input_style, get_card_style

logger = logging.getLogger(__name__)


class EnterKeyFilter(QObject):
    """Filter to handle Enter key presses in the dialog."""
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            # Find the Add to Quote button and trigger it
            dialog = obj
            if hasattr(dialog, 'add_button') and dialog.add_button.isEnabled():
                dialog.add_button.click()
                return True
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
        
        # Apply modern styling
        self._apply_modern_styling()
    
    def _apply_modern_styling(self):
        """Apply modern styling using the centralized theme system."""
        # Dialog background
        dialog_style = f"""
        QDialog {{
            background-color: {COLORS['bg_secondary']};
            border-radius: {RADIUS['lg']}px;
        }}
        """
        
        # Panel styling
        panel_style = f"""
        QFrame {{
            background-color: {COLORS['bg_primary']};
            border-radius: {RADIUS['lg']}px;
            border: 2px solid {COLORS['border_light']};
        }}
        """
        
        # List widget styling
        list_style = f"""
        QListWidget {{
            border: 2px solid {COLORS['border_light']};
            border-radius: {RADIUS['md']}px;
            background-color: {COLORS['bg_primary']};
            padding: {SPACING['md']}px;
            margin-top: {SPACING['sm']}px;
        }}
        QListWidget::item {{
            padding: {SPACING['lg']}px;
            border-bottom: 1px solid {COLORS['gray_100']};
            border-radius: {RADIUS['sm']}px;
            margin: 2px 0px;
        }}
        QListWidget::item:selected {{
            background-color: {COLORS['primary']};
            color: white;
            border: 2px solid {COLORS['primary']};
        }}
        QListWidget::item:hover {{
            background-color: {COLORS['gray_100']};
            border: 1px solid {COLORS['border_light']};
        }}
        """
        
        # Scroll area styling
        scroll_style = f"""
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QScrollBar:vertical {{
            background-color: {COLORS['gray_100']};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {COLORS['gray_300']};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['gray_400']};
        }}
        """
        
        # Button styling
        button_style = f"""
        QPushButton {{
            padding: {SPACING['md']}px {SPACING['lg']}px;
            border: none;
            border-radius: {RADIUS['md']}px;
            font-weight: {FONTS['weights']['semibold']};
            font-size: {FONTS['sizes']['base']}px;
            font-family: {FONTS['family']};
            min-height: 32px;
            max-height: 32px;
        }}
        QPushButton[text="Cancel"] {{
            background-color: {COLORS['secondary']};
            color: {COLORS['text_secondary']};
            border: 2px solid {COLORS['border_light']};
        }}
        QPushButton[text="Cancel"]:hover {{
            background-color: {COLORS['secondary_hover']};
            border-color: {COLORS['border_medium']};
        }}
        QPushButton[text="Add to Quote"] {{
            background-color: {COLORS['primary']};
            color: white;
        }}
        QPushButton[text="Add to Quote"]:hover {{
            background-color: {COLORS['primary_hover']};
        }}
        QPushButton[text="Add to Quote"]:disabled {{
            background-color: {COLORS['gray_400']};
            color: {COLORS['gray_100']};
        }}
        """
        
        # Label styling
        label_style = f"""
        QLabel {{
            font-family: {FONTS['family']};
            color: {COLORS['text_primary']};
        }}
        """
        
        # Combine all styles
        combined_style = dialog_style + panel_style + list_style + scroll_style + button_style + label_style
        self.setStyleSheet(combined_style)
    
    def _setup_ui(self):
        """Setup the UI layout."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(SPACING['2xl'])
        main_layout.setContentsMargins(SPACING['2xl'], SPACING['2xl'], SPACING['2xl'], SPACING['2xl'])
        
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
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(SPACING['2xl'], SPACING['2xl'], SPACING['2xl'], SPACING['2xl'])
        layout.setSpacing(SPACING['xl'])
        
        # Header
        header_label = QLabel("Select Product Family")
        header_label.setStyleSheet(f"""
            font-size: {FONTS['sizes']['xl']}px;
            font-weight: {FONTS['weights']['bold']};
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['sm']}px;
        """)
        layout.addWidget(header_label)
        
        # Product list
        self.product_list = QListWidget()
        self.product_list.itemClicked.connect(self._on_product_selected)
        layout.addWidget(self.product_list)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Create right panel for configuration."""
        panel = QFrame()
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(SPACING['2xl'], SPACING['2xl'], SPACING['2xl'], SPACING['2xl'])
        layout.setSpacing(SPACING['xl'])
        
        # Header area with total price
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Model number label (dynamic)
        self.model_number_label = QLabel("")
        self.model_number_label.setStyleSheet(f"""
            font-size: {FONTS['sizes']['2xl']}px;
            font-weight: {FONTS['weights']['bold']};
            color: {COLORS['text_primary']};
        """)
        header_layout.addWidget(self.model_number_label)
        
        header_layout.addStretch()
        
        # Total price display
        self.total_price_display = QLabel("Total: $0.00")
        self.total_price_display.setStyleSheet(f"""
            font-size: {FONTS['sizes']['xl']}px;
            font-weight: {FONTS['weights']['bold']};
            background: {COLORS['success_light']};
            border-radius: {RADIUS['md']}px;
            padding: {SPACING['sm']}px {SPACING['lg']}px;
            color: {COLORS['success']};
        """)
        header_layout.addWidget(self.total_price_display)
        
        layout.addLayout(header_layout)
        
        # Scrollable configuration area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.config_container = QWidget()
        self.config_layout = QVBoxLayout(self.config_container)
        self.config_layout.setSpacing(SPACING['lg'])
        self.config_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area.setWidget(self.config_container)
        layout.addWidget(scroll_area)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(SPACING['md'])
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        # Add to Quote button
        self.add_button = QPushButton("Add to Quote")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._on_add_to_quote)
        button_layout.addWidget(self.add_button)
        layout.addLayout(button_layout)

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
            vbox.setSpacing(SPACING['lg'])
            vbox.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
            default_values_to_set = []
            # --- VOLTAGE SECTION FIRST ---
            voltage_opt = next((o for o in ordered_core if o.get('name') == 'Voltage'), None)
            if voltage_opt:
                voltage_form = QFormLayout()
                voltage_form.setSpacing(SPACING['md'])
                voltage_form.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
                widget = self._create_dynamic_option_widget(voltage_opt, force_dropdown=False)
                if widget:
                    label = QLabel(voltage_opt.get('name', ''))
                    label.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['semibold']};
                        color: {COLORS['text_primary']};
                    """)
                    voltage_form.addRow(label, widget)
                    default_val = voltage_opt.get('default')
                    if default_val is not None:
                        default_values_to_set.append((voltage_opt.get('name'), default_val, widget))
                voltage_group = QGroupBox('Electrical')
                voltage_group.setStyleSheet(f"""
                    font-weight: {FONTS['weights']['bold']};
                    font-size: {FONTS['sizes']['base']}px;
                """)
                voltage_group.setLayout(voltage_form)
                vbox.addWidget(voltage_group)
            # --- PROBE SECTION: Material + Probe Length together ---
            probe_form = QFormLayout()
            probe_form.setSpacing(SPACING['md'])
            probe_form.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
            for name in ['Material', 'Probe Length']:
                opt = next((o for o in ordered_core if o.get('name') == name), None)
                if opt:
                    widget = self._create_dynamic_option_widget(opt, force_dropdown=False)
                    if widget:
                        label = QLabel(opt.get('name', ''))
                        label.setStyleSheet(f"""
                            font-weight: {FONTS['weights']['semibold']};
                            color: {COLORS['text_primary']};
                        """)
                        probe_form.addRow(label, widget)
                        default_val = opt.get('default')
                        if default_val is not None:
                            default_values_to_set.append((opt.get('name'), default_val, widget))
            probe_group = QGroupBox('Probe')
            probe_group.setStyleSheet(f"""
                font-weight: {FONTS['weights']['bold']};
                font-size: {FONTS['sizes']['base']}px;
            """)
            probe_group.setLayout(probe_form)
            vbox.addWidget(probe_group)
            # --- INSULATOR SECTION: Insulator Material + Insulator Length ---
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
            # --- CONNECTIONS SECTION ---
            if 'Connections' in options_by_category:
                opts = [opt for opt in options_by_category['Connections'] if opt.get('name') not in ['Voltage', 'Material', 'Probe Length', 'Insulator Material', 'Insulator Length']]
                if opts:
                    group = QGroupBox('Connections')
                    group.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['bold']};
                        font-size: {FONTS['sizes']['base']}px;
                    """)
                    combo_style = f"""
                        QComboBox {{
                            border: 1px solid {COLORS['border_light']};
                            border-radius: {RADIUS['md']}px;
                            padding: {SPACING['md']}px;
                            min-height: 32px;
                            background-color: {COLORS['bg_primary']};
                        }}
                        QComboBox:focus {{
                            border-color: {COLORS['primary']};
                        }}
                    """
                    form = QFormLayout()
                    form.setSpacing(SPACING['md'])
                    form.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
                    # Find the Connection Type option
                    connection_type_option = next((o for o in opts if o.get('name') == 'Connection Type'), None)
                    sub_option_map = {
                        'NPT': ['NPT Size'],
                        'Flange': ['Flange Type', 'Flange Rating', 'Flange Size'],
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
                    # Build a lookup for options by name
                    opts_by_name = {opt.get('name'): opt for opt in opts if opt.get('name') != 'Connection Type'}
                    # Add widgets in the order specified by sub_option_map
                    for name in sub_option_map.get('Flange', []):
                        opt = opts_by_name.get(name)
                        if not opt:
                            continue
                        choices = opt.get('choices', [])
                        adders = opt.get('adders', {})
                        combo = QComboBox()
                        combo.setFixedWidth(200)
                        combo.setMinimumHeight(32)
                        combo.setStyleSheet(combo_style)
                        # Special handling for Flange Type descriptive labels
                        if name == 'Flange Type' and choices:
                            label_map = {'SS': 'SS - Stainless Steel', 'CS': 'CS - Carbon Steel'}
                            for choice in choices:
                                display = label_map.get(choice, str(choice))
                                combo.addItem(display, choice)
                        elif choices and isinstance(choices[0], dict):
                            for choice in choices:
                                display_name = choice.get('display_name', choice.get('code', str(choice)))
                                code = choice.get('code', str(choice))
                                combo.addItem(display_name, code)
                        elif choices:
                            for choice in choices:
                                combo.addItem(str(choice), str(choice))
                        label = QLabel(name)
                        form.addRow(label, combo)
                        # Store both label and combo together
                        sub_option_widgets[name] = (label, combo)
                        label.hide()
                        combo.hide()
                    # Add any other sub-options not in sub_option_map (fallback, rare)
                    for sub_opt in opts:
                        name = sub_opt.get('name')
                        if name == 'Connection Type' or name in sub_option_widgets:
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
                        label = QLabel(name)
                        form.addRow(label, combo)
                        sub_option_widgets[name] = (label, combo)
                        label.hide()
                        combo.hide()
                    def on_conn_type_changed(idx):
                        selected_type = conn_type_combo.currentData() if conn_type_combo else ''
                        if not isinstance(selected_type, str):
                            selected_type = str(selected_type) if selected_type is not None else ''
                        # Hide all sub-options first
                        for label, w in sub_option_widgets.values():
                            label.hide()
                            w.hide()
                        # Show only relevant sub-options
                        if selected_type in sub_option_map:
                            for name in sub_option_map[selected_type]:
                                if name in sub_option_widgets:
                                    label, w = sub_option_widgets[name]
                                    label.show()
                                    w.show()
                    if conn_type_combo:
                        conn_type_combo.currentIndexChanged.connect(on_conn_type_changed)
                        # Show sub-options for default selection
                        on_conn_type_changed(conn_type_combo.currentIndex())
                    group.setLayout(form)
                    vbox.addWidget(group)
            # --- ACCESSORIES SECTION ---
            if 'Accessories' in options_by_category:
                opts = [opt for opt in options_by_category['Accessories'] if opt.get('name') not in ['O-Rings']]
                if opts:
                    group = QGroupBox('Accessories')
                    group.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['bold']};
                        font-size: {FONTS['sizes']['base']}px;
                    """)
                    form = QFormLayout()
                    form.setSpacing(SPACING['md'])
                    form.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
                    for option in opts:
                        name = option.get('name', '')
                        cb = QCheckBox()
                        cb.setChecked(False)
                        cb.stateChanged.connect(lambda state, n=name: self._on_option_changed(n, bool(state)))
                        self.option_widgets[name] = cb
                        label = QLabel(name)
                        label.setStyleSheet(f"""
                            font-weight: {FONTS['weights']['semibold']};
                            color: {COLORS['text_primary']};
                        """)
                        form.addRow(label, cb)
                    group.setLayout(form)
                    vbox.addWidget(group)
            # --- O-RING MATERIAL SECTION AT THE END ---
            o_ring_opt = None
            if 'O-ring Material' in options_by_category:
                for opt in options_by_category['O-ring Material']:
                    if opt.get('name') == 'O-Rings':
                        o_ring_opt = opt
                        break
            if o_ring_opt:
                o_ring_form = QFormLayout()
                o_ring_form.setSpacing(SPACING['md'])
                o_ring_form.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
                widget = self._create_dynamic_option_widget(o_ring_opt, force_dropdown=False)
                if widget:
                    label = QLabel(o_ring_opt.get('name', ''))
                    label.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['semibold']};
                        color: {COLORS['text_primary']};
                    """)
                    o_ring_form.addRow(label, widget)
                o_ring_group = QGroupBox('O-ring Material')
                o_ring_group.setStyleSheet(f"""
                    font-weight: {FONTS['weights']['bold']};
                    font-size: {FONTS['sizes']['base']}px;
                """)
                o_ring_group.setLayout(o_ring_form)
                vbox.addWidget(o_ring_group)
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
            
            # After rendering all other sections, render the Insulator section if needed
            if insulator_material_option or insulator_length_option:
                ins_group = QGroupBox('Insulator')
                ins_group.setStyleSheet(f"""
                    font-weight: {FONTS['weights']['bold']};
                    font-size: {FONTS['sizes']['base']}px;
                """)
                ins_form = QFormLayout()
                ins_form.setSpacing(SPACING['md'])
                ins_form.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
                if insulator_material_option:
                    widget = self._create_dynamic_option_widget(insulator_material_option, force_dropdown=True)
                    if widget:
                        label = QLabel(insulator_material_option.get('name', ''))
                        label.setStyleSheet(f"""
                            font-weight: {FONTS['weights']['semibold']};
                            color: {COLORS['text_primary']};
                        """)
                        ins_form.addRow(label, widget)
                if insulator_length_option:
                    widget = self._create_dynamic_option_widget(insulator_length_option, force_dropdown=True)
                    if widget:
                        label = QLabel(insulator_length_option.get('name', ''))
                        label.setStyleSheet(f"""
                            font-weight: {FONTS['weights']['semibold']};
                            color: {COLORS['text_primary']};
                        """)
                        ins_form.addRow(label, widget)
                ins_group.setLayout(ins_form)
                vbox.addWidget(ins_group)
            
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
        combo_style = f"""
            QComboBox {{
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px;
                min-height: 32px;
                background-color: {COLORS['bg_primary']};
            }}
            QComboBox:focus {{
                border-color: {COLORS['primary']};
            }}
        """
        spin_style = f"""
            QSpinBox {{
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px;
                min-height: 32px;
                background-color: {COLORS['bg_primary']};
                font-size: {FONTS['sizes']['base']}px;
            }}
            QSpinBox:focus {{
                border-color: {COLORS['primary']};
            }}
        """
        # Force dropdown if force_dropdown is set, regardless of number of choices
        if force_dropdown and choices:
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
            layout.setSpacing(SPACING['md'])
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
        # Flange Type: show descriptive labels
        if name == 'Flange Type' and choices:
            combo = QComboBox()
            combo.setFixedWidth(200)
            combo.setMinimumHeight(32)
            combo.setStyleSheet(combo_style)
            label_map = {'SS': 'SS - Stainless Steel', 'CS': 'CS - Carbon Steel'}
            for choice in choices:
                display = label_map.get(choice, str(choice))
                combo.addItem(display, choice)
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
        error_label.setStyleSheet(f"""
            color: {COLORS['error']};
            font-weight: {FONTS['weights']['bold']};
            font-size: {FONTS['sizes']['base']}px;
        """)
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