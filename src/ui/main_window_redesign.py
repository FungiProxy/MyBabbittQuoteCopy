"""
Redesigned Main Window for MyBabbittQuote Application

Clean, simplified main window with industrial theme and streamlined navigation.
Removes analytics/reports complexity and focuses on core quoting workflow.
"""

import logging

from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import (
    QApplication,
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
    QSizePolicy,
    QGridLayout,
)

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService
from src.core.services.settings_service import SettingsService
from src.ui.theme.theme_manager import ThemeManager
from src.ui.views.customers_page import CustomersPage
from src.ui.views.quote_creation_redesign import QuoteCreationPageRedesign
from src.ui.views.settings_page import SettingsPage
from src.ui.views.dashboard_redesign import DashboardRedesign

logger = logging.getLogger(__name__)


class MainWindowRedesign(QMainWindow):
    """
    Redesigned main window for Babbitt Quote Generator with simplified navigation
    and clean industrial styling. Focuses on core business functions without
    analytics complexity.
    """

    def __init__(self):
        """Initialize the redesigned main window."""
        super().__init__()
        self.setWindowTitle("MyBabbittQuote - Babbitt International")
        
        # Set initial size without aspect ratio constraint
        self.resize(1600, 900)
        
        # Set minimum size - ensure it's enforced
        self.setMinimumSize(1200, 750)
        
        # Initialize theme mode and apply default
        self.current_theme = 'Light' # Default to light mode
        self.settings_service = SettingsService()
        # Note: We will load the saved theme mode later if needed
        ThemeManager.apply_theme(self.current_theme)
        
        # Initialize UI
        self._setup_ui()
        self._connect_signals()
        
        # Show dashboard by default
        self._show_dashboard()
        
        logger.info("MainWindowRedesign initialized successfully")

    def _setup_ui(self):
        """Set up the main UI layout."""
        # Use our custom AspectRatioWidget as the central container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar and content area
        self._create_sidebar()
        self._create_content_area()
        
        # Add to main layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_frame)

    def _create_sidebar(self):
        """Create the sidebar navigation panel."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        self.sidebar_frame.setMaximumWidth(260) # Constrain sidebar width
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo
        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.logo_label)
        
        # Navigation list - SIMPLIFIED
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        # Core navigation items only (no analytics/reports)
        nav_items = [
            "📊 Dashboard",
            "🛒 New Quote", 
            "👥 Customers"
        ]
        
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            self.nav_list.addItem(item)
        
        # Set first item as selected
        self.nav_list.setCurrentRow(0)
        sidebar_layout.addWidget(self.nav_list)
        
        # Spacer
        sidebar_layout.addStretch()
        
        # Theme toggle button
        self.theme_toggle_button = QPushButton("🌙 Dark Mode")
        self.theme_toggle_button.setObjectName("settingsButton") # Reuse style
        sidebar_layout.addWidget(self.theme_toggle_button)
        
        # Settings button at bottom
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
        
        # Stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setMinimumSize(0, 0)
        content_layout.addWidget(self.stacked_widget)
        
        # Initialize pages
        self._create_pages()

    def _create_content_header(self):
        """Create the content area header."""
        self.header_frame = QFrame()
        self.header_frame.setObjectName("contentHeader")
        self.header_frame.setFixedHeight(100)
        
        # Use QGridLayout for more robust alignment
        header_layout = QGridLayout(self.header_frame)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        # Page title
        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("pageTitle")
        # Align title to the left and center vertically
        header_layout.addWidget(self.page_title, 0, 0, Qt.AlignmentFlag.AlignVCenter)
        
        # Spacer column that expands
        header_layout.setColumnStretch(1, 1)
        
        # Header actions
        self.new_quote_button = QPushButton("New Quote")
        self.new_quote_button.setObjectName("new_quote_button")
        self.new_quote_button.setProperty("class", "primary")
        # Align button to the right and center vertically
        header_layout.addWidget(self.new_quote_button, 0, 2, Qt.AlignmentFlag.AlignVCenter)

    def _create_pages(self):
        """Create and add all pages to the stacked widget."""
        # Dashboard page
        self.dashboard_page = DashboardRedesign()
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Quote creation page
        self.quote_page = QuoteCreationPageRedesign()
        self.stacked_widget.addWidget(self.quote_page)
        
        # Customers page
        self.customers_page = CustomersPage()
        self.stacked_widget.addWidget(self.customers_page)
        
        # Settings page
        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.settings_page)

    def _connect_signals(self):
        """Connect UI signals."""
        # Navigation
        self.nav_list.currentRowChanged.connect(self._on_nav_changed)
        self.settings_button.clicked.connect(self._show_settings)
        self.theme_toggle_button.clicked.connect(self._toggle_theme)
        
        # Header actions
        self.new_quote_button.clicked.connect(self._show_quote_creation)
        
        # Page-specific signals
        # The old theme switching from settings page is removed
        # if hasattr(self.settings_page, 'theme_changed'):
        #     self.settings_page.theme_changed.connect(self._apply_theme)

    @Slot(int)
    def _on_nav_changed(self, index):
        """Handle navigation list selection changes."""
        nav_items = ["Dashboard", "New Quote", "Customers"]
        
        if 0 <= index < len(nav_items):
            page_name = nav_items[index]
            self.page_title.setText(page_name)
            self.stacked_widget.setCurrentIndex(index)
            
            # Update header button visibility
            self.new_quote_button.setVisible(index != 1)  # Hide on quote page

    @Slot()
    def _show_settings(self):
        """Show settings page."""
        self.page_title.setText("Settings")
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.new_quote_button.setVisible(True)

    @Slot()
    def _show_quote_creation(self):
        """Show quote creation page."""
        self.nav_list.setCurrentRow(1)  # This will trigger _on_nav_changed

    @Slot()
    def _show_dashboard(self):
        """Show dashboard page."""
        self.nav_list.setCurrentRow(0)

    @Slot()
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_theme == 'Light':
            self.current_theme = 'Dark'
            self.theme_toggle_button.setText("☀️ Light Mode")
        else:
            self.current_theme = 'Light'
            self.theme_toggle_button.setText("🌙 Dark Mode")
            
        ThemeManager.apply_theme(self.current_theme)
        logger.info(f"Switched theme to {self.current_theme}")

    @Slot(str)
    def _apply_theme(self, theme_name):
        """Apply a theme to the application."""
        try:
            # This method is now simplified as theme is managed by the toggle
            ThemeManager.apply_theme(theme_name)
            
            # Save the theme setting
            self.settings_service.set_theme(theme_name)
            self.settings_service.sync()
            
            logger.info(f"Applied theme: {theme_name}")
        except Exception as e:
            logger.error(f"Error applying theme {theme_name}: {e}")
            QMessageBox.warning(
                self, 
                "Theme Error", 
                f"Failed to apply theme '{theme_name}'. Please try again."
            )

    def show_notification(self, message, message_type="info"):
        """Show a notification message."""
        if message_type == "info":
            QMessageBox.information(self, "Information", message)
        elif message_type == "warning":
            QMessageBox.warning(self, "Warning", message)
        elif message_type == "error":
            QMessageBox.critical(self, "Error", message)
        elif message_type == "success":
            # Create a custom success message
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Success")
            msg_box.setText(message)
            msg_box.exec()

    def refresh_dashboard(self):
        """Refresh dashboard data."""
        if hasattr(self.dashboard_page, 'refresh_data'):
            self.dashboard_page.refresh_data()

    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit MyBabbittQuote?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logger.info("Application closing")
            # Clean up services
            self.settings_service.sync()
            event.accept()
        else:
            event.ignore()


# Utility function for easy theme application
def apply_babbitt_theme(app: QApplication):
    """Apply the Babbitt theme to the entire application."""
    ThemeManager.apply_theme('Babbitt Theme', app)
