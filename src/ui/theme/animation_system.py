"""
Python Animation System for Babbitt Industrial Theme
Replicates CSS transform, transition, and shadow effects using PySide6
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, QParallelAnimationGroup, QSequentialAnimationGroup, QObject, QEvent
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Property, QRect, QPoint


class BabbittAnimationSystem:
    """Python-based animation system to replicate CSS effects."""
    
    @staticmethod
    def apply_nav_item_hover_animation(widget, direction="right"):
        """Apply navigation item hover slide animation (translateX)."""
        # Create slide animation
        slide_anim = QPropertyAnimation(widget, b"pos")
        slide_anim.setDuration(200)
        slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Get current position
        current_pos = widget.pos()
        
        if direction == "right":
            # Slide right by 4px (matching CSS translateX(4px))
            slide_anim.setStartValue(current_pos)
            slide_anim.setEndValue(current_pos + QPoint(4, 0))
        else:
            # Slide left by 4px
            slide_anim.setStartValue(current_pos + QPoint(4, 0))
            slide_anim.setEndValue(current_pos)
        
        return slide_anim
    
    @staticmethod
    def apply_card_hover_animation(widget, direction="up"):
        """Apply card hover lift animation (translateY)."""
        # Create lift animation
        lift_anim = QPropertyAnimation(widget, b"pos")
        lift_anim.setDuration(200)
        lift_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Get current position
        current_pos = widget.pos()
        
        if direction == "up":
            # Lift up by 2px (matching CSS translateY(-2px))
            lift_anim.setStartValue(current_pos)
            lift_anim.setEndValue(current_pos + QPoint(0, -2))
        else:
            # Return to original position
            lift_anim.setStartValue(current_pos + QPoint(0, -2))
            lift_anim.setEndValue(current_pos)
        
        return lift_anim
    
    @staticmethod
    def apply_button_press_animation(widget, direction="down"):
        """Apply button press animation (translateY)."""
        # Create press animation
        press_anim = QPropertyAnimation(widget, b"pos")
        press_anim.setDuration(100)
        press_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Get current position
        current_pos = widget.pos()
        
        if direction == "down":
            # Press down by 1px (matching CSS translateY(1px))
            press_anim.setStartValue(current_pos)
            press_anim.setEndValue(current_pos + QPoint(0, 1))
        else:
            # Return to original position
            press_anim.setStartValue(current_pos + QPoint(0, 1))
            press_anim.setEndValue(current_pos)
        
        return press_anim
    
    @staticmethod
    def apply_button_hover_lift(widget, direction="up"):
        """Apply primary button hover lift animation."""
        # Create lift animation
        lift_anim = QPropertyAnimation(widget, b"pos")
        lift_anim.setDuration(200)
        lift_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Get current position
        current_pos = widget.pos()
        
        if direction == "up":
            # Lift up by 1px (matching CSS translateY(-1px))
            lift_anim.setStartValue(current_pos)
            lift_anim.setEndValue(current_pos + QPoint(0, -1))
        else:
            # Return to original position
            lift_anim.setStartValue(current_pos + QPoint(0, -1))
            lift_anim.setEndValue(current_pos)
        
        return lift_anim
    
    @staticmethod
    def apply_shadow_effect(widget, shadow_type="card"):
        """Apply different shadow effects based on type."""
        shadow = QGraphicsDropShadowEffect()
        
        if shadow_type == "card":
            # Card shadow: 0 2px 8px rgba(0, 0, 0, 0.1)
            shadow.setBlurRadius(8)
            shadow.setColor(QColor(0, 0, 0, 25))
            shadow.setOffset(0, 2)
        elif shadow_type == "premium":
            # Premium shadow: 0 4px 16px rgba(0, 0, 0, 0.15)
            shadow.setBlurRadius(16)
            shadow.setColor(QColor(0, 0, 0, 38))
            shadow.setOffset(0, 4)
        elif shadow_type == "elevated":
            # Elevated shadow: 0 8px 32px rgba(0, 0, 0, 0.2)
            shadow.setBlurRadius(32)
            shadow.setColor(QColor(0, 0, 0, 51))
            shadow.setOffset(0, 8)
        elif shadow_type == "button":
            # Button shadow: 0 2px 8px rgba(0, 82, 204, 0.15)
            shadow.setBlurRadius(8)
            shadow.setColor(QColor(0, 82, 204, 38))
            shadow.setOffset(0, 2)
        elif shadow_type == "primary_button":
            # Primary button shadow: 0 2px 8px rgba(0, 82, 204, 0.3)
            shadow.setBlurRadius(8)
            shadow.setColor(QColor(0, 82, 204, 76))
            shadow.setOffset(0, 2)
        elif shadow_type == "focus":
            # Focus glow: 0 0 0 3px rgba(0, 82, 204, 0.3)
            shadow.setBlurRadius(3)
            shadow.setColor(QColor(0, 82, 204, 76))
            shadow.setOffset(0, 0)
        elif shadow_type == "inset":
            # Inset shadow for selected nav items: inset 0 1px 0 rgba(255, 255, 255, 0.2)
            shadow.setBlurRadius(1)
            shadow.setColor(QColor(255, 255, 255, 51))
            shadow.setOffset(0, 1)
        elif shadow_type == "button_hover":
            # Button hover shadow: 0 2px 8px rgba(0, 82, 204, 0.15)
            shadow.setBlurRadius(8)
            shadow.setColor(QColor(0, 82, 204, 38))
            shadow.setOffset(0, 2)
        elif shadow_type == "button_pressed":
            # Button pressed shadow: 0 2px 8px rgba(0, 82, 204, 0.3)
            shadow.setBlurRadius(8)
            shadow.setColor(QColor(0, 82, 204, 76))
            shadow.setOffset(0, 2)
        
        widget.setGraphicsEffect(shadow)
        return shadow
    
    @staticmethod
    def apply_focus_glow_animation(widget, show=True):
        """Apply focus glow animation."""
        if show:
            # Show focus glow
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(3)
            shadow.setColor(QColor(0, 82, 204, 76))
            shadow.setOffset(0, 0)
            widget.setGraphicsEffect(shadow)
        else:
            # Remove focus glow
            widget.setGraphicsEffect(None)
    
    @staticmethod
    def create_shadow_animation(widget, start_shadow_type, end_shadow_type, duration=200):
        """Create smooth shadow transition animation."""
        # Remove current shadow
        widget.setGraphicsEffect(None)
        
        # Apply new shadow
        BabbittAnimationSystem.apply_shadow_effect(widget, end_shadow_type)
        
        # Create opacity animation for smooth transition
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(duration)
        opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        opacity_anim.setStartValue(0.7)
        opacity_anim.setEndValue(1.0)
        
        return opacity_anim
    
    @staticmethod
    def create_hover_animation_group(widget, animation_type="card"):
        """Create a complete hover animation group."""
        group = QParallelAnimationGroup()
        
        if animation_type == "nav_item":
            # Navigation item: slide + shadow
            slide_anim = BabbittAnimationSystem.apply_nav_item_hover_animation(widget, "right")
            group.addAnimation(slide_anim)
            
        elif animation_type == "card":
            # Card: lift + shadow transition
            lift_anim = BabbittAnimationSystem.apply_card_hover_animation(widget, "up")
            group.addAnimation(lift_anim)
            
            # Apply premium shadow with transition
            shadow_anim = BabbittAnimationSystem.create_shadow_animation(widget, "card", "premium")
            group.addAnimation(shadow_anim)
            
        elif animation_type == "button":
            # Button: lift + shadow transition
            lift_anim = BabbittAnimationSystem.apply_button_hover_lift(widget, "up")
            group.addAnimation(lift_anim)
            
            # Apply button hover shadow with transition
            shadow_anim = BabbittAnimationSystem.create_shadow_animation(widget, "button", "button_hover")
            group.addAnimation(shadow_anim)
        
        return group
    
    @staticmethod
    def create_leave_animation_group(widget, animation_type="card"):
        """Create a complete leave animation group."""
        group = QParallelAnimationGroup()
        
        if animation_type == "nav_item":
            # Navigation item: slide back
            slide_anim = BabbittAnimationSystem.apply_nav_item_hover_animation(widget, "left")
            group.addAnimation(slide_anim)
            
        elif animation_type == "card":
            # Card: return to original position + shadow
            lift_anim = BabbittAnimationSystem.apply_card_hover_animation(widget, "down")
            group.addAnimation(lift_anim)
            
            # Return to card shadow
            shadow_anim = BabbittAnimationSystem.create_shadow_animation(widget, "premium", "card")
            group.addAnimation(shadow_anim)
            
        elif animation_type == "button":
            # Button: return to original position + shadow
            lift_anim = BabbittAnimationSystem.apply_button_hover_lift(widget, "down")
            group.addAnimation(lift_anim)
            
            # Return to button shadow
            shadow_anim = BabbittAnimationSystem.create_shadow_animation(widget, "button_hover", "button")
            group.addAnimation(shadow_anim)
        
        return group
    
    @staticmethod
    def create_press_animation_group(widget):
        """Create a complete press animation group."""
        group = QSequentialAnimationGroup()
        
        # Press down
        press_down = BabbittAnimationSystem.apply_button_press_animation(widget, "down")
        group.addAnimation(press_down)
        
        # Apply pressed shadow
        BabbittAnimationSystem.apply_shadow_effect(widget, "button_pressed")
        
        # Return to original position
        press_up = BabbittAnimationSystem.apply_button_press_animation(widget, "up")
        group.addAnimation(press_up)
        
        return group
    
    @staticmethod
    def create_selected_nav_animation(widget):
        """Create animation for selected navigation item with inset shadow."""
        # Apply inset shadow for selected state
        BabbittAnimationSystem.apply_shadow_effect(widget, "inset")
        
        # Create subtle glow animation
        glow_anim = QPropertyAnimation(widget, b"pos")
        glow_anim.setDuration(300)
        glow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        current_pos = widget.pos()
        glow_anim.setStartValue(current_pos)
        glow_anim.setEndValue(current_pos + QPoint(1, 0))
        
        return glow_anim
    
    @staticmethod
    def create_smooth_transition(widget, property_name, start_value, end_value, duration=200):
        """Create a smooth transition animation for any property."""
        anim = QPropertyAnimation(widget, property_name.encode())
        anim.setDuration(duration)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.setStartValue(start_value)
        anim.setEndValue(end_value)
        return anim


class AnimatedWidget:
    """Wrapper class to add animation capabilities to any widget."""
    
    def __init__(self):
        self._hover_animation = None
        self._leave_animation = None
        self._press_animation = None
        self._current_shadow = None
        self._widget = None
    
    def setup_hover_animation(self, animation_type="card"):
        """Setup hover animation for the widget."""
        self._animation_type = animation_type
    
    def setup_press_animation(self):
        """Setup press animation for the widget."""
        pass  # Press animations are handled by the main system
    
    def on_mouse_enter(self, widget):
        """Handle mouse enter event."""
        if self._animation_type:
            self._hover_animation = BabbittAnimationSystem.create_hover_animation_group(widget, self._animation_type)
            self._hover_animation.start()
    
    def on_mouse_leave(self, widget):
        """Handle mouse leave event."""
        if self._animation_type:
            self._leave_animation = BabbittAnimationSystem.create_leave_animation_group(widget, self._animation_type)
            self._leave_animation.start()
    
    def on_mouse_press(self, widget):
        """Handle mouse press event."""
        if self._animation_type == "button":
            self._press_animation = BabbittAnimationSystem.create_press_animation_group(widget)
            self._press_animation.start()
    
    def apply_shadow(self, shadow_type="card"):
        """Apply shadow effect to the widget."""
        self._current_shadow = shadow_type
    
    def apply_focus_glow(self, show=True):
        """Apply focus glow effect."""
        pass  # Focus glow is handled by the main system


# ============================================================================
# ANIMATION INTEGRATION HELPERS
# ============================================================================

def setup_widget_animations(widget, widget_type="card"):
    """Setup animations for a widget based on its type."""
    if not widget:
        return
    
    # Create animated widget wrapper
    animated_widget = AnimatedWidget()
    
    if widget_type == "nav_item":
        # Navigation item: slide + shadow effects
        animated_widget.setup_hover_animation("nav_item")
        animated_widget.setup_press_animation()
        
    elif widget_type == "card":
        # Card: lift + shadow effects
        animated_widget.setup_hover_animation("card")
        animated_widget.setup_press_animation()
        
    elif widget_type == "button":
        # Button: lift + shadow effects
        animated_widget.setup_hover_animation("button")
        animated_widget.setup_press_animation()
        
    elif widget_type == "form":
        # Form elements: focus glow effects - use event filter for proper handling
        BabbittAnimationSystem.apply_focus_glow_animation(widget, False)  # Start without glow
        
        # Create event filter to handle focus without overriding default behavior
        class FocusEventFilter(QObject):
            def __init__(self, target_widget):
                super().__init__()
                self.target_widget = target_widget
            
            def eventFilter(self, obj, event):
                if obj == self.target_widget:
                    if event.type() == QEvent.Type.FocusIn:
                        BabbittAnimationSystem.apply_focus_glow_animation(self.target_widget, True)
                    elif event.type() == QEvent.Type.FocusOut:
                        BabbittAnimationSystem.apply_focus_glow_animation(self.target_widget, False)
                return False  # Don't consume the event, let Qt handle it normally
        
        # Install event filter
        focus_filter = FocusEventFilter(widget)
        widget.installEventFilter(focus_filter)
        
        # Store the filter to prevent garbage collection
        widget._focus_filter = focus_filter
    
    # Store the animated widget reference
    widget.animated_widget = animated_widget
    
    # Apply initial shadow
    if widget_type in ["card", "button"]:
        animated_widget.apply_shadow("card" if widget_type == "card" else "button")


def apply_text_transform(widget, transform_type="uppercase"):
    """Apply text transform effects."""
    if transform_type == "uppercase":
        current_text = widget.text()
        widget.setText(current_text.upper())
    elif transform_type == "lowercase":
        current_text = widget.text()
        widget.setText(current_text.lower())
    elif transform_type == "capitalize":
        current_text = widget.text()
        widget.setText(current_text.title()) 