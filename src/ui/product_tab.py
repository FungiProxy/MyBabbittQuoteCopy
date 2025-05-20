"""
Product Selection Tab for the Babbitt Quote Generator.

This module defines the product selection interface for the quote generator.
It provides a user-friendly way to browse and select products from the
Babbitt International catalog, including:
- Model selection via dropdown
- Detailed product information display
- Category-based organization
- Signal emission for product selection events
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QGroupBox, QFormLayout, QSpacerItem,
    QSizePolicy, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Signal


class ProductTab(QWidget):
    """
    Product selection tab for the quote generator.
    
    This tab allows users to select products from the Babbitt International catalog
    and view detailed information about each product. It maintains a list of available
    models and their descriptions, and emits signals when selections are made.
    
    The tab is organized into two main sections:
    1. Model Selection: Dropdown for choosing the product model
    2. Product Information: Detailed display of the selected product's features
    
    Attributes:
        product_model (QComboBox): Dropdown for model selection
        product_info_label (QLabel): Label for displaying product details
        models (dict): Dictionary mapping model numbers to descriptions
        model_group (QGroupBox): Container for model selection
        info_group (QGroupBox): Container for product information
    
    Signals:
        product_selected (str): Emitted when a product is selected, carries model number
    """
    
    # Signals
    product_selected = Signal(str)  # model
    
    def __init__(self, parent=None):
        """
        Initialize the ProductTab.
        
        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.init_ui()
        
        # Connect signals
        self.product_model.currentIndexChanged.connect(self.on_model_changed)
        
    def init_ui(self):
        """
        Initialize the UI components.
        
        Sets up the tab's layout and widgets, including:
        - Model selection dropdown
        - Product information display
        - Layout management and spacing
        """
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Product model selection
        self.model_group = QGroupBox("Model Selection")
        model_layout = QFormLayout()
        
        self.product_model = QComboBox()
        
        # Add available models with their descriptions
        self.models = {
            "LS2000": "RF Admittance Level Switch - General Purpose",
            "LS2100": "Loop Powered Level Switch",
            "LS6000": "RF Admittance Level Switch - Heavy Duty",
            "LS7000": "RF Admittance Level Switch - Advanced Features",
            "LS7000/2": "Dual Point Level Switch",
            "LS8000": "Remote Mounted Level Switch",
            "LS8000/2": "Remote Mounted Dual Point Level Switch",
            "LT9000": "Level Transmitter",
            "FS10000": "Flow Switch"
        }
        
        for model, description in self.models.items():
            self.product_model.addItem(f"{model} - {description}", model)
        
        model_layout.addRow("Select Model:", self.product_model)
        self.model_group.setLayout(model_layout)
        
        # Add to main layout
        main_layout.addWidget(self.model_group)
        
        # Add product info section
        self.info_group = QGroupBox("Product Information")
        info_layout = QVBoxLayout()
        self.product_info_label = QLabel("Select a product to view details")
        info_layout.addWidget(self.product_info_label)
        self.info_group.setLayout(info_layout)
        
        main_layout.addWidget(self.info_group)
        
        # Add a spacer at the bottom to push everything up
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def on_model_changed(self, index):
        """
        Handle model selection changes.
        
        Updates the product information display and emits a signal when
        a new model is selected.
        
        Args:
            index (int): Index of the newly selected item in the combo box
        """
        if index >= 0:
            model = self.product_model.currentData()  # Get the model number from the combobox data
            
            # Update product info
            self.update_product_info(model)
            
            # Emit signal with selected product
            self.product_selected.emit(model)
    
    def update_product_info(self, model):
        """
        Update the product information section.
        
        Updates the information display with detailed features and specifications
        for the selected model.
        
        Args:
            model (str): Model number to display information for
        """
        info_text = f"<h3>{model}</h3>"
        
        # Add model-specific info
        model_info = {
            "LS2000": """
                <p>General Purpose RF Admittance Level Switch</p>
                <ul>
                    <li>Available in 115VAC or 24VDC</li>
                    <li>Standard 10" probe length (S, H materials)</li>
                    <li>Standard 4" probe length (U, T materials)</li>
                    <li>Not recommended for plastic pellets without extra static protection</li>
                </ul>
            """,
            "LS2100": """
                <p>Loop Powered Level Switch</p>
                <ul>
                    <li>24VDC Loop Powered (16-32VDC)</li>
                    <li>Standard 10" probe length</li>
                    <li>8mA to 16mA operation</li>
                </ul>
            """,
            "LS6000": """
                <p>Heavy Duty RF Admittance Level Switch</p>
                <ul>
                    <li>Available in 12VDC, 24VDC, 115VAC, or 240VAC</li>
                    <li>Standard 10" probe length</li>
                    <li>Optional 3/4" diameter probe</li>
                    <li>Higher temperature options available</li>
                </ul>
            """,
            "LS7000": """
                <p>Advanced Features RF Admittance Level Switch</p>
                <ul>
                    <li>Available in 12VDC, 24VDC, 115VAC, or 240VAC</li>
                    <li>Built-in timer for pump control</li>
                    <li>Optional stainless steel housing</li>
                    <li>Higher temperature options available</li>
                </ul>
            """,
            "LS7000/2": """
                <p>Dual Point Level Switch</p>
                <ul>
                    <li>Available in 12VDC, 24VDC, 115VAC, or 240VAC</li>
                    <li>Designed for auto-fill or auto-empty applications</li>
                    <li>Requires Halar coating for conductive liquids</li>
                    <li>Not suitable for dry materials</li>
                </ul>
            """,
            "LS8000": """
                <p>Remote Mounted Level Switch</p>
                <ul>
                    <li>Available in 12VDC, 24VDC, 115VAC, or 240VAC</li>
                    <li>Electronics can be mounted away from probe</li>
                    <li>Standard 10" probe length</li>
                    <li>Multiple transmitter sensitivities available</li>
                </ul>
            """,
            "LS8000/2": """
                <p>Remote Mounted Dual Point Level Switch</p>
                <ul>
                    <li>Available in 12VDC, 24VDC, 115VAC, or 240VAC</li>
                    <li>Can get 4 set points with two receiver cards</li>
                    <li>Designed for homogeneous liquids</li>
                    <li>Requires proper grounding for best performance</li>
                </ul>
            """,
            "LT9000": """
                <p>Level Transmitter</p>
                <ul>
                    <li>Available in 24VDC and 230VAC</li>
                    <li>Designed for electrically conductive liquids</li>
                    <li>Standard 10" probe length</li>
                    <li>Requires proper grounding for operation</li>
                </ul>
            """,
            "FS10000": """
                <p>Flow Switch</p>
                <ul>
                    <li>Available in 24VDC and 115VAC</li>
                    <li>Standard 6" insertion length</li>
                    <li>Designed for flow detection in pipes</li>
                    <li>Adjustable sensitivity for different flow rates</li>
                </ul>
            """
        }
        
        info_text += model_info.get(model, "<p>No detailed information available for this model.</p>")
        self.product_info_label.setText(info_text)
    
    def get_selected_product(self):
        """
        Get the currently selected product information.
        
        Returns a dictionary containing information about the currently
        selected product, including its model number, description,
        and category.
        
        Returns:
            dict: Product information with keys:
                - model (str): Model number
                - description (str): Product description
                - category (str): Product category
        """
        model = self.product_model.currentData()  # Get the model number
        
        # Map model to category
        category_map = {
            "LS2000": "Level Switch",
            "LS2100": "Level Switch",
            "LS6000": "Level Switch",
            "LS7000": "Level Switch",
            "LS7000/2": "Level Switch",
            "LS8000": "Level Switch",
            "LS8000/2": "Level Switch",
            "LT9000": "Level Transmitter",
            "FS10000": "Flow Switch"
        }
        
        return {
            "model": model,
            "description": self.models.get(model, ""),
            "category": category_map.get(model, "Unknown")
        }
        
    def connect_service(self, product_service):
        """
        Connect this tab to the product service.
        
        Sets up the connection to the product service for fetching
        real product data. Currently a placeholder for future implementation.
        
        Args:
            product_service: Service class for product data access
        """
        # This would be implemented to fetch real data from your service
        pass 