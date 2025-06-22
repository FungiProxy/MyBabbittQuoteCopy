#!/usr/bin/env python3
"""
Test script for Python Animation System
Demonstrates all the CSS effects replicated in Python
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt

from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialTheme, BabbittIndustrialIntegration
from src.ui.theme.animation_system import BabbittAnimationSystem, setup_widget_animations

def test_python_animations():
    """Test the Python animation system with a simple window."""
    
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Python Animation System Test")
    window.resize(800, 600)
    
    # Apply the industrial theme
    BabbittIndustrialIntegration.apply_premium_theme(window)
    
    # Create central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout(central_widget)
    layout.setContentsMargins(40, 40, 40, 40)
    layout.setSpacing(20)
    
    # Title
    title = QLabel("Python Animation System Test")
    title.setObjectName("pageTitle")
    layout.addWidget(title)
    
    # Test animated buttons
    button_layout = QHBoxLayout()
    
    # Regular button with animations
    regular_btn = BabbittIndustrialIntegration.create_animated_button("Regular Button", "secondary")
    button_layout.addWidget(regular_btn)
    
    # Primary button with animations
    primary_btn = BabbittIndustrialIntegration.create_animated_button("Primary Button", "primary")
    button_layout.addWidget(primary_btn)
    
    layout.addLayout(button_layout)
    
    # Test animated metric card
    metric_card = BabbittIndustrialIntegration.create_metric_card(
        "Test Metric", 
        "1,234", 
        "Sample data with animations", 
        "📊"
    )
    layout.addWidget(metric_card)
    
    # Test focus effects
    focus_label = QLabel("Click to test focus glow")
    focus_label.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
    layout.addWidget(focus_label)
    
    # Connect focus effects
    focus_label.mousePressEvent = lambda e: BabbittIndustrialIntegration.apply_focus_effects(focus_label, True)
    focus_label.mouseReleaseEvent = lambda e: BabbittIndustrialIntegration.apply_focus_effects(focus_label, False)
    
    # Add stretch
    layout.addStretch()
    
    # Status labels
    success_label = QLabel("Success Status")
    success_label.setProperty("status", "success")
    layout.addWidget(success_label)
    
    warning_label = QLabel("Warning Status")
    warning_label.setProperty("status", "warning")
    layout.addWidget(warning_label)
    
    error_label = QLabel("Error Status")
    error_label.setProperty("status", "error")
    layout.addWidget(error_label)
    
    info_label = QLabel("Info Status")
    info_label.setProperty("status", "info")
    layout.addWidget(info_label)
    
    print("🏭 Python Animation System Test Window Created")
    print("   ✨ All CSS effects replicated in Python")
    print("   🎯 Hover animations on cards and buttons")
    print("   🔥 Press animations on buttons")
    print("   💎 Focus glow effects")
    print("   📊 Text transform effects")
    print("   🎨 Shadow effects")
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    test_python_animations() 