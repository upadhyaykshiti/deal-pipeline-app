# Investment Deal Pipeline (IC Tool)

A lightweight internal tool for investment teams to manage deals through a pipeline,
write IC memos, and run IC approvals with full auditability.

---

## 🧩 Features

### 1️⃣ Authentication & Roles
Email/password authentication with role-based access.

**Roles**
- **Admin**
  - Manage users
  - Full access to all features
- **Analyst**
  - Create & edit deals
  - Write and version IC memos
- **Partner**
  - Comment on deals
  - Vote
  - Approve / Reject IC decisions

---

### 2️⃣ Deal Pipeline (Kanban)
- Stages:
  - Sourced → Screen → Diligence → IC → Invested → Passed
- Drag-and-drop stage movement
- Every stage change creates an **Activity Log**
  - Example:  
    `Analyst moved Deal X from Screen to Diligence`

---

### 3️⃣ IC Memo
- Fixed sections:
  - Summary
  - Market
  - Product
  - Traction
  - Risks
  - Open Questions
- Markdown / plain text
- **Versioning**
  - Every save creates a new version
  - Full snapshot stored
- **Version History UI**
  - View older versions
  - Read-only mode for historical versions

---

### 4️⃣ IC Approval Flow
- Partners can:
  - Vote
  - Comment
  - Approve / Reject
- Once final decision is made:
  - Memo is locked
  - Voting & comments are disabled
  - Decision is recorded

---

## 🛠 Tech Stack

### Backend
- **FastAPI**
- SQLAlchemy
- PostgreSQL (SQLite supported for local dev)
- JWT Authentication

### Frontend
- **React**
- React Router
- Axios
- Role-based route guards

---


### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend
``bash
Copy code
cd frontend
npm install
npm run dev


--- Frontend runs on:
http://localhost:5173


--- Backend runs on:
http://localhost:8000

## Seed Data (Optional)

To populate the database with demo users and deals:
```bash
python seed.py