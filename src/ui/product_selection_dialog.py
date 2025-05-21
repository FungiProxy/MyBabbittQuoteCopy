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

class ProductSelectionDialog(QDialog):
    """
    Modal dialog for selecting and configuring a product to add to a quote.
    Emits product_added(product_data) when a product is configured and added.
    """
    product_added = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product to Quote")
        self.resize(900, 600)
        self.selected_product = None
        self.selected_options = {}
        self.quantity = 1
        self._init_mock_data()
        self._init_ui()

    def _init_mock_data(self):
        """Initialize mock product data (replace with DB integration later)."""
        self.products = [
            {
                "id": 1,
                "name": "LS-1000 Level Switch",
                "description": "Standard level switch for liquid level detection",
                "category": "Level Switches",
                "base_price": 450,
                "options": [
                    {"name": "Voltage", "required": True, "choices": [
                        {"label": "110V AC", "price": 0},
                        {"label": "220V AC", "price": 50},
                        {"label": "24V DC", "price": 0},
                    ]},
                    {"name": "Material", "required": True, "choices": [
                        {"label": "Stainless Steel 316", "price": 100},
                        {"label": "Brass", "price": 75},
                        {"label": "PVC", "price": 25},
                    ]},
                    {"name": "Probe Length", "required": True, "choices": [
                        {"label": '6" (Standard)', "price": 0},
                        {"label": '12"', "price": 30},
                        {"label": '18"', "price": 60},
                    ]},
                ]
            },
            {
                "id": 2,
                "name": "LS-2000 Level Switch",
                "description": "Advanced level switch with digital display",
                "category": "Level Switches",
                "base_price": 650,
                "options": []
            },
            {
                "id": 3,
                "name": "FS-500 Flow Switch",
                "description": "Basic flow switch for industrial applications",
                "category": "Flow Switches",
                "base_price": 550,
                "options": []
            },
            {
                "id": 4,
                "name": "FS-750 Flow Switch",
                "description": "High-precision flow switch with temperature",
                "category": "Flow Switches",
                "base_price": 750,
                "options": []
            },
        ]

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
        for product in self.products:
            if filter_text.lower() in product["name"].lower() or filter_text.lower() in product["description"].lower():
                item = QListWidgetItem()
                item.setText(f"{product['name']}\n{product['description']}\n{product['category']}   ${product['base_price']}")
                item.setData(Qt.UserRole, product)
                self.product_list.addItem(item)

    def _filter_products(self, text):
        self._populate_product_list(text)

    def _on_product_selected(self):
        items = self.product_list.selectedItems()
        if not items:
            self._show_select_product()
            return
        product = items[0].data(Qt.UserRole)
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
        self._clear_config_panel()
        # Product details
        details = QLabel(f"<b>{product['name']}</b><br><span style='color:#888;'>{product['description']}</span><br><span style='background:#e3e8f7; color:#2563eb; border-radius:4px; padding:2px 8px; font-size:12px;'>{product['category']}</span>  <b>Base Price: ${product['base_price']}</b>")
        details.setWordWrap(True)
        self.config_layout.addWidget(details)
        # Dynamic options
        self.option_groups = {}
        for option in product.get("options", []):
            group_label = QLabel(f"<b>{option['name']} {'*' if option['required'] else ''}</b>")
            self.config_layout.addWidget(group_label)
            btn_group = QButtonGroup(self)
            btn_group.setExclusive(True)
            self.option_groups[option["name"]] = btn_group
            for choice in option["choices"]:
                radio = QRadioButton(f"{choice['label']} {'(+${})'.format(choice['price']) if choice['price'] else ''}")
                radio.toggled.connect(self._update_total_price)
                btn_group.addButton(radio)
                self.config_layout.addWidget(radio)
            # Select first by default
            if btn_group.buttons():
                btn_group.buttons()[0].setChecked(True)
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
        for opt_name, btn_group in self.option_groups.items():
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
        for opt_name, btn_group in self.option_groups.items():
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