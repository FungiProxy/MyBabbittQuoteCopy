"""
Modern Light Theme System

Provides a modern light theme for MyBabbittQuote application with green/emerald
color scheme and clean styling for contemporary applications.
"""

from PySide6.QtCore import QObject


class ModernLightTheme(QObject):
    """
    Modern light theme system for MyBabbittQuote application.

    Provides a contemporary light color scheme with emerald primary colors,
    mint accents, and clean styling appropriate for modern business applications.
    """

    # Primary Colors - Modern Green/Emerald Scheme
    PRIMARY_EMERALD = '#059669'   # Deep emerald for primary elements
    SECONDARY_EMERALD = '#10B981' # Lighter emerald for hover states
    ACCENT_MINT = '#34D399'       # Mint accent for highlights
    DARK_EMERALD = '#047857'      # Darker emerald for pressed states

    # Status Colors
    SUCCESS_GREEN = '#10B981'     # Success states, valid configurations
    WARNING_ORANGE = '#F59E0B'    # Warnings, attention needed
    ERROR_RED = '#EF4444'         # Errors, invalid states
    INFO_BLUE = '#3B82F6'         # Information, help text

    # Background Colors - Light Theme
    LIGHT_BG = '#F9FAFB'          # Primary light background
    CARD_BG = '#FFFFFF'           # Card and component backgrounds
    SURFACE_BG = '#F3F4F6'        # Elevated surface backgrounds
    BORDER_COLOR = '#E5E7EB'      # Borders and dividers
    HOVER_BG = '#ECFDF5'          # Hover state backgrounds

    # Text Colors
    PRIMARY_TEXT = '#111827'      # Primary text color
    SECONDARY_TEXT = '#6B7280'    # Secondary text color
    MUTED_TEXT = '#9CA3AF'        # Muted text color
    ACCENT_TEXT = '#059669'       # Accent text color

    @staticmethod
    def get_main_stylesheet():
        """Get the main application stylesheet."""
        return f"""
        /* Main Window and Global Styles */
        QMainWindow {{
            background-color: {ModernLightTheme.LIGHT_BG};
            color: {ModernLightTheme.PRIMARY_TEXT};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}

        /* Sidebar Styling */
        QFrame#sidebarFrame {{
            background-color: {ModernLightTheme.CARD_BG};
            border: none;
            min-width: 240px;
            max-width: 240px;
            border-right: 1px solid {ModernLightTheme.BORDER_COLOR};
        }}

        QLabel#logoLabel {{
            color: {ModernLightTheme.ACCENT_TEXT};
            font-size: 24px;
            font-weight: 600;
            padding: 20px 10px;
            background-color: transparent;
        }}

        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: {ModernLightTheme.PRIMARY_TEXT};
            font-size: 14px;
            outline: none;
        }}

        QListWidget#navList::item {{
            padding: 12px 20px;
            border-left: 3px solid transparent;
            margin: 2px 0;
        }}

        QListWidget#navList::item:hover {{
            background-color: {ModernLightTheme.HOVER_BG};
        }}

        QListWidget#navList::item:selected {{
            background-color: {ModernLightTheme.HOVER_BG};
            border-left: 3px solid {ModernLightTheme.ACCENT_MINT};
            font-weight: 500;
        }}

        QPushButton#settingsButton {{
            background-color: transparent;
            color: {ModernLightTheme.PRIMARY_TEXT};
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            padding: 10px 20px;
            margin: 10px;
            border-radius: 6px;
            font-size: 14px;
        }}

        QPushButton#settingsButton:hover {{
            background-color: {ModernLightTheme.HOVER_BG};
        }}

        /* Content Area */
        QFrame#contentAreaFrame {{
            background-color: {ModernLightTheme.LIGHT_BG};
            border: none;
        }}

        QFrame#contentHeader {{
            background-color: {ModernLightTheme.CARD_BG};
            border-bottom: 1px solid {ModernLightTheme.BORDER_COLOR};
            padding: 20px;
            min-height: 60px;
        }}

        QLabel#pageTitle {{
            font-size: 24px;
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
        }}

        /* Button Styles */
        QPushButton {{
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-weight: 500;
            font-size: 14px;
            min-height: 20px;
        }}

        QPushButton.primary {{
            background-color: {ModernLightTheme.PRIMARY_EMERALD};
            color: white;
        }}

        QPushButton.primary:hover {{
            background-color: {ModernLightTheme.SECONDARY_EMERALD};
        }}

        QPushButton.primary:pressed {{
            background-color: {ModernLightTheme.DARK_EMERALD};
        }}

        QPushButton.success {{
            background-color: {ModernLightTheme.SUCCESS_GREEN};
            color: white;
        }}

        QPushButton.success:hover {{
            background-color: #059669;
        }}

        QPushButton.secondary {{
            background-color: {ModernLightTheme.SURFACE_BG};
            color: {ModernLightTheme.PRIMARY_TEXT};
        }}

        QPushButton.secondary:hover {{
            background-color: #E5E7EB;
        }}

        QPushButton.warning {{
            background-color: {ModernLightTheme.WARNING_ORANGE};
            color: white;
        }}

        QPushButton.warning:hover {{
            background-color: #D97706;
        }}

        QPushButton:disabled {{
            background-color: {ModernLightTheme.SURFACE_BG};
            color: {ModernLightTheme.MUTED_TEXT};
        }}

        /* Card Components */
        QFrame.card {{
            background-color: {ModernLightTheme.CARD_BG};
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 20px;
        }}

        QFrame.card:hover {{
            border-color: {ModernLightTheme.ACCENT_MINT};
            background-color: {ModernLightTheme.HOVER_BG};
        }}

        QFrame.productCard {{
            background-color: {ModernLightTheme.CARD_BG};
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 20px;
            margin: 5px;
        }}

        QFrame.productCard:hover {{
            border-color: {ModernLightTheme.ACCENT_MINT};
            background-color: {ModernLightTheme.HOVER_BG};
        }}

        QFrame.familyCard {{
            background-color: {ModernLightTheme.CARD_BG};
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 10px;
            margin: 4px 0;
        }}

        QFrame.familyCard:hover {{
            border-color: {ModernLightTheme.ACCENT_MINT};
            background-color: {ModernLightTheme.HOVER_BG};
        }}

        QFrame.familyCard[selected="true"] {{
            border-color: {ModernLightTheme.ACCENT_MINT};
            background-color: {ModernLightTheme.HOVER_BG};
        }}

        /* Custom classes for Dashboard */
        .quoteItemCard {{
            background-color: {ModernLightTheme.CARD_BG};
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 15px;
            margin: 5px 0;
        }}
        .quoteItemCard:hover {{
            border-color: {ModernLightTheme.ACCENT_MINT};
        }}
        .quoteItemTitle {{
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
            font-size: 14px;
        }}
        .quoteItemDetails {{
            color: {ModernLightTheme.SECONDARY_TEXT};
            font-size: 12px;
        }}
        .status-sent {{
            background-color: {ModernLightTheme.SUCCESS_GREEN};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-draft {{
            background-color: {ModernLightTheme.WARNING_ORANGE};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-default {{
            background-color: {ModernLightTheme.SURFACE_BG};
            color: {ModernLightTheme.PRIMARY_TEXT};
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .placeholderText {{
            color: {ModernLightTheme.MUTED_TEXT};
            font-size: 14px;
            padding: 40px;
        }}
        #sectionTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
            margin-bottom: 15px;
        }}

        /* Custom classes for Quote Creation */
        .quoteSubtitle {{
            color: {ModernLightTheme.SECONDARY_TEXT};
            font-size: 14px;
        }}
        #quoteTotalLabel {{
            color: {ModernLightTheme.ACCENT_TEXT};
            font-weight: 600;
            font-size: 18px;
        }}
        .placeholderCard {{
            color: {ModernLightTheme.MUTED_TEXT};
            font-size: 14px;
            padding: 40px;
            background-color: {ModernLightTheme.SURFACE_BG};
            border-radius: 8px;
            border: 1px dashed {ModernLightTheme.BORDER_COLOR};
        }}
        QPushButton.info.small {{
            background-color: {ModernLightTheme.INFO_BLUE};
            color: white;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.info.small:hover {{
            background-color: #2563EB;
        }}
        QPushButton.danger.small {{
            background-color: {ModernLightTheme.ERROR_RED};
            color: white;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.danger.small:hover {{
            background-color: #DC2626;
        }}

        /* Custom styles for Product Selection */
        #progressIndicator {{
            background-color: {ModernLightTheme.CARD_BG};
            border-bottom: 1px solid {ModernLightTheme.BORDER_COLOR};
            padding: 20px;
        }}
        #progressLine {{
            min-width: 40px;
            max-width: 40px;
            min-height: 2px;
            max-height: 2px;
            background-color: {ModernLightTheme.BORDER_COLOR};
            border: none;
        }}
        .stepLabel {{
            color: {ModernLightTheme.SECONDARY_TEXT};
            font-size: 12px;
            font-weight: 500;
        }}
        #familiesPanel {{
            background-color: {ModernLightTheme.SURFACE_BG};
            border-right: 1px solid {ModernLightTheme.BORDER_COLOR};
        }}
        #productsPanel {{
            background-color: {ModernLightTheme.CARD_BG};
        }}
        #categoryHeader {{
            font-size: 14px;
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
            margin: 10px 0 5px 0;
            padding: 5px 0;
            border-bottom: 1px solid {ModernLightTheme.BORDER_COLOR};
        }}

        /* Custom styles for Configuration Wizard */
        #configPanel {{
            background-color: {ModernLightTheme.CARD_BG};
            border-right: 1px solid {ModernLightTheme.BORDER_COLOR};
        }}
        #summaryPanel {{
            background-color: {ModernLightTheme.SURFACE_BG};
        }}
        .formLabel {{
            font-weight: 500;
            color: {ModernLightTheme.PRIMARY_TEXT};
            margin-bottom: 8px;
        }}
        #summaryTotalFrame {{
            border-top: 2px solid {ModernLightTheme.BORDER_COLOR};
            padding-top: 15px;
            margin-top: 15px;
        }}
        #summaryTotalLabel, #summaryTotalPriceLabel {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
        }}

        /* Statistics Cards */
        QFrame.statCard {{
            background-color: {ModernLightTheme.CARD_BG};
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 12px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        QLabel.statTitle {{
            color: {ModernLightTheme.SECONDARY_TEXT};
            font-size: 14px;
            font-weight: 500;
        }}

        QLabel.statValue {{
            color: {ModernLightTheme.ACCENT_TEXT};
            font-size: 28px;
            font-weight: 600;
            margin: 5px 0;
        }}

        QLabel.statSubtitle {{
            color: {ModernLightTheme.SECONDARY_TEXT};
            font-size: 12px;
        }}

        QLabel.statIcon {{
            color: {ModernLightTheme.ACCENT_TEXT};
            font-size: 20px;
        }}

        /* Product Labels */
        QLabel.productName {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
            margin-bottom: 8px;
        }}

        QLabel.productDescription {{
            color: {ModernLightTheme.SECONDARY_TEXT};
            font-size: 14px;
            margin-bottom: 15px;
        }}

        QLabel.productPrice {{
            font-size: 16px;
            font-weight: 600;
            color: {ModernLightTheme.SUCCESS_GREEN};
            margin-bottom: 15px;
        }}

        QLabel.familyName {{
            font-size: 16px;
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
        }}

        QLabel.familyDescription {{
            font-size: 12px;
            color: {ModernLightTheme.SECONDARY_TEXT};
        }}

        /* Form Controls */
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            padding: 10px 14px;
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 6px;
            font-size: 14px;
            background-color: {ModernLightTheme.CARD_BG};
            color: {ModernLightTheme.PRIMARY_TEXT};
        }}

        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border-color: {ModernLightTheme.ACCENT_MINT};
            outline: none;
        }}

        QLabel.formLabel {{
            font-weight: 500;
            color: {ModernLightTheme.PRIMARY_TEXT};
            margin-bottom: 5px;
        }}

        QLabel.sectionTitle {{
            font-size: 16px;
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid {ModernLightTheme.BORDER_COLOR};
        }}

        /* Progress and Status */
        QProgressBar {{
            border-radius: 6px;
            height: 10px;
            background-color: {ModernLightTheme.SURFACE_BG};
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {ModernLightTheme.ACCENT_MINT};
            border-radius: 6px;
        }}

        QLabel.validationSuccess {{
            background-color: #D1FAE5;
            border: 1px solid #A7F3D0;
            color: #065F46;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
        }}

        QLabel.validationError {{
            background-color: #FEE2E2;
            border: 1px solid #FCA5A5;
            color: #991B1B;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
        }}

        QLabel.validationWarning {{
            background-color: #FEF3C7;
            border: 1px solid #FCD34D;
            color: #92400E;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
        }}

        /* Step Indicator */
        QLabel.stepNumber {{
            width: 32px;
            height: 32px;
            border-radius: 16px;
            background-color: {ModernLightTheme.SURFACE_BG};
            color: {ModernLightTheme.MUTED_TEXT};
            font-weight: 600;
            text-align: center;
        }}

        QLabel.stepNumber[active="true"] {{
            background-color: {ModernLightTheme.ACCENT_MINT};
            color: white;
        }}

        QLabel.stepNumber[completed="true"] {{
            background-color: {ModernLightTheme.SUCCESS_GREEN};
            color: white;
        }}

        /* Tables */
        QTableWidget {{
            background-color: {ModernLightTheme.CARD_BG};
            border: 1px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 6px;
            gridline-color: {ModernLightTheme.BORDER_COLOR};
            color: {ModernLightTheme.PRIMARY_TEXT};
        }}

        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {ModernLightTheme.BORDER_COLOR};
        }}

        QTableWidget::item:selected {{
            background-color: {ModernLightTheme.HOVER_BG};
            color: {ModernLightTheme.ACCENT_TEXT};
        }}

        QHeaderView::section {{
            background-color: {ModernLightTheme.SURFACE_BG};
            color: {ModernLightTheme.SECONDARY_TEXT};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {ModernLightTheme.BORDER_COLOR};
            font-weight: 500;
        }}

        /* Radio Buttons and Checkboxes */
        QRadioButton, QCheckBox {{
            color: {ModernLightTheme.PRIMARY_TEXT};
            spacing: 8px;
        }}

        QRadioButton::indicator, QCheckBox::indicator {{
            width: 18px;
            height: 18px;
        }}

        QRadioButton::indicator:unchecked {{
            border: 2px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 9px;
            background-color: {ModernLightTheme.CARD_BG};
        }}

        QRadioButton::indicator:checked {{
            border: 2px solid {ModernLightTheme.ACCENT_MINT};
            border-radius: 9px;
            background-color: {ModernLightTheme.ACCENT_MINT};
        }}

        QCheckBox::indicator:unchecked {{
            border: 2px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 3px;
            background-color: {ModernLightTheme.CARD_BG};
        }}

        QCheckBox::indicator:checked {{
            border: 2px solid {ModernLightTheme.ACCENT_MINT};
            border-radius: 3px;
            background-color: {ModernLightTheme.ACCENT_MINT};
        }}

        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            border: none;
            background-color: {ModernLightTheme.SURFACE_BG};
            width: 14px;
            border-radius: 7px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {ModernLightTheme.BORDER_COLOR};
            border-radius: 7px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {ModernLightTheme.ACCENT_MINT};
        }}

        /* Group Boxes */
        QGroupBox {{
            font-weight: 600;
            color: {ModernLightTheme.ACCENT_TEXT};
            border: 2px solid {ModernLightTheme.BORDER_COLOR};
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: {ModernLightTheme.CARD_BG};
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