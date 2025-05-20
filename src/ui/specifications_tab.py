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

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QGroupBox, QFormLayout, QSpacerItem,
    QSizePolicy, QSlider, QSpinBox, QDoubleSpinBox,
    QCheckBox, QScrollArea, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt, Signal

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
        self.add_to_quote_button.setStyleSheet("""
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
        """)
        self.add_to_quote_button.clicked.connect(self.on_add_to_quote)
        self.add_to_quote_button.setEnabled(False)  # Initially disabled until product is selected
        main_layout.addWidget(self.add_to_quote_button)
    
    def update_for_product(self, category, model):
        """
        Update specifications form for a newly selected product.
        
        Clears existing specifications and rebuilds the form with
        options appropriate for the selected product category and model.
        
        Args:
            category (str): Product category (e.g., "Level Switch")
            model (str): Product model number
        """
        self.current_product = {"category": category, "model": model}
        
        # Clear existing specs
        self.clear_specifications()
        
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
        for widget_name, widget in self.specs_widgets.items():
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
                available_voltages = self.product_service.get_available_voltages(db, product_family)
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
                available_materials = self.product_service.get_available_materials_for_product(db, product_family)
                material.addItems([m['display_name'] for m in available_materials])
            finally:
                db.close()
        
        layout.addRow("Material:", material)
        self.specs_widgets["material"] = material
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
    def add_probe_length_section(self):
        """
        Add probe length configuration section to the specifications form.
        
        Creates a group box with probe length options. Only added for
        products that have probes (skipped for emission monitoring products).
        """
        if "Emissions" in self.current_product.get("category", ""):
            return
            
        group = QGroupBox("Probe Length")
        layout = QFormLayout()
        
        probe_length = QSpinBox()
        probe_length.setRange(1, 120)
        probe_length.setValue(12)
        probe_length.setSuffix(" inches")
        layout.addRow("Probe Length:", probe_length)
        self.specs_widgets["probe_length"] = probe_length
        
        group.setLayout(layout)
        self.specs_layout.addWidget(group)
    
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
        npt_size.addItems(["1/2\" NPT", "3/4\" NPT", "1\" NPT", "1.5\" NPT", "2\" NPT"])
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
        
        # Common options for most products
        high_temp = QCheckBox("High Temperature Version")
        layout.addWidget(high_temp)
        self.specs_widgets["high_temp"] = high_temp
        
        # Product-specific options
        if "Level Switch" in self.current_product.get("category", ""):
            extended_probe = QCheckBox("Extended Probe")
            layout.addWidget(extended_probe)
            self.specs_widgets["extended_probe"] = extended_probe
        
        if "Transmitter" in self.current_product.get("category", ""):
            remote_display = QCheckBox("Remote Display Option")
            layout.addWidget(remote_display)
            self.specs_widgets["remote_display"] = remote_display
            
            output_type = QComboBox()
            output_type.addItems(["4-20mA", "0-10V", "Modbus RTU", "HART"])
            layout.addWidget(QLabel("Output Type:"))
            layout.addWidget(output_type)
            self.specs_widgets["output_type"] = output_type
        
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