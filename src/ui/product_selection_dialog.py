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
        try:
            # Fetch all product families (models)
            family_objs = self.product_service.get_product_families(self.db)
            logger.debug(f"Fetched {len(family_objs)} product families")
            
            # For each family, get the base variant to get pricing info
            products = []
            for fam in family_objs:
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
                    logger.debug(f"Adding product: {product_info}")
                    products.append(product_info)
            
            self.products = products
            logger.debug(f"Total products loaded: {len(self.products)}")
        except Exception as e:
            logger.error(f"Error fetching product families: {e}", exc_info=True)
            self.products = []
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
        self.option_widgets = {}  # Track widgets for each option
        
        # Product details
        details = QLabel(f"<b>{product['name']}</b><br><span style='color:#888;'>{product['description']}</span>")
        details.setWordWrap(True)
        self.config_layout.addWidget(details)
        
        # Add a form layout for the options
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        try:
            # Get available options for this product family
            all_options = self.product_service.get_all_additional_options(self.db)
            logger.debug(f"Found {len(all_options)} additional options")
            
            # Group options by category for dynamic UI generation
            grouped_options = {}
            for opt in all_options:
                if opt.category not in grouped_options:
                    grouped_options[opt.category] = []
                grouped_options[opt.category].append(opt)

            # Voltage options (still handled specially for now)
            voltage_combo = QComboBox()
            voltage_options = self.product_service.get_voltage_options(self.db, product['id'])
            logger.debug(f"Found {len(voltage_options)} voltage options")
            for v_opt in voltage_options:
                voltage_combo.addItem(v_opt['voltage'], userData=v_opt)
            voltage_combo.currentIndexChanged.connect(self._on_voltage_changed)
            form_layout.addRow("Voltage:", voltage_combo)
            self.option_widgets["Voltage"] = voltage_combo
            
            # Material and Probe Length options only for non-presence/absence switches
            if not product['name'] in ["LS7500", "LS8500"]:
                # Material options
                material_combo = QComboBox()
                material_options = self.product_service.get_material_options(self.db, product['id'])
                logger.debug(f"Found {len(material_options)} material options")
                for m_opt in material_options:
                    material_combo.addItem(m_opt['display_name'], userData=m_opt)
                material_combo.currentIndexChanged.connect(self._on_material_changed)
                form_layout.addRow("Material:", material_combo)
                self.option_widgets["Material"] = material_combo
                
                # Probe Length options
                length_widget = QWidget()
                length_layout = QHBoxLayout(length_widget)
                length_layout.setContentsMargins(0, 0, 0, 0)
                
                # Spinner wheel (QSpinBox)
                self.length_spinner = QSpinBox()
                self.length_spinner.setRange(1, 120)  # 1 to 120 inches
                self.length_spinner.setValue(product['base_length'])  # Use base length from product
                self.length_spinner.setSuffix('"')  # Add inch symbol
                self.length_spinner.setFixedWidth(100)
                self.length_spinner.valueChanged.connect(self._on_length_changed)
                
                # Text input (QLineEdit)
                self.length_input = QLineEdit()
                self.length_input.setPlaceholderText("Enter length (inches)")
                self.length_input.setFixedWidth(100)
                self.length_input.setValidator(QIntValidator(1, 120))  # Only allow integers between 1 and 120
                self.length_input.textChanged.connect(self._on_length_text_changed)
                
                length_layout.addWidget(self.length_spinner)
                length_layout.addWidget(self.length_input)
                length_layout.addStretch()
                
                form_layout.addRow("Probe Length:", length_widget)
                self.option_widgets["Probe Length"] = length_widget
            
            # Dynamically build the rest of the options from the database
            self._build_dynamic_options(grouped_options, form_layout)
            
            # Connection options (still handled with specific logic for visibility)
            self._setup_connection_options(form_layout, grouped_options.get("Connection", []))

            # Add the form layout to the main config layout
            self.config_layout.addLayout(form_layout)
            
            # Add some spacing
            self.config_layout.addSpacing(20)
            
            # Quantity
            qty_label = QLabel("<b>Quantity</b>")
            self.config_layout.addWidget(qty_label)
            self.qty_spin = QSpinBox()
            self.qty_spin.setMinimum(1)
            self.qty_spin.setValue(1)
            self.qty_spin.valueChanged.connect(self._on_quantity_changed)
            self.config_layout.addWidget(self.qty_spin)
            
            # Total price
            self.total_price_label = QLabel()
            self.total_price_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 10px;")
            self.config_layout.addWidget(self.total_price_label)
            
            # Add to Quote button
            btn_text = "Update Item" if self.is_edit_mode else "+ Add to Quote"
            self.add_btn = QPushButton(btn_text)
            self.add_btn.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 10px 24px; border-radius: 6px; font-size: 16px;")
            self.add_btn.clicked.connect(self._on_add_to_quote)
            self.config_layout.addWidget(self.add_btn)
            
            # Set initial options directly after creating widgets
            self._on_voltage_changed(self.option_widgets["Voltage"].currentIndex())
            if "Material" in self.option_widgets:
                self._on_material_changed(self.option_widgets["Material"].currentIndex())
            if "Probe Length" in self.option_widgets:
                self._on_length_changed(self.length_spinner.value())

            if self.is_edit_mode:
                self._apply_edited_product_options()
            
            self._update_total_price()
            logger.debug("Product configuration UI setup completed")
        except Exception as e:
            logger.error(f"Error setting up product configuration: {e}", exc_info=True)

    def _build_dynamic_options(self, grouped_options: dict, layout: QFormLayout):
        """Builds UI controls for dynamic options fetched from the database."""
        
        # Define the order of categories
        category_order = ["O-ring Material", "Exotic Metal", "Connection", "additional"]
        
        for category in category_order:
            if category in grouped_options:
                opts = grouped_options[category]
                
                if not opts:
                    continue

                # Skip connection as it's handled separately
                if category == "Connection":
                    continue

                category_label = QLabel(f"<b>{category}</b>")
                layout.addRow(category_label)
                
                # Special handling for "additional" category to be checkboxes
                if category == "additional":
                    for opt in opts:
                        checkbox = QCheckBox(f"{opt.name} - Add ${opt.price:.2f}")
                        checkbox.stateChanged.connect(lambda state, o=opt: self._on_option_selected(o.name, state == Qt.Checked))
                        layout.addRow("", checkbox)
                        self.option_widgets[opt.name] = checkbox
                    continue

                # For other categories, assume a single selection via ComboBox
                combo = QComboBox()
                # Extract all unique choices from the options in this category
                all_choices = []
                for opt in opts:
                    all_choices.extend(opt.choices)
                
                # Add "None" option if not a required field (optional)
                # For now, we add it to all for simplicity
                combo.addItem("None", userData=None)
                
                # Use a set to get unique choices
                for choice in sorted(list(set(all_choices))):
                    # Find the option associated with this choice to get data
                    choice_opt = next((o for o in opts if choice in o.choices), None)
                    if choice_opt:
                        display_text = choice
                        if choice_opt.price > 0:
                            display_text += f" (+${choice_opt.price:.2f})"
                        elif "Consult Factory" in choice_opt.description:
                            display_text += " (Consult Factory)"
                            
                        combo.addItem(display_text, userData=choice_opt)

                combo.currentTextChanged.connect(
                    lambda text, cat=category: self._on_dynamic_option_selected(cat, text)
                )
                layout.addRow(f"{category}:", combo)
                self.option_widgets[category] = combo

    def _setup_connection_options(self, form_layout: QFormLayout, connection_options: list):
        """Sets up the connection option dropdowns and visibility logic."""
        if not connection_options:
            return

        connection_types = sorted(list(set(opt.type for opt in connection_options)))
        if "NPT" in connection_types:
            connection_types.remove("NPT")
            connection_types.insert(0, "NPT")
        
        connection_combo = QComboBox()
        connection_combo.addItems(connection_types)
        connection_combo.currentTextChanged.connect(self._on_connection_type_changed)
        form_layout.addRow("Connection:", connection_combo)
        self.option_widgets["Connection"] = connection_combo
        
        # Containers for different connection types
        self.connection_containers = {}

        # NPT Container
        self.npt_container = QWidget()
        npt_layout = QFormLayout()
        npt_layout.setContentsMargins(0,0,0,0)
        npt_size_combo = QComboBox()
        npt_sizes = sorted(list(set(opt.size for opt in connection_options if opt.type == "NPT")))
        npt_size_combo.addItems(npt_sizes)
        npt_size_combo.currentTextChanged.connect(lambda text: self.config_service.select_option("NPT Size", text))
        npt_layout.addRow("NPT Size:", npt_size_combo)
        self.npt_container.setLayout(npt_layout)
        form_layout.addRow(self.npt_container)
        self.connection_containers["NPT"] = self.npt_container

        # Flange Container
        self.flange_container = QWidget()
        flange_layout = QFormLayout()
        flange_layout.setContentsMargins(0,0,0,0)
        flange_rating_combo = QComboBox()
        flange_ratings = sorted(list(set(opt.rating for opt in connection_options if opt.type == "Flange")))
        flange_rating_combo.addItems(flange_ratings)
        flange_rating_combo.currentTextChanged.connect(lambda text: self.config_service.select_option("Flange Rating", text))
        flange_layout.addRow("Flange Rating:", flange_rating_combo)
        flange_size_combo = QComboBox()
        flange_sizes = sorted(list(set(opt.size for opt in connection_options if opt.type == "Flange")))
        flange_size_combo.addItems(flange_sizes)
        flange_size_combo.currentTextChanged.connect(lambda text: self.config_service.select_option("Flange Size", text))
        flange_layout.addRow("Flange Size:", flange_size_combo)
        self.flange_container.setLayout(flange_layout)
        form_layout.addRow(self.flange_container)
        self.connection_containers["Flange"] = self.flange_container
        
        # Tri-Clamp Container
        self.triclamp_container = QWidget()
        triclamp_layout = QFormLayout()
        triclamp_layout.setContentsMargins(0,0,0,0)
        triclamp_size_combo = QComboBox()
        triclamp_sizes = sorted(list(set(opt.size for opt in connection_options if opt.type == "Tri-Clamp")))
        triclamp_size_combo.addItems(triclamp_sizes)
        triclamp_size_combo.currentTextChanged.connect(lambda text: self.config_service.select_option("Tri-Clamp Size", text))
        triclamp_layout.addRow("Tri-Clamp Size:", triclamp_size_combo)
        self.triclamp_container.setLayout(triclamp_layout)
        form_layout.addRow(self.triclamp_container)
        self.connection_containers["Tri-Clamp"] = self.triclamp_container

        # Set initial visibility
        self._on_connection_type_changed(connection_combo.currentText())

    def _on_connection_type_changed(self, connection_type):
        """Shows and hides the relevant container for the selected connection type."""
        self.config_service.select_option("Connection", connection_type)
        for type, container in self.connection_containers.items():
            container.setVisible(type == connection_type)
        self._update_total_price()

    def _on_dynamic_option_selected(self, category, text):
        """Handles selection from a dynamically generated ComboBox."""
        combo = self.option_widgets.get(category)
        if combo:
            user_data = combo.currentData()
            value = user_data.name if user_data else "None"
            self.config_service.select_option(category, value)
            self._update_total_price()

    def _on_quantity_changed(self, value):
        self.quantity = value
        self._update_total_price()

    def _on_voltage_changed(self, index):
        combo = self.sender()
        option_data = combo.itemData(index)
        self.config_service.select_option("Voltage", option_data['voltage'])
        self._update_total_price()

    def _on_material_changed(self, index):
        combo = self.sender()
        option_data = combo.itemData(index)
        self.config_service.select_option("Material", option_data['material_code'])
        self._update_total_price()

    def _on_material_selected(self, text):
        # This function seems to be intended for a different type of control
        # The logic is now handled by _on_material_changed
        pass

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
        # Clear previous configuration widgets
        for i in reversed(range(self.config_layout.count())): 
            widget = self.config_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout = self.config_layout.itemAt(i).layout()
                if layout is not None:
                    # This is a bit more complex, for now we just clear widgets
                    # A better way is to have a dedicated container widget to clear
                    pass
        
        # A more robust way to clear the layout
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                # If we have nested layouts, we might need to clear them recursively
                # For this dialog, it's probably okay for now.
                pass

    def _update_total_price(self):
        """
        Recalculates the total price by calling the configuration service
        and updates the UI label.
        """
        if not self.config_service.current_config:
            self.total_price_label.setText("Total Price: $0.00")
            return
            
        # The service is now responsible for calculation
        final_price = self.config_service.calculate_price()
        quantity = self.qty_spin.value()
        
        self.total_price_label.setText(f"Total Price: ${final_price * quantity:.2f}")

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