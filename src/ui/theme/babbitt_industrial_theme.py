"""
Babbitt Industrial Theme - Fixed for MainWindow Integration
File: src/ui/theme/babbitt_industrial_theme.py

🔴 Critical - Fixed theme that works with your existing apply_theme() system
"""


class BabbittIndustrialTheme:
    """
    Professional industrial theme matching Babbitt International's website.
    Compatible with your existing MainWindow.apply_theme() system.
    """
    
    # ============================================================================
    # BABBITT INDUSTRIAL COLOR SCHEME - Website Inspired
    # ============================================================================
    
    # Primary Colors - Matching website palette
    PRIMARY_BLUE = "#0052cc"         # Bright blue (CTAs, links, active states)
    SECONDARY_BLUE = "#003d99"       # Darker blue (hover states)
    ACCENT_BLUE = "#0066ff"          # Vibrant blue (highlights)
    
    # Navigation Colors - Dark industrial header
    NAV_BACKGROUND = "#1a1a1a"       # Very dark gray/black (header)
    NAV_TEXT = "#ffffff"             # White text on dark
    NAV_ACCENT = "#0052cc"           # Blue accent for active items
    
    # Status Colors
    SUCCESS_GREEN = "#28a745"
    WARNING_ORANGE = "#ffc107"
    ERROR_RED = "#dc3545"
    INFO_BLUE = "#0052cc"
    
    # Background Colors
    WHITE = "#ffffff"
    LIGHT_GRAY = "#f8f9fa"
    MEDIUM_GRAY = "#6c757d"
    DARK_GRAY = "#212529"
    BORDER_GRAY = "#dee2e6"
    CARD_BORDER = "#e9ecef"
    
    # Interactive States
    HOVER_BACKGROUND = "#f8f9fa"
    HOVER_BLUE = "#004299"
    ACTIVE_BACKGROUND = "#0052cc"
    FOCUS_BORDER = "#0052cc"
    FOCUS_SHADOW = "0 0 0 3px rgba(0, 82, 204, 0.25)"
    
    @staticmethod
    def get_main_stylesheet():
        """
        Get the main stylesheet compatible with your existing MainWindow.apply_theme() system.
        This method is called by your current MainWindow._apply_theme() method.
        """
        return f"""
        /* ========================================================================
           BABBITT INDUSTRIAL THEME - MAIN APPLICATION STYLING
           Compatible with existing MainWindow.apply_theme() system
        ======================================================================== */
        
        /* Main Application Window */
        QMainWindow {{
            background-color: {BabbittIndustrialTheme.WHITE};
            color: {BabbittIndustrialTheme.DARK_GRAY};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
        }}
        
        /* ====== SIDEBAR (Dark Industrial Style like website) ====== */
        QFrame#sidebarFrame {{
            background-color: {BabbittIndustrialTheme.NAV_BACKGROUND};
            border: none;
            min-width: 200px;
            max-width: 200px;
        }}
        
        QLabel#logoLabel {{
            color: {BabbittIndustrialTheme.NAV_TEXT};
            font-size: 18px;
            font-weight: 600;
            padding: 20px 16px;
            border-bottom: 1px solid #333333;
        }}
        
        /* Navigation List - Dark theme with blue accents */
        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: {BabbittIndustrialTheme.NAV_TEXT};
            font-size: 14px;
            outline: none;
            padding: 10px 0;
        }}
        
        QListWidget#navList::item {{
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
            border-radius: 0;
        }}
        
        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.1);
            color: {BabbittIndustrialTheme.NAV_TEXT};
        }}
        
        QListWidget#navList::item:selected {{
            background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            border-left: 3px solid {BabbittIndustrialTheme.ACCENT_BLUE};
            color: {BabbittIndustrialTheme.NAV_TEXT};
            font-weight: 500;
        }}
        
        /* ====== CONTENT AREA (Clean White like website) ====== */
        QFrame#contentFrame {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: none;
        }}
        
        /* Page Headers */
        QLabel#pageTitle {{
            color: {BabbittIndustrialTheme.DARK_GRAY};
            font-size: 24px;
            font-weight: 600;
            margin: 20px 0 10px 0;
            padding: 0 20px;
        }}
        
        /* ====== BUTTONS (Industrial Blue Accents) ====== */
        QPushButton {{
            background-color: {BabbittIndustrialTheme.WHITE};
            color: {BabbittIndustrialTheme.DARK_GRAY};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
            min-height: 36px;
        }}
        
        QPushButton:hover {{
            background-color: {BabbittIndustrialTheme.HOVER_BACKGROUND};
            border-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
        }}
        
        QPushButton:pressed {{
            background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            color: {BabbittIndustrialTheme.NAV_TEXT};
        }}
        
        /* Primary Button - Bright Blue (like website CTAs) */
        QPushButton#newQuoteBtn, QPushButton[buttonStyle="primary"] {{
            background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            color: {BabbittIndustrialTheme.NAV_TEXT};
            border: 1px solid {BabbittIndustrialTheme.PRIMARY_BLUE};
            font-weight: 600;
        }}
        
        QPushButton#newQuoteBtn:hover, QPushButton[buttonStyle="primary"]:hover {{
            background-color: {BabbittIndustrialTheme.HOVER_BLUE};
            border-color: {BabbittIndustrialTheme.HOVER_BLUE};
        }}
        
        /* ====== DASHBOARD CARDS (Clean Industrial Style) ====== */
        QFrame#metricsContainer {{
            background-color: transparent;
            border: none;
            padding: 20px;
        }}
        
        QFrame.metricCard {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: 1px solid {BabbittIndustrialTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
        }}
        
        QFrame.metricCard:hover {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
        }}
        
        /* Metric Card Content */
        QLabel.metricTitle {{
            color: {BabbittIndustrialTheme.MEDIUM_GRAY};
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 8px;
        }}
        
        QLabel.metricValue {{
            color: {BabbittIndustrialTheme.DARK_GRAY};
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        
        QLabel.metricSubtext {{
            color: {BabbittIndustrialTheme.MEDIUM_GRAY};
            font-size: 12px;
        }}
        
        /* ====== INPUTS & DROPDOWNS ====== */
        QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 4px;
            padding: 8px 12px;
            color: {BabbittIndustrialTheme.DARK_GRAY};
            font-size: 14px;
            min-height: 20px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            box-shadow: {BabbittIndustrialTheme.FOCUS_SHADOW};
        }}
        
        QComboBox {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 4px;
            padding: 8px 12px;
            color: {BabbittIndustrialTheme.DARK_GRAY};
            font-size: 14px;
            min-height: 20px;
        }}
        
        QComboBox:hover {{
            border-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            selection-background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            selection-color: {BabbittIndustrialTheme.NAV_TEXT};
        }}
        
        /* ====== TABLES & LISTS ====== */
        QListWidget, QTreeWidget {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 6px;
            alternate-background-color: {BabbittIndustrialTheme.LIGHT_GRAY};
        }}
        
        QListWidget::item, QTreeWidget::item {{
            padding: 8px 12px;
            border-radius: 4px;
            margin: 1px;
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected {{
            background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            color: {BabbittIndustrialTheme.NAV_TEXT};
        }}
        
        QListWidget::item:hover, QTreeWidget::item:hover {{
            background-color: {BabbittIndustrialTheme.HOVER_BACKGROUND};
        }}
        
        QTableWidget {{
            background-color: {BabbittIndustrialTheme.WHITE};
            gridline-color: {BabbittIndustrialTheme.CARD_BORDER};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 6px;
        }}
        
        QHeaderView::section {{
            background-color: {BabbittIndustrialTheme.LIGHT_GRAY};
            color: {BabbittIndustrialTheme.DARK_GRAY};
            padding: 8px 12px;
            border: none;
            border-bottom: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            font-weight: 600;
        }}
        
        /* ====== DIALOGS & WINDOWS ====== */
        QDialog {{
            background-color: {BabbittIndustrialTheme.WHITE};
            color: {BabbittIndustrialTheme.DARK_GRAY};
        }}
        
        QGroupBox {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: 600;
            color: {BabbittIndustrialTheme.DARK_GRAY};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            font-weight: 600;
        }}
        
        /* ====== SCROLLBARS ====== */
        QScrollBar:vertical {{
            background-color: {BabbittIndustrialTheme.LIGHT_GRAY};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
        }}
        
        /* ====== STATUS LABELS ====== */
        QLabel[status="success"] {{
            color: {BabbittIndustrialTheme.SUCCESS_GREEN};
            font-weight: 500;
        }}
        
        QLabel[status="warning"] {{
            color: {BabbittIndustrialTheme.WARNING_ORANGE};
            font-weight: 500;
        }}
        
        QLabel[status="error"] {{
            color: {BabbittIndustrialTheme.ERROR_RED};
            font-weight: 500;
        }}
        
        QLabel[status="info"] {{
            color: {BabbittIndustrialTheme.INFO_BLUE};
            font-weight: 500;
        }}
        
        /* ====== MENU BAR (Dark theme) ====== */
        QMenuBar {{
            background-color: {BabbittIndustrialTheme.NAV_BACKGROUND};
            color: {BabbittIndustrialTheme.NAV_TEXT};
            border-bottom: 1px solid #333333;
            padding: 4px 0;
            font-weight: 500;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 6px 12px;
            margin: 0 2px;
        }}
        
        QMenuBar::item:selected, QMenuBar::item:hover {{
            background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            color: {BabbittIndustrialTheme.NAV_TEXT};
        }}
        
        QMenu {{
            background-color: {BabbittIndustrialTheme.WHITE};
            border: 1px solid {BabbittIndustrialTheme.BORDER_GRAY};
            border-radius: 6px;
            padding: 4px 0;
        }}
        
        QMenu::item {{
            padding: 6px 16px;
            margin: 0 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {BabbittIndustrialTheme.PRIMARY_BLUE};
            color: {BabbittIndustrialTheme.NAV_TEXT};
        }}
        """


