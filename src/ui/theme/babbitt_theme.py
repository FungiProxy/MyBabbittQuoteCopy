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
        """Get the complete working stylesheet with enhanced styling and animations."""
        return f"""
        /* =====================================================================
           CORPORATE THEME - ENHANCED PROFESSIONAL STYLING
           ===================================================================== */
        
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.BACKGROUND_LIGHT},
                stop:1 {cls.GRAY_50});
            color: {cls.GRAY_800};
            font-family: 'Segoe UI', 'Roboto', 'San Francisco', 'Helvetica Neue', sans-serif;
            font-size: 14px;
            font-weight: 400;
        }}
        
        QWidget {{
            background-color: transparent;
            color: {cls.GRAY_800};
        }}
        
        /* =====================================================================
           ENHANCED BLUE SIDEBAR - CORPORATE GRADIENT
           ===================================================================== */
        
        QFrame#sidebarFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.PRIMARY_BLUE},
                stop:0.3 #1e40af,
                stop:0.7 #1d4ed8,
                stop:1 {cls.SECONDARY_BLUE});
            border: none;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 260px;
            max-width: 260px;
        }}
        
        QLabel#logoLabel {{
            color: {cls.ACCENT_ORANGE};
            font-size: 26px;
            font-weight: 700;
            padding: 28px 20px 20px 20px;
            margin-bottom: 8px;
            background: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
            letter-spacing: -0.5px;
        }}
        
        /* ENHANCED NAVIGATION LIST - CORPORATE STYLING */
        QListWidget#navList {{
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.9);
            font-size: 15px;
            font-weight: 500;
            outline: none;
            padding: 8px 0;
        }}
        
        QListWidget#navList::item {{
            padding: 14px 24px 14px 20px;
            margin: 3px 8px 3px 0;
            border-radius: 0 12px 12px 0;
            border-left: 3px solid transparent;
        }}
        
        QListWidget#navList::item:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 255, 255, 0.08),
                stop:1 rgba(255, 255, 255, 0.12));
            color: white;
        }}
        
        QListWidget#navList::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.ACCENT_ORANGE},
                stop:0.8 #ea580c,
                stop:1 rgba(234, 88, 12, 0.8));
            border-left: 3px solid white;
            color: white;
            font-weight: 600;
        }}
        
        /* ENHANCED SETTINGS BUTTON */
        QPushButton#settingsButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.12),
                stop:1 rgba(255, 255, 255, 0.08));
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 12px 20px;
            margin: 16px 12px 20px 12px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QPushButton#settingsButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.18),
                stop:1 rgba(255, 255, 255, 0.14));
            border-color: rgba(255, 255, 255, 0.3);
            color: white;
        }}
        
        QPushButton#settingsButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.08),
                stop:1 rgba(255, 255, 255, 0.04));
        }}
        
        /* =====================================================================
           ENHANCED CONTENT AREA - CORPORATE STYLING
           ===================================================================== */
        
        QFrame#contentAreaFrame {{
            background: {cls.BACKGROUND_WHITE};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.BACKGROUND_WHITE},
                stop:1 {cls.GRAY_50});
            border: none;
            border-bottom: 1px solid {cls.GRAY_200};
            min-height: 70px;
            max-height: 70px;
        }}
        
        QLabel#pageTitle {{
            color: {cls.GRAY_900};
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin: 0;
            padding: 0;
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
        
        /* =====================================================================
           ENHANCED BUTTONS - CORPORATE STYLING
           ===================================================================== */
        
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.GRAY_100},
                stop:1 {cls.GRAY_200});
            color: {cls.GRAY_800};
            border: 1px solid {cls.GRAY_300};
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-height: 40px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.GRAY_200},
                stop:1 {cls.GRAY_300});
            border-color: {cls.GRAY_400};
            color: {cls.GRAY_900};
        }}
        
        QPushButton[class="primary"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.ACCENT_ORANGE},
                stop:1 #c2410c);
            color: white;
            border: 1px solid {cls.ACCENT_ORANGE};
            font-weight: 600;
        }}
        
        QPushButton[class="primary"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ea580c,
                stop:1 #dc2626);
            border-color: #ea580c;
        }}
        
        QPushButton[class="primary"]:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #c2410c,
                stop:1 #ea580c);
        }}
        
        /* =====================================================================
           ENHANCED FORM STYLING - CORPORATE
           ===================================================================== */
        
        QLineEdit, QTextEdit {{
            background: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {cls.GRAY_900};
        }}

        QLineEdit {{
            min-height: 24px;
        }}

        QTextEdit {{
            min-height: 80px;
        }}
        
        QLineEdit:hover, QTextEdit:hover {{
            border-color: {cls.GRAY_400};
            background: {cls.GRAY_50};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {cls.PRIMARY_BLUE};
            background: #f8fafc;
        }}
        
        QComboBox {{
            background: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 14px;
            min-height: 24px;
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
           ENHANCED DASHBOARD CARDS - CORPORATE STYLING
           ===================================================================== */
        
        QFrame[class="stat-card"] {{
            background: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 16px;
            padding: 28px;
            margin: 8px;
            min-height: 140px;
        }}
        
        QLabel[class="stat-value"] {{
            color: {cls.GRAY_900};
            font-size: 36px;
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

    @staticmethod
    def get_stylesheet(theme_name: str) -> str:
        """Return the correct stylesheet for the given theme name."""
        if theme_name == BabbittTheme.DARK_THEME:
            return BabbittTheme.get_dark_stylesheet()
        # Default to corporate theme
        return BabbittTheme.get_main_stylesheet()
    
    @classmethod
    def get_dark_stylesheet(cls):
        """Get the complete dark theme stylesheet with enhanced styling."""
        return f"""
        /* =====================================================================
           DARK THEME - ENHANCED DARK MODE STYLING
           ===================================================================== */
        
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.DARK_BG},
                stop:1 #0f0f23);
            color: #e5e7eb;
            font-family: 'Segoe UI', 'Roboto', 'San Francisco', 'Helvetica Neue', sans-serif;
            font-size: 14px;
            font-weight: 400;
        }}
        
        QWidget {{
            background-color: transparent;
            color: #e5e7eb;
        }}
        
        /* =====================================================================
           ENHANCED DARK SIDEBAR - SOPHISTICATED GRADIENT
           ===================================================================== */
        
        QFrame#sidebarFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1f2937,
                stop:0.3 #111827,
                stop:0.7 #0f172a,
                stop:1 #020617);
            border: none;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 260px;
            max-width: 260px;
        }}
        
        QLabel#logoLabel {{
            color: {cls.ACCENT_ORANGE};
            font-size: 26px;
            font-weight: 700;
            padding: 28px 20px 20px 20px;
            margin-bottom: 8px;
            background: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
            letter-spacing: -0.5px;
        }}
        
        /* ENHANCED NAVIGATION LIST - DARK STYLING */
        QListWidget#navList {{
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.9);
            font-size: 15px;
            font-weight: 500;
            outline: none;
            padding: 8px 0;
        }}
        
        QListWidget#navList::item {{
            padding: 14px 24px 14px 20px;
            margin: 3px 8px 3px 0;
            border-radius: 0 12px 12px 0;
            border-left: 3px solid transparent;
        }}
        
        QListWidget#navList::item:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 255, 255, 0.08),
                stop:1 rgba(255, 255, 255, 0.12));
            color: white;
        }}
        
        QListWidget#navList::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.ACCENT_ORANGE},
                stop:0.8 #ea580c,
                stop:1 rgba(234, 88, 12, 0.8));
            border-left: 3px solid white;
            color: white;
            font-weight: 600;
        }}
        
        /* ENHANCED SETTINGS BUTTON - DARK */
        QPushButton#settingsButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.12),
                stop:1 rgba(255, 255, 255, 0.08));
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 12px 20px;
            margin: 16px 12px 20px 12px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QPushButton#settingsButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.18),
                stop:1 rgba(255, 255, 255, 0.14));
            border-color: rgba(255, 255, 255, 0.3);
            color: white;
        }}
        
        QPushButton#settingsButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.08),
                stop:1 rgba(255, 255, 255, 0.04));
        }}
        
        /* =====================================================================
           ENHANCED DARK CONTENT AREA
           ===================================================================== */
        
        QFrame#contentAreaFrame {{
            background: {cls.DARK_BG};
            border: none;
        }}
        
        QFrame#contentHeader {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1f2937,
                stop:1 #111827);
            border: none;
            border-bottom: 1px solid #374151;
            min-height: 70px;
            max-height: 70px;
        }}
        
        QLabel#pageTitle {{
            color: #f9fafb;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin: 0;
            padding: 0;
        }}
        
        QLabel[labelType="title"] {{
            color: #f9fafb;
            font-size: 22px;
            font-weight: 700;
        }}
        
        QLabel[labelType="caption"] {{
            color: #9ca3af;
            font-size: 14px;
            font-weight: 400;
            padding-top: 4px;
        }}
        
        /* =====================================================================
           ENHANCED DARK BUTTONS
           ===================================================================== */
        
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #374151,
                stop:1 #4b5563);
            color: #e5e7eb;
            border: 1px solid #4b5563;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-height: 40px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4b5563,
                stop:1 #6b7280);
            border-color: #6b7280;
            color: white;
        }}
        
        QPushButton[class="primary"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.ACCENT_ORANGE},
                stop:1 #c2410c);
            color: white;
            border: 1px solid {cls.ACCENT_ORANGE};
            font-weight: 600;
        }}
        
        QPushButton[class="primary"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ea580c,
                stop:1 #dc2626);
            border-color: #ea580c;
        }}
        
        QPushButton[class="primary"]:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #c2410c,
                stop:1 #ea580c);
        }}
        
        /* =====================================================================
           ENHANCED DARK FORM STYLING
           ===================================================================== */
        
        QLineEdit, QTextEdit {{
            background: #1f2937;
            border: 2px solid #374151;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #f9fafb;
        }}

        QLineEdit {{
            min-height: 24px;
        }}

        QTextEdit {{
            min-height: 80px;
        }}
        
        QLineEdit:hover, QTextEdit:hover {{
            border-color: #4b5563;
            background: #111827;
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {cls.PRIMARY_BLUE};
            background: #0f172a;
        }}
        
        QComboBox {{
            background: #1f2937;
            border: 2px solid #374151;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 14px;
            min-height: 24px;
            color: #f9fafb;
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
            border-top: 5px solid #9ca3af;
            margin-right: 10px;
        }}
        
        /* =====================================================================
           ENHANCED DARK DASHBOARD CARDS
           ===================================================================== */
        
        QFrame[class="stat-card"] {{
            background: #1f2937;
            border: 1px solid #374151;
            border-radius: 16px;
            padding: 28px;
            margin: 8px;
            min-height: 140px;
        }}
        
        QLabel[class="stat-value"] {{
            color: #f9fafb;
            font-size: 36px;
            font-weight: 700;
            margin: 4px 0px;
        }}
        
        QLabel[class="stat-title"] {{
            color: #9ca3af;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QLabel[class="stat-subtitle"] {{
            color: #6b7280;
            font-size: 12px;
            margin: 2px 0px;
        }}
        
        QLabel[class="stat-icon"] {{
            color: #6b7280;
            font-size: 24px;
        }}
        
        /* =====================================================================
           ENHANCED DARK CONTENT SECTIONS
           ===================================================================== */
        
        QFrame[class="content-section"] {{
            background: #1f2937;
            border: 1px solid #374151;
            border-radius: 16px;
            padding: 28px;
            margin: 16px 24px;
        }}
        
        QLabel[class="section-title"] {{
            color: #f9fafb;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 16px;
        }}
        
        /* =====================================================================
           ENHANCED DARK EMPTY STATES
           ===================================================================== */
        
        QLabel[class="empty-state"] {{
            color: #6b7280;
            font-size: 14px;
            font-style: italic;
            text-align: center;
            padding: 40px;
        }}
        
        /* =====================================================================
           ENHANCED DARK SCROLLBARS
           ===================================================================== */
        
        QScrollBar:vertical {{
            background: #374151;
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background: #4b5563;
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: #6b7280;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        """