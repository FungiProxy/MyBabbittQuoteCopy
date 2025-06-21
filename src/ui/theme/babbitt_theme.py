"""
Working Babbitt Theme - Complete Professional Styling

This file contains the complete, working theme that will immediately restore
your beautiful professional interface. Replace your existing theme file entirely.

File: src/ui/theme/babbitt_theme.py (REPLACE COMPLETELY)
"""

class BabbittTheme:
    """Complete working theme for MyBabbittQuote application."""
    
    # Babbitt Brand Colors
    PRIMARY_BLUE = "#2563eb"
    SECONDARY_BLUE = "#1e40af"
    ACCENT_ORANGE = "#ea580c"
    
    # Grays and Neutrals
    BACKGROUND_LIGHT = "#f8fafc"
    BACKGROUND_WHITE = "#ffffff"
    GRAY_50 = "#f9fafb"
    GRAY_100 = "#f3f4f6"
    GRAY_200 = "#e5e7eb"
    GRAY_300 = "#d1d5db"
    GRAY_400 = "#9ca3af"
    GRAY_500 = "#6b7280"
    GRAY_600 = "#4b5563"
    GRAY_800 = "#1f2937"
    GRAY_900 = "#111827"
    LIGHT_GRAY = "#f1f5f9"  # Added for compatibility
    
    # Theme names for compatibility
    CORPORATE_THEME = "Corporate"
    DARK_THEME = "Dark"
    DARK_BG = "#18181b"  # Placeholder for dark background
    
    # Success/Error Colors
    SUCCESS_GREEN = "#059669"
    ERROR_RED = "#dc2626"
    
    @classmethod
    def get_main_stylesheet(cls):
        """Get the complete working stylesheet."""
        return f"""
        /* =====================================================================
           MAIN APPLICATION WINDOW
           ===================================================================== */
        
        QMainWindow {{
            background-color: {cls.BACKGROUND_LIGHT};
            color: {cls.GRAY_800};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}
        
        QWidget {{
            background-color: transparent;
            color: {cls.GRAY_800};
        }}
        
        /* =====================================================================
           BEAUTIFUL BLUE SIDEBAR - RESTORED
           ===================================================================== */
        
        QFrame#sidebarFrame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.PRIMARY_BLUE}, 
                stop:1 {cls.SECONDARY_BLUE});
            border: none;
            min-width: 260px;
            max-width: 260px;
        }}
        
        QLabel#logoLabel {{
            color: {cls.ACCENT_ORANGE};
            font-size: 24px;
            font-weight: 700;
            padding: 24px 20px;
            margin-bottom: 16px;
            background-color: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* NAVIGATION LIST - BEAUTIFUL STYLING */
        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: white;
            font-size: 14px;
            outline: none;
            padding: 16px 12px;
        }}
        
        QListWidget#navList::item {{
            padding: 12px 16px;
            border-left: 3px solid transparent;
            margin: 4px 0;
            border-radius: 0 8px 8px 0;
            margin-right: 12px;
            color: white;
            font-weight: 500;
        }}
        
        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-left: 3px solid rgba(255, 255, 255, 0.5);
        }}
        
        QListWidget#navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.2);
            border-left: 3px solid {cls.ACCENT_ORANGE};
            font-weight: 600;
            color: white;
        }}
        
        /* SETTINGS BUTTON */
        QPushButton#settingsButton {{
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 12px 20px;
            margin: 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QPushButton#settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.2);
        }}
        
        /* =====================================================================
           CONTENT AREA - PROFESSIONAL STYLING
           ===================================================================== */
        
        QFrame#contentAreaFrame {{
            background-color: {cls.BACKGROUND_LIGHT};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background-color: {cls.BACKGROUND_WHITE};
            border-bottom: 1px solid {cls.GRAY_200};
            min-height: 70px;
            max-height: 70px;
            padding: 0px;
        }}
        
        QLabel#pageTitle {{
            color: {cls.GRAY_900};
            font-size: 24px;
            font-weight: 700;
            padding: 0px;
            margin: 0px;
        }}
        
        QLabel[labelType="title"] {{
            color: {cls.GRAY_900};
            font-size: 22px;
            font-weight: 700;
        }}
        
        QLabel[labelType="caption"] {{
            color: {cls.GRAY_500};
            font-size: 14px;
            font-weight: 400;
            padding-top: 4px;
        }}
        
        QLabel[status="Draft"] {{
            background-color: {cls.GRAY_200};
            color: {cls.GRAY_600};
            font-size: 12px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 10px;
            max-width: 50px;
        }}
        
        QLabel[priceType="total"] {{
            color: {cls.GRAY_800};
            font-size: 16px;
            font-weight: 600;
        }}
        
        QLabel[priceType="total-prominent"] {{
            color: {cls.GRAY_900};
            font-size: 28px;
            font-weight: 700;
            margin-top: 4px;
        }}
        
        /* =====================================================================
           STATUS BADGES - DYNAMIC AND CLEAR
           ===================================================================== */
        
        QLabel[status] {{
            font-size: 12px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 12px;
            text-align: center;
            min-width: 60px;
        }}

        QLabel[status="Draft"] {{
            background-color: {cls.GRAY_200};
            color: {cls.GRAY_600};
        }}

        QLabel[status="Sent"] {{
            background-color: #dbeafe; /* Light Blue */
            color: #1e40af; /* Dark Blue */
        }}

        QLabel[status="Confirmed"] {{
            background-color: #dcfce7; /* Light Green */
            color: #166534; /* Dark Green */
        }}

        QLabel[status="Cancelled"] {{
            background-color: #fee2e2; /* Light Red */
            color: #991b1b; /* Dark Red */
        }}
        
        /* =====================================================================
           BEAUTIFUL ORANGE BUTTONS - RESTORED
           ===================================================================== */
        
        QPushButton {{
            background-color: {cls.GRAY_100};
            color: {cls.GRAY_800};
            border: 1px solid {cls.GRAY_300};
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            min-height: 36px;
        }}
        
        QPushButton:hover {{
            background-color: {cls.GRAY_200};
            border-color: {cls.GRAY_400};
        }}
        
        QPushButton[class="primary"] {{
            background-color: {cls.ACCENT_ORANGE};
            color: white;
            border: 1px solid {cls.ACCENT_ORANGE};
            font-weight: 600;
        }}
        
        QPushButton[class="primary"]:hover {{
            background-color: #c2410c;
            border-color: #c2410c;
        }}
        
        /* =====================================================================
           PROFESSIONAL FORM STYLING
           ===================================================================== */
        
        QLineEdit, QTextEdit {{
            background-color: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 14px;
            color: {cls.GRAY_900};
        }}

        QLineEdit {{
            min-height: 20px;
        }}

        QTextEdit {{
            min-height: 80px;
        }}
        
        QLineEdit:hover, QTextEdit:hover {{
            border-color: {cls.GRAY_400};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {cls.PRIMARY_BLUE};
            background-color: #fafbfc;
        }}
        
        QComboBox {{
            background-color: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border-color: {cls.PRIMARY_BLUE};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {cls.GRAY_600};
            margin-right: 10px;
        }}
        
        /* =====================================================================
           DASHBOARD CARDS - BEAUTIFUL STYLING
           ===================================================================== */
        
        QFrame[class="stat-card"] {{
            background-color: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 12px;
            padding: 24px;
            margin: 8px;
            min-height: 120px;
        }}
        
        QLabel[class="stat-value"] {{
            color: {cls.GRAY_900};
            font-size: 32px;
            font-weight: 700;
            margin: 4px 0px;
        }}
        
        QLabel[class="stat-title"] {{
            color: {cls.GRAY_600};
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QLabel[class="stat-subtitle"] {{
            color: {cls.GRAY_500};
            font-size: 12px;
            margin: 2px 0px;
        }}
        
        QLabel[class="stat-icon"] {{
            color: {cls.GRAY_400};
            font-size: 20px;
        }}
        
        /* =====================================================================
           CONTENT SECTIONS
           ===================================================================== */
        
        QFrame[class="content-section"] {{
            background-color: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 12px;
            padding: 24px;
            margin: 16px 24px;
        }}
        
        QLabel[class="section-title"] {{
            color: {cls.GRAY_900};
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 16px;
        }}
        
        /* =====================================================================
           ENHANCED EMPTY STATES
           ===================================================================== */
        
        QLabel[class="empty-state"] {{
            color: {cls.GRAY_500};
            font-size: 14px;
            font-style: italic;
            text-align: center;
            padding: 40px;
        }}
        
        /* =====================================================================
           SCROLLBARS
           ===================================================================== */
        
        QScrollBar:vertical {{
            background-color: {cls.GRAY_100};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.GRAY_300};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.GRAY_400};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        """
    
    @classmethod
    def get_dialog_stylesheet(cls):
        """Stylesheet for dialogs and popups."""
        return f"""
        QDialog {{
            background-color: {cls.BACKGROUND_WHITE};
            color: {cls.GRAY_800};
            border: 1px solid {cls.GRAY_300};
            border-radius: 8px;
        }}
        """