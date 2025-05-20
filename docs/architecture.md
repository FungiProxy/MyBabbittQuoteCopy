# MyBabbittQuote Architecture Overview

This document provides a comprehensive overview of the MyBabbittQuote system architecture, including component relationships, data flow, and key design decisions.

## System Architecture

```mermaid
graph TB
    subgraph UI["User Interface Layer"]
        MainWindow["MainWindow"]
        ProductTab["ProductTab"]
        SpecTab["SpecificationsTab"]
        QuoteTab["QuoteTab"]
        SparePartsTab["SparePartsTab"]
    end

    subgraph Services["Service Layer"]
        PS["ProductService"]
        QS["QuoteService"]
        CS["CustomerService"]
        SPS["SparePartService"]
    end

    subgraph Core["Core Business Logic"]
        Models["Domain Models"]
        Pricing["Pricing Engine"]
        Validation["Validation Rules"]
    end

    subgraph Data["Data Layer"]
        DB["SQLite Database"]
        Migration["Alembic Migrations"]
        Utils["Database Utilities"]
    end

    UI --> Services
    Services --> Core
    Core --> Data
```

## Component Details

### UI Layer Components
```mermaid
classDiagram
    class MainWindow {
        +setup_ui()
        +init_tabs()
        +handle_events()
    }
    class ProductTab {
        +load_products()
        +filter_products()
        +select_product()
    }
    class SpecificationsTab {
        +load_options()
        +configure_product()
        +validate_inputs()
    }
    class QuoteTab {
        +create_quote()
        +add_items()
        +calculate_total()
    }
    class SparePartsTab {
        +load_spare_parts()
        +filter_parts()
        +add_to_quote()
    }

    MainWindow --> ProductTab
    MainWindow --> SpecificationsTab
    MainWindow --> QuoteTab
    MainWindow --> SparePartsTab
```

### Service Layer
```mermaid
classDiagram
    class ProductService {
        +get_products()
        +configure_product()
        +get_available_materials()
        +get_product_options()
    }
    class QuoteService {
        +create_quote()
        +add_product_to_quote()
        +calculate_total()
        +update_quote_status()
    }
    class CustomerService {
        +create_customer()
        +update_customer()
        +search_customers()
        +get_customer()
    }
    class SparePartService {
        +get_spare_parts()
        +get_by_product_family()
        +get_categories()
    }

    ProductService --> "1" PricingEngine
    QuoteService --> "1" ProductService
    QuoteService --> "1" CustomerService
    SparePartService --> "1" ProductService
```

### Data Models
```mermaid
erDiagram
    Product ||--o{ ProductVariant : "has"
    Product ||--o{ Option : "has"
    Product ||--o{ Material : "uses"
    Quote ||--o{ QuoteItem : "contains"
    QuoteItem ||--o{ QuoteItemOption : "has"
    Customer ||--o{ Quote : "places"
    ProductVariant ||--o{ SparePart : "has"
```

## Key Design Patterns

### Repository Pattern
```mermaid
graph LR
    Service["Service Layer"] --> Repository["Repository Pattern"]
    Repository --> Database["Database"]
    Repository --> Cache["Cache Layer"]
```

### Domain-Driven Design
```mermaid
graph TB
    subgraph Domain["Domain Layer"]
        Models["Domain Models"]
        Rules["Business Rules"]
        Services["Domain Services"]
    end

    subgraph Application["Application Layer"]
        AppServices["Application Services"]
        DTOs["Data Transfer Objects"]
    end

    subgraph Infrastructure["Infrastructure Layer"]
        Repos["Repositories"]
        DB["Database"]
        External["External Services"]
    end

    Application --> Domain
    Infrastructure --> Domain
```

## Data Flow

### Quote Creation Flow
```mermaid
sequenceDiagram
    participant UI as UI
    participant QS as QuoteService
    participant PS as ProductService
    participant DB as Database

    UI->>QS: create_quote(customer_id)
    QS->>DB: begin_transaction()
    QS->>DB: create_quote_record()
    UI->>QS: add_product(quote_id, product_id)
    QS->>PS: configure_product(product_id)
    PS->>DB: get_product_data()
    PS-->>QS: return configured_product
    QS->>DB: add_quote_item()
    DB-->>QS: commit_transaction()
    QS-->>UI: return updated_quote
```

### Product Configuration Flow
```mermaid
sequenceDiagram
    participant UI as UI
    participant PS as ProductService
    participant PE as PricingEngine
    participant DB as Database

    UI->>PS: configure_product(product_id, specs)
    PS->>DB: get_product_data()
    PS->>PS: validate_configuration()
    PS->>PE: calculate_price()
    PE->>DB: get_pricing_rules()
    PE-->>PS: return price
    PS-->>UI: return configured_product
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Client["Client Machine"]
        App["Desktop Application"]
        LocalDB["SQLite Database"]
        Cache["Local Cache"]
    end

    subgraph Updates["Update System"]
        Version["Version Check"]
        Download["Update Download"]
    end

    App --> LocalDB
    App --> Cache
    App --> Version
    Version --> Download
```

## Security Architecture

```mermaid
graph TB
    subgraph Security["Security Layer"]
        Auth["Authentication"]
        Access["Access Control"]
        Audit["Audit Logging"]
    end

    subgraph Data["Data Security"]
        Encrypt["Encryption"]
        Backup["Backup"]
        Validate["Input Validation"]
    end

    Security --> Data
```

## Notes and Considerations

### Performance Optimizations
- Database indexing on frequently queried fields
- Caching of product and pricing data
- Lazy loading of UI components
- Batch processing for bulk operations

### Scalability
- Modular design allows for easy addition of new features
- Service layer can be extended for new business rules
- Database schema supports future product types
- UI components are reusable and extensible

### Maintenance
- Clear separation of concerns
- Comprehensive logging
- Error handling at all layers
- Automated testing coverage

## Related Documentation
- [Developer Guide](./developer_guide.md)
- [Database Schema](./database_schema.md)
- [API Documentation](./api_docs.md)
- [Testing Strategy](./testing_strategy.md) 