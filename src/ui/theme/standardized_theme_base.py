"""
Complete Standardized Theme Base with Comprehensive UI Styling
File: src/ui/theme/standardized_theme_base.py

🔴 Critical - Replaces your existing file with complete CSS coverage
"""

from abc import ABC
from PySide6.QtCore import QCoreApplication
from src.ui.theme.dashboard_styles import get_dashboard_stylesheet


class StandardizedThemeBase(ABC):
    """
    Complete standardized base class for all themes with comprehensive UI styling.
    
    This provides consistent formatting for ALL UI components while allowing
    only colors to vary between themes.
    """
    
    # ============================================================================
    # STANDARD SIZING CONSTANTS - NEVER CHANGE THESE
    # ============================================================================
    
    # Font Sizes
    FONT_SIZE_XS = "11px"
    FONT_SIZE_SM = "12px" 
    FONT_SIZE_BASE = "14px"
    FONT_SIZE_LG = "16px"
    FONT_SIZE_XL = "18px"
    FONT_SIZE_2XL = "20px"
    FONT_SIZE_3XL = "24px"
    
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
    
    # Border Radius
    BORDER_RADIUS_SM = "4px"
    BORDER_RADIUS_MD = "6px"
    BORDER_RADIUS_LG = "8px"
    BORDER_RADIUS_XL = "12px"
    
    # Component Sizes
    BUTTON_HEIGHT = "36px"
    INPUT_HEIGHT = "36px"
    LARGE_BUTTON_HEIGHT = "44px"
    CARD_PADDING = "20px"
    SIDEBAR_WIDTH = "240px"
    
    # ============================================================================
    # COLOR PLACEHOLDERS - OVERRIDE IN EACH THEME
    # ============================================================================
    
    # Primary Colors
    PRIMARY_COLOR = "#1976d2"
    SECONDARY_COLOR = "#1565c0"
    ACCENT_COLOR = "#ff6b35"
    
    # Status Colors
    SUCCESS_COLOR = "#4caf50"
    WARNING_COLOR = "#ff9800"
    ERROR_COLOR = "#f44336"
    INFO_COLOR = "#2196f3"
    
    # Background Colors
    BACKGROUND_PRIMARY = "#ffffff"
    BACKGROUND_SECONDARY = "#f8f9fa"
    BACKGROUND_CARD = "#ffffff"
    BACKGROUND_SURFACE = "#f5f5f5"
    
    # Text Colors
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    TEXT_MUTED = "#9e9e9e"
    
    # Border Colors
    BORDER_COLOR = "#e0e0e0"
    BORDER_COLOR_LIGHT = "#f5f5f5"
    
    # Interactive States
    HOVER_BACKGROUND = "#f5f5f5"
    ACTIVE_BACKGROUND = "#1976d2"
    FOCUS_BORDER = "#1976d2"
    
    @classmethod
    def get_complete_stylesheet(cls):
        """Get the comprehensive stylesheet covering ALL UI components."""
        return f"""
        /* =====================================================================
           GLOBAL APPLICATION STYLES
           ===================================================================== */
        
        QApplication {{
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: {cls.FONT_SIZE_BASE};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QMainWindow {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QDialog {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
        }}
        
        /* =====================================================================
           SIDEBAR STYLES
           ===================================================================== */
        
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
            background-color: rgba(255, 255, 255, 0.15);
            border-left: 3px solid {cls.ACCENT_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        /* =====================================================================
           BUTTON STYLES - COMPREHENSIVE
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
        
        QPushButton:disabled {{
            background-color: {cls.BORDER_COLOR_LIGHT};
            color: {cls.TEXT_MUTED};
        }}
        
        /* Primary Button */
        QPushButton.primary, QPushButton#newQuoteButton, QPushButton[buttonStyle="primary"] {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            min-height: {cls.LARGE_BUTTON_HEIGHT};
        }}
        
        QPushButton.primary:hover, QPushButton#newQuoteButton:hover, QPushButton[buttonStyle="primary"]:hover {{
            background-color: {cls.SECONDARY_COLOR};
        }}
        
        /* Success Button */
        QPushButton.success, QPushButton#addToQuoteButton, QPushButton#configureButton {{
            background-color: {cls.SUCCESS_COLOR};
            color: white;
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        QPushButton.success:hover, QPushButton#addToQuoteButton:hover, QPushButton#configureButton:hover {{
            background-color: #388e3c;
        }}
        
        /* Secondary Button */
        QPushButton.secondary, QPushButton#saveDraftButton {{
            background-color: transparent;
            color: {cls.PRIMARY_COLOR};
            border: 2px solid {cls.PRIMARY_COLOR};
        }}
        
        QPushButton.secondary:hover, QPushButton#saveDraftButton:hover {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        /* Danger Button */
        QPushButton.danger, QPushButton#deleteButton {{
            background-color: {cls.ERROR_COLOR};
            color: white;
        }}
        
        QPushButton.danger:hover, QPushButton#deleteButton:hover {{
            background-color: #d32f2f;
        }}
        
        /* =====================================================================
           FORM CONTROLS - COMPREHENSIVE
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
        
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background-color: {cls.BACKGROUND_SURFACE};
            color: {cls.TEXT_MUTED};
        }}
        
        /* ComboBox - FIXED OVERSIZED DROPDOWN ISSUE */
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
            width: 24px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {cls.TEXT_SECONDARY};
            margin-top: 2px;
        }}
        
        QComboBox QAbstractItemView {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            background-color: {cls.BACKGROUND_CARD};
            selection-background-color: {cls.HOVER_BACKGROUND};
            max-height: 200px;
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            min-height: 32px;
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        /* SpinBox */
        QSpinBox, QDoubleSpinBox {{
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            background-color: {cls.BACKGROUND_CARD};
            min-height: {cls.INPUT_HEIGHT};
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {cls.FOCUS_BORDER};
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
        
        /* RadioButton */
        QRadioButton {{
            font-size: {cls.FONT_SIZE_BASE};
            color: {cls.TEXT_PRIMARY};
            spacing: {cls.SPACING_SM};
        }}
        
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {cls.BORDER_COLOR};
            border-radius: 9px;
            background-color: {cls.BACKGROUND_CARD};
        }}
        
        QRadioButton::indicator:checked {{
            background-color: {cls.PRIMARY_COLOR};
            border-color: {cls.PRIMARY_COLOR};
        }}
        
        /* =====================================================================
           LABELS AND TEXT
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
        
        QLabel.subtitle {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.TEXT_PRIMARY};
            margin-bottom: {cls.SPACING_MD};
        }}
        
        QLabel.section-header {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            margin: {cls.SPACING_LG} 0 {cls.SPACING_SM} 0;
        }}
        
        QLabel.field-label {{
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            color: {cls.TEXT_PRIMARY};
            margin-bottom: {cls.SPACING_XS};
        }}
        
        QLabel.secondary-text {{
            color: {cls.TEXT_SECONDARY};
            font-size: {cls.FONT_SIZE_SM};
        }}
        
        QLabel.muted-text {{
            color: {cls.TEXT_MUTED};
            font-size: {cls.FONT_SIZE_SM};
        }}
        
        QLabel.price {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
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
        
        /* Content Areas */
        QFrame#contentAreaFrame {{
            background-color: {cls.BACKGROUND_PRIMARY};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background-color: {cls.BACKGROUND_CARD};
            border-bottom: 2px solid {cls.BORDER_COLOR};
            padding: {cls.SPACING_XL};
            min-height: 80px;
        }}
        
        /* =====================================================================
           CONFIGURATION WIZARD SPECIFIC STYLES
           ===================================================================== */
        
        /* Progress Indicator */
        QFrame#progressIndicator {{
            background-color: {cls.BACKGROUND_CARD};
            border-bottom: 2px solid {cls.BORDER_COLOR};
            padding: {cls.SPACING_XL};
        }}
        
        QLabel.stepNumber {{
            min-width: 32px;
            max-width: 32px;
            min-height: 32px;
            max-height: 32px;
            border-radius: 16px;
            background-color: {cls.BORDER_COLOR};
            color: {cls.TEXT_MUTED};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            font-size: {cls.FONT_SIZE_BASE};
            qproperty-alignment: AlignCenter;
        }}
        
        QLabel.stepNumber[active="true"] {{
            background-color: {cls.PRIMARY_COLOR};
            color: white;
        }}
        
        QLabel.stepNumber[completed="true"] {{
            background-color: {cls.SUCCESS_COLOR};
            color: white;
        }}
        
        QLabel.stepLabel {{
            color: {cls.TEXT_SECONDARY};
            font-size: {cls.FONT_SIZE_SM};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            margin-top: {cls.SPACING_XS};
        }}
        
        QLabel.stepLabel[active="true"] {{
            color: {cls.PRIMARY_COLOR};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        /* Configuration Panels */
        QScrollArea#configScrollArea {{
            border: none;
            background-color: {cls.BACKGROUND_PRIMARY};
        }}
        
        QScrollArea#configScrollArea QWidget {{
            background-color: {cls.BACKGROUND_PRIMARY};
        }}
        
        QFrame.config-section {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_XL};
            margin-bottom: {cls.SPACING_LG};
        }}
        
        QLabel.config-section-title {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            margin-bottom: {cls.SPACING_LG};
        }}
        
        /* Option Groups */
        QFrame.option-group {{
            border: none;
            margin-bottom: {cls.SPACING_LG};
        }}
        
        QLabel.option-label {{
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            color: {cls.TEXT_PRIMARY};
            margin-bottom: {cls.SPACING_SM};
        }}
        
        /* Quote Summary Panel */
        QFrame#quoteSummaryPanel {{
            background-color: {cls.BACKGROUND_SECONDARY};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_XL};
        }}
        
        QLabel#quoteSummaryTitle {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.PRIMARY_COLOR};
            margin-bottom: {cls.SPACING_LG};
        }}
        
        QLabel#quoteTotal {{
            font-size: {cls.FONT_SIZE_2XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.SUCCESS_COLOR};
            margin-top: {cls.SPACING_LG};
        }}
        
        /* =====================================================================
           DASHBOARD STYLES
           ===================================================================== */
        
        QFrame.stat-card {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_XL};
            min-height: 120px;
        }}
        
        QLabel.stat-value {{
            font-size: {cls.FONT_SIZE_3XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
        }}
        
        QLabel.stat-label {{
            font-size: {cls.FONT_SIZE_BASE};
            color: {cls.TEXT_SECONDARY};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
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
           SCROLLBARS
           ===================================================================== */
        
        QScrollBar:vertical {{
            background-color: {cls.BACKGROUND_SURFACE};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 6px;
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
            height: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 6px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {cls.TEXT_MUTED};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* =====================================================================
           TOOLTIPS
           ===================================================================== */
        
        QToolTip {{
            background-color: {cls.TEXT_PRIMARY};
            color: {cls.BACKGROUND_CARD};
            border: none;
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM} {cls.SPACING_MD};
            font-size: {cls.FONT_SIZE_SM};
        }}
        
        /* =====================================================================
           STATUS BADGES
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
        """
    
    @classmethod
    def get_main_stylesheet(cls):
        """Get the complete stylesheet for this theme."""
        complete_css = cls.get_complete_stylesheet()
        
        try:
            dashboard_css = get_dashboard_stylesheet(cls)
            return complete_css + "\n" + dashboard_css
        except ImportError:
            return complete_css
    
    @classmethod
    def apply_to_widget(cls, widget):
        """Apply this theme to a specific widget."""
        stylesheet = cls.get_main_stylesheet()
        widget.setStyleSheet(stylesheet)
    
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