"""
Product Selection Dialog for Adding Products to Quote.

This dialog provides a two-panel interface:
- Left: Product search and selection
- Right: Product configuration and add-to-quote
"""

import logging
from typing import Optional, Any, Dict, List, Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QGroupBox,
)
from PySide6.QtGui import QFont

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.core.models.configuration import Configuration
from src.core.models.product import Product, ProductVariant

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProductSelectionDialog(QDialog):
    """
    Modal dialog for selecting and configuring a product to add to a quote.
    Emits product_added(product_data) when a product is configured and added.
    """

    product_added = Signal(dict)

    def __init__(
        self, product_service: ProductService, parent=None, product_to_edit=None
    ):
        super().__init__(parent)
        self.product_to_edit = product_to_edit
        self.is_edit_mode = self.product_to_edit is not None

        title = 'Edit Product' if self.is_edit_mode else 'Add Product to Quote'
        self.setWindowTitle(title)

        self.resize(900, 600)

        # Services
        self.db = SessionLocal()
        self.product_service = product_service
        self.config_service = ConfigurationService(self.db, self.product_service)

        # State
        self.products = []
        self.quantity = 1  # Default quantity
        self._fetch_products()

        self._init_ui()

        if self.is_edit_mode:
            self._populate_for_edit()

    def __del__(self):
        # Ensure the database session is closed when the dialog is destroyed
        if self.db:
            self.db.close()

    def _fetch_products(self):
        """Fetch product families from the database using ProductService."""
        logger.info('Starting to fetch product families...')
        try:
            family_objs = self.product_service.get_product_families(self.db)
            products = []
            for fam in family_objs:
                variants = self.product_service.get_variants_for_family(
                    self.db, fam['id']
                )
                if variants:
                    variant = variants[0]
                    product_info = {
                        'id': fam['id'],
                        'name': fam['name'],
                        'description': fam.get('description', ''),
                        'category': fam.get('category', ''),
                        'base_price': variant['base_price'],
                        'base_length': variant['base_length'],
                        'voltage': variant['voltage'],
                        'material': variant['material'],
                    }
                    products.append(product_info)
            self.products = products
        except Exception as e:
            logger.error(
                f'A critical error occurred while fetching product families: {e}',
                exc_info=True,
            )
            self.products = []

    def _init_ui(self):
        """Set up the dialog UI layout and widgets."""
        main_layout = QHBoxLayout(self)
        left_panel = QFrame()
        left_panel.setFixedWidth(340)
        left_layout = QVBoxLayout(left_panel)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search products...')
        self.search_bar.textChanged.connect(self._filter_products)
        left_layout.addWidget(self.search_bar)
        self.product_list = QListWidget()
        self.product_list.setSpacing(8)
        self.product_list.itemSelectionChanged.connect(self._on_product_selected)
        left_layout.addWidget(self.product_list, 1)
        main_layout.addWidget(left_panel)

        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        
        # Add model number and total price at the top in a horizontal layout
        self.top_info_layout = QHBoxLayout()
        self.model_number_label = QLabel('Model: PENDING...')
        self.model_number_label.setObjectName('modelNumberLabel')
        self.model_number_label.setStyleSheet('font-size: 16pt; font-weight: bold;')
        self.model_number_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.top_info_layout.addWidget(self.model_number_label, alignment=Qt.AlignLeft)

        self.total_price_label = QLabel('$0.00')
        self.total_price_label.setObjectName('totalPriceLabel')
        self.total_price_label.setStyleSheet('font-size: 16pt; font-weight: bold;')
        self.top_info_layout.addWidget(self.total_price_label, alignment=Qt.AlignRight)

        self.right_layout.addLayout(self.top_info_layout)
        
        self.config_scroll = QScrollArea()
        self.config_scroll.setWidgetResizable(True)
        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)
        self.config_layout.setAlignment(Qt.AlignTop)
        self.config_scroll.setWidget(self.config_widget)
        self.right_layout.addWidget(self.config_scroll)
        main_layout.addWidget(self.right_panel, 1)

        self._populate_product_list()
        if not self.is_edit_mode:
            self._show_select_product()

    def _populate_product_list(self, filter_text=''):
        """Populate the product list, optionally filtering by search text."""
        self.product_list.clear()
        filtered_products = [
            p for p in self.products if filter_text.lower() in p['name'].lower()
        ]
        for product in filtered_products:
            item = QListWidgetItem(f"{product['name']}")
            item.setData(Qt.UserRole, product)
            self.product_list.addItem(item)

    def _filter_products(self, text):
        self._populate_product_list(text)

    def _on_product_selected(self):
        """Handle product selection from the list."""
        items = self.product_list.selectedItems()
        if not items:
            logger.debug("No items selected, showing select product prompt")
            self._show_select_product()
            return

        product_data = items[0].data(Qt.UserRole)
        logger.debug(f"Selected product data: {product_data}")
        
        try:
            logger.debug(f"Starting configuration for product family: {product_data['name']}")
            self.config_service.start_configuration(
                product_family_id=product_data['id'],
                product_family_name=product_data['name'],
                base_product_info=product_data,
            )
            self.quantity = 1
            self._show_product_config(product_data)
        except Exception as e:
            logger.error(f"Error starting configuration: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to configure product: {str(e)}")

    def _show_select_product(self):
        self._clear_config_panel()
        prompt = QLabel('<b>Select a Product</b><br>Choose a product to configure.')
        prompt.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(prompt)

    def _show_product_config(self, product):
        """Show the configuration options for the selected product."""
        logger.debug(f"Showing product config for: {product['name']}")
        self._clear_config_panel()
        self.option_widgets = {}

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        try:
            logger.debug("Setting up core options")
            self._setup_core_options(form_layout, product)
        except Exception as e:
            logger.error(f"Error setting up core options: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to setup core options: {str(e)}")

        # Add mechanical options
        self._setup_mechanical_options(form_layout)

        # Get all connection-related options for the product family
        try:
            logger.debug("Fetching connection options")
            connection_options = self.product_service.get_connection_options(
                self.db, product['id']
            )
            logger.debug(f"Connection options: {connection_options}")
            self._setup_connection_options(form_layout, connection_options)
        except Exception as e:
            logger.error(f"Error setting up connection options: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to setup connection options: {str(e)}")

        self.config_layout.addLayout(form_layout)
        self._setup_quantity_and_total()
        self._setup_add_button()
        self._update_total_price()
        self._update_model_number_label()

    def _setup_core_options(self, form_layout: QFormLayout, product: dict):
        """Set up the core configuration options for the selected product."""
        logger.debug(f"Setting up core options for product: {product['name']}")
        
        # Get voltage options first
        try:
            voltage_options = self.product_service.get_voltage_options(
                self.db, product['id']
            )
            logger.debug(f"Voltage options: {voltage_options}")
            
            if voltage_options:
                voltage_combo = QComboBox()
                voltage_combo.setObjectName("option_Voltage")
                for option in voltage_options:
                    voltage_combo.addItem(option['display_name'], option['voltage'])
                voltage_combo.currentIndexChanged.connect(
                    lambda idx, cmb=voltage_combo: self._on_option_changed(
                        'Voltage', cmb.currentData()
                    )
                )
                form_layout.addRow("Voltage:", voltage_combo)
                self.option_widgets['Voltage'] = voltage_combo
                logger.debug("Added voltage options to form")
        except Exception as e:
            logger.error(f"Error fetching voltage options: {str(e)}", exc_info=True)
        
        # Get material options (refactored to use Option from additional_options)
        material_option = None
        try:
            additional_options = self.product_service.get_additional_options(
                self.db, product['name']
            )
            logger.debug(f"Additional options for {product['name']}:")
            for opt in additional_options:
                logger.debug(f"  Option: {opt['name']}")
                if opt['name'] == 'Material':
                    material_option = opt
                logger.debug(f"    Category: {opt.get('category', 'No category')}")
                logger.debug(f"    Choices: {opt.get('choices', 'No choices')}")
                logger.debug(f"    Adders: {opt.get('adders', 'No adders')}")
                logger.debug(f"    Product Families: {opt.get('product_families', 'No families')}")
                logger.debug(f"    Excluded Products: {opt.get('excluded_products', 'None')}")
        except Exception as e:
            logger.error(f"Error fetching additional options: {str(e)}", exc_info=True)
            additional_options = []

        # Build Material dropdown from Option (with adders)
        if material_option and isinstance(material_option.get('choices'), list):
            material_combo = QComboBox()
            material_combo.setObjectName("option_Material")
            adders = material_option.get('adders', {})
            for choice in material_option['choices']:
                price_adder = adders.get(choice, 0) if isinstance(adders, dict) else 0
                if price_adder:
                    display_text = f"{choice} (+${price_adder:.2f})"
                else:
                    display_text = str(choice)
                material_combo.addItem(display_text, choice)
            material_combo.currentIndexChanged.connect(
                lambda idx, cmb=material_combo: self._on_option_changed(
                    'Material', cmb.currentData()
                )
            )
            form_layout.addRow("Material:", material_combo)
            self.option_widgets['Material'] = material_combo
            logger.debug("Added material options to form (from Option)")
            # Add probe length customization (unchanged)
            probe_length_spin = QSpinBox()
            probe_length_spin.setObjectName("option_Probe Length")
            probe_length_spin.setRange(1, 120)  # Allow lengths from 1 to 120 inches
            probe_length_spin.setSuffix('"')  # Add inch symbol
            if product.get('base_length'):
                probe_length_spin.setValue(product['base_length'])
            probe_length_spin.valueChanged.connect(
                lambda value, cmb=probe_length_spin: self._on_option_changed(
                    'Probe Length', value
                )
            )
            form_layout.addRow("Probe Length:", probe_length_spin)
            self.option_widgets['Probe Length'] = probe_length_spin
            logger.debug(f"Added probe length customization to form with default value: {product.get('base_length')}")
        else:
            # fallback to old method if no material_option found
            try:
                material_options = self.product_service.get_available_materials_for_product(
                    self.db, product['name']
                )
                logger.debug(f"Material options: {material_options}")
                if material_options:
                    material_combo = QComboBox()
                    material_combo.setObjectName("option_Material")
                    for option in material_options:
                        material_combo.addItem(option['display_name'], option['code'])
                        material_combo.currentIndexChanged.connect(
                            lambda idx, cmb=material_combo: self._on_option_changed(
                                'Material', cmb.currentData()
                            )
                        )
                    form_layout.addRow("Material:", material_combo)
                    self.option_widgets['Material'] = material_combo
                    logger.debug("Added material options to form (fallback)")
                    # Add probe length customization (unchanged)
                    probe_length_spin = QSpinBox()
                    probe_length_spin.setObjectName("option_Probe Length")
                    probe_length_spin.setRange(1, 120)  # Allow lengths from 1 to 120 inches
                    probe_length_spin.setSuffix('"')  # Add inch symbol
                    if product.get('base_length'):
                        probe_length_spin.setValue(product['base_length'])
                    probe_length_spin.valueChanged.connect(
                        lambda value, cmb=probe_length_spin: self._on_option_changed(
                            'Probe Length', value
                        )
                    )
                    form_layout.addRow("Probe Length:", probe_length_spin)
                    self.option_widgets['Probe Length'] = probe_length_spin
                    logger.debug(f"Added probe length customization to form with default value: {product.get('base_length')}")
            except Exception as e:
                logger.error(f"Error fetching material options: {str(e)}", exc_info=True)
        
        # Get product family-specific options
        try:
            additional_options = self.product_service.get_additional_options(
                self.db, product['name']
            )
            logger.debug(f"Additional options for {product['name']}:")
            for opt in additional_options:
                logger.debug(f"  Option: {opt['name']}")
                logger.debug(f"    Category: {opt.get('category', 'No category')}")
                logger.debug(f"    Choices: {opt.get('choices', 'No choices')}")
                logger.debug(f"    Adders: {opt.get('adders', 'No adders')}")
                logger.debug(f"    Product Families: {opt.get('product_families', 'No families')}")
                logger.debug(f"    Excluded Products: {opt.get('excluded_products', 'None')}")
        except Exception as e:
            logger.error(f"Error fetching additional options: {str(e)}", exc_info=True)
            additional_options = []

        # Group options by category
        options_by_category = {}
        for option in additional_options:
            # Hide 'NEMA 4X Windowed Enclosure' for FS10000
            if product.get('name', '').startswith('FS10000') and option['name'] == 'NEMA 4X Windowed Enclosure':
                logger.debug("Hiding 'NEMA 4X Windowed Enclosure' from core options for FS10000")
                continue
            if product.get('name', '').startswith('LS6000') and option['name'] == '3/4" Diameter Probe':
                logger.debug("Hiding '3/4\" Diameter Probe' from core options for LS6000")
                continue
            if product.get('name', '').startswith('LS6000'):
                print(f"LS6000 option: '{option['name']}'")
            # Skip voltage options as we've already handled them
            if option['name'] == 'Voltage':
                continue
            # Skip mechanical options from core options UI
            if option['name'] in {'Stainless Steel Tag', 'Cable Probe', 'Bent Probe', 'Teflon Insulator'}:
                continue
            # Hide '3/4" Diameter Probe x 10"' for LS6000 only (core options only)
            if product.get('name', '').startswith('LS6000') and option['name'] == '3/4" Diameter Probe x 10"':
                logger.debug("Hiding '3/4 Diameter Probe x 10' from core options for LS6000")
                continue
            category = option.get('category', 'General')
            if category not in options_by_category:
                options_by_category[category] = []
            options_by_category[category].append(option)
            logger.debug(f"Added option {option['name']} to category {category}")

        # Create UI controls for each option
        # Only show the main 'O-Rings' dropdown, not individual material boxes, and skip 'None'
        oring_material_names = {"Viton", "Silicon", "Buna-N", "EPDM", "PTFE", "Kalrez", "None"}
        exotic_metal_names = {"Alloy 20", "Hastelloy-C-276", "Hastelloy-B", "Titanium"}
        exotic_metal_choices = []
        exotic_metal_option = None
        for category, options in options_by_category.items():
            logger.debug(f"Processing category: {category} with {len(options)} options")
            for option in options:
                # Skip individual O-Ring material options and 'None', but keep the main 'O-Rings' dropdown
                if option['name'] in oring_material_names:
                    logger.debug(f"Skipping option: {option['name']}")
                    continue
                # Collect exotic metal options for grouping
                if option['name'] == 'Exotic Metals' or (
                    isinstance(option.get('choices'), list) and any(
                        c in exotic_metal_names for c in option['choices']
                    )
                ):
                    exotic_metal_option = option
                    for c in option.get('choices', []):
                        if c not in exotic_metal_choices and c in exotic_metal_names:
                            exotic_metal_choices.append(c)
                    continue
                if not option.get('choices'):
                    logger.warning(f"Option {option['name']} has no choices, skipping")
                    continue
                logger.debug(f"Creating control for option: {option['name']}")
                logger.debug(f"Option details: choices={option['choices']}, adders={option['adders']}")
                try:
                    if isinstance(option['choices'], list):
                        combo = QComboBox()
                        combo.setObjectName(f"option_{option['name']}")
                        adders = option.get('adders', {})
                        for choice in option['choices']:
                            # Show price adder if present and nonzero
                            price_adder = adders.get(choice, 0) if isinstance(adders, dict) else 0
                            if price_adder:
                                display_text = f"{choice} (+${price_adder:.2f})"
                            else:
                                display_text = str(choice)
                            combo.addItem(display_text, choice)
                        combo.currentIndexChanged.connect(
                            lambda idx, name=option['name'], cmb=combo: self._on_option_changed(
                                name, cmb.currentData()
                            )
                        )
                        # Rename 'Mounting' label to 'Connection' in the UI
                        label_name = 'Connection' if option['name'] == 'Mounting' else option['name']
                        form_layout.addRow(f"{label_name}:", combo)
                        self.option_widgets[option['name']] = combo
                        logger.debug(f"Added combo box for {option['name']}")
                except Exception as e:
                    logger.error(f"Error creating control for option {option['name']}: {str(e)}", exc_info=True)

        # Add the combined Exotic Metals dropdown if any options were found
        if exotic_metal_choices:
            combo = QComboBox()
            combo.setObjectName("option_Exotic Metals")
            combo.addItem("None", "None")  # Add None as first option
            for choice in sorted(exotic_metal_choices):  # Sort choices alphabetically
                combo.addItem(str(choice), choice)
            combo.currentIndexChanged.connect(
                lambda idx, cmb=combo: self._on_option_changed("Exotic Metals", cmb.currentData())
            )
            form_layout.addRow("Exotic Metals:", combo)
            self.option_widgets["Exotic Metals"] = combo
            logger.debug("Added combined Exotic Metals combo box")

        # Set default values for core options after they have been created
        self._set_initial_option_value('Voltage', product.get('voltage'))
        self._set_initial_option_value('Material', product.get('material'))
        self._set_initial_option_value('Probe Length', product.get('base_length'))

        # --- Minimalistic fix: trigger option changed for defaults to update price ---
        # Voltage
        voltage_widget = self.option_widgets.get('Voltage')
        if isinstance(voltage_widget, QComboBox) and voltage_widget.currentIndex() >= 0:
            self._on_option_changed('Voltage', voltage_widget.currentData())
        # Material
        material_widget = self.option_widgets.get('Material')
        if isinstance(material_widget, QComboBox) and material_widget.currentIndex() >= 0:
            self._on_option_changed('Material', material_widget.currentData())
        # Probe Length
        probe_length_widget = self.option_widgets.get('Probe Length')
        if isinstance(probe_length_widget, QSpinBox):
            self._on_option_changed('Probe Length', probe_length_widget.value())

        # Add a spacer after all options
        form_layout.addRow(QWidget())

    def _set_initial_option_value(self, option_name, value):
        """Sets the initial value of a configuration widget, handling different widget types."""
        if option_name not in self.option_widgets or value is None:
            return

        widget = self.option_widgets[option_name]

        if isinstance(widget, QComboBox):
            # For QComboBox, find the index where the item data matches the value.
            # The data could be str, int, or float, so we compare as strings.
            str_value = str(value)
            if isinstance(value, float) and value.is_integer():
                str_value = str(int(value))

            for i in range(widget.count()):
                item_data_str = str(widget.itemData(i))
                if item_data_str == str_value:
                    widget.setCurrentIndex(i)
                    return

        elif isinstance(widget, QHBoxLayout):
            # For QHBoxLayout (radio buttons), find the button with the matching 'choice' property.
            for i in range(widget.count()):
                button = widget.itemAt(i).widget()
                if (
                    isinstance(button, QPushButton)
                    and button.property('choice') == value
                ):
                    button.setChecked(True)
                    return

    def _setup_quantity_and_total(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel('Quantity:'))
        self.quantity_spinner = QSpinBox()
        self.quantity_spinner.setRange(1, 999)
        self.quantity_spinner.setValue(self.quantity)
        self.quantity_spinner.valueChanged.connect(self._on_quantity_changed)
        h_layout.addWidget(self.quantity_spinner)
        h_layout.addStretch()
        self.config_layout.addLayout(h_layout)

    def _setup_add_button(self):
        self.add_button = QPushButton('Add to Quote')
        self.add_button.clicked.connect(self._on_add_to_quote)
        self.config_layout.addWidget(self.add_button)

    def _update_total_price(self):
        """Update the total price display."""
        try:
            logger.info("Starting total price update in dialog")
            if not self.config_service.current_config:
                logger.warning("No current configuration when updating total price")
                self.total_price_label.setText("$0.00")
                return
                
            final_price = self.config_service.current_config.final_price
            logger.info(f"Retrieved final price from config service: ${final_price:,.2f}")
            
            # Format the price
            formatted_price = f"${final_price:,.2f}"
            logger.info(f"Formatted price for display: {formatted_price}")
            
            # Update the label
            self.total_price_label.setText(formatted_price)
            logger.info("Updated total price label in UI")
            
        except Exception as e:
            logger.error(f"Error updating total price: {str(e)}", exc_info=True)
            self.total_price_label.setText("$0.00")

    def _on_quantity_changed(self, value: int):
        """Handle changes to quantity."""
        try:
            logger.info(f"Quantity changed to: {value}")
            if self.config_service.current_config:
                self.config_service.current_config.quantity = value
                logger.info("Updated quantity in configuration")
                
                # Update the price display
                self._update_total_price()
                logger.info("Triggered total price update after quantity change")
            else:
                logger.warning("No current configuration when quantity changed")
                
        except Exception as e:
            logger.error(f"Error handling quantity change: {str(e)}", exc_info=True)

    def _on_option_changed(self, option_name: str, value: Union[str, int, float, bool, None]):
        """Handle changes to any option value."""
        try:
            logger.info(f"Option changed: {option_name}={value}")
            self.config_service.select_option(option_name, value)
            logger.info("Updated configuration service with new option")
            
            # Update the price display
            self._update_total_price()
            logger.info("Triggered total price update after option change")
            self._update_model_number_label()
        except Exception as e:
            logger.error(f"Error handling option change: {str(e)}", exc_info=True)

    def _setup_connection_options(self, form_layout: QFormLayout, options: list):
        """Creates UI controls for connection options."""
        logger.debug(f'Setting up connection options. Received {len(options)} options.')
        if not options:
            return

        # Create the main connection type dropdown
        self.connection_type_combo = QComboBox()
        self.connection_type_combo.addItem('None', None)  # Add a 'None' option

        # Add connection types from the options
        connection_types = sorted({opt['type'] for opt in options})
        for conn_type in connection_types:
            # Find the first option with this type to get its price
            price = next(
                (opt['price'] for opt in options if opt['type'] == conn_type), 0
            )
            price_val = price or 0  # Treat None as 0 for comparison/formatting
            display_text = (
                f"{conn_type} (+${price_val:.2f})" if price_val > 0 else conn_type
            )
            self.connection_type_combo.addItem(display_text, conn_type)

        form_layout.addRow('Connection Type:', self.connection_type_combo)
        self.option_widgets['Connection Type'] = self.connection_type_combo

        # Placeholder for sub-option layouts
        self.connection_sub_options_layout = QVBoxLayout()
        form_layout.addRow(self.connection_sub_options_layout)

        # Connect signal to handler that will show/hide sub-options
        self.connection_type_combo.currentTextChanged.connect(
            lambda text: self._on_connection_type_changed(text, options)
        )

    def _on_connection_type_changed(self, selected_type: str, all_options: list):
        """Shows/hides sub-options based on the selected connection type."""
        # Clear previous sub-options
        while self.connection_sub_options_layout.count():
            child = self.connection_sub_options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add selected connection type to config
        self.config_service.select_option(
            'Connection Type', selected_type if selected_type != 'None' else None
        )
        self._update_total_price()

        if selected_type == 'None':
            return

        # Create a new form layout for the sub-options
        sub_form_layout = QFormLayout()

        # Filter options for the selected connection type
        type_options = [opt for opt in all_options if opt['type'] == selected_type]

        # Add rating options if available
        ratings = sorted({opt['rating'] for opt in type_options if opt['rating']})
        if ratings:
            rating_combo = QComboBox()
            for rating in ratings:
                price = next(
                    (opt['price'] for opt in type_options if opt['rating'] == rating), 0
                )
                price_val = price or 0
                display_text = (
                    f"{rating} (+${price_val:.2f})" if price_val > 0 else rating
                )
                rating_combo.addItem(display_text, rating)
            sub_form_layout.addRow('Rating:', rating_combo)
            self.option_widgets['Rating'] = rating_combo
            rating_combo.currentTextChanged.connect(
                lambda text: self._on_sub_option_changed('Rating', text)
            )

        # Add size options if available
        sizes = sorted({opt['size'] for opt in type_options if opt['size']})
        if sizes:
            size_combo = QComboBox()
            for size in sizes:
                price = next(
                    (opt['price'] for opt in type_options if opt['size'] == size), 0
                )
                price_val = price or 0
                display_text = (
                    f"{size} (+${price_val:.2f})" if price_val > 0 else size
                )
                size_combo.addItem(display_text, size)
            sub_form_layout.addRow('Size:', size_combo)
            self.option_widgets['Size'] = size_combo
            size_combo.currentTextChanged.connect(
                lambda text: self._on_sub_option_changed('Size', text)
            )

        # Add the sub-form to the main sub-options layout
        self.connection_sub_options_layout.addLayout(sub_form_layout)

        # Initialize the first values
        if ratings:
            self._on_sub_option_changed(
                'Rating', self.option_widgets['Rating'].currentText()
            )
        if sizes:
            self._on_sub_option_changed(
                'Size', self.option_widgets['Size'].currentText()
            )

    def _on_sub_option_changed(self, option_name: str, value: str):
        """Generic handler for any sub-option change."""
        # The 'value' from currentTextChanged is the display text, we need the data
        sender_combo = self.option_widgets.get(option_name)
        if sender_combo:
            actual_value = sender_combo.currentData()
            logger.debug(f"Sub-option '{option_name}' changed to '{actual_value}'")
            self.config_service.select_option(option_name, actual_value)
            self._update_total_price()

    def _clear_config_panel(self):
        """Clears all widgets from the configuration panel."""
        for i in reversed(range(self.config_layout.count())):
            item = self.config_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _clear_layout(self, layout):
        """Recursively clears all widgets from a layout."""
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self._clear_layout(sub_layout)

    def _on_add_to_quote(self):
        # Validation logic will be moved to ConfigurationService
        if not self.config_service.current_config:
            QMessageBox.warning(self, 'Warning', 'Please select a product.')
            return

        final_config = self.config_service.current_config
        product_data = {
            'id': str(final_config.product_family_id),
            'part_number': final_config.model_number,
            'product_family_id': final_config.product_family_id,
            'product_family_name': final_config.product_family_name,
            'quantity': self.quantity,
            'base_price': final_config.final_price,
            'unit_price': final_config.final_price,
            'description': self.config_service.get_final_description(),
            'options': [
                {
                    'name': name,
                    'selected': value,
                    'price': final_config.get_option_price(name, value) or 0,
                }
                for name, value in final_config.selected_options.items()
            ],
        }
        self.product_added.emit(product_data)
        self.accept()

    def _populate_for_edit(self):
        # This will use the config_service to load an existing configuration
        pass

    def _get_current_product_family(self) -> Optional[dict]:
        """Gets the currently selected product family from the list."""
        items = self.product_list.selectedItems()
        if not items:
            return None
        return items[0].data(Qt.UserRole)

    def _setup_mechanical_options(self, form_layout: QFormLayout):
        """Set up the mechanical options as a multi-selectable list."""
        mechanical_group = QGroupBox('Mechanical Options')
        mechanical_layout = QVBoxLayout()
        
        # Create a list widget with checkboxes
        mechanical_list = QListWidget()
        mechanical_list.setSelectionMode(QListWidget.MultiSelection)
        
        # Get the current product family name
        product_family = self.config_service.current_config.product_family_name if self.config_service.current_config else None
        
        # Define mechanical options based on product family
        if product_family == 'LS2100':
            mechanical_options = [
                ('Cable Probe', 80.00),
                ('Bent Probe', 50.00),
                ('Stainless Steel Tag', 30.00)
            ]
        elif product_family == 'LS6000':
            mechanical_options = [
                ('Stainless Steel Tag', 30.00),
                ('Cable Probe', 80.00),
                ('Bent Probe', 50.00),
                ('Teflon Insulator', 40.00),
                ('3/4" Diameter Probe x 10"', 175.00)
            ]
        elif product_family == 'LS7000':
            mechanical_options = [
                ('3/4" Diameter Probe x 10"', 175.00),
                ('Stainless Steel Housing (NEMA 4X)', 285.00),
                ('Cable Probe', 80.00),
                ('Bent Probe', 50.00),
                ('Stainless Steel Tag', 30.00)
            ]
        elif product_family == 'LS7000/2':
            mechanical_options = [
                ('Stainless Steel Tag', 30.00)
            ]
        elif product_family == 'LS8000':
            mechanical_options = [
                ('22 AWG, Twisted Shielded Pair', 0.70),  # Price per foot
                ('8" x 6" x 3.5" NEMA 4 Metal Enclosure for Receiver', 245.00),
                ('GRE EXP PROOF HOUSING FOR RECEIVER', 590.00),
                ('Cable Probe', 80.00),
                ('Bent Probe', 50.00),
                ('Stainless Steel Tag', 30.00)
            ]
        elif product_family == 'LS8000/2':
            mechanical_options = [
                ('22 AWG, Twisted Shielded Pair', 0.70),  # Price per foot
                ('10" x 8" x 4" NEMA 4 Metal Enclosure', 245.00),
                ('GRE EXP PROOF HOUSING FOR RECEIVER', 590.00),
                ('Stainless Steel Tag', 30.00)
            ]
        elif product_family == 'LT9000':
            mechanical_options = [
                ('Stainless Steel Tag', 30.00)
            ]
        elif product_family == 'FS10000':
            mechanical_options = [
                ('GRE EXP PROOF HOUSING FOR RECEIVER', 590.00)
            ]
        else:  # Default options for other models
            mechanical_options = [
                ('Stainless Steel Tag', 30.00),
                ('Cable Probe', 80.00),
                ('Bent Probe', 50.00),
                ('Teflon Insulator', 40.00),
                ('Extra Static Protection', 30.00)
            ]
        
        for option_name, price in mechanical_options:
            # Special formatting for per-foot pricing
            if option_name == '22 AWG, Twisted Shielded Pair':
                display_text = f"{option_name} (+${price:.2f}/foot)"
            else:
                display_text = f"{option_name} (+${price:.2f})"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, {'name': option_name, 'price': price})
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            mechanical_list.addItem(item)
        
        # Set fixed height based on number of items (25 pixels per item + 10 pixels padding)
        item_height = 25
        padding = 10
        mechanical_list.setFixedHeight(len(mechanical_options) * item_height + padding)
        
        # Connect the item changed signal
        mechanical_list.itemChanged.connect(
            lambda item: self._on_mechanical_option_changed(item)
        )
        
        mechanical_layout.addWidget(mechanical_list)
        mechanical_group.setLayout(mechanical_layout)
        form_layout.addRow(mechanical_group)
        self.option_widgets['Mechanical Options'] = mechanical_list

    def _on_mechanical_option_changed(self, item):
        """Handle changes to mechanical options selection."""
        if not self.config_service.current_config:
            return
            
        option_data = item.data(Qt.UserRole)
        option_name = option_data['name']
        is_selected = item.checkState() == Qt.Checked
        
        # Update the configuration service
        if is_selected:
            self.config_service.select_option(option_name, 'Yes')
        else:
            self.config_service.select_option(option_name, 'No')
            
        self._update_total_price()

    def _update_option_price(self, option_name: str, value: any):
        """Update the price display for a specific option."""
        if self.config_service.current_config:
            option = self.config_service.current_config.get_option(option_name)
            if option and hasattr(option, 'price'):
                price_label = self.option_price_labels.get(option_name)
                if price_label:
                    price_label.setText(f'${option.price:,.2f}')
            self._update_total_price()

    def _setup_option_row(self, option_name: str, option_data: dict):
        """Set up a row for an option in the configuration layout."""
        row_layout = QHBoxLayout()
        
        # Option name and value
        option_label = QLabel(f"{option_data.get('label', option_name)}:")
        option_label.setMinimumWidth(150)
        row_layout.addWidget(option_label)

        # Option value widget (combo box, checkbox, etc.)
        value_widget = self._create_option_widget(option_name, option_data)
        row_layout.addWidget(value_widget)

        # Price label
        price_label = QLabel('$0.00')
        price_label.setMinimumWidth(100)
        price_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.option_price_labels[option_name] = price_label
        row_layout.addWidget(price_label)

        self.config_layout.addLayout(row_layout)

    def _update_model_number_label(self):
        """Update the model number label based on current selections."""
        # Get the selected product/model name
        product = self._get_current_product_family()
        if not product:
            self.model_number_label.setText('Model: PENDING...')
            return
        model = product.get('name', 'PENDING')

        # Get voltage
        voltage = None
        voltage_widget = self.option_widgets.get('Voltage')
        if isinstance(voltage_widget, QComboBox) and voltage_widget.currentIndex() >= 0:
            voltage = voltage_widget.currentData()
        if not voltage:
            voltage = product.get('voltage', 'PENDING')

        # Get material code
        material_code = None
        material_widget = self.option_widgets.get('Material')
        if isinstance(material_widget, QComboBox) and material_widget.currentIndex() >= 0:
            material_code = material_widget.currentData()
        if not material_code:
            material_code = product.get('material', 'PENDING')

        # Get probe length
        probe_length = None
        probe_length_widget = self.option_widgets.get('Probe Length')
        if isinstance(probe_length_widget, QSpinBox):
            probe_length = probe_length_widget.value()
        if not probe_length:
            probe_length = product.get('base_length', 'PENDING')

        # Format probe length with inch symbol
        probe_length_str = f'{probe_length}"' if probe_length != 'PENDING' else 'PENDING'

        # Build model number string
        model_number = f"{model}-{voltage}-{material_code}-{probe_length_str}"
        self.model_number_label.setText(f"Model: {model_number}")
