"""
Spare Parts Tab for the Babbitt Quote Generator.

This module defines the spare parts management interface for the quote generator.
It provides functionality for browsing, filtering, and selecting spare parts
to add to quotes, including:
- Product family and category filtering
- Detailed part information display
- Part selection and quote integration
- Debug information for troubleshooting

The tab integrates with the database to provide real-time access to the
spare parts catalog and maintains consistency with the quote management system.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QGroupBox, QFormLayout, QSpacerItem,
    QSizePolicy, QListWidget, QListWidgetItem, QTreeWidget,
    QTreeWidgetItem, QPushButton, QDialog, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, Signal

from sqlalchemy.orm import Session
from src.core.database import SessionLocal
from src.core.services.spare_part_service import SparePartService
from src.core.models import ProductFamily, SparePart


class SparePartsTab(QWidget):
    """
    Spare parts management tab for the quote generator.
    
    This tab provides a comprehensive interface for managing spare parts,
    including browsing the catalog, filtering parts by various criteria,
    viewing detailed part information, and adding parts to quotes.
    
    The tab maintains a connection to the database for real-time access
    to the spare parts catalog and integrates with the quote management
    system for seamless part addition.
    
    Attributes:
        db (Session): Database session for data access
        spare_part_service (SparePartService): Service for spare part operations
        family_filter (QComboBox): Dropdown for product family filtering
        category_filter (QComboBox): Dropdown for category filtering
        parts_table (QTableWidget): Table displaying spare parts
        part_number_label (QLabel): Label showing selected part number
        part_name_label (QLabel): Label showing selected part name
        part_description_label (QLabel): Label showing part description
        part_price_label (QLabel): Label showing part price
        part_family_label (QLabel): Label showing product family
        part_category_label (QLabel): Label showing part category
        add_to_quote_btn (QPushButton): Button to add part to quote
    
    Signals:
        part_selected (dict): Emitted when a spare part is selected
    """
    
    # Signals
    part_selected = Signal(dict)  # part info dictionary
    
    def __init__(self, parent=None):
        """
        Initialize the SparePartsTab.
        
        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.db = SessionLocal()
        self.spare_part_service = SparePartService()
        self.init_ui()
        
    def init_ui(self):
        """
        Initialize the UI components.
        
        Sets up the tab's layout with sections for:
        1. Filtering controls (product family and category)
        2. Spare parts table
        3. Part details display
        4. Action buttons
        """
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("<h2>Spare Parts</h2>")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Filter section
        filter_layout = QHBoxLayout()
        
        # Product family filter
        self.family_filter = QComboBox()
        self.family_filter.addItem("All Product Families", None)
        self.populate_family_filter()
        filter_layout.addWidget(QLabel("Product Family:"))
        filter_layout.addWidget(self.family_filter)
        
        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories", None)
        self.populate_category_filter()
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_filter)
        
        # Filter buttons
        self.apply_filter_btn = QPushButton("Apply Filter")
        filter_layout.addWidget(self.apply_filter_btn)
        
        self.reset_filter_btn = QPushButton("Reset")
        filter_layout.addWidget(self.reset_filter_btn)
        
        self.debug_btn = QPushButton("Debug Info")
        filter_layout.addWidget(self.debug_btn)
        
        main_layout.addLayout(filter_layout)
        
        # Spare parts table
        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(5)
        self.parts_table.setHorizontalHeaderLabels(["Part Number", "Name", "Category", "Product Family", "Price"])
        self.parts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.parts_table.setSelectionMode(QTableWidget.SingleSelection)
        self.parts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.parts_table)
        
        # Details section
        self.details_group = QGroupBox("Part Details")
        details_layout = QFormLayout()
        
        self.part_number_label = QLabel()
        self.part_name_label = QLabel()
        self.part_description_label = QLabel()
        self.part_price_label = QLabel()
        self.part_family_label = QLabel()
        self.part_category_label = QLabel()
        
        details_layout.addRow("Part Number:", self.part_number_label)
        details_layout.addRow("Name:", self.part_name_label)
        details_layout.addRow("Description:", self.part_description_label)
        details_layout.addRow("Price:", self.part_price_label)
        details_layout.addRow("Product Family:", self.part_family_label)
        details_layout.addRow("Category:", self.part_category_label)
        
        self.details_group.setLayout(details_layout)
        main_layout.addWidget(self.details_group)
        
        # Add to quote button
        self.add_to_quote_btn = QPushButton("Add to Quote")
        self.add_to_quote_btn.setEnabled(False)
        main_layout.addWidget(self.add_to_quote_btn)
        
        # Connect signals
        self.apply_filter_btn.clicked.connect(self.apply_filters)
        self.reset_filter_btn.clicked.connect(self.reset_filters)
        self.parts_table.itemSelectionChanged.connect(self.on_part_selected)
        self.add_to_quote_btn.clicked.connect(self.on_add_to_quote)
        self.debug_btn.clicked.connect(self.show_debug_info)
        
        # Load initial data
        self.load_spare_parts()
    
    def populate_family_filter(self):
        """
        Populate the product family filter dropdown.
        
        Queries the database for all product families and adds them
        to the family filter dropdown.
        """
        families = self.db.query(ProductFamily).all()
        for family in families:
            self.family_filter.addItem(family.name, family.id)
    
    def populate_category_filter(self):
        """
        Populate the category filter dropdown.
        
        Queries the spare part service for all available categories
        and adds them to the category filter dropdown.
        """
        categories = self.spare_part_service.get_spare_part_categories(self.db)
        for category in categories:
            self.category_filter.addItem(category.capitalize(), category)
    
    def load_spare_parts(self):
        """
        Load spare parts into the table.
        
        Queries all spare parts from the database, sorts them by
        product family and part number, and populates the table.
        """
        # Clear existing items
        self.parts_table.setRowCount(0)
        
        # Get all spare parts
        parts = self.spare_part_service.get_all_spare_parts(self.db)

        # Sort by product family name, then part number
        parts = sorted(
            parts,
            key=lambda p: (
                p.product_family.name if p.product_family else '',
                p.part_number or ''
            )
        )
        
        print(f"Loading {len(parts)} spare parts")
        
        # Populate table
        self.parts_table.setRowCount(len(parts))
        for row, part in enumerate(parts):
            family_name = part.product_family.name if part.product_family else ""
            
            # Create table items
            self.parts_table.setItem(row, 0, QTableWidgetItem(part.part_number))
            self.parts_table.setItem(row, 1, QTableWidgetItem(part.name))
            self.parts_table.setItem(row, 2, QTableWidgetItem(part.category.capitalize() if part.category else ""))
            self.parts_table.setItem(row, 3, QTableWidgetItem(family_name))
            self.parts_table.setItem(row, 4, QTableWidgetItem(f"${part.price:.2f}"))
            
            # Store part ID in the first column item
            self.parts_table.item(row, 0).setData(Qt.UserRole, part.id)
    
    def show_debug_info(self):
        """
        Show debug information about spare parts.
        
        Displays a message box with detailed information about spare parts,
        including counts by product family and individual part listings.
        This is useful for troubleshooting database connectivity and
        data consistency issues.
        """
        try:
            # Get counts of spare parts
            all_parts = self.spare_part_service.get_all_spare_parts(self.db)
            
            # Get LS2000 and LS2100 product family IDs
            ls2000 = self.db.query(ProductFamily).filter(ProductFamily.name == "LS2000").first()
            ls2100 = self.db.query(ProductFamily).filter(ProductFamily.name == "LS2100").first()
            
            debug_info = f"Total spare parts: {len(all_parts)}\n\n"
            
            if ls2000:
                ls2000_parts = self.db.query(SparePart).filter(SparePart.product_family_id == ls2000.id).all()
                debug_info += f"LS2000 parts count: {len(ls2000_parts)}\n"
                for part in ls2000_parts:
                    debug_info += f"  - {part.part_number} ({part.name})\n"
            else:
                debug_info += "LS2000 product family not found\n"
            
            if ls2100:
                ls2100_parts = self.db.query(SparePart).filter(SparePart.product_family_id == ls2100.id).all()
                debug_info += f"\nLS2100 parts count: {len(ls2100_parts)}\n"
                for part in ls2100_parts:
                    debug_info += f"  - {part.part_number} ({part.name})\n"
            else:
                debug_info += "\nLS2100 product family not found\n"
            
            QMessageBox.information(self, "Spare Parts Debug Info", debug_info)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error getting debug info: {str(e)}")

    def apply_filters(self):
        """
        Apply selected filters to the spare parts list.
        
        Filters the spare parts table based on the selected product family
        and category filters. Updates the table to show only parts matching
        the selected criteria.
        """
        # Get filter values
        family_id = self.family_filter.currentData()
        category = self.category_filter.currentData()
        
        # Clear existing items
        self.parts_table.setRowCount(0)
        
        # Get filtered parts
        if family_id and category:
            # Both filters applied
            family = self.db.query(ProductFamily).get(family_id)
            if family:
                parts = self.db.query(SparePart).filter(
                    SparePart.product_family_id == family_id,
                    SparePart.category == category
                ).all()
            else:
                parts = []
        elif family_id:
            # Only family filter
            family = self.db.query(ProductFamily).get(family_id)
            if family:
                parts = self.db.query(SparePart).filter(
                    SparePart.product_family_id == family_id
                ).all()
            else:
                parts = []
        elif category:
            # Only category filter
            parts = self.spare_part_service.get_spare_parts_by_category(self.db, category)
        else:
            # No filters
            parts = self.spare_part_service.get_all_spare_parts(self.db)
        
        # Populate table
        self.parts_table.setRowCount(len(parts))
        for row, part in enumerate(parts):
            family_name = part.product_family.name if part.product_family else ""
            
            # Create table items
            self.parts_table.setItem(row, 0, QTableWidgetItem(part.part_number))
            self.parts_table.setItem(row, 1, QTableWidgetItem(part.name))
            self.parts_table.setItem(row, 2, QTableWidgetItem(part.category.capitalize() if part.category else ""))
            self.parts_table.setItem(row, 3, QTableWidgetItem(family_name))
            self.parts_table.setItem(row, 4, QTableWidgetItem(f"${part.price:.2f}"))
            
            # Store part ID in the first column item
            self.parts_table.item(row, 0).setData(Qt.UserRole, part.id)
    
    def reset_filters(self):
        """Reset all filters and reload parts."""
        self.family_filter.setCurrentIndex(0)
        self.category_filter.setCurrentIndex(0)
        self.load_spare_parts()
    
    def on_part_selected(self):
        """Handle part selection in the table."""
        # Get selected row
        selected_items = self.parts_table.selectedItems()
        if not selected_items:
            self.clear_details()
            self.add_to_quote_btn.setEnabled(False)
            return
        
        # Get part ID from the first column
        row = selected_items[0].row()
        part_id = self.parts_table.item(row, 0).data(Qt.UserRole)
        
        # Get part details
        part = self.db.query(SparePart).get(part_id)
        if not part:
            self.clear_details()
            self.add_to_quote_btn.setEnabled(False)
            return
        
        # Update details section
        self.part_number_label.setText(part.part_number)
        self.part_name_label.setText(part.name)
        self.part_description_label.setText(part.description or "")
        self.part_price_label.setText(f"${part.price:.2f}")
        
        if part.product_family:
            self.part_family_label.setText(part.product_family.name)
        else:
            self.part_family_label.setText("N/A")
            
        self.part_category_label.setText(part.category.capitalize() if part.category else "N/A")
        
        # Enable add to quote button
        self.add_to_quote_btn.setEnabled(True)
    
    def clear_details(self):
        """Clear the details section."""
        self.part_number_label.setText("")
        self.part_name_label.setText("")
        self.part_description_label.setText("")
        self.part_price_label.setText("")
        self.part_family_label.setText("")
        self.part_category_label.setText("")
    
    def on_add_to_quote(self):
        """Add selected part to the quote."""
        # Get selected row
        selected_items = self.parts_table.selectedItems()
        if not selected_items:
            return
        
        # Get part ID from the first column
        row = selected_items[0].row()
        part_id = self.parts_table.item(row, 0).data(Qt.UserRole)
        
        # Get part details
        part = self.db.query(SparePart).get(part_id)
        if not part:
            return
            
        # Create part info dictionary
        part_info = {
            "type": "spare_part",
            "id": part.id,
            "part_number": part.part_number,
            "name": part.name,
            "description": part.description,
            "price": part.price,
            "category": part.category,
            "product_family": part.product_family.name if part.product_family else ""
        }
        
        # Emit signal with part info
        self.part_selected.emit(part_info)
    
    def closeEvent(self, event):
        """Close database connection when widget is closed."""
        self.db.close()
        super().closeEvent(event) 