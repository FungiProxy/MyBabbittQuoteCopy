def get_dashboard_stylesheet(theme):
    """
    Generates the dashboard stylesheet for a given theme using standardized sizing.
    """
    return f"""
    /* ============================================================================
       DASHBOARD STYLES - STANDARDIZED
       ============================================================================ */
    
    /* Metric Cards */
    .metricCard {{
        background-color: {theme.BACKGROUND_CARD};
        border: 1px solid {theme.BORDER_COLOR};
        border-radius: 8px;
        padding: 16px;
    }}
    .metricCard:hover {{
        border-color: {theme.ACCENT_COLOR};
    }}
    .metricIcon {{
        font-size: 20px;
        color: {theme.ACCENT_COLOR};
    }}
    .metricLabel {{
        font-size: 13px;
        color: {theme.TEXT_SECONDARY};
        font-weight: 500;
    }}
    .metricValue {{
        font-size: 22px;
        font-weight: 600;
        color: {theme.TEXT_PRIMARY};
    }}
    .metricSubtext {{
        font-size: 12px;
        color: {theme.TEXT_MUTED};
    }}
    
    /* Recent Quotes Section */
    .recentQuotesCard {{
        padding: 16px;
    }}
    .recentQuotesTitle {{
        font-size: 18px;
        font-weight: 600;
        color: {theme.TEXT_PRIMARY};
        margin-bottom: 8px;
    }}
    .noQuotesLabel {{
        font-size: 14px;
        color: {theme.TEXT_MUTED};
        padding: 40px;
        border: 2px dashed {theme.BORDER_COLOR};
        border-radius: 6px;
    }}
    
    /* Quote Item Cards */
    .quoteItemCard {{
        background-color: {theme.BACKGROUND_CARD};
        border: 1px solid {theme.BORDER_COLOR};
        border-radius: 6px;
        padding: 12px;
        margin: 4px 0;
    }}
    .quoteItemCard:hover {{
        border-color: {theme.ACCENT_COLOR};
    }}
    .quoteItemTitle {{
        font-weight: 600;
        color: {theme.TEXT_PRIMARY};
        font-size: 14px;
    }}
    .quoteItemDetails {{
        color: {theme.TEXT_SECONDARY};
        font-size: 12px;
    }}
    
    /* Status Badges */
    .status-sent {{
        background-color: {theme.SUCCESS_COLOR};
        color: white;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
    }}
    .status-pending {{
        background-color: {theme.WARNING_COLOR};
        color: white;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
    }}
    .status-draft {{
        background-color: {theme.TEXT_MUTED};
        color: white;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
    }}
    """ 