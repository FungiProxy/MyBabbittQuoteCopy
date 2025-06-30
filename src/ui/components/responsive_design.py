"""
Responsive Design System

This module provides responsive design capabilities for the modern UI,
including breakpoint management, adaptive layouts, and mobile-friendly components.
"""

from PySide6.QtCore import QObject, Signal, QTimer, QSize
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow
from typing import Dict, Callable, List, Optional
import enum


class Breakpoint(enum.Enum):
    """Screen size breakpoints for responsive design."""
    XS = 480   # Extra small (mobile)
    SM = 768   # Small (tablet)
    MD = 1024  # Medium (small desktop)
    LG = 1280  # Large (desktop)
    XL = 1536  # Extra large (large desktop)


class ResponsiveManager(QObject):
    """
    Manages responsive design breakpoints and adaptive layouts.
    
    Features:
    - Automatic breakpoint detection
    - Responsive layout adjustments
    - Mobile-friendly component adaptations
    - Orientation change handling
    """
    
    # Signals
    breakpoint_changed = Signal(Breakpoint)  # Emitted when breakpoint changes
    orientation_changed = Signal(str)  # Emitted when orientation changes
    screen_size_changed = Signal(QSize)  # Emitted when screen size changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_breakpoint = Breakpoint.LG
        self.current_orientation = "landscape"
        self.breakpoint_callbacks = {}
        self.orientation_callbacks = {}
        self.responsive_widgets = []
        
        # Setup monitoring
        self.setup_monitoring()
    
    def setup_monitoring(self):
        """Setup screen size and orientation monitoring."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Monitor screen changes
            app.screenAdded.connect(self.on_screen_changed)
            app.screenRemoved.connect(self.on_screen_changed)
            
            # Get primary screen
            primary_screen = app.primaryScreen()
            if primary_screen:
                primary_screen.geometryChanged.connect(self.on_screen_geometry_changed)
    
    def on_screen_changed(self):
        """Handle screen addition/removal."""
        self.update_breakpoint()
    
    def on_screen_geometry_changed(self):
        """Handle screen geometry changes."""
        self.update_breakpoint()
    
    def update_breakpoint(self):
        """Update the current breakpoint based on screen size."""
        app = QApplication.instance()
        if not app or not isinstance(app, QApplication):
            return
        
        primary_screen = app.primaryScreen()
        if not primary_screen:
            return
        
        size = primary_screen.size()
        width = size.width()
        height = size.height()
        
        # Determine breakpoint
        new_breakpoint = Breakpoint.XL
        if width < Breakpoint.XS.value:
            new_breakpoint = Breakpoint.XS
        elif width < Breakpoint.SM.value:
            new_breakpoint = Breakpoint.SM
        elif width < Breakpoint.MD.value:
            new_breakpoint = Breakpoint.MD
        elif width < Breakpoint.LG.value:
            new_breakpoint = Breakpoint.LG
        
        # Update if changed
        if new_breakpoint != self.current_breakpoint:
            self.current_breakpoint = new_breakpoint
            self.breakpoint_changed.emit(new_breakpoint)
            self.apply_breakpoint_callbacks(new_breakpoint)
        
        # Update orientation
        new_orientation = "portrait" if width < height else "landscape"
        if new_orientation != self.current_orientation:
            self.current_orientation = new_orientation
            self.orientation_changed.emit(new_orientation)
            self.apply_orientation_callbacks(new_orientation)
        
        # Emit screen size change
        self.screen_size_changed.emit(size)
    
    def get_current_breakpoint(self) -> Breakpoint:
        """Get the current breakpoint."""
        return self.current_breakpoint
    
    def get_current_orientation(self) -> str:
        """Get the current orientation."""
        return self.current_orientation
    
    def is_mobile(self) -> bool:
        """Check if current breakpoint is mobile (XS or SM)."""
        return self.current_breakpoint in [Breakpoint.XS, Breakpoint.SM]
    
    def is_tablet(self) -> bool:
        """Check if current breakpoint is tablet (SM or MD)."""
        return self.current_breakpoint in [Breakpoint.SM, Breakpoint.MD]
    
    def is_desktop(self) -> bool:
        """Check if current breakpoint is desktop (LG or XL)."""
        return self.current_breakpoint in [Breakpoint.LG, Breakpoint.XL]
    
    def register_breakpoint_callback(self, breakpoint: Breakpoint, callback: Callable):
        """Register a callback for a specific breakpoint."""
        if breakpoint not in self.breakpoint_callbacks:
            self.breakpoint_callbacks[breakpoint] = []
        self.breakpoint_callbacks[breakpoint].append(callback)
    
    def register_orientation_callback(self, orientation: str, callback: Callable):
        """Register a callback for a specific orientation."""
        if orientation not in self.orientation_callbacks:
            self.orientation_callbacks[orientation] = []
        self.orientation_callbacks[orientation].append(callback)
    
    def apply_breakpoint_callbacks(self, breakpoint: Breakpoint):
        """Apply callbacks for the current breakpoint."""
        if breakpoint in self.breakpoint_callbacks:
            for callback in self.breakpoint_callbacks[breakpoint]:
                try:
                    callback(breakpoint)
                except Exception as e:
                    print(f"Error in breakpoint callback: {e}")
    
    def apply_orientation_callbacks(self, orientation: str):
        """Apply callbacks for the current orientation."""
        if orientation in self.orientation_callbacks:
            for callback in self.orientation_callbacks[orientation]:
                try:
                    callback(orientation)
                except Exception as e:
                    print(f"Error in orientation callback: {e}")
    
    def register_responsive_widget(self, widget: QWidget):
        """Register a widget for responsive updates."""
        if widget not in self.responsive_widgets:
            self.responsive_widgets.append(widget)
    
    def unregister_responsive_widget(self, widget: QWidget):
        """Unregister a widget from responsive updates."""
        if widget in self.responsive_widgets:
            self.responsive_widgets.remove(widget)


class ResponsiveWidget(QWidget):
    """
    Base class for responsive widgets that adapt to different screen sizes.
    
    Features:
    - Automatic responsive behavior
    - Breakpoint-specific styling
    - Mobile-friendly adaptations
    - Orientation awareness
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.responsive_manager = ResponsiveManager()
        self.responsive_manager.register_responsive_widget(self)
        
        # Connect signals
        self.responsive_manager.breakpoint_changed.connect(self.on_breakpoint_changed)
        self.responsive_manager.orientation_changed.connect(self.on_orientation_changed)
        
        # Setup responsive behavior
        self.setup_responsive_behavior()
    
    def setup_responsive_behavior(self):
        """Setup responsive behavior for the widget."""
        # Override in subclasses
        pass
    
    def on_breakpoint_changed(self, breakpoint: Breakpoint):
        """Handle breakpoint changes."""
        self.apply_breakpoint_styling(breakpoint)
        self.adjust_layout_for_breakpoint(breakpoint)
    
    def on_orientation_changed(self, orientation: str):
        """Handle orientation changes."""
        self.apply_orientation_styling(orientation)
        self.adjust_layout_for_orientation(orientation)
    
    def apply_breakpoint_styling(self, breakpoint: Breakpoint):
        """Apply styling based on breakpoint."""
        # Override in subclasses
        pass
    
    def apply_orientation_styling(self, orientation: str):
        """Apply styling based on orientation."""
        # Override in subclasses
        pass
    
    def adjust_layout_for_breakpoint(self, breakpoint: Breakpoint):
        """Adjust layout based on breakpoint."""
        # Override in subclasses
        pass
    
    def adjust_layout_for_orientation(self, orientation: str):
        """Adjust layout based on orientation."""
        # Override in subclasses
        pass


