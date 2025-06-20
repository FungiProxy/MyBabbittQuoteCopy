#!/usr/bin/env python3
"""
Simple test for the updated ProductSelectionDialog UI integration.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.ui.views.product_selection_dialog import ProductSelectionDialog


def test_ui_integration():
    """Test that the ProductSelectionDialog can load options from the unified structure."""
    print('Testing UI integration with unified options structure...')

    # Create QApplication instance (required for Qt widgets)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    db = SessionLocal()
    try:
        # Create services
        product_service = ProductService()
        ConfigurationService(db, product_service)

        # Create dialog
        dialog = ProductSelectionDialog(product_service)

        # Test that dialog initializes without errors
        print('✅ Dialog created successfully')

        # Test that product families are loaded
        if dialog.products:
            print(f'✅ Loaded {len(dialog.products)} product families')

            # Test with first product family
            first_product = dialog.products[0]
            print(f"✅ Testing with product family: {first_product['name']}")

            # Test that additional options can be fetched
            additional_options = product_service.get_additional_options(
                db, first_product['name']
            )
            print(f'✅ Found {len(additional_options)} additional options')

            # Test option structure
            if additional_options:
                first_option = additional_options[0]
                print(
                    f"✅ First option: {first_option['name']} ({first_option.get('category', 'No category')})"
                )
                print(f"   Choices: {len(first_option.get('choices', []))} choices")
                print(f"   Adders: {len(first_option.get('adders', {}))} adders")

            print('✅ UI integration test passed!')
            return True
        else:
            print('❌ No product families loaded')
            return False

    except Exception as e:
        print(f'❌ UI integration test failed: {e}')
        import traceback

        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == '__main__':
    success = test_ui_integration()
    sys.exit(0 if success else 1)
