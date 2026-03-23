🚗 Parking Management System

A full-stack Django-based Parking Management System that helps manage vehicle parking operations efficiently, including vehicle entry, exit tracking, parking allocation, and payment handling.

📌 Overview

This project is designed to solve real-world parking problems in institutions, malls, and offices by digitizing the parking process. It allows administrators to track vehicles, manage parking slots, and monitor usage in real time.

✨ Features

🚘 Vehicle Entry & Exit Tracking

🅿️ Parking Slot Management

⏱️ Automatic Parking Duration Calculation

💰 Payment Handling (based on duration)

📊 Admin Dashboard for monitoring

🔄 REST APIs for integration

🗂️ Database storage using SQLite

🛠️ Tech Stack

Layer	Technology Used

Backend	Python, Django

API	Django REST Framework

Database	SQLite

Frontend	HTML, CSS (Django Templates)

📂 Project Structure

parking-_management/

│

├── manage.py

├── db.sqlite3

│

├── parkingsystem/        # Project settings

│   ├── settings.py

│   ├── urls.py

│   └── ...

│

├── parking/              # Main application

│   ├── models.py         # Database schema

│   ├── views.py          # Logic & request handling

│   ├── serializers.py    # API layer

│   ├── urls.py           # Routing

│   ├── templates/        # UI files

│   ├── utils.py          # Helper functions

│   └── migrations/

⚙️ Installation & Setup

1️⃣ Clone Repository

git clone https://github.com/vinayak-ck/parking-_management.git

cd parking-_management

2️⃣ Create Virtual Environment

python -m venv venv

venv\Scripts\activate   # Windows

3️⃣ Install Dependencies

pip install django djangorestframework

4️⃣ Run Migrations

python manage.py migrate

5️⃣ Start Server

python manage.py runserver

6️⃣ Open in Browser

http://127.0.0.1:8000/

📊 System Modules

🚘 Parking Module

Handles vehicle check-in and check-out

Stores entry/exit timestamps

🅿️ Slot Management

Allocates parking slots dynamically

Tracks availability

💰 Payment Module

Calculates charges based on time

Stores payment details

📡 API Module

Built using serializers

Can be integrated with mobile apps

🎯 Use Cases

College / Campus Parking

Shopping Malls

Office Buildings

Apartment Complexes

🚀 Future Enhancements

🔐 User Authentication System

💳 Online Payment Gateway Integration

📱 Mobile App Integration

📈 Analytics Dashboard (charts & reports)

🤖 AI-based parking prediction


