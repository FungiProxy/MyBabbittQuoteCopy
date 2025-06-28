#!/usr/bin/env python3
"""
Migration script to create proper many-to-many relationships between product families and options.

This script:
1. Creates the product_family_options table
2. Migrates data from the comma-separated product_families field to proper relationships
3. Updates the Option model to remove the product_families field
"""

import logging
import os
import sys

from sqlalchemy import text
from sqlalchemy.orm import Session

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from core.database import SessionLocal
from core.models.option import Option, ProductFamilyOption
from core.models.product_variant import ProductFamily

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RelationshipMigration:
    """Handles migration to proper many-to-many relationships."""

    def __init__(self, db: Session):
        self.db = db
        self.migration_stats = {
            "product_family_options_created": 0,
            "options_updated": 0,
        }

    def create_product_family_options_table(self):
        """Create the product_family_options table."""
        logger.info("Creating product_family_options table...")

        # Create the table using raw SQL to ensure it matches our model
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS product_family_options (
            product_family_id INTEGER NOT NULL,
            option_id INTEGER NOT NULL,
            is_available INTEGER DEFAULT 1,
            family_specific_price FLOAT,
            notes TEXT,
            PRIMARY KEY (product_family_id, option_id),
            FOREIGN KEY (product_family_id) REFERENCES product_families (id),
            FOREIGN KEY (option_id) REFERENCES options (id)
        )
        """

        self.db.execute(text(create_table_sql))
        logger.info("product_family_options table created successfully")

    def get_product_family_map(self) -> dict:
        """Get mapping of product family names to IDs."""
        families = self.db.query(ProductFamily).all()
        return {family.name: family.id for family in families}

    def migrate_relationships(self):
        """Migrate comma-separated product_families to proper relationships using raw SQL."""
        logger.info("Migrating product family relationships...")

        # Use raw SQL to get all options with product_families data
        result = self.db.execute(
            text(
                "SELECT id, product_families FROM options WHERE product_families IS NOT NULL AND product_families != ''"
            )
        )
        rows = result.fetchall()

        # Get product family mapping
        family_map = self.get_product_family_map()

        for row in rows:
            option_id = row[0]
            product_families = row[1]
            if not product_families:
                continue
            # Parse comma-separated family names
            family_names = [
                name.strip() for name in product_families.split(",") if name.strip()
            ]
            # Get the Option object
            option = self.db.query(Option).filter_by(id=option_id).first()
            if not option:
                continue
            for family_name in family_names:
                if family_name in family_map:
                    family_id = family_map[family_name]
                    # Check if relationship already exists
                    existing = (
                        self.db.query(ProductFamilyOption)
                        .filter_by(product_family_id=family_id, option_id=option.id)
                        .first()
                    )
                    if not existing:
                        # Create the relationship
                        pfo = ProductFamilyOption(
                            product_family_id=family_id,
                            option_id=option.id,
                            is_available=1,
                            family_specific_price=None,
                            notes=None,
                        )
                        self.db.add(pfo)
                        self.migration_stats["product_family_options_created"] += 1
                        logger.debug(
                            f"Created relationship: {family_name} -> {option.name}"
                        )
        logger.info(
            f"Created {self.migration_stats['product_family_options_created']} relationships"
        )

    def verify_migration(self):
        """Verify the migration was successful."""
        logger.info("Verifying migration...")

        # Count total relationships
        total_relationships = self.db.query(ProductFamilyOption).count()
        logger.info(
            f"Total product_family_options relationships: {total_relationships}"
        )

        # Count options with relationships
        options_with_relationships = (
            self.db.query(Option).join(ProductFamilyOption).distinct().count()
        )
        logger.info(f"Options with relationships: {options_with_relationships}")

        # Show sample relationships
        sample_relationships = self.db.query(ProductFamilyOption).limit(5).all()
        logger.info("Sample relationships:")
        for rel in sample_relationships:
            family = (
                self.db.query(ProductFamily).filter_by(id=rel.product_family_id).first()
            )
            option = self.db.query(Option).filter_by(id=rel.option_id).first()
            if family and option:
                logger.info(f"  {family.name} -> {option.name} ({option.category})")

    def run_migration(self):
        """Run the complete migration process."""
        logger.info("Starting relationship migration...")

        try:
            # Create the new table
            self.create_product_family_options_table()

            # Migrate the relationships
            self.migrate_relationships()

            # Commit all changes
            self.db.commit()

            # Verify the migration
            self.verify_migration()

            logger.info("Relationship migration completed successfully!")
            self.print_stats()

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            self.db.rollback()
            raise

    def print_stats(self):
        """Print migration statistics."""
        logger.info("=" * 50)
        logger.info("RELATIONSHIP MIGRATION STATISTICS")
        logger.info("=" * 50)
        for key, value in self.migration_stats.items():
            logger.info(f"{key.replace('_', ' ').title()}: {value}")
        logger.info("=" * 50)


def main():
    """Main function to run the migration."""
    logger.info("Starting Relationship Migration Script")

    # Create database session
    db = SessionLocal()

    try:
        # Run migration
        migrator = RelationshipMigration(db)
        migrator.run_migration()

        logger.info("Relationship migration completed successfully!")

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
