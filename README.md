# 🎫 Evently - Modern Event Management System

**Evently** is a high-performance, secure, and visually stunning Event Management System built with **Django 5.x**. It provides a seamless experience for administrators, event organizers, and participants to manage, discover, and join events.

---

## 🌟 Key Features

### 🔐 Enterprise-Grade Security
- **Email Activation:** Secure verification links powered by **Django Signals**. New accounts are locked until activated via email.
- **RBAC (Role-Based Access Control):** Granular permissions for Admins, Organizers, and Participants.
- **Secure Auth:** Industry-standard password hashing and secure session management.
- **Password Recovery:** Fully integrated SMTP-based forgot password workflow.

### 📅 Event Management & Discovery
- **Dynamic Homepage:** Live statistics showing platform activity (Events, Users, Locations, Categories).
- **Advanced Search:** Real-time event searching by name and instant category filtering.
- **Approval Workflow:** Admins can review and approve events before they go live.
- **Participation System:** One-click Join/Leave functionality with real-time attendee tracking.

### 🎨 Premium UI/UX
- **Adaptive Theme:** Smooth transitions between Light and Dark modes with persistent user preference.
- **Responsive Design:** Optimized for everything from mobile phones to large desktop monitors.
- **Dashboard Analytics:** Tailored statistical overviews for every user role.
- **Premium Aesthetics:** Modern typography, animated backgrounds, and intuitive navigation.

---

## 📖 How to Use Evently

### 1. Getting Started
- **Registration:** Click "Get Started" or "Register". Fill in your details.
- **Account Activation:** After registering, check your inbox for an activation email. Click the link to verify your account. **Note:** You cannot login until your account is activated.
- **Login:** Use your credentials to access your personalized dashboard.

### 2. For Participants (Default Role)
- **Discover Events:** Browse the "Events" page to find upcoming experiences.
- **Search & Filter:** Use the search bar or category dropdown to narrow down your interests.
- **Join Events:** Click on an event to view details and hit "Join Event" to participate.
- **Track Activity:** Your dashboard shows how many events you've joined and provides quick access to them.

### 3. For Organizers
- **Create Events:** Use the "Add Event" button on your dashboard to submit a new event.
- **Approval:** If the platform requires it, your event will be "Pending" until an admin approves it.
- **Manage Events:** Track participation counts and update event details anytime through the "Manage My Events" section.

### 4. For Administrators
- **User Oversight:** View and manage all registered users from the "User Management" panel.
- **Content Moderation:** Approve or reject submitted events to maintain platform quality.
- **Categories:** Create and update event categories to keep the platform organized.

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

Linkedin:  **[MD. Likhon Sorkar](https://github.com/likhon)**
