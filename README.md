# MyBabbittQuote Generator

A professional quote generation system built with Python and PySide6, designed to streamline the process of creating and managing Babbitt-related quotes.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-blueviolet)](https://www.python.org/dev/peps/pep-0008/)

## 🚀 Features

- **Modern GUI Interface**
  - Responsive design built with PySide6
  - Dark/Light theme support
  - Customizable layouts
  - Real-time quote preview

- **Quote Management**
  - Database-driven storage
  - Advanced search and filtering
  - Quote history tracking
  - Bulk operations support

- **Export Capabilities**
  - PDF export with custom templates
  - DOCX export with formatting
  - Batch export functionality
  - Custom export templates

- **Security & Performance**
  - Secure credential management
  - Input validation
  - Error handling and logging
  - Performance optimizations

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- SQLite3 (included with Python)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd mybabbittquote
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

## ⚙️ Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DB_PATH=path/to/database
LOG_LEVEL=INFO
THEME=dark
```

## 🏃‍♂️ Running the Application

1. Activate the virtual environment (if not already activated)
2. Run the main application:
```bash
python main.py
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_quote_generator.py

# Run with coverage report
pytest --cov=src tests/
```

## 📁 Project Structure

```
mybabbittquote/
├── src/                    # Source code
│   ├── core/              # Core business logic
│   │   ├── models/        # Data models
│   │   ├── services/      # Business services
│   │   └── config/        # Configuration
│   ├── ui/                # User interface components
│   │   ├── views/         # UI views
│   │   ├── widgets/       # Custom widgets
│   │   └── dialogs/       # Dialog windows
│   ├── utils/             # Utility functions
│   │   ├── validators/    # Input validation
│   │   └── helpers/       # Helper functions
│   └── export/            # Export functionality
│       ├── pdf/           # PDF export
│       └── docx/          # DOCX export
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docs/                  # Documentation
├── migrations/            # Database migrations
└── data/                  # Data files and templates
    ├── templates/        # Export templates
    └── config/          # Configuration files
```

## 🔧 Development

### Code Style
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Keep functions small and focused (max 50 lines)
- Use meaningful variable and function names
- Add docstrings for all public functions and classes

### Testing
- Write unit tests for all new features
- Maintain minimum 80% code coverage
- Run tests before committing changes
- Use pytest fixtures for test setup

### Git Workflow
1. Create feature branch from `main`
2. Make changes and commit with descriptive messages
3. Run tests and linting
4. Create pull request with detailed description
5. Address review comments
6. Merge after approval

### Documentation
- Update README.md for new features
- Add docstrings for new functions
- Update API documentation
- Include usage examples

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check database path in `.env`
   - Verify SQLite installation
   - Check file permissions

2. **Export Failures**
   - Verify template files exist
   - Check file permissions
   - Ensure required fonts are installed

3. **UI Rendering Issues**
   - Clear cache directory
   - Update PySide6
   - Check theme configuration

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🆘 Support

For support:
- Open an issue in the GitHub repository
- Contact the development team at [support@mybabbittquote.com]
- Check the [documentation](docs/) for detailed guides

## 📚 Additional Resources

- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [Changelog](CHANGELOG.md) 