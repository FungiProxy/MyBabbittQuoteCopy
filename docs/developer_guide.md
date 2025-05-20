# Developer Guide

## Overview
This guide provides instructions and examples for common development tasks in the MyBabbittQuote project. It covers setup, development workflows, testing procedures, and best practices.

## Table of Contents
- [Development Environment Setup](#development-environment-setup)
- [Common Development Tasks](#common-development-tasks)
- [Working with Services](#working-with-services)
- [Database Operations](#database-operations)
- [Testing Guidelines](#testing-guidelines)
- [UI Development](#ui-development)
- [Best Practices](#best-practices)

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git
- SQLite3
- Windows 10/11 or compatible OS

### Initial Setup
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd MyBabbittQuote
   ```

2. Create and activate virtual environment:
   ```sh
   python -m venv myenv
   .\myenv\Scripts\activate  # Windows
   source myenv/bin/activate # Linux/Mac
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Initialize database:
   ```sh
   python scripts/create_db.py
   python scripts/test_db.py  # Verify setup
   ```

## Common Development Tasks

### Adding a New Product
1. Define product model in `src/core/models/product.py`
2. Add pricing rules in `src/core/pricing.py`
3. Update database schema if needed:
   ```sh
   alembic revision --autogenerate -m "Add new product fields"
   alembic upgrade head
   ```
4. Add product data through `scripts/data/products.json`
5. Run database population:
   ```sh
   python scripts/populate_db.py
   ```

### Implementing New Business Rules
1. Add rules to appropriate service class in `src/core/services/`
2. Update pricing calculations if needed in `src/core/pricing.py`
3. Add validation in service methods
4. Write tests in `tests/` directory
5. Update documentation

### Working with Customer Data
1. Use CustomerService for all customer operations:
   ```python
   from src.core.services import CustomerService
   
   # Create customer
   customer = CustomerService.create_customer(
       db,
       name="Acme Corp",
       email="contact@acme.com"
   )
   
   # Update customer
   CustomerService.update_customer(
       db,
       customer.id,
       {"address": "123 Main St"}
   )
   ```

## Working with Services

### Product Service
The ProductService handles all product and material-related operations:

```python
from src.core.services import ProductService

# Get products by category
products = ProductService.get_products(
    db,
    category="Level Switch"
)

# Configure product with specific material
product, price = ProductService.configure_product(
    db,
    product_id=1,
    length=24.0,
    material_override="S"
)

# Get available materials for product
materials = ProductService.get_available_materials_for_product(
    db,
    "LS2000"
)
```

### Quote Service
The QuoteService manages quote creation and pricing:

```python
from src.core.services import QuoteService

# Create new quote
quote = QuoteService.create_quote(
    db,
    customer_id=1,
    expiration_days=30
)

# Add product to quote
item = QuoteService.add_product_to_quote(
    db,
    quote_id=quote.id,
    product_id=1,
    quantity=2
)
```

## Database Operations

### Working with Migrations
1. Create new migration:
   ```sh
   alembic revision --autogenerate -m "Description of changes"
   ```

2. Apply migrations:
   ```sh
   alembic upgrade head
   ```

3. Rollback migration:
   ```sh
   alembic downgrade -1
   ```

### Database Utilities
- Reset database: `python scripts/reset_db.py`
- Verify database: `python scripts/test_db.py`
- Query database: `python scripts/query_db.py`

## Testing Guidelines

### Running Tests
```sh
# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/ui/

# Run with coverage
pytest --cov=src tests/
```

### Writing Tests
1. Place tests in appropriate directory:
   - Unit tests: `tests/unit/`
   - Integration tests: `tests/integration/`
   - UI tests: `tests/ui/`

2. Follow test naming convention:
   - `test_<component>_<functionality>.py`
   - Example: `test_product_service_pricing.py`

3. Use fixtures for common setup:
   ```python
   @pytest.fixture
   def sample_product(db_session):
       return ProductService.create_product(
           db_session,
           name="Test Product",
           category="Level Switch"
       )
   ```

## UI Development

### Adding New UI Components
1. Create component in `src/ui/components/`
2. Use PySide6 conventions:
   ```python
   from PySide6.QtWidgets import QWidget
   
   class MyComponent(QWidget):
       def __init__(self, parent=None):
           super().__init__(parent)
           self.setup_ui()
   
       def setup_ui(self):
           # UI setup code here
           pass
   ```

### UI Best Practices
1. Keep UI logic separate from business logic
2. Use signals/slots for communication
3. Implement proper error handling
4. Add loading indicators for long operations
5. Follow accessibility guidelines

## Best Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write descriptive docstrings
- Keep functions focused and small

### Version Control
- Create feature branches for new work
- Write clear commit messages
- Review code before committing
- Keep commits focused and atomic

### Error Handling
- Use appropriate exception types
- Add proper error messages
- Log errors with context
- Handle edge cases

### Documentation
- Update docstrings for new code
- Keep README.md current
- Document complex algorithms
- Add examples for new features

## Troubleshooting

### Common Issues
1. Database connection errors:
   - Check database file exists
   - Verify permissions
   - Reset database if needed

2. UI not updating:
   - Check signal connections
   - Verify data binding
   - Clear UI cache

3. Pricing calculation issues:
   - Verify material rules
   - Check length calculations
   - Validate product configuration

### Getting Help
- Check project documentation
- Review test cases
- Search issue tracker
- Contact project maintainers

## Related Documentation
- [README.md](../README.md): Project overview
- [ACTION_PLAN.md](../ACTION_PLAN.md): Project roadmap
- [project_notes.md](../project_notes.md): Design notes 