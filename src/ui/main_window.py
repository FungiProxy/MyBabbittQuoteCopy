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
)

from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialTheme
from src.ui.views.customers_page import CustomersPage
from src.ui.views.quote_creation_redesign import QuoteCreationPageRedesign
from src.ui.views.settings_page import SettingsPage
from src.ui.theme.theme_manager import ThemeManager

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
        self.resize(1400, 900)
        self.setMinimumSize(1200, 700)
        
        self._setup_ui()
        self._connect_signals()
        
        # Start with dashboard
        self._show_dashboard()
        
        logger.info("MainWindow initialized with professional styling")

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
            "📊 Dashboard",
            "📝 New Quote", 
            "👥 Customers",
        ]
        
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            self.nav_list.addItem(item)
        
        # Set dashboard as default selection
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
        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("pageTitle")
        header_layout.addWidget(self.page_title)
        
        # Spacer
        header_layout.addStretch()
        
        # Beautiful orange action button
        self.action_button = QPushButton("+ New Quote")
        self.action_button.setProperty("class", "primary")
        header_layout.addWidget(self.action_button)

    def _create_pages(self):
        """Create all application pages."""
        # Dashboard (Index 0) - Create simple professional dashboard
        self.dashboard_page = self._create_professional_dashboard()
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Quote Creation (Index 1)
        self.quote_creation_page = QuoteCreationPageRedesign()
        self.stacked_widget.addWidget(self.quote_creation_page)
        
        # Customers (Index 2)
        self.customers_page = CustomersPage()
        self.stacked_widget.addWidget(self.customers_page)
        
        # Settings
        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.settings_page)
        
        # Connect settings theme changes
        if hasattr(self.settings_page, 'theme_changed'):
            self.settings_page.theme_changed.connect(self._apply_theme)

    def _create_professional_dashboard(self):
        """Create a beautiful professional dashboard page."""
        dashboard_widget = QWidget()
        
        main_layout = QVBoxLayout(dashboard_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)
        
        # Statistics cards container
        stats_container = self._create_statistics_cards()
        main_layout.addWidget(stats_container)
        
        # Recent quotes section
        recent_section = self._create_recent_quotes_section()
        main_layout.addWidget(recent_section)
        
        # Add stretch to push content to top
        main_layout.addStretch()
        
        return dashboard_widget

    def _create_statistics_cards(self):
        """Create beautiful statistics cards."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Create three professional cards
        card1 = self._create_stat_card("Total Quotes", "0", "This month", "📋")
        card2 = self._create_stat_card("Quote Value", "$0.00", "Total pending", "💰")
        card3 = self._create_stat_card("Active Customers", "0", "This quarter", "👥")
        
        layout.addWidget(card1)
        layout.addWidget(card2)
        layout.addWidget(card3)
        
        return container

    def _create_stat_card(self, title, value, subtitle, icon):
        """Create a single professional statistics card."""
        card = QFrame()
        card.setProperty("class", "stat-card")
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Header with title and icon
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_label.setProperty("class", "stat-title")
        
        icon_label = QLabel(icon)
        icon_label.setProperty("class", "stat-icon")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(icon_label)
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setProperty("class", "stat-value")
        layout.addWidget(value_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setProperty("class", "stat-subtitle")
        layout.addWidget(subtitle_label)
        
        # Apply shadow effect to the card
        self._apply_shadow_effect(card)
        
        return card

    def _apply_shadow_effect(self, widget):
        """Apply a standard drop shadow effect to a widget."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        widget.setGraphicsEffect(shadow)

    def _create_recent_quotes_section(self):
        """Create a professional 'Recent Quotes' section."""
        container = QFrame()
        container.setProperty("class", "content-section")
        self._apply_shadow_effect(container)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title_label = QLabel("Recent Quotes")
        title_label.setProperty("class", "section-title")
        layout.addWidget(title_label)
        
        # This is where the quote list would go. For now, show a placeholder.
        empty_label = QLabel("No recent quotes to display.")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(empty_label)
        
        return container

    def _connect_signals(self):
        """Connect navigation and button signals."""
        self.nav_list.currentRowChanged.connect(self._on_nav_item_selected)
        self.settings_button.clicked.connect(self._show_settings)
        self.action_button.clicked.connect(self._on_action_button_clicked)

    @Slot(int)
    def _on_nav_item_selected(self, index):
        """Handle navigation item selection."""
        if index == 0:  # Dashboard
            self._show_dashboard()
        elif index == 1:  # New Quote
            self._show_quote_creation()
        elif index == 2:  # Customers
            self._show_customers()

    def _show_dashboard(self):
        """Show the dashboard page."""
        self.stacked_widget.setCurrentIndex(0)
        self.page_title.setText("Dashboard")
        self.action_button.setText("+ New Quote")
        self.action_button.show()

    def _show_quote_creation(self):
        """Show the quote creation page."""
        self.stacked_widget.setCurrentIndex(1)
        self.page_title.setText("New Quote")
        self.action_button.setText("+ Add Product")
        self.action_button.show()

    def _show_customers(self):
        """Show the customers page."""
        self.stacked_widget.setCurrentIndex(2)
        self.page_title.setText("Customers")
        self.action_button.setText("+ Add Customer")
        self.action_button.show()

    @Slot()
    def _show_settings(self):
        """Show the settings page."""
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.page_title.setText("Settings")
        self.action_button.hide()
        
        # Clear navigation selection
        self.nav_list.clearSelection()

    @Slot()
    def _on_action_button_clicked(self):
        """Handle action button clicks."""
        current_index = self.stacked_widget.currentIndex()
        
        if current_index == 0:  # Dashboard
            self._show_quote_creation()
        elif current_index == 1:  # Quote Creation
            if hasattr(self.quote_creation_page, '_add_product'):
                self.quote_creation_page._add_product()
        elif current_index == 2:  # Customers
            QMessageBox.information(self, "Add Customer", "Customer creation will be implemented.")

    def _apply_theme(self, theme_name: str):
        """Apply theme changes."""
        try:
            ThemeManager.apply_theme(theme_name)
            logger.info(f"Applied theme: {theme_name}")
        except Exception as e:
            logger.error(f"Failed to apply theme: {e}")

    def closeEvent(self, event):
        """Handle application close."""
        logger.info("Application closing")
        event.accept()