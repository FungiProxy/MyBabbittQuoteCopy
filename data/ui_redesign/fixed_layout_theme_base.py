"""
Fixed Layout & Standardized Theme Base - Professional UI
File: src/ui/theme/standardized_theme_base.py

🔴 Critical - Fixes window sizing, layout proportions, and styling issues
"""

from abc import ABC
from PySide6.QtCore import QCoreApplication


class StandardizedThemeBase(ABC):
    """
    Complete standardized theme with proper layout proportions and professional styling.
    Fixes window sizing, sidebar proportions, and overall UI/UX issues.
    """
    
    # ============================================================================
    # FIXED LAYOUT CONSTANTS - PROPER PROPORTIONS
    # ============================================================================
    
    # Window Sizing - Reasonable defaults
    DEFAULT_WINDOW_WIDTH = "1200px"
    DEFAULT_WINDOW_HEIGHT = "700px"
    MINIMUM_WINDOW_WIDTH = "1000px"
    MINIMUM_WINDOW_HEIGHT = "600px"
    
    # Layout Proportions - Much better balance
    SIDEBAR_WIDTH = "180px"        # Narrower sidebar
    CONTENT_HEADER_HEIGHT = "60px" # Reasonable header height
    
    # Font Sizes - Professional scale
    FONT_SIZE_XS = "11px"
    FONT_SIZE_SM = "12px" 
    FONT_SIZE_BASE = "13px"        # Slightly smaller base
    FONT_SIZE_LG = "15px"
    FONT_SIZE_XL = "17px"
    FONT_SIZE_2XL = "20px"
    FONT_SIZE_3XL = "24px"
    
    # Font Weights
    FONT_WEIGHT_NORMAL = "400"
    FONT_WEIGHT_MEDIUM = "500"
    FONT_WEIGHT_SEMIBOLD = "600"
    FONT_WEIGHT_BOLD = "700"
    
    # Spacing - Tighter, more professional
    SPACING_XS = "4px"
    SPACING_SM = "6px"
    SPACING_MD = "10px"
    SPACING_LG = "14px"
    SPACING_XL = "18px"
    SPACING_2XL = "22px"
    SPACING_3XL = "28px"
    
    # Border Radius
    BORDER_RADIUS_SM = "3px"
    BORDER_RADIUS_MD = "5px"
    BORDER_RADIUS_LG = "7px"
    BORDER_RADIUS_XL = "10px"
    
    # Component Sizes - Compact and professional
    BUTTON_HEIGHT = "32px"
    INPUT_HEIGHT = "32px"
    LARGE_BUTTON_HEIGHT = "38px"
    CARD_PADDING = "16px"
    
    # ============================================================================
    # MODERN COLOR SCHEME - OVERRIDE IN THEMES
    # ============================================================================
    
    # Primary Colors
    PRIMARY_COLOR = "#2563eb"      # Modern blue
    SECONDARY_COLOR = "#1d4ed8"    # Darker blue
    ACCENT_COLOR = "#f59e0b"       # Professional amber
    
    # Status Colors
    SUCCESS_COLOR = "#059669"      # Professional green
    WARNING_COLOR = "#d97706"      # Professional orange
    ERROR_COLOR = "#dc2626"        # Professional red
    INFO_COLOR = "#0891b2"         # Professional cyan
    
    # Background Colors - Clean and modern
    BACKGROUND_PRIMARY = "#ffffff"
    BACKGROUND_SECONDARY = "#f8fafc"
    BACKGROUND_CARD = "#ffffff"
    BACKGROUND_SURFACE = "#f1f5f9"
    
    # Text Colors
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    TEXT_MUTED = "#94a3b8"
    
    # Border Colors
    BORDER_COLOR = "#e2e8f0"
    BORDER_COLOR_LIGHT = "#f1f5f9"
    
    # Interactive States
    HOVER_BACKGROUND = "#f1f5f9"
    ACTIVE_BACKGROUND = "#2563eb"
    FOCUS_BORDER = "#2563eb"
    
    @classmethod
    def get_complete_stylesheet(cls):
        """Get the complete stylesheet with proper layout and modern styling."""
        return f"""
        /* =====================================================================
           MAIN WINDOW - FIXED SIZING AND LAYOUT
           ===================================================================== */
        
        QMainWindow {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', 'Inter', 'Arial', sans-serif;
            font-size: {cls.FONT_SIZE_BASE};
            min-width: {cls.MINIMUM_WINDOW_WIDTH};
            min-height: {cls.MINIMUM_WINDOW_HEIGHT};
        }}
        
        QDialog {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            min-width: 600px;
            min-height: 400px;
        }}
        
        /* =====================================================================
           SIDEBAR - MODERN PROFESSIONAL DESIGN
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
            padding: {cls.SPACING_XL} {cls.SPACING_LG};
            margin-bottom: {cls.SPACING_LG};
            background-color: transparent;
            qproperty-alignment: AlignCenter;
        }}
        
        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: white;
            font-size: {cls.FONT_SIZE_BASE};
            outline: none;
            padding: 0;
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
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QPushButton#settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.4);
        }}
        
        /* =====================================================================
           CONTENT AREA - MODERN LAYOUT
           ===================================================================== */
        
        QFrame#contentAreaFrame {{
            background-color: {cls.BACKGROUND_SECONDARY};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background-color: {cls.BACKGROUND_CARD};
            border: none;
            border-bottom: 1px solid {cls.BORDER_COLOR};
            padding: {cls.SPACING_LG} {cls.SPACING_2XL};
            min-height: {cls.CONTENT_HEADER_HEIGHT};
            max-height: {cls.CONTENT_HEADER_HEIGHT};
        }}
        
        QLabel#pageTitle {{
            font-size: {cls.FONT_SIZE_3XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
            margin: 0;
            padding: 0;
        }}
        
        /* =====================================================================
           BUTTONS - MODERN PROFESSIONAL STYLING
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
            transform: translateY(-1px);
        }}
        
        QPushButton:pressed {{
            background-color: {cls.BORDER_COLOR};
            transform: translateY(0px);
        }}
        
        QPushButton:disabled {{
            background-color: {cls.BORDER_COLOR_LIGHT};
            color: {cls.TEXT_MUTED};
        }}
        
        /* Primary Button */
        QPushButton.primary, QPushButton#newQuoteButton, QPushButton[buttonStyle="primary"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.PRIMARY_COLOR}, 
                stop:1 {cls.SECONDARY_COLOR});
            color: white;
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            min-height: {cls.LARGE_BUTTON_HEIGHT};
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        QPushButton.primary:hover, QPushButton#newQuoteButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.SECONDARY_COLOR}, 
                stop:1 {cls.PRIMARY_COLOR});
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        
        /* Success Button */
        QPushButton.success, QPushButton#addToQuoteButton, QPushButton#configureButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.SUCCESS_COLOR}, 
                stop:1 #047857);
            color: white;
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        QPushButton.success:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #047857, 
                stop:1 {cls.SUCCESS_COLOR});
        }}
        
        /* Secondary Button */
        QPushButton.secondary, QPushButton#saveDraftButton {{
            background-color: transparent;
            color: {cls.PRIMARY_COLOR};
            border: 2px solid {cls.PRIMARY_COLOR};
        }}
        
        QPushButton.secondary:hover {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        /* =====================================================================
           FORM CONTROLS - COMPACT AND MODERN
           ===================================================================== */
        
        QLineEdit, QTextEdit, QPlainTextEdit {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            font-size: {cls.FONT_SIZE_BASE};
            background-color: {cls.BACKGROUND_CARD};
            min-height: {cls.INPUT_HEIGHT};
            max-height: {cls.INPUT_HEIGHT};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {cls.FOCUS_BORDER};
            outline: none;
        }}
        
        QTextEdit, QPlainTextEdit {{
            min-height: 80px;
            max-height: none;
        }}
        
        /* ComboBox - FIXED SIZING ISSUES */
        QComboBox {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            background-color: {cls.BACKGROUND_CARD};
            font-size: {cls.FONT_SIZE_BASE};
            min-height: {cls.INPUT_HEIGHT};
            max-height: {cls.INPUT_HEIGHT};
            max-width: 250px;
        }}
        
        QComboBox:focus {{
            border-color: {cls.FOCUS_BORDER};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
            padding-right: {cls.SPACING_SM};
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {cls.TEXT_SECONDARY};
            margin-top: 2px;
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
            border-bottom: 1px solid {cls.BORDER_COLOR_LIGHT};
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        /* =====================================================================
           LABELS AND TYPOGRAPHY
           ===================================================================== */
        
        QLabel {{
            color: {cls.TEXT_PRIMARY};
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        QLabel.title, QLabel#pageTitle {{
            font-size: {cls.FONT_SIZE_3XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
            margin-bottom: {cls.SPACING_LG};
        }}
        
        QLabel.section-header {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            margin: {cls.SPACING_LG} 0 {cls.SPACING_SM} 0;
            padding-bottom: {cls.SPACING_XS};
            border-bottom: 2px solid {cls.BORDER_COLOR_LIGHT};
        }}
        
        QLabel.field-label {{
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            color: {cls.TEXT_PRIMARY};
            margin-bottom: {cls.SPACING_XS};
            font-size: {cls.FONT_SIZE_SM};
        }}
        
        QLabel.secondary-text {{
            color: {cls.TEXT_SECONDARY};
            font-size: {cls.FONT_SIZE_SM};
        }}
        
        QLabel.price {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.SUCCESS_COLOR};
        }}
        
        /* =====================================================================
           CARDS AND CONTAINERS
           ===================================================================== */
        
        QFrame.card, QGroupBox {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.CARD_PADDING};
            margin: {cls.SPACING_SM};
        }}
        
        QGroupBox {{
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            font-size: {cls.FONT_SIZE_LG};
            color: {cls.PRIMARY_COLOR};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 {cls.SPACING_SM};
            margin-top: -{cls.SPACING_SM};
            background-color: {cls.BACKGROUND_CARD};
        }}
        
        /* =====================================================================
           DASHBOARD SPECIFIC STYLES
           ===================================================================== */
        
        QFrame.stat-card {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.BACKGROUND_CARD}, 
                stop:1 {cls.BACKGROUND_SURFACE});
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_2XL};
            min-height: 100px;
            margin: {cls.SPACING_SM};
        }}
        
        QLabel.stat-value {{
            font-size: {cls.FONT_SIZE_3XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
            margin-bottom: {cls.SPACING_SM};
        }}
        
        QLabel.stat-label {{
            font-size: {cls.FONT_SIZE_BASE};
            color: {cls.TEXT_SECONDARY};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        /* =====================================================================
           FORM LAYOUT IMPROVEMENTS
           ===================================================================== */
        
        QFormLayout {{
            spacing: {cls.SPACING_MD};
        }}
        
        QVBoxLayout {{
            spacing: {cls.SPACING_MD};
        }}
        
        QHBoxLayout {{
            spacing: {cls.SPACING_MD};
        }}
        
        /* =====================================================================
           SCROLLBARS - MODERN THIN STYLE
           ===================================================================== */
        
        QScrollBar:vertical {{
            background-color: {cls.BACKGROUND_SURFACE};
            width: 8px;
            border-radius: 4px;
            border: none;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 4px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.TEXT_MUTED};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {cls.BACKGROUND_SURFACE};
            height: 8px;
            border-radius: 4px;
            border: none;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 4px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {cls.TEXT_MUTED};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* =====================================================================
           TABLES AND LISTS
           ===================================================================== */
        
        QTableWidget, QListWidget {{
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            background-color: {cls.BACKGROUND_CARD};
            alternate-background-color: {cls.BACKGROUND_SURFACE};
            gridline-color: {cls.BORDER_COLOR_LIGHT};
        }}
        
        QTableWidget::item, QListWidget::item {{
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            border-bottom: 1px solid {cls.BORDER_COLOR_LIGHT};
        }}
        
        QTableWidget::item:selected, QListWidget::item:selected {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {cls.BACKGROUND_SURFACE};
            padding: {cls.SPACING_MD} {cls.SPACING_LG};
            border: none;
            border-bottom: 2px solid {cls.BORDER_COLOR};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.TEXT_PRIMARY};
        }}
        
        /* =====================================================================
           STATUS INDICATORS
           ===================================================================== */
        
        QLabel.status-badge {{
            border-radius: {cls.BORDER_RADIUS_SM};
            padding: {cls.SPACING_XS} {cls.SPACING_SM};
            font-size: {cls.FONT_SIZE_XS};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: white;
        }}
        
        QLabel.status-badge[status="success"] {{
            background-color: {cls.SUCCESS_COLOR};
        }}
        
        QLabel.status-badge[status="warning"] {{
            background-color: {cls.WARNING_COLOR};
        }}
        
        QLabel.status-badge[status="error"] {{
            background-color: {cls.ERROR_COLOR};
        }}
        
        QLabel.status-badge[status="info"] {{
            background-color: {cls.INFO_COLOR};
        }}
        
        QLabel.status-badge[status="draft"] {{
            background-color: {cls.TEXT_MUTED};
        }}
        """
    
    @classmethod
    def get_main_stylesheet(cls):
        """Get the complete stylesheet for this theme."""
        return cls.get_complete_stylesheet()
    
    @classmethod
    def apply_to_widget(cls, widget):
        """Apply this theme to a specific widget."""
        stylesheet = cls.get_main_stylesheet()
        widget.setStyleSheet(stylesheet)
        
        # Set reasonable window size if it's a main window
        if hasattr(widget, 'resize'):
            widget.resize(1200, 700)
        if hasattr(widget, 'setMinimumSize'):
            widget.setMinimumSize(1000, 600)
    
    @classmethod
    def apply_to_application(cls, app=None):
        """Apply this theme to the entire application."""
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