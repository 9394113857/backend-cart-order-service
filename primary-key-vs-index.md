
---

## 💥 Real-world impact example 

❌ Without Index:
- 1 million rows → check all rows → slow (seconds/minutes)

✔ With Index:
- Direct jump to matching rows → fast (milliseconds)

---

## 🧾 Interview line
Index is used to improve query performance by allowing fast retrieval of rows instead of scanning the entire table. It is used on frequently searched columns.

---

---

# 🔥 PRIMARY KEY vs INDEX (DIFFERENCE)

| Feature | Primary Key | Index |
|----------|------------|-------|
| Purpose | Identity | Speed |
| Uniqueness | Yes | No |
| NULL allowed | No | Yes |
| Count per table | 1 | Many |
| Auto-created | Yes (unique index) | No |
| Main goal | Data integrity | Query performance |

---

---

# ⚡ REAL WORLD HOW BOTH WORK TOGETHER

## Example system: E-commerce orders

```sql
orders
-------
order_id (PK)
customer_id (INDEX)
status (INDEX)
created_at
