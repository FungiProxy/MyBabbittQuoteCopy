"""
Redesigned Product Selection Component

Modern card-based product selection with step-by-step workflow, family filtering,
and clean industrial design. Integrates with existing product service and database.
"""

from array import array
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
    QComboBox,
    QStackedWidget,
    QGroupBox,
    QRadioButton,
    QSpinBox,
    QButtonGroup,
    QFormLayout,
)

from src.core.config.base_models import BASE_MODELS
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from src.core.pricing import PricingContext
from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
from src.ui.theme.theme_manager import ThemeManager
from src.ui.utils.ui_integration import QuickMigrationHelper, ModernWidgetFactory

logger = logging.getLogger(__name__)


class ProductSelectionDialog(QDialog):
    """
    Redesigned product selection dialog with modern card-based interface.

    Features:
    - Step indicator showing selection progress
    - Family-based filtering in left panel
    - Product cards with pricing in main area
    - Clean, professional styling
    - Modern UI with improved styling
    """

    product_selected = Signal(dict)  # Emitted when product is chosen for configuration

    def __init__(self, parent=None, theme_name=None):
        super().__init__(parent)
        self.setWindowTitle('Select Product')
        self.setModal(True)
        self.resize(1000, 700)

        # Apply theme if provided or get from parent
        if theme_name:
            self.current_theme = theme_name
        elif parent:
            # Try to get theme from parent window
            try:
                if hasattr(parent, 'settings_service'):
                    self.current_theme = parent.settings_service.get_theme('Modern Babbitt')
                else:
                    self.current_theme = 'Modern Babbitt'
            except:
                self.current_theme = 'Modern Babbitt'
        else:
            self.current_theme = 'Modern Babbitt'
        
        # Apply the theme to this dialog
        ThemeManager.apply_theme_to_widget(self.current_theme, self)

        # Services
        self.db = SessionLocal()
        self.product_service = ProductService()
        self.config_service = ConfigurationService(self.db, self.product_service)

        # State
        self.selected_family = None
        self.product_families = self._get_product_families()
        self.selected_product = None
        self.current_config = {}
        self.available_options = {}

        # Lists to hold the updatable widgets of the progress indicator
        self.step_circles = []
        self.step_labels = []

        self._setup_ui()
        self._load_default_family()
        
        # Apply modern styling fixes
        QuickMigrationHelper.fix_oversized_dropdowns(self)
        QuickMigrationHelper.modernize_existing_dialog(self)

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
        self._update_progress_indicator(1)

        # Stacked widget for switching between selection and configuration
        self.main_stack = QStackedWidget()
        main_layout.addWidget(self.main_stack)

        # Main content area (Page 1: Product Selection)
        selection_widget = QWidget()
        content_layout = QHBoxLayout(selection_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Left panel - Product families
        self.families_panel = self._create_families_panel()
        content_layout.addWidget(self.families_panel)

        # Right panel - Product grid
        self.products_panel = self._create_products_panel()
        content_layout.addWidget(self.products_panel)

        self.main_stack.addWidget(selection_widget)

    def _update_progress_indicator(self, current_step: int):
        # 1-based step number
        steps_config = [
            {'number': '1', 'label': 'Select'},
            {'number': '2', 'label': 'Configure'},
            {'number': '3', 'label': 'Quote'}
        ]

        for i, config in enumerate(steps_config):
            is_active = (i + 1) == current_step
            self.step_circles[i].setProperty('active', is_active)
            self.step_labels[i].setProperty('active', is_active)

            # Re-polish to apply style changes
            self.step_circles[i].style().unpolish(self.step_circles[i])
            self.step_circles[i].style().polish(self.step_circles[i])
            self.step_labels[i].style().unpolish(self.step_labels[i])
            self.step_labels[i].style().polish(self.step_labels[i])
            
    def _create_progress_indicator(self) -> QWidget:
        """Creates a static, perfectly symmetrical progress indicator."""
        widget = QFrame()
        widget.setObjectName('progressIndicator')
        widget.setFixedHeight(80)

        # A QGridLayout is the correct tool for this. It allows us to create
        # three columns of equal width, guaranteeing perfect symmetry.
        main_layout = QGridLayout(widget)
        main_layout.setContentsMargins(20, 0, 20, 0)
        main_layout.setSpacing(0)

        steps_data = [
            ('1', 'Select'),
            ('2', 'Configure'),
            ('3', 'Quote')
        ]

        for i, (number, label_text) in enumerate(steps_data):
            # This container holds the circle and label vertically.
            step_container = QWidget()
            step_layout = QVBoxLayout(step_container)
            step_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_layout.setContentsMargins(0, 0, 0, 0)
            step_layout.setSpacing(8)

            circle = QLabel(number)
            circle.setFixedSize(30, 30)
            circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            circle.setProperty('class', 'stepNumber')
            
            label = QLabel(label_text)
            label.setProperty('class', 'stepLabel')
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            step_layout.addWidget(circle)
            step_layout.addWidget(label)

            # Add the container for this step to the grid, centered.
            main_layout.addWidget(step_container, 0, i, Qt.AlignmentFlag.AlignCenter)
            
            # Store references for later updates
            self.step_circles.append(circle)
            self.step_labels.append(label)

        # Set the columns to have equal stretch factor. This is the key
        # to making them all the same width.
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)
        main_layout.setColumnStretch(2, 1)

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
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        families_widget = QWidget()
        self.families_layout = QVBoxLayout(families_widget)
        self.families_layout.setSpacing(5)

        self._populate_families()

        scroll.setWidget(families_widget)
        layout.addWidget(scroll)

        return panel

    def _create_products_panel(self) -> QFrame:
        """Create the panel to display the selected product's details."""
        panel = QFrame()
        panel.setObjectName('productsPanel')

        # Use a QVBoxLayout to align the card to the top
        panel_layout = QVBoxLayout(panel)
        panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        panel_layout.setContentsMargins(20, 20, 20, 20)

        # The white card that contains the product info
        content_card = QFrame()
        content_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E4E7;
                border-radius: 12px;
            }
        """)
        content_card.setFixedSize(600, 260)

        card_layout = QVBoxLayout(content_card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(10)

        # Widgets that will be updated
        self.product_name_label = QLabel("Select a Product Family")
        self.product_name_label.setProperty('class', 'productName')
        self.product_name_label.setStyleSheet("border: none; background-color: transparent;")

        self.product_desc_label = QLabel("Details will appear here.")
        self.product_desc_label.setProperty('class', 'productDescription')
        self.product_desc_label.setStyleSheet("border: none; background-color: transparent;")

        self.product_price_label = QLabel()
        self.product_price_label.setProperty('class', 'productPrice')
        self.product_price_label.setStyleSheet("border: none; background-color: transparent;")

        self.configure_button = QPushButton('Configure')
        self.configure_button.setProperty('class', 'primary')
        self.configure_button.setFixedHeight(45)

        card_layout.addWidget(self.product_name_label)
        card_layout.addWidget(self.product_desc_label)
        card_layout.addStretch()
        card_layout.addWidget(self.product_price_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.configure_button)

        # Wrapper layout for horizontal centering
        h_wrapper = QHBoxLayout()
        h_wrapper.addStretch()
        h_wrapper.addWidget(content_card)
        h_wrapper.addStretch()
        
        panel_layout.addLayout(h_wrapper)
        panel_layout.addStretch() # Pushes everything up

        # Hide it initially, we'll show it when a product is selected
        content_card.hide()
        self.product_display_card = content_card

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
        """Load product details for the selected family into the display panel."""
        if family_name in BASE_MODELS:
            base_model = BASE_MODELS[family_name]
            product_data = {
                'family_name': family_name,
                'name': family_name,
                'description': base_model['description'].replace(' - Base Configuration', ''),
                'base_price': base_model['base_price'],
                'model_number': base_model['model_number']
            }
            
            # Update the labels
            self.product_name_label.setText(product_data['name'])
            self.product_desc_label.setText(product_data['description'])
            self.product_price_label.setText(f"Starting at ${product_data['base_price']:,.2f}")
            
            # Disconnect any old connection and connect the new one
            try:
                self.configure_button.clicked.disconnect()
            except RuntimeError:
                pass # No connections to disconnect
            self.configure_button.clicked.connect(lambda: self._configure_product(product_data))
            
            # Show the card
            self.product_display_card.show()
        else:
            # Hide the card if no product is found
            self.product_display_card.hide()

    def _configure_product(self, product: Dict):
        """Switches to configuration view instead of emitting signal."""
        self._show_configuration_page(product)

    def _show_configuration_page(self, product: Dict):
        """Switches to the configuration page for the selected product."""
        self.selected_product = product
        
        # Create configuration page
        config_page = QWidget()
        config_layout = QHBoxLayout(config_page)
        config_layout.setContentsMargins(0,0,0,0)
        config_layout.setSpacing(0)

        config_panel = self._create_config_panel()
        summary_panel = self._create_summary_panel()

        config_layout.addWidget(config_panel, 2) # Takes 2/3 of the space
        config_layout.addWidget(summary_panel, 1) # Takes 1/3 of the space

        # Add the new page to the stack and switch to it
        if self.main_stack.count() > 1:
            # remove old config page if it exists
            old_config_page = self.main_stack.widget(1)
            self.main_stack.removeWidget(old_config_page)
            old_config_page.deleteLater()
            
        self.main_stack.addWidget(config_page)
        self.main_stack.setCurrentIndex(1)
        self._update_progress_indicator(2)
        
        self._load_options_for_product()

    def _show_selection_page(self):
        """Switches back to the product selection page."""
        self.main_stack.setCurrentIndex(0)
        self._update_progress_indicator(1)

    def _add_to_quote(self):
        """Finalizes the configuration and emits the signal."""
        # This would gather the configuration data
        configured_product = self.selected_product 
        # configured_product['options'] = self.gather_options() # Example
        
        self.product_selected.emit(configured_product)
        self.accept()

    def _load_default_family(self):
        """Load the first product family by default."""
        if self.product_families and self.product_families[0]['families']:
            first_family = self.product_families[0]['families'][0]
            self._select_family(first_family)

    def _create_config_panel(self) -> QFrame:
        """Creates the main panel for displaying configuration options."""
        panel = QFrame()
        panel.setObjectName("configPanel")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        # Using a QFormLayout for a clean label-widget structure
        self.config_layout = QFormLayout(container)
        self.config_layout.setSpacing(20)
        self.config_layout.setLabelAlignment(Qt.AlignmentFlag.AlignTop)
        self.config_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(panel)
        main_layout.addWidget(scroll)

        return panel

    def _create_summary_panel(self) -> QFrame:
        """Creates the right-side summary panel."""
        panel = QFrame()
        panel.setObjectName("summaryPanel")
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        title = QLabel("Quote Summary")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Summary content (placeholders for now)
        self.summary_content_label = QLabel("Select options to see summary.")
        self.summary_content_label.setWordWrap(True)
        layout.addWidget(self.summary_content_label)
        
        layout.addStretch()

        # Total price
        total_layout = QHBoxLayout()
        total_label = QLabel("Total:")
        self.total_price_label = QLabel("$0.00")
        self.total_price_label.setObjectName("quoteTotalLabel")
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_price_label)
        layout.addLayout(total_layout)
        
        # Action Buttons
        self.add_to_quote_button = QPushButton("Add to Quote")
        self.add_to_quote_button.setProperty("class", "success")
        self.add_to_quote_button.clicked.connect(self._add_to_quote)
        layout.addWidget(self.add_to_quote_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self._show_selection_page)
        layout.addWidget(self.back_button)

        return panel

    def _load_options_for_product(self):
        """Load and display configuration options using QComboBoxes."""
        if not self.selected_product:
            logger.error("Cannot load options: no product selected.")
            return

        logger.info(f"Loading options for product: {self.selected_product['name']}")
        self.available_options = self.config_service.get_available_options(self.selected_product['name'])
        logger.info(f"Found {len(self.available_options)} available options.")
        
        # Clear previous options from the layout without deleting the layout itself
        if self.config_layout is not None:
            while self.config_layout.count():
                item = self.config_layout.takeAt(0)
                # The item can be a layout item or a widget item
                if item.widget():
                    item.widget().deleteLater()
                # If it's a layout, it might contain other widgets
                elif item.layout():
                    while item.layout().count():
                        child_item = item.layout().takeAt(0)
                        if child_item.widget():
                            child_item.widget().deleteLater()

        grouped_options = self._group_options_by_category(self.available_options)
        logger.info(f"Grouped options into {len(grouped_options)} categories.")

        for category, options in sorted(grouped_options.items()):
            if category.lower() == 'base': continue

            # Add section header
            section_label = QLabel(category)
            section_label.setObjectName("sectionTitle")
            self.config_layout.addRow(section_label)
            logger.info(f"Creating section for category: {category} with {len(options)} options.")

            for option in options:
                self._create_option_widget(self.config_layout, option)
        
        self._update_pricing()

    def _create_option_widget(self, layout: QFormLayout, option_data: Dict):
        """Creates a QComboBox for a given option and adds it to the form layout."""
        option_name = option_data.get('name', 'Unnamed Option')
        choices = option_data.get('choices', [])
        
        label = QLabel(option_name)
        combo = QComboBox()
        combo.setObjectName(f"combo_{option_name.replace(' ', '_')}")
        
        if not choices:
            combo.addItem("Not available")
            combo.setEnabled(False)
        else:
            if isinstance(choices[0], dict):
                # Handle list of dicts (e.g., Materials)
                for choice in choices:
                    display = choice.get('display_name', choice.get('name', 'Unnamed Choice'))
                    combo.addItem(display, userData=choice)
            else:
                # Handle list of strings
                for choice in choices:
                    combo.addItem(str(choice))

        # Store reference to the widget for later value retrieval
        self.current_config[option_name] = combo
        
        # Connect signal for price updates
        combo.currentTextChanged.connect(self._update_pricing)
        
        layout.addRow(label, combo)

    def _create_config_section(self, title: str) -> QGroupBox:
        """Creates a styled group box for an option category."""
        box = QGroupBox(title)
        box.setFlat(True)
        # Use a QFormLayout for a cleaner look
        layout = QFormLayout(box)
        layout.setSpacing(10)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        return box

    def _group_options_by_category(self, options: List[Dict]) -> Dict[str, List[Dict]]:
        """Groups a flat list of options by their 'category' property."""
        grouped = {}
        for option in options:
            category = option.get('category', 'General')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(option)
        return grouped

    def _update_pricing(self):
        """
        Calculates the total price based on the selected product and options
        and updates the summary panel.
        """
        if not self.selected_product:
            return

        selected_options = {}
        for option_name, widget in self.current_config.items():
            if isinstance(widget, QComboBox):
                selected_text = widget.currentText()
                user_data = widget.currentData()
                # If user_data (dict) is present, we prioritize its 'code' or 'name'
                if isinstance(user_data, dict):
                    # This handles complex options like Materials
                    selected_options[option_name] = user_data.get('code', user_data.get('name', selected_text))
                else:
                    selected_options[option_name] = selected_text
        
        # Create a pricing context
        context_data = {
            'product_family': self.selected_product.get('family_name'),
            'base_price': self.selected_product.get('base_price', 0),
            'selected_options': selected_options
        }

        # Calculate the price using the service
        total_price = self.config_service.calculate_price(context_data)
        
        # Update the UI
        self.total_price_label.setText(f"${total_price:,.2f}")
        self._update_summary_details(selected_options, total_price)

    def _update_summary_details(self, selected_options: Dict, total_price: float):
        """Updates the text in the summary panel."""
        if not self.selected_product:
            self.summary_content_label.setText("No product selected.")
            return

        summary_parts = [f"<b>Base Product:</b> {self.selected_product.get('name')}"]
        
        for name, value in sorted(selected_options.items()):
            if value and value != "N/A":
                summary_parts.append(f"<b>{name}:</b> {value}")

        summary_text = "<br>".join(summary_parts)
        self.summary_content_label.setText(summary_text)

