"""
Theme Manager for MyBabbittQuote Application

Manages the application's visual theme and facilitates switching
between light and dark modes.
"""

from PySide6.QtWidgets import QApplication
from src.ui.theme.babbitt_theme import BabbittTheme


class ThemeManager:
    """
    Manages the application's light and dark themes.
    """

    @staticmethod
    def apply_theme(mode: str):
        """
        Apply a theme mode to the entire application.

        Args:
            mode (str): The mode to apply, either 'Light' or 'Dark'.
        """
        app = QApplication.instance()
        if app is None:
            # This case should ideally not happen in a running application
            return

        # Ensure we have a QApplication instance
        if not hasattr(app, 'setStyleSheet'):
            return

        stylesheet = ""
        if mode == 'Light':
            stylesheet = BabbittTheme.get_light_stylesheet()
        elif mode == 'Dark':
            stylesheet = BabbittTheme.get_dark_stylesheet()
        else:
            # Default to light mode if an invalid mode is provided
            stylesheet = BabbittTheme.get_light_stylesheet()

        app.setStyleSheet(stylesheet)  # type: ignore

    @classmethod
    def get_theme_preview_info(cls, theme_name):
        """
        Get preview information for a theme.
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            dict: Theme preview information
        """
        theme_class = BabbittTheme
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

    @classmethod
    def get_available_themes(cls):
        """
        Get list of available theme names.
        
        Returns:
            list: List of available theme names
        """
        return ['Light', 'Dark'] 