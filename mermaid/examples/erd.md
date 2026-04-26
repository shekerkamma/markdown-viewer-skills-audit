# Mermaid Example — Entity-Relationship Diagram

E-commerce schema with customers, orders, line items, and products. Shows cardinality notation, attribute types, primary/foreign keys, and notes.

## Source

````markdown
```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  CUSTOMER {
    uuid id PK
    string email UK
    string name
    timestamp created_at
  }

  ORDER ||--|{ LINE_ITEM : contains
  ORDER {
    uuid id PK
    uuid customer_id FK
    string status "pending|paid|shipped|cancelled"
    decimal total_cents
    timestamp placed_at
  }

  LINE_ITEM }o--|| PRODUCT : refers_to
  LINE_ITEM {
    uuid id PK
    uuid order_id FK
    uuid product_id FK
    int quantity
    decimal unit_price_cents
  }

  PRODUCT ||--o{ INVENTORY : tracked_in
  PRODUCT {
    uuid id PK
    string sku UK
    string name
    decimal price_cents
    boolean active
  }

  INVENTORY {
    uuid product_id FK
    string warehouse
    int on_hand
    int reserved
  }
```
````

## Rendered

```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  CUSTOMER {
    uuid id PK
    string email UK
    string name
    timestamp created_at
  }

  ORDER ||--|{ LINE_ITEM : contains
  ORDER {
    uuid id PK
    uuid customer_id FK
    string status "pending|paid|shipped|cancelled"
    decimal total_cents
    timestamp placed_at
  }

  LINE_ITEM }o--|| PRODUCT : refers_to
  LINE_ITEM {
    uuid id PK
    uuid order_id FK
    uuid product_id FK
    int quantity
    decimal unit_price_cents
  }

  PRODUCT ||--o{ INVENTORY : tracked_in
  PRODUCT {
    uuid id PK
    string sku UK
    string name
    decimal price_cents
    boolean active
  }

  INVENTORY {
    uuid product_id FK
    string warehouse
    int on_hand
    int reserved
  }
```

## Cardinality notation

Both ends of every relationship line carry a marker:

| Left side | Right side | Meaning |
|---|---|---|
| `\|\|` | `\|\|` | Exactly one — one |
| `\|\|` | `o{` | Exactly one — zero or many |
| `\|\|` | `\|{` | Exactly one — one or many |
| `}o` | `o\|` | Zero or many — zero or one |
| `}\|` | `\|{` | One or many — one or many |

Read it like English: `CUSTOMER ||--o{ ORDER : places` = "one customer places zero or many orders".

## Attribute keys

| Marker | Meaning |
|---|---|
| `PK` | Primary key |
| `FK` | Foreign key |
| `UK` | Unique key |
| `"text"` | Inline comment / enum hint |

ER diagrams in Mermaid are layout-only — they don't validate referential integrity. For schema-as-code with constraints, prefer DBML or actual migration files; use Mermaid for documentation/communication.
