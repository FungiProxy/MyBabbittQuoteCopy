#!/usr/bin/env python3
"""
Test application for modern UI components and styling system.

This script creates a simple window that demonstrates all the modern components
we've built, allowing us to verify they work correctly and look good.
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Import our modern components
from src.ui.components import (
    StatusBadge, Card, SearchBar, PriceDisplay, 
    LoadingSpinner, EmptyState, Notification
)

# Import styling system
from src.ui.theme import COLORS, FONTS, SPACING, RADIUS


class ComponentTestWindow(QMainWindow):
    """Test window to demonstrate all modern components."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the test window UI."""
        self.setWindowTitle("Modern Components Test - MyBabbittQuote")
        self.setMinimumSize(1000, 800)
        
        # Set application style
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_secondary']};
            }}
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(SPACING['2xl'], SPACING['2xl'], SPACING['2xl'], SPACING['2xl'])
        main_layout.setSpacing(SPACING['2xl'])
        
        # Header
        header_label = QLabel("Modern Components Test")
        header_label.setFont(QFont(FONTS['family'], FONTS['sizes']['3xl'], FONTS['weights']['bold']))
        header_label.setStyleSheet(f"color: {COLORS['text_primary']}; margin-bottom: {SPACING['lg']}px;")
        main_layout.addWidget(header_label)
        
        # Scroll area for components
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(SPACING['3xl'])
        
        # Add component demonstrations
        self.add_status_badges_demo(scroll_layout)
        self.add_card_demo(scroll_layout)
        self.add_search_bar_demo(scroll_layout)
        self.add_price_display_demo(scroll_layout)
        self.add_loading_spinner_demo(scroll_layout)
        self.add_empty_state_demo(scroll_layout)
        self.add_notification_demo(scroll_layout)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
    def add_status_badges_demo(self, layout):
        """Add status badges demonstration."""
        card = Card("Status Badges")
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(SPACING['lg'])
        
        # Description
        desc_label = QLabel("Status badges for displaying different states:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['sizes']['base']}px;")
        content_layout.addWidget(desc_label)
        
        # Badge examples
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(SPACING['md'])
        
        badges = [
            ("Draft", "draft"),
            ("Active", "active"),
            ("Completed", "completed"),
            ("Cancelled", "cancelled"),
            ("Info", "info")
        ]
        
        for text, status_type in badges:
            badge = StatusBadge(text, status_type)
            badges_layout.addWidget(badge)
        
        badges_layout.addStretch()
        content_layout.addLayout(badges_layout)
        
        card.add_layout(content_layout)
        layout.addWidget(card)
        
    def add_card_demo(self, layout):
        """Add card component demonstration."""
        card = Card("Card Component")
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(SPACING['lg'])
        
        # Description
        desc_label = QLabel("Cards provide organized containers for content:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['sizes']['base']}px;")
        content_layout.addWidget(desc_label)
        
        # Example content
        example_card = Card("Example Card")
        example_content = QVBoxLayout()
        
        info_label = QLabel("This is an example card with some content inside.")
        info_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: {FONTS['sizes']['base']}px;")
        example_content.addWidget(info_label)
        
        example_card.add_layout(example_content)
        content_layout.addWidget(example_card)
        
        card.add_layout(content_layout)
        layout.addWidget(card)
        
    def add_search_bar_demo(self, layout):
        """Add search bar demonstration."""
        card = Card("Search Bar")
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(SPACING['lg'])
        
        # Description
        desc_label = QLabel("Modern search bar with real-time functionality:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['sizes']['base']}px;")
        content_layout.addWidget(desc_label)
        
        # Search bar
        search_bar = SearchBar("Search for quotes, customers, or products...")
        search_bar.search_changed.connect(self.on_search_changed)
        content_layout.addWidget(search_bar)
        
        # Search results label
        self.search_results_label = QLabel("Type in the search bar above to see results...")
        self.search_results_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: {FONTS['sizes']['sm']}px;")
        content_layout.addWidget(self.search_results_label)
        
        card.add_layout(content_layout)
        layout.addWidget(card)
        
    def add_price_display_demo(self, layout):
        """Add price display demonstration."""
        card = Card("Price Display")
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(SPACING['lg'])
        
        # Description
        desc_label = QLabel("Price displays with different sizes and formatting:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['sizes']['base']}px;")
        content_layout.addWidget(desc_label)
        
        # Price examples
        prices_layout = QVBoxLayout()
        prices_layout.setSpacing(SPACING['md'])
        
        small_price = PriceDisplay(425.00, "$", "small")
        normal_price = PriceDisplay(1250.75, "$", "normal")
        large_price = PriceDisplay(5000.00, "$", "large")
        
        prices_layout.addWidget(QLabel("Small:"))
        prices_layout.addWidget(small_price)
        prices_layout.addWidget(QLabel("Normal:"))
        prices_layout.addWidget(normal_price)
        prices_layout.addWidget(QLabel("Large:"))
        prices_layout.addWidget(large_price)
        
        content_layout.addLayout(prices_layout)
        
        card.add_layout(content_layout)
        layout.addWidget(card)
        
    def add_loading_spinner_demo(self, layout):
        """Add loading spinner demonstration."""
        card = Card("Loading Spinner")
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(SPACING['lg'])
        
        # Description
        desc_label = QLabel("Loading spinners for async operations:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['sizes']['base']}px;")
        content_layout.addWidget(desc_label)
        
        # Spinner examples
        spinners_layout = QHBoxLayout()
        spinners_layout.setSpacing(SPACING['xl'])
        
        small_spinner = LoadingSpinner(24)
        medium_spinner = LoadingSpinner(32)
        large_spinner = LoadingSpinner(48)
        
        spinners_layout.addWidget(QLabel("Small:"))
        spinners_layout.addWidget(small_spinner)
        spinners_layout.addWidget(QLabel("Medium:"))
        spinners_layout.addWidget(medium_spinner)
        spinners_layout.addWidget(QLabel("Large:"))
        spinners_layout.addWidget(large_spinner)
        spinners_layout.addStretch()
        
        content_layout.addLayout(spinners_layout)
        
        # Start all spinners
        small_spinner.start()
        medium_spinner.start()
        large_spinner.start()
        
        card.add_layout(content_layout)
        layout.addWidget(card)
        
    def add_empty_state_demo(self, layout):
        """Add empty state demonstration."""
        card = Card("Empty State")
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(SPACING['lg'])
        
        # Description
        desc_label = QLabel("Empty states for when lists or tables are empty:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['sizes']['base']}px;")
        content_layout.addWidget(desc_label)
        
        # Empty state example
        empty_state = EmptyState(
            "No quotes found",
            "Create your first quote to get started with the application.",
            "Create New Quote"
        )
        empty_state.action_button.clicked.connect(self.on_create_quote)
        content_layout.addWidget(empty_state)
        
        card.add_layout(content_layout)
        layout.addWidget(card)
        
    def add_notification_demo(self, layout):
        """Add notification demonstration."""
        card = Card("Notifications")
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(SPACING['lg'])
        
        # Description
        desc_label = QLabel("Toast notifications for user feedback:")
        desc_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: {FONTS['sizes']['base']}px;")
        content_layout.addWidget(desc_label)
        
        # Notification buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(SPACING['md'])
        
        from PySide6.QtWidgets import QPushButton
        from src.ui.theme import get_button_style
        
        success_btn = QPushButton("Success Notification")
        success_btn.setStyleSheet(get_button_style('primary'))
        success_btn.clicked.connect(lambda: self.show_notification("Quote saved successfully!", "success"))
        
        error_btn = QPushButton("Error Notification")
        error_btn.setStyleSheet(get_button_style('danger'))
        error_btn.clicked.connect(lambda: self.show_notification("Failed to save quote!", "error"))
        
        warning_btn = QPushButton("Warning Notification")
        warning_btn.setStyleSheet(get_button_style('secondary'))
        warning_btn.clicked.connect(lambda: self.show_notification("Please check your input!", "warning"))
        
        info_btn = QPushButton("Info Notification")
        info_btn.setStyleSheet(get_button_style('secondary'))
        info_btn.clicked.connect(lambda: self.show_notification("New features available!", "info"))
        
        buttons_layout.addWidget(success_btn)
        buttons_layout.addWidget(error_btn)
        buttons_layout.addWidget(warning_btn)
        buttons_layout.addWidget(info_btn)
        buttons_layout.addStretch()
        
        content_layout.addLayout(buttons_layout)
        
        card.add_layout(content_layout)
        layout.addWidget(card)
        
    def on_search_changed(self, text):
        """Handle search text changes."""
        if text:
            self.search_results_label.setText(f"Searching for: '{text}'")
        else:
            self.search_results_label.setText("Type in the search bar above to see results...")
            
    def on_create_quote(self):
        """Handle create quote button click."""
        self.show_notification("Create quote functionality would be triggered here!", "info")
        
    def show_notification(self, message, notification_type):
        """Show a notification."""
        notification = Notification(message, notification_type, self)
        notification.show_notification(self)


def main():
    """Main function to run the test application."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Modern Components Test")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Babbitt International")
    
    # Set modern font
    font = QFont(FONTS['family'], 10)
    app.setFont(font)
    
    # Create and show test window
    window = ComponentTestWindow()
    window.show()
    
    print("🚀 Modern Components Test Application Started!")
    print("✅ Testing all modern components and styling system...")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 