class ResponsiveLayout:
    """
    Responsive layout manager that adapts to different screen sizes.
    
    Features:
    - Flexible grid layouts
    - Stack layouts for mobile
    - Adaptive spacing
    - Breakpoint-specific configurations
    """
    
    def __init__(self):
        self.breakpoint_configs = {
            Breakpoint.XS: {
                'columns': 1,
                'spacing': 8,
                'margins': 16,
                'stack_vertically': True
            },
            Breakpoint.SM: {
                'columns': 2,
                'spacing': 12,
                'margins': 20,
                'stack_vertically': False
            },
            Breakpoint.MD: {
                'columns': 3,
                'spacing': 16,
                'margins': 24,
                'stack_vertically': False
            },
            Breakpoint.LG: {
                'columns': 4,
                'spacing': 20,
                'margins': 32,
                'stack_vertically': False
            },
            Breakpoint.XL: {
                'columns': 5,
                'spacing': 24,
                'margins': 40,
                'stack_vertically': False
            }
        }
    
    def get_config_for_breakpoint(self, breakpoint: Breakpoint) -> Dict:
        """Get configuration for a specific breakpoint."""
        return self.breakpoint_configs.get(breakpoint, self.breakpoint_configs[Breakpoint.LG])
    
    def calculate_grid_layout(self, breakpoint: Breakpoint, widget_count: int) -> Dict:
        """Calculate grid layout parameters for a breakpoint."""
        config = self.get_config_for_breakpoint(breakpoint)
        
        columns = config['columns']
        rows = (widget_count + columns - 1) // columns  # Ceiling division
        
        return {
            'columns': columns,
            'rows': rows,
            'spacing': config['spacing'],
            'margins': config['margins'],
            'stack_vertically': config['stack_vertically']
        }


class MobileOptimizer:
    """
    Optimizes UI components for mobile devices.
    
    Features:
    - Touch-friendly sizing
    - Simplified navigation
    - Optimized layouts
    - Mobile-specific interactions
    """
    
    def __init__(self):
        self.touch_target_size = 44  # Minimum touch target size in pixels
        self.mobile_spacing = 16     # Mobile-specific spacing
        self.mobile_font_size = 16   # Mobile-specific font size
    
    def optimize_for_mobile(self, widget: QWidget):
        """Apply mobile optimizations to a widget."""
        # Increase touch targets
        self.increase_touch_targets(widget)
        
        # Adjust spacing
        self.adjust_mobile_spacing(widget)
        
        # Optimize fonts
        self.optimize_mobile_fonts(widget)
    
    def increase_touch_targets(self, widget: QWidget):
        """Increase touch target sizes for mobile."""
        # Find buttons and make them touch-friendly
        for child in widget.findChildren(QWidget):
            if hasattr(child, 'setMinimumSize'):
                current_size = child.minimumSize()
                if current_size.width() < self.touch_target_size:
                    child.setMinimumSize(self.touch_target_size, self.touch_target_size)
    
    def adjust_mobile_spacing(self, widget: QWidget):
        """Adjust spacing for mobile devices."""
        # Increase margins and padding for better touch interaction
        if hasattr(widget, 'setContentsMargins'):
            widget.setContentsMargins(
                self.mobile_spacing,
                self.mobile_spacing,
                self.mobile_spacing,
                self.mobile_spacing
            )
    
    def optimize_mobile_fonts(self, widget: QWidget):
        """Optimize fonts for mobile readability."""
        # Increase font sizes for better mobile readability
        font = widget.font()
        if font.pointSize() < self.mobile_font_size:
            font.setPointSize(self.mobile_font_size)
            widget.setFont(font)


# Global responsive manager instance
responsive_manager = ResponsiveManager() 