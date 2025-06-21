"""
Configuration Dialog Usage Example
Shows how to apply the configuration dialog fixes to any dialog in your application.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton, QGroupBox
from src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper

class ExampleConfigurationDialog(QDialog):
    """Example dialog showing how to apply configuration fixes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Example Configuration Dialog")
        self.resize(600, 400)
        
        # Setup UI
        self._setup_ui()
        
        # 🔴 CRITICAL: Apply configuration dialog fixes
        # This fixes oversized dropdowns, spacing, and styling issues
        ConfigurationDialogHelper.apply_dialog_fixes(self)
    
    def _setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Example configuration section
        group = QGroupBox("Product Configuration")
        group_layout = QVBoxLayout(group)
        
        # Example dropdown (will be fixed by ConfigurationDialogHelper)
        label = QLabel("Select Option:")
        group_layout.addWidget(label)
        
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        group_layout.addWidget(combo)
        
        # Example button (will be styled by ConfigurationDialogHelper)
        button = QPushButton("Configure")
        group_layout.addWidget(button)
        
        layout.addWidget(group)
        
        # Add to Quote button (will be styled as primary)
        add_button = QPushButton("Add to Quote")
        layout.addWidget(add_button)


# ===== USAGE IN YOUR APPLICATION =====

def show_configuration_dialog():
    """Example function showing how to use the configuration dialog."""
    dialog = ExampleConfigurationDialog()
    
    # The dialog will automatically have:
    # ✅ Properly sized dropdowns (max 36px height, 280px width)
    # ✅ Consistent spacing (12px spacing, 16px margins)
    # ✅ Modern section styling with rounded corners
    # ✅ Proper button sizing (36-44px height)
    # ✅ Clean form field styling
    
    dialog.exec()


# ===== FOR EXISTING DIALOGS =====

def apply_fixes_to_existing_dialog(existing_dialog):
    """Apply fixes to an existing dialog instance."""
    ConfigurationDialogHelper.apply_dialog_fixes(existing_dialog)
    
    # The dialog will now have all the fixes applied:
    # - Fixed oversized dropdowns
    # - Improved spacing and layout
    # - Consistent section styling
    # - Fixed button styling
    # - Modern form styling


# ===== MAIN APPLICATION INTEGRATION =====

"""
In your main application (main.py), you already have:

# Apply Modern Babbitt theme to entire application
from src.ui.theme.modern_babbitt_theme import ModernBabbittTheme
ModernBabbittTheme.apply_to_application(app)

# Configuration dialog helper is imported and available
from src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper

Now any dialog you create can use:
ConfigurationDialogHelper.apply_dialog_fixes(your_dialog)
"""

if __name__ == "__main__":
    # Example usage
    show_configuration_dialog() 