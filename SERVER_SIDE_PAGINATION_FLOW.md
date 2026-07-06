# Server-Side Pagination Flow

## Overview

This project uses **server-side pagination**.

The Angular frontend **does not fetch all records** from the database. Instead, it requests only the records required for the current page.

The flow is:

```
User
   │
   ▼
Angular UI
   │
   ▼
HTTP Request
   │
   ▼
Flask Order Microservice
   │
   ▼
SQLAlchemy ORM
   │
   ▼
Supabase PostgreSQL
   │
   ▼
Database Rows
   │
   ▼
JSON Response
   │
   ▼
Angular Updates Table
```

---

# Angular Frontend

The Angular service sends the page number and page size to the backend.

```typescript
getMyOrders(
    page: number = 1,
    size: number = 10,
    status: string = '',
    orderId: string = ''
)
```

If no parameters are supplied:

```typescript
this.orderService.getMyOrders();
```

Angular sends

```
GET /api/orders?page=1&size=10
```

Meaning:

- Page = 1
- Records per page = 10

---

# Flask Route

The request reaches the Order Microservice.

```python
@orders_bp.get("/")
def get_orders():
```

which calls

```python
OrderService.get_orders(user_id)
```

---

# Reading Query Parameters

Flask reads the pagination values.

```python
page = request.args.get(
    "page",
    1,
    type=int
)

size = request.args.get(
    "size",
    10,
    type=int
)
```

Example:

```
GET /api/orders?page=3&size=10
```

Results in

```
page = 3
size = 10
```

---

# SQLAlchemy Pagination

The query is written as

```python
pagination = query.order_by(
    Order.created_at.desc()
).paginate(
    page=page,
    per_page=size,
    error_out=False
)
```

Notice that we never manually write SQL.

SQLAlchemy automatically generates SQL similar to:

```sql
SELECT *
FROM orders
WHERE user_id = ?
ORDER BY created_at DESC
LIMIT 10
OFFSET 20;
```

---

# Pagination Formula

SQLAlchemy internally calculates

```
OFFSET = (Page Number - 1) × Page Size
```

Examples:

| Page | Size | OFFSET |
|------|------|--------|
| 1 | 10 | 0 |
| 2 | 10 | 10 |
| 3 | 10 | 20 |
| 4 | 10 | 30 |
| 5 | 10 | 40 |

---

# SQL Generated for Each Button

## First Button

Angular sends

```
GET /api/orders?page=1&size=10
```

Equivalent SQL

```sql
SELECT *
FROM orders
WHERE user_id = ?
ORDER BY created_at DESC
LIMIT 10
OFFSET 0;
```

Returns

```
Rows 1–10
```

---

## Next Button

Current page = 1

Angular sends

```
GET /api/orders?page=2&size=10
```

SQL

```sql
SELECT *
FROM orders
WHERE user_id = ?
ORDER BY created_at DESC
LIMIT 10
OFFSET 10;
```

Returns

```
Rows 11–20
```

Click Next again

```
GET /api/orders?page=3&size=10
```

SQL

```sql
LIMIT 10
OFFSET 20;
```

Returns

```
Rows 21–30
```

---

## Previous Button

Current page = 3

Angular sends

```
GET /api/orders?page=2&size=10
```

SQL

```sql
LIMIT 10
OFFSET 10;
```

Returns

```
Rows 11–20
```

---

## Last Button

Suppose

```
Total Records = 87
Page Size = 10
```

Backend calculates

```
Total Pages = CEILING(87 / 10)

= 9
```

Angular sends

```
GET /api/orders?page=9&size=10
```

SQL

```sql
SELECT *
FROM orders
WHERE user_id = ?
ORDER BY created_at DESC
LIMIT 10
OFFSET 80;
```

Returns

```
Rows 81–87
```

Only seven rows are returned because no more records exist.

---

# Runtime Flow

## First

```
User Clicks First
        │
        ▼
Angular
page = 1
        │
        ▼
HTTP Request
        │
        ▼
Flask
        │
        ▼
SQLAlchemy
        │
        ▼
LIMIT 10 OFFSET 0
        │
        ▼
Supabase PostgreSQL
        │
        ▼
Rows 1–10
        │
        ▼
JSON Response
        │
        ▼
Angular Updates UI
```

---

## Next

