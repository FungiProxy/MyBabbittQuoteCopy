
from src.ui.theme.standardized_theme_base import StandardizedThemeBase




class DarkProfessionalTheme(StandardizedThemeBase):
    """Dark professional theme for low-light environments."""
    
    # Primary Colors
    PRIMARY_COLOR = "#3b82f6"      # Bright blue
    SECONDARY_COLOR = "#2563eb"    # Darker blue
    ACCENT_COLOR = "#fbbf24"       # Yellow accent
    
    # Status Colors
    SUCCESS_COLOR = "#10b981"      # Emerald
    WARNING_COLOR = "#f59e0b"      # Amber
    ERROR_COLOR = "#ef4444"        # Red
    INFO_COLOR = "#06b6d4"         # Cyan
    
    # Dark Backgrounds
    BACKGROUND_PRIMARY = "#1f2937"    # Dark gray
    BACKGROUND_SECONDARY = "#111827"  # Darker gray
    BACKGROUND_CARD = "#374151"       # Medium gray
    BACKGROUND_SURFACE = "#4b5563"    # Light gray
    
    # Light Text
    TEXT_PRIMARY = "#f9fafb"       # Very light
    TEXT_SECONDARY = "#d1d5db"     # Light gray
    TEXT_MUTED = "#9ca3af"         # Medium gray
    
    # Dark Borders
    BORDER_COLOR = "#6b7280"       # Medium gray
    BORDER_COLOR_LIGHT = "#4b5563" # Dark gray
    
    # Interactive
    HOVER_BACKGROUND = "#4b5563"   # Dark hover
    ACTIVE_BACKGROUND = "#3b82f6"  # Blue active
    FOCUS_BORDER = "#3b82f6"       # Blue focus
