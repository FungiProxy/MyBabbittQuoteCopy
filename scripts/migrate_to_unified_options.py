#!/usr/bin/env python3
"""
Migration script to populate the unified options table from legacy option tables.

This script migrates data from the scattered legacy option tables into the unified
options table structure. It works directly with the database schema using raw SQL
to avoid dependency on missing models.

It handles:
1. Materials (materials + material_options)
2. Voltages (voltages + voltage_options)
3. Connections (connections + connection_options)
4. Accessories (accessories + accessory_options)
5. Housing Types (housing_types + housing_type_options)
6. Insulators (insulators + insulator_options)
7. Exotic Metals (exotic_metals + exotic_metal_options)
8. O-Ring Materials (o_ring_materials + o_ring_material_options)
9. Probe Modifications (probe_modifications + probe_modification_options)

The script preserves all pricing information, compatibility rules, and relationships
while transforming the data into the unified options table format.
"""

import logging
import sys
import os
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add the absolute path to the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from core.database import SessionLocal, engine
from core.models.option import Option
from core.models.product_variant import ProductFamily

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class OptionsMigration:
    """Handles migration of legacy option tables to unified options table."""

    def __init__(self, db: Session):
        self.db = db
        self.migration_stats = {
            "materials": 0,
            "voltages": 0,
            "connections": 0,
            "accessories": 0,
            "housing_types": 0,
            "insulators": 0,
            "exotic_metals": 0,
            "o_ring_materials": 0,
            "probe_modifications": 0,
            "total_options": 0,
        }

    def get_product_family_names(self) -> Dict[int, str]:
        """Get mapping of product family IDs to names."""
        families = self.db.query(ProductFamily).all()
        return {f.id: f.name for f in families}

    def migrate_materials(self):
        """Migrate materials and material_options to unified options table."""
        logger.info("Migrating materials...")

        # Get all materials with their options using raw SQL
        query = text(
            """
            SELECT 
                m.id, m.code, m.name, m.description, m.base_length, 
                m.length_adder_per_inch, m.length_adder_per_foot,
                m.has_nonstandard_length_surcharge, m.nonstandard_length_surcharge,
                m.base_price_adder,
                mo.product_family_id, mo.display_name, mo.base_price, mo.is_available
            FROM materials m
            LEFT JOIN material_options mo ON m.code = mo.material_code
            ORDER BY m.code, mo.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by material code
        materials_by_code = {}
        for row in rows:
            code = row.code
            if code not in materials_by_code:
                materials_by_code[code] = {"material": row, "options": []}
            if row.product_family_id:
                materials_by_code[code]["options"].append(row)

        # Create unified options for each material
        for code, data in materials_by_code.items():
            material = data["material"]
            options = data["options"]

            # Build choices and adders
            choices = []
            adders = {}

            for opt in options:
                choice_data = {
                    "code": material.code,
                    "display_name": opt.display_name,
                    "base_price": opt.base_price,
                }
                choices.append(choice_data)
                adders[material.code] = opt.base_price

            # Get product families that support this material
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Material",
                description=f"Material options for {material.name}",
                price=0.0,  # Base price is 0, adders are in the choices
                price_type="fixed",
                category="Material",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
                rules=(
                    f'Base length: {material.base_length}", Length adder: ${material.length_adder_per_foot}/foot'
                    if material.length_adder_per_foot
                    else None
                ),
            )

            self.db.add(option)
            self.migration_stats["materials"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created material option: {material.name}")

    def migrate_voltages(self):
        """Migrate voltages and voltage_options to unified options table."""
        logger.info("Migrating voltages...")

        # Get all voltages with their options using raw SQL
        query = text(
            """
            SELECT 
                v.id, v.name, v.description, v.base_price_adder,
                vo.product_family_id, vo.price, vo.is_available
            FROM voltages v
            LEFT JOIN voltage_options vo ON v.id = vo.voltage_id
            ORDER BY v.name, vo.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by voltage
        voltages_by_name = {}
        for row in rows:
            name = row.name
            if name not in voltages_by_name:
                voltages_by_name[name] = {"voltage": row, "options": []}
            if row.product_family_id:
                voltages_by_name[name]["options"].append(row)

        # Create unified options for each voltage
        for name, data in voltages_by_name.items():
            voltage = data["voltage"]
            options = data["options"]

            # Build choices and adders
            choices = [voltage.name]
            adders = {voltage.name: voltage.base_price_adder or 0.0}

            # Get product families that support this voltage
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Voltage",
                description=f"Voltage options: {voltage.description or voltage.name}",
                price=voltage.base_price_adder or 0.0,
                price_type="fixed",
                category="Voltage",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["voltages"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created voltage option: {voltage.name}")

    def migrate_connections(self):
        """Migrate connections and connection_options to unified options table."""
        logger.info("Migrating connections...")

        # Get all connections with their options using raw SQL
        query = text(
            """
            SELECT 
                c.id, c.type, c.size, c.rating, c.description, c.base_price_adder, c.material,
                co.product_family_id, co.price, co.is_available
            FROM connections c
            LEFT JOIN connection_options co ON c.id = co.connection_id
            ORDER BY c.type, c.size, co.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by connection
        connections_by_id = {}
        for row in rows:
            conn_id = row.id
            if conn_id not in connections_by_id:
                connections_by_id[conn_id] = {"connection": row, "options": []}
            if row.product_family_id:
                connections_by_id[conn_id]["options"].append(row)

        # Create unified options for each connection
        for conn_id, data in connections_by_id.items():
            connection = data["connection"]
            options = data["options"]

            # Build choices and adders
            choice_name = f"{connection.type} {connection.size} {connection.rating}"
            choices = [choice_name]
            adders = {choice_name: connection.base_price_adder or 0.0}

            # Get product families that support this connection
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Connection",
                description=f"Connection options: {connection.description}",
                price=connection.base_price_adder or 0.0,
                price_type="fixed",
                category="Connection",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["connections"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created connection option: {choice_name}")

    def migrate_accessories(self):
        """Migrate accessories and accessory_options to unified options table."""
        logger.info("Migrating accessories...")

        # Get all accessories with their options using raw SQL
        query = text(
            """
            SELECT 
                a.id, a.name, a.description, a.price_type, a.base_price_adder,
                ao.product_family_id, ao.price, ao.is_available
            FROM accessories a
            LEFT JOIN accessory_options ao ON a.id = ao.accessory_id
            ORDER BY a.name, ao.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by accessory
        accessories_by_id = {}
        for row in rows:
            acc_id = row.id
            if acc_id not in accessories_by_id:
                accessories_by_id[acc_id] = {"accessory": row, "options": []}
            if row.product_family_id:
                accessories_by_id[acc_id]["options"].append(row)

        # Create unified options for each accessory
        for acc_id, data in accessories_by_id.items():
            accessory = data["accessory"]
            options = data["options"]

            # Build choices and adders
            choices = [accessory.name]
            adders = {accessory.name: accessory.base_price_adder or 0.0}

            # Get product families that support this accessory
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Accessory",
                description=f"Accessory options: {accessory.description}",
                price=accessory.base_price_adder or 0.0,
                price_type=accessory.price_type or "fixed",
                category="Accessory",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["accessories"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created accessory option: {accessory.name}")

    def migrate_housing_types(self):
        """Migrate housing_types and housing_type_options to unified options table."""
        logger.info("Migrating housing types...")

        # Get all housing types with their options using raw SQL
        query = text(
            """
            SELECT 
                ht.id, ht.name, ht.description,
                hto.product_family_id, hto.price, hto.is_available
            FROM housing_types ht
            LEFT JOIN housing_type_options hto ON ht.id = hto.housing_type_id
            ORDER BY ht.name, hto.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by housing type
        housing_types_by_id = {}
        for row in rows:
            ht_id = row.id
            if ht_id not in housing_types_by_id:
                housing_types_by_id[ht_id] = {"housing_type": row, "options": []}
            if row.product_family_id:
                housing_types_by_id[ht_id]["options"].append(row)

        # Create unified options for each housing type
        for ht_id, data in housing_types_by_id.items():
            housing_type = data["housing_type"]
            options = data["options"]

            # Build choices and adders
            choices = [housing_type.name]
            adders = {
                housing_type.name: 0.0
            }  # Housing types typically don't have adders

            # Get product families that support this housing type
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Housing Type",
                description=f"Housing type options: {housing_type.description}",
                price=0.0,
                price_type="fixed",
                category="Housing",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["housing_types"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created housing type option: {housing_type.name}")

    def migrate_insulators(self):
        """Migrate insulators and insulator_options to unified options table."""
        logger.info("Migrating insulators...")

        # Get all insulators with their options using raw SQL
        query = text(
            """
            SELECT 
                i.id, i.name, i.description, i.base_price_adder,
                io.product_family_id, io.price, io.is_available
            FROM insulators i
            LEFT JOIN insulator_options io ON i.id = io.insulator_id
            ORDER BY i.name, io.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by insulator
        insulators_by_id = {}
        for row in rows:
            ins_id = row.id
            if ins_id not in insulators_by_id:
                insulators_by_id[ins_id] = {"insulator": row, "options": []}
            if row.product_family_id:
                insulators_by_id[ins_id]["options"].append(row)

        # Create unified options for each insulator
        for ins_id, data in insulators_by_id.items():
            insulator = data["insulator"]
            options = data["options"]

            # Build choices and adders
            choices = [insulator.name]
            adders = {insulator.name: insulator.base_price_adder or 0.0}

            # Get product families that support this insulator
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Insulator",
                description=f"Insulator options: {insulator.description}",
                price=insulator.base_price_adder or 0.0,
                price_type="fixed",
                category="Insulator",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["insulators"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created insulator option: {insulator.name}")

    def migrate_exotic_metals(self):
        """Migrate exotic_metals and exotic_metal_options to unified options table."""
        logger.info("Migrating exotic metals...")

        # Get all exotic metals with their options using raw SQL
        query = text(
            """
            SELECT 
                em.id, em.name, em.description, em.base_price_adder,
                emo.product_family_id, emo.price, emo.is_available
            FROM exotic_metals em
            LEFT JOIN exotic_metal_options emo ON em.id = emo.exotic_metal_id
            ORDER BY em.name, emo.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by exotic metal
        exotic_metals_by_id = {}
        for row in rows:
            em_id = row.id
            if em_id not in exotic_metals_by_id:
                exotic_metals_by_id[em_id] = {"exotic_metal": row, "options": []}
            if row.product_family_id:
                exotic_metals_by_id[em_id]["options"].append(row)

        # Create unified options for each exotic metal
        for em_id, data in exotic_metals_by_id.items():
            exotic_metal = data["exotic_metal"]
            options = data["options"]

            # Build choices and adders
            choices = [exotic_metal.name]
            adders = {exotic_metal.name: exotic_metal.base_price_adder or 0.0}

            # Get product families that support this exotic metal
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Exotic Metal",
                description=f"Exotic metal options: {exotic_metal.description}",
                price=exotic_metal.base_price_adder or 0.0,
                price_type="fixed",
                category="Exotic Metal",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["exotic_metals"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created exotic metal option: {exotic_metal.name}")

    def migrate_o_ring_materials(self):
        """Migrate o_ring_materials and o_ring_material_options to unified options table."""
        logger.info("Migrating O-ring materials...")

        # Get all O-ring materials with their options using raw SQL
        query = text(
            """
            SELECT 
                orm.id, orm.name, orm.description, orm.base_price_adder,
                ormo.product_family_id, ormo.price, ormo.is_available
            FROM o_ring_materials orm
            LEFT JOIN o_ring_material_options ormo ON orm.id = ormo.o_ring_material_id
            ORDER BY orm.name, ormo.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by O-ring material
        o_ring_materials_by_id = {}
        for row in rows:
            orm_id = row.id
            if orm_id not in o_ring_materials_by_id:
                o_ring_materials_by_id[orm_id] = {"o_ring_material": row, "options": []}
            if row.product_family_id:
                o_ring_materials_by_id[orm_id]["options"].append(row)

        # Create unified options for each O-ring material
        for orm_id, data in o_ring_materials_by_id.items():
            o_ring_material = data["o_ring_material"]
            options = data["options"]

            # Build choices and adders
            choices = [o_ring_material.name]
            adders = {o_ring_material.name: o_ring_material.base_price_adder or 0.0}

            # Get product families that support this O-ring material
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="O-Ring Material",
                description=f"O-ring material options: {o_ring_material.description}",
                price=o_ring_material.base_price_adder or 0.0,
                price_type="fixed",
                category="O-Ring Material",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["o_ring_materials"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(f"Created O-ring material option: {o_ring_material.name}")

    def migrate_probe_modifications(self):
        """Migrate probe_modifications and probe_modification_options to unified options table."""
        logger.info("Migrating probe modifications...")

        # Get all probe modifications with their options using raw SQL
        query = text(
            """
            SELECT 
                pm.id, pm.name, pm.description, pm.base_price_adder,
                pmo.product_family_id, pmo.price, pmo.is_available
            FROM probe_modifications pm
            LEFT JOIN probe_modification_options pmo ON pm.id = pmo.probe_modification_id
            ORDER BY pm.name, pmo.product_family_id
        """
        )

        result = self.db.execute(query)
        rows = result.fetchall()

        # Group by probe modification
        probe_modifications_by_id = {}
        for row in rows:
            pm_id = row.id
            if pm_id not in probe_modifications_by_id:
                probe_modifications_by_id[pm_id] = {
                    "probe_modification": row,
                    "options": [],
                }
            if row.product_family_id:
                probe_modifications_by_id[pm_id]["options"].append(row)

        # Create unified options for each probe modification
        for pm_id, data in probe_modifications_by_id.items():
            probe_modification = data["probe_modification"]
            options = data["options"]

            # Build choices and adders
            choices = [probe_modification.name]
            adders = {
                probe_modification.name: probe_modification.base_price_adder or 0.0
            }

            # Get product families that support this probe modification
            family_names = []
            for opt in options:
                family = (
                    self.db.query(ProductFamily)
                    .filter_by(id=opt.product_family_id)
                    .first()
                )
                if family:
                    family_names.append(family.name)

            # Create the unified option
            option = Option(
                name="Probe Modification",
                description=f"Probe modification options: {probe_modification.description}",
                price=probe_modification.base_price_adder or 0.0,
                price_type="fixed",
                category="Probe Modification",
                product_families=",".join(family_names) if family_names else None,
                choices=choices,
                adders=adders,
            )

            self.db.add(option)
            self.migration_stats["probe_modifications"] += 1
            self.migration_stats["total_options"] += 1

            logger.debug(
                f"Created probe modification option: {probe_modification.name}"
            )

    def run_migration(self):
        """Run the complete migration process."""
        logger.info("Starting migration to unified options table...")

        try:
            # Clear existing options (if any)
            self.db.query(Option).delete()
            logger.info("Cleared existing options table")

            # Run all migrations
            self.migrate_materials()
            self.migrate_voltages()
            self.migrate_connections()
            self.migrate_accessories()
            self.migrate_housing_types()
            self.migrate_insulators()
            self.migrate_exotic_metals()
            self.migrate_o_ring_materials()
            self.migrate_probe_modifications()

            # Commit all changes
            self.db.commit()

            logger.info("Migration completed successfully!")
            self.print_stats()

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            self.db.rollback()
            raise

    def print_stats(self):
        """Print migration statistics."""
        logger.info("=" * 50)
        logger.info("MIGRATION STATISTICS")
        logger.info("=" * 50)
        for category, count in self.migration_stats.items():
            if category != "total_options":
                logger.info(f"{category.replace('_', ' ').title()}: {count}")
        logger.info(f"Total Options Created: {self.migration_stats['total_options']}")
        logger.info("=" * 50)


def main():
    """Main function to run the migration."""
    logger.info("Starting Options Migration Script")

    # Create database session
    db = SessionLocal()

    try:
        # Run migration
        migrator = OptionsMigration(db)
        migrator.run_migration()

        logger.info("Migration completed successfully!")

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
