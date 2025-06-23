"""
Babbitt Industrial Professional Theme - PySide6 Compatible
File: src/ui/theme/babbitt_industrial_theme.py

🔴 Critical - Professional theme with uniform sizing, proper spacing, and PySide6 compatibility
No CSS effects that aren't supported - focused on clean, structured layouts
"""


class BabbittIndustrialProfessional:
    """
    Professional industrial theme for MyBabbittQuote application.
    Based on Babbitt International website colors with uniform sizing and spacing.
    Fully compatible with PySide6 - no unsupported CSS effects.
    """
    
    # ============================================================================
    # BABBITT INTERNATIONAL COLOR SCHEME - WEBSITE ACCURATE
    # ============================================================================
    
    # Primary Blues - From Babbitt International Website
    PRIMARY_BLUE = "#0052cc"         # Bright blue (buttons, links, active states)
    SECONDARY_BLUE = "#003d99"       # Darker blue (hover states)
    ACCENT_BLUE = "#0066ff"          # Bright accent blue
    NAVY_BLUE = "#1a237e"            # Deep navy for headers
    
    # Industrial Grays - Professional Hierarchy
    CHARCOAL = "#1a1a1a"             # Sidebar background
    DARK_GRAY = "#2c2c2c"            # Secondary dark
    MEDIUM_GRAY = "#6c757d"          # Secondary text
    LIGHT_GRAY = "#adb5bd"           # Muted text
    BORDER_GRAY = "#dee2e6"          # Borders
    
    # Clean Whites and Backgrounds
    PURE_WHITE = "#ffffff"           # Cards, forms, content
    OFF_WHITE = "#fafbfc"            # Page backgrounds
    CARD_WHITE = "#ffffff"           # Card backgrounds
    SURFACE_GRAY = "#f8f9fa"         # Panel backgrounds
    
    # Status Colors - Industrial Standards
    SUCCESS_GREEN = "#28a745"        # Success states
    WARNING_YELLOW = "#ffc107"       # Warning states  
    ERROR_RED = "#dc3545"            # Error states
    INFO_BLUE = "#17a2b8"            # Info states
    
    # ============================================================================
    # STANDARDIZED SPACING SYSTEM - UNIFORM ACROSS APPLICATION
    # ============================================================================
    
    # Base spacing unit
    SPACE_UNIT = 8
    
    # Spacing scale (all measurements in pixels)
    SPACE_XS = "4px"    # 0.5 units
    SPACE_SM = "8px"    # 1 unit
    SPACE_MD = "12px"   # 1.5 units
    SPACE_LG = "16px"   # 2 units
    SPACE_XL = "20px"   # 2.5 units
    SPACE_2XL = "24px"  # 3 units
    SPACE_3XL = "32px"  # 4 units
    SPACE_4XL = "40px"  # 5 units
    
    # Component-specific spacing
    CARD_PADDING = "20px"
    FORM_SPACING = "12px"
    SECTION_SPACING = "24px"
    PAGE_MARGIN = "20px"
    
    # ============================================================================
    # STANDARDIZED SIZING SYSTEM - CONSISTENT PROPORTIONS
    # ============================================================================
    
    # Input field heights (consistent across all form elements)
    INPUT_HEIGHT = "36px"
    BUTTON_HEIGHT = "40px"
    SMALL_BUTTON_HEIGHT = "32px"
    LARGE_BUTTON_HEIGHT = "48px"
    
    # Container widths
    SIDEBAR_WIDTH = "200px"
    CONTENT_MAX_WIDTH = "1200px"
    FORM_MAX_WIDTH = "600px"
    CARD_MAX_WIDTH = "400px"
    
    # Font sizes (responsive scale)
    FONT_XS = "11px"
    FONT_SM = "12px"
    FONT_BASE = "14px"
    FONT_LG = "16px"
    FONT_XL = "18px"
    FONT_2XL = "20px"
    FONT_3XL = "24px"
    FONT_4XL = "28px"
    
    # Border radius (consistent rounding)
    RADIUS_SM = "4px"
    RADIUS_MD = "6px"
    RADIUS_LG = "8px"
    RADIUS_XL = "12px"
    
    @staticmethod
    def get_main_stylesheet():
        """
        Main stylesheet with uniform sizing, proper spacing, and PySide6 compatibility.
        No unsupported CSS effects - focus on clean, professional layout.
        """
        return f"""
        /* ========================================================================
           BABBITT INDUSTRIAL PROFESSIONAL THEME
           Clean, uniform styling with proper spacing and sizing
        ======================================================================== */
        
        /* ====== GLOBAL FOUNDATION ====== */
        QMainWindow {{
            background-color: {BabbittIndustrialProfessional.OFF_WHITE};
            color: #333333;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: {BabbittIndustrialProfessional.FONT_BASE};
        }}
        
        QDialog {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 2px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_LG};
        }}
        
        /* ====== SIDEBAR - INDUSTRIAL DARK THEME ====== */
        QFrame#sidebarFrame {{
            background-color: {BabbittIndustrialProfessional.CHARCOAL};
            border: none;
            border-right: 1px solid {BabbittIndustrialProfessional.DARK_GRAY};
            min-width: {BabbittIndustrialProfessional.SIDEBAR_WIDTH};
            max-width: {BabbittIndustrialProfessional.SIDEBAR_WIDTH};
        }}
        
        /* Logo styling */
        QLabel#logoLabel {{
            color: {BabbittIndustrialProfessional.PURE_WHITE};
            font-size: {BabbittIndustrialProfessional.FONT_XL};
            font-weight: 700;
            padding: {BabbittIndustrialProfessional.SPACE_2XL} {BabbittIndustrialProfessional.SPACE_LG};
            margin-bottom: {BabbittIndustrialProfessional.SPACE_MD};
            border-bottom: 1px solid {BabbittIndustrialProfessional.DARK_GRAY};
        }}
        
        /* Navigation list */
        QListWidget#navList {{
            background-color: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.9);
            font-size: {BabbittIndustrialProfessional.FONT_BASE};
            font-weight: 500;
            outline: none;
            padding: {BabbittIndustrialProfessional.SPACE_SM} 0;
        }}
        
        QListWidget#navList::item {{
            padding: {BabbittIndustrialProfessional.SPACE_MD} {BabbittIndustrialProfessional.SPACE_LG};
            margin: {BabbittIndustrialProfessional.SPACE_XS} {BabbittIndustrialProfessional.SPACE_SM} {BabbittIndustrialProfessional.SPACE_XS} 0;
            border-radius: 0 {BabbittIndustrialProfessional.RADIUS_MD} {BabbittIndustrialProfessional.RADIUS_MD} 0;
            border-left: 3px solid transparent;
        }}
        
        QListWidget#navList::item:hover {{
            background-color: rgba(255, 255, 255, 0.1);
            color: {BabbittIndustrialProfessional.PURE_WHITE};
        }}
        
        QListWidget#navList::item:selected {{
            background-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            border-left: 3px solid {BabbittIndustrialProfessional.ACCENT_BLUE};
            color: {BabbittIndustrialProfessional.PURE_WHITE};
            font-weight: 600;
        }}
        
        /* Settings button */
        QPushButton#settingsButton {{
            background-color: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            padding: {BabbittIndustrialProfessional.SPACE_MD} {BabbittIndustrialProfessional.SPACE_LG};
            margin: {BabbittIndustrialProfessional.SPACE_LG} {BabbittIndustrialProfessional.SPACE_MD} {BabbittIndustrialProfessional.SPACE_XL} {BabbittIndustrialProfessional.SPACE_MD};
            font-size: {BabbittIndustrialProfessional.FONT_SM};
            font-weight: 500;
            min-height: {BabbittIndustrialProfessional.SMALL_BUTTON_HEIGHT};
        }}
        
        QPushButton#settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
            color: {BabbittIndustrialProfessional.PURE_WHITE};
        }}
        
        /* ====== CONTENT AREA - CLEAN WHITE LAYOUT ====== */
        QFrame#contentAreaFrame {{
            background-color: {BabbittIndustrialProfessional.OFF_WHITE};
            border: none;
        }}
        
        /* Content header */
        QFrame#contentHeader {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: none;
            border-bottom: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            min-height: 70px;
            max-height: 70px;
        }}
        
        /* Page titles */
        QLabel#pageTitle {{
            color: #2c3e50;
            font-size: {BabbittIndustrialProfessional.FONT_4XL};
            font-weight: 700;
            margin: 0;
            padding: 0;
        }}
        
        /* ====== STANDARDIZED BUTTONS ====== */
        QPushButton {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            color: #495057;
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            padding: {BabbittIndustrialProfessional.SPACE_SM} {BabbittIndustrialProfessional.SPACE_LG};
            font-size: {BabbittIndustrialProfessional.FONT_BASE};
            font-weight: 500;
            min-height: {BabbittIndustrialProfessional.BUTTON_HEIGHT};
            max-height: {BabbittIndustrialProfessional.BUTTON_HEIGHT};
        }}
        
        QPushButton:hover {{
            background-color: {BabbittIndustrialProfessional.SURFACE_GRAY};
            border-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
        }}
        
        QPushButton:pressed {{
            background-color: {BabbittIndustrialProfessional.BORDER_GRAY};
        }}
        
        /* Primary buttons (CTAs) */
        QPushButton[class="primary"], QPushButton#newQuoteBtn {{
            background-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.PRIMARY_BLUE};
            font-weight: 600;
        }}
        
        QPushButton[class="primary"]:hover, QPushButton#newQuoteBtn:hover {{
            background-color: {BabbittIndustrialProfessional.SECONDARY_BLUE};
            border-color: {BabbittIndustrialProfessional.SECONDARY_BLUE};
        }}
        
        /* Secondary buttons */
        QPushButton[class="secondary"] {{
            background-color: transparent;
            color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            border: 1px solid {BabbittIndustrialProfessional.PRIMARY_BLUE};
        }}
        
        QPushButton[class="secondary"]:hover {{
            background-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            color: {BabbittIndustrialProfessional.PURE_WHITE};
        }}
        
        /* Danger buttons */
        QPushButton[class="danger"] {{
            background-color: {BabbittIndustrialProfessional.ERROR_RED};
            color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.ERROR_RED};
        }}
        
        QPushButton[class="danger"]:hover {{
            background-color: #c82333;
            border-color: #c82333;
        }}
        
        /* ====== STANDARDIZED FORM ELEMENTS ====== */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            padding: {BabbittIndustrialProfessional.SPACE_SM} {BabbittIndustrialProfessional.SPACE_MD};
            color: #495057;
            font-size: {BabbittIndustrialProfessional.FONT_BASE};
            min-height: 20px;
            max-height: {BabbittIndustrialProfessional.INPUT_HEIGHT};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            outline: none;
        }}
        
        QTextEdit, QPlainTextEdit {{
            min-height: 80px;
            max-height: 120px;
        }}
        
        /* Consistent ComboBox styling */
        QComboBox {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            padding: {BabbittIndustrialProfessional.SPACE_SM} {BabbittIndustrialProfessional.SPACE_MD};
            color: #495057;
            font-size: {BabbittIndustrialProfessional.FONT_BASE};
            min-height: 20px;
            max-height: {BabbittIndustrialProfessional.INPUT_HEIGHT};
        }}
        
        QComboBox:hover {{
            border-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
        }}
        
        QComboBox:focus {{
            border-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-top-right-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            border-bottom-right-radius: {BabbittIndustrialProfessional.RADIUS_MD};
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {BabbittIndustrialProfessional.MEDIUM_GRAY};
            width: 0;
            height: 0;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            selection-background-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            selection-color: {BabbittIndustrialProfessional.PURE_WHITE};
        }}
        
        QComboBox QAbstractItemView::item {{
            padding: {BabbittIndustrialProfessional.SPACE_SM} {BabbittIndustrialProfessional.SPACE_MD};
            min-height: 28px;
        }}
        
        /* ====== CARDS AND CONTAINERS ====== */
        QGroupBox {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_LG};
            margin-top: {BabbittIndustrialProfessional.SPACE_LG};
            padding-top: {BabbittIndustrialProfessional.SPACE_LG};
            font-weight: 600;
            color: #2c3e50;
            font-size: {BabbittIndustrialProfessional.FONT_LG};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {BabbittIndustrialProfessional.SPACE_LG};
            padding: 0 {BabbittIndustrialProfessional.SPACE_SM} 0 {BabbittIndustrialProfessional.SPACE_SM};
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            font-weight: 600;
        }}
        
        /* Frame cards */
        QFrame[class="card"] {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_LG};
            padding: {BabbittIndustrialProfessional.CARD_PADDING};
        }}
        
        /* ====== TABLES AND LISTS ====== */
        QListWidget, QTreeWidget {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            alternate-background-color: {BabbittIndustrialProfessional.SURFACE_GRAY};
            font-size: {BabbittIndustrialProfessional.FONT_BASE};
        }}
        
        QListWidget::item, QTreeWidget::item {{
            padding: {BabbittIndustrialProfessional.SPACE_MD};
            border-radius: {BabbittIndustrialProfessional.RADIUS_SM};
            margin: {BabbittIndustrialProfessional.SPACE_XS};
        }}
        
        QListWidget::item:hover, QTreeWidget::item:hover {{
            background-color: {BabbittIndustrialProfessional.SURFACE_GRAY};
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected {{
            background-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            color: {BabbittIndustrialProfessional.PURE_WHITE};
        }}
        
        QTableWidget {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            gridline-color: {BabbittIndustrialProfessional.BORDER_GRAY};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
        }}
        
        QHeaderView::section {{
            background-color: {BabbittIndustrialProfessional.SURFACE_GRAY};
            color: #495057;
            padding: {BabbittIndustrialProfessional.SPACE_MD};
            border: none;
            border-bottom: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            font-weight: 600;
            font-size: {BabbittIndustrialProfessional.FONT_SM};
        }}
        
        /* ====== TAB WIDGET STYLING ====== */
        QTabWidget::pane {{
            background-color: {BabbittIndustrialProfessional.PURE_WHITE};
            border: 1px solid {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: {BabbittIndustrialProfessional.RADIUS_MD};
        }}
        
        QTabBar::tab {{
            background-color: {BabbittIndustrialProfessional.SURFACE_GRAY};
            color: #6c757d;
            padding: {BabbittIndustrialProfessional.SPACE_MD} {BabbittIndustrialProfessional.SPACE_XL};
            margin-right: 2px;
            border-top-left-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            border-top-right-radius: {BabbittIndustrialProfessional.RADIUS_MD};
            font-weight: 500;
            min-height: {BabbittIndustrialProfessional.SMALL_BUTTON_HEIGHT};
        }}
        
        QTabBar::tab:selected {{
            background-color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
            color: {BabbittIndustrialProfessional.PURE_WHITE};
            font-weight: 600;
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {BabbittIndustrialProfessional.BORDER_GRAY};
            color: {BabbittIndustrialProfessional.PRIMARY_BLUE};
        }}
        
        /* ====== SCROLLBARS ====== */
        QScrollBar:vertical {{
            background-color: {BabbittIndustrialProfessional.SURFACE_GRAY};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {BabbittIndustrialProfessional.BORDER_GRAY};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {BabbittIndustrialProfessional.MEDIUM_GRAY};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* ====== STATUS INDICATORS ====== */
        QLabel[status="success"] {{
            color: {BabbittIndustrialProfessional.SUCCESS_GREEN};
            font-weight: 600;
        }}
        
        QLabel[status="warning"] {{
            color: {BabbittIndustrialProfessional.WARNING_YELLOW};
            font-weight: 600;
        }}
        
        QLabel[status="error"] {{
            color: {BabbittIndustrialProfessional.ERROR_RED};
            font-weight: 600;
        }}
        
        QLabel[status="info"] {{
            color: {BabbittIndustrialProfessional.INFO_BLUE};
            font-weight: 600;
        }}
        """


