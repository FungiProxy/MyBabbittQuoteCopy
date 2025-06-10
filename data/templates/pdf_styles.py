"""
PDF Styles Configuration Module

This module provides centralized styling constants for PDF document generation.
All measurements are in points (pt) unless otherwise specified.
ReportLab uses points where 1 inch = 72 points.

Usage:
    from data.templates.pdf_styles import COLORS, FONTS, PAGE_LAYOUT
    canvas.setFillColor(COLORS['primary'])
    canvas.setFont(FONTS['heading']['family'], FONTS['heading']['size'])
"""

from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# =============================================================================
# PAGE LAYOUT CONSTANTS
# =============================================================================

PAGE_LAYOUT = {
    # Page sizes (choose one as default)
    'page_size': letter,  # 8.5" x 11" (612 x 792 points)
    'page_size_a4': A4,   # Alternative: 210 x 297 mm (595 x 842 points)
    
    # Page dimensions in points
    'page_width': letter[0],   # 612 points
    'page_height': letter[1],  # 792 points
    
    # Margins (in points)
    'margin_top': 72,      # 1 inch
    'margin_bottom': 72,   # 1 inch  
    'margin_left': 72,     # 1 inch
    'margin_right': 72,    # 1 inch
    
    # Content area dimensions (page minus margins)
    'content_width': letter[0] - 144,   # 468 points (6.5 inches)
    'content_height': letter[1] - 144,  # 648 points (9 inches)
    
    # Header and footer zones
    'header_height': 60,
    'footer_height': 50,
    'header_margin_bottom': 12,
    'footer_margin_top': 12,
}

# =============================================================================
# TYPOGRAPHY SETTINGS
# =============================================================================

FONTS = {
    # Font families (ReportLab built-in fonts)
    'primary_family': 'Helvetica',
    'secondary_family': 'Times-Roman',
    'monospace_family': 'Courier',
    
    # Heading styles
    'company_name': {
        'family': 'Helvetica-Bold',
        'size': 24,
        'leading': 28,  # Line height
        'color': 'primary'
    },
    
    'document_title': {
        'family': 'Helvetica-Bold', 
        'size': 18,
        'leading': 22,
        'color': 'dark_gray'
    },
    
    'section_heading': {
        'family': 'Helvetica-Bold',
        'size': 14,
        'leading': 17,
        'color': 'primary'
    },
    
    'subsection_heading': {
        'family': 'Helvetica-Bold',
        'size': 12,
        'leading': 15,
        'color': 'dark_gray'
    },
    
    # Body text styles
    'body_text': {
        'family': 'Helvetica',
        'size': 10,
        'leading': 12,
        'color': 'black'
    },
    
    'body_text_small': {
        'family': 'Helvetica',
        'size': 9,
        'leading': 11,
        'color': 'dark_gray'
    },
    
    # Special text styles
    'emphasis': {
        'family': 'Helvetica-Bold',
        'size': 10,
        'leading': 12,
        'color': 'primary'
    },
    
    'currency': {
        'family': 'Helvetica-Bold',
        'size': 11,
        'leading': 13,
        'color': 'success'
    },
    
    'footer_text': {
        'family': 'Helvetica',
        'size': 8,
        'leading': 10,
        'color': 'medium_gray'
    },
    
    'watermark': {
        'family': 'Helvetica-Bold',
        'size': 48,
        'color': 'light_gray'
    }
}

# =============================================================================
# COLOR PALETTE
# =============================================================================

COLORS = {
    # Primary brand colors
    'primary': colors.Color(0.2, 0.4, 0.8),        # Professional blue
    'primary_light': colors.Color(0.4, 0.6, 0.9),  # Light blue
    'primary_dark': colors.Color(0.1, 0.2, 0.6),   # Dark blue
    
    # Secondary colors  
    'secondary': colors.Color(0.3, 0.7, 0.5),      # Professional green
    'accent': colors.Color(0.9, 0.6, 0.2),         # Orange accent
    
    # Status colors
    'success': colors.Color(0.2, 0.7, 0.3),        # Green for positive values
    'warning': colors.Color(0.9, 0.7, 0.1),        # Yellow for warnings
    'error': colors.Color(0.8, 0.2, 0.2),          # Red for errors
    'info': colors.Color(0.3, 0.6, 0.9),           # Blue for information
    
    # Grayscale
    'black': colors.black,
    'white': colors.white,
    'dark_gray': colors.Color(0.3, 0.3, 0.3),
    'medium_gray': colors.Color(0.5, 0.5, 0.5),
    'light_gray': colors.Color(0.8, 0.8, 0.8),
    'very_light_gray': colors.Color(0.95, 0.95, 0.95),
    
    # Table colors
    'table_header_bg': colors.Color(0.9, 0.9, 0.9),
    'table_alt_row_bg': colors.Color(0.98, 0.98, 0.98),
    'table_border': colors.Color(0.7, 0.7, 0.7),
    
    # Background colors
    'page_bg': colors.white,
    'section_bg': colors.Color(0.97, 0.97, 0.97),
}

