"""
Standardized Theme Base Class

This module provides a standardized base class for all themes in the MyBabbittQuote application.
All themes should inherit from this class to ensure consistent sizing, formatting, and structure.
Only colors and transition effects should vary between themes.
"""

from abc import ABC, abstractmethod
from PySide6.QtCore import QCoreApplication
from src.ui.theme.theme_template import ThemeTemplate
from src.ui.theme.dashboard_styles import get_dashboard_stylesheet


class StandardizedThemeBase(ThemeTemplate, ABC):
    """
    Standardized base class for all themes.
    
    This class inherits all the standardized sizing and formatting from ThemeTemplate
    and provides a consistent interface for theme implementation.
    
    To create a new theme:
    1. Inherit from this class
    2. Override only the color constants
    3. Optionally override transition effects
    4. Do NOT override sizing, spacing, or structural constants
    """
    
    @classmethod
    def get_main_stylesheet(cls):
        """
        Get the complete standardized stylesheet with theme-specific colors.
        
        This method combines the standard template stylesheet with theme-specific
        color overrides and dashboard styles.
        """
        # Get the standard stylesheet from the template
        standard_stylesheet = cls.get_standard_stylesheet()
        
        # Get dashboard styles with theme colors
        dashboard_stylesheet = get_dashboard_stylesheet(cls)
        
        # Combine both stylesheets
        complete_stylesheet = standard_stylesheet + "\n" + dashboard_stylesheet
        
        return complete_stylesheet
    
    @classmethod
    def get_theme_info(cls):
        """
        Get theme information for preview and management.
        
        Returns:
            dict: Theme information including name, description, and key colors
        """
        return {
            'name': cls.__name__,
            'description': cls.__doc__ or f'{cls.__name__} theme',
            'primary_color': cls.PRIMARY_COLOR,
            'secondary_color': cls.SECONDARY_COLOR,
            'accent_color': cls.ACCENT_COLOR,
            'background_color': cls.BACKGROUND_PRIMARY,
            'text_color': cls.TEXT_PRIMARY,
        }
    
    @classmethod
    def apply_to_widget(cls, widget):
        """
        Apply this theme to a specific widget.
        
        Args:
            widget: The widget to apply the theme to
        """
        stylesheet = cls.get_main_stylesheet()
        widget.setStyleSheet(stylesheet)
    
    @classmethod
    def apply_to_application(cls, app=None):
        """
        Apply this theme to the entire application.
        
        Args:
            app: QApplication instance (optional)
        """
        if app is None:
            # Get the application instance
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
        
        if app is None:
            raise RuntimeError("No QApplication instance available")
        
        # Apply the stylesheet
        stylesheet = cls.get_main_stylesheet()
        app.setStyleSheet(stylesheet)
    
    @classmethod
    def get_color_palette(cls):
        """
        Get the complete color palette for this theme.
        
        Returns:
            dict: All color constants for this theme
        """
        return {
            'primary_color': cls.PRIMARY_COLOR,
            'secondary_color': cls.SECONDARY_COLOR,
            'accent_color': cls.ACCENT_COLOR,
            'success_color': cls.SUCCESS_COLOR,
            'warning_color': cls.WARNING_COLOR,
            'error_color': cls.ERROR_COLOR,
            'info_color': cls.INFO_COLOR,
            'background_primary': cls.BACKGROUND_PRIMARY,
            'background_secondary': cls.BACKGROUND_SECONDARY,
            'background_card': cls.BACKGROUND_CARD,
            'background_surface': cls.BACKGROUND_SURFACE,
            'text_primary': cls.TEXT_PRIMARY,
            'text_secondary': cls.TEXT_SECONDARY,
            'text_muted': cls.TEXT_MUTED,
            'border_color': cls.BORDER_COLOR,
            'border_color_light': cls.BORDER_COLOR_LIGHT,
            'hover_background': cls.HOVER_BACKGROUND,
            'active_background': cls.ACTIVE_BACKGROUND,
            'focus_border': cls.FOCUS_BORDER,
        } 