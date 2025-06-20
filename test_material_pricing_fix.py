#!/usr/bin/env python3
"""
Test material pricing after fixing the format issue.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging

from src.core.database import get_db
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_material_pricing():
    """Test material pricing with different materials."""
    db = next(get_db())
    product_service = ProductService()
    config_service = ConfigurationService(db, product_service)

    try:
        # Get LS8000 product family
        families = product_service.get_product_families(db)
        ls8000_family = None
        for family in families:
            if family['name'] == 'LS8000':
                ls8000_family = family
                break

        if not ls8000_family:
            logger.error('No LS8000 family found')
            return

        logger.info(f"Testing with family: {ls8000_family['name']}")

        # Start configuration with base product info
        base_product_info = {
            'id': ls8000_family['id'],
            'name': ls8000_family['name'],
            'base_price': 500.0,  # Default base price
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        }

        config_service.start_configuration(
            ls8000_family['id'], ls8000_family['name'], base_product_info
        )

        # Test different materials
        test_materials = ['S', 'H', 'C', 'CPVC', 'A', 'HC']

        for material in test_materials:
            logger.info(f'\n--- Testing material: {material} ---')

            # Set material
            config_service.select_option('Material', material)

            # Get current price
            current_price = config_service.current_config.final_price
            logger.info(f'Price with {material}: ${current_price}')

            # If it's an exotic metal, test override
            if material in ['A', 'HC', 'HB', 'TT']:
                logger.info('Testing exotic metal override...')
                config_service.select_option('Exotic Metal Override', 150.0)
                override_price = config_service.current_config.final_price
                logger.info(f'Price with {material} + $150 override: ${override_price}')

                # Clear override
                config_service.select_option('Exotic Metal Override', 0)

    except Exception as e:
        logger.error(f'Error testing material pricing: {e}', exc_info=True)
    finally:
        db.close()


if __name__ == '__main__':
    test_material_pricing()
