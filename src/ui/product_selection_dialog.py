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
from src.core.services.product_service import ProductService
from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily

class ProductSelectionDialog(QDialog):
    """
    Modal dialog for selecting and configuring a product to add to a quote.
    Emits product_added(product_data) when a product is configured and added.
    """
    product_added = Signal(dict)

    def __init__(self, product_service: ProductService, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product to Quote")
        self.resize(900, 600)
        self.selected_product = None
        self.selected_options = {}
        self.quantity = 1
        self.product_service = product_service
        self.products = []
        self._fetch_products()
        self._init_ui()

    def _fetch_products(self):
        """Fetch product families from the database using ProductService, and ensure required fields."""
        db = SessionLocal()
        try:
            # Fetch all product families (models)
            family_objs = self.product_service.get_product_families(db)
            # For each family, try to get a representative base_price from the first variant
            products = []
            for fam in family_objs:
                # Try to get the first variant for this family to get a base_price
                variant = None
                try:
                    variants = self.product_service.get_variants_for_family(db, fam['id'])
                    if variants:
                        variant = variants[0]
                except Exception:
                    pass
                base_price = variant['base_price'] if variant and 'base_price' in variant else 0
                products.append({
                    "id": fam["id"],
                    "name": fam["name"],
                    "description": fam.get("description", ""),
                    "category": fam.get("category", ""),
                    "base_price": base_price
                })
            self.products = products
        except Exception as e:
            self.products = []
            print(f"Error fetching product families: {e}")
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
        self._show_select_product()

    def _populate_product_list(self, filter_text=""):
        """Populate the product list, optionally filtering by search text."""
        self.product_list.clear()
        filtered_products = [product for product in self.products if filter_text.lower() in product["name"].lower()]
        for product in filtered_products:
            item = QListWidgetItem()
            item.setText(f"{product['name']}")
            item.setData(Qt.UserRole, product)
            self.product_list.addItem(item)

    def _filter_products(self, text):
        self._populate_product_list(text)

    def _on_product_selected(self):
        items = self.product_list.selectedItems()
        print(f"DEBUG: _on_product_selected called. Items: {items}")
        if not items:
            print("DEBUG: No items selected. Showing select product prompt.")
            self._show_select_product()
            return
        product = items[0].data(Qt.UserRole)
        print(f"DEBUG: Product selected: {product}")
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
        self._clear_config_panel()
        self.selected_options = {}
        self.option_widgets = {}  # Track widgets for each option
        
        # Product details
        details = QLabel(f"<b>{product['name']}</b><br><span style='color:#888;'>{product['description']}</span>")
        details.setWordWrap(True)
        self.config_layout.addWidget(details)
        
        # Add a form layout for the options
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Voltage options
        voltage_combo = QComboBox()
        voltage_combo.addItems(["24VDC", "115VAC"])
        voltage_combo.currentTextChanged.connect(lambda text: self._on_option_selected("Voltage", text))
        form_layout.addRow("Voltage:", voltage_combo)
        self.option_widgets["Voltage"] = voltage_combo
        
        # Material options
        material_combo = QComboBox()
        material_combo.addItems([
            "S - 316 Stainless Steel Probe",
            "H - Halar Coated Probe",
            "TS - Teflon Sleeve",
            "U - UHMWPE Blind End Probe",
            "T - Teflon Blind End Probe"
        ])
        material_combo.currentTextChanged.connect(lambda text: self._on_material_selected(text))
        form_layout.addRow("Material:", material_combo)
        self.option_widgets["Material"] = material_combo
        
        # Exotic Metals options
        exotic_combo = QComboBox()
        exotic_combo.addItems([
            "None",
            "T - Titanium",
            "U - Monel",
            "A - Alloy 20",
            "H - Hastelloy-C-276",
            "B - Hastelloy-B"
        ])
        exotic_combo.currentTextChanged.connect(lambda text: self._on_exotic_metal_selected(text))
        form_layout.addRow("Exotic Metal:", exotic_combo)
        self.option_widgets["Exotic Metal"] = exotic_combo
        
        # Probe Length options
        length_combo = QComboBox()
        # Default to S/H: 10" to 72"
        lengths = [f"{i}\"" for i in range(10, 73)]
        length_combo.addItems(lengths)
        length_combo.setCurrentText("10\"")
        length_combo.currentTextChanged.connect(lambda text: self._on_probe_length_selected(text))
        form_layout.addRow("Probe Length:", length_combo)
        self.option_widgets["Probe Length"] = length_combo
        
        # Connection options
        connection_combo = QComboBox()
        connection_combo.addItems(["Standard", "Flanged", "Tri-Clamp"])
        connection_combo.currentTextChanged.connect(lambda text: self._on_connection_selected(text))
        form_layout.addRow("Connection:", connection_combo)
        self.option_widgets["Connection"] = connection_combo
        
        # Create containers for connection options
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
        flange_size_combo.addItems(['1"', '1.5"', '2"', '3"', '4"'])
        flange_size_combo.currentTextChanged.connect(lambda text: self._on_flange_option_selected("size", text))
        flange_layout.addRow("Flange Size:", flange_size_combo)
        self.option_widgets["Flange Size"] = flange_size_combo
        
        self.flange_container.setLayout(flange_layout)
        form_layout.addRow(self.flange_container)
        self.flange_container.hide()
        
        self.triclamp_container = QWidget()
        triclamp_layout = QFormLayout()
        triclamp_layout.setContentsMargins(0, 0, 0, 0)
        triclamp_layout.setSpacing(15)
        
        triclamp_size_combo = QComboBox()
        triclamp_size_combo.addItems(['1.5"', '2"'])
        triclamp_size_combo.currentTextChanged.connect(lambda text: self._on_triclamp_selected(text))
        triclamp_layout.addRow("Tri-Clamp Size:", triclamp_size_combo)
        self.option_widgets["Tri-Clamp Size"] = triclamp_size_combo
        
        self.triclamp_container.setLayout(triclamp_layout)
        form_layout.addRow(self.triclamp_container)
        self.triclamp_container.hide()
        
        # Additional Options
        teflon_check = QCheckBox("Teflon Insulator (Instead of UHMWPE) - Add $40.00")
        teflon_check.stateChanged.connect(lambda state: self._on_option_selected("Teflon Insulator", state == Qt.Checked))
        form_layout.addRow("", teflon_check)
        self.option_widgets["Teflon Insulator"] = teflon_check
        
        static_check = QCheckBox("Extra Static Protection - Add $30.00")
        static_check.stateChanged.connect(lambda state: self._on_option_selected("Extra Static Protection", state == Qt.Checked))
        form_layout.addRow("", static_check)
        self.option_widgets["Extra Static Protection"] = static_check
        
        cable_check = QCheckBox("Cable Probe - Add $80.00")
        cable_check.stateChanged.connect(lambda state: self._on_option_selected("Cable Probe", state == Qt.Checked))
        form_layout.addRow("", cable_check)
        self.option_widgets["Cable Probe"] = cable_check
        
        bent_check = QCheckBox("Bent Probe - Add $50.00")
        bent_check.stateChanged.connect(lambda state: self._on_option_selected("Bent Probe", state == Qt.Checked))
        form_layout.addRow("", bent_check)
        self.option_widgets["Bent Probe"] = bent_check
        
        tag_check = QCheckBox("Stainless Steel Tag - Add $30.00")
        tag_check.stateChanged.connect(lambda state: self._on_option_selected("Stainless Steel Tag", state == Qt.Checked))
        form_layout.addRow("", tag_check)
        self.option_widgets["Stainless Steel Tag"] = tag_check
        
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
        self.add_btn = QPushButton("+ Add to Quote")
        self.add_btn.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 10px 24px; border-radius: 6px; font-size: 16px;")
        self.add_btn.clicked.connect(self._on_add_to_quote)
        self.config_layout.addWidget(self.add_btn)
        
        self._update_total_price()

    def _on_material_selected(self, text):
        """Handle material selection and validate probe length."""
        material_code = text.split(" - ")[0]
        length_combo = self.option_widgets["Probe Length"]
        current_length = length_combo.currentText()
        if material_code in ["U", "T"]:
            # 4" to 72" for U/T
            length_combo.clear()
            lengths = [f"{i}\"" for i in range(4, 73)]
            length_combo.addItems(lengths)
            if current_length in lengths:
                length_combo.setCurrentText(current_length)
            else:
                length_combo.setCurrentText("4\"")
        else:
            # 10" to 72" for S/H
            length_combo.clear()
            lengths = [f"{i}\"" for i in range(10, 73)]
            length_combo.addItems(lengths)
            if current_length in lengths:
                length_combo.setCurrentText(current_length)
            else:
                length_combo.setCurrentText("10\"")
        if material_code == "H" and length_combo.currentText() == "72\"":
            QMessageBox.warning(self, "Warning", "Maximum probe length with Halar coating is 72\". For longer probes, please use Teflon Sleeve.")
        self._update_total_price()

    def _on_probe_length_selected(self, text):
        """Handle probe length selection and validate against material."""
        material = self.option_widgets["Material"].currentText()
        if material == "Halar" and text == "72\"":
            QMessageBox.warning(self, "Warning", "Maximum probe length with Halar coating is 72\". For longer probes, please use Teflon Sleeve.")
        self._on_option_selected("Probe Length", text)

    def _on_option_selected(self, option_name, value):
        """Handle option selection and update pricing."""
        self.selected_options[option_name] = value
        self._update_total_price()

    def _clear_config_panel(self):
        # Remove all widgets from config_layout
        while self.config_layout.count():
            item = self.config_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _update_total_price(self):
        """Calculate and display the total price based on selected options."""
        # Start with base price for LS2000
        total = 425.00  # Base price for LS2000
        
        # Add option prices
        for opt_name, widget in self.option_widgets.items():
            if isinstance(widget, QComboBox):
                selected = widget.currentText()
                if opt_name == "Material":
                    if selected == "Halar":
                        total += 110  # Halar coating adder
                elif opt_name == "Probe Length":
                    # Calculate length adder
                    length = int(selected.split("\"")[0])
                    if length > 10:
                        if self.option_widgets["Material"].currentText() == "316SS":
                            total += (length - 10) * 45  # $45/foot for 316SS
                        elif self.option_widgets["Material"].currentText() == "Halar":
                            total += (length - 10) * 110  # $110/foot for Halar
            elif isinstance(widget, QCheckBox):
                if widget.isChecked():
                    if opt_name == "Teflon Insulator":
                        total += 40
                    elif opt_name == "Extra Static Protection":
                        total += 30
                    elif opt_name == "Cable Probe":
                        total += 80
                    elif opt_name == "Bent Probe":
                        total += 50
                    elif opt_name == "Stainless Steel Tag":
                        total += 30
        
        # Apply quantity
        qty = self.qty_spin.value() if hasattr(self, 'qty_spin') else 1
        total_price = total * qty
        
        # Update display
        self.total_price_label.setText(f"Total: ${total_price:.2f}")

    def _on_add_to_quote(self):
        """Handle adding the configured product to the quote."""
        if not self.selected_product:
            return
            
        # Validate configuration
        if not self._validate_configuration():
            return
            
        # Prepare product data
        product_data = {
            "product_id": self.selected_product["id"],
            "name": self.selected_product["name"],
            "quantity": self.qty_spin.value(),
            "base_price": getattr(self, 'base_price', 425.00),
            "options": self.selected_options,
            "total_price": float(self.total_price_label.text().split("$")[1])
        }
        
        # Emit signal with product data
        self.product_added.emit(product_data)
        self.accept()

    def _validate_configuration(self):
        """Validate the current configuration."""
        # Check voltage
        voltage = self.option_widgets["Voltage"].currentText()
        if voltage not in ["24VDC", "115VAC"]:
            QMessageBox.warning(self, "Invalid Configuration", "Only 24VDC and 115VAC are available for LS2000.")
            return False
            
        # Check probe length with Halar
        material = self.option_widgets["Material"].currentText()
        length = self.option_widgets["Probe Length"].currentText()
        if material == "Halar" and length == "72\"":
            QMessageBox.warning(self, "Invalid Configuration", "Maximum probe length with Halar coating is 72\". Please use Teflon Sleeve for longer probes.")
            return False
            
        return True 

    def _on_connection_selected(self, text):
        """Handle connection type selection and show/hide relevant options."""
        # Hide all connection-specific containers first
        self.flange_container.hide()
        self.triclamp_container.hide()
        
        # Show relevant options based on selection
        if text == "Flanged":
            self.flange_container.show()
            QMessageBox.information(self, "Flange Connection", 
                "Please consult factory for flange connection pricing.")
        elif text == "Tri-Clamp":
            self.triclamp_container.show()
        
        self._on_option_selected("Connection", text)
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
        if text == "T - Titanium":
            self.selected_options["Exotic Metal Price"] = 280.00
        elif text == "U - Monel":
            self.selected_options["Exotic Metal Price"] = 330.00
        elif text in ["A - Alloy 20", "H - Hastelloy-C-276", "B - Hastelloy-B"]:
            QMessageBox.information(self, "Exotic Metal", "Please consult factory for pricing.")
            self.selected_options["Exotic Metal Price"] = 0.00
        else:
            self.selected_options["Exotic Metal Price"] = 0.00
        self._update_total_price() 