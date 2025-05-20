# MyBabbittQuote

A modern, domain-driven quote generator for Babbitt International products. This application provides a user-friendly interface for configuring, pricing, and quoting complex industrial products, with robust business logic and export capabilities.

## Features
- **Product Configuration**
  - Intuitive tabbed interface for product selection and configuration
  - Dynamic options based on product family and compatibility rules
  - Support for standard and non-standard lengths
  - Material selection (S, H, U, T materials) with pricing rules
  - Specialized customer-specific product offerings
  
- **Pricing Engine**
  - Material-specific pricing calculations
  - Length-based pricing with non-standard surcharges
  - Option compatibility validation
  - Customer-specific pricing rules
  - Automatic price updates based on configurations

- **Quote Management**
  - Save and load quote configurations
  - PDF export capabilities (in development)
  - Quote history tracking
  - Spare parts management

- **Business Logic**
  - Robust validation rules
  - Complex pricing calculations
  - Product compatibility checks
  - Database-driven configuration

---

## Table of Contents
- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [Related Files](#related-files)
- [License](#license)

---

## Project Overview
- **Purpose:** Streamline the process of configuring, pricing, and quoting Babbitt International products.
- **Target Users:** Sales representatives, engineers, and product specialists
- **Key Benefits:**
  - Reduced quote generation time
  - Consistent pricing application
  - Error reduction in product configuration
  - Improved quote accuracy
  - Streamlined workflow

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)
- SQLite3 (included with Python)
- Windows 10/11 or compatible OS

## Directory Structure
```
MyBabbittQuote/
├── src/                # Main application source code
│   ├── core/          # Business logic, models, services
│   │   ├── models/    # SQLAlchemy models
│   │   └── services/  # Business logic services
│   ├── ui/            # User interface (PySide6)
│   ├── export/        # Export logic (PDF, etc.)
│   └── utils/         # Shared utilities
├── scripts/           # Automation and utility scripts
│   ├── data/         # Data processing scripts
│   └── test/         # Test automation scripts
├── tests/            # Unit and integration tests
├── data/             # Configuration and data files
├── migrations/       # Database migrations (Alembic)
├── myenv/           # Virtual environment (optional)
├── docs/            # Documentation (if present)
└── [Configuration Files]
    ├── ACTION_PLAN.md    # Project roadmap
    ├── project_notes.md  # Design notes
    ├── README.md         # This file
    ├── requirements.txt  # Python dependencies
    ├── setup.py         # Project setup
    └── main.py          # Application entry
```

## Setup & Installation
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd MyBabbittQuote
   ```

2. **Create and activate a virtual environment:**
   ```sh
   # Windows
   python -m venv myenv
   .\myenv\Scripts\activate

   # Linux/Mac
   python -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```sh
   # Create and migrate database
   python scripts/create_db.py

   # Verify database setup
   python scripts/test_db.py
   ```

5. **Verify installation:**
   ```sh
   # Run basic tests
   pytest tests/test_basic.py

   # Test database queries
   python scripts/query_db.py
   ```

## Usage

### Starting the Application
```sh
python main.py
```

### Basic Workflow
1. **Product Selection**
   - Choose product family
   - Select specific model
   - Configure materials and options

2. **Specifications**
   - Set dimensions and lengths
   - Choose connection types
   - Select housing options
   - Configure special requirements

3. **Quote Generation**
   - Review configuration
   - Calculate pricing
   - Generate quote summary
   - Export quote (PDF - coming soon)

### Advanced Features
- **Save/Load Quotes:**
  ```sh
  File -> Save Quote
  File -> Load Quote
  ```

- **Database Management:**
  ```sh
  # Update product catalog
  python scripts/update_catalog.py

  # Backup database
  python scripts/backup_db.py
  ```

- **Troubleshooting:**
  ```sh
  # Check system status
  python scripts/check_status.py

  # Verify pricing rules
  python scripts/test_pricing.py
  ```

## Testing
- **Run all tests:**
  ```sh
  pytest
  ```

- **Run specific test categories:**
  ```sh
  # Unit tests
  pytest tests/unit/

  # Integration tests
  pytest tests/integration/

  # UI tests
  pytest tests/ui/
  ```

- **Test coverage report:**
  ```sh
  pytest --cov=src tests/
  ```

## Contributing
1. **Read the Documentation:**
   - Start with `START_HERE.md`
   - Review `ACTION_PLAN.md`
   - Check `project_notes.md`

2. **Development Guidelines:**
   - Follow Python PEP 8 style guide
   - Write descriptive commit messages
   - Add tests for new features
   - Update documentation
   - Use type hints where possible

3. **Code Review Process:**
   - Create feature branch
   - Submit pull request
   - Address review comments
   - Update tests and documentation

## Troubleshooting
Common issues and solutions:

1. **Database Errors:**
   ```sh
   # Reset database
   python scripts/reset_db.py
   ```

2. **UI Issues:**
   - Clear cache: `File -> Clear Cache`
   - Reset preferences: `File -> Reset Preferences`

3. **Pricing Calculation Errors:**
   ```sh
   # Verify pricing rules
   python scripts/verify_pricing.py
   ```

## Related Files
- [`ACTION_PLAN.md`](./ACTION_PLAN.md): Project roadmap and priorities
- [`project_notes.md`](./project_notes.md): Design decisions and notes
- [`requirements.txt`](./requirements.txt): Python dependencies
- [`main.py`](./main.py): Application entry point

## Support
For issues and support:
1. Check the troubleshooting section
2. Review `project_notes.md`
3. Run diagnostic tools
4. Contact project maintainers

## License
This project is proprietary software for Babbitt International.
All rights reserved.

---

**Welcome! Start with `START_HERE.md` for onboarding.**
