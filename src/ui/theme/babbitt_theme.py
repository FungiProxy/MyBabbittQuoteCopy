"""
Complete Babbitt Theme Implementation
File: src/ui/theme/babbitt_theme.py

🔴 Critical - Replace your existing babbitt_theme.py with this complete implementation
⏱️ 5 minutes to implement
"""


class BabbittTheme:
    """
    Complete Babbitt theme that matches your original polished UI.
    Professional blue gradient sidebar with orange accents.
    """
    
    # Color Constants - Matching your screenshots
    PRIMARY_BLUE = "#2C3E50"      # Deep blue from your sidebar
    SECONDARY_BLUE = "#34495E"    # Lighter blue for gradients
    ACCENT_ORANGE = "#F39C12"     # Orange accent from your buttons
    LIGHT_ORANGE = "#F8C471"      # Lighter orange for hovers
    
    # Background Colors
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F8F9FA"
    CARD_GRAY = "#F7F9FC"
    BORDER_GRAY = "#E9ECEF"
    
    # Text Colors
    DARK_TEXT = "#2C3E50"
    GRAY_TEXT = "#6C757D"
    LIGHT_TEXT = "#ADB5BD"
    
    # Status Colors
    SUCCESS_GREEN = "#28A745"
    WARNING_ORANGE = "#FFC107"
    ERROR_RED = "#DC3545"
    INFO_BLUE = "#17A2B8"

    @staticmethod
    def get_main_stylesheet():
        """Get the complete stylesheet that matches your original UI."""
        return f"""
/* =====================================================================
   GLOBAL APPLICATION STYLES
   ===================================================================== */

QMainWindow {{
    background-color: {BabbittTheme.LIGHT_GRAY};
    color: {BabbittTheme.DARK_TEXT};
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
}}

QDialog {{
    background-color: {BabbittTheme.WHITE};
    border: 1px solid {BabbittTheme.BORDER_GRAY};
    border-radius: 8px;
}}

/* =====================================================================
   SIDEBAR - BEAUTIFUL BLUE GRADIENT (MATCHES YOUR SCREENSHOT)
   ===================================================================== */

QFrame#sidebarFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {BabbittTheme.PRIMARY_BLUE}, 
        stop:1 {BabbittTheme.SECONDARY_BLUE});
    border: none;
    min-width: 200px;
    max-width: 200px;
}}

QLabel#logoLabel {{
    color: {BabbittTheme.ACCENT_ORANGE};
    font-size: 24px;
    font-weight: bold;
    padding: 24px 16px;
    margin-bottom: 10px;
    background-color: transparent;
}}

QListWidget#navList {{
    background-color: transparent;
    border: none;
    color: white;
    font-size: 14px;
    outline: none;
    padding: 0;
}}

QListWidget#navList::item {{
    padding: 12px 20px;
    border-left: 3px solid transparent;
    margin: 2px 0;
    border-radius: 0 6px 6px 0;
    margin-right: 8px;
}}

QListWidget#navList::item:hover {{
    background-color: rgba(255, 255, 255, 0.15);
}}

QListWidget#navList::item:selected {{
    background-color: rgba(255, 255, 255, 0.2);
    border-left: 3px solid {BabbittTheme.ACCENT_ORANGE};
    font-weight: 600;
}}

QPushButton#settingsButton {{
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 10px 16px;
    margin: 16px 12px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#settingsButton:hover {{
    background-color: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.4);
}}

/* =====================================================================
   CONTENT AREA - CLEAN PROFESSIONAL LAYOUT
   ===================================================================== */

QFrame#contentAreaFrame {{
    background-color: {BabbittTheme.WHITE};
    border: none;
}}

QFrame#contentHeader {{
    background-color: {BabbittTheme.WHITE};
    border: none;
    border-bottom: 1px solid {BabbittTheme.BORDER_GRAY};
    padding: 20px 24px;
    min-height: 70px;
    max-height: 70px;
}}

QLabel#pageTitle {{
    font-size: 28px;
    font-weight: bold;
    color: {BabbittTheme.PRIMARY_BLUE};
    margin: 0;
    padding: 0;
}}

/* =====================================================================
   BUTTONS - ORANGE ACCENT MATCHING YOUR SCREENSHOTS
   ===================================================================== */

QPushButton {{
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 13px;
    min-height: 32px;
    background-color: {BabbittTheme.CARD_GRAY};
    color: {BabbittTheme.DARK_TEXT};
}}

QPushButton:hover {{
    background-color: {BabbittTheme.BORDER_GRAY};
}}

QPushButton[class="primary"], QPushButton[text*="Add"], QPushButton[text*="New"], QPushButton[text*="Configure"] {{
    background-color: {BabbittTheme.ACCENT_ORANGE};
    color: white;
    font-weight: 600;
    min-height: 36px;
    padding: 10px 20px;
}}

QPushButton[class="primary"]:hover, QPushButton[text*="Add"]:hover, QPushButton[text*="New"]:hover, QPushButton[text*="Configure"]:hover {{
    background-color: {BabbittTheme.LIGHT_ORANGE};
}}

QPushButton[text*="Save"], QPushButton[text*="Generate"], QPushButton[text*="Send"] {{
    background-color: {BabbittTheme.SUCCESS_GREEN};
    color: white;
    font-weight: 600;
}}

QPushButton[text*="Save"]:hover, QPushButton[text*="Generate"]:hover, QPushButton[text*="Send"]:hover {{
    background-color: #218838;
}}

/* =====================================================================
   CARDS AND PANELS - MATCHING YOUR MODAL DESIGN
   ===================================================================== */

QFrame[frameType="card"], QGroupBox {{
    background-color: {BabbittTheme.WHITE};
    border: 1px solid {BabbittTheme.BORDER_GRAY};
    border-radius: 8px;
    padding: 16px;
    margin: 4px;
}}

QGroupBox::title {{
    color: {BabbittTheme.DARK_TEXT};
    font-weight: 600;
    font-size: 14px;
    padding: 4px 8px;
    margin-left: 8px;
}}

/* =====================================================================
   FORM INPUTS - CLEAN AND PROFESSIONAL
   ===================================================================== */

QLineEdit, QTextEdit, QPlainTextEdit {{
    border: 1px solid {BabbittTheme.BORDER_GRAY};
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 13px;
    background-color: {BabbittTheme.WHITE};
    min-height: 20px;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {BabbittTheme.ACCENT_ORANGE};
    outline: none;
}}

QComboBox {{
    border: 1px solid {BabbittTheme.BORDER_GRAY};
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
    background-color: {BabbittTheme.WHITE};
    min-height: 24px;
    max-height: 36px;
}}

QComboBox:focus {{
    border-color: {BabbittTheme.ACCENT_ORANGE};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
    background: {BabbittTheme.GRAY_TEXT};
}}

QComboBox QAbstractItemView {{
    border: 1px solid {BabbittTheme.BORDER_GRAY};
    border-radius: 4px;
    background-color: {BabbittTheme.WHITE};
    selection-background-color: {BabbittTheme.ACCENT_ORANGE};
    selection-color: white;
    padding: 4px;
}}

/* =====================================================================
   TABLES - MATCHING YOUR QUOTE TABLE DESIGN
   ===================================================================== */

QTableWidget, QTableView {{
    background-color: {BabbittTheme.WHITE};
    border: 1px solid {BabbittTheme.BORDER_GRAY};
    border-radius: 6px;
    gridline-color: {BabbittTheme.BORDER_GRAY};
    font-size: 13px;
}}

QTableWidget::item, QTableView::item {{
    padding: 8px 12px;
    border-bottom: 1px solid {BabbittTheme.BORDER_GRAY};
}}

QHeaderView::section {{
    background-color: {BabbittTheme.CARD_GRAY};
    color: {BabbittTheme.DARK_TEXT};
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid {BabbittTheme.BORDER_GRAY};
    font-weight: 600;
    font-size: 13px;
}}

/* =====================================================================
   LABELS AND TEXT - PROFESSIONAL TYPOGRAPHY
   ===================================================================== */

QLabel {{
    color: {BabbittTheme.DARK_TEXT};
    font-size: 13px;
}}

QLabel[labelType="title"] {{
    font-size: 18px;
    font-weight: bold;
    color: {BabbittTheme.PRIMARY_BLUE};
    margin-bottom: 8px;
}}

QLabel[labelType="subtitle"] {{
    font-size: 15px;
    font-weight: 600;
    color: {BabbittTheme.DARK_TEXT};
    margin-bottom: 6px;
}}

QLabel[labelType="caption"] {{
    font-size: 12px;
    color: {BabbittTheme.GRAY_TEXT};
}}

QLabel[priceType="total"] {{
    font-size: 16px;
    font-weight: bold;
    color: {BabbittTheme.SUCCESS_GREEN};
}}

/* =====================================================================
   SCROLLBARS - SUBTLE AND CLEAN
   ===================================================================== */

QScrollBar:vertical {{
    background-color: {BabbittTheme.CARD_GRAY};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {BabbittTheme.BORDER_GRAY};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {BabbittTheme.GRAY_TEXT};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* =====================================================================
   MODAL DIALOGS - MATCHING YOUR PRODUCT SELECTION MODAL
   ===================================================================== */

QDialog QLabel {{
    color: {BabbittTheme.DARK_TEXT};
}}

QDialog QPushButton {{
    min-width: 80px;
}}

QDialog QFrame {{
    background-color: transparent;
}}

/* Progress indicators for your 3-step process */
QLabel[objectName*="step"] {{
    background-color: {BabbittTheme.BORDER_GRAY};
    color: {BabbittTheme.GRAY_TEXT};
    border-radius: 16px;
    padding: 8px 12px;
    font-weight: 600;
    font-size: 12px;
}}

QLabel[objectName*="step"][active="true"] {{
    background-color: {BabbittTheme.ACCENT_ORANGE};
    color: white;
}}

/* =====================================================================
   STATUS INDICATORS
   ===================================================================== */

QLabel[status="Draft"] {{
    background-color: {BabbittTheme.WARNING_ORANGE};
    color: white;
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
}}

QLabel[status="Sent"] {{
    background-color: {BabbittTheme.SUCCESS_GREEN};
    color: white;
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
}}
"""

    @staticmethod
    def get_application_stylesheet():
        """Alias for get_main_stylesheet for compatibility with ui_integration.py."""
        return BabbittTheme.get_main_stylesheet()

    @staticmethod
    def get_card_style(elevated: bool = False):
        """Get card styling for frames and group boxes."""
        if elevated:
            return f"""
                QFrame {{
                    background-color: {BabbittTheme.WHITE};
                    border: 1px solid {BabbittTheme.BORDER_GRAY};
                    border-radius: 8px;
                    padding: 16px;
                    margin: 4px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
            """
        else:
            return f"""
                QFrame {{
                    background-color: {BabbittTheme.WHITE};
                    border: 1px solid {BabbittTheme.BORDER_GRAY};
                    border-radius: 8px;
                    padding: 16px;
                    margin: 4px;
                }}
            """

    @staticmethod
    def get_modern_form_spacing():
        """Get modern form spacing values."""
        return {
            'section_spacing': 16,
            'field_spacing': 8,
            'card_padding': 16,
            'button_spacing': 12
        }

    @staticmethod
    def apply_modern_theme(app):
        """Apply the modern theme to the application."""
        app.setStyleSheet(BabbittTheme.get_main_stylesheet())