# 🅿️ Parking Management System

A full-stack parking management web application built with Django and Django REST Framework — automating vehicle entry, exit, slot allocation, and payment calculation.

> ⚠️ **Note**: This project is not deployed online. Run it locally using the instructions below.

---

## ✨ Features

- 🚗 Vehicle entry and exit tracking
- 🔢 Real-time parking slot availability
- 🧠 Dynamic slot allocation logic
- ⏱️ Duration-based payment calculation (per hour/minute)
- 📊 Admin dashboard for monitoring all parking activity
- 🔌 RESTful API built with Django REST Framework

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Django, Django REST Framework |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| API | REST (DRF) |

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/vinayak-ck/parking_management.git
cd parking_management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.  
Admin panel: `http://127.0.0.1:8000/admin`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/entry/` | Register vehicle entry |
| POST | `/api/exit/` | Register vehicle exit + calculate fee |
| GET | `/api/slots/` | Get available slot count |
| GET | `/api/history/` | View parking history |

---

## 📁 Project Structure

```
parking_management/
├── manage.py
├── requirements.txt
├── parking/
│   ├── models.py       # Vehicle, Slot, Session models
│   ├── views.py        # Entry, exit, slot views
│   ├── serializers.py  # DRF serializers
│   └── urls.py
└── templates/
    └── dashboard.html
```

---

## 📬 Contact

Built by [Vinayak Kanavalli](https://github.com/vinayak-ck) — vckanavalli@gmail.com
