"""
Configuration Dialog UI Fixes
File: src/ui/components/configuration_dialog_helper.py

🔴 Critical - Add this to fix the configuration dialog formatting issues
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QGroupBox, QFrame, QSpacerItem,
                               QSizePolicy, QPushButton)
from PySide6.QtCore import Qt


class ConfigurationDialogHelper:
    """Helper class to apply consistent formatting to configuration dialogs."""
    
    @staticmethod
    def apply_dialog_fixes(dialog_widget):
        """
        Apply comprehensive fixes to configuration dialogs.
        
        🔴 Critical - Call this in your dialog's __init__ after setupUi()
        """
        # Fix oversized dropdowns
        ConfigurationDialogHelper._fix_oversized_dropdowns(dialog_widget)
        
        # Fix spacing and layout issues  
        ConfigurationDialogHelper._fix_spacing_issues(dialog_widget)
        
        # Apply consistent section styling
        ConfigurationDialogHelper._fix_section_styling(dialog_widget)
        
        # Fix button styling
        ConfigurationDialogHelper._fix_button_styling(dialog_widget)
        
        # Apply modern form styling
        ConfigurationDialogHelper._apply_modern_form_styling(dialog_widget)
    
    @staticmethod
    def _fix_oversized_dropdowns(widget):
        """Fix the oversized dropdown issue visible in screenshots."""
        for combo in widget.findChildren(QComboBox):
            # Set reasonable size constraints
            combo.setMaximumHeight(36)
            combo.setMinimumHeight(32)
            combo.setMaximumWidth(280)  # Prevent super wide dropdowns
            
            # Apply size policy
            combo.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    
    @staticmethod
    def _fix_spacing_issues(widget):
        """Fix spacing and margin issues."""
        # Find all layouts and apply consistent spacing
        for layout in widget.findChildren(QVBoxLayout):
            layout.setSpacing(12)
            layout.setContentsMargins(16, 16, 16, 16)
        
        for layout in widget.findChildren(QHBoxLayout):
            layout.setSpacing(12)
            layout.setContentsMargins(0, 0, 0, 0)
    
    @staticmethod
    def _fix_section_styling(widget):
        """Apply consistent styling to configuration sections."""
        # Style group boxes consistently
        for group_box in widget.findChildren(QGroupBox):
            group_box.setStyleSheet("""
                QGroupBox {
                    font-weight: 600;
                    font-size: 16px;
                    color: #1976d2;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    margin-top: 8px;
                    padding-top: 16px;
                    background-color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 8px;
                    margin-top: -8px;
                    background-color: #ffffff;
                }
            """)
    
    @staticmethod
    def _fix_button_styling(widget):
        """Apply consistent button styling."""
        for button in widget.findChildren(QPushButton):
            if "Add" in button.text() or "Configure" in button.text():
                button.setProperty("class", "primary")
            elif "Cancel" in button.text():
                button.setProperty("class", "secondary") 
            
            # Apply consistent sizing
            button.setMinimumHeight(36)
            button.setMaximumHeight(44)
    
    @staticmethod
    def _apply_modern_form_styling(widget):
        """Apply modern form field styling."""
        # Style all labels consistently
        for label in widget.findChildren(QLabel):
            label_text = label.text()
            
            # Section titles
            if any(word in label_text for word in ["Configuration", "Options", "Accessories"]):
                label.setProperty("class", "section-header")
                label.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                        font-weight: 600;
                        color: #1976d2;
                        margin: 16px 0 8px 0;
                        padding-bottom: 4px;
                        border-bottom: 2px solid #e0e0e0;
                    }
                """)
            
            # Field labels
            elif label_text.endswith(":") or label_text.endswith("*"):
                label.setProperty("class", "field-label")
                label.setStyleSheet("""
                    QLabel {
                        font-weight: 500;
                        color: #212121;
                        margin-bottom: 4px;
                        font-size: 14px;
                    }
                """)


class ConfigurationProgressIndicator:
    """Helper to create consistent progress indicators."""
    
    @staticmethod
    def create_step_indicator(steps, current_step=0):
        """
        Create a modern step indicator widget.
        
        Args:
            steps: List of step names
            current_step: Current active step index
        """
        container = QFrame()
        container.setObjectName("progressIndicator")
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 20, 24, 20)
        
        for i, step_name in enumerate(steps):
            # Step container
            step_container = QVBoxLayout()
            step_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_container.setSpacing(8)
            
            # Step number circle
            step_number = QLabel(str(i + 1))
            step_number.setObjectName("stepNumber") 
            step_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_number.setFixedSize(32, 32)
            
            # Set step state
            if i < current_step:
                step_number.setProperty("completed", "true")
            elif i == current_step:
                step_number.setProperty("active", "true")
            
            # Step label
            step_label = QLabel(step_name)
            step_label.setObjectName("stepLabel")
            step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            if i == current_step:
                step_label.setProperty("active", "true")
            
            step_container.addWidget(step_number)
            step_container.addWidget(step_label)
            
            # Create widget for the step
            step_widget = QWidget()
            step_widget.setLayout(step_container)
            layout.addWidget(step_widget)
            
            # Add connector line (except for last step)
            if i < len(steps) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setObjectName("progressLine")
                line.setStyleSheet("""
                    QFrame#progressLine {
                        background-color: #e0e0e0;
                        border: none;
                        height: 2px;
                        margin: 15px 0;
                    }
                """)
                layout.addWidget(line)
        
        return container


class ConfigurationSummaryPanel:
    """Helper to create consistent quote summary panels."""
    
    @staticmethod
    def create_summary_panel():
        """Create a modern quote summary panel."""
        panel = QFrame()
        panel.setObjectName("quoteSummaryPanel")
        panel.setMaximumWidth(300)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Quote Summary")
        title.setObjectName("quoteSummaryTitle")
        layout.addWidget(title)
        
        # Add spacer to push total to bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        
        # Total
        total_frame = QFrame()
        total_layout = QVBoxLayout(total_frame)
        total_layout.setSpacing(4)
        
        total_label = QLabel("Total:")
        total_label.setStyleSheet("font-size: 14px; color: #616161;")
        
        total_amount = QLabel("$0.00")
        total_amount.setObjectName("quoteTotal")
        
        total_layout.addWidget(total_label)
        total_layout.addWidget(total_amount)
        layout.addWidget(total_frame)
        
        # Add to Quote button
        add_button = QPushButton("Add to Quote")
        add_button.setObjectName("addToQuoteButton")
        add_button.setProperty("class", "success")
        layout.addWidget(add_button)
        
        return panel


# ===== USAGE EXAMPLE =====

def fix_configuration_dialog_example(dialog):
    """
    Example of how to apply all fixes to a configuration dialog.
    
    Add this call to your dialog's __init__ method after setupUi():
    """
    # Apply all dialog fixes
    ConfigurationDialogHelper.apply_dialog_fixes(dialog)
    
    # Apply theme
    from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
    ModernBabbittTheme.apply_to_widget(dialog)
    
    # Force style refresh
    dialog.style().unpolish(dialog)
    dialog.style().polish(dialog)