🚀 Flask CMS – Customer Management System

A lightweight, fast, and secure Customer Management System built using Flask, SQLite, and Flask-Login.
This project provides customer CRUD operations, admin authentication, theme switching (Dark/Light), and a clean UI.

📌 Features
🔐 Authentication System

Admin registration (first user becomes admin automatically)

Login using email or username

Secure password hashing

Logout system

Session-based user authentication

👤 Customer Management

Add new customers

Edit customer details

Delete customers (Admin only)

View customer list with full table layout

Validate email + phone number fields

Auto-check salary format

🎨 User Interface

Modern responsive UI

Home hero section with company banner

Sidebar navigation

Light/Dark theme toggle

Dynamic theme using CSS variables

Fully mobile-friendly layout

🗄️ Database

SQLite database (cms.sqlite)

Two tables:

users

customers

🔧 Tech Stack

Python (Flask)

SQLite

HTML + CSS + Jinja2 Templates

JavaScript (Theme Switch)

Flask-Login

SQLAlchemy ORM

📁 Project Structure

flask-cms/
│── app.py
│── cms.sqlite
│
├── static/
│ ├── css/
│ │ └── style.css
│ ├── js/
│ │ └── theme.js
│ └── images/
│ └── dummycompany.png
│
└── templates/
├── base.html
├── home.html
├── login.html
├── register.html
├── dashboard.html
├── customer_list.html
├── add_customer.html
└── edit_customer.html

⚙️ Installation Guide

1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/flask-cms.git

cd flask-cms

2️⃣ Create Virtual Environment
python -m venv venv

3️⃣ Activate Environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Run the App
python app.py

🛡️ Security Features

Password hashing using Werkzeug

Admin-only access for sensitive routes

Session protection via Flask-Login

Registration is disabled after the first admin is created

📝 License

This project is All Rights Reserved.
You may view the source code but cannot copy, modify, or reuse it without permission.
