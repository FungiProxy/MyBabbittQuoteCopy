"""
Modern Product Selection Dialog

A modern, professional product selection and configuration dialog
that integrates with the existing business logic and services.
"""

import logging
import traceback
from typing import Dict, List, Optional, Any

from PySide6.QtCore import Qt, Signal, QTimer, QObject, QEvent
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QFrame,
    QScrollArea, QWidget, QGroupBox, QListWidget, QListWidgetItem,
    QMessageBox, QProgressBar, QSplitter, QTextEdit, QDoubleSpinBox,
    QCheckBox, QRadioButton, QButtonGroup, QMenu
)
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtCore import Signal, QTimer, QObject, QEvent, QSize

# Import existing business logic (unchanged)
from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from src.core.services.spare_part_service import SparePartService
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
    """Filter to handle Enter key presses in the dialog globally."""
    
    def __init__(self):
        super().__init__()
        self._last_click_time = 0  # Track last click time to prevent double-clicks
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            # Check if the focused widget is a form input
            focused_widget = obj.focusWidget()
            if focused_widget:
                # If the focused widget is a form input, don't trigger the Add to Quote button
                # This includes all types of input widgets that should handle Enter themselves
                if (isinstance(focused_widget, (QSpinBox, QDoubleSpinBox, QLineEdit, QTextEdit)) or
                    (isinstance(focused_widget, QComboBox) and focused_widget.isEditable())):
                    # Let the form input handle the Enter key naturally
                    return False
                
                # Also check if the focused widget has the event filter installed
                # This catches any custom input widgets that might have been missed
                if hasattr(focused_widget, 'installEventFilter'):
                    return False
            
            # If not in a form input, trigger the Add to Quote button
            dialog = obj
            if hasattr(dialog, 'add_button') and dialog.add_button.isEnabled():
                # Add debug logging
                logger.info("EnterKeyFilter: Triggering add_button.click()")
                dialog.add_button.click()
                return True
        return super().eventFilter(obj, event)


class ExoticMetalAdderSpinBox(QDoubleSpinBox):
    """Custom spin box for exotic metal adders that prevents Enter from closing the dialog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            # Consume the Enter key event to prevent dialog from closing
            event.accept()
            # Optionally trigger the value change
            self.clearFocus()
        else:
            super().keyPressEvent(event)


class ProtectedSpinBox(QSpinBox):
    """SpinBox that prevents Enter key from closing the dialog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            # Consume the Enter key event to prevent dialog from closing
            event.accept()
            # Optionally trigger the value change
            self.clearFocus()
        else:
            super().keyPressEvent(event)


