"""
Product Configuration Wizard

Modern step-by-step configuration interface with real-time pricing,
validation, and quote summary. Integrates with existing pricing logic
and configuration service.
"""

import logging
from typing import Any, Dict, List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.ui.utils.ui_integration import QuickMigrationHelper, ModernWidgetFactory

logger = logging.getLogger(__name__)


class ConfigurationWizard(QDialog):
    """
    Modern configuration wizard with step-by-step product configuration.

    Features:
    - Real-time pricing updates
    - Progressive configuration workflow
    - Material, voltage, and connection options
    - Length calculations and validation
    - Live quote summary
    - Modern UI with improved styling
    """

    configuration_completed = Signal(dict)  # Emitted when configuration is finished

    def __init__(self, product_data: Dict, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setWindowTitle(f"Configure {product_data.get('name', 'Product')}")
        self.setModal(True)
        self.resize(1200, 800)

        # Services
        self.db = SessionLocal()
        self.product_service = ProductService()
        self.config_service = ConfigurationService(self.db, self.product_service)

        # Configuration state
        self.current_config = {
            'product_family': product_data.get('family_name', product_data.get('name')),
            'base_price': product_data.get('base_price', 0),
            'selected_options': {},
            'calculated_price': product_data.get('base_price', 0),
            'validation_errors': []
        }

        # Available options (loaded from database)
        self.available_options = {}

        # Initialize UI groups
        self.material_group = None
        self.voltage_group = None

        self._setup_ui()
        self._load_available_options()
        self._update_pricing()
        
        # Apply modern styling fixes
        QuickMigrationHelper.fix_oversized_dropdowns(self)
        QuickMigrationHelper.modernize_existing_dialog(self)

    def __del__(self):
        """Clean up database connection."""
        if hasattr(self, 'db') and self.db:
            self.db.close()

    def _setup_ui(self):
        """Set up the configuration wizard UI."""
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

        # Left panel - Configuration options
        self.config_panel = self._create_config_panel()
        content_layout.addWidget(self.config_panel, 2)

        # Right panel - Quote summary
        self.summary_panel = self._create_summary_panel()
        content_layout.addWidget(self.summary_panel, 1)

        main_layout.addWidget(content_widget)

    def _create_progress_indicator(self) -> QWidget:
        """Create progress indicator showing configuration completion."""
        widget = QFrame()
        widget.setObjectName('progressIndicator')
        widget.setFixedHeight(100)  # Fixed height for consistency
        
        # Main container with proper centering
        container = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        
        # Horizontal layout for steps - this is the key fix
        layout = QHBoxLayout(container)
        layout.setContentsMargins(40, 20, 40, 20)  # Proper margins
        layout.setSpacing(0)  # No spacing - we control with stretch
        
        steps = [
            ('✓', 'Select', True, True),    # (number, label, is_complete, is_active)
            ('2', 'Configure', False, True),
            ('3', 'Quote', False, False)
        ]
        
        # Add leading stretch to center the group
        layout.addStretch(1)
        
        for i, (number, label, is_complete, is_active) in enumerate(steps):
            if i > 0:
                # Connector line with proper spacing
                layout.addSpacing(20)  # Space before line
                line = QFrame()
                line.setObjectName('progressLine')
                line.setFixedSize(60, 2)  # Longer, more proportional line
                layout.addWidget(line)
                layout.addSpacing(20)  # Space after line
            
            # Step widget
            step_widget = QWidget()
            step_widget.setFixedSize(80, 60)  # Fixed size for predictable layout
            step_layout = QVBoxLayout(step_widget)
            step_layout.setContentsMargins(0, 0, 0, 0)
            step_layout.setSpacing(8)
            step_layout.setAlignment(Qt.AlignCenter)
            
            # Circle
            circle = QLabel(number)
            circle.setFixedSize(36, 36)  # Slightly larger for better proportion
            circle.setAlignment(Qt.AlignCenter)
            circle.setProperty('class', 'stepNumber')
            circle.setProperty('completed', is_complete)
            circle.setProperty('active', is_active)
            
            # Label
            step_label = QLabel(label)
            step_label.setProperty('class', 'stepLabel')
            step_label.setAlignment(Qt.AlignCenter)
            step_label.setFixedHeight(16)  # Consistent label height
            
            step_layout.addWidget(circle)
            step_layout.addWidget(step_label)
            
            layout.addWidget(step_widget)
        
        # Add trailing stretch to center the group
        layout.addStretch(1)
        
        return widget

    def _create_config_panel(self) -> QFrame:
        """Create the configuration options panel."""
        panel = QFrame()
        panel.setObjectName('configPanel')

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(60)
        layout.addWidget(self.progress_bar)

        # Scroll area for configuration sections
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Configuration sections container
        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)
        self.config_layout.setSpacing(25)

        scroll.setWidget(self.config_widget)
        layout.addWidget(scroll)

        # Validation message area
        self.validation_widget = self._create_validation_widget()
        layout.addWidget(self.validation_widget)

        return panel

    def _create_summary_panel(self) -> QFrame:
        """Create the quote summary panel."""
        panel = QFrame()
        panel.setObjectName('summaryPanel')

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Summary card
        summary_card = QFrame()
        summary_card.setProperty('class', 'card')

        card_layout = QVBoxLayout(summary_card)

        # Title
        title = QLabel('Quote Summary')
        title.setObjectName('sectionTitle')
        card_layout.addWidget(title)

        # Line items container
        self.line_items_widget = QWidget()
        self.line_items_layout = QVBoxLayout(self.line_items_widget)
        self.line_items_layout.setSpacing(5)
        card_layout.addWidget(self.line_items_widget)

        # Total
        self.total_frame = QFrame()
        self.total_frame.setObjectName('summaryTotalFrame')
        total_layout = QHBoxLayout(self.total_frame)
        total_layout.setContentsMargins(0, 0, 0, 0)

        total_label = QLabel('Total:')
        total_label.setObjectName('summaryTotalLabel')

        self.total_price_label = QLabel('$0.00')
        self.total_price_label.setObjectName('summaryTotalPriceLabel')

        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_price_label)

        card_layout.addWidget(self.total_frame)

        # Add to quote button
        self.add_to_quote_btn = QPushButton('Add to Quote')
        self.add_to_quote_btn.setProperty('class', 'success')
        self.add_to_quote_btn.clicked.connect(self._add_to_quote)
        card_layout.addWidget(self.add_to_quote_btn)

        layout.addWidget(summary_card)
        layout.addStretch()

        return panel

    def _create_validation_widget(self) -> QWidget:
        """Create validation message widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.validation_label = QLabel('')
        self.validation_label.setWordWrap(True)
        self.validation_label.hide()
        layout.addWidget(self.validation_label)

        return widget

    def _load_available_options(self):
        """Load available configuration options from the database using the service layer."""
        family_name = self.current_config['product_family']

        try:
            # Get materials using ProductService
            materials = self.product_service.get_available_materials_for_product(self.db, family_name)
            if materials:
                self._create_material_section(materials)

            # Get voltages using ProductService
            voltages = self.product_service.get_available_voltages(self.db, family_name)
            if voltages:
                self._create_voltage_section(voltages)

            # Get probe length options (can be hardcoded or moved to a config file)
            self._create_probe_section()

            # Get additional options by category
            additional_options = self.product_service.get_additional_options(self.db, family_name)
            self._create_additional_options_sections(additional_options)

        except Exception as e:
            logger.error(f'Error loading configuration options: {e}')

    def _create_material_section(self, materials_config: List[Dict]):
        """Create material selection section from service data."""
        section = self._create_config_section('1. Material Selection')

        label = QLabel('Housing Material *')
        label.setProperty('class', 'formLabel')
        section.layout().addWidget(label)

        material_layout = QVBoxLayout()
        self.material_group = QButtonGroup()

        # Handle the materials_config structure correctly
        if not materials_config:
            return

        # materials_config is a list of option dicts, we need the first one with choices
        material_option = None
        for option in materials_config:
            if option.get('category') == 'Material' and option.get('choices'):
                material_option = option
                break

        if not material_option:
            return

        choices = material_option.get('choices', [])
        adders = material_option.get('adders', {})

        for i, choice in enumerate(choices):
            # Handle both string and dict choices
            if isinstance(choice, dict):
                code = choice.get('code', '')
                display_name = choice.get('display_name', code)
            else:
                code = str(choice)
                display_name = str(choice)

            adder = adders.get(code, 0)

            radio = QRadioButton(f'{display_name}')
            radio.setProperty('material_code', code)
            radio.setProperty('adder', adder)

            if i == 0:  # Select first option by default
                radio.setChecked(True)
                self.current_config['selected_options']['Material'] = code

            radio.toggled.connect(self._on_material_changed)
            self.material_group.addButton(radio)
            material_layout.addWidget(radio)

        section.layout().addLayout(material_layout)
        self.config_layout.addWidget(section)

    def _create_voltage_section(self, voltages: List[str]):
        """Create voltage selection section from service data."""
        section = self._create_config_section('2. Electrical Configuration')

        label = QLabel('Supply Voltage *')
        label.setProperty('class', 'formLabel')
        section.layout().addWidget(label)

        voltage_layout = QHBoxLayout()
        self.voltage_group = QButtonGroup()

        for i, voltage in enumerate(voltages):
            radio = QRadioButton(voltage)
            radio.setProperty('voltage', voltage)
            radio.setProperty('adder', 0) # Assuming no adder for voltage for now

            if i == 0:  # Select first option by default
                radio.setChecked(True)
                self.current_config['selected_options']['Voltage'] = voltage

            radio.toggled.connect(self._on_voltage_changed)
            self.voltage_group.addButton(radio)
            voltage_layout.addWidget(radio)

        section.layout().addLayout(voltage_layout)
        self.config_layout.addWidget(section)

    def _create_probe_section(self):
        """Create probe configuration section."""
        section = self._create_config_section('3. Probe Configuration')

        length_layout = QHBoxLayout()

        length_label = QLabel('Probe Length (inches) *')
        length_label.setProperty('class', 'formLabel')

        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(6, 120)
        self.length_spinbox.setValue(12)  # Default length
        self.length_spinbox.setSuffix('"')
        self.length_spinbox.valueChanged.connect(self._on_length_changed)

        self.current_config['selected_options']['Probe Length'] = 12

        length_layout.addWidget(length_label)
        length_layout.addStretch()
        length_layout.addWidget(self.length_spinbox)

        section.layout().addLayout(length_layout)

        # The extended probe option can be one of the additional options now
        self.config_layout.addWidget(section)

    def _create_additional_options_sections(self, options: List[Dict]):
        """Create sections for all additional options returned by the service."""
        # Group options by category
        options_by_category = {}
        for option in options:
            category = option.get('category', 'Other Options')
            if category not in options_by_category:
                options_by_category[category] = []
            options_by_category[category].append(option)

        # Create a section for each category
        for category_name, category_options in options_by_category.items():
            # Skip core options handled elsewhere
            if category_name in ['Material', 'Voltage']:
                continue

            section = self._create_config_section(category_name)
            for option in category_options:
                self._create_option_widget(section, option)
            self.config_layout.addWidget(section)

    def _create_option_widget(self, section: QGroupBox, option_data: Dict):
        """Create a widget for a single dynamic option."""
        name = option_data.get('name')
        choices = option_data.get('choices', [])
        adders = option_data.get('adders', {})

        if not choices:
            return

        label = QLabel(f'{name}:')
        label.setProperty('class', 'formLabel')

        combo = QComboBox()
        for choice in choices:
            # Handle both simple strings and dicts for choices
            code = choice if isinstance(choice, str) else choice.get('code', '')
            display = choice if isinstance(choice, str) else choice.get('display_name', code)
            adder = adders.get(code, 0)

            display_text = f'{display} (+${adder})' if adder > 0 else display
            combo.addItem(display_text, code)

        combo.currentTextChanged.connect(
            lambda text, opt_name=name: self._on_dynamic_option_changed(opt_name, combo.currentData())
        )

        # Add to section layout
        section.layout().addWidget(label)
        section.layout().addWidget(combo)

    def _create_config_section(self, title: str) -> QGroupBox:
        """Create a configuration section with title."""
        section = QGroupBox(title)
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        return section

    # Event handlers for configuration changes
    def _on_material_changed(self, checked):
        """Handle material selection change."""
        if checked and self.material_group:
            button = self.material_group.checkedButton()
            if button:
                material_code = button.property('material_code')
                self.current_config['selected_options']['Material'] = material_code
                self._update_pricing()

    def _on_voltage_changed(self, checked):
        """Handle voltage selection change."""
        if checked and self.voltage_group:
            button = self.voltage_group.checkedButton()
            if button:
                voltage = button.property('voltage')
                self.current_config['selected_options']['Voltage'] = voltage
                self._update_pricing()

    def _on_length_changed(self, value):
        """Handle probe length change."""
        self.current_config['selected_options']['Probe Length'] = value
        self._update_pricing()

    def _on_dynamic_option_changed(self, option_name: str, value: Any):
        """Handle dynamic option changes."""
        self.current_config['selected_options'][option_name] = value
        self._update_pricing()

    def _update_pricing(self):
        """Update pricing calculations and display."""
        try:
            # Calculate total price based on selections
            base_price = self.current_config['base_price']
            total_price = base_price

            # Material adder
            for button in self.material_group.buttons():
                if button.isChecked():
                    adder = button.property('adder')
                    if adder:
                        total_price += adder
                    break

            # Voltage adder
            for button in self.voltage_group.buttons():
                if button.isChecked():
                    adder = button.property('adder')
                    if adder:
                        total_price += adder
                    break

            # Length calculation (simplified)
            base_length = BASE_MODELS.get(self.current_config['product_family'], {}).get('base_length', 10)
            current_length = self.current_config['selected_options'].get('Probe Length', base_length)
            if current_length > base_length:
                length_adder = (current_length - base_length) * 8.0  # $8 per inch
                total_price += length_adder

            # Extended probe
            if self.current_config['selected_options'].get('Extended Probe', False):
                total_price += 150

            # Connection adder
            if hasattr(self, 'connection_combo'):
                connection_data = self.connection_combo.currentData()
                if connection_data and connection_data.get('adder'):
                    total_price += connection_data['adder']

            # Additional options
            if self.current_config['selected_options'].get('Explosion Proof', False):
                total_price += 300

            if self.current_config['selected_options'].get('NEMA 4X', False):
                total_price += 100

            self.current_config['calculated_price'] = total_price
            self._update_summary_display()
            self._update_validation()

        except Exception as e:
            logger.error(f'Error updating pricing: {e}')

    def _update_summary_display(self):
        """Update the quote summary display."""
        # Clear existing line items
        for i in reversed(range(self.line_items_layout.count())):
            item = self.line_items_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        # Base product
        base_item = self._create_line_item(
            f"{self.current_config['product_family']} Base",
            self.current_config['base_price']
        )
        self.line_items_layout.addWidget(base_item)

        # Material upgrade
        for button in self.material_group.buttons():
            if button.isChecked():
                adder = button.property('adder')
                if adder and adder > 0:
                    material_code = button.property('material_code')
                    material_name = self._get_material_name(material_code)
                    material_item = self._create_line_item(f'Material: {material_name}', adder)
                    self.line_items_layout.addWidget(material_item)
                break

        # Length adder
        base_length = BASE_MODELS.get(self.current_config['product_family'], {}).get('base_length', 10)
        current_length = self.current_config['selected_options'].get('Probe Length', base_length)
        if current_length > base_length:
            extra_inches = current_length - base_length
            length_cost = extra_inches * 8.0
            length_item = self._create_line_item(f'Extra Length: {extra_inches}"', length_cost)
            self.line_items_layout.addWidget(length_item)

        # Extended probe
        if self.current_config['selected_options'].get('Extended Probe', False):
            extended_item = self._create_line_item('Extended Probe', 150)
            self.line_items_layout.addWidget(extended_item)

        # Connection upgrade
        if hasattr(self, 'connection_combo'):
            connection_data = self.connection_combo.currentData()
            if connection_data and connection_data.get('adder', 0) > 0:
                connection_item = self._create_line_item(
                    f"Connection: {connection_data['type']}",
                    connection_data['adder']
                )
                self.line_items_layout.addWidget(connection_item)

        # Additional options
        if self.current_config['selected_options'].get('Explosion Proof', False):
            exp_item = self._create_line_item('Explosion Proof Housing', 300)
            self.line_items_layout.addWidget(exp_item)

        if self.current_config['selected_options'].get('NEMA 4X', False):
            nema_item = self._create_line_item('NEMA 4X Rating', 100)
            self.line_items_layout.addWidget(nema_item)

        # Update total
        self.total_price_label.setText(f"${self.current_config['calculated_price']:,.2f}")

    def _create_line_item(self, name: str, price: float) -> QWidget:
        """Create a line item widget for the summary."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 5)

        name_label = QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 14px;
            }
        """)

        price_label = QLabel(f'${price:,.2f}')
        price_label.setAlignment(Qt.AlignRight)
        price_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 500;
            }
        """)

        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(price_label)

        widget.setStyleSheet("""
            QWidget {
                border-bottom: 1px solid #F1F3F4;
                padding: 5px 0;
            }
        """)

        return widget

    def _update_validation(self):
        """Update validation status and messages."""
        errors = []

        # Check required fields
        if 'Material' not in self.current_config['selected_options']:
            errors.append('Material selection is required')

        if 'Voltage' not in self.current_config['selected_options']:
            errors.append('Voltage selection is required')

        if 'Probe Length' not in self.current_config['selected_options']:
            errors.append('Probe length is required')

        # Update validation display
        if errors:
            self.validation_label.setText('⚠️ ' + '; '.join(errors))
            self.validation_label.setStyleSheet("""
                QLabel {
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            self.validation_label.show()
            self.add_to_quote_btn.setEnabled(False)
        else:
            self.validation_label.setText('✓ Configuration is valid and ready for quoting')
            self.validation_label.setStyleSheet("""
                QLabel {
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    color: #155724;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            self.validation_label.show()
            self.add_to_quote_btn.setEnabled(True)

        # Update progress bar
        total_sections = 5
        completed_sections = 0

        if 'Material' in self.current_config['selected_options']:
            completed_sections += 1
        if 'Voltage' in self.current_config['selected_options']:
            completed_sections += 1
        if 'Probe Length' in self.current_config['selected_options']:
            completed_sections += 1
        if 'Connection' in self.current_config['selected_options']:
            completed_sections += 1

        # Always count additional options as complete (they're optional)
        completed_sections += 1

        progress = int((completed_sections / total_sections) * 100)
        self.progress_bar.setValue(progress)

    def _add_to_quote(self):
        """Add the configured product to the quote."""
        try:
            # Generate model number
            model_number = self._generate_model_number()

            # Prepare configuration data
            configuration_data = {
                'product_family': self.current_config['product_family'],
                'model_number': model_number,
                'selected_options': self.current_config['selected_options'].copy(),
                'calculated_price': self.current_config['calculated_price'],
                'base_price': self.current_config['base_price'],
                'product_data': self.product_data.copy()
            }

            # Emit completion signal
            self.configuration_completed.emit(configuration_data)
            self.accept()

        except Exception as e:
            logger.error(f'Error adding product to quote: {e}')
            self.validation_label.setText(f'❌ Error: {e!s}')
            self.validation_label.setStyleSheet("""
                QLabel {
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    color: #721c24;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            self.validation_label.show()

    def _generate_model_number(self) -> str:
        """Generate the model number based on current configuration."""
        try:
            family = self.current_config['product_family']
            voltage = self.current_config['selected_options'].get('Voltage', '115VAC')
            material = self.current_config['selected_options'].get('Material', 'S')
            length = self.current_config['selected_options'].get('Probe Length', 12)

            # Format: FAMILY-VOLTAGE-MATERIAL-LENGTH"
            model_number = f'{family}-{voltage}-{material}-{length}"'

            # Add connection suffix if not NPT
            connection = self.current_config['selected_options'].get('Connection')
            if connection and connection != 'NPT':
                if connection == 'Flange':
                    model_number += '-FL'
                elif connection == 'Tri-Clamp':
                    model_number += '-TC'

            return model_number

        except Exception as e:
            logger.error(f'Error generating model number: {e}')
            return f"{self.current_config['product_family']}-CUSTOM"

    def closeEvent(self, event):
        """Handle dialog close event."""
        # Clean up database connection
        if hasattr(self, 'db') and self.db:
            self.db.close()
        event.accept()


class QuoteSummaryPanel(QFrame):
    """
    Standalone quote summary panel that can be reused in other contexts.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.line_items = []
        self.total_price = 0.0

    def _setup_ui(self):
        """Set up the summary panel UI."""
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E9ECEF;
                border-radius: 8px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(self)

        # Title
        title = QLabel('Quote Summary')
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2C3E50;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(title)

        # Line items
        self.items_widget = QWidget()
        self.items_layout = QVBoxLayout(self.items_widget)
        layout.addWidget(self.items_widget)

        # Total
        self.total_widget = QWidget()
        total_layout = QHBoxLayout(self.total_widget)
        total_layout.setContentsMargins(0, 15, 0, 0)

        total_label = QLabel('Total:')
        total_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2C3E50;
                border-top: 2px solid #E9ECEF;
                padding-top: 15px;
            }
        """)

        self.total_price_label = QLabel('$0.00')
        self.total_price_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2C3E50;
                border-top: 2px solid #E9ECEF;
                padding-top: 15px;
            }
        """)

        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_price_label)

        layout.addWidget(self.total_widget)

    def add_line_item(self, name: str, price: float):
        """Add a line item to the summary."""
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(0, 5, 0, 5)

        name_label = QLabel(name)
        price_label = QLabel(f'${price:,.2f}')
        price_label.setAlignment(Qt.AlignRight)

        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(price_label)

        item_widget.setStyleSheet("""
            QWidget {
                border-bottom: 1px solid #F1F3F4;
                padding: 8px 0;
            }
        """)

        self.items_layout.addWidget(item_widget)
        self.line_items.append({'name': name, 'price': price, 'widget': item_widget})

        self._update_total()

    def clear_items(self):
        """Clear all line items."""
        for item in self.line_items:
            item['widget'].setParent(None)

        self.line_items.clear()
        self.total_price = 0.0
        self._update_total()

    def _update_total(self):
        """Update the total price display."""
        self.total_price = sum(item['price'] for item in self.line_items)
        self.total_price_label.setText(f'${self.total_price:,.2f}')

    def get_total(self) -> float:
        """Get the current total price."""
        return self.total_price

    def get_line_items(self) -> List[Dict]:
        """Get all line items."""
        return [{'name': item['name'], 'price': item['price']} for item in self.line_items]
