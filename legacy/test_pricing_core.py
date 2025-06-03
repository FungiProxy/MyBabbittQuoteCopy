import pytest
from src.core.pricing import calculate_option_price, get_connection_option_price, calculate_product_price
from unittest.mock import MagicMock, patch

def test_calculate_option_price_fixed():
    assert calculate_option_price(100.0, "fixed") == 100.0

def test_calculate_option_price_per_inch():
    assert calculate_option_price(10.0, "per_inch", length=24) == 240.0

def test_calculate_option_price_per_foot():
    assert calculate_option_price(120.0, "per_foot", length=24) == 240.0

def test_calculate_option_price_per_inch_missing_length():
    # Should default to fixed price if length is None
    assert calculate_option_price(10.0, "per_inch") == 10.0

def test_calculate_option_price_per_foot_missing_length():
    # Should default to fixed price if length is None
    assert calculate_option_price(120.0, "per_foot") == 120.0

def test_calculate_option_price_invalid_type():
    # Should default to fixed price for unknown type
    assert calculate_option_price(50.0, "unknown") == 50.0

def test_get_connection_option_price_flange_found():
    db = MagicMock()
    option = MagicMock()
    option.price = 42.0
    db.query().filter_by().first.return_value = option
    specs = {"connection_type": "Flange", "flange_rating": "150#", "flange_size": "2"}
    assert get_connection_option_price(db, specs) == 42.0

def test_get_connection_option_price_flange_not_found():
    db = MagicMock()
    db.query().filter_by().first.return_value = None
    specs = {"connection_type": "Flange", "flange_rating": "150#", "flange_size": "2"}
    assert get_connection_option_price(db, specs) == 0.0

def test_get_connection_option_price_triclamp_found():
    db = MagicMock()
    option = MagicMock()
    option.price = 55.0
    db.query().filter_by().first.return_value = option
    specs = {"connection_type": "Tri-Clamp", "triclamp_size": "1.5"}
    assert get_connection_option_price(db, specs) == 55.0

def test_get_connection_option_price_triclamp_not_found():
    db = MagicMock()
    db.query().filter_by().first.return_value = None
    specs = {"connection_type": "Tri-Clamp", "triclamp_size": "1.5"}
    assert get_connection_option_price(db, specs) == 0.0

def test_get_connection_option_price_unknown_type():
    db = MagicMock()
    specs = {"connection_type": "Unknown"}
    assert get_connection_option_price(db, specs) == 0.0

def make_product(base_price=100.0, base_length=24, material="S", model_number="LS2000", voltage="115VAC"):
    product = MagicMock()
    product.base_price = base_price
    product.base_length = base_length
    product.material = material
    product.model_number = model_number
    product.voltage = voltage
    return product

def make_material(code="S", has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0):
    material = MagicMock()
    material.code = code
    material.has_nonstandard_length_surcharge = has_nonstandard_length_surcharge
    material.nonstandard_length_surcharge = nonstandard_length_surcharge
    return material

def test_calculate_product_price_basic():
    db = MagicMock()
    product = make_product()
    material = make_material()
    db.query().filter().first.side_effect = [product, material]
    result = calculate_product_price(db, 1)
    assert result == product.base_price

def test_calculate_product_price_product_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(ValueError, match="Product with ID 1 not found"):
        calculate_product_price(db, 1)

def test_calculate_product_price_material_not_found():
    db = MagicMock()
    product = make_product()
    db.query().filter().first.side_effect = [product, None]
    with pytest.raises(ValueError, match="Material S not found"):
        calculate_product_price(db, 1)

def test_calculate_product_price_material_unavailable():
    db = MagicMock()
    product = make_product()
    material = make_material(code="H")
    # Product, material, then None for MaterialAvailability
    db.query().filter().first.side_effect = [product, material, None]
    with pytest.raises(ValueError, match="Material H is not available"):
        calculate_product_price(db, 1, material_override="H")

def test_calculate_product_price_length_adjustment():
    db = MagicMock()
    product = make_product(base_length=24, material="S")
    material = make_material(code="S")
    db.query().filter().first.side_effect = [product, material]
    # Length > base_length, S material: $3.75/inch
    result = calculate_product_price(db, 1, length=36)
    assert result == product.base_price + (36-24)*3.75

def test_calculate_product_price_nonstandard_length_surcharge():
    db = MagicMock()
    product = make_product(base_length=24, material="S")
    material = make_material(code="S", has_nonstandard_length_surcharge=True, nonstandard_length_surcharge=50.0)
    # Product, material, is_standard=False
    db.query().filter().first.side_effect = [product, material, None]
    # Length > base_length, so length adder applies: (30-24)*3.75 = 22.5
    expected = product.base_price + (30-24)*3.75 + 50.0
    result = calculate_product_price(db, 1, length=30)
    assert result == expected

def test_calculate_product_price_with_specs_adds_connection_price():
    db = MagicMock()
    product = make_product()
    material = make_material()
    db.query().filter().first.side_effect = [product, material]
    with patch("src.core.pricing.get_connection_option_price", return_value=25.0):
        result = calculate_product_price(db, 1, specs={"connection_type": "Flange"})
        assert result == product.base_price + 25.0 