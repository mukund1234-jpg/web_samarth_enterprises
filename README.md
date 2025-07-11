# 🛠️ AMC Service Management System - Django Web Application

This is a Django-based web application for managing Annual Maintenance Contracts (AMC) for products like ACs, Water Purifiers, Chimneys, etc. The system is designed for businesses to handle customer requests, schedule services, track third-party workers, and generate service bills.

---

## 🚀 Features

- ✅ Role-based login system:
  - **Admin**: Add Office Workers
  - **Office Worker**: Create and manage AMC service requests
  - **Customer**: View service status and bills via OTP
- ✅ Product Categories: AC, Water Purifier, Chimney/Hob, and more
- ✅ Service tracking and duration (1-year and 3-year AMC)
- ✅ WhatsApp bill link generation
- ✅ OTP-based secure customer login (via Gmail)
- ✅ `.env` file for managing secrets (e.g., Gmail credentials, secret keys)
- ✅ Bootstrap UI with responsive design
- ✅ Clean code structure using Django best practices

---

## 🧰 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, Bootstrap, CSS
- **Database**: SQLite (can switch to PostgreSQL)
- **Email**: Gmail SMTP for OTP/bill notifications
- **Security**: `python-decouple`, `.env`, `.gitignore`

---

## 🔧 Local Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd AMCAPP
