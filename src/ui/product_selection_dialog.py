"""
Product Selection Dialog for Adding Products to Quote.

This dialog provides a two-panel interface:
- Left: Product search and selection
- Right: Product configuration and add-to-quote

Follows UI/UX overhaul and screenshot design. Uses mock data for now.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QFrame, QButtonGroup, QRadioButton, QSpinBox, QSizePolicy, QWidget, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from src.core.services.product_service import ProductService
from src.core.database import SessionLocal

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
        """Fetch product families (models) from the database using ProductService."""
        db = SessionLocal()
        try:
            # Fetch all product families (models)
            family_objs = self.product_service.get_product_families(db)
            # Each family is a dict with keys: id, name, description, category
            self.products = family_objs
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
        print(f"DEBUG: _show_product_config called with product: {product}")
        self._clear_config_panel()
        self.selected_options = {}
        self.option_widgets = {}  # Track widgets for each option
        self.family_id = product["id"]
        # Product details
        details = QLabel(f"<b>{product['name']}</b><br><span style='color:#888;'>{product['description']}</span><br><span style='background:#e3e8f7; color:#2563eb; border-radius:4px; padding:2px 8px; font-size:12px;'>{product['category']}</span>  <b>Base Price: ${product['base_price']}</b>")
        details.setWordWrap(True)
        self.config_layout.addWidget(details)
        # Fetch and show dynamic options
        self._build_dynamic_options()
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

    def _build_dynamic_options(self):
        """
        Build option widgets dynamically based on current selected options and valid choices.
        """
        db = SessionLocal()
        try:
            valid_options = self.product_service.get_valid_options_for_selection(db, self.family_id, self.selected_options)
            print(f"DEBUG: valid_options for family_id={self.family_id}, selected_options={self.selected_options}: {valid_options}")
        except Exception as e:
            print(f"Error fetching valid options: {e}")
            valid_options = {}
        finally:
            db.close()
        # Remove old option widgets
        for widget in getattr(self, 'option_widgets', {}).values():
            widget.deleteLater()
        self.option_widgets = {}
        # For each option, create a group of radio buttons for valid values
        for opt_name, values in valid_options.items():
            group_label = QLabel(f"<b>{opt_name.capitalize()}</b>")
            self.config_layout.addWidget(group_label)
            btn_group = QButtonGroup(self)
            btn_group.setExclusive(True)
            self.option_widgets[opt_name] = btn_group
            for val in values:
                radio = QRadioButton(str(val))
                # Set checked if this value is selected
                if self.selected_options.get(opt_name) == val:
                    radio.setChecked(True)
                radio.toggled.connect(lambda checked, o=opt_name, v=val: self._on_option_selected(o, v, checked))
                btn_group.addButton(radio)
                self.config_layout.addWidget(radio)
            # If nothing selected, select the first by default
            if btn_group.buttons() and opt_name not in self.selected_options:
                btn_group.buttons()[0].setChecked(True)

    def _on_option_selected(self, option_name, value, checked):
        if checked:
            self.selected_options[option_name] = value
            # Rebuild options to reflect new valid choices
            self._rebuild_options_panel()
            self._update_total_price()

    def _rebuild_options_panel(self):
        # Remove all option widgets (but not details, qty, price, add button)
        # We'll keep the first widget (details label), then remove until qty_label
        count = self.config_layout.count()
        # Find the index of the qty_label
        qty_label_idx = None
        for i in range(count):
            widget = self.config_layout.itemAt(i).widget()
            if isinstance(widget, QSpinBox):
                qty_label_idx = i - 1  # The label is just before the spinbox
                break
        # Remove widgets between details and qty_label
        if qty_label_idx is not None:
            for i in range(qty_label_idx, 0, -1):
                widget = self.config_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
        # Rebuild dynamic options
        self._build_dynamic_options()

    def _clear_config_panel(self):
        # Remove all widgets from config_layout
        while self.config_layout.count():
            item = self.config_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _update_total_price(self):
        # Calculate total price based on selected options and quantity
        if not self.selected_product:
            self.total_price_label.setText("")
            return
        base = self.selected_product["base_price"]
        total = base
        # Add option prices
        for opt_name, btn_group in self.option_widgets.items():
            for btn in btn_group.buttons():
                if btn.isChecked():
                    label = btn.text()
                    # Extract price from label
                    if '(+$' in label:
                        price_str = label.split('(+$', 1)[1].split(')', 1)[0]
                        try:
                            total += int(price_str)
                        except Exception:
                            pass
        qty = self.qty_spin.value() if hasattr(self, 'qty_spin') else 1
        total_price = total * qty
        self.total_price_label.setText(f"Total Price<br><span style='font-size:28px;'>${total_price:.2f}</span>")

    def _on_add_to_quote(self):
        # Gather selected options
        options = {}
        for opt_name, btn_group in self.option_widgets.items():
            for btn in btn_group.buttons():
                if btn.isChecked():
                    options[opt_name] = btn.text()
        qty = self.qty_spin.value() if hasattr(self, 'qty_spin') else 1
        product_data = {
            "product": self.selected_product,
            "options": options,
            "quantity": qty,
            "total_price": self.total_price_label.text()
        }
        self.product_added.emit(product_data)
        self.accept() 