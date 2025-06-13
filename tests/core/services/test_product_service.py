import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.core.models.connection_option import ConnectionOption
from src.core.models.material_option import MaterialOption
from src.core.models.option import Option
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.models.voltage_option import VoltageOption
from src.core.services.product_service import ProductService


@pytest.fixture(scope='function')
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_get_product_families(db_session):
    family = ProductFamily(
        name='LS2000', description='Level Switch Family', category='Level Switch'
    )
    db_session.add(family)
    db_session.commit()
    families = ProductService().get_product_families(db_session)
    assert len(families) == 1
    assert families[0]['name'] == 'LS2000'


def test_get_variants_for_family(db_session):
    family = ProductFamily(
        name='LS2000', description='Level Switch Family', category='Level Switch'
    )
    db_session.add(family)
    db_session.commit()
    variant = ProductVariant(
        product_family_id=family.id,
        model_number='LS2000-115VAC',
        description='115VAC Variant',
        base_price=100.0,
    )
    db_session.add(variant)
    db_session.commit()
    variants = ProductService().get_variants_for_family(db_session, family.id)
    assert len(variants) == 1
    assert variants[0]['model_number'] == 'LS2000-115VAC'


def test_get_material_options(db_session):
    mo = MaterialOption(
        product_family='LS2000',
        material_code='S',
        display_name='316 Stainless Steel',
        base_price=10.0,
        is_available=1,
    )
    db_session.add(mo)
    db_session.commit()
    options = ProductService().get_material_options(db_session, 'LS2000')
    assert len(options) == 1
    assert options[0]['material_code'] == 'S'
    assert options[0]['display_name'] == '316 Stainless Steel'
    assert options[0]['base_price'] == 10.0


def test_get_voltage_options(db_session):
    vo = VoltageOption(product_family='LS2000', voltage='24VDC', is_available=1)
    db_session.add(vo)
    db_session.commit()
    options = ProductService().get_voltage_options(db_session, 'LS2000')
    assert len(options) == 1
    assert options[0]['voltage'] == '24VDC'


def test_get_connection_options(db_session):
    co = ConnectionOption(
        type='Flange', rating='150#', size='2"', price=75.0, product_families='LS2000'
    )
    db_session.add(co)
    db_session.commit()
    options = ProductService().get_connection_options(db_session, 'LS2000')
    assert len(options) == 1
    assert options[0]['type'] == 'Flange'
    assert options[0]['rating'] == '150#'
    assert options[0]['size'] == '2"'
    assert options[0]['price'] == 75.0


def test_get_additional_options(db_session):
    # Included option
    opt1 = Option(
        name='Explosion Proof',
        description='Explosion proof housing',
        price=250.0,
        price_type='fixed',
        category='feature',
        product_families='LS2000',
        excluded_products=None,
    )
    # Excluded option
    opt2 = Option(
        name='Special Option',
        description='Not for LS2000',
        price=100.0,
        price_type='fixed',
        category='feature',
        product_families='LS2000',
        excluded_products='LS2000',
    )
    db_session.add_all([opt1, opt2])
    db_session.commit()
    options = ProductService().get_additional_options(db_session, 'LS2000')
    assert len(options) == 1
    assert options[0]['name'] == 'Explosion Proof'


def test_search_products(db_session):
    family = ProductFamily(
        name='LS2000', description='Level Switch Family', category='Level Switch'
    )
    db_session.add(family)
    db_session.commit()
    variant = ProductVariant(
        product_family_id=family.id,
        model_number='LS2000-115VAC',
        description='115VAC Variant',
        base_price=100.0,
    )
    db_session.add(variant)
    db_session.commit()
    results = ProductService().search_products(db_session, 'LS2000')
    # Should find both family and variant
    types = {r['type'] for r in results}
    assert 'family' in types
    assert 'variant' in types


def test_get_variant_by_id(db_session):
    family = ProductFamily(
        name='LS2000', description='Level Switch Family', category='Level Switch'
    )
    db_session.add(family)
    db_session.commit()
    variant = ProductVariant(
        product_family_id=family.id,
        model_number='LS2000-115VAC',
        description='115VAC Variant',
        base_price=100.0,
    )
    db_session.add(variant)
    db_session.commit()
    result = ProductService().get_variant_by_id(db_session, variant.id)
    assert result is not None
    assert result['model_number'] == 'LS2000-115VAC'
    # Test not found
    assert ProductService().get_variant_by_id(db_session, 99999) is None