# =============================================================================
# SPACING AND POSITIONING CONSTANTS  
# =============================================================================

SPACING = {
    # Vertical spacing (points)
    'line_spacing_tight': 1.0,
    'line_spacing_normal': 1.2,
    'line_spacing_loose': 1.5,
    
    # Section spacing
    'section_spacing_small': 6,   # Small gap between related items
    'section_spacing_medium': 12, # Medium gap between sections
    'section_spacing_large': 18,  # Large gap between major sections
    'section_spacing_xlarge': 24, # Extra large gap for page breaks
    
    # Paragraph spacing
    'paragraph_spacing_before': 6,
    'paragraph_spacing_after': 6,
    
    # List spacing
    'list_item_spacing': 4,
    'list_indent': 20,
    
    # Table spacing
    'table_cell_padding': 4,
    'table_row_height': 20,
    'table_margin_bottom': 12,
    
    # Border and rule spacing
    'rule_thickness': 0.5,
    'border_thickness': 1.0,
    'double_rule_spacing': 2,
}

# =============================================================================
# TABLE FORMATTING RULES
# =============================================================================

TABLE_STYLES = {
    # Standard table style
    'standard': {
        'background_color': COLORS['white'],
        'header_background': COLORS['table_header_bg'],
        'alt_row_background': COLORS['table_alt_row_bg'],
        'border_color': COLORS['table_border'],
        'border_width': 0.5,
        'cell_padding': SPACING['table_cell_padding'],
        'row_height': SPACING['table_row_height'],
        'font_name': FONTS['body_text']['family'],
        'font_size': FONTS['body_text']['size'],
        'header_font_name': FONTS['subsection_heading']['family'],
        'header_font_size': FONTS['subsection_heading']['size'],
        'text_color': COLORS['black'],
        'header_text_color': COLORS['dark_gray'],
        'alignment': TA_LEFT,
        'header_alignment': TA_CENTER,
    },
    
    # Quote items table style
    'quote_items': {
        'background_color': COLORS['white'],
        'header_background': COLORS['primary'],
        'alt_row_background': COLORS['very_light_gray'],
        'border_color': COLORS['primary_light'],
        'border_width': 1.0,
        'cell_padding': 6,
        'row_height': 24,
        'font_name': FONTS['body_text']['family'],
        'font_size': 10,
        'header_font_name': FONTS['emphasis']['family'],
        'header_font_size': 11,
        'text_color': COLORS['black'],
        'header_text_color': COLORS['white'],
        'currency_color': COLORS['success'],
        'alignment': TA_LEFT,
        'header_alignment': TA_CENTER,
        'currency_alignment': TA_RIGHT,
    },
    
    # Summary table style (totals, etc.)
    'summary': {
        'background_color': COLORS['section_bg'],
        'header_background': COLORS['primary_dark'],
        'border_color': COLORS['primary'],
        'border_width': 1.5,
        'cell_padding': 8,
        'row_height': 28,
        'font_name': FONTS['emphasis']['family'],
        'font_size': 11,
        'header_font_name': FONTS['emphasis']['family'],
        'header_font_size': 12,
        'text_color': COLORS['dark_gray'],
        'header_text_color': COLORS['white'],
        'total_color': COLORS['primary'],
        'alignment': TA_RIGHT,
        'header_alignment': TA_CENTER,
    }
}

# =============================================================================
# COMPANY BRANDING PLACEHOLDERS
# =============================================================================

