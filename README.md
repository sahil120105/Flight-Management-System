# ✈️ Flight Management System (FMS)

A full-stack, database-driven web application that simulates real-world airline operations. The Flight Management System (FMS) is designed for both passengers and administrators to manage flight schedules, bookings, transactions, and user data seamlessly.

## 📚 Overview

This project is a comprehensive flight reservation system built using:

- **Flask (Python)** for the backend  
- **MySQL** for relational data persistence  
- **HTML5/CSS3** with **Jinja2** templates for the frontend  

It models airline logistics using core DBMS concepts like ER design, DDL/DML/DCL operations, triggers, stored procedures, and more.

---

## 🚀 Features

### 👤 Passenger Module
- Search & book flights
- View booking history
- Manage profile and personal data

### 🔐 Admin Module
- Flight, airport & aircraft management
- Passenger & transaction overview
- Super admin privileges for elevated control

### ⚙️ Backend Logic
- Real-time seat availability with dynamic updates
- Data integrity via triggers and constraints
- Stored procedures and PL/SQL functions for efficiency

---

## 🛠️ Tools & Tech Stack

| Category     | Tools/Tech                          |
|--------------|-------------------------------------|
| Frontend     | HTML5, CSS3, Jinja2 Templates       |
| Backend      | Python (Flask), RESTful Routing     |
| Database     | MySQL                               |
| Utilities    | Visual Studio Code, Postman         |

---

## 🧩 System Design

- **Entity-Relationship (ER) modeling**
- **Schema normalization**
- Triggers to enforce rules like overbooking prevention
- Stored procedures to automate booking logic
- Well-structured DDL, DML, DCL operations

---


## ✅ Steps to Run the Project

Here’s how to get the Flight Management System up and running on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/sahil120105/Flight-Management-System.git
cd flight-management-system
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Configure you MySQL Database

Open *app.py* and make changes to the following lines according your own details

Ensure your MySQL server is running and the database (fms2) with all required tables has been set up. Use the provided SQL scripts (*fmsdb.sql*) for schema and data.

```bash
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'        # Your MySQL host
app.config['MYSQL_USER'] = 'root'             # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'password'     # Your MySQL password
app.config['MYSQL_DB'] = 'fms2'               # Your database name
```

### 3. Run the application

```bash
python app.py
```

Visit http://127.0.0.1:5000 in your browser to start using the Flight Management System.