class ProtectedLineEdit(QLineEdit):
    """LineEdit that prevents Enter key from closing the dialog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            # Consume the Enter key event to prevent dialog from closing
            event.accept()
            # Optionally trigger the value change
            self.clearFocus()
        else:
            super().keyPressEvent(event)


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
    instance_counter = 0
    
    def __init__(self, product_service: ProductService, parent=None, product_to_edit=None):
        super().__init__(parent)
        ModernProductSelectionDialog.instance_counter += 1
        self._instance_id = ModernProductSelectionDialog.instance_counter
        logger.info(f"ModernProductSelectionDialog __init__ (instance {self._instance_id})")
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
        
        # Add flag to prevent multiple calls to _on_add_to_quote
        self._adding_to_quote = False
        
        # Initialize configuration service
        self.config_service = ConfigurationService(self.db, self.product_service)
        
        # Setup UI
        self._setup_ui()
        
        # Connect signals after UI is set up
        self.product_list.itemSelectionChanged.connect(self._on_product_selected)
        self.add_button.clicked.connect(self._on_add_to_quote)
        logger.info(f"Connected add_button.clicked to _on_add_to_quote (instance {self._instance_id})")
        # self.installEventFilter(self.enter_key_filter)  # Temporarily disabled to test double-add issue
        
        # Load product list
        self._load_product_list()
        
        # Load product for editing if provided
        if self.product_to_edit:
            self._load_product_for_editing()
        
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
        header_label = QLabel("Select Model")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(f"""
            font-size: {FONTS['sizes']['xl']}px;
            font-weight: {FONTS['weights']['bold']};
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['sm']}px;
            padding: {SPACING['xs']}px {SPACING['sm']}px;
            border: 1px solid {COLORS['border_light']};
            border-radius: {RADIUS['sm']}px;
            background-color: {COLORS['bg_primary']};
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
        
        # Ensure only one add_button exists
        if hasattr(self, 'add_button'):
            logger.warning('add_button already exists! Removing previous instance.')
            self.add_button.deleteLater()
            del self.add_button
        self.add_button = QPushButton("Add to Quote")
        self.add_button.setEnabled(False)
        self.add_button.setAutoDefault(False)
        self.add_button.setDefault(False)
        # Signal is already connected in __init__, don't connect again
        logger.info(f"Recreated add_button (instance {self._instance_id})")
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
                item = QListWidgetItem("Spare Parts")
                item.setToolTip("Browse and add spare parts to your quote")
                item.setData(Qt.ItemDataRole.UserRole, spare_parts_family)
                item.setBackground(QColor("#f8f9fa"))
                item.setForeground(QColor("#6c757d"))
                self.product_list.addItem(item)
        except Exception as e:
            logger.error(f"Error populating product list: {e}", exc_info=True)
    
    def _on_product_selected(self):
        """Handle product selection."""
        items = self.product_list.selectedItems()
        if not items:
            return
        product_data = items[0].data(Qt.ItemDataRole.UserRole)
        # # print(f"[DEBUG] Product selected: {product_data}")
        selected_name = product_data.get('name', '')

        # Check if this is the special "Spare Parts" selection
        if product_data.get('is_spare_parts'):
            self._show_spare_parts_interface()
            return

        # PATCH: Special handling for TRAN-EX family
        if selected_name == "TRAN-EX":
            # Hardcode the correct model number for TRAN-EX
            base_product_info = self.db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
            if base_product_info:
                # print(f"[PATCH] Using TRAN-EX base product: {base_product_info.model_number} (ID: {base_product_info.id})")
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
                # print("[PATCH] TRAN-EX base product not found!")
                pass
        else:
            base_product_info = self.product_service.get_base_product_for_family(self.db, selected_name)
            if base_product_info:
                # print(f"[DEBUG] Base product info: {base_product_info}")
                product_data = base_product_info
                pass
            else:
                # print(f"[WARNING] No base product found for {selected_name}, using family info")
                pass

        # Set flag for model change and store the base length
        self._model_changed_during_setup = True
        self._pending_model_base_length = product_data.get('base_length', 10)
        # print(f"[DEBUG] Model changed, base length will be reset to: {self._pending_model_base_length}")

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
            # print(f"[DEBUG] Passing selected_options to start_configuration: {selected_options}")
            pass
            self.config_service.start_configuration(
                product_family_id=product_data.get('id', 1),
                product_family_name=selected_name,
                base_product_info=product_data,
                selected_options=selected_options,
            )
            self._show_product_config(product_data)
        except Exception as e:
            import traceback
            # print(f"[DEBUG] Exception in _on_product_selected: {e}")
            # print(traceback.format_exc())
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
            # print(f"[DEBUG] Gathering core options for: {product.get('name', '')}")
            # Voltage - skip for TRAN-EX since it has no voltage options
            if product.get('name') != 'TRAN-EX':
                voltages = self.product_service.get_available_voltages(self.db, product.get('name', ''))
                # print(f"[DEBUG] Voltages for {product.get('name', '')}: {voltages}")
                if voltages:
                    core_options.append({
                        'name': 'Voltage',
                        'choices': voltages,
                        'adders': {},
                        'category': 'Electrical',
                    })
                    seen_option_names.add('Voltage')
            else:
                # print(f"[DEBUG] Skipping voltage for TRAN-EX - no voltage options")
                pass
            # Material
            if product.get('name') == 'TRAN-EX':
                # Always force Material to be a dropdown for TRAN-EX
                core_options.append({
                    'name': 'Material',
                    'choices': [
                        {'code': 'S', 'display_name': 'S - 316 Stainless Steel'},
                        {'code': 'H', 'display_name': 'H - Halar'}
                    ],
                    'adders': {},
                    'category': 'Material',
                    'default': 'S',
                    'type': 'dropdown',
                })
                seen_option_names.add('Material')
            else:
                materials = self.product_service.get_available_materials_for_product(self.db, product.get('name', ''))
                if materials:
                    material_option = materials[0]
                    # Set default to first available material code if present
                    choices = material_option.get('choices', [])
                    if choices and isinstance(choices[0], dict) and 'code' in choices[0]:
                        material_option['default'] = choices[0]['code']
                    elif choices and isinstance(choices[0], str):
                        material_option['default'] = choices[0]
                    material_option['category'] = 'Material'
                    core_options.append(material_option)
                    seen_option_names.add('Material')
            # Special handling for TRAN-EX (fixed material)
            # elif product.get('name') == 'TRAN-EX':
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
            # print(f"[ERROR] Exception gathering core options for {product.get('name', '')}: {e}")
            import traceback
            # print(traceback.format_exc())
            self._show_error_message(f"Error gathering core options: {e}")
            return
        # Additional options
        try:
            # print(f"[DEBUG] Gathering additional options for: {product.get('name', '')}")
            additional_options = self.product_service.get_additional_options(self.db, product.get('name', ''))
            # print(f"[DEBUG] Additional options: {additional_options}")
        except Exception as e:
            # print(f"[ERROR] Exception gathering additional options for {product.get('name', '')}: {e}")
            import traceback
            # print(traceback.format_exc())
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
        
        print(f"[DEBUG] Options by category: {list(options_by_category.keys())}")
        if 'Housing' in options_by_category:
            print(f"[DEBUG] Housing options found: {[opt.get('name') for opt in options_by_category['Housing']]}")
        else:
            print(f"[DEBUG] No Housing category found in options_by_category")
            pass
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
            
            # Handle Material with potential exotic metal adder
            material_opt = next((o for o in ordered_core if o.get('name') == 'Material'), None)
            if material_opt:
                # Create a horizontal layout for Material and potential adder
                material_row = QHBoxLayout()
                material_row.setSpacing(SPACING['md'])
                
                # Material dropdown
                material_widget = self._create_dynamic_option_widget(material_opt, force_dropdown=False)
                if material_widget:
                    material_label = QLabel(material_opt.get('name', ''))
                    material_label.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['semibold']};
                        color: {COLORS['text_primary']};
                    """)
                    material_row.addWidget(material_label)
                    material_row.addWidget(material_widget)
                    
                    # Exotic metal price adder field
                    self.exotic_metal_adder_label = QLabel('Price Adder ($)')
                    self.exotic_metal_adder_label.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['semibold']};
                        color: {COLORS['text_primary']};
                    """)
                    self.exotic_metal_adder_spin = ExoticMetalAdderSpinBox()
                    self.exotic_metal_adder_spin.setFixedWidth(120)
                    self.exotic_metal_adder_spin.setMinimumHeight(32)
                    self.exotic_metal_adder_spin.setMinimum(0.0)
                    self.exotic_metal_adder_spin.setMaximum(9999.99)
                    self.exotic_metal_adder_spin.setDecimals(2)
                    self.exotic_metal_adder_spin.setSingleStep(10.0)
                    self.exotic_metal_adder_spin.setStyleSheet(f"""
                        QDoubleSpinBox {{
                            border: 1px solid {COLORS['border_light']};
                            border-radius: {RADIUS['md']}px;
                            padding: {SPACING['md']}px;
                            background-color: {COLORS['bg_primary']};
                            font-size: {FONTS['sizes']['base']}px;
                        }}
                        QDoubleSpinBox:focus {{
                            border-color: {COLORS['primary']};
                        }}
                    """)
                    
                    # Initially hide the adder field
                    self.exotic_metal_adder_label.hide()
                    self.exotic_metal_adder_spin.hide()
                    
                    # Connect the material change to show/hide adder field
                    if hasattr(material_widget, 'currentIndexChanged'):
                        material_widget.currentIndexChanged.connect(self._on_material_changed)
                    
                    # Connect the adder value change
                    self.exotic_metal_adder_spin.valueChanged.connect(self._on_exotic_metal_adder_changed)
                    
                    material_row.addWidget(self.exotic_metal_adder_label)
                    material_row.addWidget(self.exotic_metal_adder_spin)
                    material_row.addStretch()
                    
                    # Add the material row to the form
                    probe_form.addRow(material_row)
                    
                    default_val = material_opt.get('default')
                    if default_val is not None:
                        default_values_to_set.append((material_opt.get('name'), default_val, material_widget))
            
            # Handle Probe Length
            probe_length_opt = next((o for o in ordered_core if o.get('name') == 'Probe Length'), None)
            if probe_length_opt:
                widget = self._create_dynamic_option_widget(probe_length_opt, force_dropdown=False)
                if widget:
                    label = QLabel(probe_length_opt.get('name', ''))
                    label.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['semibold']};
                        color: {COLORS['text_primary']};
                    """)
                    probe_form.addRow(label, widget)
                    default_val = probe_length_opt.get('default')
                    if default_val is not None:
                        default_values_to_set.append((probe_length_opt.get('name'), default_val, widget))
            
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
                    pass
                options_by_category['Connections'] = new_conn_opts
            
            # Render the Insulator section right after Probe section
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
                        # Set default to base model's insulator_material if present
                        if self.config_service.current_config and hasattr(self.config_service.current_config, 'base_product') and self.config_service.current_config.base_product:
                            print(f"[DEBUG] base_product: {self.config_service.current_config.base_product}")
                            base_insulator = self.config_service.current_config.base_product.get('insulator_material')
                        if base_insulator:
                            print(f"[DEBUG] Base insulator material: {base_insulator}")
                            base_insulator_code = base_insulator.strip().upper()
                            found = False
                            for i in range(widget.count()):
                                item_code = str(widget.itemData(i)).strip().upper()
                                print(f"[DEBUG] Checking item {i}: code '{item_code}' against base '{base_insulator_code}'")
                                if item_code == base_insulator_code:
                                    print(f"[DEBUG] Code match found: {item_code}")
                                    widget.setCurrentIndex(i)
                                    found = True
                                    break
                            if not found:
                                print(f"[DEBUG] No code match found for base insulator '{base_insulator_code}', defaulting to first item.")
                                widget.setCurrentIndex(0)
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
                            font-family: {FONTS['family']};
                            font-weight: {FONTS['weights']['semibold']};
                            font-size: {FONTS['sizes']['base']}px;
                            color: {COLORS['text_primary']};
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
                        # For 'Connection Type' label
                        conn_type_label = QLabel('Connection Type')
                        conn_type_label.setStyleSheet(f"""
                            font-weight: {FONTS['weights']['semibold']};
                            color: {COLORS['text_primary']};
                            font-size: {FONTS['sizes']['base']}px;
                        """)
                        form.addRow(conn_type_label, conn_type_combo)
                    else:
                        conn_type_combo = None
                    pass
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
                        label.setStyleSheet(f"""
                            font-weight: {FONTS['weights']['semibold']};
                            color: {COLORS['text_primary']};
                            font-size: {FONTS['sizes']['base']}px;
                        """)
                        form.addRow(label, combo)
                        # Store both label and combo together
                        sub_option_widgets[name] = (label, combo)
                        # Connect the combo box to update configuration
                        combo.currentIndexChanged.connect(
                            lambda idx, n=name, c=combo: self._on_option_changed(n, c.currentData())
                        )
                        label.hide()
                        combo.hide()
                    # Add any other sub-options not in sub_option_map (fallback, rare)
                    for sub_opt in opts:
                        name = sub_opt.get('name')
                        if name == 'Connection Type' or name in sub_option_widgets:
                            continue
                        
                        if name == 'Tri-clamp':
                            # Create custom tri-clamp widget
                            tri_clamp_widget = self._create_tri_clamp_widget(sub_opt)
                            form.addRow(tri_clamp_widget)
                            sub_option_widgets[name] = (None, tri_clamp_widget)  # No label needed
                            tri_clamp_widget.hide()
                        else:
                            # Regular dropdown option
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
                            label.setStyleSheet(f"""
                                font-weight: {FONTS['weights']['semibold']};
                                color: {COLORS['text_primary']};
                                font-size: {FONTS['sizes']['base']}px;
                            """)
                            form.addRow(label, combo)
                            sub_option_widgets[name] = (label, combo)
                            # Connect the combo box to update configuration
                            combo.currentIndexChanged.connect(
                                lambda idx, n=name, c=combo: self._on_option_changed(n, c.currentData())
                            )
                            label.hide()
                            combo.hide()
                    def on_conn_type_changed(idx):
                        selected_type = conn_type_combo.currentData() if conn_type_combo else ''
                        if not isinstance(selected_type, str):
                            selected_type = str(selected_type) if selected_type is not None else ''
                        
                        # Update the configuration service with the new connection type
                        self._on_option_changed("Connection Type", selected_type)
                        
                        # Hide all sub-options first
                        for label, w in sub_option_widgets.values():
                            if label:
                                label.hide()
                            w.hide()
                        # Show only relevant sub-options
                        if selected_type in sub_option_map:
                            for name in sub_option_map[selected_type]:
                                if name in sub_option_widgets:
                                    label, w = sub_option_widgets[name]
                                    if label:
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
                        
                        if name == 'Bent Probe':
                            # Create a horizontal layout for Bent Probe checkbox and degree input
                            bent_row = QHBoxLayout()
                            bent_row.setSpacing(SPACING['md'])
                            
                            # Bent Probe checkbox
                            cb = QCheckBox()
                            cb.setChecked(False)
                            cb.stateChanged.connect(lambda state, n=name: self._on_option_changed(n, bool(state)))
                            self.option_widgets[name] = cb
                            
                            label = QLabel(name)
                            label.setStyleSheet(f"""
                                font-weight: {FONTS['weights']['semibold']};
                                color: {COLORS['text_primary']};
                            """)
                            
                            bent_row.addWidget(label)
                            bent_row.addWidget(cb)
                            
                            # Degree input field (initially hidden, NO label)
                            bent_probe_degree_widget = ProtectedSpinBox()
                            bent_probe_degree_widget.setFixedWidth(120)  # Set width back to 120px
                            bent_probe_degree_widget.setMinimumHeight(32)
                            bent_probe_degree_widget.setMinimum(1)
                            bent_probe_degree_widget.setMaximum(180)
                            bent_probe_degree_widget.setValue(90)  # Default to 90 degrees
                            bent_probe_degree_widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                            bent_probe_degree_widget.setStyleSheet(f"""
                                QSpinBox {{
                                    border: 1px solid {COLORS['border_light']};
                                    border-radius: {RADIUS['md']}px;
                                    padding: 2px 8px;
                                    background-color: {COLORS['bg_primary']};
                                    font-size: 14px;
                                }}
                                QSpinBox:focus {{
                                    border-color: {COLORS['primary']};
                                }}
                            """)
                            
                            # Initially hide the degree input
                            bent_probe_degree_widget.hide()
                            
                            # Connect checkbox to show/hide degree input
                            def on_bent_probe_changed(state):
                                if state:
                                    bent_probe_degree_widget.show()
                                    # Set the degree value when checkbox is checked
                                    self._on_option_changed('Bent Probe Degree', bent_probe_degree_widget.value())
                                else:
                                    bent_probe_degree_widget.hide()
                                    # Clear the degree value when checkbox is unchecked
                                    self._on_option_changed('Bent Probe Degree', None)
                            
                            cb.stateChanged.connect(on_bent_probe_changed)
                            
                            # Connect degree input to update configuration
                            bent_probe_degree_widget.valueChanged.connect(
                                lambda val: self._on_option_changed('Bent Probe Degree', val)
                            )
                            
                            bent_row.addWidget(bent_probe_degree_widget)
                            bent_row.addStretch()
                            
                            # Add the bent probe row to the form
                            form.addRow(bent_row)
                            
                        else:
                            # Regular accessory option (checkbox only)
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
            
            # --- HOUSING SECTION ---
            if 'Housing' in options_by_category:
                housing_opts = options_by_category['Housing']
                if housing_opts:
                    group = QGroupBox('Housing Configuration')
                    group.setStyleSheet(f"""
                        font-weight: {FONTS['weights']['bold']};
                        font-size: {FONTS['sizes']['base']}px;
                    """)
                    form = QFormLayout()
                    form.setSpacing(SPACING['md'])
                    form.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
                    for option in housing_opts:
                        name = option.get('name', '')
                        print(f"[DEBUG][HOUSING] Option: {name}")
                        print(f"[DEBUG][HOUSING] Choices: {option.get('choices', [])} (type: {type(option.get('choices', []))})")
                        print(f"[DEBUG][HOUSING] Option dict: {option}")
                        
                        # Use _create_dynamic_option_widget with force_dropdown=True for housing options
                        widget = self._create_dynamic_option_widget(option, force_dropdown=True)
                        if widget:
                            label = QLabel(name)
                            label.setStyleSheet(f"""
                                font-weight: {FONTS['weights']['semibold']};
                                color: {COLORS['text_primary']};
                            """)
                            form.addRow(label, widget)
                    
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
            
        except Exception as e:
            # print(f"[ERROR] Exception rendering config UI for {product.get('name', '')}: {e}")
            import traceback
            # print(traceback.format_exc())
            self._show_error_message(f"Error rendering config UI: {e}")

    def _create_dynamic_option_widget(self, option, force_dropdown=False):
        """Create the appropriate widget for an option based on its data."""
        # print(f"[DEBUG] _create_dynamic_option_widget called for option: {option.get('name')}")
        # print(f"[DEBUG] Option dict: {option}")
        # print(f"[DEBUG] opt_type: {option.get('type')}")
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
                font-family: {FONTS['family']};
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
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
                    code = str(choice.get('code', str(choice)))
                    display_name = choice.get('display_name', code)
                    # Show both code and display name
                    combo.addItem(f"{code} - {display_name}", code)
            else:
                for choice in choices:
                    combo.addItem(str(choice), str(choice))
            combo.currentIndexChanged.connect(lambda idx, n=name, c=combo: self._on_option_changed(n, str(c.currentData())))
            self.option_widgets[name] = combo
            return combo
        # Probe Length (always numeric input)
        if name == 'Probe Length':
            spin = ProtectedSpinBox()
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
            # Store the widget in option_widgets so it can be found later
            self.option_widgets[name] = spin
            return spin
        # Quantity (special case)
        if name == 'Quantity':
            spin = ProtectedSpinBox()
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
        # Always use QComboBox if type is 'dropdown'
        if opt_type == 'dropdown' and choices:
            combo = QComboBox()
            combo.setFixedWidth(200)
            combo.setMinimumHeight(32)
            combo.setStyleSheet(combo_style)
            if isinstance(choices[0], dict):
                for choice in choices:
                    code = str(choice.get('code', str(choice)))
                    display_name = choice.get('display_name', code)
                    combo.addItem(f"{code} - {display_name}", code)
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
            line = ProtectedLineEdit()
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
                
                # Auto-switch insulator material to Teflon when Halar is selected
                if value == 'H':  # Halar material
                    self._auto_set_insulator_to_teflon()
            
            self.config_service.set_option(option_name, value)
            print(f"[DEBUG] UI _on_option_changed: selected_options after set: {self.config_service.current_config.selected_options if self.config_service.current_config else None}")
            
            # Generate and display the new part number
            new_part_number = self.config_service.generate_model_number()
            print(f"[DEBUG] New part number: {new_part_number}")
            
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
            # print(f"[DEBUG] Processing deferred model change, resetting probe length to: {self._pending_model_base_length}")
            self._reset_probe_length_to_specific_base(self._pending_model_base_length)
            self._model_changed_during_setup = False
            self._pending_model_base_length = None
    
    def _reset_probe_length_to_base(self):
        """Reset the probe length to the base length for the selected product."""
        try:
            base_length = 10
            if (
                self.config_service.current_config
                and getattr(self.config_service.current_config, "base_product", None)
            ):
                base_length = self.config_service.current_config.base_product.get('base_length', 10)

            # Find the probe length widget and update it
            probe_length_widget = self.option_widgets.get('Probe Length')
            if probe_length_widget and hasattr(probe_length_widget, 'setValue'):
                probe_length_widget.setValue(base_length)
                self.config_service.set_option('Probe Length', base_length)
            else:
                pass
        except Exception as e:
            import traceback
            traceback.print_exc()

    def _reset_probe_length_to_specific_base(self, base_length):
        """Reset the probe length to a specific base length value."""
        try:
            # print(f"[DEBUG] Resetting probe length to specific base length: {base_length}")

            # Find the probe length widget and update it
            probe_length_widget = self.option_widgets.get('Probe Length')
            if probe_length_widget and hasattr(probe_length_widget, 'setValue'):
                # print(f"[DEBUG] Updating probe length widget to: {base_length}")
                probe_length_widget.setValue(base_length)
                # Update the configuration service
                self.config_service.set_option('Probe Length', base_length)
                # print(f"[DEBUG] Probe length reset to specific base length: {base_length}")
            else:
                # print(f"[DEBUG] Probe length widget not found or not a spin box")
                pass
        except Exception as e:
            # print(f"[DEBUG] Error resetting probe length to specific base: {e}")
            import traceback
            traceback.print_exc()

    def _reset_probe_length_to_material_default(self, material_default_length):
        """Reset the probe length to the default length for the given material."""
        try:
            # print(f"[DEBUG] Resetting probe length to material default: {material_default_length}")
            # print(f"[DEBUG] Available option widgets: {list(self.option_widgets.keys())}")

            # Find the probe length widget and update it
            probe_length_widget = self.option_widgets.get('Probe Length')
            # print(f"[DEBUG] Probe length widget found: {probe_length_widget}")

            if probe_length_widget and hasattr(probe_length_widget, 'setValue'):
                # print(f"[DEBUG] Updating probe length widget to material default: {material_default_length}")
                probe_length_widget.setValue(material_default_length)
                # Update the configuration service
                self.config_service.set_option('Probe Length', material_default_length)
                # print(f"[DEBUG] Probe length reset to material default: {material_default_length}")
            else:
                # print(f"[DEBUG] Probe length widget not found or not a spin box")
                # print(f"[DEBUG] Widget type: {type(probe_length_widget) if probe_length_widget else 'None'}")
                # print(f"[DEBUG] Has setValue: {hasattr(probe_length_widget, 'setValue') if probe_length_widget else False}")
                pass
        except Exception as e:
            # print(f"[DEBUG] Error resetting probe length to material default: {e}")
            import traceback
            traceback.print_exc()
    
    def _auto_set_insulator_to_teflon(self):
        """Automatically set insulator material to Teflon when Halar is selected."""
        try:
            # Find the insulator material widget
            insulator_widget = self.option_widgets.get('Insulator Material')
            if insulator_widget and hasattr(insulator_widget, 'setCurrentIndex'):
                # Find the Teflon option in the dropdown
                teflon_index = -1
                for i in range(insulator_widget.count()):
                    item_data = insulator_widget.itemData(i)
                    if isinstance(item_data, dict) and item_data.get('code') == 'TEF':
                        teflon_index = i
                        break
                    elif isinstance(item_data, str) and item_data == 'TEF':
                        teflon_index = i
                        break
                
                if teflon_index >= 0:
                    # Set the insulator material to Teflon
                    insulator_widget.setCurrentIndex(teflon_index)
                    # Update the configuration service
                    teflon_value = insulator_widget.itemData(teflon_index)
                    self.config_service.set_option('Insulator Material', teflon_value)
                    print(f"[DEBUG] Auto-set insulator material to Teflon for Halar material")
                else:
                    print(f"[DEBUG] Teflon option not found in insulator material dropdown")
            else:
                print(f"[DEBUG] Insulator material widget not found")
        except Exception as e:
            print(f"[DEBUG] Error auto-setting insulator to Teflon: {e}")
            import traceback
            traceback.print_exc()

    def _create_tri_clamp_widget(self, option_data: dict) -> "ModernTriClampWidget":
        """Create a custom tri-clamp widget with size dropdown and spud checkbox."""
        widget = ModernTriClampWidget(option_data)
        widget.option_changed.connect(
            lambda opt_name, value: self._on_option_changed(opt_name, value)
        )
        return widget
    
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
        # print(f"[DEBUG] UI _set_default_values called for family: {family_name}")
        
        # Get base model configuration including process connection defaults
        from src.core.config.base_models import get_base_model
        base_model = get_base_model(family_name)
        
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
        
        # Add process connection defaults from base model if available
        if base_model.get("process_connection_type") and base_model.get("process_connection_size"):
            if base_model["process_connection_type"] == "NPT":
                defaults["Connection Type"] = "NPT"
                defaults["NPT Size"] = base_model["process_connection_size"]
        
        for option_name, default_value in defaults.items():
            widget = self.option_widgets.get(option_name)
            # print(f"[DEBUG] UI _set_default_values: {option_name} = {default_value} (type: {type(default_value)})")
            if widget:
                # For combo boxes
                if isinstance(widget, QComboBox):
                    idx = widget.findData(default_value)
                    if idx >= 0:
                        # print(f"[DEBUG] Setting QComboBox {option_name} to index {idx} (value: {default_value})")
                        widget.setCurrentIndex(idx)
                        self._on_option_changed(option_name, default_value)
                # For radio button groups
                elif isinstance(widget, QButtonGroup):
                    for btn in widget.buttons():
                        if btn.property('choice_code') == default_value:
                            # print(f"[DEBUG] Setting QButtonGroup {option_name} to {default_value}")
                            btn.setChecked(True)
                            self._on_option_changed(option_name, default_value)
                            break
    
    def _on_add_to_quote(self):
        print(f"[DEBUG] _on_add_to_quote called (instance {self._instance_id})")
        logger.info(f"_on_add_to_quote called (instance {self._instance_id})")
        traceback.print_stack()
        if self._adding_to_quote:
            logger.warning(f"_on_add_to_quote called while already processing - ignoring (instance {self._instance_id})")
            return
        self._adding_to_quote = True
        self.add_button.setEnabled(False)
        try:
            logger.info(f"_on_add_to_quote starting product addition (instance {self._instance_id})")
            
            # Check if we're in spare parts mode
            if hasattr(self, 'spare_parts_list') and self.spare_parts_list.isVisible():
                # Handle spare part addition
                items = self.spare_parts_list.selectedItems()
                if not items:
                    QMessageBox.warning(self, "Warning", "Please select a spare part first.")
                    return
                
                item = items[0]
                part = item.data(Qt.ItemDataRole.UserRole)
                if not part:
                    QMessageBox.warning(self, "Warning", "Please select a valid spare part.")
                    return
                
                # Create spare part configuration
                config = {
                    'product_family': 'Spare Parts',
                    'product_id': part.id,
                    'quantity': self.quantity,
                    'base_price': part.price,
                    'selected_options': {},
                    'total_price': part.price * self.quantity,
                    'model_number': part.part_number,
                    'description': f"Spare Part: {part.name}",
                    'is_spare_part': True,
                    'spare_part_data': {
                        'part_number': part.part_number,
                        'name': part.name,
                        'description': part.description,
                        'price': part.price,
                        'category': part.category,
                        'product_family_name': part.product_family.name
                    }
                }
                
                logger.info(f"Would emit product_added signal with spare part config: {config} (instance {self._instance_id})")
                
                # Always add the item to the quote first
                self.product_added.emit(config)
                
                # Show alert box asking user if they want to add more items or finish
                reply = QMessageBox.question(
                    self,
                    "Item Added to Quote",
                    f"'{part.name}' has been added to your quote.\n\nWould you like to add more items to the quote?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # User wants to add more items - reset the dialog to original state
                    logger.info(f"User chose to add more items - resetting dialog (instance {self._instance_id})")
                    self._reset_dialog_to_original_state()
                else:
                    # User is done - close the dialog
                    logger.info(f"User chose to finish - closing dialog (instance {self._instance_id})")
                    self.accept()
                    
            elif self.config_service.current_config:
                # Handle regular product addition
                config = {
                    'product': self.config_service.current_config.product_family_name,
                    'description': self.config_service.get_final_description(),
                    'unit_price': self.config_service.get_final_price(),
                    'quantity': self.quantity,
                    'total_price': self.config_service.get_final_price() * self.quantity,
                    'configuration': self.config_service.current_config.selected_options,
                    'model_number': self.config_service.generate_model_number()
                }
                logger.info(f"Would emit product_added signal with config: {config} (instance {self._instance_id})")
                
                # Always add the item to the quote first
                self.product_added.emit(config)
                
                # Show alert box asking user if they want to add more items or finish
                reply = QMessageBox.question(
                    self,
                    "Item Added to Quote",
                    f"'{config['product']}' has been added to your quote.\n\nWould you like to add more items to the quote?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # User wants to add more items - reset the dialog to original state
                    logger.info(f"User chose to add more items - resetting dialog (instance {self._instance_id})")
                    self._reset_dialog_to_original_state()
                else:
                    # User is done - close the dialog
                    logger.info(f"User chose to finish - closing dialog (instance {self._instance_id})")
                    self.accept()
            else:
                logger.warning(f"No current configuration available (instance {self._instance_id})")
                QMessageBox.warning(self, "Warning", "No product configuration available.")
        except Exception as e:
            logger.error(f"Error adding to quote: {e} (instance {self._instance_id})")
            QMessageBox.critical(self, "Error", f"Failed to add to quote: {e}")
        finally:
            self._adding_to_quote = False
    
    def _reset_dialog_to_original_state(self):
        """Reset the dialog to its original state for adding more items."""
        try:
            logger.info(f"Resetting dialog to original state (instance {self._instance_id})")
            
            # Clear the current product selection
            self.product_list.clearSelection()
            
            # Reset configuration service
            self.config_service = ConfigurationService(self.db, self.product_service)
            
            # Clear the configuration layout
            while self.config_layout.count():
                child = self.config_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Reset the model number label
            if hasattr(self, 'model_number_label'):
                self.model_number_label.setText("Select a Product to Begin")
            
            # Reset the total price display
            if hasattr(self, 'total_price_display'):
                self.total_price_display.setText("Total: $0.00")
            
            # Reset quantity to 1
            self.quantity = 1
            if hasattr(self, 'quantity_spin'):
                self.quantity_spin.setValue(1)
            
            # Clear option widgets
            self.option_widgets = {}
            
            # Clear spare parts selection if in spare parts mode
            if hasattr(self, 'spare_parts_list'):
                self.spare_parts_list.clearSelection()
            
            # Disable the add button until a product is selected
            if hasattr(self, 'add_button'):
                self.add_button.setEnabled(False)
            
            # Reset any pending changes
            self._pending_model_change = None
            self._model_changed_during_setup = False
            self._pending_model_base_length = None
            
            logger.info(f"Dialog reset completed (instance {self._instance_id})")
            
        except Exception as e:
            logger.error(f"Error resetting dialog: {e} (instance {self._instance_id})")
            QMessageBox.critical(self, "Error", f"Failed to reset dialog: {str(e)}")
    
    def _load_product_for_editing(self):
        """Load product for editing."""
        if not self.product_to_edit:
            return
            
        try:
            logger.info(f"Loading product for editing: {self.product_to_edit}")
            
            # Check if this is a spare part
            if self.product_to_edit.get("is_spare_part"):
                self._load_spare_part_for_editing()
                return
            
            # Get the product family name from the quote item
            product_family_name = self.product_to_edit.get("product_family", "")
            
            if not product_family_name:
                logger.warning("No product family name found in product_to_edit")
                return
            
            # Find the product family in the product list
            product_found = False
            for i in range(self.product_list.count()):
                item = self.product_list.item(i)
                product_data = item.data(Qt.ItemDataRole.UserRole)
                
                if product_data and product_data.get('name') == product_family_name:
                    # Select this product
                    self.product_list.setCurrentItem(item)
                    product_found = True
                    logger.info(f"Found and selected product family: {product_family_name}")
                    break
            
            if not product_found:
                logger.warning(f"Product family '{product_family_name}' not found in product list")
                return
            
            # Wait a moment for the product selection to process, then load the configuration
            QTimer.singleShot(100, self._load_saved_configuration)
            
        except Exception as e:
            logger.error(f"Error loading product for editing: {e}", exc_info=True)
    
    def _load_spare_part_for_editing(self):
        """Load spare part for editing."""
        try:
            logger.info("Loading spare part for editing")
            
            # Find and select "Spare Parts" in the product list
            spare_parts_found = False
            for i in range(self.product_list.count()):
                item = self.product_list.item(i)
                product_data = item.data(Qt.ItemDataRole.UserRole)
                
                if product_data and product_data.get('is_spare_parts'):
                    # Select Spare Parts
                    self.product_list.setCurrentItem(item)
                    spare_parts_found = True
                    logger.info("Found and selected Spare Parts")
                    break
            
            if not spare_parts_found:
                logger.warning("Spare Parts not found in product list")
                return
            
            # Wait a moment for the spare parts interface to load, then select the specific part
            QTimer.singleShot(200, self._load_saved_spare_part)
            
        except Exception as e:
            logger.error(f"Error loading spare part for editing: {e}", exc_info=True)
    
    def _load_saved_spare_part(self):
        """Load the saved spare part selection."""
        try:
            if not self.product_to_edit:
                return
            
            # Get the spare part data
            spare_part_data = self.product_to_edit.get("spare_part_data", {})
            part_number = spare_part_data.get("part_number", "")
            
            if not part_number:
                logger.warning("No part number found in spare part data")
                return
            
            # Find and select the specific spare part
            if hasattr(self, 'spare_parts_list'):
                for i in range(self.spare_parts_list.count()):
                    item = self.spare_parts_list.item(i)
                    part = item.data(Qt.ItemDataRole.UserRole)
                    
                    if part and part.part_number == part_number:
                        # Select this spare part
                        self.spare_parts_list.setCurrentItem(item)
                        logger.info(f"Found and selected spare part: {part_number}")
                        
                        # Set the quantity
                        saved_quantity = self.product_to_edit.get("quantity", 1)
                        if hasattr(self, 'quantity_spin'):
                            self.quantity_spin.setValue(saved_quantity)
                            self.quantity = saved_quantity
                        
                        break
                else:
                    logger.warning(f"Spare part '{part_number}' not found in spare parts list")
            
        except Exception as e:
            logger.error(f"Error loading saved spare part: {e}", exc_info=True)
    
    def _load_saved_configuration(self):
        """Load the saved configuration options."""
        try:
            if not self.product_to_edit or not self.config_service.current_config:
                return
            
            logger.info("Loading saved configuration options")
            
            # Get the saved configuration data
            saved_config = self.product_to_edit.get("config_data", {})
            saved_options = self.product_to_edit.get("options", [])
            
            # Set the quantity
            saved_quantity = self.product_to_edit.get("quantity", 1)
            if hasattr(self, 'quantity_spin'):
                self.quantity_spin.setValue(saved_quantity)
                self.quantity = saved_quantity
            
            # Apply saved configuration options
            for option_name, option_value in saved_config.items():
                if option_name in self.option_widgets:
                    widget = self.option_widgets[option_name]
                    
                    # Set the option value based on widget type
                    if hasattr(widget, 'setCurrentText'):
                        # For combo boxes
                        widget.setCurrentText(str(option_value))
                    elif hasattr(widget, 'setValue'):
                        # For spin boxes
                        widget.setValue(float(option_value))
                    elif hasattr(widget, 'setChecked'):
                        # For check boxes
                        widget.setChecked(bool(option_value))
                    
                    # Update the configuration service
                    self.config_service.set_option(option_name, option_value)
            
            # Update the model number and price
            self._update_model_number_label()
            self._update_total_price()
            
            logger.info("Successfully loaded saved configuration")
            
        except Exception as e:
            logger.error(f"Error loading saved configuration: {e}", exc_info=True)
    
    def showEvent(self, event):
        logger.info(f"ModernProductSelectionDialog: showEvent called (instance {self._instance_id})")
        super().showEvent(event)

    def closeEvent(self, event):
        logger.info(f"ModernProductSelectionDialog: closeEvent called (instance {self._instance_id})")
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
            # print(f"[DEBUG] _update_price() - selected_options: {selected_options}")

            # Check for U or T materials specifically
            material = selected_options.get('Material')
            length = selected_options.get('Length')
            if material in ['U', 'T'] and material and length:
                # print(f"[DEBUG] U/T MATERIAL DETECTED - Material: {material}, Length: {length}")

                # Get product family for length adder calculation
                product_family = self.config_service.current_config.product_family_name
                # print(f"[DEBUG] Product family for length adder: {product_family}")

                # Calculate length adder manually to verify
                if product_family:
                    try:
                        length_adder = self.product_service.calculate_length_price(
                            product_family, str(material), float(length)
                        )
                        # print(f"[DEBUG] Manual length adder calculation: ${length_adder:.2f}")
                    except Exception as e:
                        # print(f"[DEBUG] Error calculating length adder: {e}")
                        pass

            # Calculate price using configuration service
            price = self.config_service.get_final_price()
            # print(f"[DEBUG] Final calculated price: ${price:.2f}")

            # Update price display
            self.total_price_display.setText(f"Total: ${price:.2f}")

        except Exception as e:
            # print(f"[DEBUG] Error in _update_price: {e}")
            import traceback
            traceback.print_exc()

    def _on_material_changed(self):
        """Handle material change to show/hide exotic metal adder field."""
        try:
            # Get the current material selection
            material_widget = self.option_widgets.get('Material')
            if not material_widget or not hasattr(material_widget, 'currentData'):
                return
            
            current_material = material_widget.currentData()
            if not isinstance(current_material, str):
                current_material = str(current_material) if current_material is not None else ''
            
            # Define exotic metals
            exotic_metals = ['A', 'HB', 'HC', 'TT']
            
            # Show/hide the exotic metal adder field
            if current_material in exotic_metals:
                self.exotic_metal_adder_label.show()
                self.exotic_metal_adder_spin.show()
                # Set focus to the adder field for convenience
                self.exotic_metal_adder_spin.setFocus()
                # Set the current adder value in the configuration
                adder_value = self.exotic_metal_adder_spin.value()
                self.config_service.set_option('ExoticMetalAdder', adder_value)
            else:
                self.exotic_metal_adder_label.hide()
                self.exotic_metal_adder_spin.hide()
                # Clear the adder value when switching away from exotic metals
                self.exotic_metal_adder_spin.setValue(0.0)
                self.config_service.set_option('ExoticMetalAdder', 0.0)
            
            # Update pricing
            self._update_total_price()
            
        except Exception as e:
            print(f"[DEBUG] Error in _on_material_changed: {e}")
            import traceback
            traceback.print_exc()

    def _on_exotic_metal_adder_changed(self):
        """Handle exotic metal adder change to update pricing."""
        try:
            # Get the current material selection
            material_widget = self.option_widgets.get('Material')
            if not material_widget or not hasattr(material_widget, 'currentData'):
                return
            
            current_material = material_widget.currentData()
            if not isinstance(current_material, str):
                current_material = str(current_material) if current_material is not None else ''
            
            # Define exotic metals
            exotic_metals = ['A', 'HB', 'HC', 'TT']
            
            # Only apply the adder if an exotic metal is selected
            if current_material in exotic_metals:
                adder_value = self.exotic_metal_adder_spin.value()
                # Set the exotic metal adder in the configuration
                self.config_service.set_option('ExoticMetalAdder', adder_value)
            else:
                # Clear the exotic metal adder when not using exotic metals
                self.config_service.set_option('ExoticMetalAdder', 0.0)
            
            # Update pricing
            self._update_total_price()
        except Exception as e:
            print(f"[DEBUG] Error in _on_exotic_metal_adder_changed: {e}")
            import traceback
            traceback.print_exc()

    def _show_spare_parts_interface(self):
        """Show the spare parts browsing and selection interface."""
        # Clear the current configuration area
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Update the title
        self.model_number_label.setText("Spare Parts")
        
        # Clear the price display
        if hasattr(self, 'total_price_display'):
            self.total_price_display.setText("Total: $0.00")
        
        # Reset spare parts selection
        self.selected_spare_parts = {}  # Force reset when switching to spare parts tab
        
        # Create the spare parts interface
        self._create_spare_parts_browsing_interface()
        
        # Show the configuration area
        self.config_container.setVisible(True)
        
        # Enable the add button for spare parts (will be enabled when a part is selected)
        self.add_button.setEnabled(False)  # Start disabled, will be enabled when part is selected

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
        self.spare_parts_search.setPlaceholderText("Search spare parts...")
        self.spare_parts_search.textChanged.connect(self._filter_spare_parts_browsing)
        search_layout.addWidget(self.spare_parts_search)
        
        main_layout.addLayout(search_layout)
        
        # Spare parts list
        self.spare_parts_list = QListWidget()
        self.spare_parts_list.setStyleSheet("""
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
        self.spare_parts_list.itemSelectionChanged.connect(self._on_spare_part_selected)
        self.spare_parts_list.itemDoubleClicked.connect(self._add_spare_part_to_quote)
        main_layout.addWidget(self.spare_parts_list)
        
        # Populate the spare parts list
        self._populate_spare_parts_list(all_spare_parts)
        
        # Add the main widget to the config layout
        self.config_layout.addWidget(main_widget)

    def _populate_spare_parts_list(self, spare_parts):
        """Populate the spare parts list."""
        self.spare_parts_list.clear()
        
        # Group by product family
        families = {}
        for part in spare_parts:
            family_name = part.product_family.name
            if family_name not in families:
                families[family_name] = []
            families[family_name].append(part)
        
        # Add spare parts grouped by family
        for family_name in sorted(families.keys()):
            # Add family header
            header_item = QListWidgetItem(f"📦 {family_name}")
            header_item.setBackground(QColor("#f8f9fa"))
            header_item.setForeground(QColor("#6c757d"))
            header_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.spare_parts_list.addItem(header_item)
            
            # Add spare parts for this family
            for part in sorted(families[family_name], key=lambda x: x.part_number):
                item = QListWidgetItem(f"  {part.part_number} - {part.name} (${part.price:.2f})")
                item.setData(Qt.ItemDataRole.UserRole, part)
                self.spare_parts_list.addItem(item)

    def _on_spare_part_selected(self):
        """Handle spare part selection to update UI."""
        try:
            items = self.spare_parts_list.selectedItems()
            if not items:
                # No selection - disable add button and clear display
                self.add_button.setEnabled(False)
                self.model_number_label.setText("Spare Parts")
                self.total_price_display.setText("Total: $0.00")
                return
            
            item = items[0]
            part = item.data(Qt.ItemDataRole.UserRole)
            
            # Skip if this is a header item (no part data)
            if not part:
                self.add_button.setEnabled(False)
                return
            
            # Update the model number label with part number
            self.model_number_label.setText(f"Spare Part: {part.part_number}")
            
            # Update the price display
            self.total_price_display.setText(f"Total: ${part.price:.2f}")
            
            # Enable the add button
            self.add_button.setEnabled(True)
            
        except Exception as e:
            logger.error(f"Error handling spare part selection: {e}")
            self.add_button.setEnabled(False)

    def _filter_spare_parts_browsing(self, search_text):
        """Filter spare parts based on search text."""
        try:
            all_spare_parts = SparePartService.get_all_spare_parts(self.db)
            
            if search_text:
                filtered_parts = []
                for part in all_spare_parts:
                    if (search_text.lower() in part.part_number.lower() or
                        search_text.lower() in part.name.lower()):
                        filtered_parts.append(part)
                    else:
                        try:
                            desc = getattr(part, 'description', None)
                            if desc and search_text.lower() in str(desc).lower():
                                filtered_parts.append(part)
                        except:
                            pass
            else:
                filtered_parts = all_spare_parts
            
            self._populate_spare_parts_list(filtered_parts)
        except Exception as e:
            logger.error(f"Error filtering spare parts: {e}")

    def _add_spare_part_to_quote(self, item):
        """Add a spare part to the quote."""
        try:
            part = item.data(Qt.ItemDataRole.UserRole)
            if not part:
                return
            
            # Create a spare part configuration
            spare_part_config = {
                'product_family': 'Spare Parts',
                'product_id': part.id,
                'quantity': 1,
                'base_price': part.price,
                'selected_options': {},
                'total_price': part.price,
                'model_number': part.part_number,
                'description': f"Spare Part: {part.name}",
                'is_spare_part': True,
                'spare_part_data': {
                    'part_number': part.part_number,
                    'name': part.name,
                    'description': part.description,
                    'price': part.price,
                    'category': part.category,
                    'product_family_name': part.product_family.name
                }
            }
            
            # Emit the signal to add to quote
            self.product_added.emit(spare_part_config)
            self.accept()
            
        except Exception as e:
            logger.error(f"Error adding spare part to quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add spare part to quote: {e}")


