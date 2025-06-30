"""
Modern Navigation Components for MyBabbittQuote

Reusable navigation components with consistent styling and enhanced functionality.
"""

from PySide6.QtWidgets import (
    QTabWidget, QTabBar, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QListWidget, QListWidgetItem,
    QScrollArea, QMenuBar, QMenu, QToolBar
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QIcon, QAction, QActionEvent

# Import styling from centralized theme system
from ..theme import (
    COLORS, FONTS, SPACING, RADIUS,
    get_button_style, get_card_style
)

# Define sidebar-specific colors
SIDEBAR_COLORS = {
    'sidebar_bg': '#1e293b',
    'sidebar_header': '#0f172a', 
    'sidebar_border': '#334155',
    'sidebar_text': '#cbd5e1',
    'sidebar_hover': '#334155',
    'primary_hover': '#2563eb'
}


class ModernTabWidget(QTabWidget):
    """
    A modern tab widget with enhanced styling and animations.
    
    Features:
    - Modern styling with rounded corners and shadows
    - Smooth tab switching animations
    - Hover effects and active state indicators
    - Customizable tab styling
    - Support for tab icons and badges
    
    Usage:
        tabs = ModernTabWidget()
        tabs.addTab(widget1, "Tab 1")
        tabs.addTab(widget2, "Tab 2")
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
        self.setup_animations()
    
    def setup_style(self):
        """Apply modern styling to the tab widget"""
        self.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {COLORS['bg_primary']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['lg']};
                margin-top: 8px;
            }}
            
            QTabBar::tab {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_secondary']};
                padding: {SPACING['md']} {SPACING['xl']};
                margin-right: 4px;
                border-top-left-radius: {RADIUS['md']};
                border-top-right-radius: {RADIUS['md']};
                font-weight: 500;
                font-size: {FONTS['sizes']['sm']};
                min-width: 120px;
                min-height: 40px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {COLORS['primary']};
                color: {COLORS['bg_primary']};
                font-weight: 600;
            }}
            
            QTabBar::tab:hover:!selected {{
                background-color: {COLORS['secondary_hover']};
                color: {COLORS['text_primary']};
            }}
            
            QTabBar::tab:disabled {{
                background-color: {COLORS['gray_100']};
                color: {COLORS['text_muted']};
            }}
        """)
    
    def setup_animations(self):
        """Setup tab switching animations"""
        self.currentChanged.connect(self._on_tab_changed)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def _on_tab_changed(self, index):
        """Handle tab change with animation"""
        if hasattr(self, '_animation') and self._animation.state() == QPropertyAnimation.State.Running:
            self._animation.stop()
        
        # Simple fade effect for tab content
        current_widget = self.widget(index)
        if current_widget:
            current_widget.setGraphicsEffect(None)  # Reset any existing effects
    
    def addTab(self, widget, text, icon=None):
        """Add a tab with optional icon"""
        index = super().addTab(widget, text)
        if icon:
            self.setTabIcon(index, icon)
        return index
    
    def addTabWithBadge(self, widget, text, badge_text=None, icon=None):
        """Add a tab with optional badge indicator"""
        index = self.addTab(widget, text, icon)
        if badge_text:
            # Create a custom tab button with badge
            tab_button = self._create_tab_with_badge(text, badge_text, icon)
            self.tabBar().setTabButton(index, QTabBar.ButtonPosition.LeftSide, tab_button)
        return index
    
    def _create_tab_with_badge(self, text, badge_text, icon=None):
        """Create a custom tab button with badge"""
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: {SPACING['sm']} {SPACING['md']};
                text-align: left;
                font-weight: 500;
                color: {COLORS['text_secondary']};
            }}
            QPushButton:hover {{
                color: {COLORS['text_primary']};
            }}
        """)
        
        # Add badge if provided
        if badge_text:
            badge = QLabel(badge_text)
            badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['danger']};
                    color: {COLORS['bg_primary']};
                    border-radius: 8px;
                    padding: 2px 6px;
                    font-size: 10px;
                    font-weight: bold;
                    margin-left: 8px;
                }}
            """)
            
            layout = QHBoxLayout(button)
            layout.addWidget(QLabel(text))
            layout.addWidget(badge)
            layout.addStretch()
        
        return button


