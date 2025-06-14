"""
Comprehensive test suite for the pricing system.

This module tests all aspects of the pricing system including:
- Base price calculations
- Material premiums
- Length-based pricing
- Connection options
- Non-standard length surcharges
- Edge cases and special product types
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.core.models import (
    Product,
    Material,
    ConnectionOption,
    MaterialAvailability,
    StandardLength,
)
from src.core.pricing import (
    calculate_product_price,
    calculate_option_price,
    PricingContext,
)
from src.core.pricing.strategies import (
    BasePriceStrategy,
    MaterialPremiumStrategy,
    ExtraLengthStrategy,
    NonStandardLengthSurchargeStrategy,
    ConnectionOptionStrategy,
    MaterialAvailabilityStrategy,
)


# Test fixtures
@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def base_product():
    """Create a base product for testing."""
    return Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )


@pytest.fixture
def base_material():
    """Create a base material for testing."""
    return Material(
        code="S",
        name="Stainless Steel",
        has_nonstandard_length_surcharge=True,
        nonstandard_length_surcharge=50.0,
    )


# Base Price Strategy Tests
def test_base_price_strategy_standard_material(mock_db, base_product, base_material):
    """Test base price calculation for standard materials."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="S",
    )
    context.product = base_product
    context.material = base_material

    strategy = BasePriceStrategy()
    price = strategy.calculate(context)

    assert price == 500.0  # Base price for standard material


def test_base_price_strategy_exotic_material(mock_db, base_product, base_material):
    """Test base price calculation for exotic materials (U, T)."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="U",
    )
    context.product = base_product
    context.material = Material(code="U", name="UHMWPE")

    # Mock the S material product query
    s_product = Product(
        id=2,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = s_product

    strategy = BasePriceStrategy()
    price = strategy.calculate(context)

    assert price == 500.0  # Should use S material base price


# Material Premium Strategy Tests
def test_material_premium_strategy_uhmwpe(mock_db, base_product):
    """Test material premium for UHMWPE."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="U",
    )
    context.product = base_product
    context.material = Material(code="U", name="UHMWPE")
    context.price = 500.0  # Base price

    strategy = MaterialPremiumStrategy()
    price = strategy.calculate(context)

    assert price == 520.0  # Base price + $20 UHMWPE premium


def test_material_premium_strategy_teflon(mock_db, base_product):
    """Test material premium for Teflon."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="T",
    )
    context.product = base_product
    context.material = Material(code="T", name="Teflon")
    context.price = 500.0  # Base price

    strategy = MaterialPremiumStrategy()
    price = strategy.calculate(context)

    assert price == 560.0  # Base price + $60 Teflon premium


# Extra Length Strategy Tests
def test_extra_length_strategy_ls2000_standard(mock_db, base_product, base_material):
    """Test extra length pricing for LS2000 with standard material."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=24.0,  # 24 inches
        material_override_code="S",
    )
    context.product = base_product
    context.material = base_material
    context.price = 500.0  # Base price

    strategy = ExtraLengthStrategy()
    price = strategy.calculate(context)

    # 24" - 10" = 14" extra length
    # $3.75 per inch for S material
    expected_price = 500.0 + (14.0 * 3.75)
    assert price == expected_price


def test_extra_length_strategy_ls2000_exotic(mock_db, base_product):
    """Test extra length pricing for LS2000 with exotic material."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=24.0,  # 24 inches
        material_override_code="U",
    )
    context.product = base_product
    context.material = Material(code="U", name="UHMWPE")
    context.price = 500.0  # Base price

    strategy = ExtraLengthStrategy()
    price = strategy.calculate(context)

    # 24" - 4" = 20" extra length
    # $40 per inch for U material
    expected_price = 500.0 + (20.0 * 40.0)
    assert price == expected_price


# Non-Standard Length Surcharge Tests
def test_nonstandard_length_surcharge_ls2000(mock_db, base_product, base_material):
    """Test non-standard length surcharge for LS2000."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=15.0,  # Non-standard length
        material_override_code="S",
    )
    context.product = base_product
    context.material = base_material
    context.price = 500.0  # Base price

    # Mock standard length query to return None (non-standard length)
    mock_db.query().filter().first.return_value = None

    strategy = NonStandardLengthSurchargeStrategy()
    price = strategy.calculate(context)

    assert price == 550.0  # Base price + $50 surcharge


def test_nonstandard_length_surcharge_halar_limit(mock_db, base_product):
    """Test Halar length limit enforcement."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=84.0,  # Over 72" limit
        material_override_code="H",
    )
    context.product = base_product
    context.material = Material(code="H", name="Halar")

    strategy = NonStandardLengthSurchargeStrategy()

    with pytest.raises(ValueError, match="Halar coated probes cannot exceed 72 inches"):
        strategy.calculate(context)


# Connection Option Strategy Tests
def test_connection_option_strategy_flange(mock_db, base_product, base_material):
    """Test connection option pricing for Flange."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="S",
        specs={
            "connection_type": "Flange",
            "flange_rating": "150#",
            "flange_size": '1"',
        },
    )
    context.product = base_product
    context.material = base_material
    context.price = 500.0  # Base price

    # Mock connection option query
    connection_option = ConnectionOption(
        type="Flange",
        rating="150#",
        size='1"',
        price=100.0,
    )
    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = connection_option
    mock_db.query.return_value = mock_query

    strategy = ConnectionOptionStrategy()
    price = strategy.calculate(context)

    assert price == 600.0  # Base price + $100 flange option


