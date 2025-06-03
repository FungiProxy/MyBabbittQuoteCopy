import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import engine
from src.core.models.option import Option

if __name__ == "__main__":
    Option.__table__.drop(engine)
    print("Dropped 'options' table.") 