def test_get_product_families_empty(db_session):
    # Should return empty list if no families exist
    families = ProductService().get_product_families(db_session)
    assert families == []


def test_get_variants_for_family_empty(db_session):
    # Should return empty list if no variants for a family
    family = ProductFamily(name='LS3000', description='Other Family', category='Other')
    db_session.add(family)
    db_session.commit()
    variants = ProductService().get_variants_for_family(db_session, family.id)
    assert variants == []


def test_get_material_options_empty(db_session):
    # Should return empty list if no materials for a family
    options = ProductService().get_material_options(db_session, 'NOFAM')
    assert options == []


def test_get_voltage_options_empty(db_session):
    # Should return empty list if no voltages for a family
    options = ProductService().get_voltage_options(db_session, 'NOFAM')
    assert options == []


def test_get_connection_options_empty(db_session):
    # Should return empty list if no connections for a family
    options = ProductService().get_connection_options(db_session, 'NOFAM')
    assert options == []


def test_get_additional_options_empty(db_session):
    # Should return empty list if no options for a family
    options = ProductService().get_additional_options(db_session, 'NOFAM')
    assert options == []


def test_search_products_no_match(db_session):
    # Should return empty list if no match
    results = ProductService().search_products(db_session, 'ZZZZZZ')
    assert results == []


def test_get_variant_by_id_zero(db_session):
    # Should return None for id=0 (invalid id)
    assert ProductService().get_variant_by_id(db_session, 0) is None


def test_get_additional_options_excluded_comma(db_session):
    # Excluded option with multiple excluded products
    opt = Option(
        name='Special',
        description='Special',
        price=100.0,
        price_type='fixed',
        category='feature',
        product_families='LS2000',
        excluded_products='LS2000,LS3000',
    )
    db_session.add(opt)
    db_session.commit()
    options = ProductService().get_additional_options(db_session, 'LS2000')
    assert options == []


def test_get_valid_options_for_selection(db_session):
    # Create a product family
    family = ProductFamily(
        name='LS2000', description='Level Switch Family', category='Level Switch'
    )
    db_session.add(family)
    db_session.commit()
    # Add variants with different combinations of material and voltage
    variants = [
        ProductVariant(
            product_family_id=family.id,
            model_number='LS2000-S-115VAC',
            description='S/115VAC',
            base_price=100.0,
            material='S',
            voltage='115VAC',
        ),
        ProductVariant(
            product_family_id=family.id,
            model_number='LS2000-S-24VDC',
            description='S/24VDC',
            base_price=100.0,
            material='S',
            voltage='24VDC',
        ),
        ProductVariant(
            product_family_id=family.id,
            model_number='LS2000-H-115VAC',
            description='H/115VAC',
            base_price=100.0,
            material='H',
            voltage='115VAC',
        ),
        ProductVariant(
            product_family_id=family.id,
            model_number='LS2000-H-24VDC',
            description='H/24VDC',
            base_price=100.0,
            material='H',
            voltage='24VDC',
        ),
        ProductVariant(
            product_family_id=family.id,
            model_number='LS2000-U-24VDC',
            description='U/24VDC',
            base_price=100.0,
            material='U',
            voltage='24VDC',
        ),
    ]
    db_session.add_all(variants)
    db_session.commit()
    service = ProductService()
    # No options selected: all values should be available
    result = service.get_valid_options_for_selection(db_session, family.id, {})
    assert set(result['material']) == {'S', 'H', 'U'}
    assert set(result['voltage']) == {'115VAC', '24VDC'}
    # Select material 'S': only voltages for 'S' should be available
    result = service.get_valid_options_for_selection(
        db_session, family.id, {'material': 'S'}
    )
    assert set(result['voltage']) == {'115VAC', '24VDC'}
    # Select material 'U': only voltage '24VDC' should be available
    result = service.get_valid_options_for_selection(
        db_session, family.id, {'material': 'U'}
    )
    assert set(result['voltage']) == {'24VDC'}
    # Select voltage '115VAC': only materials with that voltage
    result = service.get_valid_options_for_selection(
        db_session, family.id, {'voltage': '115VAC'}
    )
    assert set(result['material']) == {'S', 'H'}
    # Select both: only one variant should match, so no further options
    result = service.get_valid_options_for_selection(
        db_session, family.id, {'material': 'U', 'voltage': '24VDC'}
    )
    assert result == {}
