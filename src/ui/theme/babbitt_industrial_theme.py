"""
Babbitt Industrial Theme - Inspired by Babbitt International Website
File: src/ui/theme/babbitt_industrial_theme.py

🔴 Critical - New theme matching Babbitt International's website aesthetic
"""

from src.ui.theme.standardized_theme_base import StandardizedThemeBase


class BabbittIndustrialTheme(StandardizedThemeBase):
    """
    Professional industrial theme inspired by Babbitt International's website.
    Features dark navigation, bright blue accents, and clean white content areas.
    """
    
    # ============================================================================
    # BABBITT INDUSTRIAL COLOR SCHEME - Website Inspired
    # ============================================================================
    
    # Primary Colors - Matching website palette
    PRIMARY_COLOR = "#0052cc"         # Bright blue (CTAs, links, active states)
    SECONDARY_COLOR = "#003d99"       # Darker blue (hover states)
    ACCENT_COLOR = "#0066ff"          # Vibrant blue (highlights)
    
    # Navigation Colors - Dark industrial header
    NAV_BACKGROUND = "#1a1a1a"        # Very dark gray/black (header)
    NAV_TEXT = "#ffffff"              # White text on dark
    NAV_ACCENT = "#0052cc"            # Blue accent for active items
    
    # Status Colors - Clear industrial indicators
    SUCCESS_COLOR = "#28a745"         # Professional green
    WARNING_COLOR = "#ffc107"         # Industrial yellow
    ERROR_COLOR = "#dc3545"           # Alert red
    INFO_COLOR = "#0052cc"            # Uses primary blue
    
    # Background Colors - Clean and professional
    BACKGROUND_PRIMARY = "#ffffff"     # Pure white content areas
    BACKGROUND_SECONDARY = "#f8f9fa"   # Light gray secondary areas
    BACKGROUND_CARD = "#ffffff"        # White cards with borders
    BACKGROUND_SURFACE = "#f5f5f5"     # Subtle gray for panels
    BACKGROUND_DARK = "#1a1a1a"        # Dark panels (navigation style)
    
    # Text Colors - Professional hierarchy
    TEXT_PRIMARY = "#212529"           # Dark charcoal (primary text)
    TEXT_SECONDARY = "#6c757d"         # Medium gray (secondary text)
    TEXT_MUTED = "#adb5bd"             # Light gray (muted text)
    TEXT_ON_DARK = "#ffffff"           # White text on dark backgrounds
    TEXT_ACCENT = "#0052cc"            # Blue text for links/accents
    
    # Border Colors - Subtle industrial styling
    BORDER_COLOR = "#dee2e6"           # Light gray borders
    BORDER_COLOR_LIGHT = "#e9ecef"     # Very light borders
    BORDER_ACCENT = "#0052cc"          # Blue accent borders
    
    # Interactive States - Smooth professional interactions
    HOVER_BACKGROUND = "#f8f9fa"       # Light hover
    HOVER_BLUE = "#004299"             # Blue hover (darker)
    ACTIVE_BACKGROUND = "#0052cc"      # Blue active
    FOCUS_BORDER = "#0052cc"           # Blue focus
    FOCUS_SHADOW = "0 0 0 3px rgba(0, 82, 204, 0.25)"  # Blue focus shadow
    
    @classmethod
    def get_complete_stylesheet(cls):
        """Get the complete stylesheet matching Babbitt International's aesthetic."""
        return f"""
        /* ========================================================================
           BABBITT INDUSTRIAL THEME - MAIN APPLICATION STYLING
           Inspired by Babbitt International website design
        ======================================================================== */
        
        /* Main Application Window */
        QMainWindow {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: {cls.FONT_SIZE_BASE};
        }}
        
        /* ====== NAVIGATION & HEADERS (Dark Industrial Style) ====== */
        QMenuBar {{
            background-color: {cls.NAV_BACKGROUND};
            color: {cls.NAV_TEXT};
            border-bottom: 1px solid #333333;
            padding: 8px 0;
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 16px;
            border-radius: {cls.BORDER_RADIUS_SM};
            margin: 0 4px;
        }}
        
        QMenuBar::item:selected, QMenuBar::item:hover {{
            background-color: {cls.NAV_ACCENT};
            color: {cls.NAV_TEXT};
        }}
        
        QMenu {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: 8px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        QMenu::item {{
            padding: 8px 20px;
            margin: 0 8px;
            border-radius: {cls.BORDER_RADIUS_SM};
        }}
        
        QMenu::item:selected {{
            background-color: {cls.HOVER_BACKGROUND};
            color: {cls.PRIMARY_COLOR};
        }}
        
        /* ====== BUTTONS (Industrial Blue Accents) ====== */
        QPushButton {{
            background-color: {cls.BACKGROUND_CARD};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_MD} {cls.SPACING_XL};
            font-size: {cls.FONT_SIZE_BASE};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
            min-height: {cls.BUTTON_HEIGHT};
        }}
        
        QPushButton:hover {{
            background-color: {cls.HOVER_BACKGROUND};
            border-color: {cls.PRIMARY_COLOR};
        }}
        
        QPushButton:pressed {{
            background-color: {cls.PRIMARY_COLOR};
            color: {cls.NAV_TEXT};
        }}
        
        /* Primary Button - Bright Blue (like website CTAs) */
        QPushButton[buttonStyle="primary"] {{
            background-color: {cls.PRIMARY_COLOR};
            color: {cls.NAV_TEXT};
            border: 1px solid {cls.PRIMARY_COLOR};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        QPushButton[buttonStyle="primary"]:hover {{
            background-color: {cls.HOVER_BLUE};
            border-color: {cls.HOVER_BLUE};
        }}
        
        /* Secondary Button */
        QPushButton[buttonStyle="secondary"] {{
            background-color: transparent;
            color: {cls.PRIMARY_COLOR};
            border: 1px solid {cls.PRIMARY_COLOR};
        }}
        
        QPushButton[buttonStyle="secondary"]:hover {{
            background-color: {cls.PRIMARY_COLOR};
            color: {cls.NAV_TEXT};
        }}
        
        /* ====== INPUTS & DROPDOWNS (Clean Industrial Style) ====== */
        QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_SM};
            padding: {cls.SPACING_MD};
            color: {cls.TEXT_PRIMARY};
            font-size: {cls.FONT_SIZE_BASE};
            min-height: {cls.INPUT_HEIGHT};
            max-height: {cls.INPUT_HEIGHT};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {cls.PRIMARY_COLOR};
            box-shadow: {cls.FOCUS_SHADOW};
        }}
        
        QComboBox {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_SM};
            padding: {cls.SPACING_MD};
            color: {cls.TEXT_PRIMARY};
            font-size: {cls.FONT_SIZE_BASE};
            min-height: 32px;
            max-height: 32px;
        }}
        
        QComboBox:hover {{
            border-color: {cls.PRIMARY_COLOR};
        }}
        
        QComboBox:focus {{
            border-color: {cls.PRIMARY_COLOR};
            box-shadow: {cls.FOCUS_SHADOW};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid {cls.BORDER_COLOR};
            border-top-right-radius: {cls.BORDER_RADIUS_SM};
            border-bottom-right-radius: {cls.BORDER_RADIUS_SM};
        }}
        
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0iIzZjNzU3ZCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            width: 12px;
            height: 8px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: 4px 0;
            selection-background-color: {cls.PRIMARY_COLOR};
            selection-color: {cls.NAV_TEXT};
        }}
        
        /* ====== CARDS & PANELS (Clean White Style) ====== */
        QFrame[frameType="card"] {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_LG};
            padding: {cls.SPACING_XL};
            margin: {cls.SPACING_MD};
        }}
        
        QFrame[frameType="card"][elevated="true"] {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-color: {cls.BORDER_COLOR_LIGHT};
        }}
        
        QGroupBox {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            margin-top: {cls.SPACING_LG};
            padding-top: {cls.SPACING_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {cls.SPACING_LG};
            padding: 0 {cls.SPACING_MD} 0 {cls.SPACING_MD};
            color: {cls.PRIMARY_COLOR};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        /* ====== LISTS & TABLES (Industrial Clean Style) ====== */
        QListWidget, QTreeWidget {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
            padding: {cls.SPACING_SM};
            alternate-background-color: {cls.BACKGROUND_SURFACE};
        }}
        
        QListWidget::item, QTreeWidget::item {{
            padding: {cls.SPACING_MD};
            border-radius: {cls.BORDER_RADIUS_SM};
            margin: 2px;
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected {{
            background-color: {cls.PRIMARY_COLOR};
            color: {cls.NAV_TEXT};
        }}
        
        QListWidget::item:hover, QTreeWidget::item:hover {{
            background-color: {cls.HOVER_BACKGROUND};
        }}
        
        QTableWidget {{
            background-color: {cls.BACKGROUND_CARD};
            gridline-color: {cls.BORDER_COLOR_LIGHT};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
        }}
        
        QHeaderView::section {{
            background-color: {cls.BACKGROUND_SURFACE};
            color: {cls.TEXT_PRIMARY};
            padding: {cls.SPACING_MD};
            border: none;
            border-bottom: 1px solid {cls.BORDER_COLOR};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
        }}
        
        /* ====== LABELS & TEXT (Professional Hierarchy) ====== */
        QLabel {{
            color: {cls.TEXT_PRIMARY};
            background-color: transparent;
        }}
        
        QLabel[labelType="title"] {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.TEXT_PRIMARY};
            margin-bottom: {cls.SPACING_LG};
        }}
        
        QLabel[labelType="subtitle"] {{
            font-size: {cls.FONT_SIZE_LG};
            font-weight: {cls.FONT_WEIGHT_SEMIBOLD};
            color: {cls.TEXT_SECONDARY};
            margin-bottom: {cls.SPACING_MD};
        }}
        
        QLabel[labelType="caption"] {{
            font-size: {cls.FONT_SIZE_SM};
            color: {cls.TEXT_MUTED};
        }}
        
        /* Price Labels */
        QLabel[priceType="total"] {{
            font-size: {cls.FONT_SIZE_XL};
            font-weight: {cls.FONT_WEIGHT_BOLD};
            color: {cls.PRIMARY_COLOR};
        }}
        
        QLabel[priceType="adder"][adderType="positive"] {{
            color: {cls.SUCCESS_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QLabel[priceType="adder"][adderType="negative"] {{
            color: {cls.ERROR_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        /* ====== DIALOGS & WINDOWS (Professional Layout) ====== */
        QDialog {{
            background-color: {cls.BACKGROUND_PRIMARY};
            color: {cls.TEXT_PRIMARY};
        }}
        
        QTabWidget::pane {{
            background-color: {cls.BACKGROUND_CARD};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: {cls.BORDER_RADIUS_MD};
        }}
        
        QTabBar::tab {{
            background-color: {cls.BACKGROUND_SURFACE};
            color: {cls.TEXT_SECONDARY};
            padding: {cls.SPACING_MD} {cls.SPACING_XL};
            margin-right: 2px;
            border-top-left-radius: {cls.BORDER_RADIUS_MD};
            border-top-right-radius: {cls.BORDER_RADIUS_MD};
        }}
        
        QTabBar::tab:selected {{
            background-color: {cls.PRIMARY_COLOR};
            color: {cls.NAV_TEXT};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {cls.HOVER_BACKGROUND};
            color: {cls.PRIMARY_COLOR};
        }}
        
        /* ====== SCROLLBARS (Minimal Industrial Style) ====== */
        QScrollBar:vertical {{
            background-color: {cls.BACKGROUND_SURFACE};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.BORDER_COLOR};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.PRIMARY_COLOR};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* ====== STATUS INDICATORS ====== */
        QLabel[status="success"] {{
            color: {cls.SUCCESS_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QLabel[status="warning"] {{
            color: {cls.WARNING_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QLabel[status="error"] {{
            color: {cls.ERROR_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        
        QLabel[status="info"] {{
            color: {cls.INFO_COLOR};
            font-weight: {cls.FONT_WEIGHT_MEDIUM};
        }}
        """
    
    @classmethod
    def apply_theme(cls, app):
        """Apply the Babbitt Industrial theme to the entire application."""
        app.setStyleSheet(cls.get_complete_stylesheet())
        
        # Set application-wide properties
        app.setProperty("theme", "babbitt_industrial")
        
        print("🏭 Babbitt Industrial Theme applied successfully!")
        print("   ✓ Dark navigation with bright blue accents")
        print("   ✓ Clean white content areas")
        print("   ✓ Professional industrial styling")


