"""
Redesigned Product Selection Component

Modern card-based product selection with step-by-step workflow, family filtering,
and clean industrial design. Integrates with existing product service and database.
"""

import logging
from typing import Dict, List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.config.base_models import BASE_MODELS
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService

logger = logging.getLogger(__name__)


class ProductSelectionDialog(QDialog):
    """
    Redesigned product selection dialog with modern card-based interface.

    Features:
    - Step indicator showing selection progress
    - Family-based filtering in left panel
    - Product cards with pricing in main area
    - Clean, professional styling
    """

    product_selected = Signal(dict)  # Emitted when product is chosen for configuration

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Product')
        self.setModal(True)
        self.resize(1000, 700)

        # Services
        self.db = SessionLocal()
        self.product_service = ProductService()

        # State
        self.selected_family = None
        self.product_families = self._get_product_families()

        self._setup_ui()
        self._load_default_family()

    def __del__(self):
        """Clean up database connection."""
        if hasattr(self, 'db') and self.db:
            self.db.close()

    def _setup_ui(self):
        """Set up the dialog UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Progress indicator
        self.progress_widget = self._create_progress_indicator()
        main_layout.addWidget(self.progress_widget)

        # Main content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left panel - Product families
        self.families_panel = self._create_families_panel()
        content_layout.addWidget(self.families_panel)

        # Right panel - Product grid
        self.products_panel = self._create_products_panel()
        content_layout.addWidget(self.products_panel)

        main_layout.addWidget(content_widget)

    def _create_progress_indicator(self) -> QWidget:
        """Create the step progress indicator."""
        widget = QFrame()
        widget.setObjectName('progressIndicator')

        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        steps = [
            ('1', 'Select', True),    # Current step
            ('2', 'Configure', False),
            ('3', 'Quote', False)
        ]

        for i, (number, label, active) in enumerate(steps):
            if i > 0:
                line = QFrame()
                line.setObjectName('progressLine')
                layout.addWidget(line)

            step_widget = QWidget()
            step_layout = QVBoxLayout(step_widget)
            step_layout.setAlignment(Qt.AlignCenter)
            step_layout.setSpacing(5)

            circle = QLabel(number)
            circle.setFixedSize(30, 30)
            circle.setAlignment(Qt.AlignCenter)
            circle.setProperty('class', 'stepNumber')
            circle.setProperty('active', active)

            step_label = QLabel(label)
            step_label.setProperty('class', 'stepLabel')

            step_layout.addWidget(circle)
            step_layout.addWidget(step_label)
            layout.addWidget(step_widget)

        return widget

    def _create_families_panel(self) -> QFrame:
        """Create the product families panel."""
        panel = QFrame()
        panel.setFixedWidth(280)
        panel.setObjectName('familiesPanel')

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel('Product Families')
        title.setObjectName('sectionTitle')
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        families_widget = QWidget()
        self.families_layout = QVBoxLayout(families_widget)
        self.families_layout.setSpacing(5)

        self._populate_families()

        scroll.setWidget(families_widget)
        layout.addWidget(scroll)

        return panel

    def _create_products_panel(self) -> QFrame:
        """Create the products grid panel."""
        panel = QFrame()
        panel.setObjectName('productsPanel')

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)

        self.products_scroll = QScrollArea()
        self.products_scroll.setWidgetResizable(True)
        self.products_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.products_widget = QWidget()
        self.products_layout = QGridLayout(self.products_widget)
        self.products_layout.setSpacing(20)
        self.products_layout.setAlignment(Qt.AlignTop)

        self.products_scroll.setWidget(self.products_widget)
        layout.addWidget(self.products_scroll)

        return panel

    def _get_product_families(self) -> List[Dict]:
        """Get product families organized by category."""
        families = []

        # Group families by category
        categories = {
            'Level Switches': ['LS2000', 'LS2100', 'LS6000', 'LS7000', 'LS7000/2', 'LS8000', 'LS8000/2'],
            'Level Transmitters': ['LT9000'],
            'Flow Switches': ['FS10000'],
            'Presence/Absence': ['LS7500', 'LS8500']
        }

        for category, family_names in categories.items():
            category_data = {
                'name': category,
                'families': []
            }

            for family_name in family_names:
                if family_name in BASE_MODELS:
                    base_model = BASE_MODELS[family_name]
                    family_data = {
                        'name': family_name,
                        'description': base_model['description'],
                        'category': category
                    }
                    category_data['families'].append(family_data)

            if category_data['families']:
                families.append(category_data)

        return families

    def _populate_families(self):
        """Populate the families panel with family cards."""
        for category in self.product_families:
            category_header = QLabel(category['name'])
            category_header.setObjectName('categoryHeader')
            self.families_layout.addWidget(category_header)

            for family in category['families']:
                family_card = self._create_family_card(family)
                self.families_layout.addWidget(family_card)

        self.families_layout.addStretch()

    def _create_family_card(self, family: Dict) -> QFrame:
        """Create a family selection card."""
        card = QFrame()
        card.setProperty('family_name', family['name'])
        card.setProperty('class', 'familyCard')

        layout = QVBoxLayout(card)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        name_label = QLabel(family['name'])
        name_label.setProperty('class', 'familyName')
        layout.addWidget(name_label)

        desc = family['description'].replace(' - Base Configuration', '')
        if len(desc) > 40:
            desc = desc[:37] + '...'

        desc_label = QLabel(desc)
        desc_label.setProperty('class', 'familyDescription')
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        card.mousePressEvent = lambda event, f=family: self._select_family(f)

        return card

    def _select_family(self, family: Dict):
        """Handle family selection."""
        self.selected_family = family
        self._update_family_selection()
        self._load_products_for_family(family['name'])

    def _update_family_selection(self):
        """Update visual selection state of family cards."""
        for i in range(self.families_layout.count()):
            item = self.families_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if hasattr(widget, 'property') and widget.property('family_name'):
                    is_selected = widget.property('family_name') == self.selected_family['name']
                    widget.setProperty('selected', is_selected)
                    # Force a style re-polish to apply the [selected="true"] selector
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)

    def _load_products_for_family(self, family_name: str):
        """Load products for the selected family."""
        # Clear existing products
        for i in reversed(range(self.products_layout.count())):
            item = self.products_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        # For now, create a single product card per family based on BASE_MODELS
        if family_name in BASE_MODELS:
            base_model = BASE_MODELS[family_name]
            product_data = {
                'family_name': family_name,
                'name': family_name,
                'description': base_model['description'].replace(' - Base Configuration', ''),
                'base_price': base_model['base_price'],
                'model_number': base_model['model_number']
            }

            product_card = self._create_product_card(product_data)
            self.products_layout.addWidget(product_card, 0, 0)

    def _create_product_card(self, product: Dict) -> QFrame:
        """Create a product card."""
        card = QFrame()
        card.setProperty('class', 'productCard')

        layout = QVBoxLayout(card)
        layout.setSpacing(10)

        name_label = QLabel(product['name'])
        name_label.setProperty('class', 'productName')
        layout.addWidget(name_label)

        desc_label = QLabel(product['description'])
        desc_label.setWordWrap(True)
        desc_label.setProperty('class', 'productDescription')
        layout.addWidget(desc_label)

        price_label = QLabel(f"Starting at ${product['base_price']:,.2f}")
        price_label.setProperty('class', 'productPrice')
        layout.addWidget(price_label)

        configure_btn = QPushButton('Configure')
        configure_btn.setProperty('class', 'primary')
        configure_btn.clicked.connect(lambda: self._configure_product(product))
        layout.addWidget(configure_btn)

        return card

    def _configure_product(self, product: Dict):
        """Handle product configuration selection."""
        self.product_selected.emit(product)
        self.accept()

    def _load_default_family(self):
        """Load the first family by default."""
        if self.product_families:
            first_category = self.product_families[0]
            if first_category['families']:
                first_family = first_category['families'][0]
                self._select_family(first_family)


class ProductCard(QFrame):
    """
    Reusable product card component for grid displays.
    """

    product_selected = Signal(dict)

    def __init__(self, product_data: Dict, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self._setup_ui()

    def _setup_ui(self):
        """Set up the product card UI."""
        self.setProperty('class', 'productCard')
        self.setFixedSize(280, 200)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Product name
        name = QLabel(self.product_data.get('name', 'Unknown Product'))
        name.setProperty('class', 'productName')
        layout.addWidget(name)

        # Description
        desc = QLabel(self.product_data.get('description', ''))
        desc.setProperty('class', 'productDescription')
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Price
        price = QLabel(f"Starting at ${self.product_data.get('base_price', 0):,.2f}")
        price.setProperty('class', 'productPrice')
        layout.addWidget(price)

        # Spacer
        layout.addStretch()

        # Configure button
        btn = QPushButton('Configure')
        btn.setProperty('class', 'primary')
        btn.clicked.connect(self._on_configure)
        layout.addWidget(btn)

    def _on_configure(self):
        """Handle configure button click."""
        self.product_selected.emit(self.product_data)