```
User Clicks Next
        │
        ▼
page++
        │
        ▼
Angular
        │
        ▼
GET /api/orders?page=2&size=10
        │
        ▼
SQLAlchemy
        │
        ▼
LIMIT 10 OFFSET 10
        │
        ▼
Supabase
        │
        ▼
Rows 11–20
        │
        ▼
Angular Updates Table
```

---

## Previous

```
User Clicks Previous
        │
        ▼
page--
        │
        ▼
Angular
        │
        ▼
GET /api/orders?page=2&size=10
        │
        ▼
SQLAlchemy
        │
        ▼
LIMIT 10 OFFSET 10
        │
        ▼
Supabase
        │
        ▼
Rows 11–20
```

---

## Last

```
User Clicks Last
        │
        ▼
page = total_pages
        │
        ▼
Angular
        │
        ▼
GET /api/orders?page=9&size=10
        │
        ▼
SQLAlchemy
        │
        ▼
LIMIT 10 OFFSET 80
        │
        ▼
Supabase
        │
        ▼
Rows 81–87
```

---

# Pagination Metadata

The backend returns pagination information.

```json
{
    "pagination": {
        "page": 2,
        "size": 10,
        "total_records": 97,
        "total_pages": 10,
        "has_next": true,
        "has_prev": true
    }
}
```

Angular uses this metadata to:

- Enable or disable Next button
- Enable or disable Previous button
- Navigate to First page
- Navigate to Last page
- Display current page
- Display total pages

---

# What Happens on Every Button Click?

Every click sends a **new HTTP request**.

Examples:

```
Next
Previous
First
Last
Page Number
Search
Filter
Sorting
```

Every action causes:

```
Angular
      │
      ▼
HTTP Request
      │
      ▼
Flask Order Service
      │
      ▼
SQLAlchemy
      │
      ▼
Generates SQL
      │
      ▼
Supabase PostgreSQL
      │
      ▼
Returns Required Rows
      │
      ▼
JSON Response
      │
      ▼
Angular Refreshes Table
```

---

# Dynamic SQL Examples

Page 1

```sql
LIMIT 10 OFFSET 0;
```

Page 2

```sql
LIMIT 10 OFFSET 10;
```

Page 3

```sql
LIMIT 10 OFFSET 20;
```

Search

```sql
SELECT *
FROM orders
WHERE status='PLACED'
ORDER BY created_at DESC
LIMIT 10
OFFSET 0;
```

Filter

```sql
SELECT *
FROM orders
WHERE order_id = 125
ORDER BY created_at DESC
LIMIT 10
OFFSET 0;
```

Sorting

```sql
SELECT *
FROM orders
ORDER BY total_amount DESC
LIMIT 10
OFFSET 20;
```

The SQL changes dynamically based on the user's actions.

---

# Key Points

- Uses **server-side pagination**.
- Angular never connects directly to Supabase.
- Angular only sends page number, page size, filters, and sorting parameters.
- Flask reads query parameters.
- SQLAlchemy generates the SQL dynamically.
- Supabase PostgreSQL executes the SQL.
- Only the required rows are returned.
- Backend converts rows into JSON.
- Angular updates the table.
- Every user interaction (Next, Previous, First, Last, Search, Filter, Sort) results in a new SQL query being generated and executed.

---

# Complete Production Architecture

```
                    USER
                      │
                      ▼
            Angular Frontend
                      │
                      ▼
          HTTP GET /api/orders
                      │
                      ▼
      Flask Order Microservice
                      │
                      ▼
         Read page & size values
                      │
                      ▼
          SQLAlchemy paginate()
                      │
                      ▼
 Generates SQL (LIMIT + OFFSET)
                      │
                      ▼
        Supabase PostgreSQL
                      │
                      ▼
      Executes SQL & Returns Rows
                      │
                      ▼
      Flask Converts Rows to JSON
                      │
                      ▼
      Angular Receives JSON Response
                      │
                      ▼
         Orders Table Refreshes
```

---

# Conclusion

This implementation follows the standard **server-side pagination** pattern used in production applications.

Every navigation action (First, Next, Previous, Last, Search, Filter, Sort, or Page Number selection) triggers a new API request. The Flask microservice reads the pagination parameters, SQLAlchemy generates the appropriate SQL using `LIMIT` and `OFFSET`, Supabase PostgreSQL executes the query, and only the required records are returned to the Angular frontend. This approach is efficient, scalable, and avoids loading unnecessary data into memory.
