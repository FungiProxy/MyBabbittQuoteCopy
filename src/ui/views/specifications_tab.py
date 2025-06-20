"""
Specifications Tab for the Babbitt Quote Generator.

This module defines the specifications configuration interface for the quote generator.
It provides a dynamic form for configuring product specifications based on the
selected product model, including:
- Voltage selection
- Material options
- Probe configurations
- Connection types and sizes
- Additional options and features

The specifications are organized into logical sections and automatically updated
based on product selection and database-driven options.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService


class SpecificationsTab(QWidget):
    """
    Specifications configuration tab for the quote generator.

    This tab provides a dynamic form interface for configuring product specifications.
    It updates its available options based on the selected product and retrieves
    valid configurations from the database.

    The tab is organized into sections including:
    - Voltage selection
    - Material options
    - Probe configuration
    - Connection types
    - Additional features

    Attributes:
        current_product (dict): Currently selected product information
        specs_widgets (dict): References to specification input widgets
        product_service (ProductService): Service for product data access
        scroll (QScrollArea): Scrollable container for specifications
        scroll_content (QWidget): Container for specification sections
        specs_layout (QVBoxLayout): Layout manager for specifications
        add_to_quote_button (QPushButton): Button to add configured product to quote

    Signals:
        specs_updated (dict): Emitted when specifications are modified
        add_to_quote (dict): Emitted when current configuration should be added to quote
    """

    # Signals
    specs_updated = Signal(dict)  # specifications dictionary
    add_to_quote = Signal(dict)  # Signal to add current specs to quote

    def __init__(self, parent=None):
        """
        Initialize the SpecificationsTab.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.init_ui()
        self.current_product = None
        self.specs_widgets = {}  # Store references to specification widgets
        self.product_service = ProductService()

    def init_ui(self):
        """
        Initialize the UI components.

        Sets up the scrollable specifications form and the "Add to Quote" button.
        Initially displays a placeholder message until a product is selected.
        """
        # Main layout
        main_layout = QVBoxLayout(self)

        # Create a scroll area for specifications
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.specs_layout = QVBoxLayout(self.scroll_content)

        # Placeholder text when no product is selected
        self.placeholder_label = QLabel(
            "Please select a product in the Product Selection tab to configure specifications."
        )
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.specs_layout.addWidget(self.placeholder_label)

        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        # Add to Quote button
        self.add_to_quote_button = QPushButton("Add to Quote")
        self.add_to_quote_button.setObjectName("add_to_quote_button")
        self.add_to_quote_button.setStyleSheet(
            """
            #add_to_quote_button {
                background-color: #08D13F;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
            }
            #add_to_quote_button:hover {
                background-color: #05A32F;
            }
        """
        )
        self.add_to_quote_button.clicked.connect(self.on_add_to_quote)
        self.add_to_quote_button.setEnabled(
            False
        )  # Initially disabled until product is selected
        main_layout.addWidget(self.add_to_quote_button)

    def update_specifications(self, product_info):
        """
        Update the specifications display based on the selected product.

        Args:
            product_info (dict): Dictionary containing product information
        """
        self.current_product = product_info
        self._clear_specs()

        if not product_info:
            self.placeholder_label.setVisible(True)
            self.add_to_quote_button.setEnabled(False)
            return

        self.placeholder_label.setVisible(False)
        self.add_to_quote_button.setEnabled(True)

        # Create sections for different types of specifications
        voltage_group = QGroupBox("Voltage")
        voltage_layout = QFormLayout()

        voltage_combo = QComboBox()
        voltage_combo.addItems(["12VDC", "24VDC", "115VAC", "240VAC"])
        voltage_combo.currentTextChanged.connect(
            lambda text: self._on_spec_changed("voltage", text)
        )
        voltage_layout.addRow("Select Voltage:", voltage_combo)
        voltage_group.setLayout(voltage_layout)
        self.specs_widgets["voltage"] = voltage_combo

        # Only show material and probe length for non-presence/absence switches
        if product_info["model"] not in ["LS7500", "LS8500"]:
            material_group = QGroupBox("Material")
            material_layout = QFormLayout()

            material_combo = QComboBox()
            material_combo.addItems(
                [
                    "316SS",
                    "316SS with Teflon Sleeve",
                    "316SS with Halar Coating",
                    "Titanium",
                    "Titanium with Teflon Sleeve",
                ]
            )
            material_combo.currentTextChanged.connect(
                lambda text: self._on_spec_changed("material", text)
            )
            material_layout.addRow("Select Material:", material_combo)
            material_group.setLayout(material_layout)
            self.specs_widgets["material"] = material_combo

            probe_group = QGroupBox("Probe Configuration")
            probe_layout = QFormLayout()

            length_spin = QSpinBox()
            length_spin.setRange(1, 120)
            length_spin.setSuffix('"')
            length_spin.valueChanged.connect(
                lambda value: self._on_spec_changed("probe_length", value)
            )
            probe_layout.addRow("Probe Length:", length_spin)
            self.specs_widgets["probe_length"] = length_spin

            probe_group.setLayout(probe_layout)
            self.specs_layout.addWidget(probe_group)

        connection_group = QGroupBox("Connection")
        connection_layout = QFormLayout()

        connection_combo = QComboBox()
        connection_combo.addItems(["NPT", "Flange", "Tri-Clamp"])
        connection_combo.currentTextChanged.connect(
            lambda text: self._on_connection_changed(text)
        )
        connection_layout.addRow("Connection Type:", connection_combo)
        self.specs_widgets["connection_type"] = connection_combo

        # Connection size options
        self.npt_size_combo = QComboBox()
        self.npt_size_combo.addItems(['1/2"', '3/4"', '1"', '1-1/2"', '2"'])
        self.npt_size_combo.currentTextChanged.connect(
            lambda text: self._on_spec_changed("npt_size", text)
        )
        connection_layout.addRow("NPT Size:", self.npt_size_combo)
        self.specs_widgets["npt_size"] = self.npt_size_combo

        self.flange_rating_combo = QComboBox()
        self.flange_rating_combo.addItems(["150#", "300#"])
        self.flange_rating_combo.currentTextChanged.connect(
            lambda text: self._on_spec_changed("flange_rating", text)
        )
        connection_layout.addRow("Flange Rating:", self.flange_rating_combo)
        self.specs_widgets["flange_rating"] = self.flange_rating_combo

        self.flange_size_combo = QComboBox()
        self.flange_size_combo.addItems(['1"', '1-1/2"', '2"', '3"', '4"'])
        self.flange_size_combo.currentTextChanged.connect(
            lambda text: self._on_spec_changed("flange_size", text)
        )
        connection_layout.addRow("Flange Size:", self.flange_size_combo)
        self.specs_widgets["flange_size"] = self.flange_size_combo

        self.triclamp_size_combo = QComboBox()
        self.triclamp_size_combo.addItems(['1"', '1-1/2"', '2"', '3"', '4"'])
        self.triclamp_size_combo.currentTextChanged.connect(
            lambda text: self._on_spec_changed("triclamp_size", text)
        )
        connection_layout.addRow("Tri-Clamp Size:", self.triclamp_size_combo)
        self.specs_widgets["triclamp_size"] = self.triclamp_size_combo

        # Initially hide all connection size options except NPT
        self.flange_rating_combo.setVisible(False)
        self.flange_size_combo.setVisible(False)
        self.triclamp_size_combo.setVisible(False)

        connection_group.setLayout(connection_layout)

        # Add all groups to the main layout
        self.specs_layout.addWidget(voltage_group)
        if product_info["model"] not in ["LS7500", "LS8500"]:
            self.specs_layout.addWidget(material_group)
        self.specs_layout.addWidget(connection_group)

        # Add additional options group
        options_group = QGroupBox("Additional Options")
        options_layout = QVBoxLayout()

        # Add checkboxes for additional options
        self.additional_options = {
            "High Temperature": QCheckBox("High Temperature Option (+$150.00)"),
            "Explosion Proof": QCheckBox("Explosion Proof Housing (+$295.00)"),
            "Weather Shield": QCheckBox("Weather Shield (+$95.00)"),
            "Mounting Bracket": QCheckBox("Mounting Bracket (+$45.00)"),
        }

        for name, checkbox in self.additional_options.items():
            checkbox.stateChanged.connect(
                lambda state, opt=name: self._on_option_changed(
                    opt, state == Qt.Checked
                )
            )
            options_layout.addWidget(checkbox)
            self.specs_widgets[name] = checkbox

        options_group.setLayout(options_layout)
        self.specs_layout.addWidget(options_group)

        # Add spacer at the bottom
        self.specs_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def _clear_specs(self):
        """Clear all specification widgets."""
        # Delete all widgets in the specs layout
        while self.specs_layout.count():
            item = self.specs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear the specs widgets dictionary
        self.specs_widgets.clear()

    def _on_spec_changed(self, name, value):
        """Handle changes to specific specification values."""
        try:
            # Update the current specification value
            self.specs_widgets[name] = value

            # Special handling for O-ring selection
            if name == "O-Rings":
                # Get the configuration service from the parent dialog
                dialog = self.parent()
                if dialog and hasattr(dialog, "config_service"):
                    dialog.config_service.select_option("O-Rings", value)
                    dialog._update_total_price()

            # Emit signal with updated specifications
            self.specs_updated.emit(self.specs_widgets)
        except Exception as e:
            logger.error(f"Error handling specification change: {e!s}", exc_info=True)

    def _on_connection_changed(self, text):
        """Handle changes to connection type."""
        # Update the current connection type
        # Remove placeholder
        if self.placeholder_label:
            self.placeholder_label.deleteLater()
            self.placeholder_label = None

        # Add header
        header = QLabel(f"<h3>Specifications for {model}</h3>")
        header.setAlignment(Qt.AlignCenter)
        self.specs_layout.addWidget(header)

        # Add specification sections in standard order
        self.add_voltage_section()
        self.add_material_section()
        self.add_probe_length_section()
        self.add_connection_section()
        self.add_exotic_metals_section()
        self.add_oring_section()
        self.add_cable_length_section()
        self.add_housing_section()
        self.add_additional_options_section()

        # Add spacer at the bottom
        self.specs_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Connect change signals for all widgets
        for _widget_name, widget in self.specs_widgets.items():
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.on_specs_changed)
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.valueChanged.connect(self.on_specs_changed)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.on_specs_changed)
            elif isinstance(widget, QSlider):
                widget.valueChanged.connect(self.on_specs_changed)

        # Enable add to quote button
        self.add_to_quote_button.setEnabled(True)

    def add_voltage_section(self):
        """
        Add voltage selection section to the specifications form.

        Creates a group box with voltage options appropriate for the
        current product, fetching available options from the database.
        """
        group = QGroupBox("Voltage")
        layout = QFormLayout()

        voltage = QComboBox()

        # Get available voltages for the current product family
        if self.current_product and "model" in self.current_product:
            product_family = self.current_product["model"].split()[0]

            db = SessionLocal()
            try:
                available_voltages = self.product_service.get_available_voltages(
                    db, product_family
                )
                voltage.addItems(available_voltages)
            finally:
                db.close()

        layout.addRow("Supply Voltage:", voltage)
        self.specs_widgets["voltage"] = voltage

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def add_material_section(self):
        """
        Add material selection section to the specifications form.

        Creates a group box with material options appropriate for the
        current product, fetching available options from the database.
        """
        group = QGroupBox("Material")
        layout = QFormLayout()

        material = QComboBox()

        if self.current_product and "model" in self.current_product:
            product_family = self.current_product["model"].split()[0]

            db = SessionLocal()
            try:
                available_materials = (
                    self.product_service.get_available_materials_for_product(
                        db, product_family
                    )
                )
                material.addItems([m["display_name"] for m in available_materials])
            finally:
                db.close()

        layout.addRow("Material:", material)
        self.specs_widgets["material"] = material

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def add_probe_length_section(self):
        """
        Add probe length configuration section to the specifications form.

        Creates a group box with probe length options including both a spinner wheel
        and a text input box for flexible length selection.
        """
        if "Emissions" in self.current_product.get("category", ""):
            return

        group = QGroupBox("Probe Length")
        layout = QFormLayout()

        # Create a horizontal layout for the length inputs
        length_layout = QHBoxLayout()

        # Spinner wheel (QSpinBox)
        probe_length_spinner = QSpinBox()
        probe_length_spinner.setRange(1, 120)
        probe_length_spinner.setValue(12)
        probe_length_spinner.setSuffix(" inches")
        probe_length_spinner.setWrapping(True)  # Enable wrapping for circular scrolling
        probe_length_spinner.setStyleSheet(
            """
            QSpinBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
                background: #f0f0f0;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #e0e0e0;
            }
        """
        )

        # Text input box (QLineEdit)
        probe_length_input = QLineEdit()
        probe_length_input.setPlaceholderText("Enter length in inches")
        probe_length_input.setValidator(
            QIntValidator(1, 120)
        )  # Only allow integers between 1 and 120
        probe_length_input.setStyleSheet(
            """
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
        """
        )

        # Add both widgets to the horizontal layout
        length_layout.addWidget(probe_length_spinner)
        length_layout.addWidget(probe_length_input)

        # Connect signals for synchronization
        def on_spinner_changed(value):
            probe_length_input.setText(str(value))
            self._on_probe_length_changed(value)

        def on_input_changed():
            try:
                value = int(probe_length_input.text())
                if 1 <= value <= 120:
                    probe_length_spinner.setValue(value)
                    self._on_probe_length_changed(value)
            except ValueError:
                pass

        probe_length_spinner.valueChanged.connect(on_spinner_changed)
        probe_length_input.textChanged.connect(on_input_changed)

        # Add the horizontal layout to the form
        layout.addRow("Probe Length:", length_layout)

        # Store both widgets for later access
        self.specs_widgets["probe_length_spinner"] = probe_length_spinner
        self.specs_widgets["probe_length_input"] = probe_length_input

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def _on_probe_length_changed(self, value):
        """Handle probe length changes and update pricing."""
        material = self.specs_widgets.get("material")
        if material and material.currentText():
            material_code = material.currentText().split(" - ")[0]

            # Show warning for Halar coating at 96"
            if (
                hasattr(self, "material_combo")
                and self.material_combo.currentText() == "H"
                and value >= 84
            ):
                QMessageBox.warning(
                    self,
                    "Halar Coating Warning",
                    'Maximum probe length with Halar coating is 96". For longer probes, please use Teflon Sleeve.',
                    QMessageBox.StandardButton.Ok,
                )

            # Show warning for non-standard lengths with Halar
            if material_code == "H" and value not in [
                6,
                10,
                12,
                18,
                24,
                36,
                48,
                60,
                72,
                84,
                96,
            ]:
                QMessageBox.information(
                    self,
                    "Non-Standard Length",
                    "This is a non-standard length for Halar coating. A $300 adder will apply.",
                )

        # Update the total price
        self.on_specs_changed()

    def add_connection_section(self):
        """
        Add connection configuration section to the specifications form.

        Creates a group box with connection options including:
        - Connection type (NPT, Flange, Tri-Clamp)
        - Size options for each connection type
        - Flange ratings when applicable

        The visible options update dynamically based on the selected
        connection type.
        """
        group = QGroupBox("Connection")
        layout = QFormLayout()

        # Connection type selection
        connection_type = QComboBox()
        connection_type.addItems(["NPT", "Flange", "Tri-Clamp"])
        layout.addRow("Connection Type:", connection_type)
        self.specs_widgets["connection_type"] = connection_type

        # NPT size selection
        npt_size = QComboBox()
        npt_size.addItems(['1/2" NPT', '3/4" NPT', '1" NPT', '1.5" NPT', '2" NPT'])
        layout.addRow("NPT Size:", npt_size)
        self.specs_widgets["npt_size"] = npt_size

        # Flange rating and size
        flange_rating = QComboBox()
        flange_rating.addItems(["150#", "300#"])
        layout.addRow("Flange Rating:", flange_rating)
        self.specs_widgets["flange_rating"] = flange_rating

        flange_size = QComboBox()
        flange_size.addItems(['1"', '1.5"', '2"', '3"', '4"'])
        layout.addRow("Flange Size:", flange_size)
        self.specs_widgets["flange_size"] = flange_size

        # Tri-Clamp size
        triclamp_size = QComboBox()
        triclamp_size.addItems(['1.5"', '2"'])
        layout.addRow("Tri-Clamp Size:", triclamp_size)
        self.specs_widgets["triclamp_size"] = triclamp_size

        # Show/hide widgets based on connection type
        def update_connection_fields():
            if connection_type.currentText() == "NPT":
                npt_size.show()
                flange_rating.hide()
                flange_size.hide()
                triclamp_size.hide()
            elif connection_type.currentText() == "Flange":
                npt_size.hide()
                flange_rating.show()
                flange_size.show()
                triclamp_size.hide()
            elif connection_type.currentText() == "Tri-Clamp":
                npt_size.hide()
                flange_rating.hide()
                flange_size.hide()
                triclamp_size.show()

        connection_type.currentIndexChanged.connect(update_connection_fields)
        update_connection_fields()

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def add_exotic_metals_section(self):
        """
        Add exotic metals selection section to the specifications form.

        Creates a group box for selecting exotic metal options when
        available for the current product.
        """
        group = QGroupBox("Exotic Metals")
        layout = QFormLayout()

        exotic_metals = QComboBox()
        exotic_metals.addItems(["None", "T - Titanium", "U - Monel"])
        layout.addRow("Exotic Metal Option:", exotic_metals)
        self.specs_widgets["exotic_metals"] = exotic_metals

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def add_oring_section(self):
        """Add O-ring material section."""
        # Skip for products without O-rings
        if "Emissions" in self.current_product.get("category", ""):
            return

        group = QGroupBox("O-ring Material")
        layout = QFormLayout()

        oring = QComboBox()
        oring.addItems(["Viton", "PTFE", "Kalrez", "EPDM"])
        layout.addRow("O-ring Material:", oring)
        self.specs_widgets["oring"] = oring

        # Connect the O-ring selection to the configuration service
        oring.currentTextChanged.connect(
            lambda text: self._on_spec_changed("O-Rings", text)
        )

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def add_cable_length_section(self):
        """Add cable length section."""
        group = QGroupBox("Cable Length")
        layout = QFormLayout()

        cable_length = QSpinBox()
        cable_length.setRange(0, 100)
        cable_length.setValue(10)
        cable_length.setSuffix(" feet")
        layout.addRow("Cable Length:", cable_length)
        self.specs_widgets["cable_length"] = cable_length

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def add_housing_section(self):
        """Add housing type section."""
        group = QGroupBox("Housing Type")
        layout = QFormLayout()

        housing = QComboBox()
        housing.addItems(["Standard", "Explosion-Proof", "Stainless Steel"])
        layout.addRow("Housing Type:", housing)
        self.specs_widgets["housing"] = housing

        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def add_additional_options_section(self):
        """Add additional options section."""
        group = QGroupBox("Additional Options")
        layout = QVBoxLayout()
        db = SessionLocal()
        try:
            options = self.product_service.get_all_additional_options(db)
            for opt in options:
                label = f"{opt.name} (+${opt.price:.2f})" if opt.price else opt.name
                checkbox = QCheckBox(label)
                if opt.description:
                    checkbox.setToolTip(opt.description)
                layout.addWidget(checkbox)
                self.specs_widgets[opt.name] = checkbox
        finally:
            db.close()
        group.setLayout(layout)
        self.specs_layout.addWidget(group)

    def on_specs_changed(self):
        """Handle changes to specification values."""
        # Get all current specification values
        specs = self.get_specifications()

        # Emit signal with updated specifications
        self.specs_updated.emit(specs)

    def get_specifications(self):
        """Get all current specification values."""
        specs = {}

        # Extract values from all specification widgets
        for name, widget in self.specs_widgets.items():
            if isinstance(widget, QComboBox):
                specs[name] = widget.currentText()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                specs[name] = widget.value()
            elif isinstance(widget, QSlider):
                specs[name] = widget.value()
            elif isinstance(widget, QCheckBox):
                specs[name] = widget.isChecked()
            elif isinstance(widget, QLineEdit):
                specs[name] = widget.text()

        return specs

    def on_add_to_quote(self):
        """Handle add to quote button click."""
        # Get the current specifications
        specs = self.get_specifications()

        # Emit the add_to_quote signal with the specifications
        self.add_to_quote.emit(specs)

        # Reset specifications to default values
        self.reset_to_defaults()

    def reset_to_defaults(self):
        """Reset all specifications to their default values."""
        try:
            # Reset all widgets to default values
            for name, widget in self.specs_widgets.items():
                if isinstance(widget, QComboBox):
                    widget.setCurrentIndex(0)  # Set to first item
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    if "length" in name:
                        if name == "probe_length":
                            widget.setValue(12)  # Default probe length
                        elif name == "cable_length":
                            widget.setValue(10)  # Default cable length
                        else:
                            widget.setValue(widget.minimum())  # Set to minimum value
                    else:
                        widget.setValue(widget.minimum())  # Set to minimum value
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(False)  # Uncheck
                elif isinstance(widget, QSlider):
                    widget.setValue(widget.minimum())  # Set to minimum value

            # Emit signal with updated specifications
            self.on_specs_changed()

            print("Specifications reset to defaults")
        except Exception as e:
            print(f"Error resetting specifications: {e}")

    def clear_specifications(self):
        """Clear all specification widgets."""
        # Delete all widgets in the specs layout
        while self.specs_layout.count():
            item = self.specs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear the specs widgets dictionary
        self.specs_widgets.clear()
