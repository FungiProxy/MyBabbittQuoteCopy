"""
Modern styling constants and helper functions for the BabbittQuote application
"""

# Color palette
COLORS = {
    # Primary colors
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',
    'primary_pressed': '#1e40af',
    
    # Secondary colors
    'secondary': '#f8fafc',
    'secondary_hover': '#f1f5f9',
    'secondary_pressed': '#e2e8f0',
    
    # Danger colors
    'danger': '#dc2626',
    'danger_hover': '#b91c1c',
    'danger_pressed': '#991b1b',
    
    # Success colors
    'success': '#059669',
    'success_light': '#d1fae5',
    
    # Warning colors
    'warning': '#92400e',
    'warning_light': '#fef3c7',
    
    # Neutral colors
    'gray_50': '#f8fafc',
    'gray_100': '#f1f5f9',
    'gray_200': '#e2e8f0',
    'gray_300': '#cbd5e1',
    'gray_400': '#94a3b8',
    'gray_500': '#64748b',
    'gray_600': '#475569',
    'gray_700': '#334155',
    'gray_800': '#1e293b',
    'gray_900': '#0f172a',
    
    # Text colors
    'text_primary': '#1e293b',
    'text_secondary': '#475569',
    'text_muted': '#6b7280',
    
    # Background colors
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'bg_sidebar': '#1e293b',
    'bg_sidebar_header': '#0f172a',
    
    # Border colors
    'border_light': '#e2e8f0',
    'border_medium': '#cbd5e1',
}

# Typography
FONTS = {
    'family': 'Segoe UI',
    'sizes': {
        'xs': 10,
        'sm': 11,
        'base': 12,
        'lg': 14,
        'xl': 16,
        '2xl': 18,
        '3xl': 24,
        '4xl': 32,
    },
    'weights': {
        'normal': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700,
    }
}

# Spacing
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 20,
    '2xl': 24,
    '3xl': 32,
    '4xl': 48,
}

# Border radius
RADIUS = {
    'sm': 4,
    'md': 8,
    'lg': 12,
    'xl': 16,
    'full': 9999,
}

# Shadows
SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
}

def get_button_style(button_type='primary'):
    """Generate button stylesheet based on type"""
    styles = {
        'primary': f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px {SPACING['2xl']}px;
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['base']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_pressed']};
            }}
        """,
        'secondary': f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_secondary']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px {SPACING['2xl']}px;
                font-weight: {FONTS['weights']['medium']};
                font-size: {FONTS['sizes']['base']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
                border-color: {COLORS['border_medium']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['secondary_pressed']};
            }}
        """,
        'danger': f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: white;
                border: none;
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px {SPACING['2xl']}px;
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['base']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['danger_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['danger_pressed']};
            }}
        """
    }
    return styles.get(button_type, styles['primary'])

def get_input_style():
    """Generate input field stylesheet"""
    return f"""
        QLineEdit {{
            border: 2px solid {COLORS['border_light']};
            border-radius: {RADIUS['md']}px;
            padding: {SPACING['md']}px {SPACING['lg']}px;
            background-color: {COLORS['bg_primary']};
            font-size: {FONTS['sizes']['lg']}px;
            color: {COLORS['text_primary']};
        }}
        QLineEdit:focus {{
            border-color: {COLORS['primary']};
            outline: none;
        }}
        QLineEdit:hover {{
            border-color: {COLORS['border_medium']};
        }}
    """

def get_card_style():
    """Generate card/panel stylesheet"""
    return f"""
        QWidget {{
            background-color: {COLORS['bg_primary']};
            border-radius: {RADIUS['lg']}px;
            border: 1px solid {COLORS['border_light']};
        }}
    """

def get_table_style():
    """Generate table stylesheet"""
    return f"""
        QTableWidget {{
            border: 1px solid {COLORS['border_light']};
            border-radius: {RADIUS['md']}px;
            background-color: {COLORS['bg_primary']};
            gridline-color: {COLORS['gray_100']};
        }}
        QHeaderView::section {{
            background-color: {COLORS['gray_50']};
            border: none;
            border-bottom: 2px solid {COLORS['border_light']};
            padding: {SPACING['lg']}px {SPACING['md']}px;
            font-weight: {FONTS['weights']['semibold']};
            color: {COLORS['text_primary']};
            font-size: {FONTS['sizes']['base']}px;
        }}
        QTableWidget::item {{
            padding: {SPACING['lg']}px {SPACING['md']}px;
            border-bottom: 1px solid {COLORS['gray_100']};
        }}
        QTableWidget::item:selected {{
            background-color: #eff6ff;
            color: {COLORS['primary_pressed']};
        }}
    """