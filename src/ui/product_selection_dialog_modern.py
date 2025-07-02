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
            font-size: {FONTS['sizes']['xl']}px;
            font-weight: {FONTS['weights']['bold']};
            color: {COLORS['text_primary']};
            background-color: {COLORS['bg_primary']};
            border: 2px solid {COLORS['border_light']};
            border-radius: {RADIUS['md']}px;
            padding: {SPACING['md']}px {SPACING['lg']}px;
            margin-bottom: {SPACING['md']}px;
            text-align: center;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        """)
        self.model_number_label.setWordWrap(True)
        self.model_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        selected_name = product_data.get('name', '')

        # Special handling for Spare Parts
        if selected_name == "Spare Parts":
            self._show_spare_parts_interface()
            return

        # PATCH: Special handling for TRAN-EX family
        if selected_name == "TRAN-EX":
            base_product_info = self.db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
            if base_product_info:
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
            base_product_info = self.product_service.get_base_product_for_family(self.db, selected_name)
            if base_product_info:
                product_data = base_product_info

        # Set flag for model change and store the base length
        self._model_changed_during_setup = True
        self._pending_model_base_length = product_data.get('base_length', 10)

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
                # Fallback: get available materials from product service
                try:
                    available_materials = self.product_service.get_material_choices_for_family(selected_name)
                    if available_materials:
                        first_material = available_materials[0]
                    else:
                        first_material = None
                except:
                    first_material = None
            selected_options = {'material': first_material} if first_material else {}
            # DEBUG: Print selected_options before configuration

            self.config_service.start_configuration(
                product_family_id=product_data.get('id', 1),
                product_family_name=selected_name,
                base_product_info=product_data,
                selected_options=selected_options,
            )
            self._show_product_config(product_data)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            self._show_error_message(f"Error gathering core options: {e}")
            return
    
    def _show_product_config(self, product):
        """Display configuration options for the selected product."""
        if not product:
            return

        try:
            product_family_id = product.get("id")
            product_family_name = product.get("name")
            
            # Start a new configuration
            self.config_service.start_configuration(
                product_family_id=product_family_id,
                product_family_name=product_family_name,
                base_product_info=product
            )
            
            # Clear the previous configuration
            self._clear_config_layout()
            
            # Build options UI
            self._build_dynamic_options(product_family_name)

            # Set default values
            self._set_default_values(product_family_name)
            
            # Generate model number
            model_number = self.config_service.generate_model_number()
            
            # Update displays
            self._update_model_number_label()
            self._update_total_price()
            
        except Exception as e:
            logger.error(f"Error showing product config: {e}")
            import traceback
            traceback.print_exc()
            self._show_error_message(f"Error loading product configuration: {str(e)}")
    
    def _set_default_values(self, family_name: str):
        """Set default values for the product family using base model configuration."""
        
        # Get base model configuration
        from src.core.config.base_models import get_base_model
        base_model = get_base_model(family_name)
        
        if not base_model:
            logger.warning(f"No base model found for family: {family_name}")
            return
        
        # Set defaults from base model
        defaults = {}
        
        # Set voltage from base model
        if base_model.get("voltage"):
            defaults["Voltage"] = base_model["voltage"]
        
        # Set material from base model
        if base_model.get("material"):
            # Check if the material is actually available for this product family
            try:
                available_materials = self.product_service.get_material_choices_for_family(family_name)
                if base_model["material"] in available_materials:
                    defaults["Material"] = base_model["material"]
                elif available_materials:
                    # Use first available material if base model material is not available
                    defaults["Material"] = available_materials[0]
            except:
                # Fallback to base model material if we can't check availability
                defaults["Material"] = base_model["material"]
        
        # Set probe length from base model
        if base_model.get("base_length"):
            defaults["Probe Length"] = base_model["base_length"]
        
        # Add process connection defaults from base model if available
        if base_model.get("process_connection_type") and base_model.get("process_connection_size"):
            if base_model["process_connection_type"] == "NPT":
                defaults["Connection Type"] = "NPT"
                # Force LS2000, LS2100, LS8000, and LS8000/2 to always use 3/4" NPT
                if family_name in ["LS2000", "LS2100", "LS8000", "LS8000/2"]:
                    defaults["NPT Size"] = '3/4"'
                else:
                    defaults["NPT Size"] = base_model["process_connection_size"]
        
        # Set all default values
        for option_name, default_value in defaults.items():
            widget = self.option_widgets.get(option_name)
            if widget:
                # For combo boxes
                if isinstance(widget, QComboBox):
                    idx = widget.findData(default_value)
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
                        self._on_option_changed(option_name, default_value)
                # For radio button groups
                elif isinstance(widget, QButtonGroup):
                    for btn in widget.buttons():
                        if btn.property('choice_code') == default_value:
                            btn.setChecked(True)
                            self._on_option_changed(option_name, default_value)
                            break
                # For spin boxes (like Probe Length)
                elif hasattr(widget, 'setValue'):
                    widget.setValue(default_value)
                    self._on_option_changed(option_name, default_value)
    
    def _on_add_to_quote(self):
        #  _on_add_to_quote called (instance {self._instance_id})")
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
                    },
                    # Store additional data for better editing support
                    'config_data': {},
                    'options': [],
                    'unit_price': part.price
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
                    'product_id': self.config_service.current_config.base_product.get('id'),
                    'description': self.config_service.get_final_description(),
                    'unit_price': self.config_service.get_final_price(),
                    'quantity': self.quantity,
                    'total_price': self.config_service.get_final_price() * self.quantity,
                    'configuration': self.config_service.current_config.selected_options,
                    'model_number': self.config_service.generate_model_number(),
                    # Store additional data for better editing support
                    'config_data': self.config_service.current_config.selected_options.copy(),
                    'options': [],  # Empty for now, can be populated if needed
                    'base_product_info': {
                        'id': self.config_service.current_config.base_product.get('id'),
                        'model_number': self.config_service.current_config.base_product.get('model_number'),
                        'base_price': self.config_service.current_config.base_product.get('base_price'),
                        'base_length': self.config_service.current_config.base_product.get('base_length'),
                        'voltage': self.config_service.current_config.base_product.get('voltage'),
                        'material': self.config_service.current_config.base_product.get('material'),
                    }
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
            self._clear_config_layout()
            
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
            QTimer.singleShot(500, self._load_saved_configuration)  # Increased delay to 500ms
            
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
        """Load the saved configuration options, using config_data, options, and model_number."""
        try:
            if not self.product_to_edit:
                return
                
            # Check if configuration service and widgets are ready
            if not self.config_service.current_config:
                logger.warning("Configuration service not ready, retrying in 200ms")
                QTimer.singleShot(200, self._load_saved_configuration)
                return
                
            if not self.option_widgets:
                logger.warning("Option widgets not ready, retrying in 200ms")
                QTimer.singleShot(200, self._load_saved_configuration)
                return
                
            logger.info("Loading saved configuration options (enhanced)")
            logger.info(f"Configuration service ready: {self.config_service.current_config is not None}")
            logger.info(f"Option widgets count: {len(self.option_widgets)}")
            
            # Gather all possible sources
            saved_config = self.product_to_edit.get("config_data") or self.product_to_edit.get("configuration", {})
            saved_options = self.product_to_edit.get("options", [])
            model_number = self.product_to_edit.get("model_number")
            product_family = self.product_to_edit.get("product_family")
            
            logger.info(f"Saved config: {saved_config}")
            logger.info(f"Saved options: {saved_options}")
            logger.info(f"Model number: {model_number}")
            logger.info(f"Product family: {product_family}")
            
            # Parse model number if available
            parsed_from_model = self._parse_model_number_to_options(model_number, product_family) if model_number else {}
            logger.info(f"Parsed from model: {parsed_from_model}")

            # PATCH: Force NPT Size for LS2000/LS2100/LS8000/LS8000/2 if not set
            if product_family in ["LS2000", "LS2100", "LS8000", "LS8000/2"]:
                if parsed_from_model.get('Connection Type') == 'NPT' and not parsed_from_model.get('NPT Size'):
                    parsed_from_model['NPT Size'] = '3/4"'

            # Set the quantity
            saved_quantity = self.product_to_edit.get("quantity", 1)
            if hasattr(self, 'quantity_spin'):
                self.quantity_spin.setValue(saved_quantity)
                self.quantity = saved_quantity
            
            # Build a lookup for options (if present)
            options_lookup = {}
            for opt in saved_options:
                # Try to use option name as key
                if isinstance(opt, dict):
                    name = opt.get("name")
                    val = opt.get("selected") or opt.get("value") or opt.get("code")
                    if name:
                        options_lookup[name] = val
            logger.info(f"Options lookup: {options_lookup}")
            
            # Log available widgets
            logger.info(f"Available widgets: {list(self.option_widgets.keys())}")
            
            # For each widget, set value from config_data, then options, then model number
            for option_name, widget in self.option_widgets.items():
                value = None
                source = "none"
                
                # Priority: config_data/configuration > options > model_number
                if saved_config and option_name in saved_config:
                    value = saved_config[option_name]
                    source = "config_data"
                elif option_name in options_lookup:
                    value = options_lookup[option_name]
                    source = "options"
                elif parsed_from_model and option_name in parsed_from_model:
                    value = parsed_from_model[option_name]
                    source = "model_number"
                
                # Debug for Material combo box
                if option_name == 'Material':
                    if widget and hasattr(widget, 'setCurrentIndex'):
                        codes = [str(widget.itemData(i)) for i in range(widget.count())]
                
                # Handle mapping from short codes to full names for accessories
                if value is None and saved_config:
                    # Map short codes to full names
                    short_code_mapping = {
                        'XSP': 'Extra Static Protection',
                        'SSTAG': 'Stainless Steel Tag', 
                        'VR': 'Vibration Resistance',
                        'EPOX': 'Epoxy House'
                    }
                    
                    # Check if any short code exists in saved_config
                    for short_code, full_name in short_code_mapping.items():
                        if short_code in saved_config and full_name == option_name:
                            value = saved_config[short_code]
                            source = "config_data (mapped)"
                            logger.info(f"Mapped short code {short_code} to {full_name}")
                            break
                
                logger.info(f"Option '{option_name}': value={value}, source={source}")
                
                # Set the widget value if found
                if value is not None:
                    try:
                        # Special handling for tri-clamp widget
                        if option_name == 'Tri-clamp' and hasattr(widget, 'set_value'):
                            # Use the new set_value method
                            widget.set_value(str(value))
                            logger.info(f"Set tri-clamp widget to '{value}' using set_value method")
                            
                            # Also need to set the connection type to 'Tri-clamp' to show the widget
                            conn_type_widget = self.option_widgets.get('Connection Type')
                            if conn_type_widget and hasattr(conn_type_widget, 'setCurrentText'):
                                conn_type_widget.setCurrentText('Tri-clamp')
                                logger.info("Set Connection Type to Tri-clamp to show tri-clamp widget")
                        elif hasattr(widget, 'setCurrentText'):
                            widget.setCurrentText(str(value))
                            logger.info(f"Set {option_name} to '{value}' using setCurrentText")
                        elif hasattr(widget, 'setValue'):
                            # Handle both integer and float values
                            if isinstance(value, (int, float)):
                                widget.setValue(value)
                            else:
                                try:
                                    widget.setValue(float(value))
                                except (ValueError, TypeError):
                                    try:
                                        widget.setValue(int(value))
                                    except (ValueError, TypeError):
                                        logger.warning(f"Could not convert {value} to number for {option_name}")
                                        continue
                            logger.info(f"Set {option_name} to {value} using setValue")
                        elif hasattr(widget, 'setChecked'):
                            # Handle boolean values properly
                            if isinstance(value, bool):
                                widget.setChecked(value)
                            elif isinstance(value, str):
                                widget.setChecked(value.lower() in ['true', '1', 'yes', 'on'])
                            elif isinstance(value, (int, float)):
                                widget.setChecked(bool(value))
                            else:
                                widget.setChecked(bool(value))
                            logger.info(f"Set {option_name} to {value} using setChecked")
                        elif hasattr(widget, 'setCurrentIndex'):
                            # For Material, match strictly by code (itemData)
                            if option_name == 'Material':
                                found_index = -1
                                search_value = str(value)
                                available_codes = []
                                for i in range(widget.count()):
                                    item_data = widget.itemData(i)
                                    available_codes.append(str(item_data))
                                    if str(item_data) == search_value:
                                        found_index = i
                                        break
                                if found_index >= 0:
                                    widget.setCurrentIndex(found_index)
                                    logger.info(f"Set {option_name} to index {found_index} (code: {search_value}) using setCurrentIndex (data match)")
                                else:
                                    logger.warning(f"Could not find code '{search_value}' in combo box for {option_name}. Available codes: {available_codes}. Combo will remain at default.")
                            else:
                                # For other options, fallback to previous logic
                                found_index = -1
                                for i in range(widget.count()):
                                    item_data = widget.itemData(i)
                                    item_text = widget.itemText(i)
                                    if (str(item_data) == str(value) or 
                                        str(item_text) == str(value) or
                                        (isinstance(item_data, dict) and item_data.get('code') == value)):
                                        found_index = i
                                        break
                                if found_index >= 0:
                                    widget.setCurrentIndex(found_index)
                                    logger.info(f"Set {option_name} to index {found_index} (value: {value}) using setCurrentIndex")
                                else:
                                    logger.warning(f"Could not find value '{value}' in combo box for {option_name}")
                        else:
                            logger.warning(f"Widget for {option_name} has no known setter method")
                        
                        # Update the configuration service
                        self.config_service.set_option(option_name, value)
                        logger.info(f"Updated config service for {option_name} = {value}")
                        
                        # Trigger option change event to update dependent widgets
                        self._on_option_changed(option_name, value)
                        
                    except Exception as e:
                        logger.warning(f"Could not set widget for {option_name} to {value}: {e}")
                else:
                    logger.warning(f"No saved value for option '{option_name}', leaving as default.")
            
            # Handle special cases for dependent options
            self._handle_dependent_options_after_loading(saved_config, parsed_from_model)
            
            # Update the model number and price
            self._update_model_number_label()
            self._update_total_price()
            logger.info("Successfully loaded saved configuration (enhanced)")
        except Exception as e:
            logger.error(f"Error loading saved configuration: {e}", exc_info=True)
    
    def _handle_dependent_options_after_loading(self, saved_config, parsed_from_model):
        """Handle special cases for dependent options after loading configuration."""
        try:
            # Handle connection type dependencies
            connection_type = (saved_config.get("Connection Type") or 
                             parsed_from_model.get("Connection Type"))
            
            if connection_type == "Tri-clamp":
                # Ensure tri-clamp widget is visible and properly configured
                tri_clamp_widget = self.option_widgets.get("Tri-clamp")
                if tri_clamp_widget and hasattr(tri_clamp_widget, 'show'):
                    tri_clamp_widget.show()
                    
                # Set connection type widget to Tri-clamp
                conn_type_widget = self.option_widgets.get("Connection Type")
                if conn_type_widget and hasattr(conn_type_widget, 'setCurrentText'):
                    conn_type_widget.setCurrentText("Tri-clamp")
            
            # Handle material dependencies
            material = (saved_config.get("Material") or 
                       parsed_from_model.get("Material"))
            
            if material in ['A', 'HB', 'HC', 'TT']:
                # Show exotic metal adder if exotic material is selected
                if hasattr(self, 'exotic_metal_adder_label'):
                    self.exotic_metal_adder_label.show()
                if hasattr(self, 'exotic_metal_adder_spin'):
                    self.exotic_metal_adder_spin.show()
                    
                # Set exotic metal adder value if available
                exotic_adder = (saved_config.get("ExoticMetalAdder") or 
                               parsed_from_model.get("ExoticMetalAdder"))
                if exotic_adder and hasattr(self, 'exotic_metal_adder_spin'):
                    try:
                        self.exotic_metal_adder_spin.setValue(float(exotic_adder))
                    except (ValueError, TypeError):
                        pass
            
            # Handle bent probe dependencies
            bent_probe = (saved_config.get("Bent Probe") or 
                         parsed_from_model.get("Bent Probe"))
            
            if bent_probe:
                # Show bent probe degree widget if bent probe is selected
                bent_degree_widget = self.option_widgets.get("Bent Probe Degree")
                if bent_degree_widget and hasattr(bent_degree_widget, 'show'):
                    bent_degree_widget.show()
                    
                # Set bent probe degree value
                bent_degree = (saved_config.get("Bent Probe Degree") or 
                              parsed_from_model.get("Bent Probe Degree"))
                if bent_degree and bent_degree_widget and hasattr(bent_degree_widget, 'setValue'):
                    try:
                        bent_degree_widget.setValue(int(bent_degree))
                    except (ValueError, TypeError):
                        pass
            
            # Handle insulator dependencies
            insulator_material = (saved_config.get("Insulator Material") or 
                                parsed_from_model.get("Insulator Material"))
            
            if insulator_material == "TEF":
                # Show insulator length widget if teflon insulator is selected
                insulator_length_widget = self.option_widgets.get("Insulator Length")
                if insulator_length_widget and hasattr(insulator_length_widget, 'show'):
                    insulator_length_widget.show()
                    
                # Set insulator length value
                insulator_length = (saved_config.get("Insulator Length") or 
                                   parsed_from_model.get("Insulator Length"))
                if insulator_length and insulator_length_widget and hasattr(insulator_length_widget, 'setValue'):
                    try:
                        insulator_length_widget.setValue(int(insulator_length))
                    except (ValueError, TypeError):
                        pass
                        
        except Exception as e:
            logger.warning(f"Error handling dependent options: {e}")

    def _parse_model_number_to_options(self, model_number, product_family=None):
        """Parse a model number string to infer as many options as possible."""
        import re
        options = {}
        if not model_number:
            return options
        
        # Example: LS2000-115VAC-H-24"-1.5"TCSPUD-XSP-SSTAG-VR-90DEG-8"TEFINS
        logger.info(f"Parsing model number: {model_number}")
        
        # Try to infer voltage (look for VAC/VDC patterns)
        voltage_match = re.search(r'(\d+VAC|\d+VDC)', model_number)
        if voltage_match:
            options['Voltage'] = voltage_match.group(1)
        
        # Try to infer material (single letter or known codes)
        material_codes = ['S', 'H', 'A', 'HB', 'HC', 'TT', 'U', 'T', 'C', 'TS', '316SS', '304SS', 'Hastelloy C', 'Monel', 'Titanium', 'Inconel']
        for code in material_codes:
            if f'-{code}-' in model_number or f'-{code}"' in model_number:
                options['Material'] = code
                break
        
        # Try to infer probe length (number with optional ")
        # Look for patterns like "24"", "24", or "24.5""
        # More comprehensive length matching
        length_patterns = [
            r'(\d+(?:\.\d+)?)(?:\"|$)',  # Basic length pattern
            r'(\d+(?:\.\d+)?)\"',       # Length with quote
            r'(\d+(?:\.\d+)?)\s*inch',  # Length with inch
        ]
        
        for pattern in length_patterns:
            length_match = re.search(pattern, model_number)
            if length_match:
                try:
                    length_val = float(length_match.group(1))
                    options['Probe Length'] = length_val
                    break
                except ValueError:
                    continue
        
        # Parse tri-clamp configuration - enhanced patterns
        tc_patterns = [
            r'(\d+(?:\.\d+)?)\"TC(SPUD)?',  # Standard TC pattern
            r'TC(\d+(?:\.\d+)?)\"(SPUD)?',  # TC prefix pattern
            r'(\d+(?:\.\d+)?)\"TRI(SPUD)?', # TRI pattern
        ]
        
        for pattern in tc_patterns:
            tc_match = re.search(pattern, model_number)
            if tc_match:
                options['Connection Type'] = 'Tri-clamp'
                size = tc_match.group(1) if tc_match.group(1) else tc_match.group(2)
                options['Tri-clamp Size'] = size + '"'
                
                # Determine if it's a spud connection
                is_spud = 'SPUD' in tc_match.group(0) or (tc_match.group(2) and tc_match.group(2) == 'SPUD')
                if is_spud:
                    options['Tri-clamp'] = f"{size} Tri-clamp Spud"
                else:
                    options['Tri-clamp'] = f"{size} Tri-clamp Process Connection"
                logger.info(f"Found tri-clamp: {options['Tri-clamp']}")
                break
        
        # Parse NPT connections if present - enhanced patterns
        npt_patterns = [
            r'(\d+(?:\.\d+)?)"NPT',  # Standard NPT pattern
            r'NPT(\d+(?:\.\d+)?)"',  # NPT prefix pattern
            r'(\d+(?:\.\d+)?)"NPT',  # Alternative pattern
        ]
        
        for pattern in npt_patterns:
            npt_match = re.search(pattern, model_number)
            if npt_match:
                options['Connection Type'] = 'NPT'
                options['NPT Size'] = npt_match.group(1) + '"'
                break

        # PATCH: For LS2000, LS2100, LS8000, and LS8000/2, if NPT and no explicit NPT Size, force 3/4"
        if (product_family in ["LS2000", "LS2100", "LS8000", "LS8000/2"] or (product_family is None and model_number.startswith(("LS2000", "LS2100", "LS8000")))):
            if options.get('Connection Type') == 'NPT' and 'NPT Size' not in options:
                options['NPT Size'] = '3/4"'
        
        # Parse flange connections if present - enhanced patterns
        flange_patterns = [
            r'(\d+(?:\.\d+)?)"(\d+)#FLANGE',  # Size, rating, and FLANGE suffix
            r'(\d+(?:\.\d+)?)"FLANGE',         # Standard flange pattern
            r'FLANGE(\d+(?:\.\d+)?)"',         # Flange prefix pattern
            r'(\d+(?:\.\d+)?)"(\d+)#',        # Size and rating pattern
        ]
        
        for pattern in flange_patterns:
            flange_match = re.search(pattern, model_number)
            if flange_match:
                options['Connection Type'] = 'Flange'
                flange_size = flange_match.group(1)
                # Only add quote if not already present
                if not flange_size.endswith('"'):
                    flange_size += '"'
                options['Flange Size'] = flange_size
                # If rating is present (group 2), add it
                if len(flange_match.groups()) > 1 and flange_match.group(2):
                    options['Flange Rating'] = flange_match.group(2) + '#'
                break
        
        # Parse accessories - look for them anywhere in the string
        # Map short codes to actual widget names used in the UI
        accessory_patterns = {
            'Extra Static Protection': [r'XSP', r'ESP', r'Extra Static Protection'],
            'Stainless Steel Tag': [r'SSTAG', r'Stainless Steel Tag'],
            'Vibration Resistance': [r'VR', r'Vibration Resistance'],
            'EPOX': [r'EPOX', r'Epoxy House'],
            'HALAR': [r'HALAR', r'Halar Housing'],
            'TEFLON': [r'TEFLON', r'Teflon Housing'],
            'VITON': [r'VITON', r'Viton O-Rings'],
            'BUNA': [r'BUNA', r'Buna O-Rings'],
            'PTFE': [r'PTFE', r'PTFE O-Rings'],
        }
        
        for option_name, patterns in accessory_patterns.items():
            for pattern in patterns:
                if re.search(pattern, model_number, re.IGNORECASE):
                    if option_name in ['Extra Static Protection', 'Stainless Steel Tag', 'Vibration Resistance', 'EPOX']:
                        options[option_name] = True
                    elif option_name in ['HALAR', 'TEFLON']:
                        options['Housing Type'] = option_name
                    elif option_name in ['VITON', 'BUNA', 'PTFE']:
                        options['O-Rings'] = option_name
                    logger.info(f"Found {option_name} accessory")
                    break
        
        # Parse bent probe - enhanced patterns
        bent_patterns = [
            r'(\d+)DEG',  # Standard degree pattern
            r'(\d+)°',    # Degree symbol pattern
            r'BENT(\d+)', # BENT prefix pattern
        ]
        
        for pattern in bent_patterns:
            bent_match = re.search(pattern, model_number)
            if bent_match:
                options['Bent Probe'] = True
                options['Bent Probe Degree'] = int(bent_match.group(1))
                logger.info(f"Found bent probe: {bent_match.group(1)} degrees")
                break
        
        # Parse insulator details - enhanced patterns
        insulator_patterns = [
            r'(\d+)\"TEFINS',  # Standard TEFINS pattern with length
            r'TEFINS(\d+)\"',  # TEFINS prefix pattern with length
            r'(\d+)\"TEF',     # TEF pattern with length
            r'TEF(\d+)\"',     # TEF prefix pattern with length
            r'TEFINS',         # TEFINS without length (standard/default)
        ]
        
        for pattern in insulator_patterns:
            insulator_match = re.search(pattern, model_number)
            if insulator_match:
                if pattern == r'TEFINS':  # No length specified
                    options['Insulator Material'] = 'TEF'  # Teflon
                    logger.info(f"Found insulator: Teflon (standard length)")
                else:
                    options['Insulator Length'] = int(insulator_match.group(1))
                    options['Insulator Material'] = 'TEF'  # Teflon
                    logger.info(f"Found insulator: {insulator_match.group(1)}\" Teflon")
                break
        
        # Parse connection material (usually at the end)
        material_patterns = {
            'SSTAG': [r'SSTAG', r'Stainless Steel'],
            'CS': [r'CS', r'Carbon Steel'],
            '316SS': [r'316SS', r'316 Stainless'],
            '304SS': [r'304SS', r'304 Stainless'],
        }
        
        for material_name, patterns in material_patterns.items():
            for pattern in patterns:
                if re.search(pattern, model_number, re.IGNORECASE):
                    options['Connection Material'] = material_name
                    break
        
        # Parse diameter probe options
        diameter_patterns = [
            r'3/4\"OD',  # 3/4" OD pattern
            r'3/4OD',    # 3/4OD pattern
            r'(\d+(?:\.\d+)?)\"OD',  # Generic OD pattern
        ]
        
        for pattern in diameter_patterns:
            if re.search(pattern, model_number):
                options['3/4" Diameter Probe'] = True
                logger.info("Found 3/4\" diameter probe")
                break
        
        # Parse exotic metal adders
        exotic_patterns = {
            'A': [r'-A-', r'-ALLOY-'],
            'HB': [r'-HB-', r'-HASTELLOYB-'],
            'HC': [r'-HC-', r'-HASTELLOYC-'],
            'TT': [r'-TT-', r'-TITANIUM-'],
        }
        
        for metal_code, patterns in exotic_patterns.items():
            for pattern in patterns:
                if re.search(pattern, model_number, re.IGNORECASE):
                    options['ExoticMetalAdder'] = metal_code
                    logger.info(f"Found exotic metal: {metal_code}")
                    break
        
        logger.info(f"Parsed model number '{model_number}' into options: {options}")
        return options

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

    def _clear_config_layout(self):
        """Remove all widgets from the config layout."""
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _show_error_message(self, message):
        # Clear the config layout and show an error message
        self._clear_config_layout()
        label = QLabel(message)
        # Use a valid color for error (fallback to red if COLORS['danger'] not present)
        error_color = COLORS.get('danger', '#d32f2f')
        label.setStyleSheet(f"font-size: 16px; color: {error_color}; font-weight: bold; padding: 16px;")
        self.config_layout.addWidget(label)

    def _update_price(self):
        """Update the total price based on current selections."""
        try:
            if not self.config_service.current_config:
                return

            # Get current selections
            selected_options = self.config_service.current_config.selected_options

            # Check for U or T materials specifically
            material = selected_options.get('Material')
            length = selected_options.get('Length')
            if material in ['U', 'T'] and material and length:

                # Get product family for length adder calculation
                product_family = self.config_service.current_config.product_family_name

                # Calculate length adder manually to verify
                if product_family:
                    try:
                        length_adder = self.product_service.calculate_length_price(
                            product_family, str(material), float(length)
                        )
                    except Exception as e:
                        pass

            # Calculate price using configuration service
            price = self.config_service.get_final_price()

            # Update price display
            self.total_price_display.setText(f"Total: ${price:.2f}")

        except Exception as e:
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
            import traceback
            traceback.print_exc()

    def _show_spare_parts_interface(self):
        """Show the spare parts browsing and selection interface."""
        # Clear the current configuration area
        self._clear_config_layout()
        
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
                },
                # Store additional data for better editing support
                'config_data': {},
                'options': [],
                'unit_price': part.price
            }
            
            # Emit the signal to add to quote
            self.product_added.emit(spare_part_config)
            self.accept()
            
        except Exception as e:
            logger.error(f"Error adding spare part to quote: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add spare part to quote: {e}")

    def _build_dynamic_options(self, product_family_name):
        """Dynamically build option widgets for the selected product family."""
        # Clear any existing widgets
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.option_widgets.clear()

        # Fetch all available options for this product family
        all_options = self.product_service.get_additional_options(self.db, product_family_name)
        print(f"[DEBUG] all_options for {product_family_name}: {all_options}")

        if not all_options or not isinstance(all_options, list):
            label = QLabel("No configurable options available for this product.")
            label.setStyleSheet(f"""
                font-size: {FONTS['sizes']['lg']}px;
                color: {COLORS['text_secondary']};
                padding: {SPACING['xl']}px;
                text-align: center;
            """)
            self.config_layout.addWidget(label)
            return

        # Group options by category
        options_by_category = {}
        for option in all_options:
            category = option.get('category', 'Other')
            if category not in options_by_category:
                options_by_category[category] = []
            options_by_category[category].append(option)

        # Create sections for each category
        for category, options in options_by_category.items():
            # Create group box for category
            group_box = QGroupBox(category)
            group_box.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: {FONTS['weights']['bold']};
                    color: {COLORS['text_primary']};
                    border: 2px solid {COLORS['border_light']};
                    border-radius: {RADIUS['lg']}px;
                    margin-top: {SPACING['lg']}px;
                    padding-top: {SPACING['md']}px;
                    background-color: {COLORS['bg_primary']};
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: {SPACING['lg']}px;
                    padding: 0 {SPACING['md']}px;
                    background-color: {COLORS['bg_primary']};
                }}
            """)
            
            category_layout = QVBoxLayout(group_box)
            category_layout.setSpacing(SPACING['md'])
            category_layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])

            for option in options:
                name = option.get('name')
                choices = option.get('choices', [])
                adders = option.get('adders', {})
                
                # Only render if choices is a valid, non-empty list
                if not isinstance(choices, list) or not choices:
                    continue

                # Create option label
                option_label = QLabel(name)
                option_label.setStyleSheet(f"""
                    font-weight: {FONTS['weights']['semibold']};
                    color: {COLORS['text_primary']};
                    font-size: {FONTS['sizes']['base']}px;
                    margin-bottom: {SPACING['xs']}px;
                """)
                category_layout.addWidget(option_label)

                # Create widget based on number of choices
                if len(choices) <= 4:
                    widget = self._create_radio_group(name, choices, adders)
                else:
                    widget = self._create_dropdown(name, choices, adders)
                
                category_layout.addWidget(widget)
                self.option_widgets[name] = widget

            self.config_layout.addWidget(group_box)

    def _create_radio_group(self, option_name, choices, adders):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(SPACING['sm'])
        layout.setContentsMargins(0, 0, 0, 0)
        button_group = QButtonGroup(container)
        
        for i, choice in enumerate(choices):
            code = choice.get('code') if isinstance(choice, dict) else str(choice)
            display = choice.get('display_name', code) if isinstance(choice, dict) else str(choice)
            price_adder = adders.get(code, 0)
            if price_adder:
                display += f" (+${price_adder:.2f})"
            
            radio = QRadioButton(display)
            radio.setStyleSheet(f"""
                QRadioButton {{
                    font-size: {FONTS['sizes']['base']}px;
                    color: {COLORS['text_primary']};
                    padding: {SPACING['sm']}px;
                    spacing: {SPACING['sm']}px;
                }}
                QRadioButton:checked {{
                    color: {COLORS['primary']};
                    font-weight: {FONTS['weights']['semibold']};
                }}
                QRadioButton:hover {{
                    color: {COLORS['primary']};
                }}
            """)
            radio.setProperty('choice_code', code)
            radio.setProperty('option_name', option_name)
            button_group.addButton(radio, i)
            layout.addWidget(radio)
            if i == 0:
                radio.setChecked(True)
        
        button_group.buttonClicked.connect(self._on_option_changed_radio)
        return container

    def _create_dropdown(self, option_name, choices, adders):
        combo = QComboBox()
        combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px;
                background-color: {COLORS['bg_primary']};
                font-family: {FONTS['family']};
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
                min-height: 32px;
            }}
            QComboBox:focus {{
                border-color: {COLORS['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {COLORS['text_secondary']};
            }}
        """)
        
        for choice in choices:
            code = choice.get('code') if isinstance(choice, dict) else str(choice)
            display = choice.get('display_name', code) if isinstance(choice, dict) else str(choice)
            price_adder = adders.get(code, 0)
            if price_adder:
                display += f" (+${price_adder:.2f})"
            combo.addItem(display, code)
        
        combo.setProperty('option_name', option_name)
        combo.currentIndexChanged.connect(self._on_option_changed_dropdown)
        return combo

    def _on_option_changed_radio(self, button):
        option_name = button.property('option_name')
        value = button.property('choice_code')
        self.config_service.set_option(option_name, value)
        self._update_total_price()
        self._update_model_number_label()

    def _on_option_changed_dropdown(self):
        sender = self.sender()
        if sender:
            option_name = sender.property('option_name')
            value = sender.currentData()
            self.config_service.set_option(option_name, value)
            self._update_total_price()
            self._update_model_number_label()

    def _on_option_changed(self, option_name, value):
        """Handle option changes and update configuration."""
        self.config_service.set_option(option_name, value)
        self._update_total_price()
        self._update_model_number_label()

    def _update_total_price(self):
        """Update the total price display."""
        try:
            if self.config_service.current_config:
                price = self.config_service.get_final_price()
                self.total_price_display.setText(f"Total: ${price:.2f}")
        except Exception as e:
            logger.error(f"Error updating total price: {e}")
            self.total_price_display.setText("Total: $0.00")


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
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Use QFormLayout for uniform styling
        form_layout = QFormLayout()
        form_layout.setSpacing(SPACING['md'])
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Size dropdown row
        size_label = QLabel("Tri-clamp Size")
        size_label.setStyleSheet(f"""
            font-weight: {FONTS['weights']['semibold']};
            color: {COLORS['text_primary']};
            font-size: {FONTS['sizes']['base']}px;
        """)
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(["1.5\"", "2\""])
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
        
        form_layout.addRow(size_label, self.size_combo)
        
        # Spud checkbox row
        spud_label = QLabel("Spud")
        spud_label.setStyleSheet(f"""
            font-weight: {FONTS['weights']['semibold']};
            color: {COLORS['text_primary']};
            font-size: {FONTS['sizes']['base']}px;
        """)
        
        self.spud_checkbox = QCheckBox()
        self.spud_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: #2C3E50;
                font-size: 14px;
                font-weight: 500;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {COLORS['border_light']};
                border-radius: 4px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid {COLORS['primary']};
                border-radius: 4px;
                background-color: {COLORS['primary']};
            }}
        """)
        self.spud_checkbox.toggled.connect(self._on_spud_toggled)
        
        form_layout.addRow(spud_label, self.spud_checkbox)
        
        layout.addLayout(form_layout)
        
        # Initialize with default values
        self._update_selection()
        # Emit the initial value after the event loop returns to ensure the dialog is ready
        def emit_initial():
            size = self.size_combo.currentText()
            is_spud = self.spud_checkbox.isChecked()
            if is_spud:
                selection = f"{size} Tri-clamp Spud"
            else:
                selection = f"{size} Tri-clamp Process Connection"
            self.option_changed.emit("Tri-clamp", selection)
        QTimer.singleShot(0, emit_initial)
    
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
    
    def set_value(self, value: str):
        """Set the tri-clamp widget value programmatically."""
        import re
        # Parse the size
        size_match = re.search(r'(\d+(?:\.\d+)?)\"', value)
        if size_match:
            size = size_match.group(1) + '"'
            # Set the size dropdown
            size_index = self.size_combo.findText(size)
            if size_index >= 0:
                self.size_combo.setCurrentIndex(size_index)
        
        # Check if it's a spud
        is_spud = 'Spud' in value
        self.spud_checkbox.setChecked(is_spud)
        
        # Update the selection
        self._update_selection()
    
    def hide(self):
        """Override hide to also hide the widget."""
        super().hide()