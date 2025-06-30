<div align="center">

# 🎓 LearnNow — Learning Management System

**A production-style course marketplace backend built with Django REST Framework.**

Teachers publish paid courses, students browse, buy, enrol, learn, and earn certificates — all through a clean, documented, JWT-secured REST API.

[![CI](https://github.com/omonuj/learning-management-systems/actions/workflows/ci.yml/badge.svg)](https://github.com/omonuj/learning-management-systems/actions/workflows/ci.yml)
[![CodeQL](https://github.com/omonuj/learning-management-systems/actions/workflows/codeql.yml/badge.svg)](https://github.com/omonuj/learning-management-systems/actions/workflows/codeql.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Stripe](https://img.shields.io/badge/Payments-Stripe-635BFF?logo=stripe&logoColor=white)](https://stripe.com/)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render&logoColor=white)](https://render.com/)
[![License](https://img.shields.io/badge/License-BSD-blue.svg)](#-license)

[Live API](https://learning-management-systems-10.onrender.com/) · [API Docs (Swagger)](https://learning-management-systems-10.onrender.com/) · [Report a Bug](https://github.com/omonuj/learning-management-systems/issues)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Data Model](#-data-model)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Project Status & Roadmap](#-project-status--roadmap)
- [Author](#-author)
- [License](#-license)

---

## 🧭 Overview

**LearnNow** is the backend for an online learning platform in the style of Udemy or Coursera. It exposes a REST API that a separate frontend (a React / Vite single-page app) consumes to deliver the full learning experience.

The system supports three roles — **Learners**, **Tutors (Teachers)**, and **Admins** — and covers the complete lifecycle of a course: authoring, publishing, discovery, purchase, enrolment, progress tracking, certification, reviews, and course Q&A.

It was built as a capstone project to demonstrate end-to-end backend engineering: modular app design, authentication, payments, media handling, relational data modelling, and API documentation.

---

## ✨ Features

**👩‍🎓 For Students**
- Register, log in, and manage a profile with an avatar
- Browse and search a catalog of courses by category, level, and language
- Add courses to a cart, apply coupons, and check out via **Stripe**
- Enrol in purchased courses and stream video lessons
- Track lesson-by-lesson completion and earn a **certificate** on completion
- Take personal notes, rate & review courses, and maintain a wishlist
- Ask questions on a course through threaded **Q&A**

**👨‍🏫 For Teachers**
- Create, update, and structure courses into sections (variants) and lessons
- Auto-computed video durations on upload (via `moviepy`)
- A dashboard with earnings, best-selling courses, student lists, and orders
- Create and manage discount **coupons**
- Receive **notifications** for new orders, reviews, and questions

**🔐 Platform**
- **JWT authentication** with access/refresh tokens (rotation + blacklisting)
- Role-based custom user model (email as the login identifier)
- Interactive **Swagger / ReDoc** API documentation
- **CORS** configured for a decoupled frontend
- Themed Django admin for internal management

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | Django 5.2 |
| API | Django REST Framework 3.16 |
| Auth | JWT — `djangorestframework-simplejwt` |
| Database | PostgreSQL (`psycopg2-binary`) |
| API Docs | `drf-yasg` (Swagger / ReDoc) |
| Payments | Stripe · PayPal |
| Media processing | `moviepy` / `imageio-ffmpeg` |
| Config | `environs` / `python-dotenv` |
| CORS | `django-cors-headers` |
| Admin UI | `django-jazzmin` |
| Server / Hosting | Gunicorn on Render |

---

## 🏗 Architecture

LearnNow uses a modular Django layout — a project package (`learning/`) plus one focused app per bounded context. Each app owns its own models, serializers, views, and URLs, and apps reference one another through Django's string-based model references to keep coupling loose.

```
learning-management-systems/
├── manage.py                # Django management entrypoint
├── requirements.txt
├── learning/                # Project config (settings, root URLconf, WSGI/ASGI)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                   # Custom user model, auth, profiles
├── teachers/                # Teacher profiles, coupons, dashboards
├── courses/                 # Courses, curriculum, reviews, notes, wishlist
├── carts/                   # Cart, orders, checkout
├── certificates/            # Enrolment, lesson completion, certificates
├── question_answer/         # Course Q&A threads
├── notifications/           # In-app notifications
├── static/  / staticfiles/  # Static assets (dev / collected)
└── media/                   # User-uploaded files (images, videos)
```

### App responsibilities

| App | Responsibility |
|-----|----------------|
| **users** | Custom `User` (email login, Learner/Tutor/Admin roles) and `UserProfile`. Registration, login, profile, password change, logout, JWT issue/refresh. |
| **teachers** | `Teacher` profile (1:1 with a user) and `Coupon`. Teacher dashboard: earnings, best sellers, students, reviews, orders, coupons, notifications. |
| **courses** | Catalog core: `Category`, `Courses`, `Variant`, `VariantItem`, `Note`, `Review`, `WishList`, `Country`. Search, detail, create/update; auto video-duration. |
| **carts** | `Cart`, `CartOrder`, `CartOrderItem`. Cart management, order creation, tax/coupon totals, Stripe checkout. |
| **certificates** | `EnrolledCourse`, `CompletedLessons`, `Certificate`. Enrolment, progress tracking, certification, student dashboard. |
| **question_answer** | `QuestionAnswer` and `QuestionAnswerMessage` threads on a course. |
| **notifications** | `Notification` records for order/review/question events. |

### Request flow

```
Client (React SPA)
      │  HTTPS + Bearer JWT
      ▼
learning/urls.py  ──►  <app>/urls.py  ──►  DRF APIView / ViewSet
      │                                          │
      │                                    <app>/serializers.py
      ▼                                          ▼
drf-yasg Swagger UI                        <app>/models.py ──► PostgreSQL
```

---

## 🗃 Data Model

High-level relationships between the core entities:

- A **Teacher** belongs to a **User**; a Teacher authors many **Courses**.
- A **Course** has many **Variants** (sections), each with many **VariantItems** (lessons).
- A **Student (User)** adds Courses to a **Cart**, which becomes a **CartOrder** of **CartOrderItems** at checkout.
- A paid order item creates an **EnrolledCourse**, against which **CompletedLessons** and a **Certificate** are tracked.
- Students leave **Reviews** and open **QuestionAnswer** threads on a Course.

```
User ──1:1──► Teacher ──1:N──► Course ──1:N──► Variant ──1:N──► VariantItem
 │                                │
 │                                ├──1:N──► Review
 │                                └──1:N──► QuestionAnswer ──1:N──► QuestionAnswerMessage
 │
 └──► Cart ──► CartOrder ──1:N──► CartOrderItem ──► EnrolledCourse ──► CompletedLessons / Certificate
```

---

## 📡 API Reference

All endpoints are served under `/api/`. Full request/response schemas are available in the interactive docs.

| Area | Base path |
|------|-----------|
| Auth & users | `/api/` |
| Courses | `/api/v1/courses/` |
| Carts & orders | `/api/v1/carts/` |
| Certificates & enrolment | `/api/v1/certificates/` |
| Teacher dashboard | `/api/v1/teachers/` |
| Q&A | `/api/v1/qa/` |
| Django admin | `/admin/` |
| Swagger UI | `/` |
| ReDoc | `/redoc/` |

**Authentication.** Obtain a token pair at `/api/login/` (or `/api/token/`), send it as `Authorization: Bearer <access>`, and refresh at `/api/token/refresh/`. Access tokens live **30 minutes**; refresh tokens **7 days** (rotated and blacklisted on use).

<details>
<summary><strong>Example: register and log in</strong></summary>

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Ada Lovelace","username":"ada","email":"ada@example.com","password":"secret123"}'

# Log in → returns { "access": "...", "refresh": "..." }
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"ada@example.com","password":"secret123"}'

# Call a protected endpoint
curl http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Bearer <access-token>"
```
</details>

---

## 🚀 Getting Started

### Prerequisites

- Python **3.12+**
- **PostgreSQL**
- **FFmpeg** (required by `moviepy` for video-duration processing)

### Installation

```bash
# 1. Clone
git clone https://github.com/omonuj/learning-management-systems.git
cd learning-management-systems

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Dependencies
pip install -r requirements.txt

# 4. Configure environment (see below), then:
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit:
- **API docs (Swagger):** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```dotenv
SECRET_KEY=your-django-secret-key
DEBUG=True

# PostgreSQL
DB_NAME=learnnow
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Payments
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
PAYPAL_CLIENT_ID=...
PAYPAL_SECRET_ID=...

# Frontend
FRONTEND_SITE_URL=http://localhost:5173
```

> ⚠️ The app **exits on startup** if the Stripe/PayPal keys or `FRONTEND_SITE_URL` are missing.

---

## ☁️ Deployment

Configured for **Render** (see `ALLOWED_HOSTS` / `CORS_ALLOWED_ORIGINS` in `learning/settings.py`) and served with **Gunicorn**:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn learning.wsgi
```

---

## 🧩 Project Status & Roadmap

This is an actively developed capstone project. Known items to harden before true production use:

- [ ] Restrict CORS — `CORS_ALLOW_ALL_ORIGINS` is currently `True` alongside the allow-list
- [ ] Ensure `DEBUG` is falsy in production environments
- [ ] Serve static files via WhiteNoise or a CDN instead of Django
- [ ] Add automated tests and CI
- [ ] Complete PayPal checkout flow alongside Stripe

---

## 👤 Author

**Jonah Odoh**

- GitHub: [@omonuj](https://github.com/omonuj)
- Project: [learning-management-systems](https://github.com/omonuj/learning-management-systems)

---

## 📄 License

Distributed under the **BSD License**. See the API schema metadata for details.

---

<div align="center">

⭐ If you find this project useful, consider giving it a star!

</div>