def test_connection_option_strategy_triclamp(mock_db, base_product, base_material):
    """Test connection option pricing for Tri-Clamp."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="S",
        specs={
            "connection_type": "Tri-Clamp",
            "triclamp_size": '1"',
        },
    )
    context.product = base_product
    context.material = base_material
    context.price = 500.0  # Base price

    # Mock connection option query
    connection_option = ConnectionOption(
        type="Tri-Clamp",
        size='1"',
        price=75.0,
    )
    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = connection_option
    mock_db.query.return_value = mock_query

    strategy = ConnectionOptionStrategy()
    price = strategy.calculate(context)

    assert price == 575.0  # Base price + $75 tri-clamp option


# Material Availability Strategy Tests
def test_material_availability_strategy_available(mock_db, base_product):
    """Test material availability check for available material."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="H",
    )
    context.product = base_product

    # Mock material availability query
    availability = MaterialAvailability(
        material_code="H",
        product_type="LS2000",
        is_available=True,
    )
    mock_db.query().filter().first.return_value = availability

    strategy = MaterialAvailabilityStrategy()
    price = strategy.calculate(context)

    assert price == 0.0  # No price change, just validation


def test_material_availability_strategy_unavailable(mock_db, base_product):
    """Test material availability check for unavailable material."""
    context = PricingContext(
        db=mock_db,
        product_id=1,
        length_in=10.0,
        material_override_code="H",
    )
    context.product = base_product

    # Mock material availability query to return None (unavailable)
    mock_db.query().filter().first.return_value = None

    strategy = MaterialAvailabilityStrategy()

    with pytest.raises(
        ValueError, match="Material H is not available for product type LS2000"
    ):
        strategy.calculate(context)


# Integration Tests
def test_complete_pricing_calculation(mock_db, base_product, base_material):
    """Test a complete pricing calculation with multiple factors."""
    # Create separate mock queries for each type of query
    product_query = MagicMock()
    product_query.filter_by.return_value = product_query
    product_query.first.return_value = base_product

    material_query = MagicMock()
    material_query.filter_by.return_value = material_query
    material_query.first.return_value = base_material

    availability_query = MagicMock()
    availability_query.filter_by.return_value = availability_query
    availability_query.first.return_value = MaterialAvailability(
        material_code="S", product_type="LS2000", is_available=True
    )

    length_query = MagicMock()
    length_query.filter_by.return_value = length_query
    length_query.first.return_value = StandardLength(material_code="S", length=24.0)

    connection_query = MagicMock()
    connection_query.filter_by.return_value = connection_query
    connection_query.first.return_value = ConnectionOption(
        type="Flange", rating="150#", size='1"', price=100.0
    )

    # Set up the mock_db to return different queries based on the model
    def get_query(model):
        if model == Product:
            return product_query
        elif model == Material:
            return material_query
        elif model == MaterialAvailability:
            return availability_query
        elif model == StandardLength:
            return length_query
        elif model == ConnectionOption:
            return connection_query
        return MagicMock()

    mock_db.query.side_effect = get_query

    with patch("src.core.pricing.context.PricingContext.__post_init__", lambda x: None):
        context = PricingContext(
            db=mock_db,
            product_id=1,
            length_in=24.0,
            material_override_code="S",
            specs={
                "connection_type": "Flange",
                "flange_rating": "150#",
                "flange_size": '1"',
            },
        )
        context.product = base_product
        context.material = base_material
        context.effective_length_in = 24.0
        context.price = 0.0

        # Define the sequence of pricing strategies
        pricing_strategies = [
            MaterialAvailabilityStrategy(),
            BasePriceStrategy(),
            MaterialPremiumStrategy(),
            ExtraLengthStrategy(),
            NonStandardLengthSurchargeStrategy(),
            ConnectionOptionStrategy(),
        ]
        calculator = PriceCalculator(pricing_strategies)
        price = calculator.calculate(context)

    # Expected price calculation:
    # Base price: $500.0
    # Extra length (24" - 10" = 14"): 14 * $3.75 = $52.50
    # Flange connection: $100.0
    expected_price = 500.0 + (14.0 * 3.75) + 100.0
    assert price == expected_price


def test_special_product_pricing_ls7000_dual(mock_db):
    """Test pricing for LS7000/2 dual point switch."""
    product = Product(
        id=2,
        model_number="LS7000/2-120-S",
        base_price=800.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    material = Material(code="S", name="Stainless Steel")

    # Mock database queries
    mock_db.query().filter().first.side_effect = [
        product,
        material,
        MaterialAvailability(
            material_code="S", product_type="LS7000/2", is_available=True
        ),
    ]

    price = calculate_product_price(
        db=mock_db,
        product_id=2,
        length=24.0,
        material_override="S",
    )

    # Expected price calculation:
    # Base price: $800.0
    # Extra length (24" - 10" = 14"): 14 * $3.75 = $52.50
    expected_price = 800.0 + (14.0 * 3.75)
    assert price == expected_price
