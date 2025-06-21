"""
Modern Professional Theme - Fixed Layout
File: src/ui/theme/modern_professional_theme.py

🟢 5 min - Professional theme with proper layout and colors
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class ModernProfessionalTheme(StandardizedThemeBase):
    """
    Modern professional theme with excellent color scheme and proper layout.
    Uses the fixed StandardizedThemeBase for consistent sizing and proportions.
    """
    
    # ============================================================================
    # PROFESSIONAL COLOR SCHEME - EXCELLENT UX
    # ============================================================================
    
    # Primary Colors - Professional Blue
    PRIMARY_COLOR = "#1e40af"      # Professional blue
    SECONDARY_COLOR = "#1d4ed8"    # Bright blue
    ACCENT_COLOR = "#f59e0b"       # Professional amber
    
    # Status Colors - Clear and accessible
    SUCCESS_COLOR = "#059669"      # Professional green
    WARNING_COLOR = "#d97706"      # Amber warning
    ERROR_COLOR = "#dc2626"        # Red error
    INFO_COLOR = "#0891b2"         # Cyan info
    
    # Background Colors - Clean and modern
    BACKGROUND_PRIMARY = "#ffffff"     # Pure white
    BACKGROUND_SECONDARY = "#f8fafc"   # Slate 50
    BACKGROUND_CARD = "#ffffff"        # Pure white cards
    BACKGROUND_SURFACE = "#f1f5f9"     # Slate 100
    
    # Text Colors - Professional hierarchy
    TEXT_PRIMARY = "#0f172a"       # Slate 900
    TEXT_SECONDARY = "#475569"     # Slate 600
    TEXT_MUTED = "#64748b"         # Slate 500
    
    # Border Colors - Subtle and clean
    BORDER_COLOR = "#e2e8f0"       # Slate 200
    BORDER_COLOR_LIGHT = "#f1f5f9" # Slate 100
    
    # Interactive States - Smooth transitions
    HOVER_BACKGROUND = "#f1f5f9"   # Light hover
    ACTIVE_BACKGROUND = "#1e40af"  # Blue active
    FOCUS_BORDER = "#1e40af"       # Blue focus


class DarkProfessionalTheme(StandardizedThemeBase):
    """Dark professional theme for low-light environments."""
    
    # Primary Colors
    PRIMARY_COLOR = "#3b82f6"      # Bright blue for dark theme
    SECONDARY_COLOR = "#2563eb"    # Darker blue
    ACCENT_COLOR = "#fbbf24"       # Yellow accent (better for dark)
    
    # Status Colors
    SUCCESS_COLOR = "#10b981"      # Emerald
    WARNING_COLOR = "#f59e0b"      # Amber
    ERROR_COLOR = "#ef4444"        # Red
    INFO_COLOR = "#06b6d4"         # Cyan
    
    # Dark Backgrounds
    BACKGROUND_PRIMARY = "#1e293b"    # Slate 800
    BACKGROUND_SECONDARY = "#0f172a"  # Slate 900
    BACKGROUND_CARD = "#334155"       # Slate 700
    BACKGROUND_SURFACE = "#475569"    # Slate 600
    
    # Light Text for dark theme
    TEXT_PRIMARY = "#f8fafc"       # Slate 50
    TEXT_SECONDARY = "#cbd5e1"     # Slate 300
    TEXT_MUTED = "#94a3b8"         # Slate 400
    
    # Dark theme borders
    BORDER_COLOR = "#475569"       # Slate 600
    BORDER_COLOR_LIGHT = "#334155" # Slate 700
    
    # Dark theme interactions
    HOVER_BACKGROUND = "#334155"   # Slate 700
    ACTIVE_BACKGROUND = "#3b82f6"  # Blue active
    FOCUS_BORDER = "#3b82f6"       # Blue focus


class CorporateTheme(StandardizedThemeBase):
    """Corporate theme with navy and gold accents."""
    
    # Primary Colors
    PRIMARY_COLOR = "#1e3a8a"      # Navy blue
    SECONDARY_COLOR = "#1e40af"    # Blue
    ACCENT_COLOR = "#f59e0b"       # Gold
    
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


# ===== THEME REGISTRY =====

PROFESSIONAL_THEMES = {
    'modern_professional': ModernProfessionalTheme,
    'dark_professional': DarkProfessionalTheme,
    'corporate': CorporateTheme,
}


def get_theme_by_name(theme_name: str):
    """Get theme class by name."""
    return PROFESSIONAL_THEMES.get(theme_name, ModernProfessionalTheme)


def apply_theme_to_application(theme_name: str = 'modern_professional'):
    """Apply theme to the entire application."""
    theme_class = get_theme_by_name(theme_name)
    theme_class.apply_to_application()
    
    print(f"Applied theme: {theme_name}")
    return theme_class


def get_available_themes():
    """Get list of available theme names."""
    return list(PROFESSIONAL_THEMES.keys())


# ===== MAIN WINDOW INTEGRATION =====

def setup_main_window_theme(main_window, theme_name: str = 'modern_professional'):
    """
    Complete setup for main window with theme and layout fixes.
    
    🔴 Critical - Use this in your main window initialization
    """
    # Apply theme
    theme_class = get_theme_by_name(theme_name)
    theme_class.apply_to_widget(main_window)
    
    # Apply layout fixes
    from src.ui.helpers.window_layout_helper import fix_main_window_layout
    fix_main_window_layout(main_window)
    
    print(f"Main window setup complete with {theme_name} theme")
    return theme_class