# Quick integration helper
class BabbittIndustrialIntegration:
    """Helper class for integrating the Babbitt Industrial theme."""
    
    @staticmethod
    def setup_main_window(main_window):
        """Setup main window with Babbitt Industrial styling."""
        main_window.setProperty("windowType", "main")
        main_window.setMinimumSize(1200, 700)
        
    @staticmethod
    def setup_dialog(dialog, dialog_type="standard"):
        """Setup dialog with appropriate Babbitt Industrial styling."""
        dialog.setProperty("dialogType", dialog_type)
        if dialog_type == "large":
            dialog.setMinimumSize(1000, 600)
        elif dialog_type == "medium":
            dialog.setMinimumSize(800, 500)
        else:
            dialog.setMinimumSize(600, 400)
    
    @staticmethod
    def create_primary_button(text: str):
        """Create a primary button with Babbitt Industrial styling."""
        from PySide6.QtWidgets import QPushButton
        button = QPushButton(text)
        button.setProperty("buttonStyle", "primary")
        return button
    
    @staticmethod
    def create_secondary_button(text: str):
        """Create a secondary button with Babbitt Industrial styling."""
        from PySide6.QtWidgets import QPushButton
        button = QPushButton(text)
        button.setProperty("buttonStyle", "secondary")
        return button