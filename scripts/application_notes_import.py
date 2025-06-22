"""
Script to add application notes to the database for each product family.
"""

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.database import SessionLocal, init_db
from src.core.models import ProductFamily

# Application notes from the price list
APPLICATION_NOTES = {
    "LT9000": """THE LT 9000 IS DESIGNED TO BE USED IN ELECTRICALLY CONDUCTIVE LIQUIDS THAT DO NOT LEAVE A RESIDUE ON THE PROBE. A wet electrically conductive coating will give an indication of level at the highest point that there is a continuous coating from the surface of the fluid.

The LT 9000 will give a varying output, if the conductivity of the material changes.

For proper operation, the LT 9000 must be grounded to the fluid. In non-metallic tanks, extra grounding provisions may be necessary.

LONGEST PROBE WITH HALAR IS 72" (6 FEET). FOR PROBES OVER 72", USE TEFLON SLEEVE.

For high temperatures or harsh acids, please check with the factory to see if the epoxy will be compatible with the application.""",
    
    "LS2000": """It is always good engineering practice to provide a separate, independent high level alarm for emergency shut-down in critical applications.

Material that sticks on the probe or probe guard in a repetitive on/off application may make the unit chatter or create premature failure. A probe guard should be used in turbulent or splashing applications.""",
    
    "LS2100": """It is always good engineering practice to provide a separate, independent high level alarm for emergency shut-down in critical applications.

Material that sticks on the probe or probe guard in a repetitive on/off application may make the unit chatter or create premature failure. A probe guard should be used in turbulent or splashing applications.""",
    
    "LS6000": """UNIT CAN BE SUPPLIED WITH A SENSITIVITY ADJUSTMENT OR FOR A FIXED RESISTANCE.

For critical applications, use a separate independent high level switch for emergency shut-down.

Failure to ground the probe to the material may cause chatter.

Material that sticks on the probe may affect switch operation.""",
    
    "LS7000": """UNIT CAN BE SUPPLIED WITH A SENSITIVITY ADJUSTMENT OR FOR A FIXED RESISTANCE.

For critical applications, use a separate independent high level switch for emergency shut-down.

Failure to ground the probe to the material may cause chatter.

Material that sticks on the probe may affect switch operation.""",
    
    "LS7000/2": """DESIGNED FOR USE IN ELECTRICALLY CONDUCTIVE OR SEMI-CONDUCTIVE LIQUIDS AND SLURRIES WITH CHANGING PROCESS CONDITIONS.

When using a system with 2 or 4 set points on one probe, these systems are designed for homogeneous liquids that do not change in their make-up or conductivity.

For multiple points on one probe, the fluid must be grounded to the mounting nipple. Special consideration should be taken for non-metallic tanks.

Material sticking on the probe will affect the repeatability of set points in multiple-point-on-one-probe applications.""",
    
    "LS8000": """FOR USE IN NON-METALLIC TANKS.

For critical applications, use a separate independent high level switch for emergency shut-down.

Applications with water based or electrically conductive liquids must have a Halar coated probe.

Material that sticks on the probe may affect switch operation.""",
    
    "LS8000/2": """FOR USE IN NON-METALLIC TANKS WITH MULTIPLE SET POINTS.

When using a system with 2 or 4 set points on one probe, these systems are designed for homogeneous liquids that do not change in their make-up or conductivity.

For multiple points on one probe, the fluid must be grounded to the mounting nipple.

Applications with water based or electrically conductive liquids must have a Halar coated probe.

Material sticking on the probe will affect the repeatability of set points.""",
    
    "FS10000": """FLOW/NO-FLOW SWITCH FOR ELECTRICALLY CONDUCTIVE LIQUIDS.

Must be installed in the proper flow direction as indicated on the unit.

Minimum conductivity requirements apply - consult factory for your specific application.

Not suitable for use with materials that coat or build up on the electrodes.""",
    
    "LS7500": """REPLACEMENT UNIT FOR PRINCO P/N L3515.

These units are replacement units for Princo P/N's L3515 and L3545. The LS7500 replaces L3515.

Standard flanges are 316SS Flat Face Flanges.

Specify flange sensor type: PR = Partial Ring (Conductive Media), FR = Full Ring (Non-Conductive Media)""",
    
    "LS8500": """REPLACEMENT UNIT FOR PRINCO P/N L3545.

These units are replacement units for Princo P/N's L3515 and L3545. The LS8500 replaces L3545.

Standard flanges are 316SS Flat Face Flanges.

Specify flange sensor type: PR = Partial Ring (Conductive Media), FR = Full Ring (Non-Conductive Media)"""
}


def add_application_notes_to_db():
    """Add application notes to product families in the database."""
    init_db()
    
    with SessionLocal() as db:
        for family_code, notes in APPLICATION_NOTES.items():
            # Find the product family
            family = db.query(ProductFamily).filter_by(code=family_code).first()
            
            if family:
                # Add application_notes field if it doesn't exist
                if not hasattr(family, 'application_notes'):
                    # You'll need to add this column to your ProductFamily model
                    print(f"Warning: ProductFamily model needs 'application_notes' column")
                    continue
                
                family.application_notes = notes
                print(f"Added application notes for {family_code}")
            else:
                print(f"Product family {family_code} not found")
        
        db.commit()
        print("Application notes added successfully!")


# Alternative: Create a separate ApplicationNotes table
class ApplicationNote(declarative_base()):
    """Application notes for product families."""
    __tablename__ = 'application_notes'
    
    id = Column(Integer, primary_key=True)
    product_family_code = Column(String(50), unique=True, nullable=False)
    notes = Column(Text, nullable=False)


def create_application_notes_table():
    """Create a separate table for application notes."""
    engine = create_engine('sqlite:///data/quotes.db')
    ApplicationNote.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for family_code, notes in APPLICATION_NOTES.items():
            # Check if already exists
            existing = session.query(ApplicationNote).filter_by(
                product_family_code=family_code
            ).first()
            
            if not existing:
                app_note = ApplicationNote(
                    product_family_code=family_code,
                    notes=notes
                )
                session.add(app_note)
                print(f"Added application notes for {family_code}")
            else:
                existing.notes = notes
                print(f"Updated application notes for {family_code}")
        
        session.commit()
        print("Application notes table created and populated!")
        
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


def generate_quote_from_template():
    """
    This function will generate a quote from a word template.
    """
    print("Generating quote from template...")


if __name__ == "__main__":
    # Run this to create and populate the application notes
    create_application_notes_table()
    generate_quote_from_template()