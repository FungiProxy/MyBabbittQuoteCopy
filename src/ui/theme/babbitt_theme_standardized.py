"""
Standardized Babbitt International Theme

This theme inherits from StandardizedThemeBase to ensure consistent sizing and formatting
while providing the professional industrial blue color scheme.
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class BabbittThemeStandardized(StandardizedThemeBase):
    """
    Standardized Babbitt International theme with professional industrial styling.
    
    This theme provides a professional blue color scheme with gold accents,
    maintaining consistent sizing and formatting from the base template.
    """
    
    # ============================================================================
    # COLOR OVERRIDES ONLY - All sizing and formatting inherited from base
    # ============================================================================
    
    # Primary Colors
    PRIMARY_COLOR = "#2C3E50"      # Deep professional blue
    SECONDARY_COLOR = "#34495E"    # Lighter blue for hover states
    ACCENT_COLOR = "#F39C12"       # Gold accent for highlights
    
    # Status Colors
    SUCCESS_COLOR = "#28A745"      # Success states, valid configurations
    WARNING_COLOR = "#FD7E14"      # Warnings, attention needed
    ERROR_COLOR = "#DC3545"        # Errors, invalid states
    INFO_COLOR = "#17A2B8"         # Information, help text
    
    # Background Colors
    BACKGROUND_PRIMARY = "#F8F9FA"     # Primary background
    BACKGROUND_SECONDARY = "#FFFFFF"   # Secondary backgrounds, panels
    BACKGROUND_CARD = "#FFFFFF"        # Card backgrounds
    BACKGROUND_SURFACE = "#F8F9FA"     # Surface backgrounds
    
    # Text Colors
    TEXT_PRIMARY = "#343A40"       # Primary text color
    TEXT_SECONDARY = "#6C757D"     # Secondary text color
    TEXT_MUTED = "#6C757D"         # Muted text color
    
    # Border Colors
    BORDER_COLOR = "#E9ECEF"       # Primary border color
    BORDER_COLOR_LIGHT = "#F8F9FA" # Light border color
    
    # Interactive States
    HOVER_BACKGROUND = "#E3F2FD"   # Hover state background
    ACTIVE_BACKGROUND = "#2C3E50"  # Active state background
    FOCUS_BORDER = "#2C3E50"       # Focus state border 