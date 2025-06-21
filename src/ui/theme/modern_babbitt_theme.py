"""
Modern UI Styles and Improved Theme System
File: src/ui/theme/modern_babbitt_theme.py

🟢 10 min implementation - Enhanced styling for better UX
"""

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont


class ModernBabbittTheme(QObject):
    """
    Enhanced theme system with modern UI components and better visual hierarchy.
    Focuses on industrial professionalism with improved usability.
    This theme is standardized to the layout of BabbittProfessionalTheme.
    """
    
    # Modern Color Palette - Professional Industrial
    PRIMARY_BLUE = "#2C3E50"      # Deep professional blue  
    SECONDARY_BLUE = "#34495E"    # Medium blue for hover states
    LIGHT_BLUE = "#E3F2FD"       # Light blue for highlights
    ACCENT_GOLD = "#F39C12"       # Gold accent for important elements
    
    # Status Colors - Clear and accessible
    SUCCESS_GREEN = "#28A745"     # Success states, valid configs
    WARNING_ORANGE = "#FF9800"    # Warnings, needs attention  
    ERROR_RED = "#DC3545"         # Errors, invalid states
    INFO_BLUE = "#17A2B8"         # Information, help text
    
    # Neutral Palette - Modern grays
    WHITE = "#FFFFFF"             # Pure white backgrounds
    LIGHT_GRAY = "#F8F9FA"        # Secondary backgrounds
    MEDIUM_GRAY = "#6C757D"       # Secondary text, disabled
    DARK_GRAY = "#343A40"         # Primary text
    BORDER_GRAY = "#E9ECEF"       # Borders and dividers
    CARD_BORDER = "#E0E4E7"       # Card borders
    
    @staticmethod
    def get_application_stylesheet():
        """Get the main application stylesheet, standardized to BabbittProfessionalTheme."""
        return f"""
        /* Main Window and Global Styles */
        QMainWindow {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            color: {ModernBabbittTheme.DARK_GRAY};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}

        /* Sidebar Styling */
        QFrame#sidebarFrame {{
            background-color: {ModernBabbittTheme.PRIMARY_BLUE};
            border: none;
            min-width: 240px;
            max-width: 240px;
        }}

        QLabel#logoLabel {{
            color: {ModernBabbittTheme.ACCENT_GOLD};
            font-size: 24px;
            font-weight: 600;
            padding: 20px 10px;
            background-color: transparent;
        }}

        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: white;
            font-size: 14px;
            outline: none;
        }}

        QListWidget#navList::item {{
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }}

        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        QListWidget#navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-left: 3px solid {ModernBabbittTheme.ACCENT_GOLD};
            font-weight: 500;
        }}

        QPushButton#settingsButton {{
            background-color: transparent;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 10px 20px;
            margin: 10px;
            border-radius: 4px;
            font-size: 14px;
        }}

        QPushButton#settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        /* Content Area */
        QFrame#contentAreaFrame {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            border: none;
        }}

        QFrame#contentHeader {{
            background-color: {ModernBabbittTheme.WHITE};
            border-bottom: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            padding: 20px;
            min-height: 60px;
        }}

        QLabel#pageTitle {{
            font-size: 24px;
            font-weight: 600;
            color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}

        /* Button Styles */
        QPushButton {{
            border: none;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: 500;
            font-size: 14px;
            min-height: 20px;
        }}

        QPushButton.primary {{
            background-color: {ModernBabbittTheme.ACCENT_GOLD};
            color: white;
        }}

        QPushButton.primary:hover {{
            background-color: {ModernBabbittTheme.SECONDARY_BLUE};
        }}

        QPushButton.primary:pressed {{
            background-color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}

        QPushButton.success {{
            background-color: {ModernBabbittTheme.SUCCESS_GREEN};
            color: white;
        }}

        QPushButton.success:hover {{
            background-color: #2F855A; /* Darker green */
        }}

        QPushButton.secondary {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            color: {ModernBabbittTheme.DARK_GRAY};
        }}

        QPushButton.secondary:hover {{
            background-color: {ModernBabbittTheme.BORDER_GRAY};
        }}

        QPushButton.warning {{
            background-color: {ModernBabbittTheme.WARNING_ORANGE};
            color: white;
        }}

        QPushButton.warning:hover {{
            background-color: #DD6B20; /* Darker orange */
        }}

        QPushButton:disabled {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            color: {ModernBabbittTheme.MEDIUM_GRAY};
        }}

        /* Card Components */
        QFrame.card {{
            background-color: {ModernBabbittTheme.WHITE};
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 8px;
            padding: 20px;
        }}

        QFrame.card:hover {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
            background-color: {ModernBabbittTheme.LIGHT_BLUE};
        }}

        QFrame.productCard {{
            background-color: {ModernBabbittTheme.WHITE};
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 8px;
            padding: 20px;
            margin: 5px;
        }}

        QFrame.productCard:hover {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        /* Form Elements */
        QLineEdit {{
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 4px;
            padding: 8px 12px;
            background-color: {ModernBabbittTheme.WHITE};
            color: {ModernBabbittTheme.DARK_GRAY};
            font-size: 14px;
        }}

        QLineEdit:focus {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
            outline: none;
        }}

        QTextEdit {{
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 4px;
            padding: 8px 12px;
            background-color: {ModernBabbittTheme.WHITE};
            color: {ModernBabbittTheme.DARK_GRAY};
            font-size: 14px;
        }}

        QTextEdit:focus {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
            outline: none;
        }}

        /* Table Styles */
        QTableWidget {{
            background-color: {ModernBabbittTheme.WHITE};
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 4px;
            gridline-color: {ModernBabbittTheme.BORDER_GRAY};
        }}

        QTableWidget::item {{
            padding: 8px;
            border: none;
        }}

        QTableWidget::item:selected {{
            background-color: {ModernBabbittTheme.LIGHT_BLUE};
            color: {ModernBabbittTheme.DARK_GRAY};
        }}

        QHeaderView::section {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            color: {ModernBabbittTheme.DARK_GRAY};
            padding: 8px;
            border: none;
            border-bottom: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            font-weight: 600;
        }}

        /* Group Box */
        QGroupBox {{
            font-weight: 600;
            color: {ModernBabbittTheme.DARK_GRAY};
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 10px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: {ModernBabbittTheme.WHITE};
        }}

        /* Scroll Areas */
        QScrollArea {{
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 4px;
            background-color: {ModernBabbittTheme.WHITE};
        }}

        QScrollBar:vertical {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {ModernBabbittTheme.MEDIUM_GRAY};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {ModernBabbittTheme.DARK_GRAY};
        }}

        /* Status Labels */
        QLabel.status-draft {{
            color: {ModernBabbittTheme.MEDIUM_GRAY};
            font-style: italic;
        }}

        QLabel.status-active {{
            color: {ModernBabbittTheme.SUCCESS_GREEN};
            font-weight: 600;
        }}

        QLabel.status-pending {{
            color: {ModernBabbittTheme.WARNING_ORANGE};
            font-weight: 600;
        }}

        /* Progress Indicator */
        QFrame#progressIndicator {{
            background-color: {ModernBabbittTheme.WHITE};
            border-bottom: 1px solid {ModernBabbittTheme.BORDER_GRAY};
        }}

        QLabel.stepNumber {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            color: {ModernBabbittTheme.MEDIUM_GRAY};
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 15px;
            font-weight: 600;
        }}

        QLabel.stepNumber[active="true"] {{
            background-color: {ModernBabbittTheme.ACCENT_GOLD};
            color: white;
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
        }}

        QLabel.stepLabel {{
            color: {ModernBabbittTheme.MEDIUM_GRAY};
            font-size: 12px;
            font-weight: 500;
        }}

        QLabel.stepLabel[active="true"] {{
            color: {ModernBabbittTheme.ACCENT_GOLD};
            font-weight: 600;
        }}

        /* Product Selection Dialog Specific */
        QFrame#familiesPanel {{
            background-color: {ModernBabbittTheme.WHITE};
            border-right: 1px solid {ModernBabbittTheme.BORDER_GRAY};
        }}

        QFrame#productsPanel {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
        }}

        QLabel#sectionTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernBabbittTheme.PRIMARY_BLUE};
            margin-bottom: 10px;
        }}

        QLabel.placeholderCard {{
            color: {ModernBabbittTheme.MEDIUM_GRAY};
            font-style: italic;
            padding: 40px;
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            border: 2px dashed {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 8px;
        }}

        QLabel#quoteTotalLabel {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernBabbittTheme.ACCENT_GOLD};
        }}

        QLabel.quoteSubtitle {{
            color: {ModernBabbittTheme.MEDIUM_GRAY};
            font-size: 12px;
        }}

        /* Configuration Dialog Styles */
        QFrame.configPanel {{
            background-color: {ModernBabbittTheme.WHITE};
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 8px;
            padding: 20px;
        }}

        QFrame.summaryPanel {{
            background-color: {ModernBabbittTheme.LIGHT_BLUE};
            border: 1px solid {ModernBabbittTheme.ACCENT_GOLD};
            border-radius: 8px;
            padding: 20px;
        }}

        /* Radio Buttons and Checkboxes */
        QRadioButton {{
            spacing: 8px;
            color: {ModernBabbittTheme.DARK_GRAY};
        }}

        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            background-color: {ModernBabbittTheme.WHITE};
        }}

        QRadioButton::indicator:checked {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
            background-color: {ModernBabbittTheme.ACCENT_GOLD};
        }}

        QCheckBox {{
            spacing: 8px;
            color: {ModernBabbittTheme.DARK_GRAY};
        }}

        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 3px;
            background-color: {ModernBabbittTheme.WHITE};
        }}

        QCheckBox::indicator:checked {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
            background-color: {ModernBabbittTheme.ACCENT_GOLD};
        }}

        /* Spin Box */
        QSpinBox {{
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 4px;
            padding: 6px 8px;
            background-color: {ModernBabbittTheme.WHITE};
            color: {ModernBabbittTheme.DARK_GRAY};
        }}

        QSpinBox:focus {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
        }}

        /* Combo Box */
        QComboBox {{
            border: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 4px;
            padding: 6px 8px;
            background-color: {ModernBabbittTheme.WHITE};
            color: {ModernBabbittTheme.DARK_GRAY};
            min-width: 100px;
        }}

        QComboBox:focus {{
            border-color: {ModernBabbittTheme.ACCENT_GOLD};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {ModernBabbittTheme.MEDIUM_GRAY};
        }}

        QComboBox::down-arrow:hover {{
            border-top-color: {ModernBabbittTheme.DARK_GRAY};
        }}

        /* Dialog Specific */
        QDialog {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
        }}

        /* Button Sizes */
        QPushButton.small {{
            padding: 6px 12px;
            font-size: 12px;
            min-height: 16px;
        }}

        QPushButton.info {{
            background-color: {ModernBabbittTheme.INFO_BLUE};
            color: white;
        }}

        QPushButton.info:hover {{
            background-color: #138496;
        }}

        QPushButton.danger {{
            background-color: {ModernBabbittTheme.ERROR_RED};
            color: white;
        }}

        QPushButton.danger:hover {{
            background-color: #C82333;
        }}
        """

    @staticmethod
    def get_main_stylesheet():
        """Get the main stylesheet - alias for get_application_stylesheet for compatibility."""
        return ModernBabbittTheme.get_application_stylesheet()

    @staticmethod
    def apply_modern_theme(app: QApplication):
        """Apply the modern theme to the entire application."""
        app.setStyleSheet(ModernBabbittTheme.get_application_stylesheet())
        
        # Set application font
        font = QFont("Segoe UI", 10)
        font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
        app.setFont(font)
    
    @staticmethod 
    def get_pricing_style(price_value: float) -> str:
        """Get appropriate style for pricing based on value."""
        if price_value > 0:
            return f"""
                background-color: {ModernBabbittTheme.SUCCESS_GREEN};
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-weight: 600;
                font-size: 11px;
            """
        elif price_value < 0:
            return f"""
                background-color: {ModernBabbittTheme.ERROR_RED};
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-weight: 600;
                font-size: 11px;
            """
        else:
            return f"""
                background-color: {ModernBabbittTheme.MEDIUM_GRAY};
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-weight: 400;
                font-size: 11px;
            """
    
    @staticmethod
    def get_card_style(elevated: bool = False) -> str:
        """Get card styling with optional elevation."""
        base_style = f"""
            background-color: white;
            border: 1px solid {ModernBabbittTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 16px;
        """
        
        if elevated:
            base_style += ""
        
        return base_style
    
    @staticmethod
    def get_modern_form_spacing() -> dict:
        """Get recommended spacing values for modern forms."""
        return {
            'section_spacing': 24,
            'group_spacing': 16, 
            'field_spacing': 12,
            'element_spacing': 8,
            'tight_spacing': 4
        } 