#!/usr/bin/env python3
"""
Unit tests for modern UI components.

This script tests the functionality of our modern components
without requiring a GUI, ensuring they work correctly.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Import our components
from src.ui.components import (
    StatusBadge, Card, SearchBar, PriceDisplay, 
    LoadingSpinner, EmptyState, Notification
)

# Import styling system
from src.ui.theme import COLORS, FONTS, SPACING, RADIUS


def test_status_badge():
    """Test StatusBadge component functionality."""
    print("🧪 Testing StatusBadge component...")
    
    badge = StatusBadge("Test", "draft")
    
    # Test initial state
    assert badge.text() == "Test"
    assert badge.status_type == "draft"
    
    # Test status change
    badge.set_status("active")
    assert badge.status_type == "active"
    
    # Test text change
    badge.set_text("Updated")
    assert badge.text() == "Updated"
    
    print("✅ StatusBadge tests passed!")


def test_card():
    """Test Card component functionality."""
    print("🧪 Testing Card component...")
    
    card = Card("Test Card")
    
    # Test initial state
    assert card.title == "Test Card"
    
    # Test title change
    card.set_title("Updated Card")
    assert card.title == "Updated Card"
    
    # Test content management
    from PySide6.QtWidgets import QLabel
    test_label = QLabel("Test content")
    card.add_widget(test_label)
    
    print("✅ Card tests passed!")


def test_search_bar():
    """Test SearchBar component functionality."""
    print("🧪 Testing SearchBar component...")
    
    search_bar = SearchBar("Test placeholder")
    
    # Test initial state
    assert search_bar.get_text() == ""
    assert search_bar.search_input.placeholderText() == "Test placeholder"
    
    # Test text setting
    search_bar.set_text("test search")
    assert search_bar.get_text() == "test search"
    
    # Test clearing
    search_bar.clear()
    assert search_bar.get_text() == ""
    
    # Test placeholder change
    search_bar.set_placeholder("New placeholder")
    assert search_bar.search_input.placeholderText() == "New placeholder"
    
    print("✅ SearchBar tests passed!")


def test_price_display():
    """Test PriceDisplay component functionality."""
    print("🧪 Testing PriceDisplay component...")
    
    price = PriceDisplay(425.00, "$", "normal")
    
    # Test initial state
    assert price.get_amount() == 425.00
    assert price.currency == "$"
    assert price.display_size == "normal"
    
    # Test amount change
    price.set_amount(500.00)
    assert price.get_amount() == 500.00
    assert price.text() == "$500.00"
    
    # Test currency change
    price.set_currency("€")
    assert price.currency == "€"
    assert price.text() == "€500.00"
    
    # Test size change
    price.set_size("large")
    assert price.display_size == "large"
    
    print("✅ PriceDisplay tests passed!")


def test_loading_spinner():
    """Test LoadingSpinner component functionality."""
    print("🧪 Testing LoadingSpinner component...")
    
    spinner = LoadingSpinner(32)
    
    # Test initial state
    assert spinner.spinner_size == 32
    assert spinner.timer is None
    
    # Test start/stop
    spinner.start()
    assert spinner.timer is not None
    assert spinner.timer.isActive()
    
    spinner.stop()
    assert spinner.timer is None
    
    # Test size change
    spinner.set_size(48)
    assert spinner.spinner_size == 48
    
    print("✅ LoadingSpinner tests passed!")


def test_empty_state():
    """Test EmptyState component functionality."""
    print("🧪 Testing EmptyState component...")
    
    empty = EmptyState("Test Title", "Test Description", "Test Action")
    
    # Test action button exists
    assert hasattr(empty, 'action_button')
    assert empty.action_button.text() == "Test Action"
    
    # Test text updates
    empty.set_title("Updated Title")
    empty.set_description("Updated Description")
    empty.set_action_text("Updated Action")
    
    assert empty.action_button.text() == "Updated Action"
    
    print("✅ EmptyState tests passed!")


def test_notification():
    """Test Notification component functionality."""
    print("🧪 Testing Notification component...")
    
    notification = Notification("Test message", "success")
    
    # Test initial state
    assert notification.notification_type == "success"
    
    # Test type change
    notification.set_type("error")
    assert notification.notification_type == "error"
    
    # Test message change
    notification.set_message("Updated message")
    
    print("✅ Notification tests passed!")


def test_styling_system():
    """Test styling system functionality."""
    print("🧪 Testing styling system...")
    
    # Test color constants
    assert COLORS['primary'] == '#2563eb'
    assert COLORS['success'] == '#059669'
    assert COLORS['danger'] == '#dc2626'
    
    # Test font constants
    assert FONTS['family'] == 'Segoe UI'
    assert FONTS['sizes']['base'] == 12
    assert FONTS['weights']['bold'] == 700
    
    # Test spacing constants
    assert SPACING['md'] == 12
    assert SPACING['lg'] == 16
    
    # Test radius constants
    assert RADIUS['md'] == 8
    assert RADIUS['lg'] == 12
    
    # Test helper functions
    from src.ui.theme import get_button_style, get_status_badge_style
    
    button_style = get_button_style('primary')
    assert 'background-color: #2563eb' in button_style
    assert 'color: white' in button_style
    
    badge_style = get_status_badge_style('success')
    assert 'background-color: #d1fae5' in badge_style
    assert 'color: #059669' in badge_style
    
    print("✅ Styling system tests passed!")


def run_all_tests():
    """Run all component tests."""
    print("🚀 Starting Modern Components Test Suite...")
    print("=" * 50)
    
    # Create QApplication for Qt components
    app = QApplication(sys.argv)
    
    try:
        test_styling_system()
        test_status_badge()
        test_card()
        test_search_bar()
        test_price_display()
        test_loading_spinner()
        test_empty_state()
        test_notification()
        
        print("=" * 50)
        print("🎉 All tests passed! Modern components are working correctly.")
        print("✅ Phase 1 & 2 components are ready for production use.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 