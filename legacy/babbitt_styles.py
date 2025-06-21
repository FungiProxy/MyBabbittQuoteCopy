# styles/babbitt_styles.py
class BabbittStyles:
    """Centralized styling for quick, uniform appearance"""
    
    # Color scheme based on your current orange accent
    COLORS = {
        'primary_dark': '#2c3e50',      # Dark sidebar (similar to current)
        'primary': '#34495e',           # Lighter dark
        'accent': '#f39c12',            # Orange (keeping your current)
        'accent_hover': '#e67e22',      # Darker orange for hover
        'success': '#27ae60',           # Green for success
        'background': '#ffffff',        # White background
        'card_bg': '#f8f9fa',          # Light gray for cards
        'border': '#dee2e6',           # Border color
        'text_primary': '#2c3e50',     # Dark text
        'text_secondary': '#6c757d'    # Gray text
    }
    
    @staticmethod
    def get_main_window_style():
        """Main window styling"""
        return """
            QMainWindow {
                background-color: #ffffff;
            }
        """
    
    @staticmethod
    def get_sidebar_style():
        """Sidebar navigation styling"""
        return f"""
            QWidget#sidebar {{
                background-color: {BabbittStyles.COLORS['primary_dark']};
                min-width: 220px;
                max-width: 220px;
            }}
            QPushButton#sidebarButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton#sidebarButton:hover {{
                background-color: {BabbittStyles.COLORS['primary']};
                border-left: 4px solid {BabbittStyles.COLORS['accent']};
            }}
            QPushButton#sidebarButton:checked {{
                background-color: {BabbittStyles.COLORS['primary']};
                border-left: 4px solid {BabbittStyles.COLORS['accent']};
            }}
        """
    
    @staticmethod
    def get_card_style():
        """Card container styling"""
        return f"""
            QFrame#card {{
                background-color: {BabbittStyles.COLORS['card_bg']};
                border: 1px solid {BabbittStyles.COLORS['border']};
                border-radius: 8px;
                padding: 16px;
                margin: 8px;
            }}
        """
    
    @staticmethod
    def get_button_style():
        """Primary button styling"""
        return f"""
            QPushButton {{
                background-color: {BabbittStyles.COLORS['accent']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {BabbittStyles.COLORS['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: #d68910;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """
    
    @staticmethod
    def get_input_style():
        """Input field styling"""
        return f"""
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                border: 1px solid {BabbittStyles.COLORS['border']};
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 2px solid {BabbittStyles.COLORS['accent']};
                padding: 7px 11px;
            }}
            QTextEdit {{
                border: 1px solid {BabbittStyles.COLORS['border']};
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }}
        """
    
    @staticmethod
    def get_table_style():
        """Table widget styling"""
        return f"""
            QTableWidget {{
                border: 1px solid {BabbittStyles.COLORS['border']};
                gridline-color: {BabbittStyles.COLORS['border']};
                background-color: white;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: {BabbittStyles.COLORS['accent']};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {BabbittStyles.COLORS['card_bg']};
                padding: 8px;
                border: none;
                font-weight: 600;
            }}
        """