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
        """Connect UI signals and slots."""
        self.nav_list.currentRowChanged.connect(self._on_nav_changed)
        self.settings_button.clicked.connect(self._show_settings)
        
        # Connect settings page theme changes
        if hasattr(self.settings_page, 'theme_changed'):
            self.settings_page.theme_changed.connect(self.apply_theme)
    
    @Slot(int)
    def _on_nav_changed(self, index):
        """Handle navigation changes with smooth transitions."""
        if index >= 0:
            self.stacked_widget.setCurrentIndex(index)
    
    @Slot()
    def _show_dashboard(self):
        """Show dashboard page."""
        self.nav_list.setCurrentRow(0)
    
    @Slot()
    def _show_settings(self):
        """Show settings page."""
        self.stacked_widget.setCurrentWidget(self.settings_page)
    
    def _load_and_apply_theme(self):
        """Load saved theme and apply it."""
        try:
            theme_name = self.settings_service.get_theme()
            self.apply_theme(theme_name)
        except Exception as e:
            logger.warning(f"Failed to load saved theme: {e}")
            self.apply_theme("Corporate")  # Fallback theme
    
    @Slot(str)
    def apply_theme(self, theme_name):
        """🔴 Critical: Apply theme with proper styling."""
        try:
            # Get theme stylesheet
            if theme_name == "Corporate":
                stylesheet = self._get_corporate_theme()
            elif theme_name == "Modern Light":
                stylesheet = self._get_modern_light_theme()
            elif theme_name == "Babbitt Professional":
                stylesheet = self._get_babbitt_professional_theme()
            else:
                stylesheet = self._get_corporate_theme()  # Default fallback
            
            # Apply to application
            QApplication.instance().setStyleSheet(stylesheet)
            
            # Save theme preference
            self.settings_service.set_theme(theme_name)
            
            logger.info(f"Applied theme: {theme_name}")
            
        except Exception as e:
            logger.error(f"Failed to apply theme {theme_name}: {e}")
    
    def _get_corporate_theme(self):
        """🟡 Corporate theme with professional styling."""
        return """
        /* === MAIN WINDOW === */
        QMainWindow {
            background-color: #f5f6fa;
            color: #2f3542;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }
        
        /* === SIDEBAR === */
        QFrame#sidebarFrame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2c5aa0, stop:1 #1e3d6f);
            border: none;
        }
        
        QLabel#logoLabel {
            color: #ffa726;
            font-size: 28px;
            font-weight: bold;
            padding: 25px 20px;
            background-color: transparent;
        }
        
        QListWidget#navList {
            background-color: transparent;
            border: none;
            color: white;
            font-size: 15px;
            outline: none;
            padding: 10px 0;
        }
        
        QListWidget#navList::item {
            padding: 15px 25px;
            border-left: 4px solid transparent;
            margin: 2px 0;
            border-radius: 0 25px 25px 0;
            margin-right: 10px;
        }
        
        QListWidget#navList::item:hover {
            background-color: rgba(255, 255, 255, 0.15);
            border-left: 4px solid #ffa726;
        }
        
        QListWidget#navList::item:selected {
            background-color: rgba(255, 255, 255, 0.2);
            border-left: 4px solid #ffa726;
            font-weight: 600;
        }
        
        QPushButton#settingsButton {
            background-color: transparent;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 12px 20px;
            margin: 15px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
        }
        
        QPushButton#settingsButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
            border-color: #ffa726;
        }
        
        /* === CONTENT AREA === */
        QFrame#contentFrame {
            background-color: #ffffff;
            border: none;
        }
        
        /* === GENERAL WIDGET STYLING === */
        QPushButton {
            background-color: #2c5aa0;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            min-height: 15px;
        }
        
        QPushButton:hover {
            background-color: #1e3d6f;
        }
        
        QPushButton:pressed {
            background-color: #0f1e3a;
        }
        
        QLineEdit {
            padding: 8px 12px;
            border: 2px solid #e1e5e9;
            border-radius: 4px;
            background-color: white;
            color: #2f3542;
        }
        
        QLineEdit:focus {
            border-color: #2c5aa0;
        }
        
        QComboBox {
            padding: 8px 12px;
            border: 2px solid #e1e5e9;
            border-radius: 4px;
            background-color: white;
            color: #2f3542;
            max-height: 32px;
        }
        
        QComboBox:focus {
            border-color: #2c5aa0;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #2f3542;
        }
        """
    
    def _get_modern_light_theme(self):
        """🟢 Modern light theme."""
        return """
        QMainWindow {
            background-color: #fafbfc;
            color: #24292e;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QFrame#sidebarFrame {
            background-color: #0366d6;
            border: none;
        }
        
        QLabel#logoLabel {
            color: #ffffff;
            font-size: 26px;
            font-weight: bold;
            padding: 25px 20px;
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
            margin: 1px 0;
        }
        
        QListWidget#navList::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        QListWidget#navList::item:selected {
            background-color: rgba(255, 255, 255, 0.15);
            border-left: 3px solid #ffffff;
        }
        
        QPushButton#settingsButton {
            background-color: transparent;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.5);
            padding: 10px 15px;
            margin: 10px;
            border-radius: 4px;
        }
        
        QPushButton#settingsButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        """
    
    def _get_babbitt_professional_theme(self):
        """🔴 Babbitt Professional theme."""
        return """
        QMainWindow {
            background-color: #f8f9fa;
            color: #212529;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QFrame#sidebarFrame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1a237e, stop:1 #283593);
            border: none;
        }
        
        QLabel#logoLabel {
            color: #ffc107;
            font-size: 30px;
            font-weight: bold;
            padding: 30px 20px;
        }
        
        QListWidget#navList {
            background-color: transparent;
            border: none;
            color: white;
            font-size: 15px;
            outline: none;
        }
        
        QListWidget#navList::item {
            padding: 16px 25px;
            border-left: 4px solid transparent;
            margin: 3px 0;
        }
        
        QListWidget#navList::item:hover {
            background-color: rgba(255, 255, 255, 0.12);
        }
        
        QListWidget#navList::item:selected {
            background-color: rgba(255, 255, 255, 0.18);
            border-left: 4px solid #ffc107;
            font-weight: 600;
        }
        
        QPushButton#settingsButton {
            background-color: transparent;
            color: white;
            border: 2px solid #ffc107;
            padding: 12px 20px;
            margin: 15px;
            border-radius: 6px;
            font-weight: 500;
        }
        
        QPushButton#settingsButton:hover {
            background-color: #ffc107;
            color: #1a237e;
        }
        """
    
    def show_notification(self, message, message_type="info"):
        """Show modern notification messages."""
        if message_type == "info":
            msg = ModernMessageBox(self, "Information", message)
        elif message_type == "warning":
            msg = ModernMessageBox(self, "Warning", message)
        elif message_type == "error":
            msg = ModernMessageBox(self, "Error", message)
        elif message_type == "success":
            msg = ModernMessageBox(self, "Success", message)
        else:
            msg = ModernMessageBox(self, "Message", message)
        
        msg.exec()
    
    def closeEvent(self, event):
        """🔴 Critical: Custom exit dialog with proper styling."""
        # Create custom exit confirmation dialog
        msg = ModernMessageBox(
            self, 
            "Confirm Exit", 
            "Are you sure you want to exit MyBabbittQuote?",
            QDialogButtonBox.Yes | QDialogButtonBox.No
        )
        
        # Apply special styling for exit dialog
        msg.setStyleSheet(msg.styleSheet() + """
            QDialog {
                border-color: #ff6b6b;
            }
            QPushButton {
                min-width: 100px;
            }
        """)
        
        reply = msg.exec()
        
        if reply == QDialog.Accepted:
            logger.info("Application closing")
            event.accept()
        else:
            event.ignore()


def create_application():
    """🔴 Critical: Create and configure application with proper setup."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Set application properties
    app.setApplicationName("MyBabbittQuote")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Babbitt International")
    
    return app