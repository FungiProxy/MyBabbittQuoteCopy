"""
Accessibility System

This module provides comprehensive accessibility features for the modern UI,
including screen reader support, keyboard navigation, and ARIA attributes.
"""

from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit, QComboBox, QGroupBox, QSlider, QCheckBox
from PySide6.QtGui import QKeySequence, QShortcut
from typing import Dict, List, Optional, Callable
import enum


class AccessibilityLevel(enum.Enum):
    """Accessibility support levels."""
    BASIC = "basic"           # Basic keyboard navigation
    STANDARD = "standard"     # Standard accessibility features
    ENHANCED = "enhanced"     # Enhanced accessibility with ARIA
    FULL = "full"            # Full accessibility compliance


class AccessibilityManager(QObject):
    """
    Manages accessibility features throughout the application.
    
    Features:
    - Screen reader support
    - Keyboard navigation
    - ARIA attributes
    - Focus management
    - High contrast mode
    - Font scaling
    """
    
    # Signals
    accessibility_level_changed = Signal(AccessibilityLevel)
    focus_changed = Signal(QWidget)
    keyboard_shortcut_triggered = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.accessibility_level = AccessibilityLevel.STANDARD
        self.focus_trail = []
        self.keyboard_shortcuts = {}
        self.aria_attributes = {}
        self.high_contrast_mode = False
        self.font_scale_factor = 1.0
        
        # Setup accessibility features
        self.setup_accessibility()
    
    def setup_accessibility(self):
        """Setup basic accessibility features."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Enable accessibility features
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    def set_accessibility_level(self, level: AccessibilityLevel):
        """Set the accessibility support level."""
        if level != self.accessibility_level:
            self.accessibility_level = level
            self.accessibility_level_changed.emit(level)
            self.apply_accessibility_level(level)
    
    def get_accessibility_level(self) -> AccessibilityLevel:
        """Get the current accessibility level."""
        return self.accessibility_level
    
    def apply_accessibility_level(self, level: AccessibilityLevel):
        """Apply accessibility features based on level."""
        if level == AccessibilityLevel.BASIC:
            self.setup_basic_accessibility()
        elif level == AccessibilityLevel.STANDARD:
            self.setup_standard_accessibility()
        elif level == AccessibilityLevel.ENHANCED:
            self.setup_enhanced_accessibility()
        elif level == AccessibilityLevel.FULL:
            self.setup_full_accessibility()
    
    def setup_basic_accessibility(self):
        """Setup basic accessibility features."""
        # Enable basic keyboard navigation
        self.enable_keyboard_navigation()
    
    def setup_standard_accessibility(self):
        """Setup standard accessibility features."""
        self.setup_basic_accessibility()
        # Add focus indicators
        self.enable_focus_indicators()
        # Add basic ARIA support
        self.enable_basic_aria()
    
    def setup_enhanced_accessibility(self):
        """Setup enhanced accessibility features."""
        self.setup_standard_accessibility()
        # Add enhanced ARIA support
        self.enable_enhanced_aria()
        # Add keyboard shortcuts
        self.setup_keyboard_shortcuts()
    
    def setup_full_accessibility(self):
        """Setup full accessibility compliance."""
        self.setup_enhanced_accessibility()
        # Add screen reader optimizations
        self.optimize_for_screen_readers()
        # Add high contrast support
        self.enable_high_contrast_mode()
    
    def enable_keyboard_navigation(self):
        """Enable keyboard navigation throughout the app."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Set focus policy for better keyboard navigation
            for widget in app.findChildren(QWidget):
                if isinstance(widget, (QPushButton, QLineEdit, QComboBox)):
                    widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def enable_focus_indicators(self):
        """Enable visible focus indicators."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Apply visible focus styles to all interactive widgets
            for widget in app.findChildren(QWidget):
                if isinstance(widget, (QPushButton, QLineEdit, QComboBox, QSlider, QCheckBox)):
                    # Set focus policy to show focus indicators
                    widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
                    # Apply focus styles
                    current_style = widget.styleSheet()
                    focus_style = """
                        QWidget:focus {
                            border: 2px solid #0052cc;
                            border-radius: 4px;
                            background-color: rgba(0, 82, 204, 0.1);
                        }
                    """
                    widget.setStyleSheet(current_style + focus_style)
    
    def enable_basic_aria(self):
        """Enable basic ARIA attribute support."""
        # Set basic accessibility properties
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            for widget in app.findChildren(QWidget):
                if isinstance(widget, QPushButton):
                    widget.setAccessibleName(widget.text())
                    # Add visual indicator for ARIA support
                    widget.setToolTip(f"Accessible button: {widget.text()}")
                elif isinstance(widget, QLabel):
                    widget.setAccessibleName(widget.text())
                    widget.setToolTip(f"Accessible label: {widget.text()}")
    
    def enable_enhanced_aria(self):
        """Enable enhanced ARIA attribute support."""
        # Add more detailed ARIA attributes
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            for widget in app.findChildren(QWidget):
                if isinstance(widget, QPushButton):
                    widget.setAccessibleDescription(f"Button: {widget.text()}")
                    widget.setToolTip(f"Enhanced accessible button: {widget.text()}\nRole: Button\nAction: Click to activate")
                elif isinstance(widget, QLineEdit):
                    widget.setAccessibleDescription("Text input field")
                    widget.setToolTip("Enhanced accessible text input\nRole: Text field\nAction: Type to enter text")
                elif isinstance(widget, QComboBox):
                    widget.setAccessibleDescription("Dropdown selection")
                    widget.setToolTip("Enhanced accessible dropdown\nRole: Combo box\nAction: Select from options")
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for accessibility."""
        app = QApplication.instance()
        if not app or not isinstance(app, QApplication):
            return
        
        # Common accessibility shortcuts
        shortcuts = {
            'F1': 'help',
            'F6': 'next_panel',
            'Shift+F6': 'previous_panel',
            'Escape': 'close_dialog',
            'Enter': 'activate',
            'Space': 'toggle'
        }
        
        for key_sequence, action in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key_sequence), app)
            shortcut.activated.connect(lambda checked, a=action: self.handle_shortcut(a))
            self.keyboard_shortcuts[key_sequence] = shortcut
        
        # Add visual indicator that shortcuts are active
        self._show_shortcuts_active_indicator()
    
    def _show_shortcuts_active_indicator(self):
        """Show visual indicator that keyboard shortcuts are active."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Add a subtle visual indicator to the main window
            main_window = app.activeWindow()
            if main_window:
                current_style = main_window.styleSheet()
                shortcut_indicator = """
                    QMainWindow {
                        border-left: 3px solid #28a745;
                    }
                """
                main_window.setStyleSheet(current_style + shortcut_indicator)
    
    def handle_shortcut(self, action: str):
        """Handle keyboard shortcut actions."""
        self.keyboard_shortcut_triggered.emit(action)
        
        if action == 'help':
            self.show_help()
        elif action == 'next_panel':
            self.navigate_next_panel()
        elif action == 'previous_panel':
            self.navigate_previous_panel()
        elif action == 'close_dialog':
            self.close_active_dialog()
    
    def show_help(self):
        """Show accessibility help."""
        # Create a simple help dialog or notification
        from PySide6.QtWidgets import QMessageBox
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            help_dialog = QMessageBox()
            help_dialog.setWindowTitle("Accessibility Help")
            help_dialog.setText("Keyboard Navigation Help")
            help_dialog.setInformativeText(
                "• Tab: Navigate between elements\n"
                "• Shift+Tab: Navigate backwards\n"
                "• Enter/Space: Activate buttons\n"
                "• F1: Show this help\n"
                "• F6: Next panel\n"
                "• Shift+F6: Previous panel\n"
                "• Escape: Close dialogs"
            )
            help_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            help_dialog.exec()
    
    def navigate_next_panel(self):
        """Navigate to the next panel."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Find all group boxes (panels) and cycle through them
            group_boxes = app.findChildren(QGroupBox)
            if group_boxes:
                current_focus = app.focusWidget()
                if current_focus:
                    current_panel = current_focus.parent()
                    while current_panel and not isinstance(current_panel, QGroupBox):
                        current_panel = current_panel.parent()
                    
                    if current_panel in group_boxes:
                        current_index = group_boxes.index(current_panel)
                        next_index = (current_index + 1) % len(group_boxes)
                        next_panel = group_boxes[next_index]
                        # Focus the first focusable widget in the next panel
                        for child in next_panel.findChildren(QWidget):
                            if child.focusPolicy() != Qt.FocusPolicy.NoFocus:
                                child.setFocus()
                                break
    
    def navigate_previous_panel(self):
        """Navigate to the previous panel."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Find all group boxes (panels) and cycle through them
            group_boxes = app.findChildren(QGroupBox)
            if group_boxes:
                current_focus = app.focusWidget()
                if current_focus:
                    current_panel = current_focus.parent()
                    while current_panel and not isinstance(current_panel, QGroupBox):
                        current_panel = current_panel.parent()
                    
                    if current_panel in group_boxes:
                        current_index = group_boxes.index(current_panel)
                        prev_index = (current_index - 1) % len(group_boxes)
                        prev_panel = group_boxes[prev_index]
                        # Focus the first focusable widget in the previous panel
                        for child in prev_panel.findChildren(QWidget):
                            if child.focusPolicy() != Qt.FocusPolicy.NoFocus:
                                child.setFocus()
                                break
    
    def close_active_dialog(self):
        """Close the active dialog."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            active_window = app.activeWindow()
            if active_window and active_window != app.activeWindow():
                active_window.close()
    
    def optimize_for_screen_readers(self):
        """Optimize the UI for screen readers."""
        # Set proper tab order
        self.setup_tab_order()
        # Add descriptive labels
        self.add_descriptive_labels()
        # Optimize focus management
        self.optimize_focus_management()
        # Add visual indicator for screen reader optimization
        self._show_screen_reader_indicator()
    
    def _show_screen_reader_indicator(self):
        """Show visual indicator that screen reader optimizations are active."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            main_window = app.activeWindow()
            if main_window:
                current_style = main_window.styleSheet()
                sr_indicator = """
                    QMainWindow {
                        border-right: 3px solid #17a2b8;
                    }
                """
                main_window.setStyleSheet(current_style + sr_indicator)
    
    def setup_tab_order(self):
        """Setup logical tab order for keyboard navigation."""
        # This would be implemented based on the specific UI layout
        pass
    
    def add_descriptive_labels(self):
        """Add descriptive labels for screen readers."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            for widget in app.findChildren(QWidget):
                if isinstance(widget, QPushButton) and not widget.accessibleName():
                    widget.setAccessibleName(widget.text())
                elif isinstance(widget, QLineEdit) and not widget.accessibleName():
                    # Try to find associated label
                    label = self.find_associated_label(widget)
                    if label:
                        widget.setAccessibleName(label.text())
    
    def find_associated_label(self, widget: QWidget) -> Optional[QLabel]:
        """Find label associated with a widget."""
        # This is a simplified implementation
        # In a real app, you'd need more sophisticated label association
        parent = widget.parent()
        if parent:
            for child in parent.findChildren(QLabel):
                if child.buddy() == widget:
                    return child
        return None
    
    def optimize_focus_management(self):
        """Optimize focus management for screen readers."""
        # Ensure focus is properly managed
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            app.focusChanged.connect(self.on_focus_changed)
    
    def on_focus_changed(self, old_widget: QWidget, new_widget: QWidget):
        """Handle focus changes."""
        if new_widget:
            self.focus_trail.append(new_widget)
            # Keep only last 10 focus changes
            if len(self.focus_trail) > 10:
                self.focus_trail.pop(0)
            
            self.focus_changed.emit(new_widget)
    
    def enable_high_contrast_mode(self):
        """Enable high contrast mode."""
        self.high_contrast_mode = True
        self.apply_high_contrast_styles()
    
    def disable_high_contrast_mode(self):
        """Disable high contrast mode."""
        self.high_contrast_mode = False
        self.apply_normal_styles()
    
    def apply_high_contrast_styles(self):
        """Apply high contrast styles."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # High contrast color scheme
            high_contrast_styles = """
                QMainWindow, QWidget {
                    background-color: #000000;
                    color: #ffffff;
                    border: 2px solid #ffffff;
                }
                QGroupBox {
                    background-color: #000000;
                    color: #ffffff;
                    border: 3px solid #ffffff;
                    font-weight: bold;
                }
                QGroupBox::title {
                    color: #ffffff;
                    background-color: #000000;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 3px solid #ffffff;
                    font-weight: bold;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #ffff00;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #cccccc;
                    color: #000000;
                }
                QComboBox {
                    background-color: #ffffff;
                    color: #000000;
                    border: 3px solid #ffffff;
                    font-weight: bold;
                }
                QComboBox:hover {
                    background-color: #ffff00;
                    color: #000000;
                }
                QSlider::groove:horizontal {
                    border: 2px solid #ffffff;
                    background: #000000;
                    height: 10px;
                }
                QSlider::handle:horizontal {
                    background: #ffffff;
                    border: 2px solid #000000;
                    width: 20px;
                    margin: -5px 0;
                }
                QCheckBox {
                    color: #ffffff;
                    font-weight: bold;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 3px solid #ffffff;
                    background: #000000;
                }
                QCheckBox::indicator:checked {
                    background: #ffffff;
                    border: 3px solid #ffffff;
                }
                QLabel {
                    color: #ffffff;
                    font-weight: bold;
                }
            """
            app.setStyleSheet(high_contrast_styles)
    
    def apply_normal_styles(self):
        """Apply normal styles."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Clear the stylesheet to return to normal
            app.setStyleSheet("")
            # Re-apply the original theme if available
            try:
                from src.ui.theme.theme_manager import theme_manager
                theme_manager._apply_current_theme()
            except ImportError:
                pass
    
    def set_font_scale(self, scale_factor: float):
        """Set font scaling factor."""
        self.font_scale_factor = max(0.5, min(3.0, scale_factor))
        self.apply_font_scaling()
    
    def apply_font_scaling(self):
        """Apply font scaling to all widgets."""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            font = app.font()
            font.setPointSize(int(font.pointSize() * self.font_scale_factor))
            app.setFont(font)
    
    def register_widget_for_accessibility(self, widget: QWidget, 
                                        accessible_name: str = "",
                                        accessible_description: str = ""):
        """Register a widget for accessibility support."""
        if accessible_name:
            widget.setAccessibleName(accessible_name)
        if accessible_description:
            widget.setAccessibleDescription(accessible_description)


