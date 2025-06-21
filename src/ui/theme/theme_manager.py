"""
Theme Manager for MyBabbittQuote Application

Manages multiple themes and provides a unified interface for theme switching.
"""

from PySide6.QtWidgets import QApplication

# Import the existing theme classes
from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.theme.babbitt_professional_theme import BabbittProfessionalTheme
from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
from src.ui.theme.modern_light_theme import ModernLightTheme
from src.ui.theme.corporate_theme import CorporateTheme

class ThemeManager:
    """
    Manages application themes and provides theme switching functionality.
    """

    # Available themes mapping using the existing theme classes
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
        
        # Apply the theme using the theme's apply method
        if hasattr(theme_class, 'apply_to_application'):
            theme_class.apply_to_application(app)
        elif hasattr(theme_class, 'apply'):
            theme_class.apply(app)
        else:
            # Fallback: apply stylesheet directly if it's a QApplication
            if hasattr(app, 'setStyleSheet'):
                app.setStyleSheet(theme_class.get_stylesheet())
        
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
        
        # Apply the theme using the theme's apply method
        if hasattr(theme_class, 'apply_to_widget'):
            theme_class.apply_to_widget(widget)
        elif hasattr(theme_class, 'apply'):
            theme_class.apply(widget)
        else:
            # Fallback: apply stylesheet directly
            widget.setStyleSheet(theme_class.get_stylesheet())
        
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
        
        # Use the theme's info method if available
        if hasattr(theme_class, 'get_theme_info'):
            return theme_class.get_theme_info()
        elif hasattr(theme_class, 'get_info'):
            return theme_class.get_info()
        else:
            # Fallback: return basic info
            return {
                'name': theme_name,
                'description': f'{theme_name} theme',
                'author': 'Babbitt Quote Generator'
            } 