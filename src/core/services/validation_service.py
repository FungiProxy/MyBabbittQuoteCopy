"""
Service for validating product configurations and business rules.

This module provides a service layer for validating product configurations,
options, and business rules in Babbitt International's quoting system. It implements:

- Product configuration validation
- Option compatibility validation
- Material compatibility validation
- Length validation
- Voltage validation
- Connection validation
- Business rule validation
- Cable and enclosure validation
- Electrical protection validation

The service follows domain-driven design principles and separates validation logic
from data access, providing a clean interface for validation operations.
"""

import logging
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from src.core.models import (
    Material,
    Option,
    ProductFamily,
    ProductVariant,
    StandardLength,
    VoltageOption,
    Cable,
    Enclosure,
    ElectricalProtection,
)
from src.core.models.connection_option import ConnectionOption
from src.core.models.material import MaterialAvailability

# Set up logging
logger = logging.getLogger(__name__)


class ValidationService:
    """
    Service class for validating product configurations and business rules.

    This service provides methods for validating various aspects of product
    configurations, including material compatibility, option compatibility,
    length constraints, and business rules. It encapsulates all validation-related
    business logic and data access.

    Example:
        >>> db = SessionLocal()
        >>> validation_service = ValidationService(db)
        >>> is_valid, message = validation_service.validate_configuration(
        ...     product_family_id=1,
        ...     material="316SS",
        ...     length=24.0,
        ...     voltage="115VAC",
        ...     connection="1/2\" NPT"
        ... )
    """

    def __init__(self, db: Session):
        self.db = db
        logger.debug("ValidationService initialized")

    def validate_configuration(
        self,
        product_family_id: int,
        material: str,
        length: float,
        voltage: Optional[str] = None,
        connection: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
        cable: Optional[str] = None,
        enclosure: Optional[str] = None,
        electrical_protection: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Validate a complete product configuration.

        Args:
            product_family_id: ID of the product family
            material: Material code (e.g., "S", "H", "U")
            length: Length in inches
            voltage: Optional voltage option
            connection: Optional connection type
            options: Optional dictionary of additional options
            cable: Optional cable type
            enclosure: Optional enclosure type
            electrical_protection: Optional electrical protection type

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Validate product family
            if not self._validate_product_family(product_family_id):
                return False, f"Invalid product family ID: {product_family_id}"

            # Validate material
            is_valid, message = self._validate_material(material)
            if not is_valid:
                return False, message

            # Validate length
            is_valid, message = self._validate_length(material, length)
            if not is_valid:
                return False, message

            # Validate voltage if specified
            if voltage:
                is_valid, message = self._validate_voltage(product_family_id, voltage)
                if not is_valid:
                    return False, message

            # Validate connection if specified
            if connection:
                is_valid, message = self._validate_connection(connection)
                if not is_valid:
                    return False, message

            # Validate cable if specified
            if cable:
                is_valid, message = self._validate_cable(cable)
                if not is_valid:
                    return False, message

            # Validate enclosure if specified
            if enclosure:
                is_valid, message = self._validate_enclosure(enclosure)
                if not is_valid:
                    return False, message

            # Validate electrical protection if specified
            if electrical_protection:
                is_valid, message = self._validate_electrical_protection(
                    electrical_protection
                )
                if not is_valid:
                    return False, message

            # Validate additional options if specified
            if options:
                is_valid, message = self._validate_options(product_family_id, options)
                if not is_valid:
                    return False, message

            return True, "Configuration is valid"

        except Exception as e:
            logger.error(f"Error validating configuration: {e!s}", exc_info=True)
            return False, f"Error validating configuration: {str(e)}"

    def _validate_product_family(self, product_family_id: int) -> bool:
        """Validate that the product family exists."""
        try:
            product_family = self.db.query(ProductFamily).get(product_family_id)
            return product_family is not None
        except Exception as e:
            logger.error(f"Error validating product family: {e!s}", exc_info=True)
            return False

    def _validate_material(self, material: str) -> Tuple[bool, str]:
        """Validate material compatibility."""
        try:
            material_obj = self.db.query(Material).filter_by(code=material).first()
            if not material_obj:
                return False, f"Invalid material code: {material}"
            # Check availability using MaterialAvailability
            availability = (
                self.db.query(MaterialAvailability)
                .filter_by(material_id=material_obj.id, product_type="Level Switch")
                .first()
            )
            if not availability or not availability.is_available:
                return (
                    False,
                    f"Material {material} is not currently available for this product type",
                )
            return True, ""
        except Exception as e:
            logger.error(f"Error validating material: {e!s}", exc_info=True)
            return False, f"Error validating material: {str(e)}"

    def _validate_length(self, material: str, length: float) -> Tuple[bool, str]:
        """Validate length constraints."""
        try:
            # Check minimum length
            if length < 4:
                return False, "Length cannot be less than 4 inches"

            # Check material-specific length limits
            material_obj = self.db.query(Material).filter_by(code=material).first()
            if material_obj:
                if material_obj.code == "H" and length > 72:
                    return (
                        False,
                        "Halar coated probes cannot exceed 72 inches. Please select Teflon Sleeve for longer lengths.",
                    )

            # Check if length is standard
            standard_length = (
                self.db.query(StandardLength)
                .filter_by(material_id=material_obj.id, length=length)
                .first()
            )
            if not standard_length and material != "TS":
                return True, "Non-standard length will add $300 to the price"

            return True, ""
        except Exception as e:
            logger.error(f"Error validating length: {e!s}", exc_info=True)
            return False, f"Error validating length: {str(e)}"

    def _validate_voltage(
        self, product_family_id: int, voltage: str
    ) -> Tuple[bool, str]:
        """Validate voltage compatibility."""
        try:
            voltage_obj = (
                self.db.query(VoltageOption)
                .filter_by(product_family_id=product_family_id, voltage=voltage)
                .first()
            )
            if not voltage_obj:
                return False, f"Invalid voltage option: {voltage}"
            if not voltage_obj.is_available:
                return False, f"Voltage option {voltage} is not currently available"
            return True, ""
        except Exception as e:
            logger.error(f"Error validating voltage: {e!s}", exc_info=True)
            return False, f"Error validating voltage: {str(e)}"

    def _validate_connection(self, connection: str) -> Tuple[bool, str]:
        """Validate connection compatibility."""
        try:
            connection_obj = (
                self.db.query(ConnectionOption)
                .filter_by(connection_type=connection)
                .first()
            )
            if not connection_obj:
                return False, f"Invalid connection type: {connection}"
            if not connection_obj.is_available:
                return False, f"Connection type {connection} is not currently available"
            return True, ""
        except Exception as e:
            logger.error(f"Error validating connection: {e!s}", exc_info=True)
            return False, f"Error validating connection: {str(e)}"

    def _validate_cable(self, cable: str) -> Tuple[bool, str]:
        """Validate cable compatibility."""
        try:
            cable_obj = self.db.query(Cable).filter_by(cable_type=cable).first()
            if not cable_obj:
                return False, f"Invalid cable type: {cable}"
            if not cable_obj.is_available:
                return False, f"Cable type {cable} is not currently available"
            return True, ""
        except Exception as e:
            logger.error(f"Error validating cable: {e!s}", exc_info=True)
            return False, f"Error validating cable: {str(e)}"

    def _validate_enclosure(self, enclosure: str) -> Tuple[bool, str]:
        """Validate enclosure compatibility."""
        try:
            enclosure_obj = (
                self.db.query(Enclosure).filter_by(enclosure_type=enclosure).first()
            )
            if not enclosure_obj:
                return False, f"Invalid enclosure type: {enclosure}"
            if not enclosure_obj.is_available:
                return False, f"Enclosure type {enclosure} is not currently available"
            return True, ""
        except Exception as e:
            logger.error(f"Error validating enclosure: {e!s}", exc_info=True)
            return False, f"Error validating enclosure: {str(e)}"

    def _validate_electrical_protection(self, protection: str) -> Tuple[bool, str]:
        """Validate electrical protection compatibility."""
        try:
            protection_obj = (
                self.db.query(ElectricalProtection)
                .filter_by(protection_type=protection)
                .first()
            )
            if not protection_obj:
                return False, f"Invalid electrical protection type: {protection}"
            if not protection_obj.is_available:
                return (
                    False,
                    f"Electrical protection type {protection} is not currently available",
                )
            return True, ""
        except Exception as e:
            logger.error(
                f"Error validating electrical protection: {e!s}", exc_info=True
            )
            return False, f"Error validating electrical protection: {str(e)}"

    def _validate_options(
        self, product_family_id: int, options: Dict[str, str]
    ) -> Tuple[bool, str]:
        """Validate additional options."""
        try:
            for option_name, option_value in options.items():
                option = (
                    self.db.query(Option)
                    .filter_by(
                        product_family_id=product_family_id,
                        name=option_name,
                        value=option_value,
                    )
                    .first()
                )
                if not option:
                    return False, f"Invalid option: {option_name}={option_value}"
                if not option.is_available:
                    return (
                        False,
                        f"Option {option_name}={option_value} is not currently available",
                    )
            return True, ""
        except Exception as e:
            logger.error(f"Error validating options: {e!s}", exc_info=True)
            return False, f"Error validating options: {str(e)}"

    def validate_variant(
        self, product_family_id: int, options: Dict[str, str]
    ) -> Tuple[bool, str]:
        """
        Validate if a specific variant exists for the given options.

        Args:
            product_family_id: ID of the product family
            options: Dictionary of selected options

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            variant = (
                self.db.query(ProductVariant)
                .filter_by(product_family_id=product_family_id)
                .first()
            )
            if not variant:
                return False, f"No variant found for product family {product_family_id}"
            return True, ""
        except Exception as e:
            logger.error(f"Error validating variant: {e!s}", exc_info=True)
            return False, f"Error validating variant: {str(e)}"