class ModernSidebar(QFrame):
    """
    A modern sidebar component with navigation items and enhanced styling.
    
    Features:
    - Modern dark theme styling
    - Collapsible sections
    - Active state indicators
    - Smooth hover animations
    - Support for icons and badges
    - Responsive design
    
    Usage:
        sidebar = ModernSidebar()
        sidebar.add_nav_item("Dashboard", "dashboard", icon="📊")
        sidebar.add_nav_item("Quotes", "quotes", icon="📝", badge="3")
    """
    
    nav_item_clicked = Signal(str)  # Emits the item key when clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_items = {}
        self.active_item = None
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """Setup the sidebar UI layout"""
        self.setFixedWidth(280)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header section
        self.header = self._create_header()
        layout.addWidget(self.header)
        
        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
            QListWidget::item:selected {
                background-color: transparent;
            }
        """)
        self.nav_list.itemClicked.connect(self._on_nav_item_clicked)
        layout.addWidget(self.nav_list)
        
        # Bottom section (settings, etc.)
        self.bottom_section = self._create_bottom_section()
        layout.addWidget(self.bottom_section)
    
    def setup_style(self):
        """Apply modern dark theme styling"""
        self.setStyleSheet(f"""
            ModernSidebar {{
                background-color: {SIDEBAR_COLORS['sidebar_bg']};
                border: none;
            }}
        """)
    
    def _create_header(self):
        """Create the sidebar header with logo"""
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {SIDEBAR_COLORS['sidebar_header']};
                border-bottom: 1px solid {SIDEBAR_COLORS['sidebar_border']};
            }}
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # Logo/Brand
        logo_label = QLabel("Babbitt")
        logo_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        logo_label.setStyleSheet(f"color: {COLORS['primary']};")
        layout.addWidget(logo_label)
        
        return header
    
    def _create_bottom_section(self):
        """Create the bottom section for settings and user actions"""
        bottom = QFrame()
        bottom.setStyleSheet(f"""
            QFrame {{
                background-color: {SIDEBAR_COLORS['sidebar_bg']};
                border-top: 1px solid {SIDEBAR_COLORS['sidebar_border']};
            }}
        """)
        
        layout = QVBoxLayout(bottom)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Settings button
        settings_btn = self._create_nav_button("⚙️ Settings", "settings")
        layout.addWidget(settings_btn)
        
        return bottom
    
    def _create_nav_button(self, text, key, icon=None, badge=None):
        """Create a navigation button with optional icon and badge"""
        button = QPushButton(text)
        button.setProperty("nav_key", key)
        button.setMinimumHeight(48)
        button.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda: self._on_nav_item_clicked(key))
        
        # Apply styling
        self._update_nav_button_style(button, False)
        
        # Store reference
        self.nav_items[key] = button
        
        return button
    
    def _update_nav_button_style(self, button, active):
        """Update navigation button styling"""
        if active:
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary']};
                    color: {COLORS['bg_primary']};
                    border: none;
                    border-radius: {RADIUS['md']};
                    padding: 12px 16px;
                    text-align: left;
                    font-weight: 500;
                    margin: 2px 8px;
                }}
                QPushButton:hover {{
                    background-color: {SIDEBAR_COLORS['primary_hover']};
                }}
            """)
        else:
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {SIDEBAR_COLORS['sidebar_text']};
                    border: none;
                    border-radius: {RADIUS['md']};
                    padding: 12px 16px;
                    text-align: left;
                    font-weight: 500;
                    margin: 2px 8px;
                }}
                QPushButton:hover {{
                    background-color: {SIDEBAR_COLORS['sidebar_hover']};
                    color: {COLORS['bg_primary']};
                }}
            """)
    
    def add_nav_item(self, text, key, icon=None, badge=None):
        """Add a navigation item to the sidebar"""
        # Create list item
        item = QListWidgetItem()
        self.nav_list.addItem(item)
        
        # Create button widget
        button = self._create_nav_button(text, key, icon, badge)
        item.setSizeHint(button.sizeHint())
        
        # Set the button as the item widget
        self.nav_list.setItemWidget(item, button)
        
        return button
    
    def set_active_item(self, key):
        """Set the active navigation item"""
        if self.active_item == key:
            return
        
        # Update previous active item
        if self.active_item and self.active_item in self.nav_items:
            self._update_nav_button_style(self.nav_items[self.active_item], False)
        
        # Update new active item
        if key in self.nav_items:
            self._update_nav_button_style(self.nav_items[key], True)
            self.active_item = key
    
    def _on_nav_item_clicked(self, key):
        """Handle navigation item click"""
        self.set_active_item(key)
        self.nav_item_clicked.emit(key)


class ModernMenuBar(QMenuBar):
    """
    A modern menu bar with enhanced styling and functionality.
    
    Features:
    - Modern styling with hover effects
    - Dropdown menus with modern appearance
    - Keyboard shortcuts support
    - Responsive design
    
    Usage:
        menubar = ModernMenuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Quote")
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
    
    def setup_style(self):
        """Apply modern styling to the menu bar"""
        self.setStyleSheet(f"""
            QMenuBar {{
                background-color: {COLORS['bg_primary']};
                border-bottom: 1px solid {COLORS['border_light']};
                padding: 8px 16px;
                font-weight: 500;
                font-size: {FONTS['sizes']['sm']};
            }}
            
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 12px;
                border-radius: {RADIUS['sm']};
                margin: 0 2px;
            }}
            
            QMenuBar::item:selected {{
                background-color: {COLORS['secondary_hover']};
                color: {COLORS['text_primary']};
            }}
            
            QMenuBar::item:pressed {{
                background-color: {COLORS['primary']};
                color: {COLORS['bg_primary']};
            }}
            
            QMenu {{
                background-color: {COLORS['bg_primary']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']};
                padding: 8px 0;
            }}
            
            QMenu::item {{
                padding: 8px 16px;
                margin: 2px 8px;
                border-radius: {RADIUS['sm']};
            }}
            
            QMenu::item:selected {{
                background-color: {COLORS['secondary_hover']};
                color: {COLORS['text_primary']};
            }}
            
            QMenu::separator {{
                height: 1px;
                background-color: {COLORS['border_light']};
                margin: 4px 8px;
            }}
        """)


