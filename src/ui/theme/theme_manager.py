"""
Theme Manager for MyBabbittQuote Application

Manages multiple themes and provides a unified interface for theme switching.
"""

from PySide6.QtWidgets import QApplication

from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.theme.babbitt_professional_theme import BabbittProfessionalTheme
from src.ui.theme.modern_light_theme import ModernLightTheme
from src.ui.theme.corporate_theme import CorporateTheme
from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme


class ThemeManager:
    """
    Manages application themes and provides theme switching functionality.
    """

    # Available themes mapping
    THEMES = {
        'Babbitt Theme': BabbittTheme,
        'Babbitt Professional': BabbittProfessionalTheme,
        'Modern Babbitt': ModernBabbittTheme,
        'Modern Light': ModernLightTheme,
        'Corporate': CorporateTheme,
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
        
        # Apply the theme stylesheet
        stylesheet = theme_class.get_main_stylesheet()
        app.setStyleSheet(stylesheet)
        
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
        
        # Apply the theme stylesheet to the widget
        stylesheet = theme_class.get_main_stylesheet()
        widget.setStyleSheet(stylesheet)
        
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
        
        # Extract color information for preview
        preview_info = {
            'name': theme_name,
            'description': theme_class.__doc__ or f'{theme_name} theme',
            'primary_color': getattr(theme_class, 'PRIMARY_BLUE', 
                                   getattr(theme_class, 'PRIMARY_PURPLE',
                                   getattr(theme_class, 'PRIMARY_EMERALD',
                                   getattr(theme_class, 'PRIMARY_NAVY', '#000000')))),
            'accent_color': getattr(theme_class, 'ACCENT_GOLD',
                                  getattr(theme_class, 'ACCENT_TEAL',
                                  getattr(theme_class, 'ACCENT_MINT',
                                  getattr(theme_class, 'ACCENT_RED', '#000000')))),
            'background_color': getattr(theme_class, 'LIGHT_GRAY',
                                      getattr(theme_class, 'DARK_BG',
                                      getattr(theme_class, 'LIGHT_BG', '#FFFFFF'))),
        }
        
        return preview_info 