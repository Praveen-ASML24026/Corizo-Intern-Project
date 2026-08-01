# 📚 Library Management System

A terminal-based Python application for managing books, members, and borrowing transactions in a library. Built with custom Data Structure implementations (Linked List, Stack, Queue, HashMap, BST) and a MySQL backend.

---

## 📌 Overview

This system provides a complete library management workflow through a simple numbered menu. It handles book and member registration, borrow/return transactions with queue-based processing, an activity log, undo/redo support, and a borrowing report — all powered by hand-built DSA modules rather than standard library equivalents.

---

## ✨ Features

- **Book Management** — Add books and view the full catalogue with availability status
- **Member Management** — Register members and list them in a formatted table
- **Borrow & Return** — Queue-based borrow request processing with timestamp tracking
- **Activity Log** — Linked List (capped at 50 entries) tracks every action in the session
- **Undo / Redo** — Stack-based undo and redo for add-book and borrow operations
- **Reports** — Ranks books by borrow count descending
- **Pretty Tables** — All listings rendered with `prettytable` for clean terminal output

---

## 🧱 Data Structures Used

| DSA | Implementation | Used For |
|---|---|---|
| **HashMap** | Custom dict wrapper | In-memory book and member cache |
| **Linked List** | Singly linked, size-capped | Activity log (last 50 actions) |
| **Stack** | List-based LIFO | Undo and Redo operation history |
| **Queue** | List-based FIFO | Borrow request queue |
| **BST** | Binary Search Tree | Sorted data utility (available for search) |

---

## 🗂️ Project Structure

```
LibraryManagementSystem/
├── schema.sql                      # MySQL database schema
└── src/
    ├── main.py                     # Entry point and menu loop
    ├── services/
    │   ├── library_service.py      # Core business logic and DSA orchestration
    │   └── report_service.py       # Report utilities
    ├── database/
    │   ├── db_config.py            # MySQL connection config
    │   ├── book_dao.py             # Book CRUD operations
    │   ├── member_dao.py           # Member CRUD operations
    │   └── transaction_dao.py      # Transaction CRUD operations
    ├── models/
    │   ├── book.py                 # Book model
    │   ├── member.py               # Member model
    │   └── transaction.py          # Transaction model
    ├── dsa/
    │   ├── hash_map.py             # Custom HashMap
    │   ├── linked_list.py          # Custom Linked List
    │   ├── stack.py                # Custom Stack
    │   ├── queue.py                # Custom Queue
    │   └── bst.py                  # Custom Binary Search Tree
    └── utils/
        ├── validations.py          # Input validation helpers
        └── helpers.py              # General utility functions
```

---

## ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core language |
| MySQL | Persistent storage |
| mysql-connector-python | Database connectivity |
| prettytable | Formatted terminal table output |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL 8.x
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```

### Install Dependencies

```bash
pip install mysql-connector-python prettytable
```

### Database Setup

1. Open your MySQL client and run the schema:

```bash
mysql -u root -p < schema.sql
```

This creates the `library_db` database with `books`, `members`, and `transactions` tables.

2. Update the credentials in `src/database/db_config.py`:

```python
return mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="library_db"
)
```

### Run the Application

```bash
python -m src.main
```

---

## 🖥️ Menu Options

```
===== Library Management System =====
1.  Add Book
2.  Show All Books
3.  Add Member
4.  Show Members
5.  Borrow Book
6.  Return Book
7.  Show Activity Log
8.  Undo Last Action
9.  Redo Last Action
10. Reports
11. Exit
```

---

## 🔄 How It Works

### Borrowing Flow
When a borrow is requested, the `(book_id, member_id)` pair is **enqueued** into a `Queue`. The queue is immediately processed — availability is checked, the book is marked unavailable, and a transaction record is created with the current timestamp.

### Undo / Redo
Every write operation (`ADD_BOOK`, `BORROW`, `RETURN`) is **pushed onto the undo Stack**. Calling undo pops the last operation, reverses it, and pushes it onto the redo Stack. Redo reapplies the operation from the redo Stack.

### Activity Log
A **Linked List** (head-insert, capped at 50 nodes) records a human-readable description of every action. The log is viewable at any time from the menu.

### In-Memory Cache
Books and members are synced from MySQL into a **HashMap** on startup and after every write, enabling fast O(1) in-memory lookups alongside the persistent DB layer.

---

## 🗃️ Database Schema

```sql
CREATE TABLE books (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    title     VARCHAR(255),
    author    VARCHAR(255),
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE members (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE transactions (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    book_id     INT,
    member_id   INT,
    borrow_date DATETIME,
    return_date DATETIME,
    FOREIGN KEY (book_id)   REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);
```

---

## 🔮 Future Enhancements

- [ ] Search books by title or author (using BST)
- [ ] Due date tracking and overdue fine calculation
- [ ] Member borrowing history view
- [ ] Multi-copy support per book title
- [ ] GUI frontend (Tkinter or Flask)
- [ ] Export reports to CSV

---

## 📄 License

This project is intended for academic and educational purposes.
