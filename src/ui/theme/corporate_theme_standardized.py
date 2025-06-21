"""
Standardized Corporate Theme

This theme inherits from StandardizedThemeBase to ensure consistent sizing and formatting
while providing the corporate color scheme.
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class CorporateThemeStandardized(StandardizedThemeBase):
    """
    Standardized Corporate theme with professional business styling.

    This theme provides a corporate color scheme with navy and gray tones,
    maintaining consistent sizing and formatting from the base template.
    """

    # ============================================================================
    # COLOR OVERRIDES ONLY - All sizing and formatting inherited from base
    # ============================================================================

    # Primary Colors
    PRIMARY_COLOR = "#1e3a8a"      # Navy blue primary
    SECONDARY_COLOR = "#3b82f6"    # Blue secondary
    ACCENT_COLOR = "#f59e0b"       # Amber accent

    # Status Colors
    SUCCESS_COLOR = "#059669"      # Emerald success
    WARNING_COLOR = "#d97706"      # Amber warning
    ERROR_COLOR = "#dc2626"        # Red error
    INFO_COLOR = "#0891b2"         # Cyan info

    # Background Colors
    BACKGROUND_PRIMARY = "#f8fafc"     # Slate 50 background
    BACKGROUND_SECONDARY = "#ffffff"   # White secondary
    BACKGROUND_CARD = "#ffffff"        # White cards
    BACKGROUND_SURFACE = "#f1f5f9"     # Slate 100 surface

    # Text Colors
    TEXT_PRIMARY = "#0f172a"       # Slate 900 text
    TEXT_SECONDARY = "#475569"     # Slate 600 text
    TEXT_MUTED = "#64748b"         # Slate 500 text

    # Border Colors
    BORDER_COLOR = "#e2e8f0"       # Slate 200 border
    BORDER_COLOR_LIGHT = "#f1f5f9" # Slate 100 light border

    # Interactive States
    HOVER_BACKGROUND = "#dbeafe"   # Blue 100 hover
    ACTIVE_BACKGROUND = "#1e3a8a"  # Navy active
    FOCUS_BORDER = "#1e3a8a"       # Navy focus
