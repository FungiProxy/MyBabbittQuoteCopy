import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.material_option import MaterialOption
from src.core.models.option import Option
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.models.voltage_option import VoltageOption


def remove_fs10000():
    """Remove FS10000 product family and all related data from the database."""
    db = SessionLocal()
    try:
        # Get the FS10000 family
        fs10000 = db.query(ProductFamily).filter_by(name='FS10000').first()
        if not fs10000:
            print('FS10000 family not found in database')
            return

        # Delete related data
        print('Deleting FS10000 variants...')
        db.query(ProductVariant).filter_by(product_family_id=fs10000.id).delete()

        print('Deleting FS10000 material options...')
        db.query(MaterialOption).filter_by(product_family_id=fs10000.id).delete()

        print('Deleting FS10000 voltage options...')
        db.query(VoltageOption).filter_by(product_family_id=fs10000.id).delete()

        print('Deleting FS10000 options...')
        db.query(Option).filter_by(product_families='FS10000').delete()

        # Finally, delete the product family
        print('Deleting FS10000 product family...')
        db.delete(fs10000)

        db.commit()
        print('Successfully removed FS10000 and all related data from the database')
    except Exception as e:
        print(f'Error removing FS10000: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    remove_fs10000()
