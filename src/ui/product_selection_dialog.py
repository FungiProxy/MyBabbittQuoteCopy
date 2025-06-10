"""
Product Selection Dialog for Adding Products to Quote.

This dialog provides a two-panel interface:
- Left: Product search and selection
- Right: Product configuration and add-to-quote
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QFrame, QButtonGroup, QRadioButton, QSpinBox, QSizePolicy, QWidget, QScrollArea, QCheckBox,
    QComboBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.models.option import Option
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProductSelectionDialog(QDialog):
    """
    Modal dialog for selecting and configuring a product to add to a quote.
    Emits product_added(product_data) when a product is configured and added.
    """
    product_added = Signal(dict)

    def __init__(self, product_service: ProductService, parent=None, product_to_edit=None):
        super().__init__(parent)
        self.product_to_edit = product_to_edit
        self.is_edit_mode = self.product_to_edit is not None
        
        title = "Edit Product" if self.is_edit_mode else "Add Product to Quote"
        self.setWindowTitle(title)
        
        self.resize(900, 600)

        # Services
        self.db = SessionLocal()
        self.product_service = product_service
        self.config_service = ConfigurationService(self.db, self.product_service)
        
        # State
        self.products = []
        self.quantity = 1 # Default quantity
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
        logger.info("Starting to fetch product families...")
        try:
            # Fetch all product families (models)
            family_objs = self.product_service.get_product_families(self.db)
            logger.info(f"Fetched {len(family_objs)} product families from the service.")
            if not family_objs:
                logger.warning("No product families returned from service. The product list will be empty.")

            # For each family, get the base variant to get pricing info
            products = []
            for fam in family_objs:
                logger.debug(f"Processing family: {fam['name']} (ID: {fam['id']})")
                variants = self.product_service.get_variants_for_family(self.db, fam['id'])
                logger.debug(f"Found {len(variants)} variants for family {fam['name']}")
                
                if variants:
                    # Use the first variant as the base for display
                    variant = variants[0]
                    product_info = {
                        "id": fam["id"],
                        "name": fam["name"],
                        "description": fam.get("description", ""),
                        "category": fam.get("category", ""),
                        "base_price": variant['base_price'],
                        "base_length": variant['base_length'],
                        "voltage": variant['voltage'],
                        "material": variant['material']
                    }
                    logger.debug(f"Adding product to UI list: {product_info['name']}")
                    products.append(product_info)
                else:
                    logger.warning(f"No variants found for family: {fam['name']}. It will not be displayed.")
            
            self.products = products
            logger.info(f"Total products loaded for UI: {len(self.products)}")
        except Exception as e:
            logger.error(f"A critical error occurred while fetching product families: {e}", exc_info=True)
            self.products = []
        finally:
            logger.info("Finished fetching products.")
        # The session is managed by the dialog's lifecycle now, so no db.close() here

    def _product_to_dict(self, product):
        """Convert a ProductVariant SQLAlchemy object to a dictionary for UI use."""
        return {
            "id": getattr(product, "id", None),
            "name": getattr(product, "model_number", ""),
            "description": getattr(product, "description", ""),
            "category": getattr(product.product_family, "category", ""),
            "base_price": getattr(product, "base_price", 0),
            "voltage": getattr(product, "voltage", ""),
            "material": getattr(product, "material", ""),
            # Add more fields/options as needed
        }

    def _init_ui(self):
        """Set up the dialog UI layout and widgets."""
        main_layout = QHBoxLayout(self)
        # Left: Product List/Search
        left_panel = QFrame()
        left_panel.setFixedWidth(340)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 20, 10, 20)
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search products...")
        self.search_bar.textChanged.connect(self._filter_products)
        left_layout.addWidget(self.search_bar)
        # Product list
        self.product_list = QListWidget()
        self.product_list.setSpacing(8)
        self.product_list.itemSelectionChanged.connect(self._on_product_selected)
        left_layout.addWidget(self.product_list, 1)
        main_layout.addWidget(left_panel)
        # Right: Product Config
        self.right_panel = QFrame()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(30, 20, 30, 20)
        self.config_scroll = QScrollArea()
        self.config_scroll.setWidgetResizable(True)
        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)
        self.config_layout.setAlignment(Qt.AlignTop)
        self.config_scroll.setWidget(self.config_widget)
        right_layout.addWidget(self.config_scroll)
        main_layout.addWidget(self.right_panel, 1)
        self._populate_product_list()

        if not self.is_edit_mode:
            self._show_select_product()

    def _populate_product_list(self, filter_text=""):
        """Populate the product list, optionally filtering by search text."""
        self.product_list.clear()
        filtered_products = [product for product in self.products if filter_text.lower() in product["name"].lower()]
        logger.debug(f"Filtered products: {len(filtered_products)}")
        
        for product in filtered_products:
            item = QListWidgetItem()
            item.setText(f"{product['name']}")
            item.setData(Qt.UserRole, product)
            self.product_list.addItem(item)
            logger.debug(f"Added product to list: {product['name']}")

    def _filter_products(self, text):
        self._populate_product_list(text)

    def _on_product_selected(self):
        """Handle product selection from the list."""
        items = self.product_list.selectedItems()
        logger.debug(f"Product selection changed. Selected items: {len(items)}")
        
        if not items:
            logger.debug("No items selected. Showing select product prompt.")
            self._show_select_product()
            return
            
        product_data = items[0].data(Qt.UserRole)
        logger.debug(f"Selected product: {product_data}")

        # Start a new configuration session using the service
        self.config_service.start_configuration(
            product_family_id=product_data['id'],
            product_family_name=product_data['name'],
            base_product_info=product_data
        )
        
        self.quantity = 1 # Reset quantity on new selection
        self._show_product_config(product_data)

    def _show_select_product(self):
        # Show prompt to select a product
        self._clear_config_panel()
        prompt = QLabel("<div align='center'><br><br><span style='font-size:22px; color:#2563eb;'>✔</span><br><b>Select a Product</b><br><span style='color:#888;'>Choose a product from the list on the left to configure and add it to your quote.</span></div>")
        prompt.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(prompt)

    def _show_product_config(self, product):
        """Show the configuration options for the selected product."""
        logger.debug(f"Showing product config for: {product['name']}")
        self._clear_config_panel()
        self.option_widgets = {}
        
        try:
            # Start a new configuration session
            self.config_service.start_configuration(
                product_family_id=product['id'],
                product_family_name=product['name'],
                base_product_info=product
            )
            
            # Product details header
            details = QLabel(f"<b>{product['name']}</b><br><span style='color:#888;'>{product['description']}</span>")
            details.setWordWrap(True)
            details.setStyleSheet("margin-bottom: 20px;")
            self.config_layout.addWidget(details)
            
            # Main form layout for options
            form_layout = QFormLayout()
            form_layout.setSpacing(15)
            form_layout.setContentsMargins(0, 0, 0, 0)
            form_layout.setLabelAlignment(Qt.AlignRight)
            
            # Get all available options
            all_options = self.product_service.get_all_additional_options(self.db)
            logger.debug(f"Found {len(all_options)} additional options")
            
            # Group options by category
            grouped_options = {}
            for opt in all_options:
                if opt.category not in grouped_options:
                    grouped_options[opt.category] = []
                grouped_options[opt.category].append(opt)
            
            logger.debug(f"Grouped options by category: {list(grouped_options.keys())}")
            
            # Core options (Voltage, Material, Length)
            try:
                self._setup_core_options(form_layout, product, grouped_options)
            except Exception as e:
                logger.error(f"Error setting up core options: {e}", exc_info=True)
                raise
            
            # Connection options
            try:
                connection_options = self.product_service.get_connection_options(self.db, product['id'])
                logger.debug(f"Found {len(connection_options)} connection options")
                self._setup_connection_options(form_layout, connection_options)
            except Exception as e:
                logger.error(f"Error setting up connection options: {e}", exc_info=True)
                raise
            
            # Additional options (checkboxes)
            try:
                additional_options = grouped_options.get("additional", [])
                logger.debug(f"Found {len(additional_options)} additional options")
                self._setup_additional_options(form_layout, additional_options)
            except Exception as e:
                logger.error(f"Error setting up additional options: {e}", exc_info=True)
                raise
            
            # Add the form layout to the main config layout
            self.config_layout.addLayout(form_layout)
            
            # Quantity and total section
            self._setup_quantity_and_total()
            
            # Add to Quote button
            self._setup_add_button()
            
            # Initialize with default values
            self._initialize_option_values()
            
            # Update the total price
            self._update_total_price()
            
            logger.debug("Product configuration UI setup completed")
        except Exception as e:
            logger.error(f"Error setting up product configuration: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to load product configuration options: {str(e)}")

    def _setup_core_options(self, form_layout: QFormLayout, product: dict, grouped_options: dict):
        """Set up the core product options (Voltage, Material, Length)."""
        # Voltage options
        voltage_combo = QComboBox()
        voltage_combo.setMinimumWidth(200)
        voltage_options = self.product_service.get_voltage_options(self.db, product['id'])
        for v_opt in voltage_options:
            voltage_combo.addItem(v_opt['voltage'], userData=v_opt)
        voltage_combo.currentIndexChanged.connect(self._on_voltage_changed)
        form_layout.addRow("Voltage:", voltage_combo)
        self.option_widgets["Voltage"] = voltage_combo
        
        # Material options (if applicable)
        if not product['name'] in ["LS7500", "LS8500"]:
            material_combo = QComboBox()
            material_combo.setMinimumWidth(200)
            material_options = self.product_service.get_material_options(self.db, product['id'])
            for m_opt in material_options:
                material_combo.addItem(m_opt['display_name'], userData=m_opt)
            material_combo.currentIndexChanged.connect(self._on_material_changed)
            form_layout.addRow("Material:", material_combo)
            self.option_widgets["Material"] = material_combo
            
            # Probe Length
            length_widget = QWidget()
            length_layout = QHBoxLayout(length_widget)
            length_layout.setContentsMargins(0, 0, 0, 0)
            length_layout.setSpacing(10)
            
            self.length_spinner = QSpinBox()
            self.length_spinner.setRange(1, 120)
            self.length_spinner.setValue(product['base_length'])
            self.length_spinner.setSuffix('"')
            self.length_spinner.setFixedWidth(100)
            self.length_spinner.valueChanged.connect(self._on_length_changed)
            
            self.length_input = QLineEdit()
            self.length_input.setPlaceholderText("Enter length (inches)")
            self.length_input.setFixedWidth(100)
            self.length_input.setValidator(QIntValidator(1, 120))
            self.length_input.textChanged.connect(self._on_length_text_changed)
            
            length_layout.addWidget(self.length_spinner)
            length_layout.addWidget(self.length_input)
            length_layout.addStretch()
            
            form_layout.addRow("Probe Length:", length_widget)
            self.option_widgets["Probe Length"] = length_widget

    def _setup_additional_options(self, form_layout: QFormLayout, options: list):
        """Set up additional options as checkboxes."""
        if not options:
            return
            
        form_layout.addRow("", QLabel("<b>Additional Options</b>"))
        for opt in options:
            checkbox = QCheckBox(f"{opt.name} - Add ${opt.price:.2f}")
            checkbox.stateChanged.connect(
                lambda state, o=opt: self._on_option_selected(o.name, state == Qt.Checked)
            )
            form_layout.addRow("", checkbox)
            self.option_widgets[opt.name] = checkbox

    def _setup_quantity_and_total(self):
        """Set up the quantity selector and total price display."""
        # Quantity section
        qty_widget = QWidget()
        qty_layout = QHBoxLayout(qty_widget)
        qty_layout.setContentsMargins(0, 0, 0, 0)
        
        qty_label = QLabel("<b>Quantity</b>")
        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setValue(1)
        self.qty_spin.setFixedWidth(100)
        self.qty_spin.valueChanged.connect(self._on_quantity_changed)
        
        qty_layout.addWidget(qty_label)
        qty_layout.addWidget(self.qty_spin)
        qty_layout.addStretch()
        
        self.config_layout.addWidget(qty_widget)
        
        # Total price
        self.total_price_label = QLabel()
        self.total_price_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px 0;")
        self.config_layout.addWidget(self.total_price_label)

    def _setup_add_button(self):
        """Set up the Add to Quote button."""
        btn_text = "Update Item" if self.is_edit_mode else "+ Add to Quote"
        self.add_btn = QPushButton(btn_text)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                font-weight: bold;
                padding: 10px 24px;
                border-radius: 6px;
                font-size: 16px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        self.add_btn.clicked.connect(self._on_add_to_quote)
        self.config_layout.addWidget(self.add_btn, alignment=Qt.AlignCenter)

    def _initialize_option_values(self):
        """Initialize all option values with their defaults."""
        if "Voltage" in self.option_widgets:
            self._on_voltage_changed(self.option_widgets["Voltage"].currentIndex())
        if "Material" in self.option_widgets:
            self._on_material_changed(self.option_widgets["Material"].currentIndex())
        if "Probe Length" in self.option_widgets:
            self._on_length_changed(self.length_spinner.value())
            
        if self.is_edit_mode:
            self._apply_edited_product_options()

    def _update_total_price(self):
        """Update the total price display."""
        try:
            total = self.config_service.calculate_price() * self.quantity
            self.total_price_label.setText(f"Total: ${total:,.2f}")
        except Exception as e:
            logger.error(f"Error calculating total price: {e}", exc_info=True)
            self.total_price_label.setText("Error calculating price")

    def _on_quantity_changed(self, value):
        self.quantity = value
        self._update_total_price()

    def _on_voltage_changed(self, index):
        combo = self.sender()
        if isinstance(combo, QComboBox):
            option_data = combo.itemData(index)
            self.config_service.select_option("Voltage", option_data['voltage'])
            self._update_total_price()
        else:
            logger.error(f"_on_voltage_changed called from non-QComboBox sender: {type(combo)}")

    def _on_material_changed(self, index):
        combo = self.sender()
        if isinstance(combo, QComboBox):
            option_data = combo.itemData(index)
            self.config_service.select_option("Material", option_data['material_code'])
            self._update_total_price()
        else:
            logger.error(f"_on_material_changed called from non-QComboBox sender: {type(combo)}")

    def _on_length_changed(self, value):
        # Update the text input to match the spinner
        self.length_input.setText(str(value))
        self.config_service.select_option("Probe Length", value)
        self._update_total_price()
    
    def _on_length_text_changed(self, text):
        # Update the spinner to match the text input, if valid
        if text.isdigit():
            value = int(text)
            if 1 <= value <= 120:
                self.length_spinner.setValue(value)
                # No need to call _on_option_selected here as spinner's valueChanged will trigger it

    def _validate_probe_length(self):
        # This validation is now handled by the input widgets themselves (QIntValidator)
        # More complex validation could be moved to the ConfigurationService.
        return True

    def _on_option_selected(self, option_name, value, price=0, code=None):
        """
        Handles selection of any option.
        Updates the central configuration state via the service.
        """
        if not self.config_service.current_config:
            return
            
        # Use the configuration service to update the state
        self.config_service.select_option(option_name, value)
        
        logger.debug(f"Option selected: {option_name} = {value}")
        self._update_total_price()
    
    def _clear_config_panel(self):
        """Clear all widgets and layouts from the configuration panel."""
        def clear_layout_recursively(layout):
            """Recursively clear a layout and all its nested layouts."""
            if layout is None:
                return
                
            # Process all items in the layout
            while layout.count():
                child = layout.takeAt(0)
                
                if child.widget():
                    # If it's a widget, delete it
                    child.widget().deleteLater()
                elif child.layout():
                    # If it's a nested layout, clear it recursively first
                    clear_layout_recursively(child.layout())
                    # Then delete the layout itself
                    child.layout().deleteLater()
        
        # Clear the main config layout
        clear_layout_recursively(self.config_layout)
        
        # Reset the option widgets dictionary
        self.option_widgets = {}
        
        # Reset any instance variables that might hold references to widgets
        if hasattr(self, 'length_spinner'):
            self.length_spinner = None
        if hasattr(self, 'length_input'):
            self.length_input = None
        if hasattr(self, 'qty_spin'):
            self.qty_spin = None
        if hasattr(self, 'total_price_label'):
            self.total_price_label = None
        if hasattr(self, 'add_btn'):
            self.add_btn = None

    def _on_add_to_quote(self):
        if not self.config_service.current_config:
            QMessageBox.warning(self, "No Product Selected", "Please select a product before adding to the quote.")
            return

        # In the future, validation will be handled by the service
        # if not self.config_service.is_valid():
        #     errors = "\n".join(self.config_service.get_validation_errors())
        #     QMessageBox.critical(self, "Invalid Configuration", f"Please correct the following errors:\n{errors}")
        #     return
        
        # For now, we assume it's valid and get the data
        product_data = self.get_selected_product_data()
        self.product_added.emit(product_data)
        self.accept()

    def _validate_configuration(self):
        # This entire method will be replaced by calls to self.config_service.is_valid()
        # and self.config_service.get_validation_errors()
        return True

    def _on_connection_selected(self, text):
        # This is now handled by _on_connection_type_changed
        pass

    def _on_npt_size_selected(self, text):
        # This is now handled inside _setup_connection_options
        pass
        
    def _on_flange_option_selected(self, option_type, text):
        # This is now handled inside _setup_connection_options
        pass
        
    def _on_triclamp_selected(self, text):
        # This is now handled inside _setup_connection_options
        pass
        
    def _on_exotic_metal_selected(self, text):
        # This is now handled by the dynamic option handler
        pass
        
    def _apply_edited_product_options(self):
        # This will use the config_service to apply options
        pass

    def _populate_for_edit(self):
        # This will use the config_service to load an existing configuration
        pass

    def get_selected_product_data(self):
        """
        Gathers all selected data from the configuration service.
        """
        if not self.config_service.current_config:
            return {}

        config = self.config_service.current_config
        quantity = self.qty_spin.value()

        return {
            "product_family_id": config.product_family_id,
            "product_family_name": config.product_family_name,
            "base_product": config.base_product,
            "selected_options": config.selected_options,
            "quantity": quantity,
            "total_price": config.final_price * quantity,
            "description": self.config_service.get_final_description(),
        }

    def _setup_connection_options(self, form_layout: QFormLayout, options: list):
        """Set up connection options (Flange, Tri-Clamp, etc.)."""
        if not options:
            return
            
        # Connection type selection
        connection_combo = QComboBox()
        connection_combo.setMinimumWidth(200)
        
        # Add default "None" option
        connection_combo.addItem("None", userData={"type": None, "price": 0})
        
        # Add connection options
        for opt in options:
            display_text = f"{opt['type']}"
            if opt.get('rating'):
                display_text += f" {opt['rating']}"
            display_text += f" {opt['size']}"
            if opt.get('price', 0) > 0:
                display_text += f" (+${opt['price']:.2f})"
            connection_combo.addItem(display_text, userData=opt)
            
        connection_combo.currentIndexChanged.connect(
            lambda idx: self._on_connection_selected(connection_combo.itemData(idx))
        )
        form_layout.addRow("Connection:", connection_combo)
        self.option_widgets["Connection"] = connection_combo 