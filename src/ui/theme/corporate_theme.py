from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class CorporateTheme(StandardizedThemeBase):
    """Corporate theme with navy and gold color scheme."""
    
    # Primary Colors
    PRIMARY_COLOR = "#1e3a8a"      # Navy blue
    SECONDARY_COLOR = "#1e40af"    # Slightly lighter navy
    ACCENT_COLOR = "#f59e0b"       # Gold accent
    
    # Status Colors
    SUCCESS_COLOR = "#059669"      # Emerald
    WARNING_COLOR = "#d97706"      # Amber
    ERROR_COLOR = "#dc2626"        # Red
    INFO_COLOR = "#0891b2"         # Cyan
    
    # Backgrounds
    BACKGROUND_PRIMARY = "#f8fafc"
    BACKGROUND_SECONDARY = "#ffffff"
    BACKGROUND_CARD = "#ffffff"
    BACKGROUND_SURFACE = "#f1f5f9"
    
    # Text
    TEXT_PRIMARY = "#0f172a"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#64748b"
    
    # Borders
    BORDER_COLOR = "#e2e8f0"
    BORDER_COLOR_LIGHT = "#f1f5f9"
    
    # Interactive
    HOVER_BACKGROUND = "#dbeafe"
    ACTIVE_BACKGROUND = "#1e3a8a"
    FOCUS_BORDER = "#1e3a8a"

    @classmethod
    def get_theme_info(cls):
        """Get theme information for the settings page."""
        return {
            'name': 'Corporate',
            'description': 'Corporate theme with professional dark styling',
            'author': 'Babbitt Quote Generator',
            'primary_color': '#1A1A1A',
            'secondary_color': '#2D2D2D',
            'accent_color': '#007ACC',
            'background_color': '#F5F5F5',
            'text_color': '#333333',
            'success_color': '#28A745',
            'warning_color': '#FFC107',
            'error_color': '#DC3545',
            'info_color': '#17A2B8',
        }