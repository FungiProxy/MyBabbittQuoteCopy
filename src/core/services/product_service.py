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

from src.core.models import (
    Material,
    MaterialOption,
    Option,
    Product,
    VoltageOption,
)
from src.core.models.connection_option import ConnectionOption
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.pricing import calculate_product_price
from src.utils.db_utils import get_all, get_by_id

# Set up logging
logger = logging.getLogger(__name__)


class ProductService:
    """
    Service class for managing Babbitt International products, configurations, and materials.

    This service provides methods for retrieving, configuring, and pricing products,
    as well as managing product options, materials, and voltages. It encapsulates
    all product and material-related business logic and data access.

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
    ) -> List[Product]:
        """
        Retrieve products with optional filtering by material, voltage, or category.

        This method allows flexible querying of the product catalog with multiple
        filter criteria. All filters are optional and can be combined.

        Args:
            db: SQLAlchemy database session
            material: Optional material code to filter by (e.g., "S", "H", "U", "T")
            voltage: Optional voltage to filter by (e.g., "115VAC", "24VDC")
            category: Optional category to filter by (e.g., "Level Switch", "Transmitter")

        Returns:
            List[Product]: List of Product objects matching the filter criteria

        Example:
            >>> # Get all stainless steel level switches
            >>> products = ProductService.get_products(
            ...     db,
            ...     material="S",
            ...     category="Level Switch"
            ... )
            >>> # Get all 24VDC products
            >>> products = ProductService.get_products(db, voltage="24VDC")
        """
        query = db.query(Product)

        if material is not None:
            query = query.filter(Product.material == material)

        if voltage is not None:
            query = query.filter(Product.voltage == voltage)

        if category is not None:
            query = query.filter(Product.category == category)

        return query.all()

    @staticmethod
    def get_available_materials(db: Session) -> List[Material]:
        """
        Retrieve all available materials from the database.

        This method returns all materials that can be used in product configurations,
        including their properties and pricing rules.

        Args:
            db: SQLAlchemy database session

        Returns:
            List[Material]: List of all available Material objects

        Example:
            >>> materials = ProductService.get_available_materials(db)
            >>> for material in materials:
            ...     print(f"{material.code}: {material.description}")
        """
        return get_all(db, Material)

    @staticmethod
    def get_available_voltages(db: Session, product_family: str) -> List[str]:
        """
        Retrieve available voltage options for a specific product family.

        This method returns all valid voltage configurations for a given product
        family, considering compatibility and availability rules.

        Args:
            db: SQLAlchemy database session
            product_family: Product family identifier (e.g., "LS2000", "LS7000")

        Returns:
            List[str]: List of available voltage options (e.g., ["115VAC", "24VDC"])

        Example:
            >>> voltages = ProductService.get_available_voltages(db, "LS2000")
            >>> print(f"Available voltages for LS2000: {', '.join(voltages)}")
        """
        voltages = (
            db.query(VoltageOption)
            .filter(
                VoltageOption.product_family == product_family,
                VoltageOption.is_available == 1,
            )
            .all()
        )

        return [v.voltage for v in voltages]

    @staticmethod
    def get_available_materials_for_product(
        db: Session, product_family: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve available materials and their properties for a specific product family.

        This method returns detailed material information including display names
        and base prices for materials compatible with the specified product family.

        Args:
            db: SQLAlchemy database session
            product_family: Product family identifier (e.g., "LS2000", "LS7000")

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing:
                - code (str): Material code (e.g., "S", "H")
                - display_name (str): Human-readable name
                - base_price (float): Additional cost for this material

        Example:
            >>> materials = ProductService.get_available_materials_for_product(db, "LS2000")
            >>> for material in materials:
            ...     print(f"{material['display_name']}: ${material['base_price']:.2f}")
        """
        # First get the product family ID
        family = db.query(ProductFamily).filter_by(name=product_family).first()
        if not family:
            return []

        materials = (
            db.query(MaterialOption)
            .filter(
                MaterialOption.product_family_id == family.id,
                MaterialOption.is_available == 1,
            )
            .all()
        )

        return [
            {
                "code": m.material_code,
                "display_name": m.display_name,
                "base_price": m.base_price,
            }
            for m in materials
        ]

    @staticmethod
    def get_product_options(
        db: Session, product_id: Optional[int] = None
    ) -> List[Option]:
        """
        Retrieve available options, optionally filtered by product compatibility.

        This method returns product options, considering any exclusion rules if a
        specific product is specified. It handles compatibility checking to ensure
        only valid options are returned.

        Args:
            db: SQLAlchemy database session
            product_id: Optional product ID to filter compatible options

        Returns:
            List[Option]: List of compatible Option objects

        Example:
            >>> # Get all options
            >>> all_options = ProductService.get_product_options(db)
            >>> # Get options compatible with a specific product
            >>> product_options = ProductService.get_product_options(db, product_id=1)
        """
        query = db.query(Option)

        if product_id is not None:
            # Get the product to check compatibility
            product = get_by_id(db, Product, product_id)
            if product and product.model_number:
                query = query.filter(
                    ~Option.excluded_products.contains(product.model_number)
                )

        return query.all()

    @staticmethod
    def configure_product(
        db: Session,
        product_id: int,
        length: Optional[float] = None,
        material_override: Optional[str] = None,
    ) -> Tuple[Product, float]:
        """
        Configure a product with specified parameters and calculate its price.

        This method handles product configuration and pricing, applying business
        rules for material compatibility and length-based pricing adjustments.

        Args:
            db: SQLAlchemy database session
            product_id: Unique identifier of the product to configure
            length: Optional length in inches (if applicable)
            material_override: Optional material code to override product's default

        Returns:
            Tuple[Product, float]: Tuple containing:
                - Product: The configured product object
                - float: Calculated price including all adjustments

        Raises:
            ValueError: If the product is not found

        Example:
            >>> # Configure a 24-inch stainless steel product
            >>> product, price = ProductService.configure_product(
            ...     db,
            ...     product_id=1,
            ...     length=24.0,
            ...     material_override="S"
            ... )
            >>> print(f"Configured price: ${price:.2f}")
        """
        # Get product
        product = get_by_id(db, Product, product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        # Calculate price
        price = calculate_product_price(
            db=db,
            product_id=product_id,
            length=length,
            material_override=material_override,
        )

        return product, price

    @staticmethod
    def search_products(db: Session, search_term: str) -> List[Product]:
        """
        Search for products by model number or description.

        This method performs a case-insensitive search across product model numbers
        and descriptions, using partial matching for flexibility.

        Args:
            db: SQLAlchemy database session
            search_term: Search term to match against product fields

        Returns:
            List[Product]: List of matching Product objects

        Example:
            >>> # Search for level switches
            >>> products = ProductService.search_products(db, "level switch")
            >>> # Search by model number
            >>> products = ProductService.search_products(db, "LS2000")
        """
        search_pattern = f"%{search_term}%"

        return (
            db.query(Product)
            .filter(
                (Product.description.ilike(search_pattern))
                | (Product.model_number.ilike(search_pattern))
            )
            .all()
        )

    def get_product_families(self, db: Session) -> List[Dict]:
        """
        Fetch all product families from the database.
        Returns: List of dicts with id, name, description, category.
        """
        logger.debug("Fetching all product families")
        families = db.query(ProductFamily).all()
        result = [
            {
                "id": f.id,
                "name": f.name,
                "description": f.description,
                "category": f.category,
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

    @staticmethod
    def get_material_options(db, product_family_id: int) -> List[MaterialOption]:
        """Get available material options for a product family."""
        return db.query(MaterialOption).filter_by(product_family_id=product_family_id).all()

    @staticmethod
    def get_voltage_options(db, product_family_id: int) -> List[VoltageOption]:
        """Get available voltage options for a product family."""
        return db.query(VoltageOption).filter_by(product_family_id=product_family_id).all()

    @staticmethod
    def get_connection_options(db, product_family_id: int) -> List[ConnectionOption]:
        """Get available connection options for a product family."""
        return db.query(ConnectionOption).filter_by(product_family_id=product_family_id).all()

    def get_additional_options(self, db, family_name: str) -> list:
        """
        Fetch additional configurable options (add-ons) for a product family by name.
        Returns: List of dicts with name, description, price, price_type, category, choices, adders.
        """
        logger.debug(f"Fetching additional options for family: {family_name}")
        from src.core.models.option import Option

        # Query options that either have no product_families (NULL) or include this family
        options = (
            db.query(Option)
            .filter(
                (
                    Option.product_families.is_(None)
                )  # Include options with no family restrictions
                | (
                    Option.product_families.like(f"%{family_name}%")
                )  # Include options for this family
            )
            .all()
        )
        logger.debug(f"Found {len(options)} raw options for {family_name}")

        # Log raw options before filtering
        for opt in options:
            logger.debug(f"Raw option: {opt.name}")
            logger.debug(f"  Product Families: {opt.product_families}")
            logger.debug(f"  Excluded Products: {opt.excluded_products}")
            logger.debug(f"  Choices: {opt.choices}")
            logger.debug(f"  Category: {opt.category}")

        # Exclude options where family_name is in excluded_products
        filtered = [
            o
            for o in options
            if not o.excluded_products
            or family_name not in o.excluded_products.split(",")
        ]
        logger.debug(f"After filtering exclusions: {len(filtered)} options")

        result = [
            {
                "name": o.name,
                "description": o.description,
                "price": o.price,
                "price_type": o.price_type,
                "category": o.category,
                "choices": o.choices,
                "adders": o.adders,
            }
            for o in filtered
        ]

        # Log details of each option
        for opt in result:
            logger.debug(f"Option {opt['name']}:")
            logger.debug(f"  - Choices: {opt['choices']}")
            logger.debug(f"  - Adders: {opt['adders']}")
            logger.debug(f"  - Category: {opt['category']}")

        return result

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
        query = db.query(ProductVariant).filter_by(product_family_id=family_id)

        # Filter by core attributes present in the options dictionary
        if options.get("Voltage"):
            query = query.filter_by(voltage=options["Voltage"])
        if options.get("Material"):
            query = query.filter_by(material=options["Material"])

        # Add other potential variant-defining options here if needed in the future

        return query.first()
