# File: src/ui/components/configuration_wizard.py
# Add these methods to improve form proportions

def _create_config_section(self, title: str, widgets: List[QWidget]) -> QFrame:
    """Create a properly sized configuration section."""
    section = QFrame()
    section.setObjectName('configSection')
    section.setStyleSheet("""
        #configSection {
            background-color: white;
            border: 1px solid #E9ECEF;
            border-radius: 8px;
            margin-bottom: 16px;
        }
    """)
    
    layout = QVBoxLayout(section)
    layout.setContentsMargins(20, 16, 20, 20)
    layout.setSpacing(12)
    
    # Section title
    title_label = QLabel(title)
    title_label.setStyleSheet("""
        QLabel {
            font-size: 16px;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 8px;
        }
    """)
    layout.addWidget(title_label)
    
    # Add widgets with proper spacing
    for widget in widgets:
        if hasattr(widget, 'setFixedHeight'):
            widget.setFixedHeight(40)  # Consistent input height
        layout.addWidget(widget)
    
    return section

def _create_form_input(self, label_text: str, widget_type: str = 'line_edit', **kwargs) -> tuple:
    """Create properly sized form inputs."""
    # Label
    label = QLabel(label_text)
    label.setStyleSheet("""
        QLabel {
            font-size: 14px;
            font-weight: 500;
            color: #495057;
            margin-bottom: 4px;
        }
    """)
    
    # Input widget
    if widget_type == 'line_edit':
        from PySide6.QtWidgets import QLineEdit
        widget = QLineEdit()
        widget.setFixedHeight(40)
        widget.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #CED4DA;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4285F4;
                outline: none;
            }
        """)
    elif widget_type == 'combo_box':
        from PySide6.QtWidgets import QComboBox
        widget = QComboBox()
        widget.setFixedHeight(40)
        widget.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #CED4DA;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                min-width: 200px;
            }
            QComboBox:focus {
                border-color: #4285F4;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6C757D;
            }
        """)
    
    return label, widget

def _improve_dialog_proportions(self):
    """Improve overall dialog proportions - call this in __init__."""
    # Set better default size
    screen = self.screen().availableGeometry()
    width = min(1200, int(screen.width() * 0.8))
    height = min(800, int(screen.height() * 0.8))
    self.resize(width, height)
    
    # Center on screen
    self.move(
        (screen.width() - width) // 2,
        (screen.height() - height) // 2
    )