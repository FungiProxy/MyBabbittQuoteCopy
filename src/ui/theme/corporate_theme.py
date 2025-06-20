"""
Corporate Theme System

Provides a professional corporate theme for MyBabbittQuote application with navy/red
color scheme and traditional styling for business applications.
"""

from PySide6.QtCore import QObject


class CorporateTheme(QObject):
    """
    Corporate theme system for MyBabbittQuote application.

    Provides a professional corporate color scheme with navy primary colors,
    red accents, and traditional styling appropriate for business environments.
    """

    # Primary Colors - Corporate Navy/Red Scheme
    PRIMARY_NAVY = '#1E3A8A'      # Deep navy for primary elements
    SECONDARY_NAVY = '#3B82F6'    # Lighter navy for hover states
    ACCENT_RED = '#DC2626'        # Red accent for highlights
    DARK_NAVY = '#1E40AF'         # Darker navy for pressed states

    # Status Colors
    SUCCESS_GREEN = '#059669'     # Success states, valid configurations
    WARNING_ORANGE = '#D97706'    # Warnings, attention needed
    ERROR_RED = '#DC2626'         # Errors, invalid states
    INFO_BLUE = '#2563EB'         # Information, help text

    # Background Colors - Corporate Theme
    LIGHT_BG = '#F8FAFC'          # Primary light background
    CARD_BG = '#FFFFFF'           # Card and component backgrounds
    SURFACE_BG = '#F1F5F9'        # Elevated surface backgrounds
    BORDER_COLOR = '#CBD5E1'      # Borders and dividers
    HOVER_BG = '#EFF6FF'          # Hover state backgrounds

    # Text Colors
    PRIMARY_TEXT = '#0F172A'      # Primary text color
    SECONDARY_TEXT = '#475569'    # Secondary text color
    MUTED_TEXT = '#64748B'        # Muted text color
    ACCENT_TEXT = '#1E3A8A'       # Accent text color

    @staticmethod
    def get_main_stylesheet():
        """Get the main application stylesheet."""
        return f"""
        /* Main Window and Global Styles */
        QMainWindow {{
            background-color: {CorporateTheme.LIGHT_BG};
            color: {CorporateTheme.PRIMARY_TEXT};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}

        /* Sidebar Styling */
        QFrame#sidebarFrame {{
            background-color: {CorporateTheme.PRIMARY_NAVY};
            border: none;
            min-width: 240px;
            max-width: 240px;
        }}

        QLabel#logoLabel {{
            color: {CorporateTheme.ACCENT_RED};
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
            border-left: 3px solid {CorporateTheme.ACCENT_RED};
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
            background-color: {CorporateTheme.LIGHT_BG};
            border: none;
        }}

        QFrame#contentHeader {{
            background-color: {CorporateTheme.CARD_BG};
            border-bottom: 1px solid {CorporateTheme.BORDER_COLOR};
            padding: 20px;
            min-height: 60px;
        }}

        QLabel#pageTitle {{
            font-size: 24px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
        }}

        /* Button Styles */
        QPushButton {{
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 14px;
            min-height: 20px;
        }}

        QPushButton.primary {{
            background-color: {CorporateTheme.PRIMARY_NAVY};
            color: white;
        }}

        QPushButton.primary:hover {{
            background-color: {CorporateTheme.SECONDARY_NAVY};
        }}

        QPushButton.primary:pressed {{
            background-color: {CorporateTheme.DARK_NAVY};
        }}

        QPushButton.success {{
            background-color: {CorporateTheme.SUCCESS_GREEN};
            color: white;
        }}

        QPushButton.success:hover {{
            background-color: #047857;
        }}

        QPushButton.secondary {{
            background-color: {CorporateTheme.SURFACE_BG};
            color: {CorporateTheme.PRIMARY_TEXT};
        }}

        QPushButton.secondary:hover {{
            background-color: #E2E8F0;
        }}

        QPushButton.warning {{
            background-color: {CorporateTheme.WARNING_ORANGE};
            color: white;
        }}

        QPushButton.warning:hover {{
            background-color: #B45309;
        }}

        QPushButton:disabled {{
            background-color: {CorporateTheme.SURFACE_BG};
            color: {CorporateTheme.MUTED_TEXT};
        }}

        /* Card Components */
        QFrame.card {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 20px;
        }}

        QFrame.card:hover {{
            border-color: {CorporateTheme.ACCENT_RED};
            background-color: {CorporateTheme.HOVER_BG};
        }}

        QFrame.productCard {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 20px;
            margin: 5px;
        }}

        QFrame.productCard:hover {{
            border-color: {CorporateTheme.ACCENT_RED};
            background-color: {CorporateTheme.HOVER_BG};
        }}

        QFrame.familyCard {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 4px;
            padding: 10px;
            margin: 4px 0;
        }}

        QFrame.familyCard:hover {{
            border-color: {CorporateTheme.ACCENT_RED};
            background-color: {CorporateTheme.HOVER_BG};
        }}

        QFrame.familyCard[selected="true"] {{
            border-color: {CorporateTheme.ACCENT_RED};
            background-color: {CorporateTheme.HOVER_BG};
        }}

        /* Custom classes for Dashboard */
        .quoteItemCard {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 4px;
            padding: 15px;
            margin: 5px 0;
        }}
        .quoteItemCard:hover {{
            border-color: {CorporateTheme.ACCENT_RED};
        }}
        .quoteItemTitle {{
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
            font-size: 14px;
        }}
        .quoteItemDetails {{
            color: {CorporateTheme.SECONDARY_TEXT};
            font-size: 12px;
        }}
        .status-sent {{
            background-color: {CorporateTheme.SUCCESS_GREEN};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-draft {{
            background-color: {CorporateTheme.WARNING_ORANGE};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-default {{
            background-color: {CorporateTheme.SURFACE_BG};
            color: {CorporateTheme.PRIMARY_TEXT};
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .placeholderText {{
            color: {CorporateTheme.MUTED_TEXT};
            font-size: 14px;
            padding: 40px;
        }}
        #sectionTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
            margin-bottom: 15px;
        }}

        /* Custom classes for Quote Creation */
        .quoteSubtitle {{
            color: {CorporateTheme.SECONDARY_TEXT};
            font-size: 14px;
        }}
        #quoteTotalLabel {{
            color: {CorporateTheme.ACCENT_TEXT};
            font-weight: 600;
            font-size: 18px;
        }}
        .placeholderCard {{
            color: {CorporateTheme.MUTED_TEXT};
            font-size: 14px;
            padding: 40px;
            background-color: {CorporateTheme.SURFACE_BG};
            border-radius: 4px;
            border: 1px dashed {CorporateTheme.BORDER_COLOR};
        }}
        QPushButton.info.small {{
            background-color: {CorporateTheme.INFO_BLUE};
            color: white;
            border-radius: 2px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.info.small:hover {{
            background-color: #1D4ED8;
        }}
        QPushButton.danger.small {{
            background-color: {CorporateTheme.ERROR_RED};
            color: white;
            border-radius: 2px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.danger.small:hover {{
            background-color: #B91C1C;
        }}

        /* Custom styles for Product Selection */
        #progressIndicator {{
            background-color: {CorporateTheme.CARD_BG};
            border-bottom: 1px solid {CorporateTheme.BORDER_COLOR};
            padding: 20px;
        }}
        #progressLine {{
            min-width: 40px;
            max-width: 40px;
            min-height: 2px;
            max-height: 2px;
            background-color: {CorporateTheme.BORDER_COLOR};
            border: none;
        }}
        .stepLabel {{
            color: {CorporateTheme.SECONDARY_TEXT};
            font-size: 12px;
            font-weight: 500;
        }}
        #familiesPanel {{
            background-color: {CorporateTheme.SURFACE_BG};
            border-right: 1px solid {CorporateTheme.BORDER_COLOR};
        }}
        #productsPanel {{
            background-color: {CorporateTheme.CARD_BG};
        }}
        #categoryHeader {{
            font-size: 14px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
            margin: 10px 0 5px 0;
            padding: 5px 0;
            border-bottom: 1px solid {CorporateTheme.BORDER_COLOR};
        }}

        /* Custom styles for Configuration Wizard */
        #configPanel {{
            background-color: {CorporateTheme.CARD_BG};
            border-right: 1px solid {CorporateTheme.BORDER_COLOR};
        }}
        #summaryPanel {{
            background-color: {CorporateTheme.SURFACE_BG};
        }}
        .formLabel {{
            font-weight: 500;
            color: {CorporateTheme.PRIMARY_TEXT};
            margin-bottom: 8px;
        }}
        #summaryTotalFrame {{
            border-top: 2px solid {CorporateTheme.BORDER_COLOR};
            padding-top: 15px;
            margin-top: 15px;
        }}
        #summaryTotalLabel, #summaryTotalPriceLabel {{
            font-size: 18px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
        }}

        /* Statistics Cards */
        QFrame.statCard {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 6px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        QLabel.statTitle {{
            color: {CorporateTheme.SECONDARY_TEXT};
            font-size: 14px;
            font-weight: 500;
        }}

        QLabel.statValue {{
            color: {CorporateTheme.ACCENT_TEXT};
            font-size: 28px;
            font-weight: 600;
            margin: 5px 0;
        }}

        QLabel.statSubtitle {{
            color: {CorporateTheme.SECONDARY_TEXT};
            font-size: 12px;
        }}

        QLabel.statIcon {{
            color: {CorporateTheme.ACCENT_TEXT};
            font-size: 20px;
        }}

        /* Product Labels */
        QLabel.productName {{
            font-size: 18px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
            margin-bottom: 8px;
        }}

        QLabel.productDescription {{
            color: {CorporateTheme.SECONDARY_TEXT};
            font-size: 14px;
            margin-bottom: 15px;
        }}

        QLabel.productPrice {{
            font-size: 16px;
            font-weight: 600;
            color: {CorporateTheme.SUCCESS_GREEN};
            margin-bottom: 15px;
        }}

        QLabel.familyName {{
            font-size: 16px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
        }}

        QLabel.familyDescription {{
            font-size: 12px;
            color: {CorporateTheme.SECONDARY_TEXT};
        }}

        /* Form Controls */
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            padding: 8px 12px;
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 4px;
            font-size: 14px;
            background-color: {CorporateTheme.CARD_BG};
            color: {CorporateTheme.PRIMARY_TEXT};
        }}

        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border-color: {CorporateTheme.ACCENT_RED};
            outline: none;
        }}

        QLabel.formLabel {{
            font-weight: 500;
            color: {CorporateTheme.PRIMARY_TEXT};
            margin-bottom: 5px;
        }}

        QLabel.sectionTitle {{
            font-size: 16px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid {CorporateTheme.BORDER_COLOR};
        }}

        /* Progress and Status */
        QProgressBar {{
            border-radius: 4px;
            height: 8px;
            background-color: {CorporateTheme.SURFACE_BG};
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {CorporateTheme.ACCENT_RED};
            border-radius: 4px;
        }}

        QLabel.validationSuccess {{
            background-color: #D1FAE5;
            border: 1px solid #A7F3D0;
            color: #065F46;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
        }}

        QLabel.validationError {{
            background-color: #FEE2E2;
            border: 1px solid #FCA5A5;
            color: #991B1B;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
        }}

        QLabel.validationWarning {{
            background-color: #FEF3C7;
            border: 1px solid #FCD34D;
            color: #92400E;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
        }}

        /* Step Indicator */
        QLabel.stepNumber {{
            width: 30px;
            height: 30px;
            border-radius: 15px;
            background-color: {CorporateTheme.SURFACE_BG};
            color: {CorporateTheme.MUTED_TEXT};
            font-weight: 600;
            text-align: center;
        }}

        QLabel.stepNumber[active="true"] {{
            background-color: {CorporateTheme.ACCENT_RED};
            color: white;
        }}

        QLabel.stepNumber[completed="true"] {{
            background-color: {CorporateTheme.SUCCESS_GREEN};
            color: white;
        }}

        /* Tables */
        QTableWidget {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 4px;
            gridline-color: {CorporateTheme.BORDER_COLOR};
            color: {CorporateTheme.PRIMARY_TEXT};
        }}

        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {CorporateTheme.BORDER_COLOR};
        }}

        QTableWidget::item:selected {{
            background-color: {CorporateTheme.HOVER_BG};
            color: {CorporateTheme.ACCENT_TEXT};
        }}

        QHeaderView::section {{
            background-color: {CorporateTheme.SURFACE_BG};
            color: {CorporateTheme.SECONDARY_TEXT};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {CorporateTheme.BORDER_COLOR};
            font-weight: 500;
        }}

        /* Radio Buttons and Checkboxes */
        QRadioButton, QCheckBox {{
            color: {CorporateTheme.PRIMARY_TEXT};
            spacing: 8px;
        }}

        QRadioButton::indicator, QCheckBox::indicator {{
            width: 16px;
            height: 16px;
        }}

        QRadioButton::indicator:unchecked {{
            border: 2px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 8px;
            background-color: {CorporateTheme.CARD_BG};
        }}

        QRadioButton::indicator:checked {{
            border: 2px solid {CorporateTheme.ACCENT_RED};
            border-radius: 8px;
            background-color: {CorporateTheme.ACCENT_RED};
        }}

        QCheckBox::indicator:unchecked {{
            border: 2px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 2px;
            background-color: {CorporateTheme.CARD_BG};
        }}

        QCheckBox::indicator:checked {{
            border: 2px solid {CorporateTheme.ACCENT_RED};
            border-radius: 2px;
            background-color: {CorporateTheme.ACCENT_RED};
        }}

        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            border: none;
            background-color: {CorporateTheme.SURFACE_BG};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {CorporateTheme.BORDER_COLOR};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {CorporateTheme.ACCENT_RED};
        }}

        /* Group Boxes */
        QGroupBox {{
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
            border: 2px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 10px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: {CorporateTheme.CARD_BG};
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
        widget.setStyleSheet(f'{current_style} {new_style}') 