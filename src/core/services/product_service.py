"""
Service for managing products and product configuration.

This module provides a service layer for managing Babbitt International products,
including product retrieval, configuration, pricing, and option management. It
implements business logic for:

- Product filtering and searching
- Material and voltage compatibility
- Product configuration and pricing
- Option management and compatibility
- Material management and availability
- Material pricing rules and compatibility

The service follows the Repository pattern and provides a clean interface
for interacting with product-related data and business rules.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from src.core.models import Option
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.pricing import calculate_product_price
from src.utils.db_utils import get_all, get_by_id

# Set up logging
logger = logging.getLogger(__name__)


class ProductService:
    """
    Service class for managing Babbitt International products, configurations, and options.

    This service provides methods for retrieving, configuring, and pricing products,
    as well as managing product options. It encapsulates all product and option-related
    business logic and data access using the new unified options structure.

    The service handles:
    - Product retrieval and configuration
    - Material management and compatibility
    - Voltage options and compatibility
    - Product options and pricing
    - Material-specific pricing rules
    - Length-based calculations

    The service is implemented using static methods for simplicity and statelessness,
    making it easy to use across different parts of the application without
    managing instance state.

    Example:
        >>> db = SessionLocal()
        >>> # Product-related operations
        >>> products = ProductService.get_products(db, material="S", category="Level Switch")
        >>> product, price = ProductService.configure_product(db, product_id=1, length=24)
        >>>
        >>> # Material-related operations
        >>> materials = ProductService.get_available_materials(db)
        >>> product_materials = ProductService.get_available_materials_for_product(db, "LS2000")
        >>> voltages = ProductService.get_available_voltages(db, "LS2000")
    """

    @staticmethod
    def get_products(
        db: Session,
        material: Optional[str] = None,
        voltage: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[ProductVariant]:
        """
        Retrieve product variants with optional filtering by material, voltage, or category.
        """
        query = db.query(ProductVariant)
        if material is not None:
            query = query.filter(ProductVariant.material == material)
        if voltage is not None:
            query = query.filter(ProductVariant.voltage == voltage)
        if category is not None:
            query = query.join(ProductFamily).filter(ProductFamily.category == category)
        return query.all()

    @staticmethod
    def get_available_materials(
        db: Session, family_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all available material options for a product family (or all families if not specified).
        Returns a list of dicts with name, description, price, choices, adders, etc.
        """
        query = db.query(Option).filter(Option.category == "Material")
        if family_name:
            family = db.query(ProductFamily).filter_by(name=family_name).first()
            if family:
                query = query.join(Option.family_associations).filter(
                    Option.family_associations.any(
                        product_family_id=family.id, is_available=1
                    )
                )
        materials = query.all()
        return [
            {
                "name": o.name,
                "description": o.description,
                "price": o.price,
                "price_type": o.price_type,
                "choices": o.choices,
                "adders": o.adders,
            }
            for o in materials
        ]

    @staticmethod
    def get_available_voltages(db: Session, family_name: str) -> List[str]:
        """
        Retrieve available voltage options for a specific product family using the unified options structure.
        Returns a list of voltage names.
        """
        family = db.query(ProductFamily).filter_by(name=family_name).first()
        if not family:
            return []
        options = (
            db.query(Option)
            .filter(Option.category == "Voltage")
            .join(Option.family_associations)
            .filter(
                Option.family_associations.any(
                    product_family_id=family.id, is_available=1
                )
            )
            .all()
        )
        voltages = []
        for o in options:
            if o.choices:
                voltages.extend(o.choices)
            else:
                voltages.append(o.name)
        return sorted(set(voltages))

    @staticmethod
    def get_available_materials_for_product(
        db: Session, family_name: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve available materials and their properties for a specific product family using the unified options structure.
        Returns a list of dicts with name, description, price, choices, adders, etc.
        """
        return ProductService.get_available_materials(db, family_name=family_name)

    @staticmethod
    def get_product_options(
        db: Session, family_name: Optional[str] = None
    ) -> List[Option]:
        """
        Retrieve available options, optionally filtered by product family compatibility.
        Returns a list of Option objects.
        """
        query = db.query(Option)
        if family_name:
            family = db.query(ProductFamily).filter_by(name=family_name).first()
            if family:
                query = query.join(Option.family_associations).filter(
                    Option.family_associations.any(
                        product_family_id=family.id, is_available=1
                    )
                )
        return query.all()

    @staticmethod
    def configure_product(
        db: Session,
        product_id: int,
        length: Optional[float] = None,
        material_override: Optional[str] = None,
    ) -> Tuple[ProductVariant, float]:
        """
        Configure a product variant and calculate its price, supporting length and material overrides.
        """
        product = get_by_id(db, ProductVariant, product_id)
        if not product:
            raise ValueError(f"ProductVariant with id {product_id} not found")
        # Pricing logic can be updated here to use adders from options if needed
        price = product.base_price
        # Example: apply material override adder if provided
        if material_override:
            material_option = (
                db.query(Option)
                .filter(Option.category == "Material", Option.name == material_override)
                .first()
            )
            if material_option and material_option.adders:
                price += material_option.adders.get(material_override, 0)
        # Example: apply length-based adder if needed (not implemented here)
        return product, price

    def get_additional_options(self, db, family_name: str) -> list:
        """
        Fetch additional configurable options (add-ons) for a product family by name.
        Returns: List of dicts with name, description, price, price_type, category, choices, adders.
        """
        logger.debug(f"Fetching additional options for family: {family_name}")
        from src.core.models.option import Option
        from src.core.models.product_variant import ProductFamily

        # Get the product family
        family = db.query(ProductFamily).filter_by(name=family_name).first()
        if not family:
            logger.warning(f"Product family '{family_name}' not found")
            return []

        # Query options that are associated with this product family
        # Use the new many-to-many relationship through ProductFamilyOption
        options = (
            db.query(Option)
            .join(Option.family_associations)
            .filter(
                Option.family_associations.any(
                    product_family_id=family.id, is_available=1
                )
            )
            .all()
        )

        logger.debug(f"Found {len(options)} options for {family_name}")

        # Log raw options before filtering
        for opt in options:
            logger.debug(f"Raw option: {opt.name}")
            logger.debug(f"  Excluded Products: {opt.excluded_products}")
            logger.debug(f"  Choices: {opt.choices}")
            logger.debug(f"  Category: {opt.category}")

        # Don't exclude entire options based on excluded_products
        # The excluded_products field is used for adder exclusion only
        filtered = options
        logger.debug(f"After filtering exclusions: {len(filtered)} options")

        result = []
        for o in filtered:
            option_dict = {
                "name": o.name,
                "description": o.description,
                "price": o.price,
                "price_type": o.price_type,
                "category": o.category,
                "choices": o.choices,
                "adders": o.adders,
                "excluded_products": o.excluded_products,
            }

            # Apply family-specific filtering for Material options
            if o.category == "Material" and o.rules and isinstance(o.rules, dict):
                family_materials = o.rules.get("family_materials", {})
                if family_name in family_materials:
                    allowed_materials = family_materials[family_name]
                    logger.debug(
                        f"Filtering materials for {family_name}: {allowed_materials}"
                    )

                    # Filter choices to only include allowed materials for this family
                    if isinstance(o.choices, list):
                        # Handle both simple string choices and dict choices
                        filtered_choices = []
                        for choice in o.choices:
                            if isinstance(choice, dict):
                                # Choice is a dict like {'code': 'S', 'display_name': 'S - 316 Stainless Steel'}
                                if choice.get("code") in allowed_materials:
                                    filtered_choices.append(choice)
                            elif isinstance(choice, str):
                                # Choice is a simple string like 'S'
                                if choice in allowed_materials:
                                    filtered_choices.append(choice)
                        option_dict["choices"] = filtered_choices
                        logger.debug(
                            f"Filtered material choices for {family_name}: {len(filtered_choices)} materials"
                        )

                    # Filter adders to only include allowed materials
                    if isinstance(o.adders, dict):
                        filtered_adders = {
                            k: v for k, v in o.adders.items() if k in allowed_materials
                        }
                        option_dict["adders"] = filtered_adders
                        logger.debug(
                            f"Filtered material adders for {family_name}: {list(filtered_adders.keys())}"
                        )

            result.append(option_dict)

        # Log details of each option
        for opt in result:
            logger.debug(f"Option {opt['name']}:")
            logger.debug(f"  - Choices: {len(opt['choices']) if opt['choices'] else 0}")
            logger.debug(f"  - Adders: {len(opt['adders']) if opt['adders'] else 0}")
            logger.debug(f"  - Category: {opt['category']}")

        return result

    def get_product_families(self, db: Session) -> List[Dict]:
        """
        Fetch all product families from the database.
        Returns: List of dicts with id, name, description, category, base_model_number, base_price.
        """
        logger.debug("Fetching all product families")
        families = db.query(ProductFamily).all()
        result = [
            {
                "id": f.id,
                "name": f.name,
                "description": f.description,
                "category": f.category,
                "base_model_number": f.base_model_number,
                "base_price": f.base_price,
            }
            for f in families
        ]
        logger.debug(
            f"Found {len(result)} product families: {[f['name'] for f in result]}"
        )
        return result

    def get_variants_for_family(self, db: Session, family_id: int) -> List[Dict]:
        """
        Fetch all product variants for a given family.
        Returns: List of dicts with id, model_number, description, base_price, etc.
        """
        logger.debug(f"Fetching variants for family ID: {family_id}")
        variants = (
            db.query(ProductVariant)
            .filter(ProductVariant.product_family_id == family_id)
            .all()
        )
        result = [
            {
                "id": v.id,
                "model_number": v.model_number,
                "description": v.description,
                "base_price": v.base_price,
                "base_length": v.base_length,
                "voltage": v.voltage,
                "material": v.material,
            }
            for v in variants
        ]
        logger.debug(f"Found {len(result)} variants for family {family_id}")
        return result

    def get_variant_by_id(self, db: Session, variant_id: int) -> Optional[Dict]:
        """
        Fetch a single product variant by its ID.
        Returns: Dict with all variant details, or None if not found.
        """
        variant = (
            db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
        )
        if not variant:
            return None
        return {
            "id": variant.id,
            "model_number": variant.model_number,
            "description": variant.description,
            "base_price": variant.base_price,
            "base_length": variant.base_length,
            "voltage": variant.voltage,
            "material": variant.material,
            "family_id": variant.product_family_id,
        }

    @staticmethod
    def get_product_variants(db: Session) -> list:
        """Fetch all product variants (actual sellable products)."""
        from src.core.models.product_variant import ProductVariant

        return db.query(ProductVariant).all()

    @staticmethod
    def get_all_additional_options(db: Session) -> list:
        """
        Retrieve all configurable options that have choices and adders defined.
        Returns a list of Option objects.
        """
        return (
            db.query(Option)
            .filter(Option.choices.isnot(None), Option.adders.isnot(None))
            .all()
        )

    def get_valid_options_for_selection(
        self, db, family_id: int, selected_options: dict
    ) -> dict:
        """
        Given a product family and a dict of selected options, return valid values for each remaining option.
        This supports dynamic option filtering in the UI as the user makes selections.

        Args:
            db: SQLAlchemy database session
            family_id: ID of the product family
            selected_options: Dict of currently selected options (e.g., {'material': 'S', 'voltage': '115VAC'})

        Returns:
            Dict mapping option names to lists of valid values for each remaining option.
            Example: {'material': ['S', 'H'], 'voltage': ['115VAC', '24VDC']}
        """
        # Fetch all variants for the family
        variants = self.get_variants_for_family(db, family_id)
        # Filter variants by selected options
        for opt, val in selected_options.items():
            variants = [v for v in variants if v.get(opt) == val]
        # Determine all option keys present in variants
        option_keys = set()
        for v in variants:
            option_keys.update(v.keys())
        # Exclude keys that are not configuration options
        exclude_keys = {
            "id",
            "model_number",
            "description",
            "base_price",
            "base_length",
            "family_id",
            "category",
        }
        option_keys = option_keys - exclude_keys
        # For each remaining option, get unique valid values from filtered variants
        valid_options = {}
        for opt in option_keys:
            if opt not in selected_options:
                valid_options[opt] = sorted(
                    {v[opt] for v in variants if v.get(opt) is not None}
                )
        return valid_options

    def get_standard_lengths(self, product_family: str) -> List[int]:
        """
        Get the list of standard lengths for a product family.

        Args:
            product_family: Product family identifier (e.g., "LS2000")

        Returns:
            List[int]: List of standard lengths in inches
        """
        if product_family == "LS2000":
            return [6, 8, 10, 12, 16, 24, 36, 48, 60, 72]
        return []

    def validate_length(
        self, product_family: str, material_code: str, length: float
    ) -> Tuple[bool, str]:
        """
        Validate a length for a specific product and material.

        Args:
            product_family: Product family identifier (e.g., "LS2000")
            material_code: Material code (e.g., "S", "H", "U", "T", "TS")
            length: Length in inches

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if product_family == "LS2000":
            # Check minimum length
            if length < 4:
                return False, "Length cannot be less than 4 inches"

            # Check Halar length limit
            if material_code == "H" and length > 72:
                return (
                    False,
                    "Halar coated probes cannot exceed 72 inches. Please select Teflon Sleeve for longer lengths.",
                )

            # Check if length is standard
            standard_lengths = self.get_standard_lengths(product_family)
            if length not in standard_lengths and material_code != "TS":
                return True, "Non-standard length will add $300 to the price"

        return True, ""

    def calculate_length_price(
        self, product_family: str, material_code: str, length: float
    ) -> float:
        """
        Calculate the price adder for a specific length and material.

        Args:
            product_family: Product family identifier (e.g., "LS2000")
            material_code: Material code (e.g., "S", "H", "U", "T", "TS")
            length: Length in inches

        Returns:
            float: Price adder for the length
        """
        if product_family == "LS2000":
            # Define base lengths and adders
            if material_code in ["U", "T"]:
                base_length = 4.0
                if length > base_length:
                    extra_length = length - base_length
                    adder = (
                        40.0 if material_code == "U" else 50.0
                    )  # $40/inch for U, $50/inch for T
                    return extra_length * adder
            else:
                base_length = 10.0
                if length > base_length:
                    extra_length = length - base_length
                    adder = (
                        3.75 if material_code == "S" else 9.17
                    )  # $45/foot for S, $110/foot for H/TS
                    return extra_length * adder

            # Add non-standard length surcharge
            standard_lengths = self.get_standard_lengths(product_family)
            if length not in standard_lengths and material_code != "TS":
                return 300.0  # $300 adder for non-standard lengths

        return 0.0

    def find_variant(
        self, db: Session, family_id: int, options: dict
    ) -> Optional[ProductVariant]:
        """
        Find a specific product variant based on a set of selected options.

        Args:
            db: The database session.
            family_id: The ID of the product family.
            options: A dictionary of selected options, e.g., {"Voltage": "115VAC", "Material": "S"}.

        Returns:
            The matching ProductVariant object, or None if not found.
        """
        # Get the product family name
        family = db.query(ProductFamily).filter_by(id=family_id).first()
        if not family:
            return None

        # For LS8000/2, we need exact matches for core attributes
        if family.name == "LS8000/2":
            query = db.query(ProductVariant).filter_by(product_family_id=family_id)

            # Filter by core attributes
            if options.get("Voltage"):
                query = query.filter_by(voltage=options["Voltage"])
            if options.get("Material"):
                query = query.filter_by(material=options["Material"])

            # Get all matching variants
            variants = query.all()

            # Find the variant that matches all selected options
            for variant in variants:
                # Check probe type match (if specified)
                if options.get("Probe Type") and not variant.model_number.endswith(
                    '-3/4"'
                ):
                    continue
                # Check housing match (if specified)
                if options.get(
                    "Housing"
                ) == "Stainless Steel (NEMA 4X)" and not variant.model_number.endswith(
                    "-SS"
                ):
                    continue
                # If we get here, we have a match
                return variant

            return None

        # For other products, use the scoring system
        query = db.query(ProductVariant).filter_by(product_family_id=family_id)

        # Filter by core attributes present in the options dictionary
        if options.get("Voltage"):
            query = query.filter_by(voltage=options["Voltage"])
        if options.get("Material"):
            query = query.filter_by(material=options["Material"])

        # Get all variants for this family
        variants = query.all()

        # Find the variant that best matches the selected options
        best_match = None
        best_match_score = 0

        for variant in variants:
            score = 0
            # Check voltage match
            if options.get("Voltage") == variant.voltage:
                score += 1
            # Check material match
            if options.get("Material") == variant.material:
                score += 1
            # Check probe type match (if specified)
            if options.get("Probe Type") and variant.model_number.endswith('-3/4"'):
                score += 1
            # Check housing match (if specified)
            if options.get(
                "Housing"
            ) == "Stainless Steel (NEMA 4X)" and variant.model_number.endswith("-SS"):
                score += 1

            if score > best_match_score:
                best_match = variant
                best_match_score = score

        return best_match

    def search_products(self, db: Session, query: str) -> List[Dict]:
        """
        Search product families and variants by name or description.
        Returns: List of matching product families/variants.
        """
        # Search families
        families = (
            db.query(ProductFamily)
            .filter(
                (ProductFamily.name.ilike(f"%{query}%"))
                | (ProductFamily.description.ilike(f"%{query}%"))
            )
            .all()
        )
        # Search variants
        variants = (
            db.query(ProductVariant)
            .filter(
                (ProductVariant.model_number.ilike(f"%{query}%"))
                | (ProductVariant.description.ilike(f"%{query}%"))
            )
            .all()
        )
        results = [
            {
                "type": "family",
                "id": f.id,
                "name": f.name,
                "description": f.description,
                "category": f.category,
            }
            for f in families
        ] + [
            {
                "type": "variant",
                "id": v.id,
                "model_number": v.model_number,
                "description": v.description,
                "base_price": v.base_price,
                "base_length": v.base_length,
                "voltage": v.voltage,
                "material": v.material,
                "family_id": v.product_family_id,
            }
            for v in variants
        ]
        return results