class ModernToolBar(QToolBar):
    """
    A modern toolbar with enhanced styling and functionality.
    
    Features:
    - Modern styling with hover effects
    - Icon and text support
    - Responsive design
    - Customizable appearance
    
    Usage:
        toolbar = ModernToolBar()
        toolbar.addAction("New", icon="➕")
        toolbar.addAction("Save", icon="💾")
    """
    
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setup_style()
        self.setup_behavior()
    
    def setup_style(self):
        """Apply modern styling to the toolbar"""
        self.setStyleSheet(f"""
            QToolBar {{
                background-color: {COLORS['bg_primary']};
                border-bottom: 1px solid {COLORS['border_light']};
                spacing: 8px;
                padding: 8px 16px;
            }}
            
            QToolButton {{
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: {RADIUS['md']};
                padding: 8px 12px;
                margin: 2px;
                font-weight: 500;
                font-size: {FONTS['sizes']['sm']};
                color: {COLORS['text_secondary']};
            }}
            
            QToolButton:hover {{
                background-color: {COLORS['secondary_hover']};
                border-color: {COLORS['border_light']};
                color: {COLORS['text_primary']};
            }}
            
            QToolButton:pressed {{
                background-color: {COLORS['primary']};
                color: {COLORS['bg_primary']};
            }}
            
            QToolButton:checked {{
                background-color: {COLORS['primary']};
                color: {COLORS['bg_primary']};
            }}
            
            QToolBar::separator {{
                width: 1px;
                background-color: {COLORS['border_light']};
                margin: 8px 4px;
            }}
        """)
    
    def setup_behavior(self):
        """Setup toolbar behavior"""
        self.setMovable(False)  # Disable moving for consistent layout
        self.setFloatable(False)  # Disable floating for consistent layout
    
    def addAction(self, text, icon=None, triggered=None):
        """Add an action with optional icon and signal connection"""
        action = QAction(text, self)
        if icon:
            action.setIcon(QIcon(icon))
        if triggered:
            action.triggered.connect(triggered)
        super().addAction(action)
        return action 