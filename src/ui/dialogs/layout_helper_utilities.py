"""
Layout Helper Utilities - Standard Layout Application
File: src/ui/utils/layout_helpers.py

🔴 Critical - Helper methods to apply uniform layouts to existing widgets
Easy-to-use utilities for fixing existing dialogs and forms
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QPushButton,
    QLabel, QGroupBox, QFrame, QSpinBox, QDoubleSpinBox, QCheckBox,
    QRadioButton, QListWidget, QTableWidget, QTabWidget, QScrollArea
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont


class LayoutStandardizer:
    """
    Utility class to apply standard layouts and sizing to existing widgets.
    Use these methods to quickly fix inconsistent layouts throughout your application.
    """
    
    # Standard measurements (matches theme)
    STANDARD_INPUT_HEIGHT = 36
    STANDARD_BUTTON_HEIGHT = 40
    SMALL_BUTTON_HEIGHT = 32
    LARGE_BUTTON_HEIGHT = 48
    
    STANDARD_SPACING = 12
    CARD_SPACING = 16
    FORM_SPACING = 12
    SECTION_SPACING = 20
    
    STANDARD_MARGINS = (20, 20, 20, 20)  # left, top, right, bottom
    CARD_MARGINS = (20, 20, 20, 20)
    FORM_MARGINS = (20, 20, 20, 20)
    
    @classmethod
    def fix_entire_widget(cls, widget):
        """
        Apply all standard fixes to a widget and its children.
        🔴 One-call solution for fixing any dialog or widget.
        """
        cls.fix_input_heights(widget)
        cls.fix_button_heights(widget)
        cls.fix_layout_spacing(widget)
        cls.fix_layout_margins(widget)
        cls.apply_consistent_styling(widget)
        cls.fix_combo_box_sizes(widget)
        cls.fix_group_box_styling(widget)
        
        print(f"✅ Applied standard layout fixes to {widget.__class__.__name__}")
    
    @classmethod
    def fix_input_heights(cls, widget):
        """Set standard height for all input widgets."""
        input_widgets = widget.findChildren((
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox
        ))
        
        for input_widget in input_widgets:
            input_widget.setMinimumHeight(cls.STANDARD_INPUT_HEIGHT)
            input_widget.setMaximumHeight(cls.STANDARD_INPUT_HEIGHT)
        
        # Text areas get different treatment
        text_widgets = widget.findChildren((QTextEdit, QPlainTextEdit))
        for text_widget in text_widgets:
            text_widget.setMinimumHeight(80)
            text_widget.setMaximumHeight(120)
    
    @classmethod
    def fix_button_heights(cls, widget):
        """Set standard height for all buttons."""
        buttons = widget.findChildren(QPushButton)
        
        for button in buttons:
            # Check if it's marked as small or large
            if button.property("size") == "small":
                button.setMinimumHeight(cls.SMALL_BUTTON_HEIGHT)
                button.setMaximumHeight(cls.SMALL_BUTTON_HEIGHT)
            elif button.property("size") == "large":
                button.setMinimumHeight(cls.LARGE_BUTTON_HEIGHT)
                button.setMaximumHeight(cls.LARGE_BUTTON_HEIGHT)
            else:
                button.setMinimumHeight(cls.STANDARD_BUTTON_HEIGHT)
                button.setMaximumHeight(cls.STANDARD_BUTTON_HEIGHT)
    
    @classmethod
    def fix_combo_box_sizes(cls, widget):
        """Fix oversized combo boxes (common issue)."""
        combo_boxes = widget.findChildren(QComboBox)
        
        for combo in combo_boxes:
            combo.setMinimumHeight(cls.STANDARD_INPUT_HEIGHT)
            combo.setMaximumHeight(cls.STANDARD_INPUT_HEIGHT)
            combo.setMaximumWidth(300)  # Prevent super-wide dropdowns
    
    @classmethod
    def fix_layout_spacing(cls, widget):
        """Apply standard spacing to all layouts."""
        # Fix VBox layouts
        vbox_layouts = widget.findChildren(QVBoxLayout)
        for layout in vbox_layouts:
            if layout.parent() == widget:  # Only immediate children
                layout.setSpacing(cls.STANDARD_SPACING)
        
        # Fix HBox layouts
        hbox_layouts = widget.findChildren(QHBoxLayout)
        for layout in hbox_layouts:
            if layout.parent() == widget:
                layout.setSpacing(cls.STANDARD_SPACING)
        
        # Fix Form layouts
        form_layouts = widget.findChildren(QFormLayout)
        for layout in form_layouts:
            layout.setSpacing(cls.FORM_SPACING)
            layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        # Fix Grid layouts
        grid_layouts = widget.findChildren(QGridLayout)
        for layout in grid_layouts:
            layout.setSpacing(cls.STANDARD_SPACING)
    
    @classmethod
    def fix_layout_margins(cls, widget):
        """Apply standard margins to all layouts."""
        # Main widget layouts
        if widget.layout():
            widget.layout().setContentsMargins(*cls.STANDARD_MARGINS)
        
        # Card and group box layouts
        group_boxes = widget.findChildren(QGroupBox)
        for group in group_boxes:
            if group.layout():
                group.layout().setContentsMargins(*cls.CARD_MARGINS)
        
        # Frame layouts
        frames = widget.findChildren(QFrame)
        for frame in frames:
            if frame.layout() and frame.property("frameType") == "card":
                frame.layout().setContentsMargins(*cls.CARD_MARGINS)
    
    @classmethod
    def apply_consistent_styling(cls, widget):
        """Apply consistent styling properties."""
        # Labels
        labels = widget.findChildren(QLabel)
        for label in labels:
            # Apply font settings
            font = label.font()
            font.setPointSize(9)  # Standard font size
            label.setFont(font)
        
        # CheckBoxes and RadioButtons
        check_boxes = widget.findChildren((QCheckBox, QRadioButton))
        for check_box in check_boxes:
            check_box.setMinimumHeight(24)
    
    @classmethod
    def fix_group_box_styling(cls, widget):
        """Apply consistent GroupBox styling."""
        group_boxes = widget.findChildren(QGroupBox)
        
        for group_box in group_boxes:
            # Apply standard group box styling
            group_box.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: 600;
                    font-size: 16px;
                    color: #0052cc;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 15px;
                    background-color: white;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 16px;
                    padding: 0 8px 0 8px;
                    background-color: white;
                }}
            """)


