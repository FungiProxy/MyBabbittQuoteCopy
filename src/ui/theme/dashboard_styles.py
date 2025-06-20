def get_dashboard_stylesheet(theme):
    """
    Generates the dashboard stylesheet for a given theme.
    """
    return f"""
    /* Custom classes for Dashboard */
    .metricCard {{
        background-color: {theme.CARD_BG};
        border: 1px solid {theme.BORDER_COLOR};
        border-radius: 8px;
        padding: 16px;
    }}
    .metricCard:hover {{
        border-color: {getattr(theme, 'ACCENT_GOLD', theme.PRIMARY_NAVY)};
    }}
    .metricIcon {{
        font-size: 20px;
        color: {getattr(theme, 'ACCENT_GOLD', theme.PRIMARY_NAVY)};
    }}
    .metricLabel {{
        font-size: 13px;
        color: {theme.SECONDARY_TEXT};
        font-weight: 500;
    }}
    .metricValue {{
        font-size: 22px;
        font-weight: 600;
        color: {theme.PRIMARY_TEXT};
    }}
    .metricSubtext {{
        font-size: 12px;
        color: {theme.MUTED_TEXT};
    }}
    .recentQuotesCard {{
        padding: 16px;
    }}
    .recentQuotesTitle {{
        font-size: 18px;
        font-weight: 600;
        color: {getattr(theme, 'PRIMARY_NAVY', theme.PRIMARY_NAVY)};
        margin-bottom: 8px;
    }}
    .noQuotesLabel {{
        font-size: 14px;
        color: {theme.MUTED_TEXT};
        padding: 40px;
        border: 2px dashed {theme.BORDER_COLOR};
        border-radius: 6px;
    }}
    .quoteItemCard {{
        background-color: {theme.CARD_BG};
        border: 1px solid {theme.BORDER_COLOR};
        border-radius: 6px;
        padding: 12px;
        margin: 4px 0;
    }}
    .quoteItemCard:hover {{
        border-color: {getattr(theme, 'ACCENT_GOLD', theme.PRIMARY_NAVY)};
    }}
    .quoteItemTitle {{
        font-weight: 600;
        color: {getattr(theme, 'PRIMARY_NAVY', theme.PRIMARY_NAVY)};
        font-size: 14px;
    }}
    .quoteItemDetails {{
        color: {theme.SECONDARY_TEXT};
        font-size: 12px;
    }}
    .status-sent {{
        background-color: {theme.SUCCESS_GREEN};
        color: white;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
    }}
    .status-pending {{
        background-color: {theme.WARNING_ORANGE};
        color: white;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
    }}
    .status-draft {{
        background-color: {theme.MUTED_TEXT};
        color: white;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 500;
    }}
    """ 