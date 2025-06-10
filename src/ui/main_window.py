"""
Main window module for the Babbitt Quote Generator application.

This module defines the main application window and its core functionality. It includes:
- A sidebar for navigation
- A stacked widget for content display
- Signal handling for theme changes

The main window serves as the central hub for all quote generation activities.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QMessageBox, QFrame, 
    QStackedWidget, QListWidget, QListWidgetItem, QApplication
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from src.ui.quote_creation import QuoteCreationPage
from src.ui.customers_page import CustomersPage
from src.ui.settings_page import SettingsPage
from src.ui.user_profile_dialog import UserProfileDialog
from src.ui.analytics_page import AnalyticsPage
from src.ui.reports_page import ReportsPage
from src.core.services.export_service import QuoteExportService
from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService
from src.ui.themes import THEMES
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """
    Main application window for the Babbitt Quote Generator.
    This window features a sidebar for navigation and a main content area.
    """
    
    def __init__(self):
        """Initialize the main window and set up the UI components."""
        super().__init__()
        self.setWindowTitle("Babbitt")
        self.resize(1300, 700)
        
        print("MainWindow.__init__() called")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._create_sidebar()
        self._create_content_area()
        
        self.main_layout.addWidget(self.sidebar_frame, 1)
        self.main_layout.addWidget(self.content_area_frame, 4)

        self._show_dashboard_content()
        self._connect_sidebar_signals()
        
        print("MainWindow initialization complete")

    def _create_sidebar(self):
        """Creates the sidebar navigation panel."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        self.sidebar_frame.setFixedWidth(220)

        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(10)

        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.logo_label)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        nav_items = ["Dashboard", "Quote Creation", "Customers"]
        for item_text in nav_items:
            self.nav_list.addItem(QListWidgetItem(item_text))
        
        self.nav_list.setCurrentRow(0)
        self.sidebar_layout.addWidget(self.nav_list)
        self.sidebar_layout.addStretch()

        self.settings_button = QPushButton("Settings")
        self.settings_button.setObjectName("settingsButton")
        self.sidebar_layout.addWidget(self.settings_button)

    def _create_content_area(self):
        """Creates the main content area where different views will be displayed."""
        self.content_area_frame = QFrame()
        self.content_area_frame.setObjectName("contentAreaFrame")

        self.content_layout = QVBoxLayout(self.content_area_frame)
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(0)

        self._create_content_header()
        self.content_layout.addWidget(self.content_header_frame)

        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)

        self.dashboard_page = QWidget()
        self.stacked_widget.addWidget(self.dashboard_page)
        self.quote_creation_page = QuoteCreationPage()
        self.stacked_widget.addWidget(self.quote_creation_page)
        self.customers_page = CustomersPage()
        self.stacked_widget.addWidget(self.customers_page)
        
        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.settings_page)
        self.settings_page.theme_changed.connect(self.apply_theme)
        
        self.quote_creation_page.quote_deleted.connect(self.update_dashboard_stats)
        
    def _create_content_header(self):
        """Creates the header part of the content area."""
        self.content_header_frame = QFrame()
        self.content_header_frame.setObjectName("contentHeaderFrame")
        self.content_header_frame.setFixedHeight(60)

        header_layout = QHBoxLayout(self.content_header_frame)
        header_layout.setContentsMargins(20, 0, 20, 0)

        self.current_view_title = QLabel("Dashboard")
        self.current_view_title.setObjectName("currentViewTitle")
        header_layout.addWidget(self.current_view_title)
        header_layout.addStretch()

        self.bell_button = QPushButton("🔔")
        self.bell_button.setFixedSize(30,30)
        self.bell_button.setObjectName("iconButton")
        self.bell_button.clicked.connect(self.show_notifications)
        header_layout.addWidget(self.bell_button)
        
        self.user_profile_button = QPushButton("👤 John Smith")
        self.user_profile_button.setObjectName("userProfileButton")
        header_layout.addWidget(self.user_profile_button)
        self.user_profile_button.clicked.connect(self.show_user_profile)

    def _show_dashboard_content(self):
        """Populates the dashboard_page with content."""
        self.current_view_title.setText("Dashboard")
        self.stacked_widget.setCurrentWidget(self.dashboard_page)

        dashboard_layout = QVBoxLayout(self.dashboard_page)
        dashboard_layout.setContentsMargins(20,20,20,20)
        dashboard_layout.setSpacing(20)

        dashboard_tabs_layout = QHBoxLayout()
        self.overview_button = QPushButton("Overview")
        self.overview_button.setObjectName("dashboardTabButtonSelected")
        self.analytics_button = QPushButton("Analytics")
        self.analytics_button.setObjectName("dashboardTabButton")
        self.reports_button_dash = QPushButton("Reports")
        self.reports_button_dash.setObjectName("dashboardTabButton")
        
        dashboard_tabs_layout.addWidget(self.overview_button)
        dashboard_tabs_layout.addWidget(self.analytics_button)
        dashboard_tabs_layout.addWidget(self.reports_button_dash)
        dashboard_tabs_layout.addStretch()
        
        self.dashboard_content_stack = QStackedWidget()
        
        dashboard_layout.addLayout(dashboard_tabs_layout)
        dashboard_layout.addWidget(self.dashboard_content_stack)

        self.overview_widget = QWidget()
        overview_layout = QVBoxLayout(self.overview_widget)
        overview_layout.setContentsMargins(0,10,0,0)
        self.dashboard_content_stack.addWidget(self.overview_widget)

        self.dashboard_content_stack.addWidget(AnalyticsPage())
        self.dashboard_content_stack.addWidget(ReportsPage())

        self.overview_button.clicked.connect(lambda: self.dashboard_content_stack.setCurrentIndex(0))
        self.analytics_button.clicked.connect(lambda: self.dashboard_content_stack.setCurrentIndex(1))
        self.reports_button_dash.clicked.connect(lambda: self.dashboard_content_stack.setCurrentIndex(2))

        self.update_dashboard_stats()

    def update_dashboard_stats(self):
        """Fetches and displays the latest dashboard statistics."""
        # Clear existing overview layout
        # Accessing the layout of overview_widget
        overview_layout = self.overview_widget.layout()
        if overview_layout is not None:
            # Clear previous widgets from the layout
            while overview_layout.count():
                child = overview_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        db = SessionLocal()
        try:
            stats = QuoteService.get_dashboard_statistics(db)
            stats_layout = QHBoxLayout()
            stats_layout.setSpacing(20)
            
            card1 = self._create_stat_card("Total Quotes", str(stats["total_quotes"]), f"{stats['quote_change']:+}% from last month", "📄")
            card2 = self._create_stat_card("Quote Value", f"${stats['total_quote_value']:,.2f}", f"{stats['value_change']:+}% from last month", "$")
            card3 = self._create_stat_card("Customers", str(stats["total_customers"]), "Total unique customers", "👥")
            card4 = self._create_stat_card("Products", str(stats["total_products"]), "Total unique products quoted", "📦")
            
            stats_layout.addWidget(card1)
            stats_layout.addWidget(card2)
            stats_layout.addWidget(card3)
            stats_layout.addWidget(card4)
            overview_layout.addLayout(stats_layout)

            main_content_layout = QHBoxLayout()
            main_content_layout.setSpacing(20)
            recent_quotes_group = self._create_recent_quotes_section(stats.get("recent_quotes", []))
            main_content_layout.addWidget(recent_quotes_group)
            sales_category_group = self._create_sales_by_category_section(stats.get("sales_by_category", []))
            main_content_layout.addWidget(sales_category_group)
            
            overview_layout.addLayout(main_content_layout)
            overview_layout.addStretch()
            
        except Exception as e:
            logger.error(f"Error getting dashboard statistics: {e}", exc_info=True)
            overview_layout.addWidget(QLabel("Could not load dashboard statistics."))
        finally:
            db.close()

    def _create_stat_card(self, title_text, value_text, sub_text, icon_text=""):
        """Creates a styled card for displaying a statistic."""
        card = QFrame()
        card.setObjectName("statCard")
        card_layout = QVBoxLayout(card)
        top_layout = QHBoxLayout()
        title = QLabel(title_text)
        title.setObjectName("statTitle")
        icon = QLabel(icon_text)
        icon.setObjectName("statIcon")
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(icon)
        card_layout.addLayout(top_layout)
        value = QLabel(value_text)
        value.setObjectName("statValue")
        card_layout.addWidget(value)
        sub = QLabel(sub_text)
        sub.setObjectName("statSubText")
        card_layout.addWidget(sub)
        return card

    def _create_recent_quotes_section(self, recent_quotes):
        # Implementation omitted for brevity, assuming it exists
        return QFrame()

    def _create_sales_by_category_section(self, sales_data):
        # Implementation omitted for brevity, assuming it exists
        return QFrame()
        
    def _connect_sidebar_signals(self):
        """Connects signals for the sidebar navigation."""
        self.nav_list.currentRowChanged.connect(self.on_nav_item_selected)
        self.settings_button.clicked.connect(self.on_settings_selected)

    @Slot(int)
    def on_nav_item_selected(self, index):
        """Switches the main content view based on sidebar selection."""
        self.stacked_widget.setCurrentIndex(index)
        self.current_view_title.setText(self.nav_list.item(index).text())

    @Slot()
    def on_settings_selected(self):
        """Shows the settings page."""
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.current_view_title.setText("Settings")

    def show_notifications(self):
        """Shows a placeholder for notifications."""
        QMessageBox.information(self, "Notifications", "You have no new notifications.")

    def show_user_profile(self):
        """Shows the user profile dialog."""
        dialog = UserProfileDialog(self)
        dialog.exec()

    def apply_theme(self, theme_name: str):
        """Applies the selected theme to the application."""
        if theme_name not in THEMES:
            logger.warning(f"Theme '{theme_name}' not found. Using 'Default Light'.")
            theme_name = "Default Light"
            
        theme = THEMES[theme_name]
        
        style_sheet = f"""
            QMainWindow, QWidget {{
                background-color: {theme['background']};
                color: {theme['foreground']};
            }}
            QFrame#sidebarFrame {{
                background-color: {theme['card_background']};
                border-right: 1px solid {theme['card_border']};
            }}
            QLabel#logoLabel {{
                font-size: 22px; 
                font-weight: bold; 
                margin-bottom: 15px;
                padding: 10px;
                color: {theme['primary']};
            }}
            QListWidget {{
                background-color: {theme['card_background']};
                border: none;
            }}
            QListWidget#navList::item {{
                padding: 12px 15px;
                border-radius: 5px;
            }}
            QListWidget#navList::item:hover {{
                background-color: {theme['background']};
            }}
            QListWidget#navList::item:selected {{
                background-color: {theme['primary']};
                color: {theme['light']};
                font-weight: bold;
            }}
            QPushButton#settingsButton {{
                text-align: left; 
                padding: 12px 15px; 
                font-size: 14px; 
                border: none;
                border-radius: 5px;
                margin-top: 10px;
                background-color: {theme['card_background']};
                color: {theme['foreground']};
            }}
            QPushButton#settingsButton:hover {{
                background-color: {theme['background']};
            }}
            QFrame#contentAreaFrame {{
                background-color: {theme['background']};
            }}
            QFrame#contentHeaderFrame {{
                background-color: {theme['card_background']};
                border-bottom: 1px solid {theme['card_border']};
            }}
            QLabel#currentViewTitle {{
                font-size: 18px; 
                font-weight: bold;
                color: {theme['foreground']};
            }}
            QPushButton#iconButton, QPushButton#userProfileButton {{
                border: none;
                font-size: 14px;
                color: {theme['secondary']};
                padding: 5px;
                background-color: transparent;
            }}
            QPushButton#iconButton:hover, QPushButton#userProfileButton:hover {{
                color: {theme['primary']};
            }}
            QPushButton#newQuoteButtonHeader {{
                background-color: {theme['primary']}; 
                color: {theme['light']};
            }}
            QPushButton#newQuoteButtonHeader:hover {{
                background-color: {theme['dark']};
            }}
            QPushButton#dashboardTabButton {{
                padding: 8px 15px;
                font-size: 14px;
                border: none;
                background-color: transparent;
                margin-right: 5px;
                color: {theme['secondary']};
            }}
            QPushButton#dashboardTabButton:hover {{
                color: {theme['primary']};
                background-color: {theme['light']};
                border-radius: 4px;
            }}
            QPushButton#dashboardTabButtonSelected {{
                font-weight: bold;
                color: {theme['primary']};
                border-bottom: 2px solid {theme['primary']};
                padding: 8px 15px;
                font-size: 14px;
                border: none;
                background-color: transparent;
                margin-right: 5px;
            }}
            QFrame#statCard {{
                border: 1px solid {theme['card_border']}; 
                border-radius: 6px; 
                padding: 18px; 
                background-color: {theme['card_background']}; 
            }}
            QLabel#statTitle, QLabel#statCardTitle {{
                font-size: 13px; 
                color: {theme['text_muted']}; 
                font-weight: 500;
            }}
            QLabel#statIcon {{
                font-size: 18px; 
                color: {theme['text_muted']};
            }}
            QLabel#statValue {{
                font-size: 24px;
                font-weight: bold; 
                margin-top: 6px; 
                margin-bottom: 6px;
                color: {theme['foreground']};
            }}
            QLabel#statSubText {{
                font-size: 11px; 
                color: {theme['text_muted']};
            }}
            QFrame#dashboardSectionFrame, QFrame#customersCard, QFrame#itemsCard, QFrame#customerCard, QFrame#summaryCard {{
                 background-color: {theme['card_background']};
                 border: 1px solid {theme['card_border']};
                 border-radius: 6px;
                 padding: 18px;
            }}
            QFrame#itemsCard {{
                 background-color: {theme['card_background']};
                 border: 1px solid {theme['card_border']};
                 border-radius: 6px;
                 padding: 18px;
            }}
            QLabel#sectionTitle {{
                font-size: 15px;
                font-weight: bold;
                color: {theme['foreground']};
                margin-bottom: 12px;
            }}
            QGroupBox {{
                font-size: 14px;
                font-weight: bold;
                color: {theme['foreground']};
                border: 1px solid {theme['card_border']};
                border-radius: 6px;
                margin-top: 10px;
                padding: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
            }}
            QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit {{
                padding: 8px;
                border: 1px solid {theme['card_border']};
                border-radius: 4px;
                background-color: {theme['background']};
                color: {theme['foreground']};
                font-size: 14px;
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {{
                border-color: {theme['primary']};
            }}
            QPushButton {{
                padding: 8px 16px;
                border: 1px solid {theme['primary']};
                border-radius: 4px;
                background-color: {theme['primary']};
                color: {theme['light']};
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:disabled {{
                background-color: {theme['secondary']};
                border-color: {theme['secondary']};
                color: #999;
            }}
            QTableWidget {{
                gridline-color: {theme['card_border']};
                background-color: {theme['card_background']};
                color: {theme['foreground']};
                border: 1px solid {theme['card_border']};
                border-radius: 6px;
            }}
            QHeaderView::section {{
                background-color: {theme['background']};
                color: {theme['foreground']};
                padding: 4px;
                border: 1px solid {theme['card_border']};
                font-weight: bold;
            }}
            QMessageBox {{
                background-color: {theme['background']};
            }}
            QMessageBox QLabel {{
                color: {theme['foreground']};
            }}
        """
        QApplication.instance().setStyleSheet(style_sheet) 