class FormLayoutHelper:
    """Helper specifically for form layouts and dialog organization."""
    
    @classmethod
    def create_standard_form_layout(cls, parent_widget):
        """Create a form layout with standard settings."""
        layout = QFormLayout(parent_widget)
        layout.setSpacing(LayoutStandardizer.FORM_SPACING)
        layout.setContentsMargins(*LayoutStandardizer.FORM_MARGINS)
        layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layout.setFormAlignment(Qt.AlignTop)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return layout
    
    @classmethod
    def add_form_section(cls, layout, title, widgets_dict):
        """
        Add a section to a form layout with a title.
        
        Args:
            layout: QFormLayout to add to
            title: Section title
            widgets_dict: Dict of {label: widget} pairs
        """
        # Add section title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #0052cc;
                margin-top: 16px;
                margin-bottom: 8px;
                padding-bottom: 4px;
                border-bottom: 1px solid #dee2e6;
            }
        """)
        layout.addRow(title_label)
        
        # Add widgets
        for label_text, widget in widgets_dict.items():
            # Ensure widget has standard height
            if hasattr(widget, 'setMinimumHeight'):
                widget.setMinimumHeight(LayoutStandardizer.STANDARD_INPUT_HEIGHT)
            if hasattr(widget, 'setMaximumHeight') and not isinstance(widget, (QTextEdit, QPlainTextEdit)):
                widget.setMaximumHeight(LayoutStandardizer.STANDARD_INPUT_HEIGHT)
            
            layout.addRow(label_text, widget)
    
    @classmethod
    def create_standard_button_row(cls, buttons_list, alignment=Qt.AlignRight):
        """
        Create a standardized button row.
        
        Args:
            buttons_list: List of QPushButton objects
            alignment: Qt alignment for the button row
        
        Returns:
            QHBoxLayout with properly spaced buttons
        """
        button_layout = QHBoxLayout()
        button_layout.setSpacing(LayoutStandardizer.STANDARD_SPACING)
        
        if alignment == Qt.AlignRight:
            button_layout.addStretch()
        
        for button in buttons_list:
            # Apply standard button height
            button.setMinimumHeight(LayoutStandardizer.STANDARD_BUTTON_HEIGHT)
            button.setMaximumHeight(LayoutStandardizer.STANDARD_BUTTON_HEIGHT)
            button.setMinimumWidth(100)  # Minimum button width
            button_layout.addWidget(button)
        
        if alignment == Qt.AlignLeft:
            button_layout.addStretch()
        
        return button_layout


class DialogFixHelper:
    """Helper specifically for fixing dialog layout issues."""
    
    @classmethod
    def fix_dialog_proportions(cls, dialog):
        """Fix common dialog proportion issues."""
        # Set reasonable size constraints
        dialog.setMinimumSize(600, 400)
        dialog.setMaximumSize(1400, 1000)
        
        # Apply standard layout fixes
        LayoutStandardizer.fix_entire_widget(dialog)
        
        # Center the dialog
        if dialog.parent():
            parent_geo = dialog.parent().geometry()
            dialog_geo = dialog.geometry()
            x = parent_geo.x() + (parent_geo.width() - dialog_geo.width()) // 2
            y = parent_geo.y() + (parent_geo.height() - dialog_geo.height()) // 2
            dialog.move(max(0, x), max(0, y))
    
    @classmethod
    def create_dialog_header(cls, title, subtitle=None):
        """Create a standardized dialog header."""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 16)
        header_layout.setSpacing(4)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #2c3e50;
                margin: 0;
                padding: 0;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Subtitle (optional)
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #6c757d;
                    margin: 0;
                    padding: 0;
                }
            """)
            header_layout.addWidget(subtitle_label)
        
        return header_widget
    
    @classmethod
    def add_dialog_separator(cls):
        """Create a visual separator for dialogs."""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("""
            QFrame {
                color: #dee2e6;
                margin: 16px 0;
            }
        """)
        return separator


