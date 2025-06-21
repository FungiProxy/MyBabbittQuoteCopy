def __init__(self):
    super().__init__()
    # ... your existing code ...
    
    # Apply theme to dialog
    self.setStyleSheet(BabbittTheme.get_main_stylesheet())