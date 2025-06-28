import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QStackedWidget, QFrame, QLabel, 
                               QPushButton, QLineEdit, QTextEdit, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QSplitter, 
                               QScrollArea, QGridLayout, QComboBox, QSpinBox,
                               QDialog, QDialogButtonBox, QListWidget, QFormLayout,
                               QGroupBox, QTabWidget, QMessageBox)
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QPainter

class ModernButton(QPushButton):
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_style()
    
    def apply_style(self):
        if self.button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
                QPushButton:pressed {
                    background-color: #1e40af;
                }
            """)
        elif self.button_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f8fafc;
                    color: #475569;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                    border-color: #cbd5e1;
                }
                QPushButton:pressed {
                    background-color: #e2e8f0;
                }
            """)
        elif self.button_type == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #dc2626;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #b91c1c;
                }
                QPushButton:pressed {
                    background-color: #991b1b;
                }
            """)

class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(44)
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #cbd5e1;
            }
        """)

class ModernTextEdit(QTextEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(120)
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: white;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #2563eb;
                outline: none;
            }
            QTextEdit:hover {
                border-color: #cbd5e1;
            }
        """)

class ModernComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(44)
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QComboBox {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #2563eb;
            }
            QComboBox:hover {
                border-color: #cbd5e1;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)

class SidebarWidget(QWidget):
    page_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                color: white;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #0f172a; border-bottom: 1px solid #334155;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        
        logo_label = QLabel("Babbitt")
        logo_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #3b82f6;")
        header_layout.addWidget(logo_label)
        
        layout.addWidget(header)
        
        # Navigation
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(16, 24, 16, 24)
        nav_layout.setSpacing(8)
        
        self.nav_buttons = {}
        nav_items = [
            ("Quote Creator", "quote_creator"),
            ("All Quotes", "quotes"),
            ("Customers", "customers"),
            ("Settings", "settings")
        ]
        
        for text, key in nav_items:
            btn = self.create_nav_button(text, key)
            self.nav_buttons[key] = btn
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        layout.addWidget(nav_widget)
        
        # Set initial active button
        self.set_active_button("quote_creator")
    
    def create_nav_button(self, text, key):
        btn = QPushButton(text)
        btn.setMinimumHeight(48)
        btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.on_nav_clicked(key))
        self.update_nav_button_style(btn, False)
        return btn
    
    def update_nav_button_style(self, btn, active):
        if active:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 16px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #cbd5e1;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 16px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #334155;
                    color: white;
                }
            """)
    
    def on_nav_clicked(self, key):
        self.set_active_button(key)
        self.page_changed.emit(key)
    
    def set_active_button(self, active_key):
        for key, btn in self.nav_buttons.items():
            self.update_nav_button_style(btn, key == active_key)

class QuoteCreatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Quote Creator")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1e293b;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        new_product_btn = ModernButton("+ New Product", "primary")
        new_product_btn.clicked.connect(self.show_product_dialog)
        header_layout.addWidget(new_product_btn)
        
        layout.addLayout(header_layout)
        
        # Main content
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Quote details
        left_widget = self.create_quote_details_widget()
        main_splitter.addWidget(left_widget)
        
        # Right side - Customer info
        right_widget = self.create_customer_widget()
        main_splitter.addWidget(right_widget)
        
        main_splitter.setSizes([2, 1])
        layout.addWidget(main_splitter)
        
    def create_quote_details_widget(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Status and total
        status_layout = QHBoxLayout()
        
        status_label = QLabel("DRAFT")
        status_label.setStyleSheet("""
            QLabel {
                background-color: #fef3c7;
                color: #92400e;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 12px;
            }
        """)
        status_layout.addWidget(status_label)
        
        status_layout.addStretch()
        
        total_label = QLabel("$0.00")
        total_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        total_label.setStyleSheet("color: #059669;")
        status_layout.addWidget(total_label)
        
        layout.addLayout(status_layout)
        
        # Quote items section
        items_label = QLabel("Quote Items")
        items_label.setFont(QFont("Segoe UI", 16, QFont.Weight.SemiBold))
        items_label.setStyleSheet("color: #374151; margin-bottom: 16px;")
        layout.addWidget(items_label)
        
        # Add product button (when no items)
        add_product_widget = QWidget()
        add_product_widget.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border: 2px dashed #cbd5e1;
                border-radius: 12px;
                min-height: 120px;
            }
        """)
        
        add_layout = QVBoxLayout(add_product_widget)
        add_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        add_btn = ModernButton("+ Add Product", "secondary")
        add_btn.clicked.connect(self.show_product_dialog)
        add_layout.addWidget(add_btn)
        
        help_text = QLabel("No items added yet. Click 'Add Product' to get started.")
        help_text.setStyleSheet("color: #6b7280; font-size: 14px;")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_layout.addWidget(help_text)
        
        layout.addWidget(add_product_widget)
        
        # Products table (initially hidden)
        self.products_table = QTableWidget(0, 6)
        self.products_table.setHorizontalHeaderLabels([
            "Product", "Configuration", "Quantity", "Unit Price", "Total", "Actions"
        ])
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f1f5f9;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                padding: 12px;
                font-weight: 600;
                color: #374151;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f1f5f9;
            }
        """)
        self.products_table.hide()
        layout.addWidget(self.products_table)
        
        layout.addStretch()
        
        return widget
    
    def create_customer_widget(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Customer selection
        customer_layout = QHBoxLayout()
        
        select_btn = ModernButton("Select Customer", "secondary")
        customer_layout.addWidget(select_btn)
        
        new_customer_btn = ModernButton("New Customer", "secondary")
        customer_layout.addWidget(new_customer_btn)
        
        layout.addLayout(customer_layout)
        
        # Customer form
        form_layout = QFormLayout()
        form_layout.setSpacing(16)
        
        company_input = ModernLineEdit("Company Name")
        form_layout.addRow("Company Name:", company_input)
        
        contact_input = ModernLineEdit("Contact Person")
        form_layout.addRow("Contact Person:", contact_input)
        
        email_input = ModernLineEdit("Email")
        form_layout.addRow("Email:", email_input)
        
        phone_input = ModernLineEdit("Phone")
        form_layout.addRow("Phone:", phone_input)
        
        notes_input = ModernTextEdit("Notes")
        form_layout.addRow("Notes:", notes_input)
        
        layout.addLayout(form_layout)
        
        # Actions
        actions_label = QLabel("Actions")
        actions_label.setFont(QFont("Segoe UI", 16, QFont.Weight.SemiBold))
        actions_label.setStyleSheet("color: #374151; margin-top: 20px;")
        layout.addWidget(actions_label)
        
        save_btn = ModernButton("Save Draft", "secondary")
        layout.addWidget(save_btn)
        
        export_btn = ModernButton("Export to Word", "secondary")
        layout.addWidget(export_btn)
        
        clear_btn = ModernButton("Clear Quote", "danger")
        layout.addWidget(clear_btn)
        
        layout.addStretch()
        
        return widget
    
    def show_product_dialog(self):
        dialog = ProductSelectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Add product to table
            self.add_product_to_table(dialog.get_selected_product())
    
    def add_product_to_table(self, product_data):
        # Show table and hide add product widget
        self.products_table.show()
        
        row = self.products_table.rowCount()
        self.products_table.insertRow(row)
        
        # Add product data to table
        self.products_table.setItem(row, 0, QTableWidgetItem(product_data.get('name', 'N/A')))
        self.products_table.setItem(row, 1, QTableWidgetItem(product_data.get('config', 'Standard')))
        self.products_table.setItem(row, 2, QTableWidgetItem(str(product_data.get('quantity', 1))))
        self.products_table.setItem(row, 3, QTableWidgetItem(f"${product_data.get('price', 0):.2f}"))
        self.products_table.setItem(row, 4, QTableWidgetItem(f"${product_data.get('total', 0):.2f}"))
        
        # Add action buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(4, 4, 4, 4)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("QPushButton { color: #2563eb; border: none; }")
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("QPushButton { color: #dc2626; border: none; }")
        
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        
        self.products_table.setCellWidget(row, 5, actions_widget)

class ProductSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_product = {}
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Configure Product - Babbitt International")
        self.setModal(True)
        self.resize(900, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header_label = QLabel("Select a Product to Begin")
        header_label.setFont(QFont("Segoe UI", 18, QFont.Weight.SemiBold))
        header_label.setStyleSheet("color: #1e293b;")
        layout.addWidget(header_label)
        
        # Main content
        main_layout = QHBoxLayout()
        
        # Product list
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        search_input = ModernLineEdit("Search products...")
        list_layout.addWidget(search_input)
        
        self.product_list = QListWidget()
        self.product_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f1f5f9;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #f8fafc;
            }
        """)
        
        products = ["LS2000", "LS2100", "LS6000", "LS7000", "LS7000/2", 
                   "LS7500", "LS8000", "LS8000/2", "LS8500", "LT9000", "FS10000"]
        
        for product in products:
            self.product_list.addItem(product)
        
        self.product_list.currentItemChanged.connect(self.on_product_selected)
        list_layout.addWidget(self.product_list)
        
        main_layout.addWidget(list_widget, 1)
        
        # Configuration panel
        self.config_widget = self.create_config_widget()
        main_layout.addWidget(self.config_widget, 2)
        
        layout.addLayout(main_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = ModernButton("Cancel", "secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        add_btn = ModernButton("Add to Quote", "primary")
        add_btn.clicked.connect(self.accept)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
    
    def create_config_widget(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Configuration title
        config_label = QLabel("Configure LS2000")
        config_label.setFont(QFont("Segoe UI", 16, QFont.Weight.SemiBold))
        config_label.setStyleSheet("color: #1e293b;")
        layout.addWidget(config_label)
        
        # Tabs for different configuration sections
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3b82f6;
            }
        """)
        
        # Voltages tab
        voltages_widget = QWidget()
        voltages_layout = QFormLayout(voltages_widget)
        voltages_layout.setSpacing(16)
        
        voltage_combo = ModernComboBox()
        voltage_combo.addItems(["115VAC", "230VAC", "24VDC", "48VDC"])
        voltages_layout.addRow("Voltage:", voltage_combo)
        
        tabs.addTab(voltages_widget, "Voltages")
        
        # Material tab
        material_widget = QWidget()
        material_layout = QFormLayout(material_widget)
        material_layout.setSpacing(16)
        
        insulator_combo = ModernComboBox()
        insulator_combo.addItems(["Standard", "High Temperature", "Chemical Resistant"])
        material_layout.addRow("Insulator Material:", insulator_combo)
        
        material_combo = ModernComboBox()
        material_combo.addItems(["S - 316 Stainless Steel", "H - Hastelloy", "I - Inconel"])
        material_layout.addRow("Material:", material_combo)
        
        tabs.addTab(material_widget, "Material")
        
        # Probe Length tab
        probe_widget = QWidget()
        probe_layout = QFormLayout(probe_widget)
        probe_layout.setSpacing(16)
        
        length_input = ModernLineEdit("Enter probe length")
        probe_layout.addRow("Probe Length:", length_input)
        
        tabs.addTab(probe_widget, "Probe Length")
        
        layout.addWidget(tabs)
        
        # Pricing section
        pricing_widget = QWidget()
        pricing_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        pricing_layout = QHBoxLayout(pricing_widget)
        pricing_layout.setContentsMargins(16, 16, 16, 16)
        
        base_price_label = QLabel("Base Price: $425.00")
        base_price_label.setFont(QFont("Segoe UI", 12))
        pricing_layout.addWidget(base_price_label)
        
        pricing_layout.addStretch()
        
        qty_label = QLabel("Qty:")
        pricing_layout.addWidget(qty_label)
        
        qty_spin = QSpinBox()
        qty_spin.setMinimum(1)
        qty_spin.setValue(1)
        qty_spin.setStyleSheet("""
            QSpinBox {
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 8px;
                min-width: 60px;
            }
        """)
        pricing_layout.addWidget(qty_spin)
        
        pricing_layout.addStretch()
        
        total_label = QLabel("Total: $425.00")
        total_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        total_label.setStyleSheet("color: #059669;")
        pricing_layout.addWidget(total_label)
        
        layout.addWidget(pricing_widget)
        
        return widget
    
    def on_product_selected(self, current, previous):
        if current:
            product_name = current.text()
            # Update configuration widget for selected product
            # This would typically load product-specific configuration options
    
    def get_selected_product(self):
        return {
            'name': 'LS2000',
            'config': 'Standard Configuration',
            'quantity': 1,
            'price': 425.00,
            'total': 425.00
        }

class QuotesListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("All Quotes")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1e293b;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        new_quote_btn = ModernButton("+ New Quote", "primary")
        header_layout.addWidget(new_quote_btn)
        
        layout.addLayout(header_layout)
        
        # Search and filters
        search_layout = QHBoxLayout()
        
        search_input = ModernLineEdit("Search quotes by number, customer name, or company...")
        search_input.setMinimumWidth(400)
        search_layout.addWidget(search_input)
        
        refresh_btn = ModernButton("Refresh", "secondary")
        search_layout.addWidget(refresh_btn)
        
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        # Main content
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Quotes table
        table_widget = self.create_quotes_table()
        main_splitter.addWidget(table_widget)
        
        # Quote details panel
        details_widget = self.create_quote_details_panel()
        main_splitter.addWidget(details_widget)
        
        main_splitter.setSizes([2, 1])
        layout.addWidget(main_splitter)
    
    def create_quotes_table(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        table = QTableWidget(1, 5)
        table.setHorizontalHeaderLabels(["Quote #", "Customer", "Date", "Total", "Status"])
        
        # Add sample data
        table.setItem(0, 0, QTableWidgetItem("Q-1001"))
        table.setItem(0, 1, QTableWidgetItem("James Brickley"))
        table.setItem(0, 2, QTableWidgetItem("2025-06-25"))
        table.setItem(0, 3, QTableWidgetItem("$0.00"))
        
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(8, 4, 8, 4)
        
        status_label = QLabel("draft")
        status_label.setStyleSheet("""
            QLabel {
                background-color: #fef3c7;
                color: #92400e;
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 11px;
            }
        """)
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        
        table.setCellWidget(0, 4, status_widget)
        
        table.horizontalHeader().setStretchLastSection(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #f1f5f9;
                background-color: transparent;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                padding: 16px 12px;
                font-weight: 600;
                color: #374151;
            }
            QTableWidget::item {
                padding: 16px 12px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background-color: #eff6ff;
                color: #1e40af;
            }
        """)
        
        layout.addWidget(table)
        return widget
    
    def create_quote_details_panel(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Quote Details")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.SemiBold))
        title_label.setStyleSheet("color: #1e293b;")
        layout.addWidget(title_label)
        
        # Details
        details_layout = QFormLayout()
        details_layout.setSpacing(12)
        
        quote_num_label = QLabel("Q-1001")
        quote_num_label.setStyleSheet("font-weight: 600; color: #374151;")
        details_layout.addRow("QUOTE #", quote_num_label)
        
        customer_label = QLabel("James Brickley")
        customer_label.setStyleSheet("font-weight: 600; color: #374151;")
        details_layout.addRow("CUSTOMER", customer_label)
        
        date_label = QLabel("2025-06-25")
        date_label.setStyleSheet("font-weight: 600; color: #374151;")
        details_layout.addRow("DATE", date_label)
        
        total_label = QLabel("$0.00")
        total_label.setStyleSheet("font-weight: 600; color: #059669; font-size: 16px;")
        details_layout.addRow("TOTAL", total_label)
        
        status_label = QLabel("draft")
        status_label.setStyleSheet("""
            QLabel {
                background-color: #fef3c7;
                color: #92400e;
                padding: 6px 12px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 12px;
            }
        """)
        details_layout.addRow("STATUS", status_label)
        
        layout.addLayout(details_layout)
        
        layout.addStretch()
        
        # Action buttons
        edit_btn = ModernButton("Edit", "secondary")
        layout.addWidget(edit_btn)
        
        delete_btn = ModernButton("Delete", "danger")
        layout.addWidget(delete_btn)
        
        return widget

class CustomersWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Customers")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1e293b;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        new_customer_btn = ModernButton("+ New Customer", "primary")
        header_layout.addWidget(new_customer_btn)
        
        layout.addLayout(header_layout)
        
        # Placeholder content
        placeholder = QLabel("Customer management interface would go here")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        layout.addWidget(placeholder)

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        title_label = QLabel("Settings")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1e293b;")
        layout.addWidget(title_label)
        
        # Placeholder content
        placeholder = QLabel("Application settings would go here")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        layout.addWidget(placeholder)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("MyBabbittQuote - Babbitt International")
        self.setMinimumSize(1400, 900)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.page_changed.connect(self.change_page)
        layout.addWidget(self.sidebar)
        
        # Main content area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #f8fafc;")
        
        # Add pages
        self.quote_creator = QuoteCreatorWidget()
        self.quotes_list = QuotesListWidget()
        self.customers = CustomersWidget()
        self.settings = SettingsWidget()
        
        self.stacked_widget.addWidget(self.quote_creator)
        self.stacked_widget.addWidget(self.quotes_list)
        self.stacked_widget.addWidget(self.customers)
        self.stacked_widget.addWidget(self.settings)
        
        layout.addWidget(self.stacked_widget)
        
        # Set initial page
        self.stacked_widget.setCurrentWidget(self.quote_creator)
    
    def change_page(self, page_key):
        page_map = {
            "quote_creator": self.quote_creator,
            "quotes": self.quotes_list,
            "customers": self.customers,
            "settings": self.settings
        }
        
        if page_key in page_map:
            self.stacked_widget.setCurrentWidget(page_map[page_key])

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("MyBabbittQuote")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Babbitt International")
    
    # Set modern font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())