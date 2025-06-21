"""
Window Layout Helper - Fixes Main Window Sizing and Layout Issues
File: src/ui/helpers/window_layout_helper.py

🔴 Critical - Fixes the window sizing and layout problems
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QScreen


class WindowLayoutHelper:
    """Helper class to fix window sizing and layout issues."""
    
    @staticmethod
    def fix_main_window_sizing(main_window: QMainWindow):
        """
        Fix main window sizing to be reasonable and usable.
        
        🔴 Critical - Call this in your main window's __init__
        """
        # Get screen geometry
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        # Calculate reasonable window size (80% of screen, but not too large)
        max_width = min(1400, int(screen_geometry.width() * 0.8))
        max_height = min(800, int(screen_geometry.height() * 0.8))
        
        # Set reasonable minimum and default sizes
        main_window.setMinimumSize(1000, 600)
        main_window.resize(max_width, max_height)
        
        # Center the window on screen
        window_geometry = main_window.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        main_window.move(window_geometry.topLeft())
        
        print(f"Window sized to: {max_width}x{max_height}")
        print(f"Screen size: {screen_geometry.width()}x{screen_geometry.height()}")
    
    @staticmethod
    def fix_dialog_sizing(dialog: QDialog, width: int = 800, height: int = 600):
        """
        Fix dialog sizing to be reasonable.
        
        Args:
            dialog: The dialog to fix
            width: Preferred width
            height: Preferred height
        """
        # Get parent window if available for centering
        parent = dialog.parent()
        
        # Set reasonable size
        dialog.setMinimumSize(600, 400)
        dialog.resize(width, height)
        
        # Center on parent or screen
        if parent and hasattr(parent, 'geometry'):
            parent_geometry = parent.geometry()
            dialog_geometry = dialog.frameGeometry()
            center_point = parent_geometry.center()
            dialog_geometry.moveCenter(center_point)
            dialog.move(dialog_geometry.topLeft())
        else:
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            dialog_geometry = dialog.frameGeometry()
            center_point = screen_geometry.center()
            dialog_geometry.moveCenter(center_point)
            dialog.move(dialog_geometry.topLeft())
    
    @staticmethod
    def ensure_window_visible(window):
        """
        Ensure window is visible and properly sized on screen.
        
        🔴 Critical - Fixes windows opening off-screen or too large
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = window.geometry()
        
        # Check if window is too large for screen
        if window_geometry.width() > screen_geometry.width():
            window.resize(int(screen_geometry.width() * 0.9), window_geometry.height())
        
        if window_geometry.height() > screen_geometry.height():
            window.resize(window_geometry.width(), int(screen_geometry.height() * 0.9))
        
        # Check if window is off-screen
        if not screen_geometry.intersects(window.geometry()):
            window.move(screen_geometry.topLeft())
        
        # Ensure window is not below taskbar
        window_bottom = window.geometry().bottom()
        screen_bottom = screen_geometry.bottom()
        
        if window_bottom > screen_bottom:
            current_pos = window.pos()
            new_y = screen_bottom - window.geometry().height()
            window.move(current_pos.x(), max(0, new_y))


class ResponsiveLayoutHelper:
    """Helper for responsive layout behavior."""
    
    @staticmethod
    def apply_responsive_behavior(main_window):
        """
        Apply responsive behavior to main window.
        
        🟡 Nice-to-have - Makes layout adapt to window size changes
        """
        def on_resize():
            """Handle window resize events."""
            window_width = main_window.width()
            
            # Find sidebar frame
            sidebar = main_window.findChild(main_window.__class__, "sidebarFrame")
            if sidebar:
                # Collapse sidebar on very small screens
                if window_width < 1000:
                    sidebar.setMaximumWidth(120)  # Collapsed sidebar
                else:
                    sidebar.setMaximumWidth(180)  # Normal sidebar
        
        # Connect to resize events (if available)
        if hasattr(main_window, 'resizeEvent'):
            original_resize = main_window.resizeEvent
            
            def new_resize_event(event):
                original_resize(event)
                on_resize()
            
            main_window.resizeEvent = new_resize_event


# ===== USAGE EXAMPLES =====

def fix_main_window_layout(main_window):
    """
    Complete fix for main window layout issues.
    
    🔴 Critical - Add this to your MainWindow.__init__() after super().__init__()
    """
    # Fix window sizing
    WindowLayoutHelper.fix_main_window_sizing(main_window)
    
    # Ensure window is visible
    WindowLayoutHelper.ensure_window_visible(main_window)
    
    # Apply responsive behavior
    ResponsiveLayoutHelper.apply_responsive_behavior(main_window)
    
    # Set window properties for better UX
    main_window.setWindowTitle("MyBabbittQuote - Babbitt International")
    
    print("Main window layout fixes applied successfully")


def fix_configuration_dialog_layout(dialog):
    """
    Fix configuration dialog layout issues.
    
    🟡 Important - Add this to configuration dialogs
    """
    # Fix dialog sizing
    WindowLayoutHelper.fix_dialog_sizing(dialog, 900, 650)
    
    # Ensure dialog is visible
    WindowLayoutHelper.ensure_window_visible(dialog)
    
    print("Configuration dialog layout fixes applied")


# ===== SCREEN DETECTION UTILITIES =====

class ScreenHelper:
    """Helper for screen detection and sizing."""
    
    @staticmethod
    def get_optimal_window_size():
        """Get optimal window size for current screen."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        # Calculate optimal size (80% of screen, but reasonable limits)
        optimal_width = min(1400, max(1000, int(screen_geometry.width() * 0.8)))
        optimal_height = min(800, max(600, int(screen_geometry.height() * 0.8)))
        
        return QSize(optimal_width, optimal_height)
    
    @staticmethod
    def is_small_screen():
        """Check if we're on a small screen."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        return screen_geometry.width() < 1200 or screen_geometry.height() < 700
    
    @staticmethod
    def get_screen_info():
        """Get detailed screen information for debugging."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        full_geometry = screen.geometry()
        
        return {
            'available_width': screen_geometry.width(),
            'available_height': screen_geometry.height(),
            'full_width': full_geometry.width(),
            'full_height': full_geometry.height(),
            'is_small_screen': ScreenHelper.is_small_screen(),
            'optimal_size': ScreenHelper.get_optimal_window_size()
        }


# ===== INTEGRATION EXAMPLE =====

"""
Add this to your main window's __init__ method:

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Apply theme first
        from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
        ModernBabbittTheme.apply_to_widget(self)
        
        # Fix layout issues - CRITICAL
        from src.ui.helpers.window_layout_helper import fix_main_window_layout
        fix_main_window_layout(self)
        
        # Set up UI
        self._setup_ui()
        
        # Show window
        self.show()
"""