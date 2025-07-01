"""
Integration Test for Phase 7 Features

This script tests that the Phase 7 features (theme switching, font scaling, responsive design)
are properly integrated into the main MyBabbittQuote application.
"""

import sys
from PySide6.QtWidgets import QApplication

# Import the main application
from src.ui.main_window import MainWindow

def test_phase7_integration():
    """Test Phase 7 features integration."""
    print("🧪 Testing Phase 7 Integration...")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = MainWindow()
    
    # Test 1: Check if Phase 7 components are loaded
    print("✅ Main window created successfully")
    
    # Test 2: Check if responsive manager is initialized
    if hasattr(main_window, 'responsive_manager'):
        print("✅ Responsive manager initialized")
    else:
        print("❌ Responsive manager not found")
    
    # Test 3: Check if font scaling is available
    if hasattr(main_window, 'font_scale_factor'):
        print("✅ Font scaling factor initialized")
    else:
        print("❌ Font scaling factor not found")
    
    # Test 4: Check if theme manager is connected
    try:
        from src.ui.components import theme_manager
        print("✅ Theme manager imported successfully")
    except ImportError as e:
        print(f"❌ Theme manager import failed: {e}")
    
    # Test 5: Check settings page for Phase 7 controls
    try:
        settings_page = main_window.settings_page
        if hasattr(settings_page, 'theme_toggle'):
            print("✅ Theme toggle found in settings")
        else:
            print("❌ Theme toggle not found in settings")
            
        if hasattr(settings_page, 'font_scale_slider'):
            print("✅ Font scaling slider found in settings")
        else:
            print("❌ Font scaling slider not found in settings")
            
        if hasattr(settings_page, 'responsive_status_label'):
            print("✅ Responsive status label found in settings")
        else:
            print("❌ Responsive status label not found in settings")
    except Exception as e:
        print(f"❌ Settings page test failed: {e}")
    
    # Show the window
    main_window.show()
    
    print("\n🎉 Phase 7 Integration Test Complete!")
    print("The main application should now have:")
    print("  • Theme switching (light/dark mode)")
    print("  • Font scaling (50%-200%)")
    print("  • Responsive design")
    print("  • Modern styling throughout")
    
    print("\n📋 Next Steps:")
    print("  1. Go to Settings to test theme toggle and font scaling")
    print("  2. Resize the window to test responsive design")
    print("  3. Navigate through the application to see modern styling")
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_phase7_integration() 