COMPANY_BRANDING = {
    # Company information
    'company_name': 'Your Company Name',
    'company_tagline': 'Professional Solutions & Services',
    'company_address': [
        '123 Business Street',
        'Suite 100', 
        'City, State 12345'
    ],
    'company_contact': {
        'phone': '(555) 123-4567',
        'email': 'info@yourcompany.com',
        'website': 'www.yourcompany.com',
        'fax': '(555) 123-4568'  # Optional
    },
    
    # Logo settings
    'logo': {
        'path': 'data/templates/logo.png',  # Path to logo file
        'width': 120,   # Logo width in points
        'height': 40,   # Logo height in points
        'position': 'top_left',  # 'top_left', 'top_center', 'top_right'
        'margin_right': 20,  # Space between logo and text
    },
    
    # Watermark settings
    'watermark': {
        'text': 'CONFIDENTIAL',  # Set to None to disable
        'opacity': 0.1,
        'rotation': 45,  # Degrees
        'position': 'center',  # 'center', 'top_left', etc.
    },
    
    # Document footer
    'footer': {
        'left_text': '© 2024 Your Company Name',
        'center_text': 'CONFIDENTIAL',
        'right_text': 'Page {page} of {total_pages}',
        'include_date': True,
        'include_time': False,
    }
}

# =============================================================================
# DOCUMENT TYPE SPECIFIC SETTINGS
# =============================================================================

DOCUMENT_TYPES = {
    'quote': {
        'title': 'PRICE QUOTE',
        'watermark_text': 'QUOTE',
        'color_scheme': 'primary',  # Uses primary colors
        'show_validity_period': True,
        'show_terms_conditions': True,
        'footer_disclaimer': 'This quote is valid for 30 days from the date issued.',
    },
    
    'invoice': {
        'title': 'INVOICE',
        'watermark_text': 'INVOICE',
        'color_scheme': 'success',  # Uses success (green) colors
        'show_payment_terms': True,
        'show_due_date': True,
        'footer_disclaimer': 'Payment is due within 30 days of invoice date.',
    },
    
    'estimate': {
        'title': 'ESTIMATE',
        'watermark_text': 'ESTIMATE',
        'color_scheme': 'info',     # Uses info (blue) colors
        'show_validity_period': True,
        'show_assumptions': True,
        'footer_disclaimer': 'This estimate is preliminary and subject to final confirmation.',
    },
    
    'proposal': {
        'title': 'PROPOSAL',
        'watermark_text': 'PROPOSAL',
        'color_scheme': 'secondary', # Uses secondary (green) colors
        'show_executive_summary': True,
        'show_detailed_scope': True,
        'footer_disclaimer': 'This proposal is confidential and proprietary.',
    }
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_color(color_name):
    """
    Get a color object by name from the COLORS palette.
    
    Args:
        color_name (str): Name of the color from COLORS dictionary
        
    Returns:
        reportlab.lib.colors.Color: Color object
    """
    return COLORS.get(color_name, COLORS['black'])

def get_font_style(style_name):
    """
    Get font style dictionary by name.
    
    Args:
        style_name (str): Name of the font style from FONTS dictionary
        
    Returns:
        dict: Font style configuration
    """
    return FONTS.get(style_name, FONTS['body_text'])

def get_table_style(style_name):
    """
    Get table style configuration by name.
    
    Args:
        style_name (str): Name of the table style from TABLE_STYLES dictionary
        
    Returns:
        dict: Table style configuration
    """
    return TABLE_STYLES.get(style_name, TABLE_STYLES['standard'])

def get_document_config(doc_type):
    """
    Get document type specific configuration.
    
    Args:
        doc_type (str): Type of document ('quote', 'invoice', 'estimate', 'proposal')
        
    Returns:
        dict: Document configuration
    """
    return DOCUMENT_TYPES.get(doc_type, DOCUMENT_TYPES['quote'])

def points_to_inches(points):
    """Convert points to inches (1 inch = 72 points)."""
    return points / 72.0

def inches_to_points(inches):
    """Convert inches to points (1 inch = 72 points)."""
    return inches * 72.0

def mm_to_points(millimeters):
    """Convert millimeters to points."""
    return millimeters * 72.0 / 25.4

def points_to_mm(points):
    """Convert points to millimeters."""
    return points * 25.4 / 72.0

# =============================================================================
# EXPORT ALL CONSTANTS
# =============================================================================

__all__ = [
    'PAGE_LAYOUT',
    'FONTS', 
    'COLORS',
    'SPACING',
    'TABLE_STYLES',
    'COMPANY_BRANDING',
    'DOCUMENT_TYPES',
    'get_color',
    'get_font_style', 
    'get_table_style',
    'get_document_config',
    'points_to_inches',
    'inches_to_points',
    'mm_to_points',
    'points_to_mm'
]