"""
Babbitt International Theme System

Provides the industrial theme for MyBabbittQuote application with professional
blue color scheme and consistent styling across all components.
"""

from PySide6.QtCore import QObject


class BabbittTheme(QObject):
    """
    Theme system for Babbitt International MyBabbittQuote application.

    Provides a professional industrial color scheme with blue primary colors,
    gold accents, and clean styling appropriate for business use.
    """

    # Primary Colors - Industrial Blue Scheme
    PRIMARY_BLUE = '#2C3E50'      # Deep professional blue
    SECONDARY_BLUE = '#34495E'    # Lighter blue for hover states
    ACCENT_GOLD = '#F39C12'       # Gold accent for highlights

    # Status Colors
    SUCCESS_GREEN = '#28A745'     # Success states, valid configurations
    WARNING_ORANGE = '#FD7E14'    # Warnings, attention needed
    ERROR_RED = '#DC3545'         # Errors, invalid states
    INFO_BLUE = '#17A2B8'         # Information, help text

    # Background Colors
    WHITE = '#FFFFFF'             # Primary background
    LIGHT_GRAY = '#F8F9FA'        # Secondary backgrounds, panels
    MEDIUM_GRAY = '#6C757D'       # Secondary text, borders
    DARK_GRAY = '#343A40'         # Dark text, headers
    CARD_BORDER = '#E9ECEF'       # Card and component borders
    
    # Additional colors for compatibility
    CARD_BG = WHITE               # Card background
    SURFACE_BG = LIGHT_GRAY       # Surface background
    BORDER_COLOR = CARD_BORDER    # Border color
    HOVER_BG = '#E3F2FD'          # Hover background
    PRIMARY_TEXT = DARK_GRAY      # Primary text
    SECONDARY_TEXT = MEDIUM_GRAY  # Secondary text
    MUTED_TEXT = MEDIUM_GRAY      # Muted text

    @staticmethod
    def get_main_stylesheet():
        """Get the main application stylesheet."""
        return f"""
        /* Main Window and Global Styles */
        QMainWindow {{
            background-color: {BabbittTheme.LIGHT_GRAY};
            color: {BabbittTheme.DARK_GRAY};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}

        /* Sidebar Styling */
        QFrame#sidebarFrame {{
            background-color: {BabbittTheme.PRIMARY_BLUE};
            border: none;
            min-width: 240px;
            max-width: 240px;
        }}

        QLabel#logoLabel {{
            color: {BabbittTheme.ACCENT_GOLD};
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
            border-left: 3px solid {BabbittTheme.ACCENT_GOLD};
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
            background-color: {BabbittTheme.WHITE};
            border: none;
        }}

        QFrame#contentHeader {{
            background-color: {BabbittTheme.WHITE};
            border-bottom: 1px solid {BabbittTheme.CARD_BORDER};
            padding: 20px;
            min-height: 60px;
        }}

        QLabel#pageTitle {{
            font-size: 24px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
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
            background-color: {BabbittTheme.PRIMARY_BLUE};
            color: white;
        }}

        QPushButton.primary:hover {{
            background-color: {BabbittTheme.SECONDARY_BLUE};
        }}

        QPushButton.primary:pressed {{
            background-color: {BabbittTheme.DARK_GRAY};
        }}

        QPushButton.success {{
            background-color: {BabbittTheme.SUCCESS_GREEN};
            color: white;
        }}

        QPushButton.success:hover {{
            background-color: #1e7e34;
        }}

        QPushButton.secondary {{
            background-color: {BabbittTheme.MEDIUM_GRAY};
            color: white;
        }}

        QPushButton.secondary:hover {{
            background-color: #545b62;
        }}

        QPushButton.warning {{
            background-color: {BabbittTheme.WARNING_ORANGE};
            color: white;
        }}

        QPushButton.warning:hover {{
            background-color: #e0650e;
        }}

        QPushButton:disabled {{
            background-color: {BabbittTheme.CARD_BORDER};
            color: {BabbittTheme.MEDIUM_GRAY};
        }}

        /* Card Components */
        QFrame.card {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 20px;
        }}

        QFrame.card:hover {{
            border-color: {BabbittTheme.PRIMARY_BLUE};
        }}

        QFrame.productCard {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 20px;
            margin: 5px;
        }}

        QFrame.productCard:hover {{
            border-color: #2C3E50;
        }}

        QFrame.familyCard {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 6px;
            padding: 10px;
            margin: 4px 0;
        }}

        QFrame.familyCard:hover {{
            border-color: {BabbittTheme.PRIMARY_BLUE};
            background-color: #e3f2fd;
        }}

        QFrame.familyCard[selected="true"] {{
            border-color: {BabbittTheme.PRIMARY_BLUE};
            background-color: #e3f2fd;
        }}

        /* Custom classes for Dashboard */
        .quoteItemCard {{
            background-color: white;
            border: 1px solid #E9ECEF;
            border-radius: 6px;
            padding: 15px;
            margin: 5px 0;
        }}
        .quoteItemCard:hover {{
            border-color: #2C3E50;
        }}
        .quoteItemTitle {{
            font-weight: 600;
            color: #2C3E50;
            font-size: 14px;
        }}
        .quoteItemDetails {{
            color: #6C757D;
            font-size: 12px;
        }}
        .status-sent {{
            background-color: {BabbittTheme.SUCCESS_GREEN};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-draft {{
            background-color: {BabbittTheme.WARNING_ORANGE};
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-default {{
            background-color: {BabbittTheme.LIGHT_GRAY};
            color: {BabbittTheme.DARK_GRAY};
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .placeholderText {{
            color: {BabbittTheme.MEDIUM_GRAY};
            font-size: 14px;
            padding: 40px;
        }}
        #sectionTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
            margin-bottom: 15px;
        }}

        /* Custom classes for Quote Creation */
        .quoteSubtitle {{
            color: {BabbittTheme.SECONDARY_TEXT};
            font-size: 14px;
        }}
        #quoteTotalLabel {{
            color: {BabbittTheme.PRIMARY_BLUE};
            font-weight: 600;
            font-size: 18px;
        }}
        .placeholderCard {{
            color: {BabbittTheme.MUTED_TEXT};
            font-size: 14px;
            padding: 40px;
            background-color: {BabbittTheme.LIGHT_GRAY};
            border-radius: 6px;
            border: 1px dashed {BabbittTheme.CARD_BORDER};
        }}
        QPushButton.info.small {{
            background-color: {BabbittTheme.INFO_BLUE};
            color: white;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.info.small:hover {{
            background-color: #128293;
        }}
        QPushButton.danger.small {{
            background-color: {BabbittTheme.ERROR_RED};
            color: white;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
        }}
        QPushButton.danger.small:hover {{
            background-color: #b02a37;
        }}

        /* Custom styles for Product Selection */
        #progressIndicator {{
            background-color: {BabbittTheme.WHITE};
            border-bottom: 1px solid {BabbittTheme.CARD_BORDER};
            min-height: 100px;
            max-height: 100px;
        }}
        
        #progressLine {{
            background-color: {BabbittTheme.CARD_BORDER};
            border: none;
            border-radius: 1px;
        }}
        
        #progressLine[completed="true"] {{
            background-color: {BabbittTheme.SUCCESS_GREEN};
        }}
        
        .stepNumber {{
            width: 36px;
            height: 36px;
            border-radius: 18px;
            background-color: {BabbittTheme.LIGHT_GRAY};
            color: {BabbittTheme.MUTED_TEXT};
            font-weight: 600;
            font-size: 14px;
            border: 2px solid {BabbittTheme.CARD_BORDER};
        }}
        
        .stepNumber[active="true"] {{
            background-color: {BabbittTheme.PRIMARY_BLUE};
            color: white;
            border-color: {BabbittTheme.PRIMARY_BLUE};
        }}
        
        .stepNumber[completed="true"] {{
            background-color: {BabbittTheme.SUCCESS_GREEN};
            color: white;
            border-color: {BabbittTheme.SUCCESS_GREEN};
        }}
        
        .stepLabel {{
            color: {BabbittTheme.SECONDARY_TEXT};
            font-size: 12px;
            font-weight: 500;
            text-align: center;
        }}
        
        .stepLabel[active="true"] {{
            color: {BabbittTheme.PRIMARY_TEXT};
            font-weight: 600;
        }}

        /* Statistics Cards */
        QFrame.statCard {{
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
        }}

        QLabel.statTitle {{
            color: {BabbittTheme.SECONDARY_TEXT};
            font-size: 14px;
            font-weight: 500;
        }}

        QLabel.statValue {{
            color: {BabbittTheme.PRIMARY_BLUE};
            font-size: 28px;
            font-weight: 600;
            margin: 5px 0;
        }}

        QLabel.statSubtitle {{
            color: {BabbittTheme.SECONDARY_TEXT};
            font-size: 12px;
        }}

        QLabel.statIcon {{
            color: {BabbittTheme.ACCENT_GOLD};
            font-size: 20px;
        }}

        /* Product Labels */
        QLabel.productName {{
            font-size: 18px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
            margin-bottom: 8px;
        }}

        QLabel.productDescription {{
            color: {BabbittTheme.SECONDARY_TEXT};
            font-size: 14px;
            margin-bottom: 15px;
        }}

        QLabel.productPrice {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittTheme.SUCCESS_GREEN};
            margin-bottom: 15px;
        }}

        QLabel.familyName {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
        }}

        QLabel.familyDescription {{
            font-size: 12px;
            color: {BabbittTheme.SECONDARY_TEXT};
        }}

        /* Form Controls */
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
            padding: 10px 14px;
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 6px;
            font-size: 14px;
            background-color: {BabbittTheme.WHITE};
            color: {BabbittTheme.PRIMARY_TEXT};
        }}

        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
            border-color: {BabbittTheme.ACCENT_GOLD};
            outline: none;
        }}

        QLabel.formLabel {{
            font-weight: 500;
            color: {BabbittTheme.PRIMARY_TEXT};
            margin-bottom: 5px;
        }}

        QLabel.sectionTitle {{
            font-size: 16px;
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid {BabbittTheme.CARD_BORDER};
        }}

        /* Progress and Status */
        QProgressBar {{
            border-radius: 6px;
            height: 10px;
            background-color: {BabbittTheme.LIGHT_GRAY};
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {BabbittTheme.ACCENT_GOLD};
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
            background-color: {BabbittTheme.WHITE};
            border: 1px solid {BabbittTheme.CARD_BORDER};
            border-radius: 6px;
            gridline-color: {BabbittTheme.CARD_BORDER};
            color: {BabbittTheme.PRIMARY_TEXT};
        }}

        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {BabbittTheme.CARD_BORDER};
        }}

        QTableWidget::item:selected {{
            background-color: {BabbittTheme.HOVER_BG};
            color: {BabbittTheme.PRIMARY_BLUE};
        }}

        QHeaderView::section {{
            background-color: {BabbittTheme.LIGHT_GRAY};
            color: {BabbittTheme.SECONDARY_TEXT};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {BabbittTheme.CARD_BORDER};
            font-weight: 500;
        }}

        /* Radio Buttons and Checkboxes */
        QRadioButton, QCheckBox {{
            color: {BabbittTheme.PRIMARY_TEXT};
            spacing: 8px;
        }}

        QRadioButton::indicator, QCheckBox::indicator {{
            width: 18px;
            height: 18px;
        }}

        QRadioButton::indicator:unchecked {{
            border: 2px solid {BabbittTheme.CARD_BORDER};
            border-radius: 9px;
            background-color: {BabbittTheme.WHITE};
        }}

        QRadioButton::indicator:checked {{
            border: 2px solid {BabbittTheme.ACCENT_GOLD};
            border-radius: 9px;
            background-color: {BabbittTheme.ACCENT_GOLD};
        }}

        QCheckBox::indicator:unchecked {{
            border: 2px solid {BabbittTheme.CARD_BORDER};
            border-radius: 3px;
            background-color: {BabbittTheme.WHITE};
        }}

        QCheckBox::indicator:checked {{
            border: 2px solid {BabbittTheme.ACCENT_GOLD};
            border-radius: 3px;
            background-color: {BabbittTheme.ACCENT_GOLD};
        }}

        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            border: none;
            background-color: {BabbittTheme.LIGHT_GRAY};
            width: 14px;
            border-radius: 7px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {BabbittTheme.CARD_BORDER};
            border-radius: 7px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {BabbittTheme.ACCENT_GOLD};
        }}

        /* Group Boxes */
        QGroupBox {{
            font-weight: 600;
            color: {BabbittTheme.PRIMARY_BLUE};
            border: 2px solid {BabbittTheme.CARD_BORDER};
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: {BabbittTheme.WHITE};
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
