# File: src/ui/components/configuration_wizard.py
# Update the _create_progress_indicator method

def _create_progress_indicator(self) -> QWidget:
    """Create progress indicator showing configuration completion."""
    widget = QFrame()
    widget.setObjectName('progressIndicator')
    widget.setFixedHeight(100)  # Fixed height for consistency
    
    # Main container with proper centering
    container = QWidget()
    main_layout = QVBoxLayout(widget)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.addWidget(container)
    
    # Horizontal layout for steps - this is the key fix
    layout = QHBoxLayout(container)
    layout.setContentsMargins(40, 20, 40, 20)  # Proper margins
    layout.setSpacing(0)  # No spacing - we control with stretch
    
    steps = [
        ('✓', 'Select', True, True),    # (number, label, is_complete, is_active)
        ('2', 'Configure', False, True),
        ('3', 'Quote', False, False)
    ]
    
    # Add leading stretch to center the group
    layout.addStretch(1)
    
    for i, (number, label, is_complete, is_active) in enumerate(steps):
        if i > 0:
            # Connector line with proper spacing
            layout.addSpacing(20)  # Space before line
            line = QFrame()
            line.setObjectName('progressLine')
            line.setFixedSize(60, 2)  # Longer, more proportional line
            layout.addWidget(line)
            layout.addSpacing(20)  # Space after line
        
        # Step widget
        step_widget = QWidget()
        step_widget.setFixedSize(80, 60)  # Fixed size for predictable layout
        step_layout = QVBoxLayout(step_widget)
        step_layout.setContentsMargins(0, 0, 0, 0)
        step_layout.setSpacing(8)
        step_layout.setAlignment(Qt.AlignCenter)
        
        # Circle
        circle = QLabel(number)
        circle.setFixedSize(36, 36)  # Slightly larger for better proportion
        circle.setAlignment(Qt.AlignCenter)
        circle.setProperty('class', 'stepNumber')
        circle.setProperty('completed', is_complete)
        circle.setProperty('active', is_active)
        
        # Label
        step_label = QLabel(label)
        step_label.setProperty('class', 'stepLabel')
        step_label.setAlignment(Qt.AlignCenter)
        step_label.setFixedHeight(16)  # Consistent label height
        
        step_layout.addWidget(circle)
        step_layout.addWidget(step_label)
        
        layout.addWidget(step_widget)
    
    # Add trailing stretch to center the group
    layout.addStretch(1)
    
    return widget