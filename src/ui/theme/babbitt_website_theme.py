"""
Babbitt Website Theme - Cloned from babbittinternational.com

This theme replicates the look and feel of the official Babbitt International
website, featuring a clean, professional, and modern design.

File: src/ui/theme/babbitt_website_theme.py
"""

class BabbittWebsiteTheme:
    """Theme based on the official Babbitt International website."""
    
    # --- Website Color Palette ---
    # Primary blue for branding, buttons, and links
    PRIMARY_BLUE = "#007BFF" 
    # Darker blue for hover states
    PRIMARY_BLUE_HOVER = "#0056b3"
    # Standard text color
    TEXT_PRIMARY = "#212529"
    # Secondary, lighter text
    TEXT_SECONDARY = "#6c757d"
    
    # --- Greys & Neutrals ---
    BACKGROUND_MAIN = "#ffffff"
    # A very light grey for content area backgrounds or sidebars
    BACKGROUND_ALT = "#f8f9fa" 
    BORDER_COLOR = "#dee2e6"
    
    # --- Semantic Colors ---
    SUCCESS_GREEN = "#28a745"
    ERROR_RED = "#dc3545"

    @classmethod
    def get_main_stylesheet(cls):
        """Returns the full stylesheet for the application."""
        return f"""
        /* =====================================================================
           MAIN APPLICATION WINDOW & DEFAULTS
           ===================================================================== */
        
        QMainWindow, QWidget {{
            font-family: Arial, sans-serif;
            font-size: 14px;
            background-color: {cls.BACKGROUND_ALT};
            color: {cls.TEXT_PRIMARY};
        }}

        /* =====================================================================
           SIDEBAR - Clean & Professional
           ===================================================================== */
        
        QFrame#sidebarFrame {{
            background-color: {cls.BACKGROUND_ALT};
            border-right: 1px solid {cls.BORDER_COLOR};
            min-width: 260px;
            max-width: 260px;
        }}
        
        QLabel#logoLabel {{
            color: {cls.PRIMARY_BLUE};
            font-size: 24px;
            font-weight: 700;
            padding: 24px 20px;
            margin-bottom: 16px;
            background-color: transparent;
            border-bottom: 1px solid {cls.BORDER_COLOR};
        }}
        
        /* NAVIGATION LIST */
        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: {cls.TEXT_PRIMARY};
            font-size: 14px;
            outline: none;
            padding: 16px 12px;
        }}
        
        QListWidget#navList::item {{
            padding: 12px 16px;
            border-left: 3px solid transparent;
            margin: 4px 0;
            border-radius: 4px;
            margin-right: 12px;
            color: {cls.TEXT_PRIMARY};
            font-weight: 500;
        }}
        
        QListWidget#navList::item:hover {{
            background-color: {cls.BORDER_COLOR};
        }}
        
        QListWidget#navList::item:selected {{
            background-color: {cls.PRIMARY_BLUE};
            border-left: 3px solid {cls.PRIMARY_BLUE};
            color: white;
            font-weight: 600;
        }}
        
        /* SETTINGS BUTTON */
        QPushButton#settingsButton {{
            background-color: transparent;
            color: {cls.TEXT_SECONDARY};
            border: 1px solid {cls.BORDER_COLOR};
            padding: 10px 20px;
            margin: 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QPushButton#settingsButton:hover {{
            background-color: {cls.BORDER_COLOR};
            color: {cls.TEXT_PRIMARY};
        }}
        
        /* =====================================================================
           CONTENT AREA
           ===================================================================== */
        
        QFrame#contentAreaFrame {{
            background-color: {cls.BACKGROUND_MAIN};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background-color: {cls.BACKGROUND_MAIN};
            border-bottom: 1px solid {cls.BORDER_COLOR};
            min-height: 70px;
            max-height: 70px;
            padding: 0 24px;
        }}
        
        QLabel#pageTitle {{
            color: {cls.TEXT_PRIMARY};
            font-size: 24px;
            font-weight: 700;
        }}
        
        /* =====================================================================
           GENERAL WIDGET STYLING
           ===================================================================== */
        
        /* --- Buttons --- */
        QPushButton {{
            background-color: {cls.BACKGROUND_ALT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            min-height: 36px;
        }}
        
        QPushButton:hover {{
            background-color: #e2e6ea;
            border-color: #dae0e5;
        }}
        
        QPushButton[class="primary"] {{
            background-color: {cls.PRIMARY_BLUE};
            color: white;
            border: 1px solid {cls.PRIMARY_BLUE};
            font-weight: 600;
        }}
        
        QPushButton[class="primary"]:hover {{
            background-color: {cls.PRIMARY_BLUE_HOVER};
            border-color: {cls.PRIMARY_BLUE_HOVER};
        }}

        /* --- Text Inputs, Combos --- */
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {cls.BACKGROUND_MAIN};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }}

        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border-color: {cls.PRIMARY_BLUE};
            outline: none;
        }}
        
        QComboBox::drop-down {{
            border: none;
        }}

        QComboBox::down-arrow {{
            image: url(placeholder_for_arrow_icon.png); /* Needs a real icon */
        }}
        
        /* --- Tables --- */
        QTableView {{
            background-color: {cls.BACKGROUND_MAIN};
            border: 1px solid {cls.BORDER_COLOR};
            gridline-color: {cls.BORDER_COLOR};
            border-radius: 8px;
        }}

        QHeaderView::section {{
            background-color: {cls.BACKGROUND_ALT};
            color: {cls.TEXT_PRIMARY};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {cls.BORDER_COLOR};
            font-weight: 600;
        }}

        QTableView::item {{
            padding: 10px;
            border-bottom: 1px solid {cls.BORDER_COLOR};
        }}
        
        /* --- Labels & Misc --- */
        QLabel[labelType="title"] {{
            color: {cls.TEXT_PRIMARY};
            font-size: 22px;
            font-weight: 700;
        }}
        
        QLabel[labelType="caption"] {{
            color: {cls.TEXT_SECONDARY};
            font-size: 14px;
            font-weight: 400;
            padding-top: 4px;
        }}
        
        QLabel[priceType="total-prominent"] {{
            color: {cls.TEXT_PRIMARY};
            font-size: 28px;
            font-weight: 700;
        }}

        /* Status Badges */
        QLabel[status] {{
            font-size: 12px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 12px;
            text-align: center;
        }}

        QLabel[status="Draft"] {{
            background-color: #e9ecef;
            color: #495057;
        }}

        QLabel[status="Sent"] {{
            background-color: #cfe2ff;
            color: #004085;
        }}

        QLabel[status="Confirmed"] {{
            background-color: #d4edda;
            color: #155724;
        }}

        QLabel[status="Cancelled"] {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        """

    @classmethod
    def get_dialog_stylesheet(cls):
        """Returns a consistent stylesheet for dialog boxes."""
        return f"""
        QDialog {{
            background-color: {cls.BACKGROUND_MAIN};
            color: {cls.TEXT_PRIMARY};
            font-family: Arial, sans-serif;
        }}
        
        QLabel {{
            color: {cls.TEXT_PRIMARY};
        }}
        
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {cls.BACKGROUND_MAIN};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            border-radius: 6px;
            padding: 8px 12px;
        }}
        
        QPushButton {{
            background-color: {cls.BACKGROUND_ALT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_COLOR};
            padding: 10px 20px;
            border-radius: 6px;
            min-height: 36px;
        }}
        
        QPushButton:hover {{
            background-color: #e2e6ea;
        }}
        
        QPushButton[class="primary"] {{
            background-color: {cls.PRIMARY_BLUE};
            color: white;
            border: none;
        }}
        
        QPushButton[class="primary"]:hover {{
            background-color: {cls.PRIMARY_BLUE_HOVER};
        }}
        """ 