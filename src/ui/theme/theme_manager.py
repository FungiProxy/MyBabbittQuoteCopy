"""
Theme Manager for MyBabbittQuote Application

Manages multiple themes and provides a unified interface for theme switching.
"""

from PySide6.QtWidgets import QApplication

# Correctly import all standardized theme classes
from src.ui.theme.babbitt_theme_standardized import BabbittThemeStandardized
from src.ui.theme.babbitt_professional_theme_standardized import BabbittProfessionalThemeStandardized
from src.ui.theme.modern_babbitt_theme_standardized import ModernBabbittThemeStandardized
from src.ui.theme.modern_light_theme_standardized import ModernLightThemeStandardized
from src.ui.theme.corporate_theme_standardized import CorporateThemeStandardized

class ThemeManager:
    """
    Manages application themes and provides theme switching functionality.
    """

    # Available themes mapping using the new standardized theme classes
    THEMES = {
        'Babbitt Theme': BabbittThemeStandardized,
        'Babbitt Professional': BabbittProfessionalThemeStandardized,
        'Modern Babbitt': ModernBabbittThemeStandardized,
        'Modern Light': ModernLightThemeStandardized,
        'Corporate': CorporateThemeStandardized,
    }

    @classmethod
    def get_available_themes(cls):
        """Get list of available theme names."""
        return list(cls.THEMES.keys())

    @classmethod
    def get_theme_class(cls, theme_name):
        """Get the theme class for a given theme name."""
        return cls.THEMES.get(theme_name)

    @classmethod
    def apply_theme(cls, theme_name, app=None):
        """
        Apply a theme to the application.
        
        Args:
            theme_name: Name of the theme to apply
            app: QApplication instance (optional, will use QApplication.instance() if not provided)
        """
        if app is None:
            app = QApplication.instance()
        
        if app is None:
            raise RuntimeError("No QApplication instance available")
        
        theme_class = cls.get_theme_class(theme_name)
        if theme_class is None:
            raise ValueError(f"Unknown theme: {theme_name}")
        
        # Apply the theme using the standardized method from the base class
        theme_class.apply_to_application(app)
        
        return theme_class

    @classmethod
    def apply_theme_to_widget(cls, theme_name, widget):
        """
        Apply a theme to a specific widget.
        
        Args:
            theme_name: Name of the theme to apply
            widget: Widget to apply theme to
        """
        theme_class = cls.get_theme_class(theme_name)
        if theme_class is None:
            raise ValueError(f"Unknown theme: {theme_name}")
        
        # Apply the theme using the standardized method from the base class
        theme_class.apply_to_widget(widget)
        
        return theme_class

    @classmethod
    def get_theme_preview_info(cls, theme_name):
        """
        Get preview information for a theme.
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            dict: Theme preview information
        """
        theme_class = cls.get_theme_class(theme_name)
        if theme_class is None:
            return None
        
        # Use the standardized theme info method from the base class
        return theme_class.get_theme_info() 