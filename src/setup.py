from setuptools import find_packages, setup

setup(
    name="mybabbittquote",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.4.0",
        "SQLAlchemy>=2.0.0",
        "alembic>=1.15.0",
    ],
    python_requires=">=3.8",
)
