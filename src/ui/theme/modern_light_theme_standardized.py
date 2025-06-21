"""
Standardized Modern Light Theme

This theme inherits from StandardizedThemeBase to ensure consistent sizing and formatting
while providing the modern light color scheme.
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class ModernLightThemeStandardized(StandardizedThemeBase):
    """
    Standardized Modern Light theme with clean, minimal styling.

    This theme provides a light, modern color scheme with subtle accents,
    maintaining consistent sizing and formatting from the base template.
    """

    # ============================================================================
    # COLOR OVERRIDES ONLY - All sizing and formatting inherited from base
    # ============================================================================

    # Primary Colors
    PRIMARY_COLOR = "#6200ea"      # Purple primary
    SECONDARY_COLOR = "#7c4dff"    # Light purple secondary
    ACCENT_COLOR = "#00c853"       # Green accent

    # Status Colors
    SUCCESS_COLOR = "#00c853"      # Green success
    WARNING_COLOR = "#ff6d00"      # Orange warning
    ERROR_COLOR = "#d50000"        # Red error
    INFO_COLOR = "#2962ff"         # Blue info

    # Background Colors
    BACKGROUND_PRIMARY = "#ffffff"     # White background
    BACKGROUND_SECONDARY = "#fafafa"   # Very light gray secondary
    BACKGROUND_CARD = "#ffffff"        # White cards
    BACKGROUND_SURFACE = "#fafafa"     # Very light gray surface

    # Text Colors
    TEXT_PRIMARY = "#212121"       # Dark text
    TEXT_SECONDARY = "#757575"     # Medium gray text
    TEXT_MUTED = "#bdbdbd"         # Light gray text

    # Border Colors
    BORDER_COLOR = "#e0e0e0"       # Light gray border
    BORDER_COLOR_LIGHT = "#f5f5f5" # Very light border

    # Interactive States
    HOVER_BACKGROUND = "#f3e5f5"   # Light purple hover
    ACTIVE_BACKGROUND = "#6200ea"  # Purple active
    FOCUS_BORDER = "#6200ea"       # Purple focus
