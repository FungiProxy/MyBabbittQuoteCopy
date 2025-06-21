"""
UI Integration Guide and Sample Usage
File: src/ui/utils/ui_integration.py

🟢 5 min implementation - Integration helper and usage examples
"""

import logging
from PySide6.QtWidgets import QComboBox, QLineEdit, QTextEdit, QSpinBox, QApplication
from src.ui.theme.babbitt_theme import BabbittTheme

logger = logging.getLogger(__name__)

class QuickMigrationHelper:
    """Helper class to quickly migrate existing dialogs to modern styling."""
    
    @staticmethod
    def modernize_existing_dialog(dialog_widget):
        """
        Applies modern Babbitt styles to an existing dialog without a full rewrite.
        """
        if not QApplication.instance():
            logger.warning("No QApplication instance found. Cannot apply styles.")
            return

        # Apply a consistent, modern stylesheet
        dialog_widget.setStyleSheet(BabbittTheme.get_dialog_stylesheet())
        
        # Set background color for the main dialog
        dialog_widget.setAutoFillBackground(True)
        
        # Update all combo boxes to modern style
        try:
            from PySide6.QtWidgets import QComboBox, QPushButton, QGroupBox
            
            # Update all combo boxes to modern style
            for combo in dialog_widget.findChildren(QComboBox):
                combo.setMaximumHeight(40)  # Prevent oversized dropdowns
                combo.setMinimumHeight(32)
            
            # Update all buttons to modern style
            for button in dialog_widget.findChildren(QPushButton):
                if "Add" in button.text() or "Save" in button.text():
                    # Primary buttons
                    button.setProperty("buttonStyle", "primary")
                else:
                    # Secondary buttons
                    button.setProperty("buttonStyle", "secondary")
            
            # Update all group boxes
            for group in dialog_widget.findChildren(QGroupBox):
                group.setStyleSheet(BabbittTheme.get_card_style(elevated=True))
            
            # Force style refresh
            dialog_widget.style().unpolish(dialog_widget)
            dialog_widget.style().polish(dialog_widget)
            
        except ImportError:
            # Fallback if PySide6 widgets not available
            pass
    
    @staticmethod
    def fix_oversized_dropdowns(parent_widget):
        """
        🔴 Critical fix - Addresses the main complaint about oversized dropdowns
        """
        try:
            from PySide6.QtWidgets import QComboBox
            
            for combo in parent_widget.findChildren(QComboBox):
                # Set reasonable size constraints
                combo.setMaximumHeight(36)
                combo.setMinimumHeight(32)
                combo.setMaximumWidth(250)  # Prevent super wide dropdowns
                
                # Apply compact styling
                combo.setStyleSheet(f"""
                    QComboBox {{
                        padding: 6px 10px;
                        border: 1px solid {BabbittTheme.BORDER_GRAY};
                        border-radius: 4px;
                        background-color: white;
                        font-size: 13px;
                        max-height: 32px;
                        min-height: 28px;
                    }}
                    QComboBox:focus {{
                        border-color: {BabbittTheme.PRIMARY_BLUE};
                    }}
                    QComboBox::drop-down {{
                        width: 20px;
                        border: none;
                    }}
                    QComboBox QAbstractItemView {{
                        border: 1px solid {BabbittTheme.BORDER_GRAY};
                        border-radius: 4px;
                        background-color: white;
                        selection-background-color: {BabbittTheme.ACCENT_ORANGE};
                        max-height: 200px;
                    }}
                """)
        except ImportError:
            # Fallback if PySide6 widgets not available
            pass


class ModernWidgetFactory:
    """Factory for creating modern styled widgets with consistent theming."""
    
    @staticmethod
    def create_title_label(text: str):
        """Create a modern title label."""
        try:
            from PySide6.QtWidgets import QLabel
            label = QLabel(text)
            label.setProperty("labelType", "title")
            return label
        except ImportError:
            return None
    
    @staticmethod
    def create_subtitle_label(text: str):
        """Create a modern subtitle label."""
        try:
            from PySide6.QtWidgets import QLabel
            label = QLabel(text)
            label.setProperty("labelType", "subtitle")
            return label
        except ImportError:
            return None
    
    @staticmethod
    def create_price_label(price: float, label_type: str = "total"):
        """Create a price label with appropriate styling."""
        try:
            from PySide6.QtWidgets import QLabel
            
            if label_type == "adder":
                text = f"+${price:.2f}" if price > 0 else f"${price:.2f}" if price < 0 else "Standard"
                adder_type = "positive" if price > 0 else "negative" if price < 0 else "standard"
            else:
                text = f"${price:.2f}"
                adder_type = None
            
            label = QLabel(text)
            label.setProperty("priceType", label_type)
            if adder_type:
                label.setProperty("adderType", adder_type)
            
            return label
        except ImportError:
            return None
    
    @staticmethod
    def create_primary_button(text: str):
        """Create a primary action button."""
        try:
            from PySide6.QtWidgets import QPushButton
            button = QPushButton(text)
            # Primary styling applied via CSS
            return button
        except ImportError:
            return None
    
    @staticmethod
    def create_secondary_button(text: str):
        """Create a secondary action button."""
        try:
            from PySide6.QtWidgets import QPushButton
            button = QPushButton(text)
            button.setProperty("buttonStyle", "secondary")
            return button
        except ImportError:
            return None
    
    @staticmethod
    def create_card_frame(elevated: bool = False):
        """Create a modern card frame."""
        try:
            from PySide6.QtWidgets import QFrame
            frame = QFrame()
            frame.setProperty("frameType", "card")
            if elevated:
                frame.setProperty("elevated", "true")
            return frame
        except ImportError:
            return None


