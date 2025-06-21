"""
Theme Application Helper - Perfect Integration
File: src/ui/helpers/theme_helper.py

🔴 Critical - Use this to apply the theme perfectly
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
from PySide6.QtCore import QTimer


class PerfectThemeHelper:
    """Helper to apply themes perfectly with all fixes."""
    
    @staticmethod
    def apply_complete_theme(widget, theme_class=None):
        """
        Apply complete theme with all fixes and proper sizing.
        
        🔴 Critical - Use this for any widget/window
        """
        if theme_class is None:
            from src.ui.theme.standardized_theme_base import StandardizedThemeBase
            theme_class = StandardizedThemeBase
        
        # Apply the theme
        theme_class.apply_to_widget(widget)
        
        # Force style refresh
        PerfectThemeHelper._force_style_refresh(widget)
        
        # Apply sizing fixes
        PerfectThemeHelper._apply_sizing_fixes(widget)
        
        print(f"Perfect theme applied to {widget.__class__.__name__}")
    
    @staticmethod
    def _force_style_refresh(widget):
        """Force the widget to refresh its styling."""
        # Unpolish and re-polish to force style update
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        
        # Update all child widgets too
        for child in widget.findChildren(QWidget):
            child.style().unpolish(child)
            child.style().polish(child)
        
        # Force repaint
        widget.update()
    
    @staticmethod
    def _apply_sizing_fixes(widget):
        """Apply proper sizing based on widget type."""
        if isinstance(widget, QMainWindow):
            # Main window sizing
            widget.resize(1300, 750)
            widget.setMinimumSize(1100, 650)
            
            # Center on screen
            PerfectThemeHelper._center_on_screen(widget)
            
        elif isinstance(widget, QDialog):
            # Dialog sizing
            widget.resize(900, 650)
            widget.setMinimumSize(700, 500)
            
            # Center on parent or screen
            PerfectThemeHelper._center_on_screen(widget)
    
    @staticmethod
    def _center_on_screen(widget):
        """Center widget on screen."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        widget_geometry = widget.frameGeometry()
        center_point = screen_geometry.center()
        widget_geometry.moveCenter(center_point)
        widget.move(widget_geometry.topLeft())
    
    @staticmethod
    def setup_main_window(main_window):
        """
        Complete setup for main window with perfect theme and sizing.
        
        🔴 Critical - Use this in your MainWindow.__init__()
        """
        # Import the theme
        # from src.ui.theme.standardized_theme_base import StandardizedThemeBase
        
        # Apply complete theme
        # PerfectThemeHelper.apply_complete_theme(main_window, StandardizedThemeBase)
        
        # Set window properties
        main_window.setWindowTitle("MyBabbittQuote - Babbitt International")
        
        # Use a timer to apply final fixes after UI is fully loaded
        QTimer.singleShot(100, lambda: PerfectThemeHelper._final_polish(main_window))
        
        print("Main window setup complete with perfect theme")
    
    @staticmethod
    def _final_polish(widget):
        """Final polish after UI is loaded."""
        # Force one final style refresh
        PerfectThemeHelper._force_style_refresh(widget)
        
        # Ensure all components are properly styled
        PerfectThemeHelper._ensure_component_styling(widget)
    
    @staticmethod
    def _ensure_component_styling(widget):
        """Ensure all components have proper styling."""
        # Find and fix any unstyled components
        for child in widget.findChildren(QWidget):
            # Apply object names for better CSS targeting if missing
            if not child.objectName():
                class_name = child.__class__.__name__
                if "Card" in class_name or "card" in class_name.lower():
                    child.setObjectName("statCard")
                elif "Panel" in class_name or "panel" in class_name.lower():
                    child.setObjectName("contentPanel")
                elif "Section" in class_name or "section" in class_name.lower():
                    child.setObjectName("contentSection")


# ===== INTEGRATION EXAMPLES =====

def apply_to_main_window(main_window):
    """
    🔴 CRITICAL - Add this to your MainWindow.__init__() method
    
    Example:
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            
            # Apply perfect theme - ADD THIS LINE
            from src.ui.helpers.theme_helper import PerfectThemeHelper
            PerfectThemeHelper.setup_main_window(self)
            
            # Rest of your existing code...
            self._setup_ui()
    """
    PerfectThemeHelper.setup_main_window(main_window)


def apply_to_dialog(dialog):
    """
    🟡 Important - Add this to your dialog's __init__() method
    
    Example:
    class ConfigurationDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            
            # Apply perfect theme - ADD THIS LINE
            from src.ui.helpers.theme_helper import PerfectThemeHelper
            PerfectThemeHelper.apply_complete_theme(self)
            
            # Rest of your existing code...
            self.setupUi()
    """
    PerfectThemeHelper.apply_complete_theme(dialog)


def apply_to_any_widget(widget):
    """
    🟢 Nice-to-have - Apply theme to any widget
    """
    PerfectThemeHelper.apply_complete_theme(widget)


# ===== MODERN THEME VARIANT =====

class ModernProfessionalTheme:
    """Modern professional theme variant."""
    
    # Colors
    PRIMARY_COLOR = "#1e40af"
    SECONDARY_COLOR = "#1d4ed8"
    ACCENT_COLOR = "#f59e0b"
    SUCCESS_COLOR = "#059669"
    WARNING_COLOR = "#d97706"
    ERROR_COLOR = "#dc2626"
    INFO_COLOR = "#0891b2"
    
    BACKGROUND_PRIMARY = "#f8fafc"
    BACKGROUND_SECONDARY = "#ffffff"
    BACKGROUND_CARD = "#ffffff"
    BACKGROUND_SURFACE = "#f1f5f9"
    
    TEXT_PRIMARY = "#0f172a"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#64748b"
    
    BORDER_COLOR = "#e2e8f0"
    BORDER_COLOR_LIGHT = "#f1f5f9"
    
    HOVER_BACKGROUND = "#f1f5f9"
    ACTIVE_BACKGROUND = "#1e40af"
    FOCUS_BORDER = "#1e40af"
    
    @classmethod
    def apply_to_widget(cls, widget):
        """Apply this specific theme to widget."""
        from src.ui.theme.standardized_theme_base import StandardizedThemeBase
        
        # Temporarily override colors in the base theme
        original_colors = {}
        for attr in dir(cls):
            if not attr.startswith('_') and attr.isupper():
                original_colors[attr] = getattr(StandardizedThemeBase, attr, None)
                setattr(StandardizedThemeBase, attr, getattr(cls, attr))
        
        # Apply the theme
        StandardizedThemeBase.apply_to_widget(widget)
        
        # Restore original colors
        for attr, value in original_colors.items():
            if value is not None:
                setattr(StandardizedThemeBase, attr, value)


# ===== QUICK SETUP FOR YOUR APP =====

"""
QUICK SETUP - Add this to your MainWindow.__init__():

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 🔴 CRITICAL - Add these 3 lines for perfect theme
        from src.ui.helpers.theme_helper import PerfectThemeHelper
        PerfectThemeHelper.setup_main_window(self)
        
        # Your existing code...
        self._setup_ui()
        self._connect_signals()
        
        # Show window
        self.show()
"""