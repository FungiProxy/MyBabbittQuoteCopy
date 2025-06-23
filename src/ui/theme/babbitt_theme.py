"""
Enhanced Babbitt Theme - Modern Professional Styling

Enhanced professional styling with modern spacing, improved typography,
and better visual hierarchy while maintaining all existing functionality.

File: src/ui/theme/babbitt_theme.py (ENHANCED VERSION)
"""

class BabbittTheme:
    """Enhanced working theme for MyBabbittQuote application."""
    
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
    GRAY_700 = "#374151"
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
        """Get the enhanced working stylesheet with modern styling and animations."""
        return f"""
        /* =====================================================================
           ENHANCED CORPORATE THEME - MODERN PROFESSIONAL STYLING
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
           ENHANCED BLUE SIDEBAR - MODERN GRADIENT
           ===================================================================== */
        
        QFrame#sidebarFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.PRIMARY_BLUE}, 
                stop:0.3 #1e40af,
                stop:0.7 #1d4ed8,
                stop:1 {cls.SECONDARY_BLUE});
            border: none;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 280px;
            max-width: 280px;
        }}
        
        QLabel#logoLabel {{
            color: {cls.ACCENT_ORANGE};
            font-size: 28px;
            font-weight: 700;
            padding: 32px 20px 24px 20px;
            margin-bottom: 12px;
            background: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
            letter-spacing: -0.5px;
        }}
        
        /* ENHANCED NAVIGATION LIST - MODERN STYLING */
        QListWidget#navList {{
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            font-weight: 500;
            outline: none;
            padding: 12px 0;
        }}
        
        QListWidget#navList::item {{
            padding: 16px 28px 16px 24px;
            margin: 4px 12px 4px 0;
            border-radius: 0 14px 14px 0;
            border-left: 4px solid transparent;
        }}
        
        QListWidget#navList::item:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 255, 255, 0.1),
                stop:1 rgba(255, 255, 255, 0.15));
            color: white;
        }}
        
        QListWidget#navList::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.ACCENT_ORANGE},
                stop:0.8 #ea580c,
                stop:1 rgba(234, 88, 12, 0.8));
            border-left: 4px solid white;
            color: white;
            font-weight: 600;
        }}
        
        /* ENHANCED SETTINGS BUTTON */
        QPushButton#settingsButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.15),
                stop:1 rgba(255, 255, 255, 0.1));
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 10px;
            padding: 14px 24px;
            margin: 20px 16px 24px 16px;
            font-size: 15px;
            font-weight: 500;
        }}
        
        QPushButton#settingsButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.2),
                stop:1 rgba(255, 255, 255, 0.16));
            border-color: rgba(255, 255, 255, 0.35);
            color: white;
        }}
        
        QPushButton#settingsButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.1),
                stop:1 rgba(255, 255, 255, 0.06));
        }}
        
        /* =====================================================================
           ENHANCED CONTENT AREA - MODERN STYLING
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
            min-height: 80px;
            max-height: 80px;
        }}
        
        QLabel#pageTitle {{
            color: {cls.GRAY_900};
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin: 0;
            padding: 0;
        }}
        
        QLabel[labelType="title"] {{
            color: {cls.GRAY_900};
            font-size: 24px;
            font-weight: 700;
        }}
        
        QLabel[labelType="caption"] {{
            color: {cls.GRAY_500};
            font-size: 15px;
            font-weight: 400;
            padding-top: 6px;
        }}
        
        /* =====================================================================
           ENHANCED BUTTONS - MODERN STYLING
           ===================================================================== */
        
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.GRAY_100},
                stop:1 {cls.GRAY_200});
            color: {cls.GRAY_700};
            border: 1px solid {cls.GRAY_300};
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 500;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.GRAY_200},
                stop:1 {cls.GRAY_300});
            border-color: {cls.GRAY_400};
            color: {cls.GRAY_800};
        }}
        
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.GRAY_300},
                stop:1 {cls.GRAY_400});
            border-color: {cls.GRAY_500};
        }}
        
        QPushButton:disabled {{
            background: {cls.GRAY_100};
            color: {cls.GRAY_400};
            border-color: {cls.GRAY_200};
        }}
        
        /* ENHANCED PRIMARY BUTTON */
        QPushButton[class="primary"], QPushButton#primaryActionButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.ACCENT_ORANGE},
                stop:1 #ea580c);
            color: white;
            border: 1px solid {cls.ACCENT_ORANGE};
            border-radius: 10px;
            padding: 14px 24px;
            font-size: 15px;
            font-weight: 600;
            min-height: 24px;
        }}
        
        QPushButton[class="primary"]:hover, QPushButton#primaryActionButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ea580c,
                stop:1 #dc2626);
            border-color: #dc2626;
        }}
        
        QPushButton[class="primary"]:pressed, QPushButton#primaryActionButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #dc2626,
                stop:1 #b91c1c);
        }}
        
        /* =====================================================================
           ENHANCED FORM ELEMENTS - MODERN STYLING
           ===================================================================== */
        
        QLineEdit {{
            background: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {cls.GRAY_800};
            selection-background-color: {cls.PRIMARY_BLUE};
        }}
        
        QLineEdit:focus {{
            border-color: {cls.PRIMARY_BLUE};
            background: {cls.BACKGROUND_WHITE};
        }}
        
        QLineEdit:hover {{
            border-color: {cls.GRAY_300};
        }}
        
        QLineEdit:disabled {{
            background: {cls.GRAY_100};
            color: {cls.GRAY_500};
            border-color: {cls.GRAY_200};
        }}
        
        QTextEdit {{
            background: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {cls.GRAY_800};
            selection-background-color: {cls.PRIMARY_BLUE};
        }}
        
        QTextEdit:focus {{
            border-color: {cls.PRIMARY_BLUE};
        }}
        
        QTextEdit:hover {{
            border-color: {cls.GRAY_300};
        }}
        
        QComboBox {{
            background: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {cls.GRAY_800};
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border-color: {cls.PRIMARY_BLUE};
        }}
        
        QComboBox:hover {{
            border-color: {cls.GRAY_300};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {cls.GRAY_500};
            margin-right: 8px;
        }}
        
        QComboBox QAbstractItemView {{
            background: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.PRIMARY_BLUE};
            border-radius: 8px;
            selection-background-color: {cls.PRIMARY_BLUE};
            selection-color: white;
        }}
        
        /* =====================================================================
           ENHANCED TABLES - MODERN STYLING
           ===================================================================== */
        
        QTableWidget {{
            background: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 8px;
            gridline-color: {cls.GRAY_100};
            selection-background-color: {cls.PRIMARY_BLUE};
            selection-color: white;
        }}
        
        QTableWidget::item {{
            padding: 12px 16px;
            border-bottom: 1px solid {cls.GRAY_100};
        }}
        
        QTableWidget::item:selected {{
            background: {cls.PRIMARY_BLUE};
            color: white;
        }}
        
        QHeaderView::section {{
            background: {cls.GRAY_50};
            color: {cls.GRAY_700};
            padding: 16px 20px;
            border: none;
            border-bottom: 2px solid {cls.GRAY_200};
            font-weight: 600;
            font-size: 14px;
        }}
        
        QHeaderView::section:hover {{
            background: {cls.GRAY_100};
        }}
        
        /* =====================================================================
           ENHANCED SCROLLBARS - MODERN STYLING
           ===================================================================== */
        
        QScrollBar:vertical {{
            background: {cls.GRAY_100};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: {cls.GRAY_300};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {cls.GRAY_400};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background: {cls.GRAY_100};
            height: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {cls.GRAY_300};
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {cls.GRAY_400};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* =====================================================================
           ENHANCED DIALOGS - MODERN STYLING
           ===================================================================== */
        
        QDialog {{
            background: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 12px;
        }}
        
        QDialog QLabel {{
            color: {cls.GRAY_800};
            font-size: 14px;
        }}
        
        QDialog QPushButton {{
            margin: 4px;
        }}
        
        /* =====================================================================
           ENHANCED MESSAGE BOXES - MODERN STYLING
           ===================================================================== */
        
        QMessageBox {{
            background: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 12px;
        }}
        
        QMessageBox QLabel {{
            color: {cls.GRAY_800};
            font-size: 14px;
        }}
        
        QMessageBox QPushButton {{
            margin: 4px;
        }}
        
        /* =====================================================================
           ENHANCED PLACEHOLDER PAGES - MODERN STYLING
           ===================================================================== */
        
        QWidget#placeholderPage {{
            background: {cls.BACKGROUND_WHITE};
        }}
        
        QLabel#pageSubtitle {{
            color: {cls.GRAY_500};
            font-size: 16px;
            font-weight: 400;
        }}
        
        /* =====================================================================
           ENHANCED CONTENT STACKED WIDGET - MODERN STYLING
           ===================================================================== */
        
        QStackedWidget#contentStackedWidget {{
            background: {cls.BACKGROUND_WHITE};
            border: none;
        }}
        
        /* =====================================================================
           ENHANCED GROUP BOXES - MODERN STYLING
           ===================================================================== */
        
        QGroupBox {{
            font-weight: 600;
            font-size: 16px;
            color: {cls.GRAY_800};
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            margin-top: 16px;
            padding-top: 16px;
            background: {cls.BACKGROUND_WHITE};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 8px;
            background: {cls.BACKGROUND_WHITE};
        }}
        
        /* =====================================================================
           ENHANCED CHECKBOXES - MODERN STYLING
           ===================================================================== */
        
        QCheckBox {{
            spacing: 8px;
            color: {cls.GRAY_800};
            font-size: 14px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {cls.GRAY_300};
            border-radius: 4px;
            background: {cls.BACKGROUND_WHITE};
        }}
        
        QCheckBox::indicator:checked {{
            background: {cls.PRIMARY_BLUE};
            border-color: {cls.PRIMARY_BLUE};
        }}
        
        QCheckBox::indicator:checked::after {{
            content: "✓";
            color: white;
            font-weight: bold;
            font-size: 12px;
        }}
        
        /* =====================================================================
           ENHANCED RADIO BUTTONS - MODERN STYLING
           ===================================================================== */
        
        QRadioButton {{
            spacing: 8px;
            color: {cls.GRAY_800};
            font-size: 14px;
        }}
        
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {cls.GRAY_300};
            border-radius: 9px;
            background: {cls.BACKGROUND_WHITE};
        }}
        
        QRadioButton::indicator:checked {{
            background: {cls.PRIMARY_BLUE};
            border-color: {cls.PRIMARY_BLUE};
        }}
        
        QRadioButton::indicator:checked::after {{
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 4px;
            background: white;
            margin: 3px;
        }}
        
        /* =====================================================================
           ENHANCED SPINBOXES - MODERN STYLING
           ===================================================================== */
        
        QSpinBox {{
            background: {cls.BACKGROUND_WHITE};
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {cls.GRAY_800};
        }}
        
        QSpinBox:focus {{
            border-color: {cls.PRIMARY_BLUE};
        }}
        
        QSpinBox:hover {{
            border-color: {cls.GRAY_300};
        }}
        
        QSpinBox::up-button, QSpinBox::down-button {{
            background: {cls.GRAY_100};
            border: none;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
            background: {cls.GRAY_200};
        }}
        
        /* =====================================================================
           ENHANCED PROGRESS BARS - MODERN STYLING
           ===================================================================== */
        
        QProgressBar {{
            border: 2px solid {cls.GRAY_200};
            border-radius: 8px;
            background: {cls.GRAY_100};
            text-align: center;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.PRIMARY_BLUE},
                stop:1 {cls.SECONDARY_BLUE});
            border-radius: 6px;
        }}
        
        /* =====================================================================
           ENHANCED TOOLTIPS - MODERN STYLING
           ===================================================================== */
        
        QToolTip {{
            background: {cls.GRAY_800};
            color: white;
            border: 1px solid {cls.GRAY_600};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        /* =====================================================================
           ENHANCED MENUS - MODERN STYLING
           ===================================================================== */
        
        QMenu {{
            background: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 16px;
            border-radius: 4px;
            color: {cls.GRAY_800};
        }}
        
        QMenu::item:selected {{
            background: {cls.PRIMARY_BLUE};
            color: white;
        }}
        
        QMenu::separator {{
            height: 1px;
            background: {cls.GRAY_200};
            margin: 4px 8px;
        }}

        /* =====================================================================
           ENHANCED CUSTOMER PAGE - MODERN STYLING
           ===================================================================== */

        QTableWidget#customersTable {{
            alternate-background-color: {cls.GRAY_50};
            border: 1px solid {cls.GRAY_200};
            border-radius: 8px;
        }}

        QFrame#detailsCard {{
            background-color: {cls.BACKGROUND_WHITE};
            border: 1px solid {cls.GRAY_200};
            border-radius: 12px;
        }}

        QLabel#detailsTitle {{
            font-size: 20px;
            font-weight: 600;
            color: {cls.GRAY_800};
            padding-bottom: 8px;
            border-bottom: 1px solid {cls.GRAY_200};
        }}

        QScrollArea#detailsScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QWidget#detailsScrollContent {{
            background-color: transparent;
        }}

        QLabel#detailLabel {{
            font-size: 12px;
            font-weight: 600;
            color: {cls.GRAY_500};
            text-transform: uppercase;
        }}

        QLabel#detailValue {{
            font-size: 15px;
            font-weight: 400;
            color: {cls.GRAY_800};
            padding: 4px 0;
        }}
        
        QTextEdit#detailValueNotes {{
            font-size: 14px;
            color: {cls.GRAY_800};
            background-color: {cls.GRAY_50};
            border: 1px solid {cls.GRAY_200};
            border-radius: 6px;
            padding: 8px;
        }}

        /* --- Placeholder Styles --- */
        QWidget#detailsPlaceholder {{
            background-color: transparent;
        }}

        QLabel#placeholderIcon {{
            font-size: 48px;
            color: {cls.GRAY_300};
        }}

        QLabel#placeholderText {{
            font-size: 18px;
            font-weight: 500;
            color: {cls.GRAY_600};
        }}

        QLabel#placeholderSubtext {{
            font-size: 14px;
            color: {cls.GRAY_400};
        }}
        """

    @classmethod
    def get_dialog_stylesheet(cls):
        """Get enhanced dialog stylesheet."""
        return cls.get_main_stylesheet()

    @staticmethod
    def get_stylesheet(theme_name: str) -> str:
        """Get stylesheet by theme name."""
        if theme_name == BabbittTheme.CORPORATE_THEME:
            return BabbittTheme.get_main_stylesheet()
        elif theme_name == BabbittTheme.DARK_THEME:
            return BabbittTheme.get_dark_stylesheet()
        else:
            return BabbittTheme.get_main_stylesheet()

    @classmethod
    def get_dark_stylesheet(cls):
        """Get dark theme stylesheet (placeholder for future implementation)."""
        return cls.get_main_stylesheet()  # For now, return main stylesheet