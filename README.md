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

Developed with ❤️ by **[MD. Likhon Sorkar](https://github.com/likhon)**
