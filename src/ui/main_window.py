# src/ui/main_window.py
"""
MyBabbittQuote - Polished Main Window
🔴 Critical: Complete UI/UX refactor for smooth, professional application
"""

import logging
from PySide6.QtCore import Qt, QTimer, Slot, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFrame, QLabel, QListWidget, QListWidgetItem, QPushButton,
    QStackedWidget, QMessageBox, QDialog, QDialogButtonBox
)
from PySide6.QtGui import QFont, QIcon

from src.core.services.settings_service import SettingsService
from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.views.dashboard_redesign import DashboardRedesign
from src.ui.views.quote_creation_redesign import QuoteCreationPageRedesign
from src.ui.views.customers_page import CustomersPage
from src.ui.views.settings_page import SettingsPage

logger = logging.getLogger(__name__)


class ModernMessageBox(QDialog):
    """Custom message box with proper theming and readability."""
    
    def __init__(self, parent, title, message, buttons=QDialogButtonBox.Ok):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 200)
        self._setup_ui(message, buttons)
        self._apply_modern_styling()
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        
        # Apply modern UI integration enhancements
        from src.ui.utils.ui_integration import QuickMigrationHelper
        QuickMigrationHelper.fix_oversized_dropdowns(self)
        QuickMigrationHelper.modernize_existing_dialog(self)
        
    def _setup_ui(self, message, buttons):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 20)
        
        # Message label
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        message_label.setFont(font)
        layout.addWidget(message_label)
        
        # Button box
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
    def _apply_modern_styling(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 2px solid #2c5aa0;
                border-radius: 8px;
                color: #333333;
            }
            QLabel {
                color: #333333;
                background-color: transparent;
                padding: 10px;
            }
            QPushButton {
                background-color: #2c5aa0;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1e3d6f;
            }
            QPushButton:pressed {
                background-color: #0f1e3a;
            }
        """)


class MainWindow(QMainWindow):
    """
    Polished main window with proper sizing, smooth animations, and professional styling.
    """
    
    # Signal for theme changes
    theme_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.settings_service = SettingsService()
        
        # 🔴 Critical: Set proper window properties first
        self._setup_window_properties()
        
        # Initialize UI components
        self._setup_ui()
        self._connect_signals()
        
        # Apply saved theme
        self._load_and_apply_theme()
        
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        
        # Show dashboard by default
        self._show_dashboard()
        
        logger.info("MainWindow initialized successfully")
    
    def _setup_window_properties(self):
        """🔴 Critical: Proper window sizing and properties."""
        self.setWindowTitle("MyBabbittQuote - Babbitt International")
        
        # Set optimal window size (based on your screenshot preference)
        self.resize(1400, 800)
        self.setMinimumSize(1200, 700)
        
        # Center window on screen
        self._center_on_screen()
        
    def _center_on_screen(self):
        """Center the window on the primary screen."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def _setup_ui(self):
        """Set up the main UI layout with modern design."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar and content area
        self._create_modern_sidebar()
        self._create_content_area()
        
        # Add to main layout
        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_frame)
    
    def _create_modern_sidebar(self):
        """Create a modern, professional sidebar."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebarFrame")
        self.sidebar_frame.setFixedWidth(250)
        
        # Sidebar layout
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo/Title area
        self.logo_label = QLabel("Babbitt")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.logo_label)
        
        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        # Add navigation items
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("📋 New Quote", "new_quote"),
            ("👥 Customers", "customers"),
        ]
        
        for text, data in nav_items:
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, data)
            self.nav_list.addItem(item)
        
        sidebar_layout.addWidget(self.nav_list)
        
        # Spacer
        sidebar_layout.addStretch()
        
        # Settings button
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setObjectName("settingsButton")
        sidebar_layout.addWidget(self.settings_button)
    
    def _create_content_area(self):
        """Create the main content area."""
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Initialize pages
        self.dashboard_page = DashboardRedesign()
        self.quote_page = QuoteCreationPageRedesign()
        self.customers_page = CustomersPage()
        self.settings_page = SettingsPage()
        
        # Add pages to stack
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.quote_page)
        self.stacked_widget.addWidget(self.customers_page)
        self.stacked_widget.addWidget(self.settings_page)
        
        content_layout.addWidget(self.stacked_widget)
    
    def _connect_signals(self):
        """Connect all signals."""
        self.nav_list.itemSelectionChanged.connect(self._on_nav_changed)
        self.settings_button.clicked.connect(self._show_settings)
        self.settings_page.theme_changed.connect(self.apply_theme)
    
    @Slot(int)
    def _on_nav_changed(self, index):
        """Handle navigation changes."""
        pass  # Navigation logic handled elsewhere
    
    @Slot()
    def _show_dashboard(self):
        """Show dashboard page."""
        self.stacked_widget.setCurrentIndex(0)
    
    @Slot()
    def _show_settings(self):
        """Show settings page."""
        self.stacked_widget.setCurrentIndex(3)
    
    def _load_and_apply_theme(self):
        """Load and apply the saved theme."""
        try:
            theme_name = self.settings_service.get_theme()
            self.apply_theme(theme_name)
        except Exception as e:
            logger.warning(f"Failed to load theme: {e}")
            self.apply_theme("Corporate")  # Fallback theme
    
    @Slot(str)
    def apply_theme(self, theme_name):
        """Apply the specified theme."""
        # Simplified theme application - just use BabbittTheme
        app = QApplication.instance()
        if app:
            app.setStyleSheet(BabbittTheme.get_main_stylesheet())
        logger.info(f"Applied Babbitt theme")
    
    def _get_corporate_theme(self):
        """Get corporate theme stylesheet."""
        return """
        /* Corporate Theme - Professional Blue and Gray */
        QMainWindow {
            background-color: #f5f5f5;
            color: #333333;
        }
        
        QFrame#sidebarFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #2c3e50, stop:1 #34495e);
            border: none;
            min-width: 220px;
            max-width: 220px;
        }
        
        QLabel#logoLabel {
            color: #f39c12;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            background-color: transparent;
        }
        
        QListWidget#navList {
            background-color: transparent;
            border: none;
            color: white;
            font-size: 14px;
            outline: none;
        }
        
        QListWidget#navList::item {
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }
        
        QListWidget#navList::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        QListWidget#navList::item:selected {
            background-color: rgba(255, 255, 255, 0.2);
            border-left: 3px solid #f39c12;
            font-weight: 600;
        }
        
        QPushButton#settingsButton {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 10px 16px;
            margin: 16px 12px;
            border-radius: 6px;
            font-size: 13px;
        }
        
        QPushButton#settingsButton:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        QFrame#contentFrame {
            background-color: white;
            border: none;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #21618c;
        }
        
        QLineEdit, QComboBox, QSpinBox {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 8px 12px;
            background-color: white;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border-color: #3498db;
        }
        
        QTableWidget {
            border: 1px solid #bdc3c7;
            gridline-color: #ecf0f1;
            background-color: white;
        }
        
        QHeaderView::section {
            background-color: #ecf0f1;
            padding: 8px;
            border: none;
            font-weight: 600;
        }
        """
    
    def _get_modern_light_theme(self):
        """🟢 Modern light theme."""
        return """
        /* Modern Light Theme - Clean and Minimal */
        QMainWindow {
            background-color: #ffffff;
            color: #2c3e50;
        }
        
        QFrame#sidebarFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #34495e, stop:1 #2c3e50);
            border: none;
            min-width: 220px;
            max-width: 220px;
        }
        
        QLabel#logoLabel {
            color: #e74c3c;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            background-color: transparent;
        }
        
        QListWidget#navList {
            background-color: transparent;
            border: none;
            color: white;
            font-size: 14px;
            outline: none;
        }
        
        QListWidget#navList::item {
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }
        
        QListWidget#navList::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        QListWidget#navList::item:selected {
            background-color: rgba(255, 255, 255, 0.2);
            border-left: 3px solid #e74c3c;
            font-weight: 600;
        }
        
        QPushButton#settingsButton {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 10px 16px;
            margin: 16px 12px;
            border-radius: 6px;
            font-size: 13px;
        }
        
        QPushButton#settingsButton:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        QFrame#contentFrame {
            background-color: #f8f9fa;
            border: none;
        }
        
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #c0392b;
        }
        
        QPushButton:pressed {
            background-color: #a93226;
        }
        
        QLineEdit, QComboBox, QSpinBox {
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 8px 12px;
            background-color: white;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border-color: #e74c3c;
        }
        
        QTableWidget {
            border: 1px solid #dee2e6;
            gridline-color: #f8f9fa;
            background-color: white;
        }
        
        QHeaderView::section {
            background-color: #f8f9fa;
            padding: 8px;
            border: none;
            font-weight: 600;
        }
        """
    
    def _get_babbitt_professional_theme(self):
        """Get Babbitt professional theme stylesheet."""
        return """
        /* Babbitt Professional Theme - Orange and Blue */
        QMainWindow {
            background-color: #f8f9fa;
            color: #2c3e50;
        }
        
        QFrame#sidebarFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #2c3e50, stop:1 #34495e);
            border: none;
            min-width: 220px;
            max-width: 220px;
        }
        
        QLabel#logoLabel {
            color: #f39c12;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            background-color: transparent;
        }
        
        QListWidget#navList {
            background-color: transparent;
            border: none;
            color: white;
            font-size: 14px;
            outline: none;
        }
        
        QListWidget#navList::item {
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }
        
        QListWidget#navList::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        QListWidget#navList::item:selected {
            background-color: rgba(255, 255, 255, 0.2);
            border-left: 3px solid #f39c12;
            font-weight: 600;
        }
        
        QPushButton#settingsButton {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 10px 16px;
            margin: 16px 12px;
            border-radius: 6px;
            font-size: 13px;
        }
        
        QPushButton#settingsButton:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        QFrame#contentFrame {
            background-color: white;
            border: none;
        }
        
        QPushButton {
            background-color: #f39c12;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #e67e22;
        }
        
        QPushButton:pressed {
            background-color: #d68910;
        }
        
        QLineEdit, QComboBox, QSpinBox {
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            padding: 8px 12px;
            background-color: white;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border-color: #f39c12;
        }
        
        QTableWidget {
            border: 1px solid #bdc3c7;
            gridline-color: #ecf0f1;
            background-color: white;
        }
        
        QHeaderView::section {
            background-color: #ecf0f1;
            padding: 8px;
            border: none;
            font-weight: 600;
        }
        """
    
    def show_notification(self, message, message_type="info"):
        """Show a notification message."""
        if message_type == "error":
            QMessageBox.critical(self, "Error", message)
        elif message_type == "warning":
            QMessageBox.warning(self, "Warning", message)
        else:
            QMessageBox.information(self, "Information", message)
    
    def closeEvent(self, event):
        """Handle window close event."""
        try:
            # Save any pending changes
            logger.info("MainWindow closing...")
            event.accept()
        except Exception as e:
            logger.error(f"Error during close: {e}")
            event.accept()


def create_application():
    """Create and configure the main application."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("MyBabbittQuote")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Babbitt International")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app, window


if __name__ == "__main__":
    app, window = create_application()
    sys.exit(app.exec())