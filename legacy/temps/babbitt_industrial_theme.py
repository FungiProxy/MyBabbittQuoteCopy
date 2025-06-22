"""
Babbitt Industrial Premium Theme - Sophisticated UI System
File: src/ui/theme/babbitt_industrial_premium.py

🔴 Critical - Premium industrial theme with sophisticated styling and micro-interactions
"""


class BabbittIndustrialPremium:
    """
    Premium industrial theme system that transforms MyBabbittQuote into a 
    sophisticated, high-end application matching Babbitt International's 
    professional standards. Features advanced styling, animations, and 
    premium visual hierarchy.
    """
    
    # ============================================================================
    # SOPHISTICATED COLOR PALETTE - INDUSTRIAL PREMIUM
    # ============================================================================
    
    # Primary Industrial Blues - Premium Gradient System
    PRIMARY_BLUE = "#0052cc"         # Bright primary blue (CTAs, active states)
    SECONDARY_BLUE = "#003d99"       # Darker blue (hover, pressed)
    ACCENT_BLUE = "#0066ff"          # Vibrant blue (highlights, focus)
    STEEL_BLUE = "#2c5aa0"           # Industrial steel blue
    
    # Industrial Dark Palette - Sophisticated Navigation
    CHARCOAL = "#1a1a1a"             # Primary dark (sidebar, headers)
    DARK_STEEL = "#2d3748"           # Secondary dark
    GUNMETAL = "#4a5568"             # Tertiary dark
    
    # Premium Grays - Professional Hierarchy
    PLATINUM = "#f7fafc"             # Lightest background
    SILVER = "#edf2f7"               # Secondary background
    STEEL_GRAY = "#e2e8f0"           # Borders, dividers
    CHARCOAL_GRAY = "#718096"        # Secondary text
    IRON_GRAY = "#4a5568"            # Primary text
    
    # Premium Whites and Lights
    PURE_WHITE = "#ffffff"           # Pure white cards, forms
    OFF_WHITE = "#fefefe"            # Slight tint for depth
    CREAM_WHITE = "#fdfdfd"          # Warm white for comfort
    
    # Status Colors - Industrial Safety Standards
    SUCCESS_GREEN = "#38a169"        # Success, complete states
    WARNING_AMBER = "#d69e2e"        # Warning, attention needed
    ERROR_RED = "#e53e3e"            # Error, critical states
    INFO_CYAN = "#0987a0"            # Information, help states
    
    # Accent Colors - Premium Industrial
    GOLD_ACCENT = "#d69e2e"          # Premium gold highlights
    COPPER_ACCENT = "#dd6b20"        # Industrial copper
    STEEL_ACCENT = "#718096"         # Steel metallic
    
    # Advanced Interactive States
    HOVER_OVERLAY = "rgba(0, 82, 204, 0.08)"
    ACTIVE_OVERLAY = "rgba(0, 82, 204, 0.12)"
    FOCUS_GLOW = "0 0 0 3px rgba(0, 82, 204, 0.3)"
    PREMIUM_SHADOW = "0 4px 16px rgba(0, 0, 0, 0.15)"
    CARD_SHADOW = "0 2px 8px rgba(0, 0, 0, 0.1)"
    ELEVATED_SHADOW = "0 8px 32px rgba(0, 0, 0, 0.2)"
    
    @staticmethod
    def get_main_stylesheet():
        """
        Premium industrial stylesheet with sophisticated styling and micro-interactions.
        Transforms every UI element into a premium experience.
        """
        return f"""
        /* ========================================================================
           BABBITT INDUSTRIAL PREMIUM THEME
           Sophisticated styling system for premium industrial applications
        ======================================================================== */
        
        /* ====== GLOBAL FOUNDATION ====== */
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PLATINUM},
                stop:1 {BabbittIndustrialPremium.SILVER});
            color: {BabbittIndustrialPremium.IRON_GRAY};
            font-family: 'Segoe UI', 'Roboto', 'San Francisco', 'Helvetica Neue', sans-serif;
            font-size: 14px;
            font-weight: 400;
        }}
        
        /* ====== PREMIUM SIDEBAR - INDUSTRIAL GRADIENT ====== */
        QFrame#sidebarFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {BabbittIndustrialPremium.CHARCOAL},
                stop:0.3 #1e1e1e,
                stop:0.7 #222222,
                stop:1 {BabbittIndustrialPremium.DARK_STEEL});
            border: none;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 220px;
            max-width: 220px;
        }}
        
        /* Premium Logo with Industrial Styling */
        QLabel#logoLabel {{
            color: {BabbittIndustrialPremium.PURE_WHITE};
            font-size: 22px;
            font-weight: 700;
            padding: 28px 20px 20px 20px;
            margin-bottom: 8px;
            background: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        }}
        
        /* Sophisticated Navigation List */
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
            transition: all 0.2s ease-in-out;
        }}
        
        QListWidget#navList::item:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 255, 255, 0.08),
                stop:1 rgba(255, 255, 255, 0.12));
            color: {BabbittIndustrialPremium.PURE_WHITE};
            transform: translateX(4px);
        }}
        
        QListWidget#navList::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {BabbittIndustrialPremium.PRIMARY_BLUE},
                stop:0.8 {BabbittIndustrialPremium.ACCENT_BLUE},
                stop:1 rgba(0, 82, 204, 0.8));
            border-left: 3px solid {BabbittIndustrialPremium.GOLD_ACCENT};
            color: {BabbittIndustrialPremium.PURE_WHITE};
            font-weight: 600;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }}
        
        /* Premium Settings Button */
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
            color: {BabbittIndustrialPremium.PURE_WHITE};
        }}
        
        QPushButton#settingsButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.08),
                stop:1 rgba(255, 255, 255, 0.04));
        }}
        
        /* ====== PREMIUM CONTENT AREA ====== */
        QFrame#contentAreaFrame {{
            background: {BabbittIndustrialPremium.PURE_WHITE};
            border: none;
        }}
        
        /* Sophisticated Content Header */
        QFrame#contentHeader {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PURE_WHITE},
                stop:1 {BabbittIndustrialPremium.CREAM_WHITE});
            border: none;
            border-bottom: 1px solid {BabbittIndustrialPremium.STEEL_GRAY};
            min-height: 70px;
            max-height: 70px;
        }}
        
        /* Premium Page Titles */
        QLabel#pageTitle {{
            color: {BabbittIndustrialPremium.IRON_GRAY};
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin: 0;
            padding: 0;
        }}
        
        /* ====== SOPHISTICATED DASHBOARD CARDS ====== */
        QFrame[class="statCard"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PURE_WHITE},
                stop:1 {BabbittIndustrialPremium.OFF_WHITE});
            border: 1px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 12px;
            padding: 24px;
            margin: 8px;
            box-shadow: {BabbittIndustrialPremium.CARD_SHADOW};
        }}
        
        QFrame[class="statCard"]:hover {{
            border-color: {BabbittIndustrialPremium.PRIMARY_BLUE};
            box-shadow: {BabbittIndustrialPremium.PREMIUM_SHADOW};
            transform: translateY(-2px);
            transition: all 0.2s ease-out;
        }}
        
        /* Premium Card Typography */
        QLabel[class="statTitle"] {{
            color: {BabbittIndustrialPremium.CHARCOAL_GRAY};
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        QLabel[class="statValue"] {{
            color: {BabbittIndustrialPremium.IRON_GRAY};
            font-size: 32px;
            font-weight: 800;
            line-height: 1.2;
            margin: 8px 0;
        }}
        
        QLabel[class="statSubtitle"] {{
            color: {BabbittIndustrialPremium.CHARCOAL_GRAY};
            font-size: 13px;
            font-weight: 500;
            opacity: 0.8;
        }}
        
        QLabel[class="statIcon"] {{
            color: {BabbittIndustrialPremium.STEEL_BLUE};
            font-size: 24px;
            opacity: 0.7;
        }}
        
        /* ====== PREMIUM BUTTONS SYSTEM ====== */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PURE_WHITE},
                stop:1 {BabbittIndustrialPremium.CREAM_WHITE});
            color: {BabbittIndustrialPremium.IRON_GRAY};
            border: 1px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 500;
            min-height: 40px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PLATINUM},
                stop:1 {BabbittIndustrialPremium.SILVER});
            border-color: {BabbittIndustrialPremium.PRIMARY_BLUE};
            box-shadow: 0 2px 8px rgba(0, 82, 204, 0.15);
        }}
        
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.SILVER},
                stop:1 {BabbittIndustrialPremium.STEEL_GRAY});
            transform: translateY(1px);
        }}
        
        /* Primary Buttons - Premium Blue Gradient */
        QPushButton[class="primary"], QPushButton#newQuoteBtn {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PRIMARY_BLUE},
                stop:0.5 {BabbittIndustrialPremium.STEEL_BLUE},
                stop:1 {BabbittIndustrialPremium.SECONDARY_BLUE});
            color: {BabbittIndustrialPremium.PURE_WHITE};
            border: 1px solid {BabbittIndustrialPremium.SECONDARY_BLUE};
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0, 82, 204, 0.3);
        }}
        
        QPushButton[class="primary"]:hover, QPushButton#newQuoteBtn:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.ACCENT_BLUE},
                stop:0.5 {BabbittIndustrialPremium.PRIMARY_BLUE},
                stop:1 {BabbittIndustrialPremium.STEEL_BLUE});
            box-shadow: {BabbittIndustrialPremium.PREMIUM_SHADOW};
            transform: translateY(-1px);
        }}
        
        /* ====== SOPHISTICATED FORM ELEMENTS ====== */
        QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {{
            background: {BabbittIndustrialPremium.PURE_WHITE};
            border: 2px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 6px;
            padding: 10px 14px;
            color: {BabbittIndustrialPremium.IRON_GRAY};
            font-size: 14px;
            font-weight: 500;
            min-height: 20px;
            selection-background-color: {BabbittIndustrialPremium.PRIMARY_BLUE};
            selection-color: {BabbittIndustrialPremium.PURE_WHITE};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {BabbittIndustrialPremium.PRIMARY_BLUE};
            box-shadow: {BabbittIndustrialPremium.FOCUS_GLOW};
            background: {BabbittIndustrialPremium.CREAM_WHITE};
        }}
        
        /* Premium Dropdown System */
        QComboBox {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PURE_WHITE},
                stop:1 {BabbittIndustrialPremium.CREAM_WHITE});
            border: 2px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 6px;
            padding: 8px 12px;
            color: {BabbittIndustrialPremium.IRON_GRAY};
            font-size: 14px;
            font-weight: 500;
            min-height: 24px;
            max-height: 36px;
        }}
        
        QComboBox:hover {{
            border-color: {BabbittIndustrialPremium.PRIMARY_BLUE};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.CREAM_WHITE},
                stop:1 {BabbittIndustrialPremium.PLATINUM});
        }}
        
        QComboBox:focus {{
            border-color: {BabbittIndustrialPremium.ACCENT_BLUE};
            box-shadow: {BabbittIndustrialPremium.FOCUS_GLOW};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            border-left: 1px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PLATINUM},
                stop:1 {BabbittIndustrialPremium.SILVER});
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid {BabbittIndustrialPremium.CHARCOAL_GRAY};
            width: 0;
            height: 0;
        }}
        
        QComboBox QAbstractItemView {{
            background: {BabbittIndustrialPremium.PURE_WHITE};
            border: 2px solid {BabbittIndustrialPremium.PRIMARY_BLUE};
            border-radius: 8px;
            padding: 6px 0;
            selection-background-color: {BabbittIndustrialPremium.PRIMARY_BLUE};
            selection-color: {BabbittIndustrialPremium.PURE_WHITE};
            box-shadow: {BabbittIndustrialPremium.ELEVATED_SHADOW};
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: 8px 16px;
            margin: 2px 6px;
            border-radius: 4px;
        }}
        
        QComboBox QAbstractItemView::item:hover {{
            background: {BabbittIndustrialPremium.HOVER_OVERLAY};
        }}
        
        /* ====== PREMIUM DIALOG SYSTEM ====== */
        QDialog {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PURE_WHITE},
                stop:1 {BabbittIndustrialPremium.PLATINUM});
            border: 2px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 16px;
            box-shadow: {BabbittIndustrialPremium.ELEVATED_SHADOW};
        }}
        
        /* Sophisticated Group Boxes */
        QGroupBox {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PURE_WHITE},
                stop:1 {BabbittIndustrialPremium.OFF_WHITE});
            border: 2px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 10px;
            margin-top: 14px;
            padding-top: 16px;
            font-weight: 600;
            color: {BabbittIndustrialPremium.IRON_GRAY};
            font-size: 15px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px;
            padding: 4px 12px;
            background: {BabbittIndustrialPremium.PRIMARY_BLUE};
            color: {BabbittIndustrialPremium.PURE_WHITE};
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* ====== PREMIUM LISTS AND TABLES ====== */
        QListWidget, QTreeWidget {{
            background: {BabbittIndustrialPremium.PURE_WHITE};
            border: 2px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 8px;
            padding: 6px;
            alternate-background-color: {BabbittIndustrialPremium.PLATINUM};
            font-size: 14px;
        }}
        
        QListWidget::item, QTreeWidget::item {{
            padding: 10px 14px;
            border-radius: 6px;
            margin: 2px;
            transition: all 0.15s ease-in-out;
        }}
        
        QListWidget::item:hover, QTreeWidget::item:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {BabbittIndustrialPremium.HOVER_OVERLAY},
                stop:1 rgba(0, 82, 204, 0.04));
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {BabbittIndustrialPremium.PRIMARY_BLUE},
                stop:1 {BabbittIndustrialPremium.ACCENT_BLUE});
            color: {BabbittIndustrialPremium.PURE_WHITE};
            font-weight: 500;
        }}
        
        QTableWidget {{
            background: {BabbittIndustrialPremium.PURE_WHITE};
            gridline-color: {BabbittIndustrialPremium.STEEL_GRAY};
            border: 2px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 8px;
            selection-background-color: {BabbittIndustrialPremium.PRIMARY_BLUE};
        }}
        
        QHeaderView::section {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.DARK_STEEL},
                stop:1 {BabbittIndustrialPremium.GUNMETAL});
            color: {BabbittIndustrialPremium.PURE_WHITE};
            padding: 12px 16px;
            border: none;
            border-bottom: 1px solid {BabbittIndustrialPremium.STEEL_GRAY};
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* ====== PREMIUM SCROLLBARS ====== */
        QScrollBar:vertical {{
            background: {BabbittIndustrialPremium.PLATINUM};
            width: 14px;
            border-radius: 7px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {BabbittIndustrialPremium.STEEL_GRAY},
                stop:1 {BabbittIndustrialPremium.CHARCOAL_GRAY});
            border-radius: 7px;
            min-height: 30px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {BabbittIndustrialPremium.PRIMARY_BLUE},
                stop:1 {BabbittIndustrialPremium.STEEL_BLUE});
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* ====== PREMIUM STATUS SYSTEM ====== */
        QLabel[status="success"] {{
            color: {BabbittIndustrialPremium.SUCCESS_GREEN};
            font-weight: 600;
            background: rgba(56, 161, 105, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        QLabel[status="warning"] {{
            color: {BabbittIndustrialPremium.WARNING_AMBER};
            font-weight: 600;
            background: rgba(214, 158, 46, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        QLabel[status="error"] {{
            color: {BabbittIndustrialPremium.ERROR_RED};
            font-weight: 600;
            background: rgba(229, 62, 62, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        QLabel[status="info"] {{
            color: {BabbittIndustrialPremium.INFO_CYAN};
            font-weight: 600;
            background: rgba(9, 135, 160, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        /* ====== PREMIUM TAB SYSTEM ====== */
        QTabWidget::pane {{
            background: {BabbittIndustrialPremium.PURE_WHITE};
            border: 2px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 8px;
            margin-top: 4px;
        }}
        
        QTabBar::tab {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.SILVER},
                stop:1 {BabbittIndustrialPremium.STEEL_GRAY});
            color: {BabbittIndustrialPremium.IRON_GRAY};
            padding: 12px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 500;
        }}
        
        QTabBar::tab:selected {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PRIMARY_BLUE},
                stop:1 {BabbittIndustrialPremium.STEEL_BLUE});
            color: {BabbittIndustrialPremium.PURE_WHITE};
            font-weight: 600;
        }}
        
        QTabBar::tab:hover:!selected {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.PLATINUM},
                stop:1 {BabbittIndustrialPremium.SILVER});
            color: {BabbittIndustrialPremium.PRIMARY_BLUE};
        }}
        
        /* ====== PREMIUM MENU SYSTEM ====== */
        QMenuBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {BabbittIndustrialPremium.CHARCOAL},
                stop:1 {BabbittIndustrialPremium.DARK_STEEL});
            color: {BabbittIndustrialPremium.PURE_WHITE};
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 6px 0;
            font-weight: 500;
        }}
        
        QMenuBar::item {{
            background: transparent;
            padding: 8px 16px;
            margin: 0 2px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected, QMenuBar::item:hover {{
            background: {BabbittIndustrialPremium.PRIMARY_BLUE};
            color: {BabbittIndustrialPremium.PURE_WHITE};
        }}
        
        QMenu {{
            background: {BabbittIndustrialPremium.PURE_WHITE};
            border: 2px solid {BabbittIndustrialPremium.PRIMARY_BLUE};
            border-radius: 8px;
            padding: 6px 0;
            box-shadow: {BabbittIndustrialPremium.ELEVATED_SHADOW};
        }}
        
        QMenu::item {{
            padding: 8px 20px;
            margin: 2px 6px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background: {BabbittIndustrialPremium.PRIMARY_BLUE};
            color: {BabbittIndustrialPremium.PURE_WHITE};
        }}
        
        /* ====== PROGRESS BARS ====== */
        QProgressBar {{
            background: {BabbittIndustrialPremium.SILVER};
            border: 1px solid {BabbittIndustrialPremium.STEEL_GRAY};
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            height: 16px;
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {BabbittIndustrialPremium.SUCCESS_GREEN},
                stop:1 {BabbittIndustrialPremium.PRIMARY_BLUE});
            border-radius: 7px;
            margin: 1px;
        }}
        """


