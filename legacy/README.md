# Babbitt Quote Generator

A modern, desktop-based Configure, Price, Quote (CPQ) application for Babbitt International's industrial products. This application is built with Python, using PySide6 for the user interface and SQLAlchemy for the database backend. It provides a rich, user-friendly interface for configuring complex products, managing customers, creating quotes, and exporting documents.

## Project Status (As of last update)

**Complete & Functional:**
-   **Core Application:** Main window with a modern sidebar navigation and theme support.
-   **Database:** SQLAlchemy models with Alembic for migrations.
-   **Product Service:** Fetches product families, variants, and all options from the database.
-   **Configuration Service:** Manages the state of a product being configured.
-   **Quote Service:** Core logic for creating quotes and handling dashboard statistics.
-   **UI - Product Selection:** Comprehensive dialog for selecting and configuring products with real-time price updates.
-   **UI - Customer Management:** Dedicated page for viewing and managing customers.
-   **UI - Dashboard:** Displays key business metrics like total quotes, quote value, and customer counts.
-   **UI - Quote Management:** Full quote creation, editing, and line item management.
-   **UI - Settings:** Application settings page with theme customization.
-   **UI - User Profile:** Basic user profile management.
-   **UI - Spare Parts:** Dedicated spare parts management interface.
-   **UI - Specifications:** Detailed product specifications management.
-   **Export:** Basic PDF and Word export functionality.

**In Development / To-Do:**
-   **Advanced Analytics:** Building out the "Analytics" and "Reports" sections of the dashboard.
-   **Full User Authentication:** Implementing comprehensive user roles and permissions.
-   **Export Templates:** Advanced formatting and template customization for exports.
-   **Performance Optimization:** Improving load times for large product catalogs.
-   **Integration Testing:** Expanding test coverage for critical workflows.
-   **Documentation:** Comprehensive user and developer documentation.

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
-   **Modern UI:** A responsive and intuitive user interface built with PySide6, featuring a sidebar navigation, theme support, and tab-based content area.
-   **Dynamic Product Configuration:** Select a product and configure it in real-time with options, pricing, and availability updates.
-   **Guided Selling:** The configuration dialog guides users through required choices and additional options.
-   **Quote Creation & Management:** Full quote lifecycle management including creation, editing, and line item management.
-   **Customer Dashboard:** At-a-glance dashboard showing total quotes, total value, number of customers, and number of products quoted.
-   **Customer Management:** Dedicated page to view and manage the customer list.
-   **Spare Parts Management:** Comprehensive interface for managing spare parts and accessories.
-   **Product Specifications:** Detailed management of product specifications and technical details.
-   **Settings & Customization:** Application settings with theme support and user preferences.
-   **Data Export:** Export quotes to PDF or Word format.
-   **User Profiles:** Basic user profile management functionality.

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
    The application will create the SQLite database on first run. To apply schema changes run Alembic migrations, then seed core option data:
    ```sh
    alembic upgrade head
    python scripts/seed_options.py
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
