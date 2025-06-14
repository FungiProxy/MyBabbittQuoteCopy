from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from src.core.models import Material, Product


@dataclass
class PricingContext:
    db: Session
    product_id: int
    length_in: Optional[float] = None
    material_override_code: Optional[str] = None
    specs: Optional[Dict[str, Any]] = field(default_factory=dict)

    # These fields will be populated by strategies
    product: Optional[Product] = None
    material: Optional[Material] = None
    effective_length_in: Optional[float] = None

    # The price is accumulated through strategies
    price: float = 0.0

    def __post_init__(self):
        # Initial lookup for product
        self.product = (
            self.db.query(Product).filter(Product.id == self.product_id).first()
        )
        if not self.product:
            raise ValueError(f"Product with ID {self.product_id} not found")

        # Determine effective length
        self.effective_length_in = (
            self.length_in if self.length_in is not None else self.product.base_length
        )

        # Determine effective material
        material_code = (
            self.material_override_code
            if self.material_override_code
            else self.product.material
        )
        self.material = (
            self.db.query(Material).filter(Material.code == material_code).first()
        )
        if not self.material:
            raise ValueError(f"Material {material_code} not found")
