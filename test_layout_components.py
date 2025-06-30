"""
Test Application for Modern Layout Components

This application demonstrates the modern layout components and their functionality.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

# Import modern components
from src.ui.components import (
    ModernScrollArea,
    ModernSplitter,
    ModernStackedWidget,
    ModernDockWidget,
    ModernLayoutContainer,
    ModernResizablePanel,
    ModernButton,
    ModernLineEdit,
    Card,
    StatusBadge
)

from src.ui.theme import COLORS, FONTS, SPACING, RADIUS


class LayoutComponentsDemo(QMainWindow):
    """Demo application for modern layout components."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Layout Components Demo")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
        self.apply_modern_styling()
    
    def setup_ui(self):
        """Setup the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(SPACING['2xl'], SPACING['2xl'], SPACING['2xl'], SPACING['2xl'])
        main_layout.setSpacing(SPACING['xl'])
        
        # Header
        header = QLabel("Modern Layout Components Demo")
        header.setStyleSheet(f"""
            font-size: {FONTS['sizes']['3xl']}px;
            font-weight: {FONTS['weights']['bold']};
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['lg']}px;
        """)
        main_layout.addWidget(header)
        
        # Create splitter for main content
        splitter = ModernSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Component list
        left_panel = self.create_component_list_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Component demo
        right_panel = self.create_demo_panel()
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
        # Bottom controls
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()
        
        # Test buttons
        test_scroll_btn = ModernButton("Test Scroll Area", "primary")
        test_scroll_btn.clicked.connect(self.test_scroll_area)
        controls_layout.addWidget(test_scroll_btn)
        
        test_splitter_btn = ModernButton("Test Splitter", "secondary")
        test_splitter_btn.clicked.connect(self.test_splitter)
        controls_layout.addWidget(test_splitter_btn)
        
        test_stacked_btn = ModernButton("Test Stacked Widget", "primary")
        test_stacked_btn.clicked.connect(self.test_stacked_widget)
        controls_layout.addWidget(test_stacked_btn)
        
        main_layout.addLayout(controls_layout)
    
    def create_component_list_panel(self):
        """Create the left panel with component list."""
        container = ModernLayoutContainer("Available Components")
        
        # Component list
        component_list = QListWidget()
        components = [
            "ModernScrollArea - Enhanced scroll area with modern styling",
            "ModernSplitter - Splitter with smooth animations",
            "ModernStackedWidget - Stacked widget with transitions",
            "ModernDockWidget - Dock widget with modern styling",
            "ModernLayoutContainer - Card-like layout container",
            "ModernResizablePanel - Resizable panel with drag handles"
        ]
        
        for component in components:
            item = QListWidgetItem(component)
            component_list.addItem(item)
        
        container.addWidget(component_list)
        
        return container
    
    def create_demo_panel(self):
        """Create the right panel with component demonstrations."""
        container = ModernLayoutContainer("Component Demonstrations")
        
        # Create stacked widget for different demos
        self.stacked_widget = ModernStackedWidget()
        
        # Page 1: Scroll Area Demo
        scroll_demo = self.create_scroll_area_demo()
        self.stacked_widget.addWidget(scroll_demo)
        
        # Page 2: Splitter Demo
        splitter_demo = self.create_splitter_demo()
        self.stacked_widget.addWidget(splitter_demo)
        
        # Page 3: Layout Container Demo
        container_demo = self.create_container_demo()
        self.stacked_widget.addWidget(container_demo)
        
        container.addWidget(self.stacked_widget)
        
        return container
    
    def create_scroll_area_demo(self):
        """Create scroll area demonstration."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(SPACING['lg'])
        
        # Title
        title = QLabel("ModernScrollArea Demo")
        title.setStyleSheet(f"""
            font-size: {FONTS['sizes']['xl']}px;
            font-weight: {FONTS['weights']['semibold']};
            color: {COLORS['text_primary']};
        """)
        layout.addWidget(title)
        
        # Create scroll area with content
        scroll_area = ModernScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(SPACING['md'])
        
        # Add lots of content to demonstrate scrolling
        for i in range(20):
            card = Card(f"Card {i+1}")
            card.add_widget(QLabel(f"This is the content for card {i+1}. It demonstrates how the modern scroll area handles content overflow with smooth scrolling and modern styling."))
            scroll_layout.addWidget(card)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        return widget
    
    def create_splitter_demo(self):
        """Create splitter demonstration."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(SPACING['lg'])
        
        # Title
        title = QLabel("ModernSplitter Demo")
        title.setStyleSheet(f"""
            font-size: {FONTS['sizes']['xl']}px;
            font-weight: {FONTS['weights']['semibold']};
            color: {COLORS['text_primary']};
        """)
        layout.addWidget(title)
        
        # Create splitter
        splitter = ModernSplitter(Qt.Orientation.Horizontal)
        
        # Left side
        left_container = ModernLayoutContainer("Left Panel")
        left_text = QTextEdit()
        left_text.setPlainText("This is the left panel of the splitter. You can drag the handle to resize the panels. The splitter provides smooth animations and modern styling.")
        left_container.addWidget(left_text)
        splitter.addWidget(left_container)
        
        # Right side
        right_container = ModernLayoutContainer("Right Panel")
        right_text = QTextEdit()
        right_text.setPlainText("This is the right panel of the splitter. The splitter handle has hover effects and smooth animations when you drag it.")
        right_container.addWidget(right_text)
        splitter.addWidget(right_container)
        
        layout.addWidget(splitter)
        
        return widget
    
    def create_container_demo(self):
        """Create layout container demonstration."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(SPACING['lg'])
        
        # Title
        title = QLabel("ModernLayoutContainer Demo")
        title.setStyleSheet(f"""
            font-size: {FONTS['sizes']['xl']}px;
            font-weight: {FONTS['weights']['semibold']};
            color: {COLORS['text_primary']};
        """)
        layout.addWidget(title)
        
        # Create containers
        containers_layout = QHBoxLayout()
        
        # Container 1
        container1 = ModernLayoutContainer("Container 1")
        container1.addWidget(QLabel("This is a modern layout container with card-like styling."))
        container1.addWidget(ModernButton("Button 1", "primary"))
        containers_layout.addWidget(container1)
        
        # Container 2
        container2 = ModernLayoutContainer("Container 2")
        container2.addWidget(QLabel("Containers provide consistent spacing and modern appearance."))
        container2.addWidget(ModernButton("Button 2", "secondary"))
        containers_layout.addWidget(container2)
        
        layout.addLayout(containers_layout)
        
        return widget
    
    def test_scroll_area(self):
        """Test scroll area functionality."""
        self.stacked_widget.setCurrentIndex(0)
        print("Testing ModernScrollArea...")
    
    def test_splitter(self):
        """Test splitter functionality."""
        self.stacked_widget.setCurrentIndex(1)
        print("Testing ModernSplitter...")
    
    def test_stacked_widget(self):
        """Test stacked widget functionality."""
        self.stacked_widget.setCurrentIndex(2)
        print("Testing ModernStackedWidget...")
    
    def apply_modern_styling(self):
        """Apply modern styling to the main window."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_secondary']};
            }}
        """)


def main():
    """Main function to run the demo."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Modern Layout Components Demo")
    app.setApplicationVersion("1.0")
    
    # Create and show the demo window
    demo = LayoutComponentsDemo()
    demo.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 