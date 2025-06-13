"""
Product Selection Dialog for Adding Products to Quote.

This dialog provides a two-panel interface:
- Left: Product search and selection
- Right: Product configuration and add-to-quote
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QSpinBox,
    QWidget,
    QScrollArea,
    QComboBox,
    QFormLayout,
    QMessageBox,
    QSlider,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from src.core.database import SessionLocal
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
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

        title = "Edit Product" if self.is_edit_mode else "Add Product to Quote"
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
        logger.info("Starting to fetch product families...")
        try:
            family_objs = self.product_service.get_product_families(self.db)
            products = []
            for fam in family_objs:
                variants = self.product_service.get_variants_for_family(
                    self.db, fam["id"]
                )
                if variants:
                    variant = variants[0]
                    product_info = {
                        "id": fam["id"],
                        "name": fam["name"],
                        "description": fam.get("description", ""),
                        "category": fam.get("category", ""),
                        "base_price": variant["base_price"],
                        "base_length": variant["base_length"],
                        "voltage": variant["voltage"],
                        "material": variant["material"],
                    }
                    products.append(product_info)
            self.products = products
        except Exception as e:
            logger.error(
                f"A critical error occurred while fetching product families: {e}",
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
        self.search_bar.setPlaceholderText("Search products...")
        self.search_bar.textChanged.connect(self._filter_products)
        left_layout.addWidget(self.search_bar)
        self.product_list = QListWidget()
        self.product_list.setSpacing(8)
        self.product_list.itemSelectionChanged.connect(self._on_product_selected)
        left_layout.addWidget(self.product_list, 1)
        main_layout.addWidget(left_panel)

        self.right_panel = QFrame()
        right_layout = QVBoxLayout(self.right_panel)
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
        filtered_products = [
            p for p in self.products if filter_text.lower() in p["name"].lower()
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
            self._show_select_product()
            return

        product_data = items[0].data(Qt.UserRole)
        self.config_service.start_configuration(
            product_family_id=product_data["id"],
            product_family_name=product_data["name"],
            base_product_info=product_data,
        )
        self.quantity = 1
        self._show_product_config(product_data)

    def _show_select_product(self):
        self._clear_config_panel()
        prompt = QLabel("<b>Select a Product</b><br>Choose a product to configure.")
        prompt.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(prompt)

    def _show_product_config(self, product):
        """Show the configuration options for the selected product."""
        self._clear_config_panel()
        self.option_widgets = {}

        details = QLabel(f"<b>{product['name']}</b><br>{product['description']}")
        details.setWordWrap(True)
        self.config_layout.addWidget(details)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self._setup_core_options(form_layout, product)

        # Get all connection-related options for the product family
        connection_options = self.product_service.get_connection_options(
            self.db, product["id"]
        )
        self._setup_connection_options(form_layout, connection_options)

        self.config_layout.addLayout(form_layout)
        self._setup_quantity_and_total()
        self._setup_add_button()
        self._update_total_price()

    def _setup_core_options(self, form_layout: QFormLayout, product: dict):
        # Voltage
        self.voltage_combo = QComboBox()
        voltages = self.product_service.get_voltage_options(self.db)
        for v in voltages:
            self.voltage_combo.addItem(v["voltage"], v)
        self.voltage_combo.currentIndexChanged.connect(self._on_voltage_changed)
        form_layout.addRow("Voltage:", self.voltage_combo)

        # Material
        self.material_combo = QComboBox()
        materials = self.product_service.get_material_options(self.db)
        for m in materials:
            self.material_combo.addItem(m["name"], m)
        self.material_combo.currentIndexChanged.connect(self._on_material_changed)
        form_layout.addRow("Material:", self.material_combo)

        # Length
        length_layout = QHBoxLayout()
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setRange(6, 120)
        self.length_slider.valueChanged.connect(self._on_length_changed)
        length_layout.addWidget(self.length_slider)
        self.length_input = QLineEdit()
        self.length_input.setValidator(QIntValidator(6, 120))
        self.length_input.setFixedWidth(50)
        self.length_input.textChanged.connect(self._on_length_text_changed)
        length_layout.addWidget(self.length_input)
        form_layout.addRow("Length (in):", length_layout)

        # Set initial values
        base_length = float(product.get("base_length", 10.0))
        self.length_slider.setValue(int(base_length))
        self.length_input.setText(str(int(base_length)))

    def _setup_quantity_and_total(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Quantity:"))
        self.quantity_spinner = QSpinBox()
        self.quantity_spinner.setRange(1, 999)
        self.quantity_spinner.setValue(self.quantity)
        self.quantity_spinner.valueChanged.connect(self._on_quantity_changed)
        h_layout.addWidget(self.quantity_spinner)
        h_layout.addStretch()
        self.total_price_label = QLabel("$0.00")
        self.total_price_label.setObjectName("totalPriceLabel")
        h_layout.addWidget(self.total_price_label)
        self.config_layout.addLayout(h_layout)

    def _setup_add_button(self):
        self.add_button = QPushButton("Add to Quote")
        self.add_button.clicked.connect(self._on_add_to_quote)
        self.config_layout.addWidget(self.add_button)

    def _update_total_price(self):
        if self.config_service.current_config:
            total = self.config_service.current_config.final_price * self.quantity
            self.total_price_label.setText(f"${total:,.2f}")

    def _on_quantity_changed(self, value):
        self.quantity = value
        self._update_total_price()

    def _on_voltage_changed(self, index):
        if index == -1:
            return
        # Using currentData which was set from the dictionary
        selected_voltage = self.voltage_combo.currentData()["voltage"]
        self.config_service.select_option("Voltage", selected_voltage)
        self._update_total_price()

    def _on_material_changed(self, index):
        if index == -1:
            return
        # Using currentData which was set from the dictionary
        selected_material = self.material_combo.currentData()["material_code"]
        self.config_service.select_option("Material", selected_material)
        self._update_total_price()

    def _update_length(self, value: float):
        """Unified method to update length from any source."""
        # Block signals to prevent an infinite loop between slider and text box
        self.length_input.blockSignals(True)
        self.length_slider.blockSignals(True)

        self.length_input.setText(str(int(value)))
        self.length_slider.setValue(int(value))

        self.length_input.blockSignals(False)
        self.length_slider.blockSignals(False)

        logger.debug(f"Length updated to: {value}")
        self.config_service.select_option("Length", value)
        self._update_total_price()

    def _on_length_changed(self, value):
        """Handle QSlider value change."""
        self._update_length(float(value))

    def _on_length_text_changed(self, text):
        """Handle QLineEdit text change."""
        try:
            if text:
                self._update_length(float(text))
        except ValueError:
            logger.warning(f"Invalid length input: {text}")
            # Optionally revert to a valid number or show an error
            pass

    def _setup_connection_options(self, form_layout: QFormLayout, options: list):
        """Creates UI controls for connection options."""
        logger.debug(f"Setting up connection options. Received {len(options)} options.")
        if not options:
            return

        # Create the main connection type dropdown
        self.connection_type_combo = QComboBox()
        self.connection_type_combo.addItem("None", None)  # Add a 'None' option

        # Add connection types from the options
        connection_types = sorted(set(opt["type"] for opt in options))
        for conn_type in connection_types:
            # Find the first option with this type to get its price
            price = next(
                (opt["price"] for opt in options if opt["type"] == conn_type), 0
            )
            display_text = f"{conn_type} (+${price:.2f})" if price > 0 else conn_type
            self.connection_type_combo.addItem(display_text, conn_type)

        form_layout.addRow("Connection Type:", self.connection_type_combo)
        self.option_widgets["Connection Type"] = self.connection_type_combo

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
            "Connection Type", selected_type if selected_type != "None" else None
        )
        self._update_total_price()

        if selected_type == "None":
            return

        # Create a new form layout for the sub-options
        sub_form_layout = QFormLayout()

        # Filter options for the selected connection type
        type_options = [opt for opt in all_options if opt["type"] == selected_type]

        # Add rating options if available
        ratings = sorted(set(opt["rating"] for opt in type_options if opt["rating"]))
        if ratings:
            rating_combo = QComboBox()
            for rating in ratings:
                price = next(
                    (opt["price"] for opt in type_options if opt["rating"] == rating), 0
                )
                display_text = f"{rating} (+${price:.2f})" if price > 0 else rating
                rating_combo.addItem(display_text, rating)
            sub_form_layout.addRow("Rating:", rating_combo)
            self.option_widgets["Rating"] = rating_combo
            rating_combo.currentTextChanged.connect(
                lambda text: self._on_sub_option_changed("Rating", text)
            )

        # Add size options if available
        sizes = sorted(set(opt["size"] for opt in type_options if opt["size"]))
        if sizes:
            size_combo = QComboBox()
            for size in sizes:
                price = next(
                    (opt["price"] for opt in type_options if opt["size"] == size), 0
                )
                display_text = f"{size} (+${price:.2f})" if price > 0 else size
                size_combo.addItem(display_text, size)
            sub_form_layout.addRow("Size:", size_combo)
            self.option_widgets["Size"] = size_combo
            size_combo.currentTextChanged.connect(
                lambda text: self._on_sub_option_changed("Size", text)
            )

        # Add the sub-form to the main sub-options layout
        self.connection_sub_options_layout.addLayout(sub_form_layout)

        # Initialize the first values
        if ratings:
            self._on_sub_option_changed(
                "Rating", self.option_widgets["Rating"].currentText()
            )
        if sizes:
            self._on_sub_option_changed(
                "Size", self.option_widgets["Size"].currentText()
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
        while self.config_layout.count():
            child = self.config_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                # This doesn't recursively clear layouts, but for this dialog it's okay
                pass

    def _on_add_to_quote(self):
        # Validation logic will be moved to ConfigurationService
        if not self.config_service.current_config:
            QMessageBox.warning(self, "Warning", "Please select a product.")
            return

        final_config = self.config_service.current_config
        product_data = {
            "product_family_id": final_config.product_family_id,
            "product_family_name": final_config.product_family_name,
            "quantity": self.quantity,
            "unit_price": final_config.final_price,
            "description": self.config_service.get_final_description(),
            "options": final_config.selected_options,
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
