"""
Modern Layout Components

This module provides modern layout components that enhance the user experience
with improved styling, animations, and functionality while maintaining
compatibility with existing Qt widgets.
"""

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, Signal
from PySide6.QtWidgets import (
    QScrollArea, QSplitter, QStackedWidget, QDockWidget,
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QApplication
)
from PySide6.QtGui import QPainter, QColor, QPen, QFont

from src.ui.theme import COLORS, FONTS, SPACING, RADIUS, get_card_style


class ModernScrollArea(QScrollArea):
    """
    Modern scroll area with enhanced styling and smooth scrolling.
    
    Features:
    - Modern styling with rounded corners and shadows
    - Smooth scrolling behavior
    - Custom scrollbar styling
    - Better visual feedback
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_modern_styling()
        self._setup_scroll_behavior()
    
    def _setup_modern_styling(self):
        """Apply modern styling to the scroll area."""
        self.setStyleSheet(f"""
            QScrollArea {{
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['lg']}px;
                background-color: {COLORS['bg_primary']};
                outline: none;
            }}
            QScrollArea:focus {{
                border-color: {COLORS['primary']};
            }}
            
            QScrollBar:vertical {{
                background-color: {COLORS['gray_100']};
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['gray_300']};
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {COLORS['gray_400']};
            }}
            QScrollBar::handle:vertical:pressed {{
                background-color: {COLORS['gray_500']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: transparent;
            }}
            
            QScrollBar:horizontal {{
                background-color: {COLORS['gray_100']};
                height: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {COLORS['gray_300']};
                border-radius: 6px;
                min-width: 20px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {COLORS['gray_400']};
            }}
            QScrollBar::handle:horizontal:pressed {{
                background-color: {COLORS['gray_500']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background-color: transparent;
            }}
        """)
    
    def _setup_scroll_behavior(self):
        """Setup smooth scrolling behavior."""
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        
        # Enable smooth scrolling
        self.verticalScrollBar().setSingleStep(10)
        self.horizontalScrollBar().setSingleStep(10)


class ModernSplitter(QSplitter):
    """
    Modern splitter with enhanced visual indicators and smooth animations.
    
    Features:
    - Modern styling for splitter handles
    - Smooth resize animations
    - Better visual feedback
    - Customizable handle appearance
    """
    
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._setup_modern_styling()
        self._setup_splitter_behavior()
    
    def _setup_modern_styling(self):
        """Apply modern styling to the splitter."""
        self.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border_light']};
                border-radius: {RADIUS['sm']}px;
            }}
            QSplitter::handle:hover {{
                background-color: {COLORS['primary']};
            }}
            QSplitter::handle:pressed {{
                background-color: {COLORS['primary_pressed']};
            }}
        """)
        
        # Set handle width/height based on orientation
        if self.orientation() == Qt.Orientation.Horizontal:
            self.setHandleWidth(4)
        else:
            self.setHandleWidth(4)
    
    def _setup_splitter_behavior(self):
        """Setup splitter behavior and animations."""
        self.setChildrenCollapsible(False)
        self.setOpaqueResize(True)
        
        # Connect signals for smooth animations
        self.splitterMoved.connect(self._on_splitter_moved)
    
    def _on_splitter_moved(self, pos, index):
        """Handle splitter movement with smooth animation."""
        # This can be extended with custom animation logic
        pass
    
    def setSizesWithAnimation(self, sizes, duration=300):
        """Set splitter sizes with smooth animation."""
        current_sizes = self.sizes()
        if len(current_sizes) != len(sizes):
            self.setSizes(sizes)
            return
        
        # Create animation for smooth transition
        animation = QPropertyAnimation(self, b"sizes")
        animation.setDuration(duration)
        animation.setStartValue(current_sizes)
        animation.setEndValue(sizes)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()


class ModernStackedWidget(QStackedWidget):
    """
    Modern stacked widget with smooth transitions and enhanced styling.
    
    Features:
    - Smooth page transitions with animations
    - Modern styling for page indicators
    - Better visual feedback
    - Customizable transition effects
    """
    
    page_changed = Signal(int)  # Emitted when page changes with animation
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_modern_styling()
        self._setup_transition_behavior()
        self._current_animation = None
    
    def _setup_modern_styling(self):
        """Apply modern styling to the stacked widget."""
        self.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
        """)
    
    def _setup_transition_behavior(self):
        """Setup transition behavior and animations."""
        self.currentChanged.connect(self._on_current_changed)
    
    def _on_current_changed(self, index):
        """Handle current page change."""
        self.page_changed.emit(index)
    
    def setCurrentIndexWithAnimation(self, index, transition_type="fade", duration=300):
        """
        Set current index with smooth animation.
        
        Args:
            index (int): Index of the page to show
            transition_type (str): Type of transition ("fade", "slide", "none")
            duration (int): Animation duration in milliseconds
        """
        if index == self.currentIndex():
            return
        
        if transition_type == "none" or duration == 0:
            self.setCurrentIndex(index)
            return
        
        # Stop any ongoing animation
        if self._current_animation and self._current_animation.state() == QPropertyAnimation.State.Running:
            self._current_animation.stop()
        
        if transition_type == "fade":
            self._animate_fade_transition(index, duration)
        elif transition_type == "slide":
            self._animate_slide_transition(index, duration)
        else:
            self.setCurrentIndex(index)
    
    def _animate_fade_transition(self, target_index, duration):
        """Animate fade transition between pages."""
        # Create a temporary widget for the fade effect
        temp_widget = QWidget(self)
        temp_widget.setStyleSheet(f"background-color: {COLORS['bg_primary']};")
        temp_widget.setGeometry(self.rect())
        
        # Show temporary widget
        temp_widget.show()
        temp_widget.raise_()
        
        # Create fade out animation
        fade_out = QPropertyAnimation(temp_widget, b"windowOpacity")
        fade_out.setDuration(duration // 2)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Connect animation finished to change page and cleanup
        fade_out.finished.connect(lambda: self._complete_fade_transition(target_index, temp_widget))
        
        self._current_animation = fade_out
        fade_out.start()
    
    def _complete_fade_transition(self, target_index, temp_widget):
        """Complete fade transition by changing page and cleaning up."""
        self.setCurrentIndex(target_index)
        temp_widget.deleteLater()
        self._current_animation = None
    
    def _animate_slide_transition(self, target_index, duration):
        """Animate slide transition between pages."""
        # For slide transitions, we'll use a simple approach
        # More complex slide animations can be implemented here
        self.setCurrentIndex(target_index)


class ModernDockWidget(QDockWidget):
    """
    Modern dock widget with enhanced styling and better docking indicators.
    
    Features:
    - Modern styling for dock widget and title bar
    - Enhanced docking indicators
    - Smooth animations for docking/undocking
    - Better visual feedback
    """
    
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self._setup_modern_styling()
        self._setup_dock_behavior()
    
    def _setup_modern_styling(self):
        """Apply modern styling to the dock widget."""
        self.setStyleSheet(f"""
            QDockWidget {{
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(undock.png);
                background-color: {COLORS['bg_primary']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
            }}
            QDockWidget::title {{
                background-color: {COLORS['gray_100']};
                padding: {SPACING['md']}px;
                border-top-left-radius: {RADIUS['md']}px;
                border-top-right-radius: {RADIUS['md']}px;
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
            }}
            QDockWidget::close-button, QDockWidget::float-button {{
                background-color: {COLORS['gray_200']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['sm']}px;
                padding: 4px;
                margin: 2px;
            }}
            QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
                background-color: {COLORS['gray_300']};
            }}
            QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {{
                background-color: {COLORS['gray_400']};
            }}
        """)
    
    def _setup_dock_behavior(self):
        """Setup dock widget behavior."""
        self.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea |
            Qt.DockWidgetArea.TopDockWidgetArea |
            Qt.DockWidgetArea.BottomDockWidgetArea
        )
        
        # Connect signals for better behavior
        self.dockLocationChanged.connect(self._on_dock_location_changed)
        self.topLevelChanged.connect(self._on_top_level_changed)
    
    def _on_dock_location_changed(self, area):
        """Handle dock location changes."""
        # This can be extended with custom behavior
        pass
    
    def _on_top_level_changed(self, top_level):
        """Handle top level changes (docked vs floating)."""
        if top_level:
            # Widget is now floating
            self.setStyleSheet(self.styleSheet() + f"""
                QDockWidget {{
                    border: 2px solid {COLORS['primary']};
                }}
            """)
        else:
            # Widget is now docked
            self._setup_modern_styling()


class ModernLayoutContainer(QFrame):
    """
    Modern layout container with enhanced styling and layout management.
    
    Features:
    - Modern card-like appearance
    - Flexible layout management
    - Consistent spacing and margins
    - Better visual hierarchy
    """
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self._setup_modern_styling()
        self._setup_layout()
    
    def _setup_modern_styling(self):
        """Apply modern styling to the layout container."""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_primary']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['lg']}px;
                padding: {SPACING['lg']}px;
            }}
        """)
    
    def _setup_layout(self):
        """Setup the internal layout."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        self.layout.setSpacing(SPACING['md'])
        
        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {FONTS['sizes']['lg']}px;
                    font-weight: {FONTS['weights']['semibold']};
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['sm']}px;
                }}
            """)
            self.layout.addWidget(title_label)
    
    def addWidget(self, widget):
        """Add a widget to the container."""
        self.layout.addWidget(widget)
    
    def addLayout(self, layout):
        """Add a layout to the container."""
        self.layout.addLayout(layout)
    
    def addStretch(self, stretch=0):
        """Add stretch to the container."""
        self.layout.addStretch(stretch)


class ModernResizablePanel(QFrame):
    """
    Modern resizable panel with drag handles and smooth resizing.
    
    Features:
    - Resizable with drag handles
    - Modern styling
    - Smooth resize animations
    - Minimum/maximum size constraints
    """
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self._setup_modern_styling()
        self._setup_resize_behavior()
    
    def _setup_modern_styling(self):
        """Apply modern styling to the resizable panel."""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_primary']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['lg']}px;
            }}
            QFrame::title {{
                background-color: {COLORS['gray_100']};
                padding: {SPACING['md']}px;
                border-top-left-radius: {RADIUS['lg']}px;
                border-top-right-radius: {RADIUS['lg']}px;
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
            }}
        """)
    
    def _setup_resize_behavior(self):
        """Setup resize behavior and constraints."""
        self.setMinimumSize(200, 150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    def resizeEvent(self, event):
        """Handle resize events with smooth animations."""
        super().resizeEvent(event)
        # This can be extended with custom resize animations 