"""
Working Main Window Implementation

This implementation will immediately restore your beautiful professional interface
with the blue gradient sidebar and proper styling.

File: src/ui/views/main_window.py (REPLACE COMPLETELY)
"""

import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
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
    QDialog,
)

from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.theme.babbitt_industrial_theme import BabbittPremiumIntegration
from src.ui.views.customers_page import CustomersPage
from src.ui.views.quote_creation_redesign import QuoteCreationPageRedesign
from src.ui.views.quotes_page import QuotesPage
from src.ui.views.settings_page import SettingsPage
from src.ui.theme.theme_manager import ThemeManager
from src.ui.dialogs.customer_dialog import CustomerDialog
from src.core.services.quote_service import QuoteService
from src.core.database import SessionLocal

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Professional main window with beautiful blue sidebar and Babbitt International styling.
    This implementation will immediately restore your professional interface.
    """

    def __init__(self):
        """Initialize the main window with proper styling."""
        super().__init__()
        self.setWindowTitle("MyBabbittQuote - Babbitt International")
        self.resize(1600, 900)
        self.setMinimumSize(1200, 700)
        
        # Store reference to self for theme switching
        self._main_window_instance = self
        
        # Apply the enhanced industrial theme with Python animations
        BabbittPremiumIntegration.apply_premium_theme(self)
        
        self._setup_ui()
        self._connect_signals()
        
        # Start with quote creator
        self._show_quote_creation()
        
        logger.info("MainWindow initialized with professional styling and Python animations")

    def _setup_ui(self):
        """Set up the main UI layout."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create components
        self._create_beautiful_sidebar()
        self._create_professional_content_area()
        
        # Add to layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_frame, 1)

    def _create_beautiful_sidebar(self):
        """Create the beautiful blue gradient sidebar."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Beautiful Babbitt logo
        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(self.logo_label)
        
        # Professional navigation list
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        # Core navigation items
        nav_items = [
            "📝 Quote Creator",
            "📂 Quotes",
            "👥 Customers",
        ]
        
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            self.nav_list.addItem(item)
        
        # Set quote creator as default selection
        self.nav_list.setCurrentRow(0)
        sidebar_layout.addWidget(self.nav_list)
        
        # Spacer to push settings to bottom
        sidebar_layout.addStretch()
        
        # Settings button at bottom
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setObjectName("settingsButton")
        sidebar_layout.addWidget(self.settings_button)

    def _create_professional_content_area(self):
        """Create the professional content area."""
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentAreaFrame")
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Professional header
        self._create_professional_header()
        content_layout.addWidget(self.header_frame)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        # Initialize pages
        self._create_pages()

    def _create_professional_header(self):
        """Create the professional content header with orange accent button."""
        self.header_frame = QFrame()
        self.header_frame.setObjectName("contentHeader")
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        # Page title
        self.page_title = QLabel("Quote Creator")
        self.page_title.setObjectName("pageTitle")
        header_layout.addWidget(self.page_title)
        
        # Spacer
        header_layout.addStretch()
        
        # Beautiful orange action button
        self.action_button = QPushButton("+ New Product")
        self.action_button.setProperty("class", "primary")
        header_layout.addWidget(self.action_button)

    def _create_pages(self):
        """Create all application pages."""
        # Quote Creation (Index 0)
        self.quote_creation_page = QuoteCreationPageRedesign()
        self.stacked_widget.addWidget(self.quote_creation_page)
        
        # Quotes Page (Index 1)
        self.quotes_page = QuotesPage()
        self.stacked_widget.addWidget(self.quotes_page)
        
        # Customers (Index 2)
        self.customers_page = CustomersPage()
        self.stacked_widget.addWidget(self.customers_page)
        
        # Settings
        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.settings_page)
        
    def _connect_signals(self):
        """Connect UI element signals to slots."""
        self.nav_list.currentRowChanged.connect(self._on_nav_item_selected)
        self.settings_button.clicked.connect(self._show_settings)
        self.action_button.clicked.connect(self._on_action_button_clicked)
        
        # Connect settings theme changes
        if hasattr(self.settings_page, 'theme_changed'):
            self.settings_page.theme_changed.connect(self._apply_theme)
        
        # Connect quotes page signals
        self.quotes_page.edit_quote_requested.connect(self._edit_quote)
        
        # Connect quote deletion to reset quote creation page
        if hasattr(self.quotes_page, 'quote_deleted'):
            self.quotes_page.quote_deleted.connect(self._reset_quote_creation_page)

    @Slot(int)
    def _on_nav_item_selected(self, index):
        """Handle navigation selection."""
        if index == 0: self._show_quote_creation()
        elif index == 1: self._show_quotes()
        elif index == 2: self._show_customers()

    def _show_quote_creation(self):
        """Show quote creation page."""
        self.page_title.setText("Quote Creator")
        self.action_button.setText("+ New Product")
        self.action_button.show()
        self.stacked_widget.setCurrentIndex(0)

    def _show_quotes(self):
        """Show quotes page."""
        self.page_title.setText("All Quotes")
        self.action_button.setText("+ New Quote")
        self.quotes_page.load_quotes() # Refresh quotes
        self.stacked_widget.setCurrentIndex(1)

    def _show_customers(self):
        """Show customers page."""
        self.page_title.setText("Customers")
        self.action_button.setText("+ Add Customer")
        self.action_button.show()
        self.stacked_widget.setCurrentIndex(2)

    @Slot()
    def _show_settings(self):
        """Show the settings page."""
        self.page_title.setText("Settings")
        self.action_button.hide()
        self.stacked_widget.setCurrentWidget(self.settings_page)
        # Clear navigation selection
        self.nav_list.clearSelection()

    @Slot()
    def _on_action_button_clicked(self):
        """Handle the main action button click based on the current page."""
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0: # Quote Creator
            if hasattr(self.quote_creation_page, '_add_product'):
                self.quote_creation_page._add_product()
        elif current_index == 1: # Quotes
            self._show_quote_creation()
        elif current_index == 2: # Customers
            dialog = CustomerDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if hasattr(self.customers_page, '_filter_customers'):
                    self.customers_page._filter_customers()

    @Slot(int)
    def _edit_quote(self, quote_id: int):
        """Open a quote in the editor."""
        try:
            with SessionLocal() as db:
                quote_data = QuoteService.get_full_quote_details(db, quote_id)
            
            if quote_data:
                self.quote_creation_page.load_quote(quote_data)
                self.stacked_widget.setCurrentWidget(self.quote_creation_page)
                self.page_title.setText(f"Editing Quote: {quote_data['quote_number']}")
                # Select the "Quote Creator" in nav
                self.nav_list.setCurrentRow(0)
            else:
                QMessageBox.warning(self, "Error", "Could not load quote details.")
        except Exception as e:
            logger.error(f"Error loading quote for editing: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to load quote: {e}")

    @Slot(int)
    def _reset_quote_creation_page(self, deleted_quote_id: int):
        """Reset quote creation page when a quote is deleted."""
        try:
            # Check if we're currently editing the deleted quote
            current_quote = getattr(self.quote_creation_page, 'current_quote', {})
            current_quote_id = current_quote.get('id')
            
            if current_quote_id == deleted_quote_id:
                # Reset the quote creation page to a clean state
                self.quote_creation_page.new_quote()
                self.page_title.setText("Quote Creator")
                # Show a message to the user
                QMessageBox.information(
                    self, 
                    "Quote Deleted", 
                    "The quote you were editing has been deleted. A new quote has been started."
                )
        except Exception as e:
            logger.error(f"Error resetting quote creation page: {e}", exc_info=True)

    def _apply_theme(self, theme_name: str):
        """Apply the selected theme."""
        ThemeManager.apply_theme(theme_name, self)

    def closeEvent(self, event):
        """Handle widget close event."""
        # Clean up database connections if they exist
        if hasattr(self.quote_creation_page, 'db'):
            self.quote_creation_page.db.close()
        event.accept()