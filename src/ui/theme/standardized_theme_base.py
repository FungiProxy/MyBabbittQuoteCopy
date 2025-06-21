"""
Complete UI Fix - Professional Component Styling
File: src/ui/theme/standardized_theme_base.py

🔴 Critical - Replaces your theme base with working component styling
"""

from abc import ABC


class StandardizedThemeBase(ABC):
    """
    Complete theme base with working component styling for your application.
    Fixes all the flat, unstyled components visible in your screenshots.
    """
    
    # ============================================================================
    # LAYOUT CONSTANTS - OPTIMAL SIZING
    # ============================================================================
    
    # Window Sizing
    DEFAULT_WINDOW_WIDTH = "1300px"
    DEFAULT_WINDOW_HEIGHT = "750px"
    MINIMUM_WINDOW_WIDTH = "1100px"
    MINIMUM_WINDOW_HEIGHT = "650px"
    
    # Layout Proportions
    SIDEBAR_WIDTH = "180px"
    CONTENT_HEADER_HEIGHT = "70px"
    
    # Typography
    FONT_SIZE_XS = "11px"
    FONT_SIZE_SM = "12px"
    FONT_SIZE_BASE = "14px"
    FONT_SIZE_LG = "16px"
    FONT_SIZE_XL = "18px"
    FONT_SIZE_2XL = "22px"
    FONT_SIZE_3XL = "26px"
    
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
    
    # Border Radius
    BORDER_RADIUS_SM = "4px"
    BORDER_RADIUS_MD = "6px"
    BORDER_RADIUS_LG = "8px"
    BORDER_RADIUS_XL = "12px"
    
    # Component Sizes
    BUTTON_HEIGHT = "36px"
    INPUT_HEIGHT = "38px"
    LARGE_BUTTON_HEIGHT = "44px"
    
    # ============================================================================
    # PROFESSIONAL COLOR SCHEME
    # ============================================================================
    
    # Primary Colors
    PRIMARY_COLOR = "#1e40af"
    SECONDARY_COLOR = "#1d4ed8"
    ACCENT_COLOR = "#f59e0b"
    
    # Status Colors
    SUCCESS_COLOR = "#059669"
    WARNING_COLOR = "#d97706"
    ERROR_COLOR = "#dc2626"
    INFO_COLOR = "#0891b2"
    
    # Background Colors
    BACKGROUND_PRIMARY = "#f8fafc"
    BACKGROUND_SECONDARY = "#ffffff"
    BACKGROUND_CARD = "#ffffff"
    BACKGROUND_SURFACE = "#f1f5f9"
    
    # Text Colors
    TEXT_PRIMARY = "#0f172a"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#64748b"
    
    # Border Colors
    BORDER_COLOR = "#e2e8f0"
    BORDER_COLOR_LIGHT = "#f1f5f9"
    
    # Interactive States
    HOVER_BACKGROUND = "#f1f5f9"
    ACTIVE_BACKGROUND = "#1e40af"
    FOCUS_BORDER = "#1e40af"
    
    @classmethod
    def get_complete_stylesheet(cls):
        """Get the complete working stylesheet."""
        return f"""
        /* =====================================================================
           GLOBAL STYLES
           ===================================================================== */
        
        QMainWindow {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', 'Inter', 'Arial', sans-serif;
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        QWidget {{
            background-color: transparent;
            color: {cls.TEXT_PRIMARY};
        }}
        
        /* =====================================================================
           SIDEBAR - PROFESSIONAL GRADIENT
           ===================================================================== */
        
        QFrame#sidebarFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.PRIMARY_COLOR}, 
                stop:1 {cls.SECONDARY_COLOR});
            border: none;
            min-width: {cls.SIDEBAR_WIDTH};
            max-width: {cls.SIDEBAR_WIDTH};
        }}
        
        QLabel#logoLabel {{
            color: white;
            font-size: {cls.FONT_SIZE_2XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            padding: {cls.SPACING_2XL} {cls.SPACING_LG};
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
            padding: {cls.SPACING_MD} {cls.SPACING_LG};
            border-left: 3px solid transparent;
            margin: {cls.SPACING_XS} 0;
            border-radius: 0 {cls.BORDER_RADIUS_MD} {cls.BORDER_RADIUS_MD} 0;
            margin-right: {cls.SPACING_SM};
        }}
        
        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.15);
        }}
        
        QListWidget#navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.2);
            border-left: 3px solid {cls.ACCENT_COLOR};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        QPushButton#settingsButton {{
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: {cls.SPACING_SM} {cls.SPACING_LG};
            margin: {cls.SPACING_LG} {cls.SPACING_MD};
            border-radius: {cls.BORDER_RADIUS_MD};
            font-size: {cls.FONT_SIZE_SM};
        }}
        
        QPushButton#settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.2);
        }}
        
        /* =====================================================================
           CONTENT AREA
           ===================================================================== */
        
        QFrame#contentAreaFrame {{
            background-color: {cls.BACKGROUND_PRIMARY};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background-color: {cls.BACKGROUND_SECONDARY};
            border: none;
            border-bottom: 2px solid {cls.BORDER_COLOR};
            padding: {cls.SPACING_XL} {cls.SPACING_3XL};
            min-height: {cls.CONTENT_HEADER_HEIGHT};
            max-height: {cls.CONTENT_HEADER_HEIGHT};
        }}
        
        QLabel#pageTitle {{
            font-size: {cls.FONT_SIZE_3XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
        }}
        
        /* =====================================================================
           DASHBOARD STAT CARDS - FIXED
           ===================================================================== */
        
        QFrame[objectName*="statCard"], QFrame[objectName*="StatCard"], 
        QFrame[objectName*="card"], QFrame[objectName*="Card"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.BACKGROUND_CARD}, 
                stop:1 {cls.BACKGROUND_SURFACE});
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_2XL};
            margin: {cls.SPACING_MD};
            min-height: 120px;
        }}
        
        /* Dashboard specific styling for any QFrame that contains stats */
        QFrame:has(QLabel[text*="Total"]), QFrame:has(QLabel[text*="Quote"]), 
        QFrame:has(QLabel[text*="Active"]), QFrame:has(QLabel[text*="Customer"]) {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.BACKGROUND_CARD}, 
                stop:1 {cls.BACKGROUND_SURFACE});
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_2XL};
            margin: {cls.SPACING_MD};
        }}
        
        /* Stat card labels styling */
        QLabel[text*="Total Quotes"], QLabel[text*="Quote Value"], 
        QLabel[text*="Active Customers"], QLabel[text*="This month"],
        QLabel[text*="Total pending"], QLabel[text*="This quarter"] {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            margin-bottom: {cls.SPACING_SM};
        }}
        
        /* Stat values (numbers) */
        QLabel[text="0"], QLabel[text="$0.00"] {{
            font-size: {cls.FONT_SIZE_3XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
        }}
        
        /* =====================================================================
           BUTTONS - COMPREHENSIVE STYLING
           ===================================================================== */
        
        QPushButton {{
            border: none;
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_LG};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            font-size: {cls.FONT_SIZE_BASE};
            min-height: {cls.BUTTON_HEIGHT};
            background-color: {cls.BACKGROUND_SURFACE};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QPushButton:hover {{
            background-color: {cls.HOVER_BACKGROUND};
        }}
        
        QPushButton:pressed {{
            background-color: {cls.BORDER_COLOR};
        }}
        
        /* Primary Buttons */
        QPushButton#newQuoteButton, QPushButton[text*="New Quote"],
        QPushButton[text*="Add Product"], QPushButton[text*="Generate PDF"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.PRIMARY_COLOR}, 
                stop:1 {cls.SECONDARY_COLOR});
            color: white;
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            min-height: {cls.LARGE_BUTTON_HEIGHT};
        }}
        
        QPushButton#newQuoteButton:hover, QPushButton[text*="New Quote"]:hover,
        QPushButton[text*="Add Product"]:hover, QPushButton[text*="Generate PDF"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.SECONDARY_COLOR}, 
                stop:1 {cls.PRIMARY_COLOR});
        }}
        
        /* Success Buttons */
        QPushButton[text*="Finalize"], QPushButton[text*="Send"],
        QPushButton[text*="Save"], QPushButton[text*="Confirm"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.SUCCESS_COLOR}, 
                stop:1 #047857);
            color: white;
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        QPushButton[text*="Finalize"]:hover, QPushButton[text*="Send"]:hover,
        QPushButton[text*="Save"]:hover, QPushButton[text*="Confirm"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #047857, 
                stop:1 {cls.SUCCESS_COLOR});
        }}
        
        /* Secondary Buttons */
        QPushButton[text*="Save Draft"], QPushButton[text*="Cancel"],
        QPushButton[text*="Browse"], QPushButton[text*="Reset"] {{
            background-color: transparent;
            color: {cls.PRIMARY_COLOR};
            border: 2px solid {cls.PRIMARY_COLOR};
        }}
        
        QPushButton[text*="Save Draft"]:hover, QPushButton[text*="Cancel"]:hover,
        QPushButton[text*="Browse"]:hover, QPushButton[text*="Reset"]:hover {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        /* =====================================================================
           FORM CONTROLS - MODERN STYLING
           ===================================================================== */
        
        QLineEdit, QTextEdit, QPlainTextEdit {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            font-size: {cls.FONT_SIZE_BASE};
            background-color: {cls.BACKGROUND_CARD};
            min-height: {cls.INPUT_HEIGHT};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {cls.FOCUS_BORDER};
            outline: none;
        }}
        
        QLineEdit[placeholderText*="Enter"], QLineEdit[placeholderText*="Additional"] {{
            font-style: italic;
            color: {cls.TEXT_MUTED};
        }}
        
        /* ComboBox - Fixed sizing */
        QComboBox {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            background-color: {cls.BACKGROUND_CARD};
            font-size: {cls.FONT_SIZE_BASE};
            min-height: {cls.INPUT_HEIGHT};
            max-height: {cls.INPUT_HEIGHT};
        }}
        
        QComboBox:focus {{
            border-color: {cls.FOCUS_BORDER};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {cls.TEXT_SECONDARY};
        }}
        
        QComboBox QAbstractItemView {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            background-color: {cls.BACKGROUND_CARD};
            selection-background-color: {cls.PRIMARY_COLOR};
            selection-color: white;
            max-height: 200px;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            min-height: 28px;
        }}
        
        /* CheckBox */
        QCheckBox {{
            font-size: {cls.FONT_SIZE_BASE};
            color: {cls.TEXT_PRIMARY};
            spacing: {cls.SPACING_SM};
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 3px;
            background-color: {cls.BACKGROUND_CARD};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {cls.PRIMARY_COLOR};
            border-color: {cls.PRIMARY_COLOR};
        }}
        
        /* =====================================================================
           LABELS AND TYPOGRAPHY
           ===================================================================== */
        
        QLabel {{
            color: {cls.TEXT_PRIMARY};
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        /* Section headers */
        QLabel[text*="General"], QLabel[text*="Theme Preview"],
        QLabel[text*="Export Settings"], QLabel[text*="Database"],
        QLabel[text*="Quote Items"], QLabel[text*="Customer Information"] {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
            margin: {cls.SPACING_XL} 0 {cls.SPACING_LG} 0;
            padding-bottom: {cls.SPACING_SM};
            border-bottom: 2px solid {cls.BORDER_COLOR_LIGHT};
        }}
        
        /* Form field labels */
        QLabel[text*="Application Theme"], QLabel[text*="Startup Page"],
        QLabel[text*="Default Export Path"], QLabel[text*="Database Path"],
        QLabel[text*="Company Name"], QLabel[text*="Contact Person"],
        QLabel[text*="Email"], QLabel[text*="Phone"], QLabel[text*="Notes"] {{
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.TEXT_PRIMARY};
            font-size: {cls.FONT_SIZE_BASE};
            margin-bottom: {cls.SPACING_XS};
        }}
        
        /* Status labels */
        QLabel[text*="Status"], QLabel[text*="Total"] {{
            font-size: {cls.FONT_SIZE_SM};
            color: {cls.TEXT_SECONDARY};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QLabel[text*="Draft"] {{
            background-color: {cls.TEXT_MUTED};
            color: white;
            padding: {cls.SPACING_XS} {cls.SPACING_SM};
            border-radius: {cls.BORDER_RADIUS_SM};
            font-size: {cls.FONT_SIZE_XS};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        /* =====================================================================
           CONTAINERS AND SECTIONS
           ===================================================================== */
        
        /* Main content sections */
        QFrame[objectName*="section"], QFrame[objectName*="Section"],
        QFrame[objectName*="panel"], QFrame[objectName*="Panel"] {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_2XL};
            margin: {cls.SPACING_MD};
        }}
        
        /* Group boxes */
        QGroupBox {{
            background-color: {cls.BACKGROUND_CARD};
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding-top: {cls.SPACING_LG};
            margin-top: {cls.SPACING_MD};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            font-size: {cls.FONT_SIZE_LG};
            color: {cls.PRIMARY_COLOR};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 {cls.SPACING_SM};
            background-color: {cls.BACKGROUND_CARD};
        }}
        
        /* =====================================================================
           SPECIFIC UI FIXES
           ===================================================================== */
        
        /* Quote Items area */
        QFrame:has(QLabel[text*="No items added"]) {{
            background-color: {cls.BACKGROUND_SURFACE};
            border: 2px dashed {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_3XL};
            text-align: center;
        }}
        
        QLabel[text*="No items added"] {{
            color: {cls.TEXT_MUTED};
            font-style: italic;
            text-align: center;
        }}
        
        /* Recent Quotes section */
        QLabel[text*="No recent quotes found"] {{
            color: {cls.TEXT_MUTED};
            font-style: italic;
            text-align: center;
            padding: {cls.SPACING_3XL};
        }}
        
        /* =====================================================================
           SCROLLBARS
           ===================================================================== */
        
        QScrollBar:vertical {{
            background-color: {cls.BACKGROUND_SURFACE};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.TEXT_MUTED};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* =====================================================================
           FORM LAYOUT IMPROVEMENTS
           ===================================================================== */
        
        QFormLayout {{
            spacing: {cls.SPACING_LG};
        }}
        
        QVBoxLayout {{
            spacing: {cls.SPACING_MD};
        }}
        
        QHBoxLayout {{
            spacing: {cls.SPACING_MD};
        }}
        """
    
    @classmethod
    def get_main_stylesheet(cls):
        """Get the complete stylesheet."""
        return cls.get_complete_stylesheet()
    
    @classmethod
    def apply_to_widget(cls, widget):
        """Apply theme to widget with proper sizing."""
        stylesheet = cls.get_main_stylesheet()
        widget.setStyleSheet(stylesheet)
        
        # Set reasonable window size
        if hasattr(widget, 'resize'):
            widget.resize(1300, 750)
        if hasattr(widget, 'setMinimumSize'):
            widget.setMinimumSize(1100, 650)
    
    @classmethod
    def apply_to_application(cls, app=None):
        """Apply theme to entire application."""
        if app is None:
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
        
        if app is None:
            raise RuntimeError("No QApplication instance available")
        
        stylesheet = cls.get_main_stylesheet()
        app.setStyleSheet(stylesheet)
    
    @classmethod
    def get_theme_info(cls):
        """Get theme information."""
        return {
            'name': cls.__name__,
            'primary_color': cls.PRIMARY_COLOR,
            'secondary_color': cls.SECONDARY_COLOR,
            'accent_color': cls.ACCENT_COLOR,
            'background_color': cls.BACKGROUND_PRIMARY,
        }