class AccessibleWidget(QWidget):
    """
    Base class for widgets with enhanced accessibility support.
    
    Features:
    - Automatic accessibility setup
    - Screen reader optimization
    - Keyboard navigation support
    - ARIA attribute management
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.accessibility_manager = AccessibilityManager()
        self.setup_accessibility()
    
    def setup_accessibility(self):
        """Setup accessibility for this widget."""
        # Set focus policy
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Register with accessibility manager
        self.accessibility_manager.register_widget_for_accessibility(
            self,
            accessible_name=self.get_accessible_name(),
            accessible_description=self.get_accessible_description()
        )
    
    def get_accessible_name(self) -> str:
        """Get accessible name for this widget."""
        # Override in subclasses
        return self.objectName() or self.__class__.__name__
    
    def get_accessible_description(self) -> str:
        """Get accessible description for this widget."""
        # Override in subclasses
        return ""
    
    def keyPressEvent(self, event):
        """Handle key press events for accessibility."""
        # Handle common accessibility keys
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.activate()
        elif event.key() == Qt.Key.Key_Space:
            self.toggle()
        elif event.key() == Qt.Key.Key_Escape:
            self.cancel()
        else:
            super().keyPressEvent(event)
    
    def activate(self):
        """Activate the widget (for accessibility)."""
        # Override in subclasses
        pass
    
    def toggle(self):
        """Toggle the widget (for accessibility)."""
        # Override in subclasses
        pass
    
    def cancel(self):
        """Cancel the widget action (for accessibility)."""
        # Override in subclasses
        pass


# Global accessibility manager instance
accessibility_manager = AccessibilityManager() 