"""
Modern UI Components Package

This package provides modern, reusable UI components that enhance the user experience
with consistent styling, animations, and functionality.
"""

# Core components
from .modern_components import (
    StatusBadge,
    Card,
    SearchBar,
    PriceDisplay,
    LoadingSpinner,
    EmptyState,
    Notification
)

# Form components
from .modern_form_components import (
    ModernButton,
    ModernLineEdit,
    ModernTextEdit,
    ModernComboBox,
    ModernSpinBox,
    ModernCheckBox,
    ModernRadioButton
)

# Navigation components
from .modern_navigation import (
    ModernTabWidget,
    ModernMenuBar,
    ModernToolBar,
    ModernSidebar
)

# Layout components
from .modern_layout import (
    ModernScrollArea,
    ModernSplitter,
    ModernStackedWidget,
    ModernDockWidget,
    ModernLayoutContainer,
    ModernResizablePanel
)

# Advanced Features (Phase 7)
from .modern_theme_toggle import (
    ModernThemeToggle,
    ModernThemeSelector
)

from .responsive_design import (
    ResponsiveManager,
    ResponsiveWidget,
    ResponsiveLayout,
    MobileOptimizer,
    Breakpoint,
    responsive_manager
)

from .accessibility_system import (
    AccessibilityManager,
    AccessibleWidget,
    AccessibilityLevel,
    accessibility_manager
)

# Animation System
from src.ui.theme.theme_manager import (
    ThemeManager,
    AnimationManager,
    theme_manager,
    animation_manager
)

# Export all components for easy importing
__all__ = [
    # Core components
    'StatusBadge',
    'Card',
    'SearchBar',
    'PriceDisplay',
    'LoadingSpinner',
    'EmptyState',
    'Notification',
    
    # Form components
    'ModernButton',
    'ModernLineEdit',
    'ModernTextEdit',
    'ModernComboBox',
    'ModernSpinBox',
    'ModernCheckBox',
    'ModernRadioButton',
    
    # Navigation components
    'ModernTabWidget',
    'ModernMenuBar',
    'ModernToolBar',
    'ModernSidebar',
    
    # Layout components
    'ModernScrollArea',
    'ModernSplitter',
    'ModernStackedWidget',
    'ModernDockWidget',
    'ModernLayoutContainer',
    'ModernResizablePanel',
    
    # Advanced Features
    'ModernThemeToggle',
    'ModernThemeSelector',
    'ResponsiveManager',
    'ResponsiveWidget',
    'ResponsiveLayout',
    'MobileOptimizer',
    'Breakpoint',
    'responsive_manager',
    'AccessibilityManager',
    'AccessibleWidget',
    'AccessibilityLevel',
    'accessibility_manager',
    'ThemeManager',
    'AnimationManager',
    'theme_manager',
    'animation_manager'
]