class ModernTriClampWidget(QFrame):
    """Custom widget for tri-clamp selection with size dropdown and spud checkbox for modern dialog."""
    
    option_changed = Signal(str, str)  # option_name, value
    
    def __init__(self, option_data: dict, parent=None):
        super().__init__(parent)
        self.option_data = option_data
        self.choices = option_data.get("choices", [])
        self.adders = option_data.get("adders", {})
        
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            ModernTriClampWidget {
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the tri-clamp UI with size dropdown and spud checkbox."""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Size dropdown row
        size_layout = QHBoxLayout()
        size_label = QLabel("Size:")
        size_label.setStyleSheet(f"""
            font-family: {FONTS['family']};
            font-weight: {FONTS['weights']['semibold']};
            font-size: {FONTS['sizes']['base']}px;
            color: {COLORS['text_primary']};
            min-width: 60px;
        """)
        size_layout.addWidget(size_label)
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(["1-1/2\"", "2\""])
        self.size_combo.setFixedWidth(200)
        self.size_combo.setMinimumHeight(32)
        self.size_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px;
                background-color: {COLORS['bg_primary']};
                font-family: {FONTS['family']};
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
            }}
            QComboBox:focus {{
                border-color: {COLORS['primary']};
            }}
        """)
        self.size_combo.currentTextChanged.connect(self._on_size_changed)
        size_layout.addWidget(self.size_combo)
        size_layout.addStretch()
        layout.addLayout(size_layout)
        
        # Spud checkbox row
        spud_layout = QHBoxLayout()
        spud_layout.addSpacing(60)  # Align with dropdown
        self.spud_checkbox = QCheckBox("Spud")
        self.spud_checkbox.setStyleSheet("""
            QCheckBox {
                color: #2C3E50;
                font-size: 14px;
                font-weight: 500;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #e0e4e7;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #2C3E50;
                border-radius: 4px;
                background-color: #2C3E50;
            }
        """)
        self.spud_checkbox.toggled.connect(self._on_spud_toggled)
        spud_layout.addWidget(self.spud_checkbox)
        spud_layout.addStretch()
        layout.addLayout(spud_layout)
        
        # Initialize with default values
        self._update_selection()
    
    def _on_size_changed(self, size: str):
        """Handle size dropdown change."""
        self._update_selection()
    
    def _on_spud_toggled(self, checked: bool):
        """Handle spud checkbox toggle."""
        self._update_selection()
    
    def _update_selection(self):
        """Update the selection and emit the change."""
        size = self.size_combo.currentText()
        is_spud = self.spud_checkbox.isChecked()
        
        # Create the selection string
        if is_spud:
            selection = f"{size} Tri-clamp Spud"
        else:
            selection = f"{size} Tri-clamp Process Connection"
        
        # Emit the change
        self.option_changed.emit("Tri-clamp", selection)
    
    def get_current_value(self) -> str:
        """Get the current tri-clamp selection value."""
        size = self.size_combo.currentText()
        is_spud = self.spud_checkbox.isChecked()
        
        if is_spud:
            return f"{size} Tri-clamp Spud"
        else:
            return f"{size} Tri-clamp Process Connection"
    
    def hide(self):
        """Override hide to also hide the widget."""
        super().hide()
    
    def show(self):
        """Override show to also show the widget."""
        super().show()