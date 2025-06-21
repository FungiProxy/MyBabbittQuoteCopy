#!/usr/bin/env python3
"""
Theme Standardization Script

This script provides the code for creating standardized versions of all existing themes.
Each theme will inherit from StandardizedThemeBase and only override color values,
ensuring consistent sizing and formatting across all themes.
"""

import os

def create_standardized_theme_files():
    """
    Create standardized versions of all existing themes.
    """
    
    # Define the standardized theme files to create
    themes = {
        'babbitt_professional_theme_standardized.py': '''
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
''',
        
        'modern_babbitt_theme_standardized.py': '''
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
''',
        
        'modern_light_theme_standardized.py': '''
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
''',
        
        'corporate_theme_standardized.py': '''
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
'''
    }
    
    # Create the theme files
    theme_dir = "src/ui/theme"
    
    for filename, content in themes.items():
        filepath = os.path.join(theme_dir, filename)
        
        print(f"Creating {filepath}...")
        print("=" * 50)
        print(content.strip())
        print("=" * 50)
        print()
        
        # You can uncomment the following lines to automatically create the files
        # with open(filepath, 'w') as f:
        #     f.write(content.strip())
    
    print("Theme standardization complete!")
    print("\nNext steps:")
    print("1. Manually create the files above with the provided code")
    print("2. Update theme_manager.py to use the new standardized themes")
    print("3. Test the themes to ensure they work correctly")

if __name__ == "__main__":
    create_standardized_theme_files() 