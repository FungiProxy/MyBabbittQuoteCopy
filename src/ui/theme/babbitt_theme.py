"""
Babbitt International Theme System

Provides the industrial theme for MyBabbittQuote application with professional
blue color scheme and consistent styling across all components.
"""

from PySide6.QtWidgets import QWidget
from src.ui.theme.dashboard_styles import get_dashboard_stylesheet


class BabbittTheme(QWidget):
    """
    Theme system for Babbitt International MyBabbittQuote application.
    
    Provides a professional industrial color scheme with blue primary colors,
    gold accents, and clean styling appropriate for business use.
    """
    
    # ============================================================================
    # STANDARD SIZING CONSTANTS
    # ============================================================================
    FONT_SIZE_XS = "11px"
    FONT_SIZE_SM = "12px"
    FONT_SIZE_BASE = "14px"
    FONT_SIZE_LG = "16px"
    FONT_SIZE_XL = "18px"
    FONT_SIZE_2XL = "24px"
    FONT_SIZE_3XL = "28px"
    
    FONT_WEIGHT_NORMAL = "400"
    FONT_WEIGHT_MEDIUM = "500"
    FONT_WEIGHT_SEMIBOLD = "600"
    
    SPACING_SM = "8px"
    SPACING_MD = "12px"
    SPACING_LG = "16px"
    SPACING_XL = "20px"
    
    BORDER_RADIUS_MD = "6px"
    BORDER_RADIUS_LG = "8px"
    
    BUTTON_HEIGHT = "40px"
    INPUT_HEIGHT = "44px"
    
    # ============================================================================
    # COLOR DEFINITIONS
    # ============================================================================
    PRIMARY_BLUE = "#2C3E50"      # Deep professional blue
    SECONDARY_BLUE = "#34495E"    # Lighter blue for hover states
    ACCENT_GOLD = "#F39C12"       # Gold accent for highlights
    
    # Status Colors
    SUCCESS_GREEN = "#28A745"     # Success states, valid configurations
    WARNING_ORANGE = "#FD7E14"    # Warnings, attention needed
    ERROR_RED = "#DC3545"         # Errors, invalid states
    INFO_BLUE = "#17A2B8"         # Information, help text
    
    # Background Colors
    WHITE = "#FFFFFF"             # Primary background
    LIGHT_GRAY = "#F8F9FA"        # Secondary backgrounds, panels
    MEDIUM_GRAY = "#6C757D"       # Secondary text, borders
    DARK_GRAY = "#343A40"         # Dark text, headers
    CARD_BORDER = "#E9ECEF"       # Card and component borders
    
    @staticmethod
    def get_main_stylesheet():
        """Get the main application stylesheet."""
        return f"""
        /* Main Window and Global Styles */
        QMainWindow {{
            background-color: {BabbittTheme.LIGHT_GRAY};
            color: {BabbittTheme.DARK_GRAY};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {BabbittTheme.FONT_SIZE_BASE};
        }}
        
        /* Sidebar Styling */
        QFrame#sidebarFrame {{
            background-color: {BabbittTheme.PRIMARY_BLUE};
            border: none;
            min-width: 240px;
            max-width: 240px;
        }}
        
        QLabel#logoLabel {{
            color: {BabbittTheme.ACCENT_GOLD};
            font-size: {BabbittTheme.FONT_SIZE_2XL};
            font-weight: {BabbittTheme.FONT_WEIGHT_SEMIBOLD};
            padding: {BabbittTheme.SPACING_XL} {BabbittTheme.SPACING_MD};
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
            padding: {BabbittTheme.SPACING_MD} {BabbittTheme.SPACING_XL};
            border-left: 3px solid transparent;
            margin: 2px 0;
        }}
        
        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}
        
        QListWidget#navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-left: 3px solid {BabbittTheme.ACCENT_GOLD};
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
            background-color: {BabbittTheme.WHITE};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background-color: {BabbittTheme.WHITE};
            border-bottom: 1px solid {BabbittTheme.CARD_BORDER};
            padding: 20px;
            min-height: 60px;
        }}
        
        QLabel#pageTitle {{
            font-size: 24px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        /* Button Styles */
        QPushButton {{
            border-radius: {BabbittTheme.BORDER_RADIUS_MD};
            padding: {BabbittTheme.SPACING_SM} {BabbittTheme.SPACING_LG};
            font-weight: {BabbittTheme.FONT_WEIGHT_MEDIUM};
            font-size: {BabbittTheme.FONT_SIZE_BASE};
            min-height: {BabbittTheme.BUTTON_HEIGHT};
        }}
        
        QPushButton.primary {{
            background-color: {BabbittTheme.PRIMARY_BLUE};
            color: white;
        }}
        
        QPushButton.primary:hover {{
            background-color: {BabbittTheme.SECONDARY_BLUE};
        }}
        
        QPushButton.primary:pressed {{
            background-color: {BabbittTheme.DARK_GRAY};
        }}
        
        QPushButton.success {{
            background-color: {BabbittTheme.SUCCESS_GREEN};
            color: white;
        }}
        
        QPushButton.success:hover {{
            background-color: #1e7e34;
        }}
        
        QPushButton.secondary {{
            background-color: {BabbittTheme.MEDIUM_GRAY};
            color: white;
        }}
        
        QPushButton.secondary:hover {{
            background-color: #545b62;
        }}
        
        QPushButton.warning {{
            background-color: {BabbittTheme.WARNING_ORANGE};
            color: white;
        }}
        
        QPushButton.warning:hover {{
            background-color: #e0650e;
        }}
        
        QPushButton:disabled {{
            background-color: {BabbittTheme.CARD_BORDER};
            color: {BabbittTheme.MEDIUM_GRAY};
        }}
        
        /* Card Components */
        QFrame.card {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 20px;
        }}
        
        QFrame.card:hover {{
            border-color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        QFrame.productCard {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 20px;
            margin: 5px;
        }}
        
        QFrame.productCard:hover {{
            border-color: #2C3E50;
        }}
        
        QFrame.familyCard {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 6px;
            padding: 10px;
            margin: 4px 0;
        }}
        
        QFrame.familyCard:hover {{
            border-color: {BabbittTheme.PRIMARY_BLUE};
            background-color: #e3f2fd;
        }}
        
        QFrame.familyCard[selected="true"] {{
            border-color: {BabbittTheme.PRIMARY_BLUE};
            background-color: #e3f2fd;
        }}
        
        /* Custom classes for Dashboard */
        .quoteItemCard {{
            background-color: white;
            border: 1px solid #E9ECEF;
            border-radius: 6px;
            padding: 15px;
            margin: 5px 0;
        }}
        .quoteItemCard:hover {{
            border-color: #2C3E50;
        }}
        .quoteItemTitle {{
            font-weight: 600;
            color: #2C3E50;
            font-size: 14px;
        }}
        .quoteItemDetails {{
            color: #6C757D;
            font-size: 12px;
        }}
        .status-sent {{
            background-color: {BabbittTheme.SUCCESS_GREEN};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-draft {{
            background-color: {BabbittTheme.WARNING_ORANGE};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-default {{
            background-color: {BabbittTheme.MEDIUM_GRAY};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .placeholderText {{
            color: #6C757D;
            font-size: 14px;
            padding: 40px;
        }}
        #sectionTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
            margin-bottom: 15px;
        }}
        
        /* Custom classes for Quote Creation */
        .quoteSubtitle {{
            color: #6C757D;
            font-size: 14px;
        }}
        #quoteTotalLabel {{
            color: #2C3E50;
            font-weight: 600;
            font-size: 18px;
        }}
        .placeholderCard {{
            color: #6C757D;
            font-size: 14px;
            padding: 40px;
            background-color: #F8F9FA;
            border-radius: 4px;
            border: 1px dashed #E9ECEF;
        }}
        QPushButton.info.small {{
            background-color: {BabbittTheme.INFO_BLUE};
            color: white;
            border-radius: 2px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.info.small:hover {{
            background-color: #138496;
        }}
        QPushButton.danger.small {{
            background-color: {BabbittTheme.ERROR_RED};
            color: white;
            border-radius: 2px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.danger.small:hover {{
            background-color: #c82333;
        }}
        
        /* Custom styles for Product Selection */
        #progressIndicator {{
            background-color: white;
            border-bottom: 1px solid #E9ECEF;
            padding: 20px;
        }}
        #progressLine {{
            min-width: 40px;
            max-width: 40px;
            min-height: 2px;
            max-height: 2px;
            background-color: #E9ECEF;
            border: none;
        }}
        .stepLabel {{
            color: #6C757D;
            font-size: 12px;
            font-weight: 500;
        }}
        #familiesPanel {{
            background-color: #F8F9FA;
            border-right: 1px solid #E9ECEF;
        }}
        #productsPanel {{
            background-color: white;
        }}
        #categoryHeader {{
            font-size: 14px;
            font-weight: 600;
            color: #2C3E50;
            margin: 10px 0 5px 0;
            padding: 5px 0;
            border-bottom: 1px solid #E9ECEF;
        }}
        
        /* Custom styles for Configuration Wizard */
        #configPanel {{
            background-color: white;
            border-right: 1px solid #E9ECEF;
        }}
        #summaryPanel {{
            background-color: #F8F9FA;
        }}
        .formLabel {{
            font-weight: 500;
            color: #495057;
            margin-bottom: 8px;
        }}
        #summaryTotalFrame {{
            border-top: 2px solid #E9ECEF;
            padding-top: 15px;
            margin-top: 15px;
        }}
        #summaryTotalLabel, #summaryTotalPriceLabel {{
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
        }}
        
        /* Statistics Cards */
        QFrame.statCard {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
        }}
        
        QLabel.statTitle {{
            color: {BabbittTheme.MEDIUM_GRAY};
            font-size: 14px;
            font-weight: 500;
        }}
        
        QLabel.statValue {{
            color: {BabbittTheme.PRIMARY_BLUE};
            font-size: 28px;
            font-weight: 600;
            margin: 5px 0;
        }}
        
        QLabel.statSubtitle {{
            color: {BabbittTheme.MEDIUM_GRAY};
            font-size: 12px;
        }}
        
        QLabel.statIcon {{
            color: {BabbittTheme.PRIMARY_BLUE};
            font-size: 20px;
        }}
        
        /* Product Labels */
        QLabel.productName {{
            font-size: 18px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
            margin-bottom: 8px;
        }}
        
        QLabel.productDescription {{
            color: {BabbittTheme.MEDIUM_GRAY};
            font-size: 14px;
            margin-bottom: 15px;
        }}
        
        QLabel.productPrice {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittTheme.SUCCESS_GREEN};
            margin-bottom: 15px;
        }}
        
        QLabel.familyName {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        QLabel.familyDescription {{
            font-size: 12px;
            color: {BabbittTheme.MEDIUM_GRAY};
        }}
        
        /* Form Controls */
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            padding: {BabbittTheme.SPACING_SM} {BabbittTheme.SPACING_MD};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: {BabbittTheme.BORDER_RADIUS_MD};
            font-size: {BabbittTheme.FONT_SIZE_BASE};
            min-height: {BabbittTheme.INPUT_HEIGHT};
        }}
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border-color: {BabbittTheme.PRIMARY_BLUE};
            outline: none;
        }}
        
        QLabel.formLabel {{
            font-weight: 500;
            color: {BabbittTheme.DARK_GRAY};
            margin-bottom: 5px;
        }}
        
        QLabel.sectionTitle {{
            font-size: {BabbittTheme.FONT_SIZE_LG};
            font-weight: {BabbittTheme.FONT_WEIGHT_SEMIBOLD};
            color: {BabbittTheme.PRIMARY_BLUE};
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid {BabbittTheme.CARD_BORDER};
        }}
        
        /* Progress and Status */
        QProgressBar {{
            border-radius: 4px;
            height: 8px;
            background-color: {BabbittTheme.CARD_BORDER};
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {BabbittTheme.PRIMARY_BLUE};
            border-radius: 4px;
        }}
        
        QLabel.validationSuccess {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
        }}
        
        QLabel.validationError {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
        }}
        
        QLabel.validationWarning {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
        }}
        
        /* Step Indicator */
        QLabel.stepNumber {{
            width: 30px;
            height: 30px;
            border-radius: 15px;
            background-color: {BabbittTheme.CARD_BORDER};
            color: {BabbittTheme.MEDIUM_GRAY};
            font-weight: 600;
            text-align: center;
        }}
        
        QLabel.stepNumber[active="true"] {{
            background-color: {BabbittTheme.PRIMARY_BLUE};
            color: white;
        }}
        
        QLabel.stepNumber[completed="true"] {{
            background-color: {BabbittTheme.SUCCESS_GREEN};
            color: white;
        }}
        
        /* Tables */
        QTableWidget {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 4px;
            gridline-color: {BabbittTheme.CARD_BORDER};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {BabbittTheme.CARD_BORDER};
        }}
        
        QTableWidget::item:selected {{
            background-color: #e3f2fd;
            color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        QHeaderView::section {{
            background-color: {BabbittTheme.LIGHT_GRAY};
            color: {BabbittTheme.MEDIUM_GRAY};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {BabbittTheme.CARD_BORDER};
            font-weight: 500;
        }}
        
        /* Radio Buttons and Checkboxes */
        QRadioButton, QCheckBox {{
            color: {BabbittTheme.DARK_GRAY};
            spacing: 8px;
        }}
        
        QRadioButton::indicator, QCheckBox::indicator {{
            width: 16px;
            height: 16px;
        }}
        
        QRadioButton::indicator:unchecked {{
            border: 2px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            background-color: {BabbittTheme.WHITE};
        }}
        
        QRadioButton::indicator:checked {{
            border: 2px solid {BabbittTheme.PRIMARY_BLUE};
            border-radius: 8px;
            background-color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        QCheckBox::indicator:unchecked {{
            border: 2px solid {BabbittTheme.CARD_BORDER};
            border-radius: 2px;
            background-color: {BabbittTheme.WHITE};
        }}
        
        QCheckBox::indicator:checked {{
            border: 2px solid {BabbittTheme.PRIMARY_BLUE};
            border-radius: 2px;
            background-color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            border: none;
            background-color: {BabbittTheme.LIGHT_GRAY};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {BabbittTheme.MEDIUM_GRAY};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        /* Group Boxes */
        QGroupBox {{
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
            border: 2px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: {BabbittTheme.WHITE};
        }}
        """ + get_dashboard_stylesheet(BabbittTheme)

    # The STYLES dictionary and related methods are no longer needed
    # as dashboard styles are handled by get_dashboard_stylesheet.
    STYLES = {}

    @staticmethod
    def get_button_style(style_name: str) -> str:
        """Get the stylesheet for a specific button style."""
        return BabbittTheme.STYLES.get(style_name, "")

    @staticmethod
    def apply_stylesheet(widget, css_class):
        """Apply a CSS class to a widget."""
        current_class = widget.property("class") or ""
        widget.setProperty("class", f"{current_class} {css_class}".strip())
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    @staticmethod
    def apply_property_styles(widget, properties):
        """Apply property-based styles to a widget."""
        for name, value in properties.items():
            widget.setProperty(name, value)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
