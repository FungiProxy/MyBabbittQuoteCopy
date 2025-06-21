"""
Standardized Modern Babbitt Theme

This theme inherits from StandardizedThemeBase to ensure consistent sizing and formatting
while providing the modern blue color scheme.
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class ModernBabbittThemeStandardized(StandardizedThemeBase):
    """
    Standardized Modern Babbitt theme with contemporary styling.

    This theme provides a modern blue color scheme with clean aesthetics,
    maintaining consistent sizing and formatting from the base template.
    """

    # ============================================================================
    # COLOR OVERRIDES ONLY - All sizing and formatting inherited from base
    # ============================================================================

    # Primary Colors
    PRIMARY_COLOR = "#1976d2"      # Modern blue primary
    SECONDARY_COLOR = "#1565c0"    # Darker blue secondary
    ACCENT_COLOR = "#ff6b35"       # Orange accent

    # Status Colors
    SUCCESS_COLOR = "#388e3c"      # Green success
    WARNING_COLOR = "#f57c00"      # Orange warning
    ERROR_COLOR = "#d32f2f"        # Red error
    INFO_COLOR = "#1976d2"         # Blue info

    # Background Colors
    BACKGROUND_PRIMARY = "#fafafa"     # Very light gray background
    BACKGROUND_SECONDARY = "#ffffff"   # White secondary
    BACKGROUND_CARD = "#ffffff"        # White cards
    BACKGROUND_SURFACE = "#fafafa"     # Very light gray surface

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