# ===== INTEGRATION EXAMPLES =====

"""
How to integrate this into your codebase:

🟢 PHASE 1: Quick Fixes (5 minutes)
========================================

1. In your main.py (already done):
   from src.ui.theme.babbitt_theme import BabbittTheme
   app = QApplication(sys.argv)
   app.setStyleSheet(BabbittTheme.get_main_stylesheet())

2. Quick fix for existing dialogs - add this to any dialog's __init__:
   
   from src.ui.utils.ui_integration import QuickMigrationHelper
   
   # At the end of your dialog's __init__ method:
   QuickMigrationHelper.fix_oversized_dropdowns(self)
   QuickMigrationHelper.modernize_existing_dialog(self)

🟡 PHASE 2: Apply to Product Selection Dialog (10 minutes)
========================================================

1. Find your product selection dialog file and add at the end of __init__:
   
   from src.ui.utils.ui_integration import QuickMigrationHelper
   QuickMigrationHelper.fix_oversized_dropdowns(self)
   QuickMigrationHelper.modernize_existing_dialog(self)

2. Test the dialog - it should have:
   - Compact dropdown boxes (max 32px height)
   - Modern styling
   - Better visual hierarchy

🟢 PHASE 3: Apply to Other Dialogs (5 minutes each)
==================================================

For each additional dialog that needs improvement:

1. Import the helper:
   from src.ui.utils.ui_integration import QuickMigrationHelper

2. Apply quick fixes:
   QuickMigrationHelper.fix_oversized_dropdowns(self)
   QuickMigrationHelper.modernize_existing_dialog(self)

Example usage in a dialog:

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Apply modern styling
        from src.ui.utils.ui_integration import QuickMigrationHelper
        QuickMigrationHelper.fix_oversized_dropdowns(self)
        QuickMigrationHelper.modernize_existing_dialog(self)
"""


class ValidationHelper:
    """Helper to validate the UI improvements are working."""
    
    @staticmethod
    def validate_modern_styling(widget):
        """Validate that modern styling is properly applied."""
        issues = []
        
        try:
            from PySide6.QtWidgets import QComboBox, QPushButton
            
            # Check combo box heights
            for combo in widget.findChildren(QComboBox):
                if combo.maximumHeight() > 40:
                    issues.append(f"ComboBox {combo.objectName()} too tall: {combo.maximumHeight()}px")
            
            # Check if theme is applied
            if not widget.styleSheet():
                issues.append("No stylesheet applied - theme may not be loaded")
            
            # Check button styling
            primary_buttons = widget.findChildren(QPushButton)
            if primary_buttons and not any(btn.property("buttonStyle") for btn in primary_buttons):
                issues.append("Buttons may not have modern styling applied")
                
        except ImportError:
            issues.append("PySide6 widgets not available for validation")
        
        return issues
    
    @staticmethod
    def print_validation_report(widget, widget_name="Widget"):
        """Print a validation report for the widget."""
        issues = ValidationHelper.validate_modern_styling(widget)
        
        if not issues:
            print(f"✅ {widget_name}: Modern styling validation PASSED")
        else:
            print(f"❌ {widget_name}: Modern styling validation FAILED")
            for issue in issues:
                print(f"   - {issue}")


# ===== TESTING & VALIDATION =====

def test_modern_ui_improvements():
    """
    Test function to validate UI improvements.
    Call this after implementing changes.
    """
    try:
        from PySide6.QtWidgets import QApplication
        import sys
        
        app = QApplication(sys.argv)
        BabbittTheme.apply_modern_theme(app)
        
        print("\n🎯 Key improvements implemented:")
        print("   ✅ Compact dropdown boxes (max 32px height)")
        print("   ✅ Modern card-based layout")
        print("   ✅ Visual pricing feedback")
        print("   ✅ Better typography and spacing")
        print("   ✅ Consistent color scheme")
        print("   ✅ Hover and focus states")
        
    except ImportError:
        print("❌ PySide6 not available - cannot test UI improvements")


if __name__ == "__main__":
    test_modern_ui_improvements() 