# ============================================================================
# LAYOUT STANDARDS FOR UNIFORM SIZING
# ============================================================================

class LayoutStandards:
    """Standardized layout settings for consistent sizing across the application."""
    
    @staticmethod
    def apply_standard_form_layout(form_layout):
        """Apply standard spacing to form layouts."""
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setFieldGrowthPolicy(form_layout.ExpandingFieldsGrow)
    
    @staticmethod
    def apply_standard_container_layout(layout):
        """Apply standard spacing to container layouts."""
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
    
    @staticmethod
    def apply_card_layout(layout):
        """Apply standard spacing to card layouts."""
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
    
    @staticmethod
    def set_standard_input_height(widget):
        """Set standard height for input widgets."""
        widget.setMinimumHeight(36)
        widget.setMaximumHeight(36)
    
    @staticmethod
    def set_standard_button_height(widget):
        """Set standard height for buttons."""
        widget.setMinimumHeight(40)
        widget.setMaximumHeight(40)


# ============================================================================
# ENHANCED SETTINGS OPTIONS
# ============================================================================

class SettingsConfiguration:
    """Comprehensive settings options for the application."""
    
    @staticmethod
    def get_general_settings():
        """Return general application settings."""
        return {
            'theme': {
                'display_name': 'Application Theme',
                'type': 'dropdown',
                'options': ['Babbitt Industrial', 'Corporate Blue', 'Classic'],
                'default': 'Babbitt Industrial'
            },
            'startup_page': {
                'display_name': 'Startup Page',
                'type': 'dropdown', 
                'options': ['Dashboard', 'Quote Creator', 'Customers'],
                'default': 'Dashboard'
            },
            'auto_save': {
                'display_name': 'Auto-save drafts',
                'type': 'checkbox',
                'default': True
            },
            'confirm_delete': {
                'display_name': 'Confirm before deleting',
                'type': 'checkbox',
                'default': True
            }
        }
    
    @staticmethod
    def get_quote_settings():
        """Return quote-specific settings."""
        return {
            'default_currency': {
                'display_name': 'Default Currency',
                'type': 'dropdown',
                'options': ['USD', 'CAD', 'EUR', 'GBP'],
                'default': 'USD'
            },
            'quote_validity_days': {
                'display_name': 'Quote Valid For (days)',
                'type': 'number',
                'default': 30,
                'min': 1,
                'max': 365
            },
            'include_tax': {
                'display_name': 'Include tax in pricing',
                'type': 'checkbox',
                'default': False
            },
            'default_tax_rate': {
                'display_name': 'Default Tax Rate (%)',
                'type': 'number',
                'default': 0,
                'min': 0,
                'max': 50
            }
        }
    
    @staticmethod
    def get_export_settings():
        """Return export-specific settings."""
        return {
            'default_export_path': {
                'display_name': 'Default Export Location',
                'type': 'folder',
                'default': ''
            },
            'include_logo': {
                'display_name': 'Include company logo',
                'type': 'checkbox',
                'default': True
            },
            'pdf_format': {
                'display_name': 'PDF Format',
                'type': 'dropdown',
                'options': ['Standard', 'Detailed', 'Summary'],
                'default': 'Standard'
            },
            'email_template': {
                'display_name': 'Default Email Template',
                'type': 'dropdown',
                'options': ['Professional', 'Formal', 'Friendly'],
                'default': 'Professional'
            }
        }
    
    @staticmethod 
    def get_company_settings():
        """Return company information settings."""
        return {
            'company_name': {
                'display_name': 'Company Name',
                'type': 'text',
                'default': 'Babbitt International'
            },
            'company_address': {
                'display_name': 'Company Address',
                'type': 'textarea',
                'default': ''
            },
            'company_phone': {
                'display_name': 'Phone Number',
                'type': 'text',
                'default': ''
            },
            'company_email': {
                'display_name': 'Email Address',
                'type': 'text',
                'default': ''
            },
            'company_website': {
                'display_name': 'Website',
                'type': 'text',
                'default': 'https://www.babbittinternational.com'
            }
        }


