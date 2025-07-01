import logging
from typing import Optional, Any

from sqlalchemy.orm import Session

from src.core.models.configuration import Configuration
from src.core.pricing import PricingContext, calculate_product_price
from src.core.services.product_service import ProductService

# Set up logging
logger = logging.getLogger(__name__)


class ConfigurationService:
    """
    Manages the business logic of configuring a product.
    This service is responsible for creating a configuration session,
    handling option selections, validating the configuration, and calculating the final price.
    """

    def __init__(self, db: Session, product_service: ProductService):
        self.db = db
        self.product_service = product_service
        self._current_config: Optional[Configuration] = None
        # logger.debug("ConfigurationService initialized")

    @property
    def current_config(self) -> Optional[Configuration]:
        """Get the current configuration."""
        return self._current_config

    @current_config.setter
    def current_config(self, value: Optional[Configuration]):
        """Set the current configuration."""
        self._current_config = value
        if value:
            # logger.debug(
            #     f"Current configuration set for product family: {value.product_family_name}"
            # )
            pass
        else:
            # logger.debug("Current configuration cleared")
            pass

    def start_configuration(
        self, product_family_id: int, product_family_name: str, base_product_info: dict, selected_options: Optional[dict] = None
    ):
        """
        Start a new configuration session for a product family.

        Args:
            product_family_id (int): The ID of the product family.
            product_family_name (str): The name of the product family.
            base_product_info (dict): Information about the base product.
            selected_options (dict, optional): Initial selected options (e.g., {'material': 'H'})
        """
        print(f"[DEBUG] start_configuration() called")
        print(f"[DEBUG] product_family_id: {product_family_id}")
        print(f"[DEBUG] product_family_name: {product_family_name}")
        print(f"[DEBUG] base_product_info: {base_product_info}")
        print(f"[DEBUG] base_product_info type: {type(base_product_info)}")
        print(f"[DEBUG] selected_options: {selected_options}")
        try:
            # Normalize selected_options to use 'Material' as the key
            normalized_options = {}
            if selected_options:
                for k, v in selected_options.items():
                    if k.lower() == 'material':
                        normalized_options['Material'] = v
                    elif k.lower() == 'voltage':
                        normalized_options['Voltage'] = v
                    else:
                        normalized_options[k] = v
            # Create a new configuration
            self.current_config = Configuration(
                db=self.db,
                product_family_id=product_family_id,
                product_family_name=product_family_name,
                base_product=base_product_info,
                selected_options=normalized_options.copy() if normalized_options else {},
                final_price=0.0,
                final_description="",
                model_number="",
                quantity=1,
                is_valid=False,
                validation_errors=[],
            )
            print(f"[DEBUG] Configuration created successfully")
            print(f"[DEBUG] Current config selected_options: {self.current_config.selected_options}")
            # Set default material and voltage from base product ONLY if not already set
            if (not normalized_options or 'Material' not in normalized_options) and "material" in base_product_info:
                print(f"[DEBUG] set_option Material: {base_product_info['material']} (type: {type(base_product_info['material'])})")
                self.set_option("Material", base_product_info["material"])
            # Skip voltage for TRAN-EX since it has no voltage options
            if (product_family_name != "TRAN-EX" and 
                (not normalized_options or 'Voltage' not in normalized_options) and 
                "voltage" in base_product_info):
                print(f"[DEBUG] set_option Voltage: {base_product_info['voltage']} (type: {type(base_product_info['voltage'])})")
                self.set_option("Voltage", base_product_info["voltage"])
            elif product_family_name == "TRAN-EX":
                print(f"[DEBUG] Skipping voltage for TRAN-EX - no voltage options")
            print(f"[DEBUG] About to call _update_price()")
            self._update_price()
            print(f"[DEBUG] About to call _update_model_number()")
            self._update_model_number()
            print(f"[DEBUG] start_configuration completed successfully")
        except Exception as e:
            print(f"[DEBUG] Error creating configuration: {e}")
            print(f"[DEBUG] Error type: {type(e)}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            raise

    def set_option(self, option_name: str, value: Any):
        """Set an option in the current configuration."""
        print(f"[DEBUG] set_option called: {option_name} = {value} (type: {type(value)})")
        if self._current_config:
            # Defensive: If value is a dict, extract 'code' if present
            if isinstance(value, dict):
                print(f"[DEBUG] set_option received dict for {option_name}: {value}")
                if 'code' in value:
                    value = value['code']
                    print(f"[DEBUG] Extracted code: {value}")
                else:
                    value = str(value)
                    print(f"[DEBUG] Converted to string: {value}")
            self._current_config.set_option(option_name, value)
            print(f"[DEBUG] After set_option, selected_options: {self._current_config.selected_options}")
            self._update_price()
            self._update_model_number()

    def select_option(self, option_name: str, value: Any):
        """
        Updates the current configuration with a selected option.

        Args:
            option_name (str): The name of the option (e.g., "Material", "Length").
            value (any): The selected value for the option.
        """
        print(f"DEBUG: select_option called with {option_name}={value}")

        if not self.current_config:
            print("DEBUG: No current configuration")
            return

        # Store the current material before updating options
        current_material = self.current_config.selected_options.get("Material")
        if not current_material:
            current_material = self.current_config.base_product.get("material")

        # Update the selected option
        if option_name == "Material":
            print(f"DEBUG: Processing material selection: {value}")
            # If the value is a number (like a length), don't update it
            if str(value).isdigit():
                print(
                    f"DEBUG: Material value {value} is numeric, keeping current material: {current_material}"
                )
                self.current_config.selected_options["Material"] = current_material
            else:
                print(f"DEBUG: Updating material to: {value}")
                self.current_config.selected_options["Material"] = value
        else:
            print(f"DEBUG: Updating option {option_name} to: {value}")
            self.current_config.selected_options[option_name] = value

        print("DEBUG: About to call _update_price()")
        # Update the model number and price
        self._update_model_number()
        self._update_price()
        print("DEBUG: Finished _update_price()")
        print(f"DEBUG: Final configuration: {self.current_config.selected_options}")

    def _update_model_number(self):
        """Update the model number based on selected options."""
        print(f"[DEBUG] _update_model_number() called")
        if not self.current_config:
            print(f"[DEBUG] No current configuration in _update_model_number")
            return

        print(f"[DEBUG] _update_model_number - selected_options: {self.current_config.selected_options}")
        print(f"[DEBUG] _update_model_number - selected_options types:")
        for k, v in self.current_config.selected_options.items():
            print(f"  {k}: {v} (type: {type(v)})")
        
        # logger.debug("Updating model number")
        # Implementation details...
        print(f"[DEBUG] _update_model_number completed")

    def _get_current_variant(self):
        """Get the current product variant based on selected options."""
        if not self.current_config:
            # logger.warning("No current configuration when trying to get variant")
            return None

        print(f"[DEBUG] _get_current_variant() called")
        print(f"[DEBUG] product_family_id: {self.current_config.product_family_id}")
        print(f"[DEBUG] selected_options: {self.current_config.selected_options}")
        print(f"[DEBUG] selected_options types:")
        for k, v in self.current_config.selected_options.items():
            print(f"  {k}: {v} (type: {type(v)})")

        try:
            # Find the specific variant that matches the current selection
            print(f"[DEBUG] About to call product_service.find_variant()")
            variant = self.product_service.find_variant(
                self.db,
                self.current_config.product_family_id,
                self.current_config.selected_options,
            )
            print(f"[DEBUG] find_variant returned: {variant}")

            if not variant:
                # logger.warning(
                #     f"No matching variant found for options: {self.current_config.selected_options}"
                # )
                print(f"[DEBUG] No matching variant found")
                return None

            return variant

        except Exception as e:
            print(f"[DEBUG] Error in _get_current_variant: {e}")
            print(f"[DEBUG] Error type: {type(e)}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            logger.error(f"Error getting current variant: {e!s}", exc_info=True)
            return None

    def _get_option_price(self, option_name: str, value: Any) -> float:
        """Get the price for a given option and its selected value using the unified options structure."""
        if not self.current_config:
            return 0.0

        try:
            # Get all options for this product family
            all_options = self.product_service.get_additional_options(
                self.db, self.current_config.product_family_name
            )

            # Find the specific option
            for option in all_options:
                if option.get("name") == option_name:
                    adders = option.get("adders", {})
                    if isinstance(adders, dict) and value in adders:
                        return float(adders[value])
                    break

            # Fallback to configuration's get_option_price method
            price = self.current_config.get_option_price(option_name, value)
            # logger.debug(f"Price for {option_name}={value}: ${price:,.2f}")
            return price
        except Exception as e:
            logger.error(f"Error getting option price: {e!s}", exc_info=True)
            return 0.0

    def _to_float(self, value, default=0.0):
        """Convert value to float, handling MagicMock and None."""
        try:
            if value is None:
                return default

            # Handle MagicMock objects - get the actual value without recursion
            if hasattr(value, "return_value"):
                value = value.return_value
            if hasattr(value, "base_price"):
                value = value.base_price
            if hasattr(value, "price"):
                value = value.price
            if hasattr(value, "adder"):
                value = value.adder
            if hasattr(value, "price_multiplier"):
                value = value.price_multiplier
            if hasattr(value, "length"):
                value = value.length

            # Handle basic types
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                return float(value)
            return default
        except (TypeError, ValueError):
            return default

    def _update_price(self):
        """Update the price based on the current configuration."""
        if not self.current_config:
            return

        print(f"[DEBUG] _update_price() called")
        print(f"[DEBUG] Current selected_options: {self.current_config.selected_options}")
        print(f"[DEBUG] Selected options types:")
        for k, v in self.current_config.selected_options.items():
            print(f"  {k}: {v} (type: {type(v)})")

        effective_length = self.current_config.get_effective_length()
        material_code = self.current_config.get_selected_material_code()

        print(f"[DEBUG] effective_length: {effective_length} (type: {type(effective_length)})")
        print(f"[DEBUG] material_code: {material_code} (type: {type(material_code)})")

        base_product = self.current_config.base_product
        if not base_product or "id" not in base_product:
            logger.error("Base product not found or missing ID in configuration.")
            return

        print(f"[DEBUG] base_product: {base_product}")
        print(f"[DEBUG] Creating PricingContext with specs: {self.current_config.selected_options}")

        # Create a pricing context
        context = PricingContext(
            db=self.db,
            product_id=base_product["id"],
            length_in=effective_length,
            material_override_code=material_code,
            specs=self.current_config.selected_options,
        )

        print(f"[DEBUG] PricingContext created successfully")
        print(f"[DEBUG] About to call calculate_product_price()")

        # Calculate price using the pricing engine
        try:
            self.current_config.final_price = calculate_product_price(context)
            print(f"[DEBUG] Price calculation successful: ${self.current_config.final_price}")
            print(f"[DEBUG] About to call _update_model_number()")
            print(f"[DEBUG] selected_options before _update_model_number: {self.current_config.selected_options}")
            # --- TRAN-EX H MATERIAL ADDER FIX ---
            if self.current_config.product_family_name == "TRAN-EX":
                material = self.current_config.selected_options.get("Material")
                if material == "H":
                    print(f"[DEBUG] Applying TRAN-EX H material base adder: $110")
                    self.current_config.final_price += 110  # base adder
                    print(f"[DEBUG] New final price after H base adder: ${self.current_config.final_price}")
            # --- END FIX ---
        except Exception as e:
            print(f"[DEBUG] Error in calculate_product_price: {e}")
            print(f"[DEBUG] Error type: {type(e)}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            raise

    def generate_model_number(self) -> str:
        """Generates the model number based on the current configuration."""
        if not self.current_config:
            return ""

        config = self.current_config
        family = config.product_family_name

        # Special handling for TRAN-EX
        if family == "TRAN-EX":
            material = config.selected_options.get("Material")
            length = config.selected_options.get("Probe Length", config.base_product.get("base_length", 10))
            if not material:
                material = "S"
                config.selected_options["Material"] = material
            material_map = {
                "316SS": "S",
                "304SS": "S",
                "Hastelloy C": "H",
                "Monel": "M",
                "Titanium": "T",
                "Inconel": "I",
            }
            material_code = (
                material if len(str(material)) == 1 else material_map.get(str(material), material)
            )
            try:
                length_val = float(length)
                length_str = (
                    f'{int(length_val)}"' if length_val.is_integer() else f'{length_val}"'
                )
            except (ValueError, TypeError):
                length_str = f'{length}"' if length else 'LENGTH"'
            return f"LS8000/2-TRAN-EX-{material_code}-{length_str}"

        voltage = config.selected_options.get("Voltage")
        material = config.selected_options.get("Material")
        length = config.selected_options.get("Probe Length", config.base_product.get("base_length", 10))
        if not voltage:
            family_defaults = {
                "LS2000": "115VAC",
                "LS2100": "115VAC",
                "LS7000": "115VAC",
                "LS7500": "115VAC",
                "LS8500": "115VAC",
                "LT9000": "115VAC",
                "FS10000": "115VAC",
                "LS1000": "24VDC",
                "LS6000": "115VAC",
                "LS8000": "115VAC",
            }
            voltage = family_defaults.get(family, "115VAC")
            config.selected_options["Voltage"] = voltage
        if not material:
            material = "S"
            config.selected_options["Material"] = material
        material_map = {
            "316SS": "S",
            "304SS": "S",
            "Hastelloy C": "H",
            "Monel": "M",
            "Titanium": "T",
            "Inconel": "I",
        }
        material_code = (
            material if len(str(material)) == 1 else material_map.get(str(material), material)
        )
        try:
            length_val = float(length)
            length_str = (
                f'{int(length_val)}"' if length_val.is_integer() else f'{length_val}"'
            )
        except (ValueError, TypeError):
            length_str = f'{length}"' if length else 'LENGTH"'

        part_number_parts = [family, voltage, material_code, length_str]
        process_connection = self._get_process_connection_code(config.selected_options)
        if process_connection:
            part_number_parts.append(process_connection)
        additional_codes = self._get_additional_option_codes(config.selected_options)
        part_number_parts.extend(additional_codes)
        # Debug output
        print("[DEBUG] Part number components:", part_number_parts)
        return "-".join([str(p) for p in part_number_parts if p])

    def _get_process_connection_code(self, selected_options: dict) -> str:
        """Extract process connection code from selected options, only if non-base."""
        print(f"[DEBUG] _get_process_connection_code - selected_options: {selected_options}")
        
        connection_type = selected_options.get("Connection Type")
        print(f"[DEBUG] Connection Type: {connection_type}")
        
        if not connection_type:
            print(f"[DEBUG] No connection type found, returning empty string")
            return ""
        
        # Get base model defaults for comparison
        from src.core.config.base_models import get_base_model
        product_family = getattr(self.current_config, 'product_family_name', 'LS2000')
        base_model = get_base_model(product_family)
        base_connection_type = base_model.get("process_connection_type")
        base_connection_size = base_model.get("process_connection_size")
        
        print(f"[DEBUG] Base model defaults - type: {base_connection_type}, size: {base_connection_size}")
        
        # Check if current selection matches base defaults
        if connection_type == base_connection_type:
            if connection_type == "NPT":
                npt_size = selected_options.get("NPT Size", "3/4")
                # Normalize both values for comparison
                npt_size_norm = str(npt_size).replace('"', '').strip()
                base_size_norm = str(base_connection_size).replace('"', '').strip()
                print(f"[DEBUG] Comparing NPT sizes: user='{npt_size_norm}' base='{base_size_norm}'")
                if npt_size_norm == base_size_norm:
                    print(f"[DEBUG] NPT selection matches base defaults ({npt_size_norm}), returning empty string")
                    return ""
            
        # If we get here, the selection is different from base defaults
        if connection_type == "NPT":
            npt_size = selected_options.get("NPT Size", "3/4")
            code = f'{npt_size}"NPT'
            print(f"[DEBUG] NPT connection code (non-base): {code}")
            return code
        elif connection_type == "Flange":
            flange_size = selected_options.get("Flange Size", "2")
            flange_rating = selected_options.get("Flange Rating", "150#")
            code = f'{flange_size}"{flange_rating}'
            print(f"[DEBUG] Flange connection code (non-base): {code}")
            return code
        elif connection_type == "Tri-clamp":
            tri_clamp = selected_options.get("Tri-clamp", "")
            print(f"[DEBUG] Tri-clamp value: {tri_clamp}")
            
            if "Spud" in tri_clamp:
                if "1-1/2" in tri_clamp:
                    code = 'TC1-1/2"SPD'
                elif "2" in tri_clamp:
                    code = 'TC2"SPD'
                else:
                    code = "TC"
            else:
                if "1-1/2" in tri_clamp:
                    code = 'TC1-1/2"'
                elif "2" in tri_clamp:
                    code = 'TC2"'
                else:
                    code = "TC"
            
            print(f"[DEBUG] Tri-clamp connection code (non-base): {code}")
            return code
        else:
            print(f"[DEBUG] Unknown connection type: {connection_type}")
            return ""

    def _get_additional_option_codes(self, selected_options: dict) -> list:
        """Extract codes for all additional options, preserving order and skipping empty/defaults."""
        codes = []
        
        # Debug the selected options
        print(f"[DEBUG] _get_additional_option_codes - selected_options: {selected_options}")
        
        # Extra Static Protection - handle both "Yes" and True
        extra_static = selected_options.get("Extra Static Protection")
        if extra_static == "Yes" or extra_static is True:
            codes.append("XSP")
            print(f"[DEBUG] Added XSP code")
        
        # Stainless Steel Tag - handle both "Yes" and True
        stainless_tag = selected_options.get("Stainless Steel Tag")
        if stainless_tag == "Yes" or stainless_tag is True:
            codes.append("SSTAG")
            print(f"[DEBUG] Added SSTAG code")
        
        # Vibration Resistance - handle both "Yes" and True
        vibration_resistance = selected_options.get("Vibration Resistance")
        if vibration_resistance == "Yes" or vibration_resistance is True:
            codes.append("VR")
            print(f"[DEBUG] Added VR code")
        
        # Epoxy House - handle both "Yes" and True
        epoxy_house = selected_options.get("Epoxy House")
        if epoxy_house == "Yes" or epoxy_house is True:
            codes.append("EPOX")
            print(f"[DEBUG] Added EPOX code")
        
        # Bent Probe - handle both "Yes" and True
        bent_probe = selected_options.get("Bent Probe")
        if bent_probe == "Yes" or bent_probe is True:
            deg = selected_options.get("Bent Probe Degree")
            if deg:
                codes.append(f"{deg}DEG")
                print(f"[DEBUG] Added {deg}DEG code")
        
        # 3/4" Diameter Probe - handle both "Yes" and True
        probe_3_4 = selected_options.get('3/4" Diameter Probe')
        if probe_3_4 == "Yes" or probe_3_4 is True:
            codes.append("3/4OD")
            print(f"[DEBUG] Added 3/4OD code")
        
        # Insulator Material - handle actual codes from database
        # Only add insulator material if it's explicitly selected (not base setup)
        ins_mat = selected_options.get("Insulator Material")
        ins_len = selected_options.get("Insulator Length")
        
        # Map database codes to part number codes
        ins_mat_map = {
            "TEF": "TEFINS",  # Teflon Upgrade
            "PK": "PEEKINS",  # PEEK
            "CER": "CERINS",  # Ceramic
            "DEL": "DELINS",  # Delrin
            "Teflon Upgrade": "TEFINS",
            "PEEK": "PEEKINS", 
            "Ceramic": "CERINS",
            "Delrin": "DELINS",
        }
        
        # Only add insulator material code if it's explicitly selected and not the base/default
        if ins_mat and ins_mat in ins_mat_map:
            # Define base insulator materials for each product family
            # These are the default/standard insulator materials that should NOT add codes
            base_insulator_materials = {
                "LS2000": ["Standard", "Default", "", "S"],  # S material is base for LS2000
                "LS2100": ["Standard", "Default", "", "S"],
                "LS6000": ["Standard", "Default", "", "S"],
                "LS7000": ["Standard", "Default", "", "S"],
                "LS7500": ["Standard", "Default", "", "S"],
                "LS8000": ["Standard", "Default", "", "S"],
                "LS8500": ["Standard", "Default", "", "S"],
                "LT9000": ["Standard", "Default", "", "S"],
                "FS10000": ["Standard", "Default", "", "S"],
                "LS1000": ["Standard", "Default", "", "S"],
                "TRAN-EX": ["Standard", "Default", "", "S"],
            }
            
            # Get the current product family
            product_family = getattr(self.current_config, 'product_family_name', 'LS2000')
            base_insulators = base_insulator_materials.get(product_family, ["Standard", "Default", ""])
            
            # Check if this is a non-base insulator material selection
            # For LS2000 and LS6000, when H material is selected, TEF is automatically set
            # But if user manually changes insulator back to S, we should remove the code
            current_material = selected_options.get("Material", "S")
            
            # Special handling for H material with automatic TEF insulator
            if product_family in ["LS2000", "LS6000"] and current_material == "H":
                # If user has manually set insulator to S (base), don't add TEFINS code
                if str(ins_mat).strip() in base_insulators:
                    print(f"[DEBUG] Skipping insulator material code for {ins_mat} (user manually set to base for H material)")
                else:
                    # Auto-selected TEF for H material, add the code
                    if ins_len and str(ins_len).strip() not in ("", "Standard"):
                        clean_ins_len = str(ins_len).rstrip('"')
                        codes.append(f'{clean_ins_len}"{ins_mat_map[ins_mat]}')
                        print(f"[DEBUG] Added {clean_ins_len}\"{ins_mat_map[ins_mat]} code for {product_family} (auto-selected for H material)")
                    else:
                        codes.append(ins_mat_map[ins_mat])
                        print(f"[DEBUG] Added {ins_mat_map[ins_mat]} code for {product_family} (auto-selected for H material)")
            else:
                # Normal logic for other cases
                if str(ins_mat).strip() not in base_insulators:
                    if ins_len and str(ins_len).strip() not in ("", "Standard"):
                        # Remove any trailing quote from ins_len
                        clean_ins_len = str(ins_len).rstrip('"')
                        codes.append(f'{clean_ins_len}"{ins_mat_map[ins_mat]}')
                        print(f"[DEBUG] Added {clean_ins_len}\"{ins_mat_map[ins_mat]} code for {product_family}")
                    else:
                        codes.append(ins_mat_map[ins_mat])
                        print(f"[DEBUG] Added {ins_mat_map[ins_mat]} code for {product_family}")
                else:
                    print(f"[DEBUG] Skipping insulator material code for {ins_mat} (base material for {product_family})")
        
        print(f"[DEBUG] Final codes: {codes}")
        return codes

    def calculate_price(self) -> float:
        """Calculate the current price based on selected options."""
        if not self.current_config:
            return 0.0

        try:
            print(f"[DEBUG] ConfigurationService.calculate_price() called")
            print(f"[DEBUG] Selected options: {self.current_config.selected_options}")
            
            # Check for U or T materials specifically
            material = self.current_config.selected_options.get('Material')
            length = self.current_config.selected_options.get('Length')
            if material in ['U', 'T'] and material and length:
                print(f"[DEBUG] U/T MATERIAL DETECTED in calculate_price - Material: {material}, Length: {length}")
                
                # Get product family for length adder calculation
                product_family = self.current_config.product_family_name
                print(f"[DEBUG] Product family for length adder: {product_family}")
                
                # Calculate length adder manually to verify
                if product_family:
                    try:
                        length_adder = self.product_service.calculate_length_price(
                            product_family, str(material), float(length)
                        )
                        print(f"[DEBUG] Manual length adder calculation in calculate_price: ${length_adder:.2f}")
                    except Exception as e:
                        print(f"[DEBUG] Error calculating length adder in calculate_price: {e}")

            self._update_price()
            return self.current_config.final_price
        except Exception as e:
            logger.error(f"Error calculating price: {e}", exc_info=True)
            return 0.0

    def get_final_description(self) -> str:
        """
        Generates a final description based on the selected options.
        """
        if not self.current_config:
            return ""

        # Basic description, can be expanded
        desc = f"{self.current_config.product_family_name} with:"
        for name, value in self.current_config.selected_options.items():
            if value:
                desc += f" {name}: {value},"

        return desc.strip(",")

    def add_non_standard_length_adder(self):
        """Add the non-standard length surcharge to the configuration."""
        if not self.current_config:
            return

        # Add the non-standard length surcharge
        self.current_config.selected_options["NonStandardLengthSurcharge"] = True
        self.current_config.final_price = self.calculate_price()

    def remove_non_standard_length_adder(self):
        """Remove the non-standard length surcharge from the configuration."""
        if not self.current_config:
            return

        # Remove the non-standard length surcharge
        self.current_config.selected_options.pop("NonStandardLengthSurcharge", None)
        self.current_config.final_price = self.calculate_price()

    def get_final_price(self) -> float:
        """Get the final price of the configured product."""
        if not self.current_config:
            return 0.0
        return self.current_config.final_price

    def get_available_options(self, product_family_name: str) -> list:
        """
        Retrieves all available configuration options for a given product family.

        Args:
            product_family_name (str): The name of the product family.

        Returns:
            list: A list of dictionaries, where each dictionary represents an option.
        """
        # logger.debug(f"Fetching available options for product family: {product_family_name}")
        try:
            options = self.product_service.get_additional_options(self.db, product_family_name)
            # logger.debug(f"Found {len(options)} options for {product_family_name}")
            return options
        except Exception as e:
            logger.error(f"Error fetching available options for {product_family_name}: {e!s}", exc_info=True)
            return []

    # More methods will be added here to handle validation, etc.