# Integration helper to update your settings service
class BabbittIndustrialIntegration:
    """Helper for integrating the Babbitt Industrial theme with your existing system."""
    
    @staticmethod
    def register_theme():
        """
        Register this theme with your settings service.
        Add this to your SettingsService theme options.
        """
        return {
            'name': 'babbitt_industrial',
            'display_name': 'Babbitt Industrial',
            'description': 'Professional industrial theme matching Babbitt International website',
            'theme_class': BabbittIndustrialTheme
        }
    
    @staticmethod
    def apply_to_main_window(main_window):
        """Apply theme directly to main window if needed."""
        stylesheet = BabbittIndustrialTheme.get_main_stylesheet()
        main_window.setStyleSheet(stylesheet)
        print("🏭 Babbitt Industrial Theme applied to main window")


# ===== QUICK INTEGRATION INSTRUCTIONS =====
"""
1. Replace your theme file with this version:
   📁 src/ui/theme/babbitt_industrial_theme.py

2. Update your SettingsService to include this theme:
   
   # In your settings service file, add:
   from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialTheme
   
   AVAILABLE_THEMES = {
       'babbitt': BabbittTheme,
       'babbitt_industrial': BabbittIndustrialTheme,  # Add this line
   }

3. Your existing apply_theme() method should now work:
   
   # This will now work with your existing MainWindow.apply_theme():
   window.apply_theme('babbitt_industrial')

4. OR test directly:
   
   # Add this to your MainWindow.__init__() to test immediately:
   from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialTheme
   self.setStyleSheet(BabbittIndustrialTheme.get_main_stylesheet())
"""