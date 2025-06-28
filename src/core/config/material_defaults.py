"""
Material default configurations.
Defines default lengths and other properties for each material type.
"""

# Default lengths for each material type
MATERIAL_DEFAULT_LENGTHS = {
    "S": 10.0,    # 316 Stainless Steel - 10" default
    "H": 10.0,    # Halar Coated - 10" default
    "TS": 10.0,   # Teflon Sleeve - 10" default
    "U": 4.0,     # UHMWPE Blind End - 4" default (blind end materials typically shorter)
    "T": 4.0,     # Teflon Blind End - 4" default (blind end materials typically shorter)
    "C": 12.0,    # Cable - 12" default (cable materials typically longer)
    "CPVC": 4.0,  # CPVC Blind End - 4" default (blind end materials typically shorter)
}

def get_material_default_length(material_code: str) -> float:
    """Get the default length for a given material code."""
    return MATERIAL_DEFAULT_LENGTHS.get(material_code, 10.0)

def get_all_material_defaults() -> dict:
    """Get all material default configurations."""
    return MATERIAL_DEFAULT_LENGTHS.copy() 