class QuickFixApplicator:
    """One-call solutions for common layout problems."""
    
    @classmethod
    def fix_product_configuration_dialog(cls, dialog):
        """
        🔴 Specific fix for product configuration dialogs.
        Addresses the oversized dropdowns and spacing issues visible in screenshots.
        """
        # Apply all standard fixes
        LayoutStandardizer.fix_entire_widget(dialog)
        
        # Specific fixes for configuration dialogs
        cls._fix_configuration_specific_issues(dialog)
        
        # Set reasonable dialog size
        dialog.resize(1000, 700)
        dialog.setMinimumSize(800, 600)
        
        print("✅ Applied product configuration dialog fixes")
    
    @classmethod
    def fix_settings_page(cls, widget):
        """🔴 Specific fix for settings pages."""
        LayoutStandardizer.fix_entire_widget(widget)
        
        # Settings-specific fixes
        tab_widgets = widget.findChildren(QTabWidget)
        for tab_widget in tab_widgets:
            tab_widget.setMinimumHeight(400)
        
        print("✅ Applied settings page fixes")
    
    @classmethod
    def fix_quote_creation_page(cls, widget):
        """🔴 Specific fix for quote creation pages."""
        LayoutStandardizer.fix_entire_widget(widget)
        
        # Quote creation specific fixes
        list_widgets = widget.findChildren(QListWidget)
        for list_widget in list_widgets:
            list_widget.setMinimumHeight(200)
        
        table_widgets = widget.findChildren(QTableWidget)
        for table_widget in table_widgets:
            table_widget.setMinimumHeight(300)
        
        print("✅ Applied quote creation page fixes")
    
    @classmethod
    def _fix_configuration_specific_issues(cls, dialog):
        """Fix issues specific to configuration dialogs."""
        # Fix price labels to be more prominent
        price_labels = dialog.findChildren(QLabel)
        for label in price_labels:
            if "total" in label.objectName().lower() or "$" in label.text():
                label.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                        font-weight: 600;
                        color: #0052cc;
                        padding: 8px;
                        background-color: white;
                        border: 1px solid #dee2e6;
                        border-radius: 6px;
                    }
                """)
        
        # Ensure quantity spinners are reasonable size
        spin_boxes = dialog.findChildren((QSpinBox, QDoubleSpinBox))
        for spin_box in spin_boxes:
            spin_box.setMaximumWidth(120)


# ============================================================================
# EASY IMPLEMENTATION EXAMPLES
# ============================================================================

class EasyApplicationExamples:
    """Examples showing how to easily apply these fixes to your existing code."""
    
    @staticmethod
    def example_dialog_init_fix():
        """
        Example: Add this to any dialog's __init__ method.
        """
        return """
        # At the end of your dialog's __init__ method, add:
        from src.ui.utils.layout_helpers import LayoutStandardizer
        LayoutStandardizer.fix_entire_widget(self)
        """
    
    @staticmethod
    def example_product_config_fix():
        """
        Example: Fix product configuration dialog.
        """
        return """
        # In your ProductSelectionDialog.__init__ method:
        from src.ui.utils.layout_helpers import QuickFixApplicator
        QuickFixApplicator.fix_product_configuration_dialog(self)
        """
    
    @staticmethod
    def example_form_creation():
        """
        Example: Create a new form with standard layout.
        """
        return """
        # When creating new forms:
        from src.ui.utils.layout_helpers import FormLayoutHelper
        
        form_layout = FormLayoutHelper.create_standard_form_layout(self)
        
        # Add sections
        FormLayoutHelper.add_form_section(form_layout, "Basic Information", {
            "Name:": name_edit,
            "Email:": email_edit,
            "Phone:": phone_edit
        })
        
        # Add button row
        buttons = [cancel_btn, save_btn]
        button_layout = FormLayoutHelper.create_standard_button_row(buttons)
        """


# ============================================================================
# INTEGRATION INSTRUCTIONS
# ============================================================================

"""
🔴 IMPLEMENTATION STEPS (Easy integration):

