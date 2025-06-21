"""
Standardized Babbitt Professional Theme

This theme inherits from StandardizedThemeBase to ensure consistent sizing and formatting
while providing the professional dark blue color scheme.
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class BabbittProfessionalThemeStandardized(StandardizedThemeBase):
    """
    Standardized Babbitt Professional theme with dark professional styling.

    This theme provides a dark professional color scheme with blue accents,
    maintaining consistent sizing and formatting from the base template.
    """

    # ============================================================================
    # COLOR OVERRIDES ONLY - All sizing and formatting inherited from base
    # ============================================================================

    # Primary Colors
    PRIMARY_COLOR = "#1a237e"      # Dark blue primary
    SECONDARY_COLOR = "#283593"    # Slightly lighter blue
    ACCENT_COLOR = "#ffc107"       # Gold accent

    # Status Colors
    SUCCESS_COLOR = "#4caf50"      # Green success
    WARNING_COLOR = "#ff9800"      # Orange warning
    ERROR_COLOR = "#f44336"        # Red error
    INFO_COLOR = "#2196f3"         # Blue info

    # Background Colors
    BACKGROUND_PRIMARY = "#f5f5f5"     # Light gray background
    BACKGROUND_SECONDARY = "#ffffff"   # White secondary
    BACKGROUND_CARD = "#ffffff"        # White cards
    BACKGROUND_SURFACE = "#f5f5f5"     # Light gray surface

    # Text Colors
    TEXT_PRIMARY = "#212121"       # Dark text
    TEXT_SECONDARY = "#757575"     # Medium gray text
    TEXT_MUTED = "#9e9e9e"         # Light gray text

    # Border Colors
    BORDER_COLOR = "#e0e0e0"       # Light gray border
    BORDER_COLOR_LIGHT = "#f5f5f5" # Very light border

    # Interactive States
    HOVER_BACKGROUND = "#e3f2fd"   # Light blue hover
    ACTIVE_BACKGROUND = "#1a237e"  # Dark blue active
    FOCUS_BORDER = "#1a237e"       # Dark blue focus
