"""
Standardized Theme Template

This template defines the standard structure, sizing, and formatting that all themes
should follow. Only colors and transition effects should vary between themes.
"""

from src.ui.theme.dashboard_styles import get_dashboard_stylesheet


class ThemeTemplate:
    """
    Standardized theme template for MyBabbittQuote application.
    
    This template ensures all themes have consistent:
    - Font sizes and weights
    - Padding and margins
    - Border radius values
    - Component sizing
    - Spacing between elements
    - Structure and organization
    
    Only colors and transition effects should vary between themes.
    """
    
    # ============================================================================
    # STANDARD SIZING CONSTANTS - DO NOT CHANGE
    # ============================================================================
    
    # Font Sizes
    FONT_SIZE_XS = "11px"      # Small labels, status badges
    FONT_SIZE_SM = "12px"      # Secondary text, captions
    FONT_SIZE_BASE = "14px"    # Default text size
    FONT_SIZE_LG = "16px"      # Section headers, form labels
    FONT_SIZE_XL = "18px"      # Card titles, important text
    FONT_SIZE_2XL = "24px"     # Page titles, main headers
    FONT_SIZE_3XL = "28px"     # Large statistics, hero text
    
    # Font Weights
    FONT_WEIGHT_NORMAL = "400"
    FONT_WEIGHT_MEDIUM = "500"
    FONT_WEIGHT_SEMIBOLD = "600"
    FONT_WEIGHT_BOLD = "700"
    
    # Spacing
    SPACING_XS = "4px"
    SPACING_SM = "8px"
    SPACING_MD = "12px"
    SPACING_LG = "16px"
    SPACING_XL = "20px"
    SPACING_2XL = "24px"
    SPACING_3XL = "32px"
    SPACING_4XL = "40px"
    
    # Border Radius
    BORDER_RADIUS_SM = "4px"
    BORDER_RADIUS_MD = "6px"
    BORDER_RADIUS_LG = "8px"
    BORDER_RADIUS_XL = "12px"
    BORDER_RADIUS_2XL = "16px"
    BORDER_RADIUS_FULL = "50%"
    
    # Component Heights
    BUTTON_HEIGHT = "40px"
    INPUT_HEIGHT = "44px"
    CARD_PADDING = "20px"
    SIDEBAR_WIDTH = "240px"
    
    # ============================================================================
    # COLOR PLACEHOLDERS - OVERRIDE IN EACH THEME
    # ============================================================================
    
    # Primary Colors
    PRIMARY_COLOR = "#PLACEHOLDER"
    SECONDARY_COLOR = "#PLACEHOLDER"
    ACCENT_COLOR = "#PLACEHOLDER"
    
    # Status Colors
    SUCCESS_COLOR = "#PLACEHOLDER"
    WARNING_COLOR = "#PLACEHOLDER"
    ERROR_COLOR = "#PLACEHOLDER"
    INFO_COLOR = "#PLACEHOLDER"
    
    # Background Colors
    BACKGROUND_PRIMARY = "#PLACEHOLDER"
    BACKGROUND_SECONDARY = "#PLACEHOLDER"
    BACKGROUND_CARD = "#PLACEHOLDER"
    BACKGROUND_SURFACE = "#PLACEHOLDER"
    
    # Text Colors
    TEXT_PRIMARY = "#PLACEHOLDER"
    TEXT_SECONDARY = "#PLACEHOLDER"
    TEXT_MUTED = "#PLACEHOLDER"
    
    # Border Colors
    BORDER_COLOR = "#PLACEHOLDER"
    BORDER_COLOR_LIGHT = "#PLACEHOLDER"
    
    # Interactive States
    HOVER_BACKGROUND = "#PLACEHOLDER"
    ACTIVE_BACKGROUND = "#PLACEHOLDER"
    FOCUS_BORDER = "#PLACEHOLDER"
    
    @classmethod
    def get_standard_stylesheet(cls):
        """
        Get the standardized stylesheet with consistent sizing and formatting.
        This method should be called by each theme's get_main_stylesheet method.
        """
        return f"""
        /* ============================================================================
           GLOBAL APPLICATION STYLES - STANDARDIZED
           ============================================================================ */
        
        QApplication {{
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: {cls.FONT_SIZE_BASE};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QMainWindow {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
        }}
        
        /* ============================================================================
           SIDEBAR STYLES - STANDARDIZED
           ============================================================================ */
        
        QFrame#sidebarFrame {{
            background-color: {cls.PRIMARY_COLOR};
            border: none;
            min-width: {cls.SIDEBAR_WIDTH};
            max-width: {cls.SIDEBAR_WIDTH};
        }}
        
        QLabel#logoLabel {{
            color: {cls.ACCENT_COLOR};
            font-size: {cls.FONT_SIZE_2XL};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            padding: {cls.SPACING_XL} {cls.SPACING_LG};
            background-color: transparent;
        }}
        
        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: white;
            font-size: {cls.FONT_SIZE_BASE};
            outline: none;
        }}
        
        QListWidget#navList::item {{
            padding: {cls.SPACING_MD} {cls.SPACING_XL};
            border-left: 3px solid transparent;
            margin: {cls.SPACING_XS} 0;
        }}
        
        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}
        
        QListWidget#navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-left: 3px solid {cls.ACCENT_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QPushButton#settingsButton {{
            background-color: transparent;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: {cls.SPACING_LG} {cls.SPACING_XL};
            margin: {cls.SPACING_LG};
            border-radius: {cls.BORDER_RADIUS_SM};
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        QPushButton#settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}
        
        /* ============================================================================
           CONTENT AREA STYLES - STANDARDIZED
           ============================================================================ */
        
        QFrame#contentAreaFrame {{
            background-color: {cls.BACKGROUND_PRIMARY};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background-color: {cls.BACKGROUND_CARD};
            border-bottom: 1px solid {cls.BORDER_COLOR};
            padding: {cls.SPACING_XL};
            min-height: 60px;
        }}
        
        QLabel#pageTitle {{
            font-size: {cls.FONT_SIZE_2XL};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
        }}
        
        /* ============================================================================
           BUTTON STYLES - STANDARDIZED
           ============================================================================ */
        
        QPushButton {{
            border: none;
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            font-size: {cls.FONT_SIZE_BASE};
            min-height: {cls.BUTTON_HEIGHT};
        }}
        
        QPushButton.primary {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        QPushButton.primary:hover {{
            background-color: {cls.SECONDARY_COLOR};
        }}
        
        QPushButton.primary:pressed {{
            background-color: {cls.ACTIVE_BACKGROUND};
        }}
        
        QPushButton.success {{
            background-color: {cls.SUCCESS_COLOR};
            color: white;
        }}
        
        QPushButton.success:hover {{
            background-color: {cls.SUCCESS_COLOR};
            opacity: 0.9;
        }}
        
        QPushButton.secondary {{
            background-color: {cls.BACKGROUND_SURFACE};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QPushButton.secondary:hover {{
            background-color: {cls.HOVER_BACKGROUND};
        }}
        
        QPushButton.warning {{
            background-color: {cls.WARNING_COLOR};
            color: white;
        }}
        
        QPushButton.warning:hover {{
            background-color: {cls.WARNING_COLOR};
            opacity: 0.9;
        }}
        
        QPushButton:disabled {{
            background-color: {cls.BACKGROUND_SURFACE};
            color: {cls.TEXT_MUTED};
        }}
        
        /* ============================================================================
           CARD COMPONENTS - STANDARDIZED
           ============================================================================ */
        
        QFrame.card {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.CARD_PADDING};
        }}
        
        QFrame.card:hover {{
            border-color: {cls.ACCENT_COLOR};
        }}
        
        QFrame.productCard {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.CARD_PADDING};
            margin: {cls.SPACING_SM};
        }}
        
        QFrame.productCard:hover {{
            border-color: {cls.ACCENT_COLOR};
        }}
        
        QFrame.familyCard {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_LG};
            margin: {cls.SPACING_XS} 0;
        }}
        
        QFrame.familyCard:hover {{
            border-color: {cls.ACCENT_COLOR};
            background-color: {cls.HOVER_BACKGROUND};
        }}
        
        QFrame.familyCard[selected="true"] {{
            border-color: {cls.ACCENT_COLOR};
            background-color: {cls.HOVER_BACKGROUND};
        }}
        
        /* ============================================================================
           FORM CONTROLS - STANDARDIZED
           ============================================================================ */
        
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            font-size: {cls.FONT_SIZE_BASE};
            background-color: {cls.BACKGROUND_CARD};
            min-height: {cls.INPUT_HEIGHT};
        }}
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border-color: {cls.FOCUS_BORDER};
            outline: none;
        }}
        
        QLabel.formLabel {{
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            color: {cls.TEXT_PRIMARY};
            margin-bottom: {cls.SPACING_SM};
        }}
        
        QLabel.sectionTitle {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            margin-bottom: {cls.SPACING_LG};
            padding-bottom: {cls.SPACING_SM};
            border-bottom: 2px solid {cls.BORDER_COLOR};
        }}
        
        /* ============================================================================
           TABLES - STANDARDIZED
           ============================================================================ */
        
        QTableWidget {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            gridline-color: {cls.BORDER_COLOR};
        }}
        
        QTableWidget::item {{
            padding: {cls.SPACING_SM};
            border-bottom: 1px solid {cls.BORDER_COLOR};
        }}
        
        QTableWidget::item:selected {{
            background-color: {cls.HOVER_BACKGROUND};
            color: {cls.PRIMARY_COLOR};
        }}
        
        QHeaderView::section {{
            background-color: {cls.BACKGROUND_SURFACE};
            color: {cls.TEXT_SECONDARY};
            padding: {cls.SPACING_LG};
            border: none;
            border-bottom: 1px solid {cls.BORDER_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        /* ============================================================================
           RADIO BUTTONS AND CHECKBOXES - STANDARDIZED
           ============================================================================ */
        
        QRadioButton, QCheckBox {{
            color: {cls.TEXT_PRIMARY};
            spacing: {cls.SPACING_SM};
        }}
        
        QRadioButton::indicator, QCheckBox::indicator {{
            width: 18px;
            height: 18px;
        }}
        
        QRadioButton::indicator:unchecked {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 9px;
            background-color: {cls.BACKGROUND_CARD};
        }}
        
        QRadioButton::indicator:checked {{
            border: 2px solid {cls.ACCENT_COLOR};
            border-radius: 9px;
            background-color: {cls.ACCENT_COLOR};
        }}
        
        QCheckBox::indicator:unchecked {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 4px;
            background-color: {cls.BACKGROUND_CARD};
        }}
        
        QCheckBox::indicator:checked {{
            border: 2px solid {cls.ACCENT_COLOR};
            border-radius: 4px;
            background-color: {cls.ACCENT_COLOR};
        }}
        
        /* ============================================================================
           SCROLL AREAS - STANDARDIZED
           ============================================================================ */
        
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            border: none;
            background-color: {cls.BACKGROUND_SECONDARY};
            width: 12px;
            margin: 0px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.ACCENT_COLOR};
        }}
        
        /* ============================================================================
           GROUP BOXES - STANDARDIZED
           ============================================================================ */
        
        QGroupBox {{
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            margin-top: {cls.SPACING_MD};
            padding-top: {cls.SPACING_MD};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {cls.SPACING_MD};
            padding: 0 {cls.SPACING_SM} 0 {cls.SPACING_SM};
            background-color: {cls.BACKGROUND_CARD};
        }}
        
        /* ============================================================================
           PROGRESS AND STATUS - STANDARDIZED
           ============================================================================ */
        
        QProgressBar {{
            border-radius: {cls.BORDER_RADIUS_SM};
            height: 8px;
            background-color: {cls.BORDER_COLOR};
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {cls.PRIMARY_COLOR};
            border-radius: {cls.BORDER_RADIUS_SM};
        }}
        
        QLabel.validationSuccess {{
            background-color: {cls.SUCCESS_COLOR};
            border: 1px solid {cls.SUCCESS_COLOR};
            color: white;
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            border-radius: {cls.BORDER_RADIUS_MD};
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        QLabel.validationError {{
            background-color: {cls.ERROR_COLOR};
            border: 1px solid {cls.ERROR_COLOR};
            color: white;
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            border-radius: {cls.BORDER_RADIUS_MD};
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        QLabel.validationWarning {{
            background-color: {cls.WARNING_COLOR};
            border: 1px solid {cls.WARNING_COLOR};
            color: white;
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            border-radius: {cls.BORDER_RADIUS_MD};
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        /* ============================================================================
           STEP INDICATOR - STANDARDIZED
           ============================================================================ */
        
        QLabel.stepNumber {{
            width: 30px;
            height: 30px;
            border-radius: 15px;
            background-color: {cls.BORDER_COLOR};
            color: {cls.TEXT_MUTED};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            text-align: center;
        }}
        
        QLabel.stepNumber[active="true"] {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        QLabel.stepNumber[completed="true"] {{
            background-color: {cls.SUCCESS_COLOR};
            color: white;
        }}
        
        /* ============================================================================
           PRODUCT LABELS - STANDARDIZED
           ============================================================================ */
        
        QLabel.productName {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            margin-bottom: {cls.SPACING_SM};
        }}
        
        QLabel.productDescription {{
            color: {cls.TEXT_SECONDARY};
            font-size: {cls.FONT_SIZE_BASE};
            margin-bottom: {cls.SPACING_LG};
        }}
        
        QLabel.productPrice {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.SUCCESS_COLOR};
            margin-bottom: {cls.SPACING_LG};
        }}
        
        QLabel.familyName {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
        }}
        
        QLabel.familyDescription {{
            font-size: {cls.FONT_SIZE_SM};
            color: {cls.TEXT_SECONDARY};
        }}
        """
    
    @staticmethod
    def apply_stylesheet(widget, css_class):
        """
        Apply a specific CSS class to a widget.
        
        This is a helper to simplify applying styles in the UI code.
        """
        widget.setProperty("class", css_class)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    @staticmethod
    def apply_property_styles(widget, properties):
        """
        Apply dynamic properties to a widget for styling.
        
        Example: apply_property_styles(my_label, {"active": "true"})
        """
        for prop, value in properties.items():
            widget.setProperty(prop, value)
        
        widget.style().unpolish(widget)
        widget.style().polish(widget)
