# RFQ Auction System

## 📌 Overview

This project implements a **Request for Quotation (RFQ) system with British Auction logic**.

Suppliers compete by placing bids, and the system dynamically extends auction time based on configurable rules. The goal is to ensure **fair competition, prevent last-minute manipulation, and provide transparent bidding**.

---

## 🚀 Features

### RFQ Management

* Create RFQ with configurable auction parameters
* Define bid start, close, and forced close times

### Bidding System

* Suppliers can place bids
* Automatic ranking (L1, L2, L3...) based on price
* Validation to prevent invalid bids

### Auction Extension Logic

* Trigger window (X minutes)
* Extension duration (Y minutes)
* Extension triggers:

  * Bid placed in last X minutes
  * Rank change
  * Lowest bidder (L1) change

### Auction Lifecycle

* ACTIVE → CLOSED → FORCE_CLOSED
* No bids allowed after close time
* Hard stop at forced close time

### Activity Logs

* Tracks:

  * Bid submissions
  * Auction extensions
* Provides transparency and audit trail

---

## 🧱 Tech Stack

* **Frontend:** React
* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy

---

## 🏗️ High Level Design

The system follows a **3-tier architecture**:

* **Frontend (React):** User interface for auctions, bidding, and logs
* **Backend (FastAPI):** Handles business logic, validation, and auction rules
* **Database (PostgreSQL):** Stores RFQs, bids, suppliers, and logs

📌 See architecture diagram:
`/docs/HLD.png`

---

## 🗄️ Database Schema

Main tables:

### RFQ

* id (PK)
* name
* bid_start_time
* bid_close_time
* current_bid_close_time
* forced_close_time
* trigger_window_minutes
* extension_duration_minutes
* extension_type
* status

### Bids

* id (PK)
* rfq_id (FK)
* supplier_id (FK)
* price
* created_at

### Suppliers

* id (PK)
* name

### AuctionLogs

* id (PK)
* rfq_id (FK)
* event_type
* description
* created_at

📌 See schema diagram:
`/docs/DB_Schema.png`

---

## 🔄 System Flow

1. User views RFQ list
2. Opens RFQ details
3. Places bid
4. Backend validates:

   * RFQ exists
   * Supplier exists
   * Auction time validity
5. Bid is stored
6. Ranking updated
7. Auction extension logic applied
8. Logs recorded

---

## ⚙️ Backend Features

* REST APIs for RFQ, bids, suppliers
* Auction validation:

  * No bids after bid close time
  * No bids after forced close time
* Auction extension service
* Status updates (ACTIVE / CLOSED / FORCE_CLOSED)

---

## 🎨 Frontend Features

* RFQ List Page:

  * Shows auctions, status, lowest bid

* RFQ Details Page:

  * Timer countdown
  * Bid submission
  * Ranking table (L1, L2, L3)
  * Auction configuration
  * Activity logs

* Components:

  * Timer
  * Bid Form
  * Bid List
  * Logs List

---

## 🧪 Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### Frontend

```bash
cd frontend
npm install
npm start
```

---

## 🧠 Key Design Decisions

* **Backend validation enforced** to prevent invalid bids
* **Forced close time ensures auction termination**
* **Extension logic implemented in service layer** for modularity
* **Logs provide auditability and transparency**

---

## ⚠️ Assumptions

* Simplified supplier model
* No authentication system
* Quote fields minimized

---

## 🔮 Future Improvements

* Real-time updates using WebSockets
* Authentication and user roles
* Advanced analytics dashboard
* Notifications for bid updates

---

## 📎 Submission Artifacts

* HLD Diagram → `/docs/HLD.png`
* Database Schema → `/docs/DB_Schema.png`
* Backend Code → `/backend`
* Frontend Code → `/frontend`

---

## 🙌 Conclusion

This project demonstrates a scalable and modular implementation of a **British Auction RFQ system**, focusing on fairness, extensibility, and clear system design.

---

**Thank you for reviewing this submission.**
