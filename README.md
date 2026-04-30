# Library System (Palin Book Management)

A comprehensive web-based **library book management system** built with **Django** for managing the book catalog, member accounts, and borrowing requests in a single platform.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
  - [Core Features](#core-features)
  - [Book & Catalog Management](#book--catalog-management)
  - [Member Accounts & Profiles](#member-accounts--profiles)
  - [Borrowing & Requests](#borrowing--requests)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Development Server](#development-server)
  - [Admin Panel](#admin-panel)
- [User Roles](#user-roles)
- [Application Modules](#application-modules)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
  - [Key Settings (`backend/settings.py`)](#key-settings-backendsettingspy)
  - [Media Uploads (Cover Images)](#media-uploads-cover-images)
- [Documentation Files](#documentation-files)
- [Version History](#version-history)
- [License](#license)
- [Support](#support)

## Overview

**Library System (Palin Book Management)** is a Django-based web application developed for **IT 205 (IT 2A) – Integrative Programming & Technologies**.

It is designed to help a library:

- Maintain a centralized **book catalog** (including book details and availability)
- Manage **member accounts** and basic profile information
- Handle **borrowing requests/records** with status tracking for librarians/admins

The system focuses on making day-to-day library operations more organized for staff, while giving members a clear way to browse books and request borrowing.

## Features

### Core Features

- **Authentication and role-based access**
  - Sign up / login / logout flows (powered by Django + `django-allauth`)
  - Role-aware navigation and permissions (e.g., Member vs Librarian/Admin)
- **Library catalog browsing**
  - Browse available books through a web interface
  - View detailed book information pages
- **Borrowing workflow**
  - Members can submit borrowing requests
  - Librarians/Admins can review and update request status

### Book & Catalog Management

- **Book records**
  - Add new books to the catalog
  - Edit existing book details
  - Remove outdated/incorrect book entries (as permitted)
- **Catalog organization**
  - Author and category organization (where applicable in the UI)
  - Improved discoverability via search and results pages
- **Cover images**
  - Optional cover image upload/display for richer book detail pages

### Member Accounts & Profiles

- **Member registration and management**
  - Register member accounts
  - View and maintain member information
- **Profile pages**
  - Member-facing profile page
  - Basic profile editing (where enabled by templates/views)

### Borrowing & Requests

- **Request tracking**
  - Track which member requested/borrowed which book
  - Maintain relevant dates and status (based on the borrowing module)
- **Librarian review**
  - Review request details
  - Update request status to reflect the current state of the transaction

## System Requirements

| Requirement | Version |
|---|---|
| Python | 3.10 or higher (3.12 recommended) |
| Django | 4.x or higher |
| Database | SQLite (default) |
| Browser | Chrome, Firefox, Edge, Safari |

Recommended:

- 4GB RAM minimum
- 1GB free disk space

## Installation

1. Clone or download the project

```bash
git clone <repository-url>
cd Palin_Book_Management
```

2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the virtual environment

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. Install dependencies

If your project includes a `requirements.txt`, install from it:

```bash
pip install -r requirements.txt
```

If no `requirements.txt` is provided, install the core dependencies manually:

```bash
pip install django django-allauth
```

5. Run database migrations

```bash
python manage.py migrate
```

6. (Optional) Create a superuser account

```bash
python manage.py createsuperuser
```

## Running the Application

### Development Server

Activate your virtual environment (if not already active), then run:

```bash
python manage.py runserver
```

Open your browser and navigate to:

- `http://127.0.0.1:8000/` (application)
- `http://127.0.0.1:8000/admin/` (admin panel)

### Admin Panel

Use the Django admin to manage records (depending on what’s registered in `admin.py` across apps):

- User accounts (including roles via the custom user model)
- Books / members / borrowing records (if enabled in admin)

## User Roles

| Role | Permissions |
|---|---|
| Member (Student/Guest) | Browse the catalog, view book details, manage profile (where enabled), submit borrow requests. |
| Librarian / Admin | Manage books and member records, review borrow requests, update request statuses, access admin features as configured. |

## Application Modules

| Module | Purpose |
|---|---|
| `accounts/` | Custom user model (`CustomUser`), role handling, account-related logic, and authentication integration. |
| `book_management/` | Core catalog pages (browse, add/edit books), search and book detail views, and shared templates for the library UI. |
| `borrow/` | Borrowing workflow: request creation, record tracking, request detail, and status updates. |
| `members/` | Member-facing registration/management pages and member data handling. |
| `backend/` | Django project configuration (settings, root URLs, WSGI/ASGI). |

## Project Structure

```text
Palin_Book_Management/
├── accounts/
├── backend/
├── book_management/
├── borrow/
├── members/
├── templates/
├── media/               # Uploaded files (e.g., book cover images)
├── static/              # Project-level static assets (if present)
└── manage.py
```

## Configuration

### Key Settings (`backend/settings.py`)

| Setting | Description |
|---|---|
| `DEBUG` | Keep `True` for development; set `False` for production. |
| `ALLOWED_HOSTS` | Configure allowed domains/hosts for deployment. |
| `DATABASES` | Uses SQLite by default (`db.sqlite3`). |
| `AUTH_USER_MODEL` | Set to `accounts.CustomUser` (custom user model). |
| `STATIC_URL` / `STATICFILES_DIRS` | Static file configuration for CSS/JS assets. |
| `MEDIA_URL` / `MEDIA_ROOT` | Media file configuration for uploads (e.g., cover images). |

### Media Uploads (Cover Images)

This project is configured to serve uploaded media files in development via:

- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = BASE_DIR / "media"`

When running locally with `DEBUG=True`, uploaded files are accessible via the dev server.

## Documentation Files

| File | Description |
|---|---|
| `README.md` | Main project documentation and setup guide. |
| `CODE_COMMENTS.md` | Notes and explanations about the codebase (if provided). |

## Version History

- **Version 1.0 – Initial Release**
  - Core user authentication and role support
  - Book catalog management (add/edit/remove, book details)
  - Member management and profile pages
  - Borrowing/request module with status tracking

## License

This project is intended for academic use as part of coursework. If you plan to distribute or deploy publicly, add a license file (e.g., MIT) and update this section accordingly.

## Support

If you encounter issues running the project:

- Confirm your virtual environment is activated and dependencies are installed.
- Re-run migrations: `python manage.py migrate`
- Check Django settings in `backend/settings.py` (especially `DEBUG`, `ALLOWED_HOSTS`, and media/static settings).

