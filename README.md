# 🎫 Evently - Modern Event Management System

**Evently** is a high-performance, secure, and visually stunning Event Management System built with **Django 5.x**. It provides a seamless experience for administrators, event organizers, and participants to manage, discover, and join events.

---

## 🚀 Key Features

### 🔐 Enterprise-Grade Security
- **Email Activation:** Automatic account inactivation upon registration with secure email verification links handled via **Django Signals**.
- **Role-Based Access Control (RBAC):**
  - 🛡️ **Admin:** Platform-wide oversight, user management, category creation, and event approval.
  - 🎤 **Organizer:** Create and manage personal events, track participants.
  - 👤 **Participant:** Personal dashboard, event discovery, and one-click join/leave functionality.
- **Secure Password Reset:** Fully integrated SMTP-based password recovery.

### 📅 Advanced Event Discovery
- **Live Search & Filtering:** Real-time event search by name and filtering by categories.
- **Participation Tracking:** Monitor attendee counts and participant lists.
- **Approval Workflow:** Optional admin review for new events to ensure quality.

### 🎨 Premium UI/UX
- **Responsive & Modern:** Built with a "Mobile-First" philosophy.
- **Adaptive Dark Mode:** High-contrast dark theme for better accessibility.
- **Interactive Dashboards:** Tailored statistical overviews for every user role.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Framework** | Django 5.x (Python 3.10+) |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Frontend** | Tailwind CSS / Alpine.js / Vanilla CSS |
| **Config** | Python-Decouple (.env) |
| **Task Handling** | Django Signals |
| **Mailing** | SMTP (Gmail/Custom) |

---

## ⚙️ Installation & Setup

### 1. Clone & Environment
```bash
git clone https://github.com/yourusername/evently.git
cd evently
python -m venv .venv
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2. Configuration (`.env`)
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SITE_DOMAIN=evently.likhon.com.bd
SITE_PROTOCOL=https
```

### 3. Database & Roles
```bash
python manage.py migrate
python manage.py createsuperuser
# Ensure 'admin', 'organizer', and 'participant' groups are created in Django Admin
```

---

## 📊 Role Permissions Overview

| Feature | Participant | Organizer | Admin |
| :--- | :---: | :---: | :---: |
| Browse Events | ✅ | ✅ | ✅ |
| Join Events | ✅ | ✅ | ✅ |
| Create Events | ❌ | ✅ | ✅ |
| Manage Own Events | ❌ | ✅ | ✅ |
| Approve Events | ❌ | ❌ | ✅ |
| Manage Users | ❌ | ❌ | ✅ |
| Manage Categories | ❌ | ❌ | ✅ |

---

## 🤝 Contributing
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

Developed with ❤️ by **[MD. Likhon Sorkar](https://github.com/likhon)**