# ============================================================================
# INTEGRATION HELPER
# ============================================================================

class BabbittProfessionalIntegration:
    """Integration helper for applying the professional theme."""
    
    @staticmethod
    def apply_theme_to_application(app):
        """Apply the theme to the entire application."""
        stylesheet = BabbittIndustrialProfessional.get_main_stylesheet()
        app.setStyleSheet(stylesheet)
        print("🏭 Babbitt Industrial Professional Theme Applied")
        print("   ✅ Uniform sizing and spacing")
        print("   ✅ PySide6 compatible styling")
        print("   ✅ Babbitt International colors")
        print("   ✅ Professional layout standards")
    
    @staticmethod
    def apply_standard_layout_to_widget(widget):
        """Apply standard layout settings to any widget."""
        # Apply to all form layouts
        for form_layout in widget.findChildren(widget.QFormLayout):
            LayoutStandards.apply_standard_form_layout(form_layout)
        
        # Apply to container layouts
        for layout in widget.findChildren(widget.QVBoxLayout):
            LayoutStandards.apply_standard_container_layout(layout)
        
        # Set standard heights for inputs and buttons
        for input_widget in widget.findChildren((widget.QLineEdit, widget.QComboBox)):
            LayoutStandards.set_standard_input_height(input_widget)
        
        for button in widget.findChildren(widget.QPushButton):
            LayoutStandards.set_standard_button_height(button)


