"""
Test Application for Modern Navigation Components

This script tests all the navigation components to ensure they work correctly
and display with proper styling.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt

# Import our navigation components
from src.ui.components import (
    ModernTabWidget,
    ModernSidebar,
    ModernMenuBar,
    ModernToolBar
)

# Import theme for consistent styling
from src.ui.theme.babbitt_theme import BabbittTheme


class NavigationTestWindow(QMainWindow):
    """Test window for navigation components"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navigation Components Test")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply theme
        self.setStyleSheet(BabbittTheme.get_main_stylesheet())
        
        # Setup UI
        self.setup_ui()
        
        # Connect signals
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the test UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create main content area
        self.content_area = self.create_content_area()
        main_layout.addWidget(self.content_area, 1)
    
    def create_sidebar(self):
        """Create and configure the modern sidebar"""
        sidebar = ModernSidebar()
        
        # Add navigation items
        sidebar.add_nav_item("📝 Quote Creator", "quote_creator")
        sidebar.add_nav_item("📂 All Quotes", "quotes")
        sidebar.add_nav_item("👥 Customers", "customers")
        sidebar.add_nav_item("📊 Analytics", "analytics", badge="3")
        sidebar.add_nav_item("⚙️ Settings", "settings")
        
        # Set initial active item
        sidebar.set_active_item("quote_creator")
        
        return sidebar
    
    def create_content_area(self):
        """Create the main content area with tabs and toolbar"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create menu bar
        self.menubar = self.create_menubar()
        content_layout.addWidget(self.menubar)
        
        # Create toolbar
        self.toolbar = self.create_toolbar()
        content_layout.addWidget(self.toolbar)
        
        # Create tab widget
        self.tab_widget = self.create_tab_widget()
        content_layout.addWidget(self.tab_widget)
        
        return content_widget
    
    def create_menubar(self):
        """Create and configure the modern menu bar"""
        menubar = ModernMenuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Quote")
        file_menu.addAction("Open Quote")
        file_menu.addAction("Save Quote")
        file_menu.addSeparator()
        file_menu.addAction("Export PDF")
        file_menu.addAction("Print")
        file_menu.addSeparator()
        file_menu.addAction("Exit")
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Zoom In")
        view_menu.addAction("Zoom Out")
        view_menu.addAction("Reset Zoom")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("User Guide")
        help_menu.addAction("About")
        
        return menubar
    
    def create_toolbar(self):
        """Create and configure the modern toolbar"""
        toolbar = ModernToolBar("Main Toolbar")
        
        # Add toolbar actions
        toolbar.addAction("➕ New Quote", triggered=self.on_new_quote)
        toolbar.addAction("💾 Save", triggered=self.on_save)
        toolbar.addAction("📤 Export", triggered=self.on_export)
        toolbar.addSeparator()
        toolbar.addAction("🔍 Search", triggered=self.on_search)
        toolbar.addAction("📊 Reports", triggered=self.on_reports)
        
        return toolbar
    
    def create_tab_widget(self):
        """Create and configure the modern tab widget"""
        tab_widget = ModernTabWidget()
        
        # Create tab content
        quote_tab = self.create_quote_tab()
        customers_tab = self.create_customers_tab()
        analytics_tab = self.create_analytics_tab()
        
        # Add tabs
        tab_widget.addTab(quote_tab, "Quote Creator")
        tab_widget.addTab(customers_tab, "Customers")
        tab_widget.addTab(analytics_tab, "Analytics")
        
        return tab_widget
    
    def create_quote_tab(self):
        """Create the quote creator tab content"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Quote Creator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Content
        content = QTextEdit()
        content.setPlaceholderText("Start creating your quote here...")
        content.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
            }
        """)
        layout.addWidget(content)
        
        return widget
    
    def create_customers_tab(self):
        """Create the customers tab content"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Customer Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Content
        content = QTextEdit()
        content.setPlaceholderText("Customer management interface will be implemented here...")
        content.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
            }
        """)
        layout.addWidget(content)
        
        return widget
    
    def create_analytics_tab(self):
        """Create the analytics tab content"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Analytics Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Content
        content = QTextEdit()
        content.setPlaceholderText("Analytics dashboard will be implemented here...")
        content.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
            }
        """)
        layout.addWidget(content)
        
        return widget
    
    def setup_connections(self):
        """Setup signal connections"""
        # Connect sidebar navigation
        self.sidebar.nav_item_clicked.connect(self.on_nav_item_clicked)
    
    def on_nav_item_clicked(self, key):
        """Handle sidebar navigation item clicks"""
        print(f"Navigation item clicked: {key}")
        
        # Update tab widget based on navigation
        if key == "quote_creator":
            self.tab_widget.setCurrentIndex(0)
        elif key == "quotes":
            self.tab_widget.setCurrentIndex(0)  # Could be a different tab
        elif key == "customers":
            self.tab_widget.setCurrentIndex(1)
        elif key == "analytics":
            self.tab_widget.setCurrentIndex(2)
        elif key == "settings":
            print("Settings clicked - would open settings dialog")
    
    def on_new_quote(self):
        """Handle new quote action"""
        print("New Quote action triggered")
    
    def on_save(self):
        """Handle save action"""
        print("Save action triggered")
    
    def on_export(self):
        """Handle export action"""
        print("Export action triggered")
    
    def on_search(self):
        """Handle search action"""
        print("Search action triggered")
    
    def on_reports(self):
        """Handle reports action"""
        print("Reports action triggered")


def main():
    """Main function to run the test application"""
    app = QApplication(sys.argv)
    
    # Create and show the test window
    window = NavigationTestWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 