# ============================================================================
# PREMIUM INTEGRATION SYSTEM
# ============================================================================

class BabbittPremiumIntegration:
    """Premium integration system with advanced UI enhancements."""
    
    @staticmethod
    def apply_premium_theme(main_window):
        """Apply the complete premium theme with advanced features."""
        # Apply the main stylesheet
        stylesheet = BabbittIndustrialPremium.get_main_stylesheet()
        main_window.setStyleSheet(stylesheet)
        
        # Set advanced window properties
        main_window.setWindowTitle("MyBabbittQuote - Babbitt International")
        main_window.setMinimumSize(1200, 750)
        
        # Apply premium window effects
        BabbittPremiumIntegration._apply_window_effects(main_window)
        
        print("🏭 Babbitt Industrial Premium Theme Applied")
        print("   ✨ Sophisticated gradients and shadows")
        print("   🎯 Premium typography hierarchy")
        print("   🔥 Advanced micro-interactions")
        print("   💎 Industrial luxury aesthetic")
    
    @staticmethod
    def _apply_window_effects(window):
        """Apply advanced window effects and properties."""
        # Enable advanced styling
        window.setAttribute(Qt.WA_TranslucentBackground, False)
        window.setProperty("themeLevel", "premium")
        
        # Set premium properties for better rendering
        if hasattr(window, 'setGraphicsEffect'):
            from PySide6.QtWidgets import QGraphicsDropShadowEffect
            from PySide6.QtCore import Qt
            from PySide6.QtGui import QColor
            
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 30))
            shadow.setOffset(0, 10)
            # Note: Only apply to specific widgets, not main window
    
    @staticmethod
    def create_premium_button(text: str, button_type: str = "primary"):
        """Create premium styled buttons."""
        from PySide6.QtWidgets import QPushButton
        
        button = QPushButton(text)
        button.setProperty("class", button_type)
        return button
    
    @staticmethod
    def create_metric_card(title: str, value: str, subtitle: str, icon: str = "📊"):
        """Create premium styled metric cards."""
        from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
        
        card = QFrame()
        card.setProperty("class", "statCard")
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header with title and icon
        header_layout = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setProperty("class", "statTitle")
        
        icon_label = QLabel(icon)
        icon_label.setProperty("class", "statIcon")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(icon_label)
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setProperty("class", "statValue")
        layout.addWidget(value_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setProperty("class", "statSubtitle")
        layout.addWidget(subtitle_label)
        
        return card


# ============================================================================
# QUICK IMPLEMENTATION GUIDE
# ============================================================================
"""
🔴 IMMEDIATE IMPLEMENTATION - Transform Your App in 5 Minutes:

1. Replace your theme file with this premium version:
   📁 src/ui/theme/babbitt_industrial_premium.py

2. Apply the premium theme in your MainWindow.__init__():
   
   from src.ui.theme.babbitt_industrial_premium import BabbittPremiumIntegration
   
   def __init__(self):
       super().__init__()
       # Your existing setup...
       
       # Apply premium theme
       BabbittPremiumIntegration.apply_premium_theme(self)

3. Your dashboard cards will automatically become premium styled

4. All dialogs, forms, and buttons will gain sophisticated styling

5. Navigation will have beautiful gradients and micro-interactions

🎯 EXPECTED RESULTS:
- Sophisticated dark sidebar with premium gradients
- Dashboard cards with shadows, hover effects, and premium typography
- Form elements with focus glows and smooth transitions  
- Professional color hierarchy throughout
- Industrial luxury aesthetic matching Babbitt International's brand
- Micro-interactions that make the app feel premium and responsive

This theme transforms every element of your application into a sophisticated, 
premium experience worthy of a high-end industrial company.
"""