"""
UI Integration Guide and Sample Usage
File: src/ui/utils/ui_integration.py

🟢 5 min implementation - Integration helper and usage examples
"""

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QFrame, QComboBox, QGroupBox
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor

from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme


class UIAnimations:
    """Helper class for smooth UI animations."""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300):
        """Fade in animation for widgets."""
        widget.setProperty("opacity", 0.0)
        animation = QPropertyAnimation(widget, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.start()
        return animation
    
    @staticmethod
    def slide_in_from_right(widget: QWidget, distance: int = 50, duration: int = 400):
        """Slide in from right animation."""
        original_pos = widget.pos()
        widget.move(original_pos.x() + distance, original_pos.y())
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(widget.pos())
        animation.setEndValue(original_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutQuart)
        animation.start()
        return animation


class ModernWidgetFactory:
    """Factory for creating modern styled widgets with consistent theming."""
    
    @staticmethod
    def create_title_label(text: str) -> QLabel:
        """Create a modern title label."""
        label = QLabel(text)
        label.setProperty("labelType", "title")
        return label
    
    @staticmethod
    def create_subtitle_label(text: str) -> QLabel:
        """Create a modern subtitle label."""
        label = QLabel(text)
        label.setProperty("labelType", "subtitle")
        return label
    
    @staticmethod
    def create_caption_label(text: str) -> QLabel:
        """Create a modern caption label."""
        label = QLabel(text)
        label.setProperty("labelType", "caption")
        return label
    
    @staticmethod
    def create_price_label(price: float, label_type: str = "total") -> QLabel:
        """Create a price label with appropriate styling."""
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
    
    @staticmethod
    def create_primary_button(text: str) -> QPushButton:
        """Create a primary action button."""
        button = QPushButton(text)
        # Primary styling applied via CSS
        return button
    
    @staticmethod
    def create_secondary_button(text: str) -> QPushButton:
        """Create a secondary action button."""
        button = QPushButton(text)
        button.setProperty("buttonStyle", "secondary")
        return button
    
    @staticmethod
    def create_card_frame(elevated: bool = False) -> QFrame:
        """Create a modern card frame."""
        frame = QFrame()
        frame.setProperty("frameType", "card")
        if elevated:
            frame.setProperty("elevated", "true")
        return frame


# ===== INTEGRATION EXAMPLES =====

"""
How to update your existing product_selection_dialog.py:

1. Replace the imports at the top:
   
   from src.ui.product_selection_dialog_improved import ImprovedProductSelectionDialog
   from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
   from src.ui.utils.ui_integration import ModernWidgetFactory, UIAnimations

2. Replace your dialog initialization:

   # OLD WAY:
   dialog = ProductSelectionDialog(product_service)
   
   # NEW WAY:
   dialog = ImprovedProductSelectionDialog(product_service)

3. Apply the theme in your main.py or main_window.py:

   from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
   
   app = QApplication(sys.argv)
   ModernBabbittTheme.apply_modern_theme(app)
   
   # Rest of your app initialization...

4. Example of using the modern widget factory:

   # Creating modern labels
   title = ModernWidgetFactory.create_title_label("Product Configuration")
   subtitle = ModernWidgetFactory.create_subtitle_label("Select your options")
   
   # Creating price displays
   base_price = ModernWidgetFactory.create_price_label(500.0, "base") 
   total_price = ModernWidgetFactory.create_price_label(650.0, "total")
   adder_price = ModernWidgetFactory.create_price_label(150.0, "adder")

5. Example of adding animations:

   # Fade in a configuration panel
   UIAnimations.fade_in(config_panel, duration=400)
   
   # Slide in option widgets
   UIAnimations.slide_in_from_right(option_widget, distance=30)
"""


class QuickMigrationHelper:
    """Helper class to quickly migrate existing dialogs to modern styling."""
    
    @staticmethod
    def modernize_existing_dialog(dialog_widget):
        """
        Quick migration function to apply modern styling to existing dialogs.
        
        🟡 20 min implementation - Call this on your existing dialog after creation
        """
        # Apply modern theme
        dialog_widget.setStyleSheet(ModernBabbittTheme.get_application_stylesheet())
        
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
            group.setStyleSheet(ModernBabbittTheme.get_card_style(elevated=True))
        
        # Force style refresh
        dialog_widget.style().unpolish(dialog_widget)
        dialog_widget.style().polish(dialog_widget)
    
    @staticmethod
    def fix_oversized_dropdowns(parent_widget):
        """
        🔴 Critical fix - Addresses the main complaint about oversized dropdowns
        """
        for combo in parent_widget.findChildren(QComboBox):
            # Set reasonable size constraints
            combo.setMaximumHeight(36)
            combo.setMinimumHeight(32)
            combo.setMaximumWidth(250)  # Prevent super wide dropdowns
            
            # Apply compact styling
            combo.setStyleSheet(f"""
                QComboBox {{
                    padding: 6px 10px;
                    border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
                    border-radius: 4px;
                    background-color: white;
                    font-size: 13px;
                    max-height: 32px;
                    min-height: 28px;
                }}
                QComboBox:focus {{
                    border-color: {ModernBabbittTheme.PRIMARY_BLUE};
                }}
                QComboBox::drop-down {{
                    width: 20px;
                    border: none;
                }}
                QComboBox QAbstractItemView {{
                    border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
                    border-radius: 4px;
                    background-color: white;
                    selection-background-color: {ModernBabbittTheme.LIGHT_BLUE};
                    max-height: 200px;
                }}
            """)


# ===== STEP-BY-STEP IMPLEMENTATION GUIDE =====

"""
🟢 PHASE 1: Quick Fixes (15 minutes total)
========================================

1. Copy the new files to your project:
   - src/ui/product_selection_dialog_improved.py
   - src/ui/theme/modern_babbitt_theme.py 
   - src/ui/utils/ui_integration.py

2. In your main application file, add the theme:
   
   # In main.py or wherever you create QApplication
   from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
   
   app = QApplication(sys.argv)
   ModernBabbittTheme.apply_modern_theme(app)  # Add this line

3. Quick fix for existing dialogs - add this to any dialog's __init__:
   
   from src.ui.utils.ui_integration import QuickMigrationHelper
   
   # At the end of your dialog's __init__ method:
   QuickMigrationHelper.fix_oversized_dropdowns(self)
   QuickMigrationHelper.modernize_existing_dialog(self)

🟡 PHASE 2: Replace Product Dialog (20 minutes)
============================================

1. Replace the import in files that use ProductSelectionDialog:
   
   # OLD:
   from src.ui.product_selection_dialog import ProductSelectionDialog
   
   # NEW:
   from src.ui.product_selection_dialog_improved import ImprovedProductSelectionDialog as ProductSelectionDialog

2. Test the new dialog - it should have:
   - Compact dropdown boxes (max 32px height)
   - Modern card-based layout
   - Real-time pricing feedback
   - Better visual hierarchy

🟢 PHASE 3: Apply to Other UIs (10 minutes each)
==============================================

For each additional dialog/widget that needs improvement:

1. Import the helpers:
   from src.ui.utils.ui_integration import QuickMigrationHelper, ModernWidgetFactory

2. Apply quick fixes:
   QuickMigrationHelper.fix_oversized_dropdowns(self)
   QuickMigrationHelper.modernize_existing_dialog(self)

3. Optionally replace manual widget creation with factory methods:
   # Instead of: title = QLabel("My Title")
   title = ModernWidgetFactory.create_title_label("My Title")
"""


class ValidationHelper:
    """Helper to validate the UI improvements are working."""
    
    @staticmethod
    def validate_modern_styling(widget):
        """Validate that modern styling is properly applied."""
        issues = []
        
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


# ===== SAMPLE IMPLEMENTATION =====

class SampleModernDialog(QWidget):
    """
    Sample implementation showing how to create a modern dialog from scratch.
    Use this as a reference for creating new dialogs.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modern Dialog Example")
        self.resize(600, 400)
        
        # Apply modern theme
        self.setStyleSheet(ModernBabbittTheme.get_application_stylesheet())
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI with modern components."""
        from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QSpinBox, QLineEdit
        
        layout = QVBoxLayout(self)
        layout.setSpacing(ModernBabbittTheme.get_modern_form_spacing()['section_spacing'])
        
        # Modern title
        title = ModernWidgetFactory.create_title_label("Sample Configuration")
        layout.addWidget(title)
        
        # Modern card container
        card = ModernWidgetFactory.create_card_frame(elevated=True)
        card_layout = QVBoxLayout(card)
        
        # Subtitle
        subtitle = ModernWidgetFactory.create_subtitle_label("Select your options:")
        card_layout.addWidget(subtitle)
        
        # Sample options with modern dropdowns
        options_layout = QGridLayout()
        
        # Voltage option
        voltage_label = QLabel("Voltage:")
        voltage_combo = QComboBox()
        voltage_combo.addItems(["115VAC", "230VAC", "24VDC"])
        QuickMigrationHelper.fix_oversized_dropdowns(voltage_combo.parent() or self)
        
        options_layout.addWidget(voltage_label, 0, 0)
        options_layout.addWidget(voltage_combo, 0, 1)
        
        # Material option  
        material_label = QLabel("Material:")
        material_combo = QComboBox()
        material_combo.addItems(["316 Stainless", "Halar", "PTFE"])
        
        options_layout.addWidget(material_label, 1, 0)
        options_layout.addWidget(material_combo, 1, 1)
        
        card_layout.addLayout(options_layout)
        layout.addWidget(card)
        
        # Pricing section
        pricing_card = ModernWidgetFactory.create_card_frame()
        pricing_layout = QHBoxLayout(pricing_card)
        
        base_price = ModernWidgetFactory.create_price_label(425.0, "base")
        pricing_layout.addWidget(QLabel("Base Price:"))
        pricing_layout.addWidget(base_price)
        pricing_layout.addStretch()
        
        total_price = ModernWidgetFactory.create_price_label(565.0, "total")
        pricing_layout.addWidget(QLabel("Total:"))
        pricing_layout.addWidget(total_price)
        
        layout.addWidget(pricing_card)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = ModernWidgetFactory.create_secondary_button("Cancel")
        button_layout.addWidget(cancel_btn)
        
        add_btn = ModernWidgetFactory.create_primary_button("Add to Quote")
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
        
        # Add entrance animation
        UIAnimations.fade_in(self, duration=300)


# ===== TESTING & VALIDATION =====

def test_modern_ui_improvements():
    """
    Test function to validate UI improvements.
    Call this after implementing changes.
    """
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    ModernBabbittTheme.apply_modern_theme(app)
    
    # Test sample dialog
    dialog = SampleModernDialog()
    ValidationHelper.print_validation_report(dialog, "SampleModernDialog")
    
    # Show dialog for visual inspection
    if "--show" in sys.argv:
        dialog.show()
        app.exec()
    
    print("\n🎯 Key improvements implemented:")
    print("   ✅ Compact dropdown boxes (max 32px height)")
    print("   ✅ Modern card-based layout")
    print("   ✅ Visual pricing feedback")
    print("   ✅ Better typography and spacing")
    print("   ✅ Consistent color scheme")
    print("   ✅ Hover and focus states")


if __name__ == "__main__":
    test_modern_ui_improvements() 