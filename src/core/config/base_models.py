"""
Base Models Configuration
Defines the base models and pricing for each product family.
This is the single source of truth for base model information.
"""

# Base model configurations for each product family
BASE_MODELS = {
    "LS2000": {
        "model_number": 'LS2000-115VAC-S-10"',
        "description": "LS2000 Level Switch - Base Configuration",
        "base_price": 425.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "S",
        "process_connection_type": "NPT",
        "process_connection_size": '3/4"',
    },
    "LS2100": {
        "model_number": 'LS2100-24VDC-S-10"',
        "description": "LS2100 Level Switch - Base Configuration",
        "base_price": 460.0,
        "base_length": 10.0,
        "voltage": "24VDC",
        "material": "S",
        "process_connection_type": "NPT",
        "process_connection_size": '3/4"',
    },
    "LS6000": {
        "model_number": 'LS6000-115VAC-S-10"',
        "description": "LS6000 Level Switch - Base Configuration",
        "base_price": 550.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "S",
        "process_connection_type": "NPT",
        "process_connection_size": '1"',
    },
    "LS7000": {
        "model_number": 'LS7000-115VAC-S-10"',
        "description": "LS7000 Level Switch - Base Configuration",
        "base_price": 680.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "S",
        "process_connection_type": "NPT",
        "process_connection_size": '1"',
    },
    "LS7000/2": {
        "model_number": 'LS7000/2-115VAC-H-10"',
        "description": "LS7000/2 Level Switch - Base Configuration",
        "base_price": 770.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "H",
        "process_connection_type": "NPT",
        "process_connection_size": '1"',
    },
    "LS8000": {
        "model_number": 'LS8000-115VAC-S-10"',
        "description": "LS8000 Level Switch - Base Configuration",
        "base_price": 715.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "S",
        "process_connection_type": "NPT",
        "process_connection_size": '3/4"',
    },
    "LS8000/2": {
        "model_number": 'LS8000/2-115VAC-H-10"',
        "description": "LS8000/2 Level Switch - Base Configuration",
        "base_price": 850.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "H",
        "process_connection_type": "NPT",
        "process_connection_size": '3/4"',
    },
    "LT9000": {
        "model_number": 'LT9000-115VAC-H-10"',
        "description": "LT9000 Level Transmitter - Base Configuration",
        "base_price": 855.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "H",
        "process_connection_type": "NPT",
        "process_connection_size": '1"',
    },
    "FS10000": {
        "model_number": 'FS10000-115VAC-S-6"',
        "description": "FS10000 Flow Switch - Base Configuration",
        "base_price": 1885.0,
        "base_length": 6.0,
        "voltage": "115VAC",
        "material": "S",
        "process_connection_type": "NPT",
        "process_connection_size": '3/4"',
    },
    # Presence/Absence switches - to be configured later
    "LS7500": {
        "model_number": "LS7500-BASE",  # Placeholder
        "description": "LS7500 Presence/Absence Switch - Base Configuration",
        "base_price": 0.0,  # To be determined
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "S",
    },
    "LS8500": {
        "model_number": "LS8500-BASE",  # Placeholder
        "description": "LS8500 Presence/Absence Switch - Base Configuration",
        "base_price": 0.0,  # To be determined
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "S",
    },
    "TRAN-EX": {
        "model_number": "LS8000/2-TRAN-EX-S-10\"",
        "description": "TRAN-EX Level Switch - Base Configuration",
        "base_price": 850.0,
        "base_length": 10.0,
        "voltage": "115VAC",
        "material": "S",
        "process_connection_type": "NPT",
        "process_connection_size": '3/4"',
    },
}


def get_base_model(family_name: str) -> dict:
    """Get base model configuration for a product family."""
    return BASE_MODELS.get(family_name, {})


def get_base_price(family_name: str) -> float:
    """Get base price for a product family."""
    model = get_base_model(family_name)
    return model.get("base_price", 0.0)


def get_all_base_models() -> dict:
    """Get all base model configurations."""
    return BASE_MODELS.copy()


def get_family_names() -> list:
    """Get list of all product family names."""
    return list(BASE_MODELS.keys())


# Original pricing data for reference
ORIGINAL_PRICING = """
LS2000-115VAC-S-10"  =  425
LS2100-24VDC-S-10"  =  460
LS6000-115VAC-S-10"  =  550
LS7000-115VAC-S-10"  =  680
LS7000/2-115VAC-H-10"  =  770
LS8000-115VAC-S-10"  =  715
LS8000/2-115VAC-H-10"  =  850
LT9000-115VAC-H-10"  =  855
FS10000-115VAC-S-6"  =  1885
"""
