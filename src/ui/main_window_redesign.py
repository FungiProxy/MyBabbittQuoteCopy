"""
Updated Main Window Implementation  
File: src/ui/views/main_window_redesign.py

🟡 Important - Replace your existing main_window_redesign.py with this version
⏱️ 5 minutes to implement
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
)

from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.views.customers_page import CustomersPage
from src.ui.views.quote_creation_redesign import QuoteCreationPageRedesign
from src.ui.views.settings_page import SettingsPage
from src.ui.views.dashboard_redesign import DashboardRedesign

logger = logging.getLogger(__name__)


class MainWindowRedesign(QMainWindow):
    """
    Main window with beautiful blue gradient sidebar and professional styling.
    Matches the polished UI from your screenshots.
    """

    def __init__(self):
        """Initialize the main window with complete styling."""
        super().__init__()
        self.setWindowTitle("MyBabbittQuote - Babbitt International")
        
        # Set proper window size to match your screenshots
        self.resize(1400, 900)
        self.setMinimumSize(1200, 800)
        
        # Apply the complete theme immediately
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        
        # Initialize UI components
        self._setup_ui()
        self._connect_signals()
        
        # Show dashboard by default
        self._show_dashboard()
        
        logger.info("MainWindowRedesign initialized with complete styling")

    def _setup_ui(self):
        """Set up the main UI layout with proper proportions."""
        # Central widget with horizontal layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar and content area
        self._create_sidebar()
        self._create_content_area()
        
        # Add to main layout with proper proportions
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_frame, 1)  # Content takes remaining space

    def _create_sidebar(self):
        """Create the beautiful blue gradient sidebar."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo with proper styling
        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.logo_label)
        
        # Navigation list with proper styling
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        # Core navigation items (matches your screenshots)
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
        
        # Spacer to push settings button to bottom
        sidebar_layout.addStretch()
        
        # Settings button at bottom with proper styling
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setObjectName("settingsButton")
        sidebar_layout.addWidget(self.settings_button)

    def _create_content_area(self):
        """Create the main content area with proper header."""
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentAreaFrame")
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Content header with proper styling
        self._create_content_header()
        content_layout.addWidget(self.header_frame)
        
        # Stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Initialize all pages
        self._create_pages()

    def _create_content_header(self):
        """Create the content area header with orange accent button."""
        self.header_frame = QFrame()
        self.header_frame.setObjectName("contentHeader")
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(24, 20, 24, 20)
        
        # Page title with proper styling
        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("pageTitle")
        header_layout.addWidget(self.page_title)
        
        # Spacer
        header_layout.addStretch()
        
        # Header actions - orange accent button
        self.new_quote_button = QPushButton("New Quote")
        self.new_quote_button.setProperty("class", "primary")
        header_layout.addWidget(self.new_quote_button)

    def _create_pages(self):
        """Create and add all pages to the stacked widget."""
        try:
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
            
        except Exception as e:
            logger.error(f"Error creating pages: {e}")
            # Create placeholder widgets if pages don't exist
            for page_name in ["Dashboard", "Quote Creation", "Customers", "Settings"]:
                placeholder = QWidget()
                label = QLabel(f"{page_name} Page")
                label.setAlignment(Qt.AlignCenter)
                layout = QVBoxLayout(placeholder)
                layout.addWidget(label)
                self.stacked_widget.addWidget(placeholder)

    def _connect_signals(self):
        """Connect UI signals."""
        # Navigation
        self.nav_list.currentRowChanged.connect(self._on_nav_changed)
        self.settings_button.clicked.connect(self._show_settings)
        
        # Header actions
        self.new_quote_button.clicked.connect(self._show_quote_creation)
        
        # Page-specific signals
        try:
            if hasattr(self.settings_page, 'theme_changed'):
                self.settings_page.theme_changed.connect(self._apply_theme)
        except:
            pass

    @Slot(int)
    def _on_nav_changed(self, index):
        """Handle navigation list selection changes."""
        nav_items = ["Dashboard", "New Quote", "Customers"]
        
        if 0 <= index < len(nav_items):
            page_name = nav_items[index]
            self.page_title.setText(page_name)
            self.stacked_widget.setCurrentIndex(index)
            
            # Update header button visibility (hide on quote page)
            self.new_quote_button.setVisible(index != 1)

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

    @Slot(str)
    def _apply_theme(self, theme_name):
        """Apply a theme to the application."""
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        logger.info(f"Applied theme: {theme_name}")

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
            event.accept()
        else:
            event.ignore()


# Utility function for easy theme application
def apply_babbitt_theme(app: QApplication):
    """Apply the Babbitt theme to the entire application."""
    app.setStyleSheet(BabbittTheme.get_main_stylesheet())