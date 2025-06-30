"""
Test Application for Advanced UI Features (Phase 7)

This application demonstrates the advanced features implemented in Phase 7:
- Theme switching (light/dark mode)
- Responsive design
- Accessibility features
- Animations
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QSlider, QCheckBox, QGroupBox, QGridLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# Import our advanced features
from src.ui.components import (
    ModernThemeToggle,
    ResponsiveManager,
    theme_manager,
    animation_manager,
    Breakpoint
)

from src.ui.theme import COLORS, FONTS, SPACING, RADIUS


class AdvancedFeaturesDemo(QMainWindow):
    """
    Demo application showcasing advanced UI features.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced UI Features Demo - Phase 7")
        self.setGeometry(100, 100, 1200, 800)
        
        # Setup UI
        self.setup_ui()
        self.setup_advanced_features()
        self.apply_modern_styling()
        
        # Start responsive monitoring
        self.responsive_manager.update_breakpoint()
    
    def setup_ui(self):
        """Setup the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(SPACING['lg'])
        main_layout.setContentsMargins(SPACING['xl'], SPACING['xl'], SPACING['xl'], SPACING['xl'])
        
        # Header
        self.create_header(main_layout)
        
        # Theme section
        self.create_theme_section(main_layout)
        
        # Responsive section
        self.create_responsive_section(main_layout)
        
        # Accessibility section
        self.create_accessibility_section(main_layout)
        
        # Animation section
        self.create_animation_section(main_layout)
        
        # Status section
        self.create_status_section(main_layout)
    
    def create_header(self, layout):
        """Create the header section."""
        header_group = QGroupBox("Advanced Features Demo - Phase 7")
        header_layout = QVBoxLayout(header_group)
        
        title = QLabel("Modern UI Advanced Features")
        title.setFont(QFont(FONTS['family'], 24, FONTS['weights']['bold']))
        title.setStyleSheet(f"color: {COLORS['text_primary']}; margin-bottom: {SPACING['md']}px;")
        
        subtitle = QLabel("Theme Switching • Responsive Design • Accessibility • Animations")
        subtitle.setFont(QFont(FONTS['family'], 14, FONTS['weights']['medium']))
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_group)
    
    def create_theme_section(self, layout):
        """Create the theme switching section."""
        theme_group = QGroupBox("Theme Switching")
        theme_layout = QVBoxLayout(theme_group)
        
        # Theme toggle
        self.theme_toggle = ModernThemeToggle()
        theme_layout.addWidget(self.theme_toggle)
        
        # Theme selector
        theme_selector_layout = QHBoxLayout()
        theme_selector_layout.addWidget(QLabel("Theme:"))
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light Theme", "Dark Theme"])
        self.theme_combo.setCurrentText("Light Theme")
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_selector_layout.addWidget(self.theme_combo)
        
        theme_layout.addLayout(theme_selector_layout)
        
        layout.addWidget(theme_group)
    
    def create_responsive_section(self, layout):
        """Create the responsive design section."""
        responsive_group = QGroupBox("Responsive Design")
        responsive_layout = QVBoxLayout(responsive_group)
        
        # Current breakpoint display
        self.breakpoint_label = QLabel("Current Breakpoint: Detecting...")
        self.breakpoint_label.setFont(QFont(FONTS['family'], 12, FONTS['weights']['semibold']))
        responsive_layout.addWidget(self.breakpoint_label)
        
        # Responsive controls
        controls_layout = QGridLayout()
        
        # Simulate different screen sizes
        size_buttons = [
            ("Mobile (XS)", 375),
            ("Tablet (SM)", 768),
            ("Small Desktop (MD)", 1024),
            ("Desktop (LG)", 1280),
            ("Large Desktop (XL)", 1536)
        ]
        
        for i, (label, width) in enumerate(size_buttons):
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, w=width: self.simulate_screen_size(w))
            controls_layout.addWidget(btn, i // 3, i % 3)
        
        responsive_layout.addLayout(controls_layout)
        
        layout.addWidget(responsive_group)
    
    def create_accessibility_section(self, layout):
        """Create the font scaling section."""
        font_group = QGroupBox("Font Scaling")
        font_layout = QVBoxLayout(font_group)
        
        # Font scaling controls
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("Font Scale:"))
        self.font_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_scale_slider.setRange(50, 200)
        self.font_scale_slider.setValue(100)
        self.font_scale_slider.valueChanged.connect(self.on_font_scale_changed)
        controls_layout.addWidget(self.font_scale_slider)
        
        self.font_scale_label = QLabel("100%")
        controls_layout.addWidget(self.font_scale_label)
        
        font_layout.addLayout(controls_layout)
        
        # Add a description
        description = QLabel("Adjust the font size throughout the application")
        description.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        font_layout.addWidget(description)
        
        layout.addWidget(font_group)
    
    def create_animation_section(self, layout):
        """Create the animation section."""
        animation_group = QGroupBox("Animations")
        animation_layout = QVBoxLayout(animation_group)
        
        # Animation controls
        controls_layout = QHBoxLayout()
        
        # Fade in/out buttons
        fade_in_btn = QPushButton("Fade In")
        fade_in_btn.clicked.connect(lambda: self.demo_fade_animation("in"))
        controls_layout.addWidget(fade_in_btn)
        
        fade_out_btn = QPushButton("Fade Out")
        fade_out_btn.clicked.connect(lambda: self.demo_fade_animation("out"))
        controls_layout.addWidget(fade_out_btn)
        
        # Slide buttons
        slide_left_btn = QPushButton("Slide Left")
        slide_left_btn.clicked.connect(lambda: self.demo_slide_animation("left"))
        controls_layout.addWidget(slide_left_btn)
        
        slide_right_btn = QPushButton("Slide Right")
        slide_right_btn.clicked.connect(lambda: self.demo_slide_animation("right"))
        controls_layout.addWidget(slide_right_btn)
        
        animation_layout.addLayout(controls_layout)
        
        # Animation demo area
        self.animation_demo = QLabel("Animation Demo Area")
        self.animation_demo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animation_demo.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['primary']};
                color: white;
                padding: {SPACING['lg']}px;
                border-radius: {RADIUS['lg']}px;
                font-size: {FONTS['sizes']['lg']}px;
                font-weight: {FONTS['weights']['semibold']};
            }}
        """)
        self.animation_demo.setMinimumHeight(100)
        animation_layout.addWidget(self.animation_demo)
        
        layout.addWidget(animation_group)
    
    def create_status_section(self, layout):
        """Create the status section."""
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_group)
    
    def setup_advanced_features(self):
        """Setup advanced features."""
        # Initialize managers
        self.responsive_manager = ResponsiveManager()
        
        # Connect signals
        self.responsive_manager.breakpoint_changed.connect(self.on_breakpoint_changed)
        self.theme_toggle.theme_toggled.connect(self.on_theme_toggled)
        theme_manager.theme_changed.connect(self.on_theme_manager_changed)
    
    def apply_modern_styling(self):
        """Apply modern styling to the window."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
            }}
            QGroupBox {{
                font-weight: {FONTS['weights']['semibold']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['lg']}px;
                margin-top: {SPACING['md']}px;
                padding-top: {SPACING['md']}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: {SPACING['md']}px;
                padding: 0 {SPACING['sm']}px 0 {SPACING['sm']}px;
                color: {COLORS['text_primary']};
            }}
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                padding: {SPACING['md']}px {SPACING['lg']}px;
                border-radius: {RADIUS['md']}px;
                font-weight: {FONTS['weights']['medium']};
                font-size: {FONTS['sizes']['base']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_pressed']};
            }}
            QComboBox {{
                background-color: {COLORS['bg_primary']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['sm']}px {SPACING['md']}px;
                font-size: {FONTS['sizes']['base']}px;
            }}
            QComboBox:hover {{
                border-color: {COLORS['border_medium']};
            }}
            QSlider::groove:horizontal {{
                border: 1px solid {COLORS['border_light']};
                height: 8px;
                background: {COLORS['bg_secondary']};
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['primary']};
                border: 1px solid {COLORS['primary']};
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }}
            QCheckBox {{
                font-size: {FONTS['sizes']['base']}px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {COLORS['border_light']};
                background: {COLORS['bg_primary']};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid {COLORS['primary']};
                background: {COLORS['primary']};
                border-radius: 3px;
            }}
        """)
    
    def on_theme_changed(self, theme_name):
        """Handle theme combo box changes."""
        if "Light" in theme_name:
            theme_manager.switch_theme("light", animate=True)
        else:
            theme_manager.switch_theme("dark", animate=True)
    
    def on_theme_toggled(self, theme_name):
        """Handle theme toggle changes."""
        self.theme_combo.setCurrentText(f"{theme_name.title()} Theme")
        self.update_status(f"Theme switched to {theme_name}")
    
    def on_theme_manager_changed(self, theme_name):
        """Handle theme manager changes."""
        self.apply_modern_styling()
        self.update_status(f"Theme applied: {theme_name}")
    
    def on_breakpoint_changed(self, breakpoint):
        """Handle breakpoint changes."""
        self.breakpoint_label.setText(f"Current Breakpoint: {breakpoint.name} ({breakpoint.value}px)")
        self.update_status(f"Breakpoint changed to {breakpoint.name}")
    
    def simulate_screen_size(self, width):
        """Simulate a different screen size."""
        # Resize window to simulate screen size
        self.resize(width, 600)
        self.update_status(f"Simulated screen width: {width}px")
    
    def on_font_scale_changed(self, value):
        """Handle font scale changes."""
        scale_factor = value / 100.0
        self.font_scale_label.setText(f"{value}%")
        self.update_status(f"Font scale: {value}%")
        self._apply_font_scale_to_widgets(self, scale_factor)
    
    def _apply_font_scale_to_widgets(self, widget, scale_factor):
        """Recursively apply font scaling to all child widgets."""
        font = widget.font()
        try:
            from src.ui.theme import FONTS
            base_size = FONTS['sizes'].get('base', 14)
        except Exception:
            base_size = 14
        font.setPointSize(int(base_size * scale_factor))
        widget.setFont(font)
        for child in widget.findChildren(QWidget):
            self._apply_font_scale_to_widgets(child, scale_factor)
    
    def demo_fade_animation(self, direction):
        """Demo fade animation."""
        from PySide6.QtWidgets import QGraphicsOpacityEffect
        try:
            # Ensure the label has an opacity effect
            if not hasattr(self.animation_demo, '_opacity_effect'):
                effect = QGraphicsOpacityEffect(self.animation_demo)
                self.animation_demo.setGraphicsEffect(effect)
                setattr(self.animation_demo, '_opacity_effect', effect)
            effect = getattr(self.animation_demo, '_opacity_effect')
            effect.setOpacity(1.0 if direction == "in" else 0.0)
            # Animate opacity
            from PySide6.QtCore import QPropertyAnimation
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(400)
            if direction == "in":
                anim.setStartValue(0.0)
                anim.setEndValue(1.0)
            else:
                anim.setStartValue(1.0)
                anim.setEndValue(0.0)
            anim.start()
            self._current_fade_anim = anim  # Keep reference
            self.update_status(f"Fade {direction} animation started")
        except Exception as e:
            self.update_status(f"Animation error: {str(e)}")
    
    def demo_slide_animation(self, direction):
        """Demo slide animation."""
        try:
            animation_manager.slide_in(self.animation_demo, direction)
            self.update_status(f"Slide {direction} animation started")
        except Exception as e:
            self.update_status(f"Animation error: {str(e)}")
    
    def update_status(self, message):
        """Update status message."""
        self.status_label.setText(message)
        print(f"Status: {message}")


def main():
    """Main function to run the demo."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Advanced UI Features Demo")
    app.setApplicationVersion("1.0")
    
    # Create and show demo window
    demo = AdvancedFeaturesDemo()
    demo.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 