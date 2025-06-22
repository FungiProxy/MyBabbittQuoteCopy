"""
Theme Manager for MyBabbittQuote Application

Manages the application's visual theme and facilitates switching
between light and dark modes.
"""

from PySide6.QtWidgets import QApplication
from src.ui.theme.babbitt_theme import BabbittTheme
from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialTheme


class ThemeManager:
    """
    Manages the application's visual themes.
    """

    @staticmethod
    def get_available_themes() -> list[str]:
        """Returns a list of available theme names."""
        return [
            BabbittTheme.CORPORATE_THEME, 
            BabbittTheme.DARK_THEME,
            "Babbitt Industrial"
        ]

    @staticmethod
    def apply_theme(theme_name: str):
        """
        Applies a theme to the entire application.
        """
        app = QApplication.instance()
        if not app:
            return

        if theme_name == "Babbitt Industrial":
            stylesheet = BabbittIndustrialTheme.get_main_stylesheet()
        else:
            stylesheet = BabbittTheme.get_stylesheet(theme_name)
        
        app.setStyleSheet(stylesheet)
        
    @staticmethod
    def get_theme_preview_info(theme_name: str) -> dict:
        """
        Gets basic color information for a theme preview.
        """
        if theme_name == "Babbitt Industrial":
            return {
                'primary_color': BabbittIndustrialTheme.PRIMARY_BLUE,
                'accent_color': BabbittIndustrialTheme.GOLD_ACCENT,
                'background_color': BabbittIndustrialTheme.PLATINUM,
                'description': 'Premium industrial theme with sophisticated gradients'
            }
        elif theme_name == BabbittTheme.DARK_THEME:
            return {
                'primary_color': BabbittTheme.PRIMARY_BLUE,
                'accent_color': BabbittTheme.ACCENT_ORANGE,
                'background_color': BabbittTheme.DARK_BG,
            }
        
        # Default to Corporate theme preview
        return {
            'primary_color': BabbittTheme.PRIMARY_BLUE,
            'accent_color': BabbittTheme.ACCENT_ORANGE,
            'background_color': BabbittTheme.LIGHT_GRAY,
        } 