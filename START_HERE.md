# Onboarding Checklist

Welcome to the MyBabbittQuote project! This guide will help you get started quickly.

## Quick Start

1. **Read the Documentation**
   - [README.md](./README.md) - Project overview and setup instructions
   - [ACTION_PLAN.md](./ACTION_PLAN.md) - Current 2-day completion plan
   - [Code_Review.md](./Code_Review.md) - Code review guidelines

2. **Environment Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## Project Timeline

The project is currently in a 2-day sprint to completion. Please refer to [ACTION_PLAN.md](./ACTION_PLAN.md) for detailed tasks and timeline.

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Write comprehensive tests
   - Document all public APIs

2. **Git Workflow**
   - Create feature branches
   - Write descriptive commit messages
   - Keep commits focused and atomic
   - Update documentation with changes

3. **Testing**
   - Run tests before committing
   - Maintain test coverage
   - Document test cases
   - Use pytest for testing

## Important Notes

- The `legacy/` directory contains archived code for reference only
- All new development should be in the `src/` directory
- Keep documentation up-to-date with changes
- Report issues immediately

## Getting Help

If you have questions:
1. Check the documentation first
2. Review the code review guidelines
3. Ask the project lead
4. Document any new questions in project_notes.md

## For Cursor AI

When starting a new Cursor session, run:
> Please read START_HERE.md, README.md, and ACTION_PLAN.md in order. Confirm understanding of the project state and current sprint goals. 