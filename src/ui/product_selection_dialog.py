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
        self.selected_product = None
        self.selected_options = {}
        self.quantity = 1
        self.product_service = product_service
        self.products = []
        self._fetch_products()
        self._init_ui()
        
        if self.is_edit_mode:
            self._populate_for_edit()

    def _fetch_products(self):
        """Fetch product families from the database using ProductService."""
        db = SessionLocal()
        try:
            # Fetch all product families (models)
            family_objs = self.product_service.get_product_families(db)
            logger.debug(f"Fetched {len(family_objs)} product families")
            
            # For each family, get the base variant to get pricing info
            products = []
            for fam in family_objs:
                variants = self.product_service.get_variants_for_family(db, fam['id'])
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
        finally:
            db.close()

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
            
        product = items[0].data(Qt.UserRole)
        logger.debug(f"Selected product: {product}")
        self.selected_product = product
        self.selected_options = {}
        self.quantity = 1
        self._show_product_config(product)

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
        self.selected_options = {}
        self.option_widgets = {}  # Track widgets for each option
        
        # Product details
        details = QLabel(f"<b>{product['name']}</b><br><span style='color:#888;'>{product['description']}</span>")
        details.setWordWrap(True)
        self.config_layout.addWidget(details)
        
        # Add a form layout for the options
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        db = SessionLocal()
        try:
            # Get available options for this product family
            options = self.product_service.get_all_additional_options(db)
            logger.debug(f"Found {len(options)} additional options")
            
            # Voltage options
            voltage_combo = QComboBox()
            voltage_options = self.product_service.get_voltage_options(db, product['id'])
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
                material_options = self.product_service.get_material_options(db, product['id'])
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
            
            # O-ring Material options
            oring_combo = QComboBox()
            oring_combo.addItems([
                "Viton",
                "Silicon",
                "Buna-N",
                "EPDM",
                "PTFE",
                "Kalrez (+$295.00)"
            ])
            oring_combo.currentTextChanged.connect(lambda text: self._on_option_selected("O-ring Material", text))
            form_layout.addRow("O-ring Material:", oring_combo)
            self.option_widgets["O-ring Material"] = oring_combo
            
            # Exotic Metals options
            exotic_combo = QComboBox()
            exotic_combo.addItems([
                "None",
                "A - Alloy 20 (Consult Factory)",
                "H - Hastelloy-C-276 (Consult Factory)",
                "B - Hastelloy-B (Consult Factory)",
                "T - Titanium (Consult Factory)"
            ])
            exotic_combo.currentTextChanged.connect(lambda text: self._on_exotic_metal_selected(text))
            form_layout.addRow("Exotic Metal:", exotic_combo)
            self.option_widgets["Exotic Metal"] = exotic_combo
            
            # Connection options
            connection_options = self.product_service.get_connection_options(db, product['id'])
            connection_types = sorted(set(opt['type'] for opt in connection_options))
            # Ensure NPT is first in the list
            if "NPT" in connection_types:
                connection_types.remove("NPT")
                connection_types.insert(0, "NPT")
            connection_combo = QComboBox()
            connection_combo.addItems(connection_types)
            connection_combo.currentTextChanged.connect(lambda text: self._on_connection_selected(text))
            form_layout.addRow("Connection:", connection_combo)
            self.option_widgets["Connection"] = connection_combo
            
            # Create containers for connection options
            self.npt_container = QWidget()
            npt_layout = QFormLayout()
            npt_layout.setContentsMargins(0, 0, 0, 0)
            npt_layout.setSpacing(15)
            
            npt_size_combo = QComboBox()
            npt_sizes = sorted(set(opt['size'] for opt in connection_options if opt['type'] == "NPT"))
            npt_size_combo.addItems(npt_sizes)
            npt_size_combo.currentTextChanged.connect(lambda text: self._on_npt_size_selected(text))
            npt_layout.addRow("NPT Size:", npt_size_combo)
            self.option_widgets["NPT Size"] = npt_size_combo
            
            self.npt_container.setLayout(npt_layout)
            form_layout.addRow(self.npt_container)
            
            self.flange_container = QWidget()
            flange_layout = QFormLayout()
            flange_layout.setContentsMargins(0, 0, 0, 0)
            flange_layout.setSpacing(15)
            
            flange_rating_combo = QComboBox()
            flange_rating_combo.addItems(["150#", "300#"])
            flange_rating_combo.currentTextChanged.connect(lambda text: self._on_flange_option_selected("rating", text))
            flange_layout.addRow("Flange Rating:", flange_rating_combo)
            self.option_widgets["Flange Rating"] = flange_rating_combo
            
            flange_size_combo = QComboBox()
            flange_sizes = sorted(set(opt['size'] for opt in connection_options if opt['type'] == "Flange"))
            flange_size_combo.addItems(flange_sizes)
            flange_size_combo.currentTextChanged.connect(lambda text: self._on_flange_option_selected("size", text))
            flange_layout.addRow("Flange Size:", flange_size_combo)
            self.option_widgets["Flange Size"] = flange_size_combo
            
            self.flange_container.setLayout(flange_layout)
            form_layout.addRow(self.flange_container)
            
            self.triclamp_container = QWidget()
            triclamp_layout = QFormLayout()
            triclamp_layout.setContentsMargins(0, 0, 0, 0)
            triclamp_layout.setSpacing(15)
            
            triclamp_size_combo = QComboBox()
            triclamp_sizes = sorted(set(opt['size'] for opt in connection_options if opt['type'] == "Tri-Clamp"))
            triclamp_size_combo.addItems(triclamp_sizes)
            triclamp_size_combo.currentTextChanged.connect(lambda text: self._on_triclamp_selected(text))
            triclamp_layout.addRow("Tri-Clamp Size:", triclamp_size_combo)
            self.option_widgets["Tri-Clamp Size"] = triclamp_size_combo
            
            self.triclamp_container.setLayout(triclamp_layout)
            form_layout.addRow(self.triclamp_container)
            
            # Set initial visibility based on default connection type
            self.npt_container.show()
            self.flange_container.hide()
            self.triclamp_container.hide()
            
            # Add additional options from database
            for option in options:
                if option.category == "additional":
                    checkbox = QCheckBox(f"{option.name} - Add ${option.price:.2f}")
                    checkbox.stateChanged.connect(lambda state, opt=option: self._on_option_selected(opt.name, state == Qt.Checked))
                    form_layout.addRow("", checkbox)
                    self.option_widgets[option.name] = checkbox
            
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
            self.qty_spin.valueChanged.connect(self._update_total_price)
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
        finally:
            db.close()

    def _on_voltage_changed(self, index):
        """Handle voltage selection."""
        combo_box = self.option_widgets["Voltage"]
        voltage_text = combo_box.itemText(index)
        voltage_code = voltage_text.replace(" ", "")  # "120 VAC" -> "120VAC"
        self._on_option_selected("Voltage", voltage_text, code=voltage_code)

    def _on_material_changed(self, index):
        """Handle material selection."""
        combo_box = self.option_widgets["Material"]
        selected_data = combo_box.itemData(index)
        self._on_material_selected(combo_box.itemText(index))
        self._on_option_selected(
            "Material", 
            selected_data['display_name'],
            price=selected_data.get('base_price', 0),
            code=selected_data.get('material_code')
        )

    def _on_material_selected(self, text):
        """Handle material selection and validate probe length."""
        material_code = text.split(" - ")[0]
        length_widget = self.option_widgets["Probe Length"]
        current_length = self.length_spinner.value()
        
        # Clear current options
        self.length_spinner.clear()
        self.length_input.clear()
        
        if material_code in ["U", "T"]:
            # 4" to 72" for U/T
            self.length_spinner.setRange(4, 72)
            self.length_spinner.setValue(current_length)
            self.length_input.setPlaceholderText("Enter length (inches)")
        elif material_code == "H":
            # All lengths from 4" to 72" for H
            self.length_spinner.setRange(4, 72)
            self.length_spinner.setValue(current_length)
            self.length_input.setPlaceholderText("Enter length (inches)")
        else:
            # 10" to 72" for S/TS
            self.length_spinner.setRange(10, 72)
            self.length_spinner.setValue(current_length)
            self.length_input.setPlaceholderText("Enter length (inches)")
        
        self._update_total_price()

    def _on_length_changed(self, value):
        """Handle changes from the spinner wheel."""
        self.length_input.setText(str(value))
        self._on_option_selected("Probe Length", value)
        self._validate_probe_length()

    def _on_length_text_changed(self, text):
        """Handle changes from the text input."""
        if text:
            try:
                value = int(text)
                self.length_spinner.setValue(value)
                self._on_option_selected("Probe Length", value)
                self._validate_probe_length()
            except ValueError:
                pass

    def _validate_probe_length(self):
        """Validate probe length based on material and show warnings if needed."""
        material = self.selected_options.get("Material", "")
        length = self.length_spinner.value()
        
        # Check for Halar coating length restrictions
        if "H - Halar Coated Probe" in material and length > 72:
            QMessageBox.warning(
                self,
                "Length Warning",
                "Probes over 72 inches with Halar coating require a $300 adder.\n"
                "Consider using a Teflon Sleeve to avoid this charge."
            )
        elif "H - Halar Coated Probe" in material and length < 10:
            QMessageBox.warning(
                self,
                "Length Warning",
                "Minimum length for Halar coated probes is 10 inches."
            )
        
        # Check for U/T material length restrictions
        elif any(x in material for x in ["U - UHMWPE Blind End Probe", "T - Teflon Blind End Probe"]):
            if length < 4:
                QMessageBox.warning(
                    self,
                    "Length Warning",
                    "Minimum length for U/T material probes is 4 inches."
                )

    def _on_option_selected(self, option_name, value, price=0, code=None):
        """Handle option selection and update pricing."""
        if value:
            self.selected_options[option_name] = {"selected": value, "price": price, "name": option_name, "code": code}
        elif option_name in self.selected_options:
            del self.selected_options[option_name]
        self._update_total_price()

    def _clear_config_panel(self):
        """Clear all widgets and layout items from the config panel."""
        # First clear all widgets
        while self.config_layout.count():
            item = self.config_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Clear nested layouts
                while item.layout().count():
                    nested_item = item.layout().takeAt(0)
                    if nested_item.widget():
                        nested_item.widget().deleteLater()
                # Delete the layout itself
                QWidget().setLayout(item.layout())
        
        # Reset the option widgets dictionary
        self.option_widgets = {}

    def _update_total_price(self):
        """Calculate and display the total price based on selected options."""
        if not self.selected_product:
            return

        base_price = self.selected_product.get("base_price", 0)
        options_price = 0.0

        for option in self.selected_options.values():
            options_price += option.get("price", 0)

        total_price = (base_price + options_price) * self.qty_spin.value()
            
        # Update display
        self.total_price_label.setText(f"Total: ${total_price:,.2f}")

    def _on_add_to_quote(self):
        """Handle adding the configured product to the quote."""
        if not self.selected_product:
            return
            
        # Validate configuration
        if not self._validate_configuration():
            return
            
        # Prepare product data
        self.selected_product = self.get_selected_product_data()
        
        # Emit signal with product data - not needed for edit, but keep for 'add'
        if not self.is_edit_mode:
            self.product_added.emit(self.selected_product)

        self.accept()

    def _validate_configuration(self):
        """Ensure all required configurations are selected."""
        if not self.selected_product:
            return False

        db = SessionLocal()
        try:
            # Get the base variant for validation
            variants = self.product_service.get_variants_for_family(db, self.selected_product["id"])
            if not variants:
                return False

            # Check voltage
            voltage = self.option_widgets["Voltage"].currentText()
            voltage_options = self.product_service.get_voltage_options(db, self.selected_product["id"])
            if voltage not in [v['voltage'] for v in voltage_options]:
                QMessageBox.warning(self, "Invalid Configuration", f"Invalid voltage option: {voltage}")
                return False
                
            # Check probe length with Halar
            material = self.option_widgets["Material"].currentText()
            length = self.length_spinner.value()
            if "Halar" in material and length > 72:
                QMessageBox.warning(self, "Invalid Configuration", "Maximum probe length with Halar coating is 72\". Please use Teflon Sleeve for longer probes.")
                return False
                
            return True
        finally:
            db.close()

    def _on_connection_selected(self, text):
        """Handle connection type selection and show/hide relevant options."""
        # Hide all connection-specific containers first
        self.npt_container.hide()
        self.flange_container.hide()
        self.triclamp_container.hide()
        
        # Show relevant options based on selection
        if text == "NPT":
            self.npt_container.show()
        elif text == "Flange":
            self.flange_container.show()
            QMessageBox.information(self, "Flange Connection", 
                "Please consult factory for flange connection pricing.")
        elif text == "Tri-Clamp":
            self.triclamp_container.show()
        
        self._on_option_selected("Connection", text)
        self._update_total_price()

    def _on_npt_size_selected(self, text):
        """Handle NPT size selection and update pricing."""
        self.selected_options["NPT Size"] = text
        self._update_total_price()

    def _on_flange_option_selected(self, option_type, text):
        """Handle flange rating or size selection."""
        if option_type == "rating":
            self.selected_options["Flange Rating"] = text
        else:  # size
            self.selected_options["Flange Size"] = text
        self._update_total_price()

    def _on_triclamp_selected(self, text):
        """Handle tri-clamp size selection and update pricing."""
        self.selected_options["Tri-Clamp Size"] = text
        if text == '1.5"':
            self.selected_options["Tri-Clamp Price"] = 280.00
        elif text == '2"':
            self.selected_options["Tri-Clamp Price"] = 330.00
        self._update_total_price()

    def _on_exotic_metal_selected(self, text):
        """Handle exotic metal selection and update pricing."""
        if text != "None":
            QMessageBox.information(self, "Exotic Metal", "Please consult factory for pricing.")
            self.selected_options["Exotic Metal Price"] = 0.00
        else:
            self.selected_options["Exotic Metal Price"] = 0.00
        self._update_total_price()

    def _apply_edited_product_options(self):
        """If in edit mode, apply the existing options to the UI widgets."""
        if not self.is_edit_mode:
            return

        # Set quantity
        self.qty_spin.setValue(self.product_to_edit.get("quantity", 1))

        # Set selected options
        for option in self.product_to_edit.get("options", []):
            option_name = option.get("name")
            selected_value = option.get("selected")
            
            if option_name in self.option_widgets:
                widget = self.option_widgets[option_name]
                if isinstance(widget, QComboBox):
                    widget.setCurrentText(selected_value)
                # Add logic for other widget types (QCheckBox, etc.) if needed

    def _populate_for_edit(self):
        """Populate the dialog with the product to be edited."""
        if not self.is_edit_mode:
            return

        product_id = self.product_to_edit.get("product_id")
        
        # Find the product in the list
        for i in range(self.product_list.count()):
            item = self.product_list.item(i)
            product_data = item.data(Qt.UserRole)
            if product_data and product_data.get("id") == product_id:
                self.product_list.setCurrentItem(item)
                # _on_product_selected will be called automatically
                break

    def get_selected_product_data(self):
        """Returns the configured product data."""
        if not self.selected_product:
            return None

        # Build final product data
        total_price = float(self.total_price_label.text().split("$")[1]) if hasattr(self, 'total_price_label') and self.total_price_label.text() else 0.0
        
        # Generate part number
        family = self.selected_product.get("name", "UNK")
        
        voltage_opt = self.selected_options.get("Voltage", {})
        voltage_code = voltage_opt.get("code", "UNK")

        part_number_components = [family, voltage_code]

        if not self.selected_product['name'] in ["LS7500", "LS8500"]:
            material_opt = self.selected_options.get("Material", {})
            material_code = material_opt.get("code", "UNK")
            part_number_components.append(material_code)
            
            probe_length = self.length_spinner.value() if hasattr(self, 'length_spinner') else 0
            part_number_components.append(f'{probe_length}"')
        
        part_number = "-".join(part_number_components)
        
        product_data = {
            "part_number": part_number,
            "product_id": self.selected_product["id"],
            "name": self.selected_product["name"],
            "quantity": self.qty_spin.value() if hasattr(self, 'qty_spin') else 1,
            "base_price": self.selected_product["base_price"],
            "options": list(self.selected_options.values()),
            "total_price": total_price
        }

        # Preserve the unique item ID if editing
        if self.is_edit_mode and 'id' in self.product_to_edit:
            product_data['id'] = self.product_to_edit['id']
            
        return product_data 