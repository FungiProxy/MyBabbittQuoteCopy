"""
Quick UI Enhancement Utility

Apply immediate visual improvements to existing pages
without requiring complete rewrites. Perfect for end-of-day launch.

File: src/ui/utils/ui_enhancer.py
"""

from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel, QPushButton, QLineEdit, 
    QTextEdit, QTableWidget, QHeaderView, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt


class QuickUIEnhancer:
    """Utility to rapidly enhance existing UI elements."""
    
    @staticmethod
    def enhance_dashboard_page(dashboard_page):
        """Apply visual enhancements to the dashboard page."""
        # Find and enhance statistics cards
        for frame in dashboard_page.findChildren(QFrame):
            if frame.objectName() == "statCard":
                frame.setProperty("class", "stat-card")
                
                # Enhance labels within stat cards
                for label in frame.findChildren(QLabel):
                    text = label.text()
                    if text.isdigit() or '$' in text:  # Value labels
                        label.setProperty("class", "stat-value")
                    elif text.isupper() or len(text) < 20:  # Title labels
                        label.setProperty("class", "stat-label")
        
        # Add content container styling
        dashboard_page.setProperty("class", "content-container")
    
    @staticmethod
    def enhance_quote_creation_page(quote_page):
        """Apply visual enhancements to the quote creation page."""
        # Enhance customer information section
        for widget in quote_page.findChildren(QWidget):
            if "customer" in widget.objectName().lower():
                widget.setProperty("class", "form-section")
        
        # Enhance input fields
        for line_edit in quote_page.findChildren(QLineEdit):
            line_edit.setProperty("class", "customer-input")
            line_edit.setPlaceholderText(line_edit.placeholderText() or "Enter information...")
        
        # Enhance text areas
        for text_edit in quote_page.findChildren(QTextEdit):
            text_edit.setProperty("class", "notes-input")
        
        # Enhance action buttons
        for button in quote_page.findChildren(QPushButton):
            button_text = button.text().lower()
            if any(word in button_text for word in ['save', 'generate', 'send', 'add']):
                if 'add' in button_text:
                    button.setProperty("class", "action-button")
                else:
                    button.setProperty("class", "secondary-button")
    
    @staticmethod
    def enhance_customers_page(customers_page):
        """Apply visual enhancements to the customers page."""
        # Enhance the customer table
        for table in customers_page.findChildren(QTableWidget):
            table.setProperty("class", "data-table")
            
            # Enhance table header
            header = table.horizontalHeader()
            if header:
                header.setProperty("class", "table-header")
        
        # Add empty state if table is empty
        QuickUIEnhancer._add_empty_state_if_needed(customers_page, "No customers yet")
        
        # Enhance search box
        for line_edit in customers_page.findChildren(QLineEdit):
            if "search" in line_edit.objectName().lower():
                line_edit.setProperty("class", "customer-input")
                line_edit.setPlaceholderText("Search customers...")
    
    @staticmethod
    def enhance_settings_page(settings_page):
        """Apply visual enhancements to the settings page."""
        # Create form sections
        for widget in settings_page.findChildren(QWidget):
            if hasattr(widget, 'layout') and widget.layout():
                widget.setProperty("class", "form-section")
        
        # Enhance save button
        for button in settings_page.findChildren(QPushButton):
            if 'save' in button.text().lower():
                button.setProperty("class", "action-button")
    
    @staticmethod
    def _add_empty_state_if_needed(parent_widget, message):
        """Add an attractive empty state when content is missing."""
        # Check if there's already content
        tables = parent_widget.findChildren(QTableWidget)
        if tables and tables[0].rowCount() == 0:
            # Create empty state frame
            empty_frame = QFrame()
            empty_frame.setProperty("class", "empty-state")
            
            layout = QVBoxLayout(empty_frame)
            
            # Icon
            icon_label = QLabel("📊")
            icon_label.setProperty("class", "empty-state-icon")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label)
            
            # Title
            title_label = QLabel("Getting Started")
            title_label.setProperty("class", "empty-state-title")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)
            
            # Message
            message_label = QLabel(message)
            message_label.setProperty("class", "empty-state-text")
            message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(message_label)
    
    @staticmethod
    def apply_to_main_window(main_window):
        """Apply enhancements to all pages in the main window."""
        try:
            # Get the stacked widget containing all pages
            stacked_widget = main_window.stacked_widget
            
            for i in range(stacked_widget.count()):
                page = stacked_widget.widget(i)
                page_name = page.__class__.__name__.lower()
                
                if 'dashboard' in page_name or 'professional' in page_name:
                    QuickUIEnhancer.enhance_dashboard_page(page)
                elif 'quote' in page_name:
                    QuickUIEnhancer.enhance_quote_creation_page(page)
                elif 'customer' in page_name:
                    QuickUIEnhancer.enhance_customers_page(page)
                elif 'settings' in page_name:
                    QuickUIEnhancer.enhance_settings_page(page)
                
                # Refresh the styling
                page.style().unpolish(page)
                page.style().polish(page)
                page.update()
                
        except Exception as e:
            print(f"Enhancement error: {e}")


# Quick application function to enhance your current UI
def enhance_current_ui(main_window):
    """One-line function to enhance your existing UI immediately."""
    QuickUIEnhancer.apply_to_main_window(main_window)
    
    # Refresh the main window styling
    main_window.style().unpolish(main_window)
    main_window.style().polish(main_window)
    main_window.update()
    
    print("✨ UI enhancements applied!")


def test_ui_enhancement():
    """Test function to verify UI enhancement system is working."""
    print("🧪 Testing UI Enhancement System...")
    
    # Create a simple test widget
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
    
    app = QApplication([])
    
    # Create a test widget with various elements
    test_widget = QWidget()
    layout = QVBoxLayout(test_widget)
    
    # Add some test elements
    title = QLabel("Test Dashboard")
    title.setObjectName("pageTitle")
    layout.addWidget(title)
    
    stat_card = QFrame()
    stat_card.setObjectName("statCard")
    stat_layout = QVBoxLayout(stat_card)
    stat_layout.addWidget(QLabel("42"))
    stat_layout.addWidget(QLabel("TOTAL QUOTES"))
    layout.addWidget(stat_card)
    
    input_field = QLineEdit()
    input_field.setObjectName("customerName")
    layout.addWidget(input_field)
    
    action_button = QPushButton("Save")
    layout.addWidget(action_button)
    
    # Apply enhancements
    QuickUIEnhancer.enhance_dashboard_page(test_widget)
    QuickUIEnhancer.enhance_quote_creation_page(test_widget)
    
    # Show the widget
    test_widget.show()
    
    print("✅ UI Enhancement test completed!")
    print("   - Dashboard page enhanced")
    print("   - Quote creation page enhanced")
    print("   - Styling classes applied")
    
    return app.exec()


if __name__ == "__main__":
    test_ui_enhancement()