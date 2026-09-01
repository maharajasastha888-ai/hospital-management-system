# Hospital Management System (HMS)

A full-stack Hospital Management System built with **Flask (REST API)** + **HTML/CSS/JavaScript (Bootstrap)**. Supports role-based access for Admin, Doctor, Receptionist, Pharmacist, and Lab Technician.

## Features

### Core Modules
- **Patient Management** — Add, Edit, Delete, Search patients with QR code generation
- **Doctor Management** — Manage doctors by department with schedule & availability
- **Appointment Booking** — Book, Cancel, Complete appointments with time slot management
- **OPD/IPD** — OPD registration, IPD admission, bed allocation
- **Pharmacy** — Medicine inventory, stock tracking (low stock alerts), pharmacy billing
- **Laboratory** — Order lab tests (Blood, Urine, X-Ray, MRI, etc.), upload reports
- **Billing** — Consolidated billing (consultation + lab + medicine), payment tracking, PDF invoice download
- **Reports** — Daily patient report, monthly revenue, doctor performance

### Extra Features
- **QR Code** — Auto-generated QR code for each patient
- **PDF Invoice** — Download/print professional invoices via ReportLab
- **Dashboard Charts** — Monthly revenue bar chart & patient distribution doughnut (Chart.js)
- **Dark Mode** — Toggleable dark theme (persisted in localStorage)
- **Chatbot** — Rule-based health assistant widget
- **AI Symptom Checker** — Analyze symptoms → suggest conditions, department & urgency level
- **Role-Based Access** — JWT authentication with role decorators (`@admin_required`, `@doctor_required`, etc.)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, Chart.js, Font Awesome |
| Backend | Python 3, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS |
| Database | SQLite (dev) / MySQL 8.0 (production) |
| Services | ReportLab (PDF), qrcode (QR), bcrypt (auth), Chart.js (charts) |

## Project Structure

```
Hospital-Management-System/
├── frontend/
│   ├── css/                        # style.css, dark-mode.css
│   ├── js/                         # api.js, auth.js, main.js, dashboard-charts.js, chatbot.js
│   ├── images/
│   └── pages/
│       ├── login.html
│       ├── admin/                  # Dashboard, Patients, Doctors, Appointments, Departments,
│       │                           # Pharmacy, Lab, Billing, Reports, Symptom Checker
│       ├── doctor/
│       ├── receptionist/
│       ├── pharmacist/
│       └── lab/
├── backend/
│   ├── app.py                      # Flask application factory
│   ├── config.py                   # Configuration (DB, JWT, Email, Uploads)
│   ├── models/                     # SQLAlchemy models (11 tables)
│   ├── routes/                     # REST API blueprints (11 modules)
│   ├── services/                   # QR generator, PDF generator, Email, SMS, AI checker
│   ├── middleware/                 # JWT + role-based auth decorators
│   └── utils/                      # Validators, helpers
├── database/
│   └── schema.sql                  # MySQL schema reference
├── assets/qrcodes/                 # Generated patient QR codes
├── uploads/lab_reports/            # Uploaded lab report files
├── run.py                          # Start the server
├── manage.py                       # CLI: seed, reset, init_db, create-admin
├── requirements.txt
└── .env                            # Environment variables
```

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Hospital-Management-System.git
cd Hospital-Management-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed the database (creates SQLite DB + sample data)
python manage.py seed

# 4. Start the server
python run.py
```

Open **http://localhost:5000** in your browser.

## Login Credentials

| Role | Username | Password |
|------|----------|---------|
| Admin | `admin` | `admin123` |
| Doctor | `doctor1` | `password123` |
| Receptionist | `reception` | `password123` |
| Pharmacist | `pharmacist` | `password123` |
| Lab Technician | `labtech` | `password123` |

## Switching to MySQL

1. Create a MySQL database named `hospital_management`
2. Edit `.env`:
   ```env
   DB_TYPE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_NAME=hospital_management
   ```
3. Run the seed script again:
   ```bash
   python manage.py seed
   ```

## API Overview

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/login` | POST | None | Login → returns JWT |
| `/api/auth/me` | GET | All | Current user info |
| `/api/admin/dashboard` | GET | Admin | Dashboard stats |
| `/api/patients` | GET/POST | Staff | List/Create patients |
| `/api/patients/<id>` | GET/PUT/DELETE | Staff | Patient CRUD |
| `/api/doctors` | GET/POST | Staff/Admin | List/Create doctors |
| `/api/appointments` | GET/POST | Staff | List/Book appointments |
| `/api/appointments/<id>/cancel` | PUT | Staff | Cancel appointment |
| `/api/departments` | GET/POST | Staff/Admin | Department CRUD |
| `/api/lab/tests` | GET/POST | Staff | Order lab tests |
| `/api/lab/tests/<id>/result` | PUT | Staff | Update test result |
| `/api/pharmacy/medicines` | GET/POST | Staff | Medicine CRUD |
| `/api/pharmacy/bills` | GET/POST | Staff | Pharmacy billing |
| `/api/billing/bills` | GET/POST | Staff | Create/View bills |
| `/api/billing/bills/<id>/pay` | POST | Staff | Record payment |
| `/api/billing/bills/<id>/pdf` | GET | Staff | Download PDF invoice |
| `/api/reports/daily-patients` | GET | Admin | Daily report |
| `/api/reports/monthly-revenue` | GET | Admin | Monthly revenue |
| `/api/symptom-checker` | POST | Staff | AI symptom analysis |

## Management Commands

```bash
python manage.py seed       # Create tables + seed sample data
python manage.py reset      # Drop all tables, re-create + seed
python manage.py init_db    # Create tables only
python manage.py create-admin  # Create a new admin user
```

## Extra Features Configuration

### Email (Appointment Confirmation)
Set these in `.env`:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### SMS (Twilio)
```env
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=+1234567890
```

### AI Symptom Checker
The built-in rule-based engine works out of the box. For external AI API:
```env
AI_API_KEY=your-key
AI_API_URL=https://api.example.com/symptom-checker
```

## License

MIT