1. Save this file as src/ui/utils/layout_helpers.py

2. Apply to existing dialogs (one line each):
   
   # In any dialog's __init__, after UI setup:
   from src.ui.utils.layout_helpers import LayoutStandardizer
   LayoutStandardizer.fix_entire_widget(self)

3. Specific dialog fixes:
   
   # Product configuration dialog:
   from src.ui.utils.layout_helpers import QuickFixApplicator
   QuickFixApplicator.fix_product_configuration_dialog(self)
   
   # Settings page:
   QuickFixApplicator.fix_settings_page(self)
   
   # Quote creation page:
   QuickFixApplicator.fix_quote_creation_page(self)

4. For new forms, use the FormLayoutHelper:
   
   from src.ui.utils.layout_helpers import FormLayoutHelper
   layout = FormLayoutHelper.create_standard_form_layout(self)

✅ BENEFITS:
- One-call fixes for entire widgets
- Uniform 36px input heights
- Consistent 40px button heights  
- Proper spacing (12px form, 20px sections)
- Standard 20px margins on containers
- Fixes oversized dropdown issues
- Professional GroupBox styling
- Easy application to existing code

✅ USAGE PATTERNS:
- LayoutStandardizer.fix_entire_widget(self) - Fix everything
- QuickFixApplicator.fix_product_configuration_dialog(self) - Specific fixes
- FormLayoutHelper.create_standard_form_layout(parent) - New forms
- DialogFixHelper.fix_dialog_proportions(dialog) - Dialog sizing

Just add one line to any existing dialog to apply all the fixes!
"""