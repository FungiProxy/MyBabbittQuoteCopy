"""
Modernized Main Window Implementation

Enhanced professional interface with modern styling, better spacing,
and improved user experience while maintaining all existing functionality.

File: src/ui/main_window.py (MODERNIZED VERSION)
"""

import logging

from PySide6.QtCore import Qt, Slot, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QFont, QPalette
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
    QSpacerItem,
    QSizePolicy,
)

from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.theme.babbitt_industrial_theme import BabbittPremiumIntegration
from src.ui.views.customers_page import CustomersPage
from src.ui.views.quote_creation_redesign import QuoteCreationPageRedesign
from src.ui.views.quotes_page import QuotesPage
from src.ui.views.enhanced_settings_page import EnhancedSettingsPage as SettingsPage
from src.ui.theme.theme_manager import ThemeManager
from src.ui.dialogs.customer_dialog import CustomerDialog
from src.core.services.quote_service import QuoteService
from src.core.database import SessionLocal
from src.ui.theme import COLORS, FONTS, SPACING, RADIUS, get_button_style

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Modernized main window with enhanced professional styling and improved UX.
    Maintains all existing functionality while providing a more polished interface.
    """

    def __init__(self):
        """Initialize the main window with enhanced styling."""
        super().__init__()
        self.setWindowTitle("MyBabbittQuote - Babbitt International")
        self.resize(1600, 900)
        self.setMinimumSize(1200, 700)
        
        # Initialize services
        self.quote_service = QuoteService()

        # Store reference to self for theme switching
        self._main_window_instance = self
        
        # Apply the enhanced industrial theme with Python animations
        BabbittPremiumIntegration.apply_theme_to_application(self)
        
        # Add modern window styling
        self._apply_modern_window_styling()
        
        self._setup_ui()
        self._connect_signals()
        
        # Start with quote creator
        self._show_quote_creation()
        
        logger.info("MainWindow initialized with modern styling and enhanced UX")

    def _apply_modern_window_styling(self):
        """Apply modern window styling and effects."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
                font-size: {FONTS['sizes']['base']}px;
            }}
            QFrame#sidebarFrame {{
                background-color: {COLORS['bg_sidebar']};
                border: none;
                min-width: 220px;
                max-width: 220px;
            }}
            QLabel#logoLabel {{
                color: {COLORS['primary']};
                font-size: {FONTS['sizes']['3xl']}px;
                font-weight: {FONTS['weights']['bold']};
                padding: {SPACING['xl']}px {SPACING['lg']}px {SPACING['md']}px {SPACING['lg']}px;
                margin-bottom: {SPACING['md']}px;
                background: transparent;
                border-bottom: 1px solid {COLORS['gray_700']};
                letter-spacing: -0.5px;
            }}
            QListWidget#navList {{
                background: transparent;
                border: none;
                color: {COLORS['text_secondary']};
                font-size: {FONTS['sizes']['lg']}px;
                font-weight: {FONTS['weights']['medium']};
                outline: none;
                padding: {SPACING['md']}px 0;
            }}
            QListWidget#navList::item {{
                padding: {SPACING['lg']}px {SPACING['xl']}px {SPACING['lg']}px {SPACING['lg']}px;
                margin: {SPACING['xs']}px {SPACING['md']}px {SPACING['xs']}px 0;
                border-radius: {RADIUS['md']}px;
                border-left: 4px solid transparent;
            }}
            QListWidget#navList::item:hover {{
                background: {COLORS['gray_800']};
                color: {COLORS['primary']};
            }}
            QListWidget#navList::item:selected {{
                background: {COLORS['primary']};
                border-left: 4px solid {COLORS['primary']};
                color: {COLORS['bg_primary']};
                font-weight: {FONTS['weights']['bold']};
            }}
            QPushButton#settingsButton {{
                {get_button_style('secondary')}
                margin: {SPACING['lg']}px;
                font-size: {FONTS['sizes']['base']}px;
                font-weight: {FONTS['weights']['medium']};
            }}
            QPushButton#settingsButton:hover {{
                background-color: {COLORS['primary']};
                color: {COLORS['bg_primary']};
            }}
            QFrame#contentAreaFrame {{
                background: {COLORS['bg_primary']};
                border: none;
            }}
            QFrame#contentHeader {{
                background: {COLORS['bg_primary']};
                border: none;
                border-bottom: 1px solid {COLORS['border_light']};
                min-height: 80px;
                max-height: 80px;
            }}
            QLabel#pageTitle {{
                color: {COLORS['text_primary']};
                font-size: {FONTS['sizes']['3xl']}px;
                font-weight: {FONTS['weights']['bold']};
                letter-spacing: -0.5px;
                margin: 0;
                padding: 0;
            }}
            QStackedWidget#contentStackedWidget {{
                background: {COLORS['bg_primary']};
                border: none;
            }}
        """)

    def _setup_ui(self):
        """Set up the modernized UI layout with enhanced spacing."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create components with enhanced styling
        self._create_enhanced_sidebar()
        self._create_enhanced_content_area()
        
        # Add to layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_frame, 1)

    def _create_enhanced_sidebar(self):
        """Create the enhanced blue gradient sidebar with modern styling."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Enhanced Babbitt logo with modern typography
        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add modern font styling
        logo_font = QFont()
        logo_font.setFamily("Segoe UI")
        logo_font.setPointSize(26)
        logo_font.setWeight(QFont.Weight.Bold)
        self.logo_label.setFont(logo_font)
        
        sidebar_layout.addWidget(self.logo_label)
        
        # Add spacer for better logo positioning
        sidebar_layout.addSpacing(8)
        
        # Enhanced navigation list with modern styling
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        # Core navigation items with enhanced icons
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
        
        # Enhanced spacer to push settings to bottom
        sidebar_layout.addStretch()
        
        # Enhanced settings button with modern styling
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setObjectName("settingsButton")
        
        # Add hover animation
        self._setup_button_animation(self.settings_button)
        
        sidebar_layout.addWidget(self.settings_button)

    def _create_enhanced_content_area(self):
        """Create the enhanced content area with modern styling."""
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentAreaFrame")
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Enhanced header with modern styling
        self._create_enhanced_header()
        content_layout.addWidget(self.header_frame)
        
        # Enhanced stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("contentStackedWidget")
        content_layout.addWidget(self.stacked_widget)
        
        # Initialize pages
        self._create_pages()

    def _create_enhanced_header(self):
        """Create the enhanced content header with modern styling."""
        self.header_frame = QFrame()
        self.header_frame.setObjectName("contentHeader")
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(32, 24, 32, 24)  # Enhanced spacing
        header_layout.setSpacing(16)
        
        # Enhanced page title with modern typography
        self.page_title = QLabel("Quote Creator")
        self.page_title.setObjectName("pageTitle")
        
        # Add modern font styling
        title_font = QFont()
        title_font.setFamily("Segoe UI")
        title_font.setPointSize(28)
        title_font.setWeight(QFont.Weight.Bold)
        self.page_title.setFont(title_font)
        
        header_layout.addWidget(self.page_title)
        
        # Enhanced spacer
        header_layout.addStretch()
        
        # Enhanced action button with modern styling
        self.action_button = QPushButton("+ New Product")
        self.action_button.setProperty("class", "primary")
        self.action_button.setObjectName("primaryActionButton")
        
        # Add hover animation
        self._setup_button_animation(self.action_button)
        
        header_layout.addWidget(self.action_button)

    def _setup_button_animation(self, button):
        """Setup hover animation for buttons."""
        # Create hover animation
        self.hover_animation = QPropertyAnimation(button, b"geometry")
        self.hover_animation.setDuration(150)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _create_pages(self):
        """Create all application pages with enhanced styling."""
        try:
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
            
        except Exception as e:
            logger.error(f"Error creating pages: {e}")
            # Create placeholder widgets if pages don't exist
            for page_name in ["Quote Creation", "Quotes", "Customers", "Settings"]:
                placeholder = self._create_placeholder_page(page_name)
                self.stacked_widget.addWidget(placeholder)
        
    def _create_placeholder_page(self, page_name):
        """Create a placeholder page with modern styling."""
        placeholder = QWidget()
        placeholder.setObjectName("placeholderPage")
        
        layout = QVBoxLayout(placeholder)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Modern placeholder content
        title = QLabel(f"{page_name} Page")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("This page is under development")
        subtitle.setObjectName("pageSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        
        return placeholder
        
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
        self.quotes_page.quote_deleted.connect(self.quote_creation_page.clear_if_quote_matches)

    @Slot(int)
    def _on_nav_item_selected(self, index):
        """Handle navigation selection with enhanced feedback."""
        if index == 0: 
            self._show_quote_creation()
        elif index == 1: 
            self._show_quotes()
        elif index == 2: 
            self._show_customers()

    def _show_quote_creation(self):
        """Show quote creation page with enhanced styling."""
        self.page_title.setText("Quote Creator")
        self.action_button.setText("+ New Product")
        self.action_button.show()
        self.stacked_widget.setCurrentIndex(0)
        
        # Add subtle animation
        self._animate_page_transition()

    def _show_quotes(self):
        """Show quotes page with enhanced styling."""
        self.page_title.setText("All Quotes")
        self.action_button.setText("+ New Quote")
        self.quotes_page.load_quotes()  # Refresh quotes
        self.stacked_widget.setCurrentIndex(1)
        
        # Add subtle animation
        self._animate_page_transition()

    def _show_customers(self):
        """Show customers page with enhanced styling."""
        self.page_title.setText("Customers")
        self.action_button.setText("+ Add Customer")
        self.action_button.show()
        self.stacked_widget.setCurrentIndex(2)
        
        # Add subtle animation
        self._animate_page_transition()

    def _animate_page_transition(self):
        """Add subtle animation for page transitions."""
        # Create a simple fade animation
        animation = QPropertyAnimation(self.stacked_widget, b"windowOpacity")
        animation.setDuration(150)
        animation.setStartValue(0.8)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()

    @Slot()
    def _show_settings(self):
        """Show the settings page with enhanced styling."""
        self.page_title.setText("Settings")
        self.action_button.hide()
        self.stacked_widget.setCurrentWidget(self.settings_page)
        # Clear navigation selection
        self.nav_list.clearSelection()
        
        # Add subtle animation
        self._animate_page_transition()

    @Slot()
    def _on_action_button_clicked(self):
        """Handle the main action button click based on the current page."""
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0:  # Quote Creator
            if hasattr(self.quote_creation_page, '_add_product'):
                self.quote_creation_page._add_product()
        elif current_index == 1:  # Quotes
            self._show_quote_creation()
        elif current_index == 2:  # Customers
            dialog = CustomerDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if hasattr(self.customers_page, '_filter_customers'):
                    self.customers_page._filter_customers()

    @Slot(int)
    def _edit_quote(self, quote_id: int):
        """Edit a quote with enhanced styling."""
        try:
            # Load the quote data
            with SessionLocal() as db:
                quote = self.quote_service.get_full_quote_details(db, quote_id)
            
            if quote:
                # Switch to quote creation page
                self._show_quote_creation()
                
                # Load quote data into the creation page
                if hasattr(self.quote_creation_page, 'load_quote'):
                    self.quote_creation_page.load_quote(quote)
                    
                logger.info(f"Loaded quote {quote_id} for editing")
            else:
                QMessageBox.warning(self, "Quote Not Found", 
                                  f"Quote with ID {quote_id} could not be found.")
                
        except Exception as e:
            logger.error(f"Error editing quote {quote_id}: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", 
                               f"An error occurred while loading the quote: {str(e)}")

    def _apply_theme(self, theme_name: str):
        """Apply the selected theme with enhanced styling."""
        ThemeManager.apply_theme(theme_name, self)
        logger.info(f"Applied theme: {theme_name}")

    def closeEvent(self, event):
        """Handle widget close event with proper cleanup."""
        # Clean up database connections if they exist
        if hasattr(self.quote_creation_page, 'db'):
            self.quote_creation_page.db.close()
        event.accept()