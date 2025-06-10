# Babbitt Quote Generator

A modern, desktop-based Configure, Price, Quote (CPQ) application for Babbitt International's industrial products. This application is built with Python, using PySide6 for the user interface and SQLAlchemy for the database backend. It provides a rich, user-friendly interface for configuring complex products, managing customers, creating quotes, and exporting documents.

## Project Status (As of last update)

**Complete & Functional:**
-   **Core Application:** Main window with a modern sidebar navigation.
-   **Database:** SQLAlchemy models with Alembic for migrations.
-   **Product Service:** Fetches product families, variants, and all options from the database.
-   **Configuration Service:** Manages the state of a product being configured.
-   **Quote Service:** Core logic for creating quotes and handling dashboard statistics.
-   **UI - Product Selection:** A comprehensive dialog for selecting and configuring products with real-time price updates.
-   **UI - Customer Management:** A dedicated page for viewing and managing customers.
-   **UI - Dashboard:** Displays key business metrics like total quotes, quote value, and customer counts.

**In Development / To-Do:**
-   **Quote Editing:** Editing an existing quote and its line items.
-   **PDF/Data Export:** Finalizing the export templates and logic.
-   **Full User Authentication:** Implementing user roles and permissions.
-   **Advanced Analytics:** Building out the "Analytics" and "Reports" sections of the dashboard.
-   **Settings Page:** Implementing application-level settings.

---

## Table of Contents
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Testing](#testing)

---

## Features
-   **Modern UI:** A responsive and intuitive user interface built with PySide6, featuring a sidebar navigation and a tab-based content area.
-   **Dynamic Product Configuration:** Select a product and configure it in real-time. Options, pricing, and availability are dynamically updated.
-   **Guided Selling:** The configuration dialog guides the user through required choices like voltage, material, and probe length, plus additional options categorized for clarity.
-   **Quote Creation & Management:** Add configured products to a quote, manage quantities, and see a running total. View existing quotes.
-   **Customer Dashboard:** An at-a-glance dashboard showing total quotes, total value, number of customers, and number of products quoted.
-   **Customer Management:** A dedicated page to view and manage the customer list.
-   **Data Export:** Functionality to export quotes to various formats (implementation in progress).

## Directory Structure
```
/
├── src/                # Main application source code
│   ├── core/           # Business logic, models, services
│   │   ├── models/     # SQLAlchemy ORM models
│   │   ├── services/   # Business logic services (Product, Quote, etc.)
│   │   └── pricing/    # Pricing calculation modules
│   ├── ui/             # User interface (PySide6 widgets and dialogs)
│   ├── export/         # Logic for exporting data (e.g., to PDF)
│   └── utils/          # Shared utility functions
├── data/               # Data files (e.g., database file, seed data)
├── migrations/         # Alembic database migrations
├── tests/              # Unit and integration tests
├── main.py             # Application entry point
├── requirements.txt    # Python runtime dependencies
├── README.md           # This file
└── ... (Configuration files like alembic.ini, pytest.ini)
```

## Prerequisites
-   Python 3.9 or higher
-   Pip (Python package installer)

## Setup & Installation
1.  **Clone the repository:**
    ```sh
    git clone <repo-url>
    cd <repo-directory>
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```sh
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Initialize and seed the database:**
    The application is designed to create and seed the database on first run if it doesn't exist. Run the `seed_database.py` script if you need to reset the data.
    ```sh
    python scripts/seed_database.py
    ```

## Usage

To start the application, run the `main.py` script from the root of the project:
```sh
python main.py
```

## Testing
To run the test suite, use `pytest`. For development, you may want to install development dependencies.
```sh
# It is recommended to install development dependencies first
pip install -r requirements-dev.txt

# Run all tests
pytest
```
