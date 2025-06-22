"""
Theme Manager for MyBabbittQuote Application

Manages the application's visual theme and facilitates switching
between light and dark modes.
"""

from PySide6.QtWidgets import QApplication, QListWidget, QPushButton, QFrame, QLineEdit, QComboBox, QSpinBox
from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialPremium, BabbittPremiumIntegration


class ThemeManager:
    """
    Manages the application's visual themes.
    """

    @staticmethod
    def get_available_themes() -> list[str]:
        """Returns a list of available theme names."""
        return [
            "Babbitt Industrial"
        ]

    @staticmethod
    def apply_theme(theme_name: str, main_window=None):
        """
        Applies a theme to the entire application.
        
        Args:
            theme_name: Name of the theme to apply
            main_window: Optional main window instance for theme animations
        """
        app = QApplication.instance()
        assert isinstance(app, QApplication)
        if not app:
            return

        # Apply Industrial theme with animations
        stylesheet = BabbittIndustrialPremium.get_main_stylesheet()
        app.setStyleSheet(stylesheet)
        
        # If main window is provided, apply Industrial theme animations
        if main_window:
            BabbittPremiumIntegration.apply_premium_theme(main_window)
        
    @staticmethod
    def _apply_enhanced_animations(main_window, theme_name):
        """Apply enhanced animations to Corporate and Dark themes."""
        from src.ui.theme.animation_system import setup_widget_animations
        
        # Setup navigation animations
        nav_list = main_window.findChild(QListWidget, "navList")
        if nav_list:
            # Apply basic navigation animations
            for i in range(nav_list.count()):
                item = nav_list.item(i)
                if item:
                    # Apply subtle hover effects
                    pass  # Basic hover effects are handled by CSS
        
        # Setup button animations
        for button in main_window.findChildren(QPushButton):
            if button.objectName() in ['newQuoteButton', 'settingsButton']:
                setup_widget_animations(button, "button")
        
        # Setup card animations
        for frame in main_window.findChildren(QFrame):
            if frame.objectName() in ['metricCard', 'contentCard']:
                setup_widget_animations(frame, "card")
        
        # Setup form animations
        for line_edit in main_window.findChildren(QLineEdit):
            setup_widget_animations(line_edit, "form")
        
        for combo in main_window.findChildren(QComboBox):
            setup_widget_animations(combo, "form")
        
        for spinbox in main_window.findChildren(QSpinBox):
            setup_widget_animations(spinbox, "form")
        
    @staticmethod
    def _remove_industrial_animations(main_window):
        """Remove Industrial theme animations when switching to other themes."""
        # Remove event filters from form widgets
        from PySide6.QtWidgets import QLineEdit, QComboBox, QSpinBox
        
        for line_edit in main_window.findChildren(QLineEdit):
            if hasattr(line_edit, '_focus_filter'):
                line_edit.removeEventFilter(line_edit._focus_filter)
                line_edit._focus_filter = None
                line_edit.setGraphicsEffect(None)  # Remove focus glow
        
        for combo in main_window.findChildren(QComboBox):
            if hasattr(combo, '_focus_filter'):
                combo.removeEventFilter(combo._focus_filter)
                combo._focus_filter = None
                combo.setGraphicsEffect(None)
        
        for spinbox in main_window.findChildren(QSpinBox):
            if hasattr(spinbox, '_focus_filter'):
                spinbox.removeEventFilter(spinbox._focus_filter)
                spinbox._focus_filter = None
                spinbox.setGraphicsEffect(None)
        
        # Remove animated widget references
        for widget in main_window.findChildren(QLineEdit):
            if hasattr(widget, 'animated_widget'):
                delattr(widget, 'animated_widget')
        
        for widget in main_window.findChildren(QComboBox):
            if hasattr(widget, 'animated_widget'):
                delattr(widget, 'animated_widget')
        
        for widget in main_window.findChildren(QSpinBox):
            if hasattr(widget, 'animated_widget'):
                delattr(widget, 'animated_widget')
        
    @staticmethod
    def get_theme_preview_info(theme_name: str) -> dict:
        """
        Gets basic color information for a theme preview.
        """
        return {
            'primary_color': BabbittIndustrialPremium.PRIMARY_BLUE,
            'accent_color': BabbittIndustrialPremium.GOLD_ACCENT,
            'background_color': BabbittIndustrialPremium.PLATINUM,
            'description': 'Premium industrial theme with sophisticated gradients and animations'
        } 