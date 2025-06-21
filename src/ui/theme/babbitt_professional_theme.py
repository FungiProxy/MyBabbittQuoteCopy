"""
Babbitt Professional Theme System

Provides a professional theme for MyBabbittQuote application that matches
the Babbitt International website colors and branding.
"""

from PySide6.QtCore import QObject
from .dashboard_styles import get_dashboard_stylesheet


class BabbittProfessionalTheme(QObject):
    """
    Professional theme system for MyBabbittQuote application.

    Provides a clean, professional color scheme that matches the Babbitt International
    website branding with navy blue primary colors, gold accents, and modern styling.
    """

    # Primary Colors - Babbitt Professional Brand
    PRIMARY_NAVY = '#1B365D'      # Deep navy blue from website
    SECONDARY_NAVY = '#2C5282'    # Lighter navy for hover states
    ACCENT_GOLD = '#D69E2E'       # Gold accent from website
    DARK_NAVY = '#0F2027'         # Darker navy for pressed states

    # Status Colors
    SUCCESS_GREEN = '#38A169'     # Success states, valid configurations
    WARNING_ORANGE = '#ED8936'    # Warnings, attention needed
    ERROR_RED = '#E53E3E'         # Errors, invalid states (matches website red)
    INFO_BLUE = '#3182CE'         # Information, help text

    # Background Colors - Professional Theme
    WHITE_BG = '#FFFFFF'          # Primary white background
    LIGHT_GRAY = '#F7FAFC'        # Light gray backgrounds
    CARD_BG = '#FFFFFF'           # Card and component backgrounds
    SURFACE_BG = '#EDF2F7'        # Elevated surface backgrounds
    BORDER_COLOR = '#E2E8F0'      # Borders and dividers
    HOVER_BG = '#EBF8FF'          # Hover state backgrounds

    # Text Colors
    PRIMARY_TEXT = '#1A202C'      # Primary text color
    SECONDARY_TEXT = '#4A5568'    # Secondary text color
    MUTED_TEXT = '#718096'        # Muted text color
    ACCENT_TEXT = '#D69E2E'       # Accent text color

    @staticmethod
    def get_main_stylesheet():
        """Get the main application stylesheet."""
        return f"""
        /* Main Window and Global Styles */
        QMainWindow {{
            background-color: {BabbittProfessionalTheme.LIGHT_GRAY};
            color: {BabbittProfessionalTheme.PRIMARY_TEXT};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}

        /* Sidebar Styling */
        QFrame#sidebarFrame {{
            background-color: {BabbittProfessionalTheme.PRIMARY_NAVY};
            border: none;
            min-width: 240px;
            max-width: 240px;
        }}

        QLabel#logoLabel {{
            color: {BabbittProfessionalTheme.ACCENT_GOLD};
            font-size: 24px;
            font-weight: 600;
            padding: 20px 10px;
            background-color: transparent;
        }}

        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: white;
            font-size: 14px;
            outline: none;
        }}

        QListWidget#navList::item {{
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }}

        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        QListWidget#navList::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-left: 3px solid {BabbittProfessionalTheme.ACCENT_GOLD};
            font-weight: 500;
        }}

        QPushButton#settingsButton {{
            background-color: transparent;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 10px 20px;
            margin: 10px;
            border-radius: 4px;
            font-size: 14px;
        }}

        QPushButton#settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        /* Content Area */
        QFrame#contentAreaFrame {{
            background-color: {BabbittProfessionalTheme.LIGHT_GRAY};
            border: none;
        }}

        QFrame#contentHeader {{
            background-color: {BabbittProfessionalTheme.WHITE_BG};
            border-bottom: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            padding: 20px;
            min-height: 60px;
        }}

        QLabel#pageTitle {{
            font-size: 24px;
            font-weight: 600;
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
        }}

        /* Button Styles */
        QPushButton {{
            border: none;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: 500;
            font-size: 14px;
            min-height: 20px;
        }}

        QPushButton.primary {{
            background-color: {BabbittProfessionalTheme.ACCENT_GOLD};
            color: white;
        }}

        QPushButton.primary:hover {{
            background-color: #B7791F;
        }}

        QPushButton.primary:pressed {{
            background-color: #975A16;
        }}

        QPushButton.success {{
            background-color: {BabbittProfessionalTheme.SUCCESS_GREEN};
            color: white;
        }}

        QPushButton.success:hover {{
            background-color: #2F855A;
        }}

        QPushButton.secondary {{
            background-color: {BabbittProfessionalTheme.SURFACE_BG};
            color: {BabbittProfessionalTheme.PRIMARY_TEXT};
        }}

        QPushButton.secondary:hover {{
            background-color: #E2E8F0;
        }}

        QPushButton.warning {{
            background-color: {BabbittProfessionalTheme.WARNING_ORANGE};
            color: white;
        }}

        QPushButton.warning:hover {{
            background-color: #DD6B20;
        }}

        QPushButton:disabled {{
            background-color: {BabbittProfessionalTheme.SURFACE_BG};
            color: {BabbittProfessionalTheme.MUTED_TEXT};
        }}

        /* Card Components */
        QFrame.card {{
            background-color: {BabbittProfessionalTheme.CARD_BG};
            border: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 16px;
        }}

        QFrame.card:hover {{
            border-color: {BabbittProfessionalTheme.ACCENT_GOLD};
            background-color: {BabbittProfessionalTheme.HOVER_BG};
        }}

        QFrame.productCard {{
            background-color: {BabbittProfessionalTheme.CARD_BG};
            border: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 20px;
            margin: 5px;
        }}

        QFrame.productCard:hover {{
            border-color: {BabbittProfessionalTheme.ACCENT_GOLD};
            background-color: {BabbittProfessionalTheme.HOVER_BG};
        }}

        QFrame.familyCard {{
            background-color: {BabbittProfessionalTheme.CARD_BG};
            border: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 6px;
            padding: 10px;
            margin: 4px 0;
        }}

        QFrame.familyCard:hover {{
            border-color: {BabbittProfessionalTheme.ACCENT_GOLD};
            background-color: {BabbittProfessionalTheme.HOVER_BG};
        }}

        QFrame.familyCard[selected="true"] {{
            border-color: {BabbittProfessionalTheme.ACCENT_GOLD};
            background-color: {BabbittProfessionalTheme.HOVER_BG};
        }}

        /* Custom classes for Dashboard */
        /* === All dashboard styles have been moved to dashboard_styles.py === */

        /* Main Content Headers */
        QLabel#contentTitle {{
            font-size: 28px;
            font-weight: 600;
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
        }}
        
        QFrame#contentDivider {{
            background-color: {BabbittProfessionalTheme.BORDER_COLOR};
            height: 1px;
        }}

        /* Statistics Cards */
        QFrame.statCard {{
            background-color: {BabbittProfessionalTheme.CARD_BG};
            border: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        QLabel.statTitle {{
            color: {BabbittProfessionalTheme.SECONDARY_TEXT};
            font-size: 14px;
            font-weight: 500;
        }}

        QLabel.statValue {{
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
            font-size: 28px;
            font-weight: 600;
            margin: 5px 0;
        }}

        QLabel.statSubtitle {{
            color: {BabbittProfessionalTheme.SECONDARY_TEXT};
            font-size: 12px;
        }}

        QLabel.statIcon {{
            color: {BabbittProfessionalTheme.ACCENT_GOLD};
            font-size: 20px;
        }}

        /* Product Labels */
        QLabel.productName {{
            font-size: 18px;
            font-weight: 600;
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
            margin-bottom: 8px;
        }}

        QLabel.productDescription {{
            color: {BabbittProfessionalTheme.SECONDARY_TEXT};
            font-size: 14px;
            margin-bottom: 15px;
        }}

        QLabel.productPrice {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittProfessionalTheme.SUCCESS_GREEN};
            margin-bottom: 15px;
        }}

        QLabel.familyName {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
        }}

        QLabel.familyDescription {{
            font-size: 12px;
            color: {BabbittProfessionalTheme.SECONDARY_TEXT};
        }}

        /* Form Controls */
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            padding: 10px 14px;
            border: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 6px;
            font-size: 14px;
            background-color: {BabbittProfessionalTheme.CARD_BG};
            color: {BabbittProfessionalTheme.PRIMARY_TEXT};
        }}

        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border-color: {BabbittProfessionalTheme.ACCENT_GOLD};
            outline: none;
        }}

        QLabel.formLabel {{
            font-weight: 500;
            color: {BabbittProfessionalTheme.PRIMARY_TEXT};
            margin-bottom: 5px;
        }}

        QLabel.sectionTitle {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid {BabbittProfessionalTheme.BORDER_COLOR};
        }}

        /* Progress and Status */
        QProgressBar {{
            border-radius: 6px;
            height: 10px;
            background-color: {BabbittProfessionalTheme.SURFACE_BG};
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {BabbittProfessionalTheme.ACCENT_GOLD};
            border-radius: 6px;
        }}

        QLabel.validationSuccess {{
            background-color: #C6F6D5;
            border: 1px solid #9AE6B4;
            color: #22543D;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
        }}

        QLabel.validationError {{
            background-color: #FED7D7;
            border: 1px solid #FEB2B2;
            color: #742A2A;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
        }}

        QLabel.validationWarning {{
            background-color: #FEEBC8;
            border: 1px solid #FBD38D;
            color: #744210;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
        }}

        /* Tables */
        QTableWidget {{
            background-color: {BabbittProfessionalTheme.CARD_BG};
            border: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 6px;
            gridline-color: {BabbittProfessionalTheme.BORDER_COLOR};
            color: {BabbittProfessionalTheme.PRIMARY_TEXT};
        }}

        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
        }}

        QTableWidget::item:selected {{
            background-color: {BabbittProfessionalTheme.HOVER_BG};
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
        }}

        QHeaderView::section {{
            background-color: {BabbittProfessionalTheme.SURFACE_BG};
            color: {BabbittProfessionalTheme.SECONDARY_TEXT};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            font-weight: 500;
        }}

        /* Radio Buttons and Checkboxes */
        QRadioButton, QCheckBox {{
            color: {BabbittProfessionalTheme.PRIMARY_TEXT};
            spacing: 8px;
        }}

        QRadioButton::indicator, QCheckBox::indicator {{
            width: 18px;
            height: 18px;
        }}

        QRadioButton::indicator:unchecked {{
            border: 2px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 9px;
            background-color: {BabbittProfessionalTheme.CARD_BG};
        }}

        QRadioButton::indicator:checked {{
            border: 2px solid {BabbittProfessionalTheme.ACCENT_GOLD};
            border-radius: 9px;
            background-color: {BabbittProfessionalTheme.ACCENT_GOLD};
        }}

        QCheckBox::indicator:unchecked {{
            border: 2px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 3px;
            background-color: {BabbittProfessionalTheme.CARD_BG};
        }}

        QCheckBox::indicator:checked {{
            border: 2px solid {BabbittProfessionalTheme.ACCENT_GOLD};
            border-radius: 3px;
            background-color: {BabbittProfessionalTheme.ACCENT_GOLD};
        }}

        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            border: none;
            background-color: {BabbittProfessionalTheme.SURFACE_BG};
            width: 14px;
            border-radius: 7px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 7px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {BabbittProfessionalTheme.ACCENT_GOLD};
        }}

        /* Group Boxes */
        QGroupBox {{
            font-weight: 600;
            color: {BabbittProfessionalTheme.PRIMARY_NAVY};
            border: 2px solid {BabbittProfessionalTheme.BORDER_COLOR};
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: {BabbittProfessionalTheme.CARD_BG};
        }}

        /* === ENHANCED PROGRESS INDICATOR STYLES === */
        #progressIndicator {{
            background-color: {BabbittProfessionalTheme.CARD_BG};
            border-bottom: 1px solid {BabbittProfessionalTheme.BORDER_COLOR};
            min-height: 100px;
            max-height: 100px;
        }}
        
        #progressLine {{
            background-color: {BabbittProfessionalTheme.BORDER_COLOR};
            border: none;
            border-radius: 1px;
        }}
        
        #progressLine[completed="true"] {{
            background-color: {BabbittProfessionalTheme.SUCCESS_GREEN};
        }}
        
        .stepNumber {{
            width: 36px;
            height: 36px;
            border-radius: 18px;
            background-color: {BabbittProfessionalTheme.SURFACE_BG};
            color: {BabbittProfessionalTheme.MUTED_TEXT};
            font-weight: 600;
            font-size: 14px;
            border: 2px solid {BabbittProfessionalTheme.BORDER_COLOR};
        }}
        
        .stepNumber[active="true"] {{
            background-color: {BabbittProfessionalTheme.PRIMARY_NAVY};
            color: white;
            border-color: {BabbittProfessionalTheme.PRIMARY_NAVY};
        }}
        
        .stepNumber[completed="true"] {{
            background-color: {BabbittProfessionalTheme.SUCCESS_GREEN};
            color: white;
            border-color: {BabbittProfessionalTheme.SUCCESS_GREEN};
        }}
        
        .stepLabel {{
            color: {BabbittProfessionalTheme.SECONDARY_TEXT};
            font-size: 12px;
            font-weight: 500;
            text-align: center;
        }}
        
        .stepLabel[active="true"] {{
            color: {BabbittProfessionalTheme.PRIMARY_TEXT};
            font-weight: 600;
        }}
        """ + get_dashboard_stylesheet(BabbittProfessionalTheme)

    STYLES = {
        "card": {
            "background-color": CARD_BG,
            "border": f"1px solid {BORDER_COLOR}",
            "border-radius": "8px",
            "padding": "16px",
        },
        "metricCard": {
            "background-color": CARD_BG,
            "border": f"1px solid {BORDER_COLOR}",
            "border-radius": "8px",
            "padding": "16px",
        },
        "metricIcon": {
            "font-size": "20px",
            "color": ACCENT_GOLD,
        },
        "metricLabel": {
            "font-size": "13px",
            "color": SECONDARY_TEXT,
            "font-weight": "500",
        },
        "metricValue": {
            "font-size": "22px",
            "font-weight": "600",
            "color": PRIMARY_TEXT,
        },
        "metricSubtext": {
            "font-size": "12px",
            "color": MUTED_TEXT,
        },
        "recentQuotesCard": {
            "padding": "16px",
        },
        "recentQuotesTitle": {
            "font-size": "18px",
            "font-weight": "600",
            "color": PRIMARY_NAVY,
            "margin-bottom": "8px",
        },
        "noQuotesLabel": {
            "font-size": "14px",
            "color": MUTED_TEXT,
            "padding": "40px",
            "border": f"2px dashed {BORDER_COLOR}",
            "border-radius": "6px",
        },
        "quoteItemCard": {
            "background-color": CARD_BG,
            "border": f"1px solid {BORDER_COLOR}",
            "border-radius": "6px",
            "padding": "12px",
            "margin": "4px 0",
        },
        "quoteItemTitle": {
            "font-weight": "600",
            "color": PRIMARY_NAVY,
            "font-size": "14px",
        },
        "quoteItemDetails": {
            "color": SECONDARY_TEXT,
            "font-size": "12px",
        },
        "status-sent": {
            "background-color": SUCCESS_GREEN,
            "color": "white",
            "border-radius": "10px",
            "padding": "4px 8px",
            "font-size": "11px",
            "font-weight": "500",
        },
        "status-pending": {
            "background-color": WARNING_ORANGE,
            "color": "white",
            "border-radius": "10px",
            "padding": "4px 8px",
            "font-size": "11px",
            "font-weight": "500",
        },
        "status-draft": {
            "background-color": MUTED_TEXT,
            "color": "white",
            "border-radius": "10px",
            "padding": "4px 8px",
            "font-size": "11px",
            "font-weight": "500",
        },
    }

    @staticmethod
    def apply_stylesheet(widget, css_class):
        """Apply a predefined style to a widget."""
        style = BabbittProfessionalTheme.STYLES.get(css_class, {})
        style_str = "; ".join([f"{key}: {value}" for key, value in style.items()])
        widget.setStyleSheet(style_str)

    @staticmethod
    def apply_property_styles(widget, properties):
        """
        Dynamically applies styles to a widget based on a dictionary of properties.
        This is useful for applying styles that are not covered by a single css_class.
        """
        if not widget or not properties:
            return

        current_style = widget.styleSheet()
        new_styles = []

        for prop, value in properties.items():
            # Convert property from camelCase to kebab-case
            css_property = ''.join(['-' + c.lower() if c.isupper() else c for c in prop]).lstrip('-')
            new_styles.append(f"{css_property}: {value};")

        # Combine new styles with existing ones
        widget.setStyleSheet(current_style + " " + " ".join(new_styles))

    @classmethod
    def get_theme_info(cls):
        """Get theme information for the settings page."""
        return {
            'name': 'Babbitt Professional',
            'description': 'Professional Babbitt theme with corporate styling',
            'author': 'Babbitt Quote Generator',
            'primary_color': '#1B4F72',
            'secondary_color': '#2874A6',
            'accent_color': '#F39C12',
            'background_color': '#F8F9FA',
            'text_color': '#2C3E50',
            'success_color': '#27AE60',
            'warning_color': '#F39C12',
            'error_color': '#E74C3C',
            'info_color': '#3498DB',
        } 