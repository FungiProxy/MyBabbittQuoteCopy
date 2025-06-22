"""
Test Enhanced Animations for Babbitt Industrial Theme
Demonstrates all the missing animations that were added to match the original CSS theme.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFrame, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

# Add the src directory to the path
sys.path.append('src')

from ui.theme.babbitt_industrial_theme import BabbittIndustrialTheme, BabbittIndustrialIntegration
from ui.theme.animation_system import BabbittAnimationSystem, setup_widget_animations


class AnimationTestWindow(QMainWindow):
    """Test window to demonstrate all enhanced animations."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Animations Test - Babbitt Industrial Theme")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply the industrial theme
        BabbittIndustrialIntegration.apply_premium_theme(self)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QHBoxLayout(central_widget)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        layout.addWidget(sidebar)
        
        # Create main content
        main_content = self.create_main_content()
        layout.addWidget(main_content)
        
        # Setup all animations
        self.setup_animations()
    
    def create_sidebar(self):
        """Create sidebar with navigation items."""
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebarFrame")
        sidebar_frame.setFixedWidth(220)
        
        layout = QVBoxLayout(sidebar_frame)
        
        # Logo
        logo = QLabel("BABBITT INDUSTRIAL")
        logo.setObjectName("logoLabel")
        layout.addWidget(logo)
        
        # Navigation list
        nav_list = QListWidget()
        nav_list.setObjectName("navList")
        
        nav_items = [
            "Dashboard",
            "New Quote", 
            "Product Configuration",
            "Customers",
            "Settings"
        ]
        
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            nav_list.addItem(item)
        
        layout.addWidget(nav_list)
        
        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.setObjectName("settingsButton")
        layout.addWidget(settings_btn)
        
        layout.addStretch()
        return sidebar_frame
    
    def create_main_content(self):
        """Create main content area with test elements."""
        content_frame = QFrame()
        content_frame.setObjectName("contentAreaFrame")
        
        layout = QVBoxLayout(content_frame)
        
        # Header
        header = QFrame()
        header.setObjectName("contentHeader")
        header.setFixedHeight(70)
        
        header_layout = QHBoxLayout(header)
        title = QLabel("Enhanced Animations Test")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # Test content
        content_layout = QHBoxLayout()
        
        # Left column - Cards
        left_column = QVBoxLayout()
        
        # Metric cards
        for i in range(3):
            card = self.create_metric_card(f"Metric {i+1}", f"Value {i+1}", f"Description {i+1}")
            card.setObjectName("metricCard")
            left_column.addWidget(card)
        
        content_layout.addLayout(left_column)
        
        # Right column - Buttons
        right_column = QVBoxLayout()
        
        # Test buttons
        primary_btn = BabbittIndustrialIntegration.create_animated_button("Primary Button", "primary")
        primary_btn.setObjectName("newQuoteButton")
        right_column.addWidget(primary_btn)
        
        secondary_btn = BabbittIndustrialIntegration.create_animated_button("Secondary Button", "secondary")
        right_column.addWidget(secondary_btn)
        
        # Form elements
        form_frame = QFrame()
        form_frame.setObjectName("contentCard")
        form_layout = QVBoxLayout(form_frame)
        
        form_title = QLabel("Form Elements")
        form_title.setObjectName("sectionTitle")
        form_layout.addWidget(form_title)
        
        # Add some form elements for testing
        from PySide6.QtWidgets import QLineEdit, QComboBox, QSpinBox
        
        line_edit = QLineEdit("Test Input")
        line_edit.setPlaceholderText("Enter text...")
        form_layout.addWidget(line_edit)
        
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        form_layout.addWidget(combo)
        
        spinbox = QSpinBox()
        spinbox.setRange(0, 100)
        spinbox.setValue(50)
        form_layout.addWidget(spinbox)
        
        right_column.addWidget(form_frame)
        right_column.addStretch()
        
        content_layout.addLayout(right_column)
        
        layout.addLayout(content_layout)
        return content_frame
    
    def create_metric_card(self, title, value, subtitle):
        """Create a metric card for testing."""
        card = QFrame()
        card.setObjectName("metricCard")
        card.setFixedSize(200, 120)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("metricValue")
        layout.addWidget(value_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("metricSubtitle")
        layout.addWidget(subtitle_label)
        
        return card
    
    def setup_animations(self):
        """Setup all enhanced animations."""
        # Setup navigation animations
        nav_list = self.findChild(QListWidget, "navList")
        if nav_list:
            BabbittIndustrialIntegration.setup_navigation_animations(nav_list)
        
        # Setup button animations
        for button in self.findChildren(QPushButton):
            if button.objectName() in ['newQuoteButton', 'settingsButton']:
                setup_widget_animations(button, "button")
        
        # Setup card animations
        for frame in self.findChildren(QFrame):
            if frame.objectName() in ['metricCard', 'contentCard']:
                setup_widget_animations(frame, "card")
        
        # Setup form animations - search for each type separately
        from PySide6.QtWidgets import QLineEdit, QComboBox, QSpinBox
        
        for line_edit in self.findChildren(QLineEdit):
            setup_widget_animations(line_edit, "form")
        
        for combo in self.findChildren(QComboBox):
            setup_widget_animations(combo, "form")
        
        for spinbox in self.findChildren(QSpinBox):
            setup_widget_animations(spinbox, "form")


def main():
    """Run the animation test."""
    app = QApplication(sys.argv)
    
    # Apply the industrial theme stylesheet
    app.setStyleSheet(BabbittIndustrialTheme.get_main_stylesheet())
    
    # Create and show the test window
    window = AnimationTestWindow()
    window.show()
    
    print("🎨 Enhanced Animations Test Window")
    print("=" * 50)
    print("This window demonstrates all the enhanced animations:")
    print("✅ Navigation item slide effects (translateX)")
    print("✅ Card lift animations (translateY)")
    print("✅ Button press animations (translateY)")
    print("✅ Shadow transitions")
    print("✅ Inset shadows for selected nav items")
    print("✅ Focus glow effects for form elements")
    print("✅ Smooth hover/leave transitions")
    print("\nTry hovering over different elements to see the animations!")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 