"""
Theme Manager for Advanced UI Features

This module provides theme switching capabilities, animation management,
and advanced styling features for the modern UI system.
"""

from PySide6.QtCore import QObject, Signal, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
import json
import os
from typing import Dict, Any, Optional

from .modern_styles import COLORS, FONTS, SPACING, RADIUS


class ThemeManager(QObject):
    """
    Advanced theme manager with light/dark mode switching and animations.
    
    Features:
    - Light and dark theme support
    - Smooth theme transitions
    - Theme persistence
    - Dynamic color palette generation
    - Animation management
    """
    
    # Signals
    theme_changed = Signal(str)  # Emitted when theme changes
    animation_started = Signal(str)  # Emitted when animation starts
    animation_finished = Signal(str)  # Emitted when animation finishes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_theme = "light"
        self.animations = {}
        self.theme_file = "theme_settings.json"
        
        # Initialize themes
        self._setup_themes()
        self._load_theme_preference()
        self._apply_current_theme()
    
    def _setup_themes(self):
        """Setup light and dark theme color palettes."""
        self.themes = {
            "light": {
                "name": "Light Theme",
                "colors": {
                    # Primary colors
                    'primary': '#2563eb',
                    'primary_hover': '#1d4ed8',
                    'primary_pressed': '#1e40af',
                    
                    # Secondary colors
                    'secondary': '#f8fafc',
                    'secondary_hover': '#f1f5f9',
                    'secondary_pressed': '#e2e8f0',
                    
                    # Danger colors
                    'danger': '#dc2626',
                    'danger_hover': '#b91c1c',
                    'danger_pressed': '#991b1b',
                    
                    # Success colors
                    'success': '#059669',
                    'success_light': '#d1fae5',
                    
                    # Warning colors
                    'warning': '#92400e',
                    'warning_light': '#fef3c7',
                    
                    # Neutral colors
                    'gray_50': '#f8fafc',
                    'gray_100': '#f1f5f9',
                    'gray_200': '#e2e8f0',
                    'gray_300': '#cbd5e1',
                    'gray_400': '#94a3b8',
                    'gray_500': '#64748b',
                    'gray_600': '#475569',
                    'gray_700': '#334155',
                    'gray_800': '#1e293b',
                    'gray_900': '#0f172a',
                    
                    # Text colors
                    'text_primary': '#1e293b',
                    'text_secondary': '#475569',
                    'text_muted': '#6b7280',
                    
                    # Background colors
                    'bg_primary': '#ffffff',
                    'bg_secondary': '#f8fafc',
                    'bg_sidebar': '#1e293b',
                    'bg_sidebar_header': '#0f172a',
                    
                    # Border colors
                    'border_light': '#e2e8f0',
                    'border_medium': '#cbd5e1',
                }
            },
            "dark": {
                "name": "Dark Theme",
                "colors": {
                    # Primary colors (slightly adjusted for dark mode)
                    'primary': '#3b82f6',
                    'primary_hover': '#60a5fa',
                    'primary_pressed': '#2563eb',
                    
                    # Secondary colors
                    'secondary': '#374151',
                    'secondary_hover': '#4b5563',
                    'secondary_pressed': '#6b7280',
                    
                    # Danger colors
                    'danger': '#ef4444',
                    'danger_hover': '#f87171',
                    'danger_pressed': '#dc2626',
                    
                    # Success colors
                    'success': '#10b981',
                    'success_light': '#064e3b',
                    
                    # Warning colors
                    'warning': '#f59e0b',
                    'warning_light': '#451a03',
                    
                    # Neutral colors (inverted for dark mode)
                    'gray_50': '#111827',
                    'gray_100': '#1f2937',
                    'gray_200': '#374151',
                    'gray_300': '#4b5563',
                    'gray_400': '#6b7280',
                    'gray_500': '#9ca3af',
                    'gray_600': '#d1d5db',
                    'gray_700': '#e5e7eb',
                    'gray_800': '#f3f4f6',
                    'gray_900': '#f9fafb',
                    
                    # Text colors (inverted for dark mode)
                    'text_primary': '#f9fafb',
                    'text_secondary': '#d1d5db',
                    'text_muted': '#9ca3af',
                    
                    # Background colors (inverted for dark mode)
                    'bg_primary': '#111827',
                    'bg_secondary': '#1f2937',
                    'bg_sidebar': '#374151',
                    'bg_sidebar_header': '#111827',
                    
                    # Border colors (inverted for dark mode)
                    'border_light': '#374151',
                    'border_medium': '#4b5563',
                }
            }
        }
    
    def _load_theme_preference(self):
        """Load theme preference from file."""
        try:
            if os.path.exists(self.theme_file):
                with open(self.theme_file, 'r') as f:
                    data = json.load(f)
                    self.current_theme = data.get('theme', 'light')
        except Exception as e:
            print(f"Error loading theme preference: {e}")
            self.current_theme = "light"
    
    def _save_theme_preference(self):
        """Save theme preference to file."""
        try:
            data = {'theme': self.current_theme}
            with open(self.theme_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving theme preference: {e}")
    
    def _apply_current_theme(self):
        """Apply the current theme to the application."""
        theme_data = self.themes[self.current_theme]
        
        # Update global COLORS
        global COLORS
        COLORS.update(theme_data['colors'])
        
        # Apply to QApplication
        self._apply_to_application()
    
    def _apply_to_application(self):
        """Apply theme to QApplication palette."""
        app = QApplication.instance()
        if not app or not isinstance(app, QApplication):
            return
        
        palette = QPalette()
        theme_colors = self.themes[self.current_theme]['colors']
        
        # Set palette colors
        palette.setColor(QPalette.ColorRole.Window, QColor(theme_colors['bg_primary']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme_colors['text_primary']))
        palette.setColor(QPalette.ColorRole.Base, QColor(theme_colors['bg_primary']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme_colors['bg_secondary']))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(theme_colors['bg_primary']))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(theme_colors['text_primary']))
        palette.setColor(QPalette.ColorRole.Text, QColor(theme_colors['text_primary']))
        palette.setColor(QPalette.ColorRole.Button, QColor(theme_colors['primary']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor('#ffffff'))
        palette.setColor(QPalette.ColorRole.BrightText, QColor('#ffffff'))
        palette.setColor(QPalette.ColorRole.Link, QColor(theme_colors['primary']))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(theme_colors['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor('#ffffff'))
        
        app.setPalette(palette)
    
    def switch_theme(self, theme_name: str, animate: bool = True):
        """
        Switch to a different theme with optional animation.
        
        Args:
            theme_name (str): Name of the theme ('light' or 'dark')
            animate (bool): Whether to animate the transition
        """
        if theme_name not in self.themes:
            raise ValueError(f"Unknown theme: {theme_name}")
        
        if theme_name == self.current_theme:
            return
        
        if animate:
            self._animate_theme_switch(theme_name)
        else:
            self._instant_theme_switch(theme_name)
    
    def _animate_theme_switch(self, new_theme: str):
        """Animate theme switching with smooth transitions."""
        # Create fade animation
        app = QApplication.instance()
        if not app:
            self._instant_theme_switch(new_theme)
            return

        # Fade out current theme
        fade_out = QPropertyAnimation(app, b"windowOpacity")
        fade_out.setDuration(200)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.7)
        fade_out.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Connect fade out to theme change
        fade_out.finished.connect(lambda: self._complete_theme_switch(new_theme))
        
        self.animations['theme_switch'] = fade_out
        fade_out.start()
        
        self.animation_started.emit('theme_switch')
    
    def _complete_theme_switch(self, new_theme: str):
        """Complete theme switching after fade out."""
        # Change theme
        self._instant_theme_switch(new_theme)
        
        # Fade back in
        app = QApplication.instance()
        if app:
            fade_in = QPropertyAnimation(app, b"windowOpacity")
            fade_in.setDuration(200)
            fade_in.setStartValue(0.7)
            fade_in.setEndValue(1.0)
            fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            fade_in.finished.connect(lambda: self.animation_finished.emit('theme_switch'))
            
            self.animations['theme_switch'] = fade_in
            fade_in.start()
    
    def _instant_theme_switch(self, new_theme: str):
        """Instantly switch themes without animation."""
        self.current_theme = new_theme
        self._apply_current_theme()
        self._save_theme_preference()
        self.theme_changed.emit(new_theme)
    
    def get_current_theme(self) -> str:
        """Get the current theme name."""
        return self.current_theme
    
    def get_theme_colors(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        """Get colors for a specific theme."""
        theme = theme_name or self.current_theme
        return self.themes[theme]['colors'].copy()
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes with their display names."""
        return {name: data['name'] for name, data in self.themes.items()}
    
    def toggle_theme(self, animate: bool = True):
        """Toggle between light and dark themes."""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.switch_theme(new_theme, animate)


class AnimationManager(QObject):
    """
    Animation manager for smooth UI transitions and effects.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animations = {}
    
    def fade_in(self, widget, duration: int = 300):
        """Fade in a widget."""
        # Stop any existing animations on this widget
        self.stop_widget_animations(widget)
        
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        animation_id = f"fade_in_{id(widget)}"
        self.animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def fade_out(self, widget, duration: int = 300):
        """Fade out a widget."""
        # Stop any existing animations on this widget
        self.stop_widget_animations(widget)
        
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        animation_id = f"fade_out_{id(widget)}"
        self.animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def slide_in(self, widget, direction: str = "left", duration: int = 300):
        """Slide in a widget from a direction."""
        # Stop any existing animations on this widget
        self.stop_widget_animations(widget)
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Get current geometry
        current_geo = widget.geometry()
        
        # Set start position based on direction
        if direction == "left":
            start_geo = current_geo.translated(-current_geo.width(), 0)
        elif direction == "right":
            start_geo = current_geo.translated(current_geo.width(), 0)
        elif direction == "top":
            start_geo = current_geo.translated(0, -current_geo.height())
        elif direction == "bottom":
            start_geo = current_geo.translated(0, current_geo.height())
        else:
            start_geo = current_geo
        
        animation.setStartValue(start_geo)
        animation.setEndValue(current_geo)
        
        animation_id = f"slide_in_{direction}_{id(widget)}"
        self.animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def pulse(self, widget, duration: int = 200):
        """Pulse animation for a widget."""
        # Stop any existing animations on this widget
        self.stop_widget_animations(widget)
        
        # Scale animation (simulated with size change)
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        current_geo = widget.geometry()
        
        # Scale up slightly
        scaled_width = int(current_geo.width() * 1.05)
        scaled_height = int(current_geo.height() * 1.05)
        scaled_geo = current_geo.adjusted(
            (current_geo.width() - scaled_width) // 2,
            (current_geo.height() - scaled_height) // 2,
            (scaled_width - current_geo.width()) // 2,
            (scaled_height - current_geo.height()) // 2
        )
        
        animation.setStartValue(current_geo)
        animation.setEndValue(scaled_geo)
        
        # Create reverse animation
        reverse_animation = QPropertyAnimation(widget, b"geometry")
        reverse_animation.setDuration(duration)
        reverse_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        reverse_animation.setStartValue(scaled_geo)
        reverse_animation.setEndValue(current_geo)
        
        # Chain animations
        animation.finished.connect(reverse_animation.start)
        
        animation_id = f"pulse_{id(widget)}"
        self.animations[animation_id] = animation
        animation.start()
        
        return animation_id
    
    def stop_widget_animations(self, widget):
        """Stop all animations for a specific widget."""
        widget_id = id(widget)
        animations_to_remove = []
        
        for animation_id, animation in self.animations.items():
            if str(widget_id) in animation_id:
                animation.stop()
                animations_to_remove.append(animation_id)
        
        for animation_id in animations_to_remove:
            del self.animations[animation_id]
    
    def stop_animation(self, animation_id: str):
        """Stop a specific animation."""
        if animation_id in self.animations:
            self.animations[animation_id].stop()
            del self.animations[animation_id]
    
    def stop_all_animations(self):
        """Stop all running animations."""
        for animation in self.animations.values():
            animation.stop()
        self.animations.clear()


# Global instances
theme_manager = ThemeManager()
animation_manager = AnimationManager() 