# ============================================================================
# COMPATIBILITY ALIASES
# ============================================================================

# Alias for compatibility with existing main_window.py
BabbittPremiumIntegration = BabbittProfessionalIntegration


# ============================================================================
# QUICK IMPLEMENTATION INSTRUCTIONS
# ============================================================================
"""
🔴 IMPLEMENTATION STEPS (Easy integration with your existing code):

1. Replace your theme file:
   📁 src/ui/theme/babbitt_industrial_professional.py

2. Update your MainWindow theme application:
   
   # In your MainWindow.__init__ or apply_theme method:
   from src.ui.theme.babbitt_industrial_professional import BabbittIndustrialProfessional
   
   def _apply_theme(self, theme_name):
       if theme_name == "Babbitt Industrial":
           self.setStyleSheet(BabbittIndustrialProfessional.get_main_stylesheet())

3. Apply standard layouts (optional but recommended):
   
   # In any widget initialization:
   from src.ui.theme.babbitt_industrial_professional import LayoutStandards
   
   # For forms:
   LayoutStandards.apply_standard_form_layout(your_form_layout)
   
   # For containers:
   LayoutStandards.apply_standard_container_layout(your_container_layout)

4. Enhanced settings (see next artifact for complete settings page):
   - Replace your settings page with enhanced version
   - Includes all core options for quote applications
   - Organized in logical tabs with proper spacing

✅ BENEFITS:
- No unsupported CSS effects
- Uniform 36px input height across all forms  
- Consistent 40px button height
- Standardized 20px padding on cards
- 12px spacing between form elements
- Babbitt International website-accurate colors
- Professional industrial styling throughout
"""