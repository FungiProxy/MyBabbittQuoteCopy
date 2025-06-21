"""
Babbitt Unified Theme

The single source for the application's visual identity, providing a clean,
professional, and brand-aligned theme with both light and dark modes.
"""

from PySide6.QtCore import QObject


class BabbittTheme(QObject):
    """
    Defines the color palettes and generates the stylesheets for the application.
    """

    # --- LIGHT MODE COLOR PALETTE ---
    class Light:
        PRIMARY = '#1B365D'      # Deep navy blue
        SECONDARY = '#2C5282'    # Lighter navy for hover
        ACCENT = '#D69E2E'       # Gold accent
        
        # Backgrounds
        BG_0 = '#FFFFFF'         # Pure white (cards, primary background)
        BG_1 = '#F7FAFC'         # Light gray (main window background)
        BG_2 = '#EDF2F7'         # Hover, surfaces
        
        # Text
        TEXT_PRIMARY = '#1A202C'
        TEXT_SECONDARY = '#4A5568'
        TEXT_MUTED = '#718096'
        TEXT_ON_PRIMARY = '#FFFFFF' # Text on navy components

        # Borders
        BORDER = '#E2E8F0'
        BORDER_STRONG = '#D1D5DB' # For subtle shadow effect
        
        # Status
        SUCCESS = '#38A169'
        WARNING = '#ED8936'
        ERROR = '#E53E3E'

    # --- DARK MODE COLOR PALETTE ---
    class Dark:
        PRIMARY = '#2C5282'      # Brighter navy blue for dark mode
        SECONDARY = '#4A5568'    # A lighter gray-blue
        ACCENT = '#D69E2E'       # Gold accent (can often remain the same)
        
        # Backgrounds
        BG_0 = '#1A202C'         # Very dark slate (main window)
        BG_1 = '#2D3748'         # Dark slate (cards, primary surfaces)
        BG_2 = '#4A5568'         # Hover, surfaces
        
        # Text
        TEXT_PRIMARY = '#F7FAFC'
        TEXT_SECONDARY = '#E2E8F0'
        TEXT_MUTED = '#A0AEC0'
        TEXT_ON_PRIMARY = '#FFFFFF'

        # Borders
        BORDER = '#4A5568'
        BORDER_STRONG = '#2D3748' # For subtle shadow effect
        
        # Status
        SUCCESS = '#38A169'
        WARNING = '#ED8936'
        ERROR = '#E53E3E'

    @staticmethod
    def get_light_stylesheet():
        """Generates the full stylesheet for light mode."""
        
        light = BabbittTheme.Light
        
        return f"""
        /* === MAIN WINDOW & DIALOGS === */
        QMainWindow, QDialog {{
            background-color: {light.BG_1};
            color: {light.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        /* === SIDEBAR === */
        #sidebarFrame {{
            background-color: {light.PRIMARY};
            border-right: 1px solid {light.PRIMARY};
        }}
        #logoLabel {{
            color: {light.ACCENT};
            font-size: 24px;
            font-weight: 600;
            padding: 20px 10px;
        }}
        #navList {{
            background-color: transparent;
            border: none;
            color: {light.TEXT_ON_PRIMARY};
            font-size: 14px;
            outline: none;
        }}
        #navList::item {{
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }}
        #navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        #navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-left: 3px solid {light.ACCENT};
            font-weight: 500;
        }}
        #settingsButton {{
            background-color: transparent;
            color: {light.TEXT_ON_PRIMARY};
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 10px;
            margin: 10px;
            border-radius: 4px;
        }}
        #settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        /* === CONTENT AREA === */
        #contentAreaFrame {{
            background-color: {light.BG_1};
            border: none;
        }}
        #contentHeader {{
            background-color: {light.BG_0};
            border-bottom: 1px solid {light.BORDER};
            padding: 10px 20px;
            min-height: 40px;
        }}
        #pageTitle {{
            font-size: 28px;
            font-weight: 600;
            color: {light.PRIMARY};
        }}
        
        /* === CARDS & FRAMES === */
        QFrame[card="true"] {{
            background-color: {light.BG_0};
            border: 1px solid {light.BORDER};
            border-radius: 8px;
            padding: 20px;
        }}
        QFrame[elevated="true"] {{
            border-bottom: 3px solid {light.BORDER_STRONG};
        }}
        QFrame[interactive="true"]:hover {{
            border-color: {light.ACCENT};
            background-color: {light.BG_2};
        }}

        /* === GENERAL WIDGETS === */
        QGroupBox {{
            font-weight: 600;
            color: {light.PRIMARY};
            border: 1px solid {light.BORDER};
            border-radius: 8px;
            margin-top: 10px;
            padding: 15px;
            padding-top: 25px;
            background-color: {light.BG_0};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 15px;
            top: 8px;
            background-color: {light.BG_0};
            color: {light.TEXT_MUTED};
            font-size: 11px;
            text-transform: uppercase;
        }}
        
        /* === BUTTONS === */
        QPushButton {{
            border: 1px solid {light.BORDER};
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: 500;
            font-size: 14px;
            background-color: {light.BG_0};
            color: {light.TEXT_PRIMARY};
        }}
        QPushButton:hover {{
            background-color: {light.BG_2};
        }}
        QPushButton:pressed {{
            background-color: {light.BORDER};
        }}
        QPushButton[class~="primary"], QPushButton#new_quote_button {{
            background-color: {light.ACCENT};
            color: {light.TEXT_PRIMARY};
            border: 1px solid {light.ACCENT};
            font-weight: 600;
        }}
        QPushButton[class~="primary"]:hover, QPushButton#new_quote_button:hover {{
            background-color: #EAC54F; /* Lighter gold */
        }}
        QPushButton.success {{
            background-color: {light.SUCCESS};
            color: white;
            border: 1px solid {light.SUCCESS};
        }}
        
        /* === FORMS === */
        QLineEdit, QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox {{
            padding: 10px 12px;
            border: 1px solid {light.BORDER};
            border-radius: 6px;
            font-size: 14px;
            background-color: {light.BG_0};
            color: {light.TEXT_PRIMARY};
        }}
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {light.ACCENT};
            outline: none;
        }}
        QLabel.formLabel {{
            font-weight: 500;
            color: {light.TEXT_PRIMARY};
        }}
        
        /* === TABLES === */
        QTableWidget {{
            background-color: {light.BG_0};
            border: 1px solid {light.BORDER};
            border-radius: 6px;
            gridline-color: {light.BORDER};
        }}
        QTableWidget::item {{
            padding: 8px;
        }}
        QHeaderView::section {{
            background-color: {light.BG_2};
            color: {light.TEXT_SECONDARY};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {light.BORDER};
            font-weight: 500;
        }}

        /* === PRODUCT-SPECIFIC STYLES === */
        #progressIndicator {{
            background-color: {light.BG_0};
            border-bottom: 1px solid {light.BORDER};
            min-height: 80px;
            max-height: 80px;
        }}
        .stepNumber {{
            width: 30px;
            height: 30px;
            border-radius: 15px;
            background-color: {light.BG_2};
            color: {light.TEXT_MUTED};
            font-weight: 600;
            font-size: 14px;
            border: 2px solid {light.BORDER};
        }}
        .stepNumber[active="true"] {{
            background-color: {light.PRIMARY};
            color: white;
            border-color: {light.PRIMARY};
        }}
        .stepLabel {{
            color: {light.TEXT_SECONDARY};
            font-size: 12px;
            font-weight: 500;
        }}
        .stepLabel[active="true"] {{
            color: {light.TEXT_PRIMARY};
            font-weight: 600;
        }}
        
        /* === Custom Classes === */
        #sectionTitle, .sectionTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {light.PRIMARY};
            margin-bottom: 10px;
        }}
        .productName {{
            font-size: 18px;
            font-weight: 600;
            color: {light.PRIMARY};
        }}
        .productDescription {{
            color: {light.TEXT_SECONDARY};
            font-size: 14px;
        }}
        .productPrice {{
            font-size: 16px;
            font-weight: 600;
            color: {light.SUCCESS};
        }}
        .familyName {{
            font-size: 16px;
            font-weight: 600;
            color: {light.PRIMARY};
        }}
        .familyDescription {{
            font-size: 12px;
            color: {light.TEXT_SECONDARY};
        }}
        QFrame.familyCard[selected="true"] {{
            border-color: {light.ACCENT};
            background-color: {light.BG_2};
        }}

        /* === DASHBOARD & CUSTOM WIDGETS === */
        .statTitle {{
            color: {light.TEXT_SECONDARY};
            font-size: 13px;
            font-weight: 500;
        }}
        .statValue {{
            color: {light.TEXT_PRIMARY};
            font-size: 32px;
            font-weight: 600;
        }}
        .statSubtitle {{
            color: {light.TEXT_MUTED};
            font-size: 12px;
        }}
        .statIcon {{
            font-size: 24px;
        }}
        .placeholderText {{
            color: {light.TEXT_MUTED};
            font-size: 14px;
        }}
        """

    @staticmethod
    def get_dark_stylesheet():
        """Generates the full stylesheet for dark mode."""
        dark = BabbittTheme.Dark
        
        return f"""
        /* === MAIN WINDOW & DIALOGS === */
        QMainWindow, QDialog {{
            background-color: {dark.BG_0};
            color: {dark.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        /* === SIDEBAR === */
        #sidebarFrame {{
            background-color: {dark.BG_1};
            border-right: 1px solid {dark.BORDER};
        }}
        #logoLabel {{
            color: {dark.ACCENT};
            font-size: 24px;
            font-weight: 600;
            padding: 20px 10px;
        }}
        #navList {{
            background-color: transparent;
            border: none;
            color: {dark.TEXT_ON_PRIMARY};
            font-size: 14px;
            outline: none;
        }}
        #navList::item {{
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }}
        #navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        #navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-left: 3px solid {dark.ACCENT};
            font-weight: 500;
        }}
        #settingsButton {{
            background-color: transparent;
            color: {dark.TEXT_ON_PRIMARY};
            border: 1px solid {dark.BORDER};
            padding: 10px;
            margin: 10px;
            border-radius: 4px;
        }}
        #settingsButton:hover {{
            background-color: {dark.BG_2};
        }}

        /* === CONTENT AREA === */
        #contentAreaFrame {{
            background-color: {dark.BG_0};
            border: none;
        }}
        #contentHeader {{
            background-color: {dark.BG_1};
            border-bottom: 1px solid {dark.BORDER};
            padding: 10px 20px;
            min-height: 40px;
        }}
        #pageTitle {{
            font-size: 28px;
            font-weight: 600;
            color: {dark.TEXT_PRIMARY};
        }}
        
        /* === CARDS & FRAMES === */
        QFrame[card="true"] {{
            background-color: {dark.BG_1};
            border: 1px solid {dark.BORDER};
            border-radius: 8px;
            padding: 20px;
        }}
        QFrame[elevated="true"] {{
            border-bottom: 3px solid {dark.BORDER_STRONG};
        }}
        QFrame[interactive="true"]:hover {{
            border-color: {dark.ACCENT};
            background-color: {dark.BG_2};
        }}

        /* === GENERAL WIDGETS === */
        QGroupBox {{
            font-weight: 600;
            color: {dark.TEXT_PRIMARY};
            border: 1px solid {dark.BORDER};
            border-radius: 8px;
            margin-top: 10px;
            padding: 15px;
            padding-top: 25px;
            background-color: {dark.BG_1};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 15px;
            top: 8px;
            background-color: {dark.BG_1};
            color: {dark.TEXT_MUTED};
            font-size: 11px;
            text-transform: uppercase;
        }}
        
        /* === BUTTONS === */
        QPushButton {{
            border: 1px solid {dark.BORDER};
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: 500;
            font-size: 14px;
            background-color: {dark.BG_2};
            color: {dark.TEXT_PRIMARY};
        }}
        QPushButton:hover {{
            background-color: {dark.SECONDARY};
        }}
        QPushButton:pressed {{
            background-color: {dark.BORDER};
        }}
        QPushButton[class~="primary"], QPushButton#new_quote_button {{
            background-color: {dark.ACCENT};
            color: {dark.TEXT_PRIMARY};
            border: 1px solid {dark.ACCENT};
            font-weight: 600;
        }}
        QPushButton[class~="primary"]:hover, QPushButton#new_quote_button:hover {{
            background-color: #EAC54F; /* Lighter gold */
        }}
        QPushButton.success {{
            background-color: {dark.SUCCESS};
            color: white;
            border: 1px solid {dark.SUCCESS};
        }}
        
        /* === FORMS === */
        QLineEdit, QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox {{
            padding: 10px 12px;
            border: 1px solid {dark.BORDER};
            border-radius: 6px;
            font-size: 14px;
            background-color: {dark.BG_0};
            color: {dark.TEXT_PRIMARY};
        }}
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {dark.ACCENT};
            outline: none;
        }}
        QLabel.formLabel {{
            font-weight: 500;
            color: {dark.TEXT_PRIMARY};
        }}
        
        /* === TABLES === */
        QTableWidget {{
            background-color: {dark.BG_1};
            border: 1px solid {dark.BORDER};
            border-radius: 6px;
            gridline-color: {dark.BORDER};
        }}
        QTableWidget::item {{
            padding: 8px;
        }}
        QHeaderView::section {{
            background-color: {dark.BG_2};
            color: {dark.TEXT_SECONDARY};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {dark.BORDER};
            font-weight: 500;
        }}

        /* === PRODUCT-SPECIFIC STYLES === */
        #progressIndicator {{
            background-color: {dark.BG_1};
            border-bottom: 1px solid {dark.BORDER};
            min-height: 80px;
            max-height: 80px;
        }}
        .stepNumber {{
            width: 30px;
            height: 30px;
            border-radius: 15px;
            background-color: {dark.BG_2};
            color: {dark.TEXT_MUTED};
            font-weight: 600;
            font-size: 14px;
            border: 2px solid {dark.BORDER};
        }}
        .stepNumber[active="true"] {{
            background-color: {dark.PRIMARY};
            color: white;
            border-color: {dark.PRIMARY};
        }}
        .stepLabel {{
            color: {dark.TEXT_SECONDARY};
            font-size: 12px;
            font-weight: 500;
        }}
        .stepLabel[active="true"] {{
            color: {dark.TEXT_PRIMARY};
            font-weight: 600;
        }}
        
        /* === Custom Classes === */
        #sectionTitle, .sectionTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {dark.TEXT_PRIMARY};
            margin-bottom: 10px;
        }}
        .productName {{
            font-size: 18px;
            font-weight: 600;
            color: {dark.TEXT_PRIMARY};
        }}
        .productDescription {{
            color: {dark.TEXT_SECONDARY};
            font-size: 14px;
        }}
        .productPrice {{
            font-size: 16px;
            font-weight: 600;
            color: {dark.SUCCESS};
        }}
        .familyName {{
            font-size: 16px;
            font-weight: 600;
            color: {dark.TEXT_PRIMARY};
        }}
        .familyDescription {{
            font-size: 12px;
            color: {dark.TEXT_SECONDARY};
        }}
        QFrame.familyCard[selected="true"] {{
            border-color: {dark.ACCENT};
            background-color: {dark.BG_2};
        }}

        /* === DASHBOARD & CUSTOM WIDGETS === */
        .statTitle {{
            color: {dark.TEXT_SECONDARY};
            font-size: 13px;
            font-weight: 500;
        }}
        .statValue {{
            color: {dark.TEXT_PRIMARY};
            font-size: 32px;
            font-weight: 600;
        }}
        .statSubtitle {{
            color: {dark.TEXT_MUTED};
            font-size: 12px;
        }}
        .statIcon {{
            font-size: 24px;
        }}
        .placeholderText {{
            color: {dark.TEXT_MUTED};
            font-size: 14px;
        }}
        """

    @staticmethod
    def apply_property_styles(widget, properties):
        """Apply style properties to a widget."""
        style_parts = []
        for prop, value in properties.items():
            style_parts.append(f'{prop}: {value};')

        current_style = widget.styleSheet()
        new_style = ' '.join(style_parts)
        widget.setStyleSheet(f'{{current_style}} {{new_style}}')

    @staticmethod
    def get_card_style(elevated=False, interactive=False):
        """Returns a string for a card stylesheet."""
        # This is a helper, but direct property setting is now preferred.
        # This can be used for widgets that can't have properties easily set.
        style = f"background-color: {BabbittTheme.Light.BG_0}; border: 1px solid {BabbittTheme.Light.BORDER}; border-radius: 8px; padding: 20px;"
        if elevated:
            style += f" border-bottom: 3px solid {BabbittTheme.Light.BORDER_STRONG};"
        return style

    @staticmethod
    def get_application_stylesheet(mode='Light'):
        """Gets the full application stylesheet for a given mode."""
        if mode == 'Dark':
            return BabbittTheme.get_dark_stylesheet()
        return BabbittTheme.get_light_stylesheet()
