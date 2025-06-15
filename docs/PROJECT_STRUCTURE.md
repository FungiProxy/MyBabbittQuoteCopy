# Project Structure

This document outlines the organization of the MyBabbittQuote project.

## Directory Structure

```
mybabbittquote/
├── src/                      # Source code
│   ├── core/                # Core domain models and business logic
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic services
│   │   └── config/         # Core configuration
│   ├── api/                # API endpoints and routes
│   ├── ui/                 # UI components and views
│   │   ├── components/     # Reusable UI components
│   │   ├── views/         # Main view screens
│   │   └── dialogs/       # Dialog windows
│   ├── utils/              # Utility functions
│   └── export/             # Export functionality
├── scripts/                 # Scripts and tools
│   ├── data/               # Data management scripts
│   │   ├── config/        # Configuration data
│   │   ├── seeds/         # Seed data
│   │   └── init/          # Initialization scripts
│   └── tools/             # Development and maintenance tools
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test fixtures
├── docs/                   # Documentation
├── migrations/             # Database migrations
└── config/                 # Application configuration
    ├── development/       # Development configs
    ├── production/        # Production configs
    └── testing/          # Testing configs
```

## Key Components

### Core (`src/core/`)
- Contains the core business logic and domain models
- Models represent database tables and business entities
- Services implement business rules and operations
- Configuration contains core application settings

### UI (`src/ui/`)
- Components: Reusable UI elements
- Views: Main application screens
- Dialogs: Modal windows and popups

### API (`src/api/`)
- API endpoints and routes
- Request/response handlers
- API documentation

### Utils (`src/utils/`)
- Helper functions
- Common utilities
- Shared functionality

### Export (`src/export/`)
- Export functionality
- File format handlers
- Export templates

### Scripts (`scripts/`)
- Data management scripts
- Development tools
- Maintenance utilities

### Tests (`tests/`)
- Unit tests for individual components
- Integration tests for system interactions
- Test fixtures and utilities

### Config (`config/`)
- Environment-specific configurations
- Development settings
- Production settings
- Testing configurations

## Best Practices

1. **Module Organization**
   - Keep related functionality together
   - Use clear, descriptive names
   - Follow Python package conventions

2. **Code Structure**
   - One class per file
   - Clear separation of concerns
   - Consistent naming conventions

3. **Documentation**
   - Keep documentation up to date
   - Include docstrings for all modules
   - Document complex logic

4. **Testing**
   - Write tests for new features
   - Maintain test coverage
   - Use appropriate test types

5. **Configuration**
   - Use environment-specific configs
   - Keep sensitive data secure
   - Document configuration options

## Development Workflow

1. **Setup**
   ```bash
   # Create virtual environment
   python -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   .\myenv\Scripts\activate   # Windows

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

2. **Running Tests**
   ```bash
   # Run all tests
   pytest

   # Run specific test file
   pytest tests/unit/test_specific.py

   # Run with coverage
   pytest --cov=src tests/
   ```

3. **Database Management**
   ```bash
   # Initialize database
   python scripts/data/init/init_business_config.py
   python scripts/data/init/init_sample_data.py

   # Run migrations
   alembic upgrade head
   ```

4. **Development**
   - Follow PEP 8 style guide
   - Write tests for new features
   - Update documentation
   - Use type hints
   - Run linters before committing

## Configuration Management

1. **Environment Variables**
   - Use `.env` files for local development
   - Never commit sensitive data
   - Document all required variables

2. **Configuration Files**
   - Keep in `config/` directory
   - Use environment-specific files
   - Document all settings

## Deployment

1. **Production Setup**
   - Use production configuration
   - Set up proper logging
   - Configure security settings

2. **Monitoring**
   - Set up error tracking
   - Monitor performance
   - Track usage metrics

## Contributing

1. **Code Style**
   - Follow PEP 8
   - Use type hints
   - Write docstrings

2. **Git Workflow**
   - Create feature branches
   - Write descriptive commits
   - Submit PRs for review

3. **Review Process**
   - Code review required
   - Tests must pass
   - Documentation updated