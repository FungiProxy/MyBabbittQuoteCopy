"""
Main window module for the Babbitt Quote Generator application.

This module defines the main application window and its core functionality. It includes:
- Tab-based interface for product selection, specifications, quotes, and spare parts
- Navigation controls between tabs
- Quote management (save and export)
- Signal handling for inter-tab communication

The main window serves as the central hub for all quote generation activities,
coordinating between different tabs and managing the overall application state.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTabWidget, QMessageBox, QFileDialog,
    QFrame, QStackedWidget, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Slot, QTimer, QSize
from PySide6.QtGui import QIcon # Added for icons
from src.ui.quote_creation import QuoteCreationPage

# Remove old tab imports if they are not immediately used as stacked widgets
# from src.ui.product_tab import ProductTab
# from src.ui.specifications_tab import SpecificationsTab
# from src.ui.quote_tab import QuoteTab
# from src.ui.spare_parts_tab import SparePartsTab

class MainWindow(QMainWindow):
    """
    Main application window for the Babbitt Quote Generator.
    This window features a sidebar for navigation and a main content area.
    """
    
    def __init__(self):
        """Initialize the main window and set up the UI components."""
        super().__init__()
        self.setWindowTitle("Babbitt") # Changed window title
        self.resize(1200, 800) # Adjusted initial size
        
        print("MainWindow.__init__() called")
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # Main horizontal layout: sidebar | content_area
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0) # No margins for the main layout
        self.main_layout.setSpacing(0) # No spacing between sidebar and content

        self._create_sidebar()
        self._create_content_area()
        
        # Add sidebar and content area to the main layout
        self.main_layout.addWidget(self.sidebar_frame, 1) # Sidebar takes 1 part of stretch
        self.main_layout.addWidget(self.content_area_frame, 4) # Content area takes 4 parts

        # Example: Initially show Dashboard content
        self._show_dashboard_content()

        # Connect signals for sidebar navigation
        self._connect_sidebar_signals()
        
        print("MainWindow initialization complete")

    def _create_sidebar(self):
        """Creates the sidebar navigation panel."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        self.sidebar_frame.setFixedWidth(220)
        # self.sidebar_frame.setStyleSheet("background-color: #f0f0f0;") # Basic styling

        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(10)

        # Babbitt Title/Logo (Placeholder)
        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        # self.logo_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.sidebar_layout.addWidget(self.logo_label)

        # Navigation List/Buttons
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        # self.nav_list.setStyleSheet("QListWidget { border: none; font-size: 16px; } QListWidget::item { padding: 10px; } QListWidget::item:selected { background-color: #e0e0e0; color: black; }")
        
        nav_items = [
            ("Dashboard", "dashboard_icon.png"), # Placeholder icon names
            ("Quote Creation", "quote_icon.png")
        ]

        for item_text, icon_path in nav_items:
            list_item = QListWidgetItem(item_text) # Ideally QListWidgetItem(QIcon(icon_path), item_text)
            # For now, no actual icons, just text
            self.nav_list.addItem(list_item)
        
        self.nav_list.setCurrentRow(0) # Default to Dashboard
        self.sidebar_layout.addWidget(self.nav_list)

        self.sidebar_layout.addStretch() # Pushes settings to the bottom

        # Settings Button
        self.settings_button = QPushButton("Settings") # Ideally QPushButton(QIcon("settings_icon.png"), " Settings")
        self.settings_button.setObjectName("settingsButton")
        # self.settings_button.setStyleSheet("QPushButton { text-align: left; padding: 10px; font-size: 16px; border: none; } QPushButton:hover { background-color: #e0e0e0; }")
        self.sidebar_layout.addWidget(self.settings_button)

    def _create_content_area(self):
        """Creates the main content area where different views will be displayed."""
        self.content_area_frame = QFrame()
        self.content_area_frame.setObjectName("contentAreaFrame")
        # self.content_area_frame.setStyleSheet("background-color: #ffffff;")

        self.content_layout = QVBoxLayout(self.content_area_frame)
        self.content_layout.setContentsMargins(0,0,0,0) # Content fills frame
        self.content_layout.setSpacing(0)

        # Header for the content area
        self._create_content_header()
        self.content_layout.addWidget(self.content_header_frame)

        # StackedWidget to switch between different content views
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)

        # Create and add pages to stacked_widget (initially just dashboard placeholder)
        self.dashboard_page = QWidget() # This will be fleshed out
        self.stacked_widget.addWidget(self.dashboard_page)
        self.quote_creation_page = QuoteCreationPage()
        self.stacked_widget.addWidget(self.quote_creation_page)
        self.settings_page = QLabel("Settings Content (Placeholder)") # For settings button
        self.settings_page.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(self.settings_page)
        
    def _create_content_header(self):
        """Creates the header part of the content area."""
        self.content_header_frame = QFrame()
        self.content_header_frame.setObjectName("contentHeaderFrame")
        self.content_header_frame.setFixedHeight(60)
        # self.content_header_frame.setStyleSheet("background-color: #f8f9fa; border-bottom: 1px solid #dee2e6;")

        header_layout = QHBoxLayout(self.content_header_frame)
        header_layout.setContentsMargins(20, 0, 20, 0)

        self.current_view_title = QLabel("Dashboard") # This will change based on selected view
        self.current_view_title.setObjectName("currentViewTitle")
        # self.current_view_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(self.current_view_title)

        header_layout.addStretch()

        # Placeholder for Bell Icon
        self.bell_button = QPushButton("🔔") # Placeholder for icon
        self.bell_button.setFixedSize(30,30)
        self.bell_button.setObjectName("iconButton")
        header_layout.addWidget(self.bell_button)
        
        # Placeholder for User Profile
        self.user_profile_button = QPushButton("👤 John Smith") # Placeholder
        self.user_profile_button.setObjectName("userProfileButton")
        # self.user_profile_button.setStyleSheet("padding: 5px; margin-left:10px; border:none;")
        header_layout.addWidget(self.user_profile_button)
        
        # New Quote Button
        self.new_quote_button_header = QPushButton("+ New Quote")
        self.new_quote_button_header.setObjectName("newQuoteButtonHeader")
        # self.new_quote_button_header.setStyleSheet("background-color: #007bff; color: white; padding: 8px 15px; border-radius: 5px; margin-left: 15px;")
        header_layout.addWidget(self.new_quote_button_header)
        
    def _show_dashboard_content(self):
        """Populates the dashboard_page with content resembling the image."""
        self.current_view_title.setText("Dashboard")
        self.stacked_widget.setCurrentWidget(self.dashboard_page)

        # Layout for the dashboard page
        dashboard_layout = QVBoxLayout(self.dashboard_page)
        dashboard_layout.setContentsMargins(20,20,20,20)
        dashboard_layout.setSpacing(20)

        # Top section with Overview/Analytics/Reports tabs (simplified as buttons for now)
        dashboard_tabs_layout = QHBoxLayout()
        self.overview_button = QPushButton("Overview")
        self.overview_button.setObjectName("dashboardTabButtonSelected") # Selected by default
        self.analytics_button = QPushButton("Analytics")
        self.analytics_button.setObjectName("dashboardTabButton")
        self.reports_button_dash = QPushButton("Reports") # Renamed to avoid clash
        self.reports_button_dash.setObjectName("dashboardTabButton")
        
        dashboard_tabs_layout.addWidget(self.overview_button)
        dashboard_tabs_layout.addWidget(self.analytics_button)
        dashboard_tabs_layout.addWidget(self.reports_button_dash)
        dashboard_tabs_layout.addStretch()
        dashboard_layout.addLayout(dashboard_tabs_layout)

        # Stats cards section
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Card 1: Total Quotes
        card1 = self._create_stat_card("Total Quotes", "127", "+5.2% from last month", "📄")
        # Card 2: Quote Value
        card2 = self._create_stat_card("Quote Value", "$45,231.89", "+20.1% from last month", "$")
        # Card 3: Customers
        card3 = self._create_stat_card("Customers", "42", "+10.5% from last month", "👥")
        # Card 4: Products
        card4 = self._create_stat_card("Products", "89", "+3 new products added", "📦")
        
        stats_layout.addWidget(card1)
        stats_layout.addWidget(card2)
        stats_layout.addWidget(card3)
        stats_layout.addWidget(card4)
        dashboard_layout.addLayout(stats_layout)

        # Main content section (Recent Quotes | Sales by Product Category)
        main_dashboard_content_layout = QHBoxLayout()
        main_dashboard_content_layout.setSpacing(20)

        # Recent Quotes section
        recent_quotes_frame = QFrame()
        recent_quotes_frame.setObjectName("dashboardSectionFrame")
        recent_quotes_layout = QVBoxLayout(recent_quotes_frame)
        recent_quotes_title = QLabel("Recent Quotes")
        recent_quotes_title.setObjectName("sectionTitle")
        recent_quotes_layout.addWidget(recent_quotes_title)
        # Add placeholder items for recent quotes
        for i in range(2): # As per image
            quote_item_layout = QHBoxLayout()
            quote_id_customer = QLabel(f"Quote #202310{i+1}\\nAcme Corporation")
            quote_value_date = QLabel(f"${120.00 + i*1350:.2f}\\n5/13/2025")
            quote_value_date.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            quote_item_layout.addWidget(quote_id_customer)
            quote_item_layout.addStretch()
            quote_item_layout.addWidget(quote_value_date)
            recent_quotes_layout.addLayout(quote_item_layout)
            if i < 1: # Add a separator line, not after the last one
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                recent_quotes_layout.addWidget(line)
        recent_quotes_layout.addStretch()
        main_dashboard_content_layout.addWidget(recent_quotes_frame, 2) # Takes 2 parts of stretch

        # Sales by Product Category section
        sales_category_frame = QFrame()
        sales_category_frame.setObjectName("dashboardSectionFrame")
        sales_category_layout = QVBoxLayout(sales_category_frame)
        sales_category_title = QLabel("Sales by Product Category")
        sales_category_title.setObjectName("sectionTitle")
        sales_category_layout.addWidget(sales_category_title)
        # Add placeholder items for sales by category
        categories = [
            ("Level Switches", "45%"),
            ("Flow Switches", "30%"),
            ("Transmitters", "15%"),
            ("Spare Parts", "10%")
        ]
        for cat_name, cat_value in categories:
            cat_item_layout = QHBoxLayout()
            # Placeholder for colored dot + Name
            cat_label = QLabel(f"• {cat_name}") # Simple dot for now
            cat_percent = QLabel(cat_value)
            cat_percent.setAlignment(Qt.AlignRight)
            cat_item_layout.addWidget(cat_label)
            cat_item_layout.addWidget(cat_percent)
            sales_category_layout.addLayout(cat_item_layout)
        sales_category_layout.addStretch()
        main_dashboard_content_layout.addWidget(sales_category_frame, 1) # Takes 1 part of stretch
        
        dashboard_layout.addLayout(main_dashboard_content_layout)
        dashboard_layout.addStretch() # Pushes content up

        # Footer
        footer_layout = QHBoxLayout()
        footer_label_left = QLabel("Babbitt International Inc.")
        footer_label_right = QLabel("© 2025 All rights reserved")
        footer_layout.addWidget(footer_label_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_label_right)
        dashboard_layout.addLayout(footer_layout)


    def _create_stat_card(self, title_text, value_text, sub_text, icon_text=""):
        """Helper function to create a statistics card widget."""
        card_frame = QFrame()
        card_frame.setObjectName("statCard")
        # card_frame.setStyleSheet("QFrame#statCard { border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; background-color: white; }")
        card_layout = QVBoxLayout(card_frame)

        title_icon_layout = QHBoxLayout()
        title_label = QLabel(title_text)
        title_label.setObjectName("statCardTitle")
        # title_label.setStyleSheet("font-size: 14px; color: #555;")
        title_icon_layout.addWidget(title_label)
        title_icon_layout.addStretch()
        if icon_text:
            icon_label = QLabel(icon_text)
            icon_label.setObjectName("statCardIcon")
            # icon_label.setStyleSheet("font-size: 18px;") # Adjust as needed
            title_icon_layout.addWidget(icon_label)
        card_layout.addLayout(title_icon_layout)
        
        value_label = QLabel(value_text)
        value_label.setObjectName("statCardValue")
        # value_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-top: 5px; margin-bottom: 5px;")
        card_layout.addWidget(value_label)
        
        sub_label = QLabel(sub_text)
        sub_label.setObjectName("statCardSubText")
        # sub_label.setStyleSheet("font-size: 12px; color: #777;")
        card_layout.addWidget(sub_label)
        
        return card_frame

    def _connect_sidebar_signals(self):
        """Connect signals for sidebar navigation items."""
        self.nav_list.currentRowChanged.connect(self.on_nav_item_selected)
        self.settings_button.clicked.connect(self.on_settings_selected)

    @Slot(int)
    def on_nav_item_selected(self, index):
        """Handle sidebar navigation item selection."""
        # Titles correspond to the order in nav_items
        view_titles = ["Dashboard", "Quote Creation"]
        if 0 <= index < len(view_titles):
            self.current_view_title.setText(view_titles[index])
            self.stacked_widget.setCurrentIndex(index)
            if view_titles[index] == "Dashboard":
                self._show_dashboard_content() # Re-populate if needed or ensure it's up-to-date
            # Add logic here to populate other views if necessary when they are selected
        print(f"Navigation item selected: Index {index}, Title: {self.current_view_title.text()}")

    @Slot()
    def on_settings_selected(self):
        """Handle settings button click."""
        self.current_view_title.setText("Settings")
        self.stacked_widget.setCurrentWidget(self.settings_page) # Assuming settings_page is at index 3
        print("Settings selected")

    def showEvent(self, event):
        """Called when the window is shown."""
        super().showEvent(event)
        print(f"Window shown: Geometry = {self.geometry().x()}, {self.geometry().y()}, {self.geometry().width()}, {self.geometry().height()}")
        print(f"Window visible: {self.isVisible()}")
        print(f"Window active: {self.isActiveWindow()}")
    
    def check_window_state(self):
        """Check the window state and print debug info."""
        # Reduced frequency and print only if count is low to avoid too much console noise
        if self.check_count < 3: # Check only a few times
            print(f"Window check ({self.check_count}): Visible={self.isVisible()}, Active={self.isActiveWindow()}, Minimized={self.isMinimized()}")
        self.check_count += 1
        if self.check_count > 5: # Stop after a few checks
            self.check_timer.stop()
            print("Window check timer stopped.")
            
    def _connect_signals(self):
        """
        Connect all signal handlers for the main window.
        This method will need to be updated or removed if tab signals are no longer relevant.
        For now, we keep it and connect sidebar signals separately.
        """
        # Comment out or remove old tab-specific signals if ProductTab etc. are not used in this structure
        # self.product_tab.product_selected.connect(self.on_product_selected)
        # self.specifications_tab.specs_updated.connect(self.on_specs_updated)
        # self.specifications_tab.add_to_quote.connect(self.on_specs_add_to_quote)
        # self.spare_parts_tab.part_selected.connect(self.on_spare_part_selected)
        
        # Old button signals - these buttons are removed or repurposed
        # self.next_button.clicked.connect(self.next_tab)
        # self.prev_button.clicked.connect(self.prev_tab)
        # self.save_button.clicked.connect(self.save_quote)
        # self.export_button.clicked.connect(self.export_quote)
        # self.tabs.currentChanged.connect(self.on_tab_changed)
        pass # Replaced by _connect_sidebar_signals and specific content signals

    @Slot(str)
    def on_product_selected(self, model):
        """
        Handle product selection events.
        
        Updates the specifications and quote tabs with the newly selected product
        information.
        
        Args:
            model (str): The model number/identifier of the selected product
        """
        print(f"Product selected: {model}")
        # Get full product info including derived category
        product_info = self.product_tab.get_selected_product()
        category = product_info["category"]
        
        # Update specifications tab with product info
        self.specifications_tab.update_for_product(category, model)
        
        # Update quote tab with product info
        self.quote_tab.update_product_info(product_info)
    
    def on_specs_updated(self, specs):
        """
        Handle specification update events.
        
        Updates the quote tab with the modified specifications.
        
        Args:
            specs (dict): Dictionary containing the updated specifications
        """
        print("Specifications updated")
        # Update quote tab with specifications
        self.quote_tab.update_specifications(specs)
    
    def update_button_states(self):
        """
        Update the enabled/disabled state of navigation buttons.
        This is no longer needed for previous/next tab buttons.
        Could be repurposed if other buttons need state management.
        """
        # current_index = self.tabs.currentIndex()
        # self.prev_button.setEnabled(current_index > 0)
        # self.next_button.setEnabled(current_index < self.tabs.count() - 1)
        pass

    def on_tab_changed(self, index):
        """
        Handle tab change events.
        This is no longer needed as QTabWidget is removed.
        """
        # print(f"Tab changed to: {index}")
        # self.update_button_states()
        pass
    
    @Slot()
    def next_tab(self):
        """Navigate to the next tab if available."""
        # This logic is now handled by sidebar navigation
        pass
    
    @Slot()
    def prev_tab(self):
        """Navigate to the previous tab if available."""
        # This logic is now handled by sidebar navigation
        pass

    @Slot()
    def save_quote(self):
        """
        Save the current quote.
        
        Validates that a product is selected and saves the quote data.
        Currently shows a success message; in production, this would
        save to a database.
        
        Raises:
            QMessageBox: Warning if no product is selected
        """
        print("Save quote action triggered")
        # Get quote data
        quote_data = self.quote_tab.get_quote_data()
        
        # Check if product is selected
        if not quote_data['product'].get('model'):
            QMessageBox.warning(self, "Missing Product", 
                "Please select a product before saving the quote.")
            return
        
        # In the full implementation, this would save to your database
        # For now, we'll just show a success message
        customer_name = quote_data['customer'].get('name', 'Customer')
        product_model = quote_data['product'].get('model', 'Unknown')
        
        QMessageBox.information(self, "Quote Saved", 
            f"Quote for {customer_name} for {product_model} has been saved.")
    
    def setup_styles(self):
        """Apply custom styles to the main window and its components."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa; /* Light grey background for the whole window */
            }
            QFrame#sidebarFrame {
                background-color: #ffffff; /* White sidebar */
                border-right: 1px solid #dee2e6; /* Light border separating sidebar */
            }
            QLabel#logoLabel {
                font-size: 22px; 
                font-weight: bold; 
                margin-bottom: 15px;
                padding: 10px;
                color: #333;
            }
            QListWidget#navList {
                border: none; 
                font-size: 14px; 
            }
            QListWidget#navList::item {
                padding: 12px 15px;
                border-radius: 5px; /* Rounded corners for items */
            }
            QListWidget#navList::item:hover {
                background-color: #f0f0f0; /* Light hover for items */
            }
            QListWidget#navList::item:selected {
                background-color: #e0e7ff; /* Light blue for selected item */
                color: #0033cc; /* Darker blue text for selected item */
                font-weight: bold;
            }
            QPushButton#settingsButton {
                text-align: left; 
                padding: 12px 15px; 
                font-size: 14px; 
                border: none;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton#settingsButton:hover {
                background-color: #f0f0f0;
            }

            QFrame#contentAreaFrame {
                background-color: #f8f9fa; /* Light background for content */
            }
            
            QFrame#contentHeaderFrame {
                background-color: #ffffff; /* White header bar */
                border-bottom: 1px solid #dee2e6;
            }
            QLabel#currentViewTitle {
                font-size: 18px; 
                font-weight: bold;
                color: #343a40;
            }
            QPushButton#iconButton, QPushButton#userProfileButton {
                border: none;
                font-size: 14px; /* Adjusted for icon buttons */
                color: #555;
                padding: 5px;
            }
             QPushButton#iconButton:hover, QPushButton#userProfileButton:hover {
                color: #000;
            }
            QPushButton#userProfileButton {
                 margin-left: 5px;
            }
            QPushButton#newQuoteButtonHeader {
                background-color: #007bff; 
                color: white; 
                padding: 8px 12px; 
                border-radius: 4px; 
                margin-left: 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#newQuoteButtonHeader:hover {
                background-color: #0056b3;
            }

            /* Dashboard specific styles */
            QPushButton#dashboardTabButton, QPushButton#dashboardTabButtonSelected {
                padding: 8px 15px;
                font-size: 14px;
                border: none;
                background-color: transparent;
                margin-right: 5px;
                color: #495057;
            }
            QPushButton#dashboardTabButton:hover {
                color: #007bff;
                background-color: #e9ecef;
                border-radius: 4px;
            }
            QPushButton#dashboardTabButtonSelected {
                font-weight: bold;
                color: #007bff;
                border-bottom: 2px solid #007bff; /* Underline for selected tab */
            }

            QFrame#statCard {
                border: 1px solid #e9ecef; 
                border-radius: 6px; 
                padding: 18px; 
                background-color: white; 
            }
            QLabel#statCardTitle {
                font-size: 13px; 
                color: #6c757d; 
                font-weight: 500; /* Medium weight */
            }
            QLabel#statCardIcon {
                font-size: 18px; 
                color: #6c757d;
            }
            QLabel#statCardValue {
                font-size: 24px; /* Slightly smaller */
                font-weight: bold; 
                margin-top: 6px; 
                margin-bottom: 6px;
                color: #212529; /* Darker text */
            }
            QLabel#statCardSubText {
                font-size: 11px; 
                color: #6c757d;
            }

            QFrame#dashboardSectionFrame {
                 background-color: white;
                 border: 1px solid #e9ecef;
                 border-radius: 6px;
                 padding: 18px;
            }
            QLabel#sectionTitle {
                font-size: 15px; /* Slightly smaller */
                font-weight: bold;
                color: #343a40;
                margin-bottom: 12px;
            }
        """)
        print("Styles setup complete.")