"""
Simplified Main Window for MyBabbittQuote Application

Clean, focused main window that prioritizes the core quoting workflow.
Removes analytics complexity and focuses on Quote Creation, Customers, and Settings.

File: src/ui/views/main_window.py (REPLACE EXISTING)
"""

import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.views.customers_page import CustomersPage
from src.ui.views.quote_creation import QuoteCreationPage
from src.ui.views.settings_page import SettingsPage
from src.ui.views.dashboard_enhanced import ProfessionalDashboard
from src.ui.utils.ui_enhancer import enhance_current_ui

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Simplified main window focusing on core business functions:
    - Quote Creation (primary workflow)
    - Customer Management
    - Settings
    
    Beautiful, professional styling with Babbitt International branding.
    """

    def __init__(self):
        """Initialize the main window with simplified navigation."""
        super().__init__()
        self.setWindowTitle("MyBabbittQuote - Babbitt International")
        self.resize(1400, 900)
        self.setMinimumSize(1200, 700)
        
        # Apply Babbitt theme immediately
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        
        self._setup_ui()
        self._connect_signals()
        
        # Start with Dashboard (the overview page)
        self._show_dashboard()
        
        # Add UI enhancement system
        enhance_current_ui(self)
        
        logger.info("MainWindow initialized with simplified navigation")

    def _setup_ui(self):
        """Set up the main UI layout."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create components
        self._create_sidebar()
        self._create_content_area()
        
        # Add to layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_frame, 1)

    def _create_sidebar(self):
        """Create the beautiful blue gradient sidebar."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo
        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(self.logo_label)
        
        # Navigation list - SIMPLIFIED for launch
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        # Core navigation items only (no analytics/reports)
        nav_items = [
            "📊 Dashboard",        # Dashboard overview
            "🚀 Quote Creation",   # Primary workflow
            "👥 Customers",       # Essential for quotes
            "📦 Product Catalog", # Will add later
        ]
        
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            self.nav_list.addItem(item)
        
        # Set Quote Creation as default
        self.nav_list.setCurrentRow(0)
        sidebar_layout.addWidget(self.nav_list)
        
        # Spacer to push settings to bottom
        sidebar_layout.addStretch()
        
        # Settings at bottom
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setObjectName("settingsButton")
        sidebar_layout.addWidget(self.settings_button)

    def _create_content_area(self):
        """Create the main content area."""
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentAreaFrame")
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Content header
        self._create_content_header()
        content_layout.addWidget(self.header_frame)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Initialize pages
        self._create_pages()

    def _create_content_header(self):
        """Create the content area header with orange accent button."""
        self.header_frame = QFrame()
        self.header_frame.setObjectName("contentHeader")
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        # Page title
        self.page_title = QLabel("Quote Creation")
        self.page_title.setObjectName("pageTitle")
        header_layout.addWidget(self.page_title)
        
        # Spacer
        header_layout.addStretch()
        
        # Quick action button with Babbitt orange
        self.quick_action_button = QPushButton("+ New Quote")
        self.quick_action_button.setProperty("class", "primary")
        header_layout.addWidget(self.quick_action_button)

    def _create_pages(self):
        """Create and add all pages to the stacked widget."""
        # Dashboard Page (Index 0)
        self.dashboard_page = ProfessionalDashboard()
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Quote Creation Page (Index 1)
        self.quote_creation_page = QuoteCreationPage()
        self.stacked_widget.addWidget(self.quote_creation_page)
        
        # Customers Page (Index 2) 
        self.customers_page = CustomersPage()
        self.stacked_widget.addWidget(self.customers_page)
        
        # Product Catalog Placeholder (Index 3)
        # We'll add this later - for now just a placeholder
        self.catalog_placeholder = QWidget()
        placeholder_layout = QVBoxLayout(self.catalog_placeholder)
        placeholder_label = QLabel("Product Catalog - Coming Soon")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_layout.addWidget(placeholder_label)
        self.stacked_widget.addWidget(self.catalog_placeholder)
        
        # Settings Page
        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.settings_page)
        
        # Connect settings theme changes
        if hasattr(self.settings_page, 'theme_changed'):
            self.settings_page.theme_changed.connect(self.apply_theme)

    def _connect_signals(self):
        """Connect navigation signals."""
        self.nav_list.currentRowChanged.connect(self._on_nav_item_selected)
        self.settings_button.clicked.connect(self._show_settings)
        self.quick_action_button.clicked.connect(self._on_quick_action)

    @Slot(int)
    def _on_nav_item_selected(self, index):
        """Handle navigation item selection."""
        if index == 0:  # Dashboard
            self._show_dashboard()
        elif index == 1:  # Quote Creation
            self._show_quote_creation()
        elif index == 2:  # Customers
            self._show_customers()
        elif index == 3:  # Product Catalog
            self._show_catalog_placeholder()

    def _show_dashboard(self):
        """Show the enhanced dashboard page."""
        self.stacked_widget.setCurrentWidget(self.dashboard_page)
        self.page_title.setText("Dashboard")
        self.quick_action_button.setText("+ New Quote")
        self.quick_action_button.show()
        
        # Refresh dashboard data when shown
        if hasattr(self.dashboard_page, 'refresh_data'):
            self.dashboard_page.refresh_data()

    def _show_quote_creation(self):
        """Show the quote creation page."""
        self.stacked_widget.setCurrentIndex(1)
        self.page_title.setText("Quote Creation")
        self.quick_action_button.setText("+ New Quote")
        self.quick_action_button.show()

    def _show_customers(self):
        """Show the customers page."""
        self.stacked_widget.setCurrentIndex(2)
        self.page_title.setText("Customer Management")
        self.quick_action_button.setText("+ Add Customer")
        self.quick_action_button.show()

    def _show_catalog_placeholder(self):
        """Show the product catalog placeholder."""
        self.stacked_widget.setCurrentIndex(3)
        self.page_title.setText("Product Catalog")
        self.quick_action_button.hide()

    @Slot()
    def _show_settings(self):
        """Show the settings page."""
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.page_title.setText("Settings")
        self.quick_action_button.hide()
        
        # Clear navigation selection when showing settings
        self.nav_list.clearSelection()

    @Slot()
    def _on_quick_action(self):
        """Enhanced quick action handling."""
        current_page = self.stacked_widget.currentIndex()
        
        if current_page == 0:  # Dashboard
            # Switch to quote creation page
            self._show_quote_creation()
            # Optionally trigger the product dialog immediately
            if hasattr(self.quote_creation_page, 'open_product_dialog'):
                self.quote_creation_page.open_product_dialog()
        elif current_page == 1:  # Quote Creation
            # Trigger new quote creation in the quote page
            if hasattr(self.quote_creation_page, 'open_product_dialog'):
                self.quote_creation_page.open_product_dialog()
        elif current_page == 2:  # Customers
            # Trigger add customer in the customers page
            if hasattr(self.customers_page, 'add_new_customer'):
                self.customers_page.add_new_customer()

    def apply_theme(self, theme_name: str):
        """Apply theme changes from settings."""
        try:
            # For now, we'll stick with our Babbitt theme
            # You can extend this later to support multiple themes
            self.setStyleSheet(BabbittTheme.get_main_stylesheet())
            logger.info(f"Theme applied: {theme_name}")
        except Exception as e:
            logger.error(f"Failed to apply theme {theme_name}: {e}")

    def show_notification(self, title: str, message: str):
        """Show a simple notification to the user."""
        QMessageBox.information(self, title, message)

    def closeEvent(self, event):
        """Handle application close event."""
        # Add any cleanup here if needed
        logger.info("Application closing")
        event.accept()