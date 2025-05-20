import pytest
from src.core.models.product import Product


def test_create_and_query_product(db_session):
    product = Product(model_number="LS2000", base_price=100.0, base_length=24, material="S", voltage="115VAC")
    db_session.add(product)
    db_session.commit()
    queried = db_session.query(Product).filter_by(model_number="LS2000").first()
    assert queried is not None
    assert queried.base_price == 100.0
    assert queried.material == "S"

def test_update_product(db_session):
    product = Product(model_number="LS2001", base_price=120.0, base_length=30, material="H", voltage="230VAC")
    db_session.add(product)
    db_session.commit()
    product.base_price = 150.0
    db_session.commit()
    updated = db_session.query(Product).filter_by(model_number="LS2001").first()
    assert updated.base_price == 150.0

def test_delete_product(db_session):
    product = Product(model_number="LS2002", base_price=80.0, base_length=18, material="U", voltage="24VDC")
    db_session.add(product)
    db_session.commit()
    db_session.delete(product)
    db_session.commit()
    deleted = db_session.query(Product).filter_by(model_number="LS2002").first()
    assert deleted is None 