"""
Modern UI Styles and Improved Theme System
File: src/ui/theme/modern_babbitt_theme.py

🟢 10 min implementation - Enhanced styling for better UX
"""

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QPalette, QColor


class ModernBabbittTheme(QObject):
    """
    Enhanced theme system with modern UI components and better visual hierarchy.
    Focuses on industrial professionalism with improved usability.
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
    
    # Interactive States
    HOVER_OVERLAY = "rgba(44, 62, 80, 0.1)"
    ACTIVE_OVERLAY = "rgba(44, 62, 80, 0.2)"
    FOCUS_SHADOW = "0 0 0 3px rgba(44, 62, 80, 0.25)"
    
    @staticmethod
    def get_application_stylesheet():
        """Get complete application stylesheet with modern components."""
        return f"""
        /* === GLOBAL APPLICATION STYLES === */
        QApplication {{
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: 14px;
            color: {ModernBabbittTheme.DARK_GRAY};
        }}
        
        /* === DIALOG AND WINDOW STYLES === */
        QDialog {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            border-radius: 12px;
        }}
        
        QMainWindow {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
        }}
        
        /* === MODERN BUTTON STYLES === */
        QPushButton {{
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            background-color: {ModernBabbittTheme.PRIMARY_BLUE};
            color: white;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background-color: {ModernBabbittTheme.SECONDARY_BLUE};
            transform: translateY(-1px);
        }}
        
        QPushButton:pressed {{
            background-color: {ModernBabbittTheme.PRIMARY_BLUE};
            transform: translateY(0px);
        }}
        
        QPushButton:disabled {{
            background-color: {ModernBabbittTheme.MEDIUM_GRAY};
            color: {ModernBabbittTheme.LIGHT_GRAY};
        }}
        
        /* Secondary Button Style */
        QPushButton[buttonStyle="secondary"] {{
            background-color: white;
            color: {ModernBabbittTheme.PRIMARY_BLUE};
            border: 2px solid {ModernBabbittTheme.PRIMARY_BLUE};
        }}
        
        QPushButton[buttonStyle="secondary"]:hover {{
            background-color: {ModernBabbittTheme.LIGHT_BLUE};
        }}
        
        /* === ENHANCED FORM CONTROLS === */
        QLineEdit {{
            padding: 10px 12px;
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 6px;
            background-color: white;
            font-size: 14px;
            selection-background-color: {ModernBabbittTheme.LIGHT_BLUE};
        }}
        
        QLineEdit:focus {{
            border-color: {ModernBabbittTheme.PRIMARY_BLUE};
            outline: none;
        }}
        
        QLineEdit:disabled {{
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            color: {ModernBabbittTheme.MEDIUM_GRAY};
        }}
        
        /* === MODERN COMBOBOX STYLES === */
        QComboBox {{
            padding: 8px 12px;
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 6px;
            background-color: white;
            font-size: 14px;
            min-height: 20px;
            selection-background-color: {ModernBabbittTheme.LIGHT_BLUE};
        }}
        
        QComboBox:hover {{
            border-color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}
        
        QComboBox:focus {{
            border-color: {ModernBabbittTheme.PRIMARY_BLUE};
            outline: none;
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {ModernBabbittTheme.MEDIUM_GRAY};
            margin-right: 5px;
        }}
        
        QComboBox QAbstractItemView {{
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 6px;
            background-color: white;
            selection-background-color: {ModernBabbittTheme.LIGHT_BLUE};
            padding: 4px;
            outline: none;
        }}
        
        /* === SPINBOX STYLES === */
        QSpinBox {{
            padding: 8px 12px;
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 6px;
            background-color: white;
            font-size: 14px;
            font-weight: 600;
        }}
        
        QSpinBox:focus {{
            border-color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}
        
        QSpinBox::up-button, QSpinBox::down-button {{
            width: 20px;
            border: none;
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
        }}
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background-color: {ModernBabbittTheme.BORDER_GRAY};
        }}
        
        /* === MODERN GROUP BOX STYLES === */
        QGroupBox {{
            font-weight: 600;
            font-size: 15px;
            color: {ModernBabbittTheme.PRIMARY_BLUE};
            border: 2px solid {ModernBabbittTheme.CARD_BORDER};
            border-radius: 10px;
            margin-top: 14px;
            padding-top: 10px;
            background-color: white;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 15px;
            padding: 0 10px;
            background-color: white;
            border: 2px solid {ModernBabbittTheme.CARD_BORDER};
            border-radius: 4px;
        }}
        
        /* === RADIO BUTTON IMPROVEMENTS === */
        QRadioButton {{
            font-size: 13px;
            padding: 6px;
            spacing: 10px;
            color: {ModernBabbittTheme.DARK_GRAY};
        }}
        
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
        }}
        
        QRadioButton::indicator:unchecked {{
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 9px;
            background-color: white;
        }}
        
        QRadioButton::indicator:checked {{
            border: 2px solid {ModernBabbittTheme.PRIMARY_BLUE};
            border-radius: 9px;
            background-color: {ModernBabbittTheme.PRIMARY_BLUE};
            background-image: radial-gradient(circle, white 30%, transparent 32%);
        }}
        
        QRadioButton::indicator:hover {{
            border-color: {ModernBabbittTheme.SECONDARY_BLUE};
        }}
        
        /* === SCROLL AREA IMPROVEMENTS === */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            border: none;
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {ModernBabbittTheme.MEDIUM_GRAY};
            border-radius: 6px;
            min-height: 30px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* === LIST WIDGET MODERN STYLING === */
        QListWidget {{
            border: 2px solid {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 8px;
            background-color: {ModernBabbittTheme.LIGHT_GRAY};
            outline: none;
            font-size: 13px;
        }}
        
        QListWidget::item {{
            padding: 12px 16px;
            border-bottom: 1px solid {ModernBabbittTheme.BORDER_GRAY};
            background-color: white;
            margin: 3px;
            border-radius: 6px;
        }}
        
        QListWidget::item:hover {{
            background-color: {ModernBabbittTheme.LIGHT_BLUE};
            border-color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}
        
        QListWidget::item:selected {{
            background-color: {ModernBabbittTheme.PRIMARY_BLUE};
            color: white;
            border-color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}
        
        /* === PROGRESS BAR STYLING === */
        QProgressBar {{
            border: none;
            background-color: {ModernBabbittTheme.BORDER_GRAY};
            border-radius: 4px;
            text-align: center;
            font-weight: 600;
            font-size: 12px;
        }}
        
        QProgressBar::chunk {{
            background-color: {ModernBabbittTheme.SUCCESS_GREEN};
            border-radius: 4px;
        }}
        
        /* === FRAME IMPROVEMENTS === */
        QFrame[frameType="card"] {{
            background-color: white;
            border: 1px solid {ModernBabbittTheme.CARD_BORDER};
            border-radius: 8px;
            margin: 4px;
        }}
        
        QFrame[frameType="panel"] {{
            background-color: white;
            border: none;
            border-radius: 0px;
        }}
        
        /* === LABEL STYLING === */
        QLabel[labelType="title"] {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernBabbittTheme.PRIMARY_BLUE};
            margin: 8px 0;
        }}
        
        QLabel[labelType="subtitle"] {{
            font-size: 14px;
            font-weight: 500;
            color: {ModernBabbittTheme.DARK_GRAY};
            margin: 4px 0;
        }}
        
        QLabel[labelType="caption"] {{
            font-size: 12px;
            color: {ModernBabbittTheme.MEDIUM_GRAY};
            margin: 2px 0;
        }}
        
        /* === STATUS INDICATOR STYLES === */
        QLabel[status="success"] {{
            color: {ModernBabbittTheme.SUCCESS_GREEN};
            font-weight: 600;
        }}
        
        QLabel[status="warning"] {{
            color: {ModernBabbittTheme.WARNING_ORANGE};
            font-weight: 600;
        }}
        
        QLabel[status="error"] {{
            color: {ModernBabbittTheme.ERROR_RED};
            font-weight: 600;
        }}
        
        QLabel[status="info"] {{
            color: {ModernBabbittTheme.INFO_BLUE};
            font-weight: 600;
        }}
        
        /* === PRICING LABEL STYLES === */
        QLabel[priceType="base"] {{
            font-size: 14px;
            color: {ModernBabbittTheme.MEDIUM_GRAY};
            font-weight: 400;
        }}
        
        QLabel[priceType="total"] {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernBabbittTheme.PRIMARY_BLUE};
        }}
        
        QLabel[priceType="adder"] {{
            font-size: 11px;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        QLabel[priceType="adder"][adderType="positive"] {{
            background-color: {ModernBabbittTheme.SUCCESS_GREEN};
            color: white;
        }}
        
        QLabel[priceType="adder"][adderType="negative"] {{
            background-color: {ModernBabbittTheme.ERROR_RED};
            color: white;
        }}
        
        QLabel[priceType="adder"][adderType="standard"] {{
            background-color: {ModernBabbittTheme.MEDIUM_GRAY};
            color: white;
        }}
        """
    
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
            base_style += """
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            """
        
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