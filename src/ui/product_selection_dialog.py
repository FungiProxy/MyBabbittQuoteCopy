"""
Product Selection Dialog for Adding Products to Quote.

This dialog provides a two-panel interface:
- Left: Product search and selection
- Right: Product configuration and add-to-quote
"""

import logging
from typing import Optional, Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
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
)

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
                base_product = self.product_service.get_base_product_for_family(
                    self.db, fam['name']
                )
                if base_product:
                    products.append(base_product)
                else:
                    logger.warning(
                        f"Could not fetch base product for family: {fam['name']}"
                    )
            self.products = products
            logger.info(f'Loaded {len(products)} base products for families')
        except Exception as e:
            logger.error(
                f'A critical error occurred while fetching base products: {e}',
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
            logger.debug('No items selected, showing select product prompt')
            self._show_select_product()
            return

        product_data = items[0].data(Qt.UserRole)
        logger.debug(f'Selected product data: {product_data}')

        try:
            logger.debug(
                f"Starting configuration for product family: {product_data['name']}"
            )
            self.config_service.start_configuration(
                product_family_id=product_data['id'],
                product_family_name=product_data['name'],
                base_product_info=product_data,
            )
            self.quantity = 1
            self._show_product_config(product_data)
        except Exception as e:
            logger.error(f'Error starting configuration: {e!s}', exc_info=True)
            QMessageBox.critical(
                self, 'Error', f'Failed to configure product: {e!s}'
            )

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
            logger.debug('Setting up core options')
            self._setup_core_options(form_layout, product)
        except Exception as e:
            logger.error(f'Error setting up core options: {e!s}', exc_info=True)
            QMessageBox.critical(
                self, 'Error', f'Failed to setup core options: {e!s}'
            )

        # Build dynamic options from unified structure
        try:
            logger.debug('Building dynamic options')
            self._build_dynamic_options(form_layout, product)
        except Exception as e:
            logger.error(f'Error building dynamic options: {e!s}', exc_info=True)
            QMessageBox.critical(
                self, 'Error', f'Failed to build dynamic options: {e!s}'
            )

        self.config_layout.addLayout(form_layout)
        self._setup_quantity_and_total()
        self._setup_add_button()
        self._update_total_price()
        self._update_model_number_label()

    def _get_material_base_length(self, material_code: str) -> Optional[float]:
        """Get the base length for a specific material from the database."""
        try:
            from src.core.models.material import Material
            material = self.db.query(Material).filter(Material.code == material_code).first()
            if material:
                return material.base_length
        except Exception as e:
            logger.error(f"Error getting base length for material {material_code}: {e}")
        return None

    def _setup_core_options(self, form_layout: QFormLayout, product: dict):
        """Set up core product options (Voltage, Material, Probe Length)."""
        logger.debug(f"Setting up core options for product: {product['name']}")

        # Get material options for this product family
        try:
            material_options = self.product_service.get_available_materials_for_product(
                self.db, product['name']
            )
            material_choices = material_options[0].get('choices', [])
        except (IndexError, KeyError) as e:
            logger.error(
                f'Could not find material choices for {product["name"]}: {e!s}',
                exc_info=True,
            )
            material_choices = []
            QMessageBox.warning(
                self, 'Warning', f'No material choices found for {product["name"]}.'
            )

        material_combo = QComboBox()
        for choice in material_choices:
            if isinstance(choice, dict):
                # Handle dict choices like {'code': 'S', 'display_name': ...}
                material_combo.addItem(choice.get('display_name', ''), choice.get('code', ''))
            else:
                # Handle simple string choices like 'S'
                material_combo.addItem(choice, choice)

        def on_material_changed():
            value = material_combo.currentData()
            logger.debug(f'Material changed to: {value}')
            self._on_option_changed('Material', value)
            
            # Automatically set probe length to the base length for this material
            material_base_length = self._get_material_base_length(value)
            if material_base_length is not None:
                # Update both the spin box and edit field
                spin_widget = self.option_widgets.get('Probe Length Spin')
                edit_widget = self.option_widgets.get('Probe Length Edit')
                if spin_widget and edit_widget:
                    # Block signals to prevent recursion
                    spin_widget.blockSignals(True)
                    edit_widget.blockSignals(True)
                    
                    # Set the values
                    length_value = int(material_base_length)
                    spin_widget.setValue(length_value)
                    edit_widget.setText(str(length_value))
                    
                    # Re-enable signals
                    spin_widget.blockSignals(False)
                    edit_widget.blockSignals(False)
                    
                    # Update the configuration
                    self._on_option_changed('Probe Length', length_value)
                    logger.debug(f'Auto-set probe length to {length_value}" for material {value}')
            
            self._update_total_price()
            # Handle exotic metal override display
            self._handle_exotic_metal_override(value)

        material_combo.currentIndexChanged.connect(on_material_changed)
        form_layout.addRow('Material:', material_combo)
        self.option_widgets['Material'] = material_combo

        # Get voltage options for this product family
        voltage_options = self.product_service.get_available_voltages(
            self.db, product['name']
        )
        logger.debug(f'Voltage options: {voltage_options}')

        # Add voltage selection
        if voltage_options:
            voltage_combo = QComboBox()
            voltage_combo.setObjectName('option_Voltage')
            for voltage in voltage_options:
                voltage_combo.addItem(
                    str(voltage), str(voltage)
                )  # Use voltage as both display and data

            def on_voltage_changed():
                value = voltage_combo.currentData()
                logger.debug(f'Voltage changed to: {value}')
                self._on_option_changed('Voltage', value)
                self._update_total_price()

            voltage_combo.currentIndexChanged.connect(on_voltage_changed)
            form_layout.addRow('Voltage:', voltage_combo)
            self.option_widgets['Voltage'] = voltage_combo
            logger.debug('Added voltage options to form')
        else:
            logger.warning(f"No voltage options found for {product['name']}")

        # Add probe length customization (both boxes always visible, integer only)
        probe_length_layout = QHBoxLayout()
        probe_length_spin = QSpinBox()
        probe_length_spin.setObjectName('option_Probe Length Spin')
        probe_length_spin.setRange(1, 120)
        probe_length_spin.setSuffix('"')
        if product.get('base_length'):
            probe_length_spin.setValue(int(product['base_length']))
        probe_length_spin.setFixedWidth(70)

        probe_length_edit = QLineEdit()
        probe_length_edit.setObjectName('option_Probe Length Edit')
        probe_length_edit.setPlaceholderText('Manual (1-120)')
        probe_length_edit.setFixedWidth(90)
        probe_length_edit.setText(str(probe_length_spin.value()))
        validator = QIntValidator(1, 120)
        probe_length_edit.setValidator(validator)

        probe_length_spin.partner = probe_length_edit
        probe_length_edit.partner = probe_length_spin

        # Sync: Spin -> Edit
        def on_spin_changed(val):
            probe_length_edit.setText(str(val))
            self._on_option_changed('Probe Length', val)

        probe_length_spin.valueChanged.connect(on_spin_changed)

        # Sync: Edit -> Spin (integer only)
        def on_edit_changed():
            text = probe_length_edit.text()
            try:
                val = int(text)
                val = max(1, min(120, val))
                probe_length_edit.blockSignals(True)
                probe_length_edit.setText(str(val))
                probe_length_edit.blockSignals(False)
                probe_length_spin.blockSignals(True)
                probe_length_spin.setValue(val)
                probe_length_spin.blockSignals(False)
                self._on_option_changed('Probe Length', val)
            except ValueError:
                # If invalid, revert to spin value
                probe_length_edit.setText(str(probe_length_spin.value()))

        probe_length_edit.textChanged.connect(on_edit_changed)

        probe_length_layout.addWidget(probe_length_spin)
        probe_length_layout.addWidget(probe_length_edit)
        form_layout.addRow('Probe Length:', probe_length_layout)
        self.option_widgets['Probe Length Spin'] = probe_length_spin
        self.option_widgets['Probe Length Edit'] = probe_length_edit

        # Set default values for this product family
        self._set_default_values(product['name'])

    def _handle_exotic_metal_override(self, material_value):
        """Show/hide manual override field based on material selection."""
        exotic_metals = ['A', 'HC', 'HB', 'TT']  # Use material codes

        if material_value in exotic_metals:
            self.exotic_override_widget.show()
            logger.debug(f'Showing manual override for exotic metal: {material_value}')
        else:
            self.exotic_override_widget.hide()
            # Clear the override value when hiding
            if hasattr(self, 'exotic_override_input'):
                self.exotic_override_input.clear()
                self._on_option_changed('Exotic Metal Override', 0)
            logger.debug(f'Hiding manual override for material: {material_value}')

    def _set_default_values(self, family_name: str):
        """Set default values for the selected product family."""
        logger.debug(f'Setting default values for {family_name}')

        # Define default configurations for each family
        default_configs = {
            'LS2000': {'Voltage': '115VAC', 'Material': 'S', 'Probe Length': 10},
            'LS2100': {'Voltage': '24VDC', 'Material': 'S', 'Probe Length': 10},
            'LS6000': {'Voltage': '115VAC', 'Material': 'S', 'Probe Length': 10},
            'LS7000': {'Voltage': '115VAC', 'Material': 'S', 'Probe Length': 10},
            'LS7000/2': {'Voltage': '115VAC', 'Material': 'H', 'Probe Length': 10},
            'LS8000': {'Voltage': '115VAC', 'Material': 'S', 'Probe Length': 10},
            'LS8000/2': {'Voltage': '115VAC', 'Material': 'H', 'Probe Length': 10},
            'LT9000': {'Voltage': '115VAC', 'Material': 'H', 'Probe Length': 10},
            'FS10000': {'Voltage': '115VAC', 'Material': 'S', 'Probe Length': 6},
            'LS7500': {'Voltage': '115VAC', 'Material': 'S', 'Probe Length': 10},
        }

        defaults = default_configs.get(family_name, {})
        logger.debug(f'Default config for {family_name}: {defaults}')

        # Set default values for each option
        for option_name, default_value in defaults.items():
            if option_name == 'Probe Length':
                # Handle probe length widgets
                spin_widget = self.option_widgets.get('Probe Length Spin')
                edit_widget = self.option_widgets.get('Probe Length Edit')
                if spin_widget and edit_widget:
                    spin_widget.setValue(default_value)
                    edit_widget.setText(str(default_value))
                    self._on_option_changed('Probe Length', default_value)
                    logger.debug(f'Set {option_name} to {default_value}')
            else:
                # Handle combo boxes (Voltage, Material)
                widget = self.option_widgets.get(option_name)
                if widget:
                    for i in range(widget.count()):
                        if widget.itemData(i) == default_value:
                            widget.setCurrentIndex(i)
                            self._on_option_changed(option_name, default_value)
                            logger.debug(f'Set {option_name} to {default_value}')
                            break
        # Update price after all defaults are set
        self._update_total_price()

    def _build_dynamic_options(self, form_layout: QFormLayout, product: dict):
        """Build dynamic options from the unified options structure."""
        logger.debug(f"Building dynamic options for product: {product['name']}")

        try:
            # Get all additional options for this product family
            all_options = self.product_service.get_additional_options(
                self.db, product['name']
            )
            logger.debug(f"Found {len(all_options)} options for {product['name']}")

            # Group options by category for better organization
            options_by_category = {}
            for option in all_options:
                category = option.get('category', 'Other')
                if category not in options_by_category:
                    options_by_category[category] = []
                options_by_category[category].append(option)

            # Process each category
            for category, options in options_by_category.items():
                logger.debug(
                    f'Processing category: {category} with {len(options)} options'
                )

                # Skip Material and Voltage as they're handled in core options
                if category in ['Material', 'Voltage']:
                    continue

                # Create a group for this category
                category_group = QGroupBox(category)
                category_layout = QVBoxLayout()

                for option in options:
                    option_name = option.get('name', 'Unknown')
                    choices = option.get('choices', [])
                    adders = option.get('adders', {})

                    logger.debug(f'  Processing option: {option_name}')
                    logger.debug(f'    Choices: {choices}')
                    logger.debug(f'    Adders: {adders}')

                    # Only create widget if we have valid choices
                    if not isinstance(choices, list) or not choices:
                        logger.debug(f'    Skipping {option_name} - no valid choices')
                        continue

                    # Create the appropriate widget based on option type
                    widget = self._create_option_widget(option_name, choices, adders)
                    if widget:
                        category_layout.addWidget(widget)
                        self.option_widgets[option_name] = widget
                        logger.debug(f'    Added widget for {option_name}')

                # Only add category group if it has widgets
                if category_layout.count() > 0:
                    category_group.setLayout(category_layout)
                    form_layout.addRow(category_group)
                    logger.debug(f'Added category group: {category}')

        except Exception as e:
            logger.error(f'Error building dynamic options: {e!s}', exc_info=True)
            QMessageBox.critical(
                self, 'Error', f'Failed to build dynamic options: {e!s}'
            )

    def _create_option_widget(self, option_name: str, choices: list, adders: dict):
        """Create the appropriate widget for an option based on its choices."""
        logger.debug(f'Creating widget for {option_name}')

        # Handle different choice formats
        if isinstance(choices[0], dict):
            # New format: list of dicts with code, display_name, etc.
            codes = [choice.get('code', '') for choice in choices]
            display_names = {
                choice.get('code', ''): choice.get('display_name', '')
                for choice in choices
            }
        else:
            # Old format: list of strings
            codes = choices
            display_names = {code: code for code in codes}

        # Create combo box for selection
        combo = QComboBox()
        combo.setObjectName(f'option_{option_name}')

        # Add items with pricing information
        for code in codes:
            display_name = display_names.get(code, code)
            price_adder = adders.get(code, 0) if isinstance(adders, dict) else 0
            if price_adder != 0:
                display_name = f'{display_name} (+${price_adder:.2f})'
            combo.addItem(display_name, code)

        # Connect change handler
        def on_option_changed():
            value = combo.currentData()
            logger.debug(f'{option_name} changed to: {value}')
            self._on_option_changed(option_name, value)

        combo.currentIndexChanged.connect(on_option_changed)

        # Create label and layout
        label = QLabel(f'{option_name}:')
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(combo)
        layout.addStretch()

        # Create container widget
        container = QWidget()
        container.setLayout(layout)

        return container

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
            logger.info('Starting total price update in dialog')
            if not self.config_service.current_config:
                logger.warning('No current configuration when updating total price')
                self.total_price_label.setText('$0.00')
                return

            final_price = self.config_service.current_config.final_price
            logger.info(
                f'Retrieved final price from config service: ${final_price:,.2f}'
            )

            # Format the price
            formatted_price = f'${final_price:,.2f}'
            logger.info(f'Formatted price for display: {formatted_price}')

            # Update the label
            self.total_price_label.setText(formatted_price)
            logger.info('Updated total price label in UI')

        except Exception as e:
            logger.error(f'Error updating total price: {e!s}', exc_info=True)
            self.total_price_label.setText('$0.00')

    def _on_quantity_changed(self, value: int):
        """Handle changes to quantity."""
        try:
            logger.info(f'Quantity changed to: {value}')
            if self.config_service.current_config:
                self.config_service.current_config.quantity = value
                logger.info('Updated quantity in configuration')

                # Update the price display
                self._update_total_price()
                logger.info('Triggered total price update after quantity change')
            else:
                logger.warning('No current configuration when quantity changed')

        except Exception as e:
            logger.error(f'Error handling quantity change: {e!s}', exc_info=True)

    def _on_option_changed(
        self, option_name: str, value: Union[str, int, float, bool, None]
    ):
        """Handle changes to any option value."""
        try:
            logger.info(f'Option changed: {option_name}={value}')
            self.config_service.select_option(option_name, value)
            logger.info('Updated configuration service with new option')

            # Update the price display
            self._update_total_price()
            logger.info('Triggered total price update after option change')
            self._update_model_number_label()
        except Exception as e:
            logger.error(f'Error handling option change: {e!s}', exc_info=True)

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
        if (
            isinstance(material_widget, QComboBox)
            and material_widget.currentIndex() >= 0
        ):
            material_code = material_widget.currentData()
        if not material_code:
            material_code = product.get('material', 'PENDING')

        # Get probe length
        probe_length = None
        probe_length_widget = self.option_widgets.get('Probe Length Spin')
        if isinstance(probe_length_widget, QSpinBox):
            probe_length = probe_length_widget.value()
        if not probe_length:
            probe_length = product.get('base_length', 'PENDING')

        # Format probe length with inch symbol
        probe_length_str = (
            f'{probe_length}"' if probe_length != 'PENDING' else 'PENDING'
        )

        # Build model number string
        model_number = f'{model}-{voltage}-{material_code}-{probe_length_str}'
        self.model_number_label.setText(f'Model: {model_number}')
