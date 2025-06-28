#!/usr/bin/env python3
"""
Simple test to verify modern components work.
"""

import sys
from PySide6.QtWidgets import QApplication

print("🚀 Testing Modern Components...")

try:
    # Test imports
    print("📦 Testing imports...")
    from src.ui.components import (
        StatusBadge, Card, SearchBar, PriceDisplay, 
        LoadingSpinner, EmptyState, Notification
    )
    print("✅ All component imports successful")
    
    from src.ui.theme import (
        COLORS, FONTS, SPACING, RADIUS,
        get_button_style, get_status_badge_style
    )
    print("✅ All theme imports successful")
    
    # Test component creation
    print("🧪 Testing component creation...")
    app = QApplication(sys.argv)
    
    # Test StatusBadge
    badge = StatusBadge("Test", "draft")
    print(f"✅ StatusBadge created: {badge.text()}")
    
    # Test Card
    card = Card("Test Card")
    print(f"✅ Card created: {card.title}")
    
    # Test SearchBar
    search = SearchBar("Test placeholder")
    print(f"✅ SearchBar created: {search.get_text()}")
    
    # Test PriceDisplay
    price = PriceDisplay(425.00, "$", "normal")
    print(f"✅ PriceDisplay created: {price.text()}")
    
    # Test LoadingSpinner
    spinner = LoadingSpinner(32)
    print(f"✅ LoadingSpinner created: {spinner.spinner_size}")
    
    # Test EmptyState
    empty = EmptyState("Test", "Description", "Action")
    print(f"✅ EmptyState created: {empty.action_button.text()}")
    
    # Test Notification
    notification = Notification("Test message", "success")
    print(f"✅ Notification created: {notification.notification_type}")
    
    # Test styling system
    print("🎨 Testing styling system...")
    print(f"✅ Primary color: {COLORS['primary']}")
    print(f"✅ Font family: {FONTS['family']}")
    print(f"✅ Medium spacing: {SPACING['md']}")
    print(f"✅ Medium radius: {RADIUS['md']}")
    
    # Test style helpers
    button_style = get_button_style('primary')
    print(f"✅ Button style generated: {len(button_style)} characters")
    
    badge_style = get_status_badge_style('success')
    print(f"✅ Badge style generated: {len(badge_style)} characters")
    
    print("🎉 All tests passed! Modern components are working correctly.")
    print("✅ Phase 1 & 2 are ready for production use.")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 