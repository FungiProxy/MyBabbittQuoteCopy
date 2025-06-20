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
    PRIMARY_EMERALD = '#047857'   # Deep emerald for primary elements (more vibrant)
    SECONDARY_EMERALD = '#059669' # Lighter emerald for hover states
    ACCENT_MINT = '#10B981'       # Mint accent for highlights (brighter)
    DARK_EMERALD = '#065F46'      # Darker emerald for pressed states

    # Status Colors
    SUCCESS_GREEN = '#10B981'     # Success states, valid configurations
    WARNING_ORANGE = '#F59E0B'    # Warnings, attention needed
    ERROR_RED = '#EF4444'         # Errors, invalid states
    INFO_BLUE = '#3B82F6'         # Information, help text

    # Background Colors - Light Theme
    LIGHT_BG = '#F0FDF4'          # Primary light background (green tinted)
    CARD_BG = '#FFFFFF'           # Card and component backgrounds
    SURFACE_BG = '#ECFDF5'        # Elevated surface backgrounds (green tinted)
    BORDER_COLOR = '#D1FAE5'      # Borders and dividers (mint tinted)
    HOVER_BG = '#D1FAE5'          # Hover state backgrounds (mint tinted)

    # Text Colors
    PRIMARY_TEXT = '#064E3B'      # Primary text color (dark emerald)
    SECONDARY_TEXT = '#065F46'    # Secondary text color (medium emerald)
    MUTED_TEXT = '#047857'        # Muted text color (light emerald)
    ACCENT_TEXT = '#047857'       # Accent text color (emerald)

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
            min-height: 100px;
            max-height: 100px;
        }}
        
        #progressLine {{
            background-color: {ModernLightTheme.BORDER_COLOR};
            border: none;
            border-radius: 1px;
        }}
        
        #progressLine[completed="true"] {{
            background-color: {ModernLightTheme.SUCCESS_GREEN};
        }}
        
        .stepNumber {{
            width: 36px;
            height: 36px;
            border-radius: 18px;
            background-color: {ModernLightTheme.SURFACE_BG};
            color: {ModernLightTheme.MUTED_TEXT};
            font-weight: 600;
            font-size: 14px;
            border: 2px solid {ModernLightTheme.BORDER_COLOR};
        }}
        
        .stepNumber[active="true"] {{
            background-color: {ModernLightTheme.PRIMARY_EMERALD};
            color: white;
            border-color: {ModernLightTheme.PRIMARY_EMERALD};
        }}
        
        .stepNumber[completed="true"] {{
            background-color: {ModernLightTheme.SUCCESS_GREEN};
            color: white;
            border-color: {ModernLightTheme.SUCCESS_GREEN};
        }}
        
        .stepLabel {{
            color: {ModernLightTheme.SECONDARY_TEXT};
            font-size: 12px;
            font-weight: 500;
            text-align: center;
        }}
        
        .stepLabel[active="true"] {{
            color: {ModernLightTheme.PRIMARY_TEXT};
            font-weight: 600;
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