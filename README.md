# Laundry Billing Management System (Django)

A professional Laundry Billing Management System built using Django, designed for laundry service providers working with hotels and institutions.  
This system helps manage hotels, laundry items, item-wise rates, monthly bills, invoices (PDF), and billing summaries in an organized way.

---

## Features

### 🔹 Master Management
- Add / Update / Delete Hotels
- Add Laundry Items (bedsheets, towels, etc.)
- Assign item-wise rates per hotel
- Set transport rate per trip for each hotel

### 🔹 Billing System
- Generate Monthly Bills hotel-wise
- Add multiple items with quantities
- Auto calculation:
  - Item Total = Quantity × Rate
  - Transport Charges
  - Grand Total
- Auto-generated Invoice Number
- Printable invoice view
- PDF invoice generation

### 🔹 Billing Summary
- View all invoices in one place
- Filter bills by month
- Total revenue calculation
- Delete incorrect/practice invoices safely

### 🔹 Professional Invoice
- Company branding
- Client details
- Item-wise billing
- Payment terms
- Authorized signatory
- Computer-generated invoice note

---

## 🛠 Tech Stack

- Backend: Python, Django
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite (development)
- PDF Generation: xhtml2pdf
- Version Control: Git & GitHub

---


## ⚙️ Installation & Setup

### 1. Clone the Repository
  git clone https://github.com/Abhinandan2424/laundry-billing-system-django.git
  cd laundry-billing-system-django

### 2.create virtual environment
  python -m venv venv
  venv\Scripts\activate   # Windows

### 3. Install Dependencies
  pip freeze > requirements.txt

### 4. Run Migrations
  python manage.py makemigrations
  python manage.py migrate

### 5. Run Development Server
  python manage.py runserver



