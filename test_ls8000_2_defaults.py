#!/usr/bin/env python3
"""
Test script to debug LS8000/2 default configuration issue.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import logging

from PyQt5.QtWidgets import QApplication

from src.core.database import Database
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.ui.views.product_selection_dialog import ProductSelectionDialog

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_ls8000_2_defaults():
    """Test LS8000/2 default configuration."""
    app = QApplication(sys.argv)

    try:
        # Initialize database and services
        db = Database()
        product_service = ProductService()
        config_service = ConfigurationService()

        # Get LS8000/2 product
        products = product_service.get_products(db)
        ls8000_2_product = None
        for product in products:
            if product["name"] == "LS8000/2":
                ls8000_2_product = product
                break

        if not ls8000_2_product:
            logger.error("LS8000/2 product not found!")
            return

        logger.info(f"Found LS8000/2 product: {ls8000_2_product}")

        # Create dialog
        dialog = ProductSelectionDialog(product_service, product_to_edit=None)

        # Simulate selecting LS8000/2
        logger.info("Simulating LS8000/2 selection...")
        dialog._show_product_config(ls8000_2_product)

        # Check what widgets were created
        logger.info("Widgets created:")
        for widget_name, widget in dialog.option_widgets.items():
            logger.info(f"  {widget_name}: {type(widget).__name__}")
            if hasattr(widget, "currentData"):
                logger.info(f"    Current data: {widget.currentData()}")
            if hasattr(widget, "currentText"):
                logger.info(f"    Current text: {widget.currentText()}")

        # Check if Material widget exists and what its current value is
        material_widget = dialog.option_widgets.get("Material")
        if material_widget:
            logger.info(
                f"Material widget found. Current index: {material_widget.currentIndex()}"
            )
            logger.info(
                f"Material widget current data: {material_widget.currentData()}"
            )
            logger.info(
                f"Material widget current text: {material_widget.currentText()}"
            )

            # Check all available materials
            logger.info("Available materials:")
            for i in range(material_widget.count()):
                data = material_widget.itemData(i)
                text = material_widget.itemText(i)
                logger.info(f"  {i}: {text} (data: {data})")
        else:
            logger.error("Material widget not found!")

        # Check current configuration
        if config_service.current_config:
            logger.info(
                f"Current config material: {config_service.current_config.material}"
            )
            logger.info(
                f"Current config final price: ${config_service.current_config.final_price:,.2f}"
            )
        else:
            logger.warning("No current configuration!")

        logger.info("Test completed.")

    except Exception as e:
        logger.error(f"Error during test: {e!s}", exc_info=True)
    finally:
        app.quit()


if __name__ == "__main__":
    test_ls8000_2_defaults()
