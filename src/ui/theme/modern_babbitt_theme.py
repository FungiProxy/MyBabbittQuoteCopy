"""
Modern Babbitt Theme - Colors Only Override
File: src/ui/theme/modern_babbitt_theme.py

🟢 5 min - Replace your existing theme file
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class ModernBabbittTheme(StandardizedThemeBase):
    """
    Modern Babbitt theme with professional blue color scheme.
    All formatting and sizing inherited from StandardizedThemeBase.
    """
    
    # ============================================================================
    # COLOR OVERRIDES ONLY - All formatting inherited from base
    # ============================================================================
    
    # Primary Colors
    PRIMARY_COLOR = "#1976d2"      # Modern blue primary
    SECONDARY_COLOR = "#1565c0"    # Darker blue secondary  
    ACCENT_COLOR = "#ff6b35"       # Orange accent
    
    # Status Colors
    SUCCESS_COLOR = "#4caf50"      # Green success
    WARNING_COLOR = "#ff9800"      # Orange warning
    ERROR_COLOR = "#f44336"        # Red error
    INFO_COLOR = "#2196f3"         # Blue info
    
    # Background Colors
    BACKGROUND_PRIMARY = "#fafafa"     # Very light gray background
    BACKGROUND_SECONDARY = "#ffffff"   # White secondary
    BACKGROUND_CARD = "#ffffff"        # White cards
    BACKGROUND_SURFACE = "#f5f5f5"     # Light gray surface
    
    # Text Colors  
    TEXT_PRIMARY = "#212121"       # Dark text
    TEXT_SECONDARY = "#616161"     # Medium gray text
    TEXT_MUTED = "#9e9e9e"         # Light gray text
    
    # Border Colors
    BORDER_COLOR = "#e0e0e0"       # Light gray border
    BORDER_COLOR_LIGHT = "#f5f5f5" # Very light border
    
    # Interactive States
    HOVER_BACKGROUND = "#e3f2fd"   # Light blue hover
    ACTIVE_BACKGROUND = "#1976d2"  # Blue active
    FOCUS_BORDER = "#1976d2"       # Blue focus
    
    @classmethod
    def get_theme_info(cls):
        """Get theme information for the settings page."""
        return {
            'name': 'Modern Babbitt',
            'description': 'Modern professional theme with blue color scheme',
            'author': 'Babbitt Quote Generator',
            'primary_color': cls.PRIMARY_COLOR,
            'secondary_color': cls.SECONDARY_COLOR,
            'accent_color': cls.ACCENT_COLOR,
            'background_color': cls.BACKGROUND_PRIMARY,
            'text_color': cls.TEXT_PRIMARY,
            'success_color': cls.SUCCESS_COLOR,
            'warning_color': cls.WARNING_COLOR,
            'error_color': cls.ERROR_COLOR,
            'info_color': cls.INFO_COLOR,
        }