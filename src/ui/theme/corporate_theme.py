"""
Corporate Theme System

Provides a professional corporate theme for MyBabbittQuote application with navy/red
color scheme and traditional styling for business applications.
"""

from PySide6.QtCore import QObject
from .dashboard_styles import get_dashboard_stylesheet


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
    PRIMARY_RED = '#DC2626'       # Primary red (same as accent red)
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
            padding: 16px;
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
        .metricCard {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 8px;
            padding: 16px;
        }}
        .metricCard:hover {{
            border-color: {CorporateTheme.ACCENT_RED};
        }}
        .metricIcon {{
            font-size: 20px;
            color: {CorporateTheme.PRIMARY_NAVY};
        }}
        .metricLabel {{
            font-size: 13px;
            color: {CorporateTheme.SECONDARY_TEXT};
            font-weight: 500;
        }}
        .metricValue {{
            font-size: 22px;
            font-weight: 600;
            color: {CorporateTheme.PRIMARY_TEXT};
        }}
        .metricSubtext {{
            font-size: 12px;
            color: {CorporateTheme.MUTED_TEXT};
        }}
        .recentQuotesCard {{
            padding: 16px;
        }}
        .recentQuotesTitle {{
            font-size: 18px;
            font-weight: 600;
            color: {CorporateTheme.ACCENT_TEXT};
            margin-bottom: 8px;
        }}
        .noQuotesLabel {{
            font-size: 14px;
            color: {CorporateTheme.MUTED_TEXT};
            padding: 40px;
            border: 2px dashed {CorporateTheme.BORDER_COLOR};
            border-radius: 6px;
        }}
        .quoteItemCard {{
            background-color: {CorporateTheme.CARD_BG};
            border: 1px solid {CorporateTheme.BORDER_COLOR};
            border-radius: 6px;
            padding: 12px;
            margin: 4px 0;
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
            border-radius: 10px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-pending {{
            background-color: {CorporateTheme.WARNING_ORANGE};
            color: white;
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-draft {{
            background-color: {CorporateTheme.MUTED_TEXT};
            color: white;
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 500;
        }}
        .placeholderText {{
            color: {CorporateTheme.MUTED_TEXT};
            font-size: 14px;
            font-style: italic;
        }}
        """ + get_dashboard_stylesheet(CorporateTheme)

    # The STYLES dictionary and related methods are no longer needed
    # as dashboard styles are handled by get_dashboard_stylesheet.
    STYLES = {}

    @staticmethod
    def apply_stylesheet(widget, css_class):
        pass

    @staticmethod
    def apply_property_styles(widget, properties):
        pass 