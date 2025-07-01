"""
Phone number formatting utilities.

This module provides functions for formatting phone numbers to the standard
(XXX) XXX-XXXX format used in the United States.
"""

import re
from typing import Optional


def format_phone_number(phone: Optional[str]) -> Optional[str]:
    """
    Format a phone number to (XXX) XXX-XXXX format.
    
    Args:
        phone: Phone number string (can contain digits, spaces, dashes, dots, parentheses)
        
    Returns:
        Formatted phone number as (XXX) XXX-XXXX or None if invalid/empty
        
    Examples:
        >>> format_phone_number("5551234567")
        "(555) 123-4567"
        >>> format_phone_number("555-123-4567")
        "(555) 123-4567"
        >>> format_phone_number("(555) 123-4567")
        "(555) 123-4567"
        >>> format_phone_number("555.123.4567")
        "(555) 123-4567"
        >>> format_phone_number("")
        None
        >>> format_phone_number("123")
        None
    """
    if not phone:
        return None
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if we have exactly 10 digits (US phone number)
    if len(digits_only) != 10:
        return None
    
    # Format as (XXX) XXX-XXXX
    return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"


def is_valid_phone_number(phone: Optional[str]) -> bool:
    """
    Check if a phone number is valid (10 digits).
    
    Args:
        phone: Phone number string to validate
        
    Returns:
        True if valid, False otherwise
        
    Examples:
        >>> is_valid_phone_number("5551234567")
        True
        >>> is_valid_phone_number("555-123-4567")
        True
        >>> is_valid_phone_number("123")
        False
        >>> is_valid_phone_number("")
        False
    """
    if not phone:
        return False
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if we have exactly 10 digits
    return len(digits_only) == 10


def clean_phone_number(phone: Optional[str]) -> Optional[str]:
    """
    Clean a phone number by removing all non-digit characters.
    
    Args:
        phone: Phone number string to clean
        
    Returns:
        Cleaned phone number (digits only) or None if empty
        
    Examples:
        >>> clean_phone_number("(555) 123-4567")
        "5551234567"
        >>> clean_phone_number("555-123-4567")
        "5551234567"
        >>> clean_phone_number("")
        None
    """
    if not phone:
        return None
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    return digits_only if digits_only else None 