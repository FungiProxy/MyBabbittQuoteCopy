from src.ui.theme.standardized_theme_base import StandardizedThemeBase

class ModernLightTheme(StandardizedThemeBase):
    """Clean, minimal light theme."""
    
    # Primary Colors
    PRIMARY_COLOR = "#6366f1"      # Indigo
    SECONDARY_COLOR = "#4f46e5"    # Darker indigo
    ACCENT_COLOR = "#06d6a0"       # Teal accent
    
    # Status Colors
    SUCCESS_COLOR = "#22c55e"      # Green
    WARNING_COLOR = "#f59e0b"      # Amber
    ERROR_COLOR = "#ef4444"        # Red
    INFO_COLOR = "#3b82f6"         # Blue
    
    # Light Backgrounds
    BACKGROUND_PRIMARY = "#ffffff"
    BACKGROUND_SECONDARY = "#f8fafc"
    BACKGROUND_CARD = "#ffffff"
    BACKGROUND_SURFACE = "#f1f5f9"
    
    # Text
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    TEXT_MUTED = "#94a3b8"
    
    # Borders
    BORDER_COLOR = "#e2e8f0"
    BORDER_COLOR_LIGHT = "#f1f5f9"
    
    # Interactive
    HOVER_BACKGROUND = "#f1f5f9"
    ACTIVE_BACKGROUND = "#6366f1"
    FOCUS_BORDER = "#6366f1"

    @classmethod
    def get_theme_info(cls):
        """Get theme information for the settings page."""
        return {
            'name': 'Modern Light',
            'description': 'Modern light theme with clean, minimal design',
            'author': 'Babbitt Quote Generator',
            'primary_color': '#2196F3',
            'secondary_color': '#1976D2',
            'accent_color': '#FF5722',
            'background_color': '#FFFFFF',
            'text_color': '#212121',
            'success_color': '#4CAF50',
            'warning_color': '#FF9800',
            'error_color': '#F44336',
            'info_color': '#2196F3',
        }