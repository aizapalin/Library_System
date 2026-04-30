# System Comments Guide

This file contains simple comments for folders and files in this project without changing runtime behavior.

## Folder Comments

- `backend/`: This folder contains the Django project configuration and entry settings.
- `accounts/`: This folder handles custom users, authentication helpers, and account-related setup.
- `accounts/migrations/`: This folder stores database migration history for the accounts app.
- `book_management/`: This folder contains the main library catalog features and book workflows.
- `book_management/migrations/`: This folder stores database migration history for the book management app.
- `book_management/templates/`: This folder stores HTML templates for catalog and profile screens.
- `book_management/static/`: This folder stores CSS and JavaScript assets for UI behavior and styling.
- `book_management/static/book_management/css/`: This folder stores stylesheet files for page design.
- `book_management/static/book_management/js/`: This folder stores frontend scripts for carousel and search.
- `borrow/`: This folder contains borrowing request features and status update workflows.
- `borrow/migrations/`: This folder stores database migration history for the borrow app.
- `borrow/templates/`: This folder stores borrowing page templates.
- `members/`: This folder contains member registry and member management features.
- `members/migrations/`: This folder stores database migration history for the members app.
- `members/templates/`: This folder stores member page templates.
- `templates/`: This folder stores shared/global templates.
- `templates/book_management/`: This folder stores auth templates used by book management screens.

## File Comments

### Root / Project

- `manage.py`: This file is the Django command-line entry point for running management commands.
- `backend/settings.py`: This file defines project settings such as apps, middleware, templates, and database.
- `backend/urls.py`: This file defines root URL routing for all apps.
- `backend/asgi.py`: This file exposes ASGI application configuration.
- `backend/wsgi.py`: This file exposes WSGI application configuration.
- `templates/base.html`: This file is the shared base template used by app pages.

### Accounts App

- `accounts/apps.py`: This file defines app metadata for the accounts app.
- `accounts/models.py`: This file defines the custom user model and account-related signals.
- `accounts/views.py`: This file contains account-specific view logic.
- `accounts/decorators.py`: This file contains access control decorators such as librarian checks.
- `accounts/admin.py`: This file configures account models in Django admin.
- `accounts/tests.py`: This file is reserved for account app tests.
- `accounts/migrations/0001_initial.py`: This migration creates initial account tables.
- `accounts/migrations/0002_customuser_profile_pic_alter_customuser_role.py`: This migration updates user profile fields.
- `accounts/migrations/0003_migrate_student_to_guest.py`: This migration updates legacy role values.
- `accounts/migrations/0004_customuser_library_id.py`: This migration handles user library ID updates.
- `accounts/migrations/0004_customuser_librarian_flags.py`: This migration adds librarian flag fields.
- `accounts/migrations/0005_merge_20260430_0539.py`: This migration merges branching migration histories.

### Book Management App (Python)

- `book_management/apps.py`: This file defines app metadata for the book management app.
- `book_management/models.py`: This file defines book, author, category, and detail models.
- `book_management/forms.py`: This file defines forms such as librarian registration.
- `book_management/views.py`: This file implements catalog, profile, borrow, and management workflows.
- `book_management/urls.py`: This file maps book management routes to view functions.
- `book_management/admin.py`: This file configures book management models in admin.
- `book_management/tests.py`: This file is reserved for book management tests.
- `book_management/members/models.py`: This file contains member model code under the nested module.
- `book_management/migrations/0001_initial.py`: This migration creates initial book management tables.
- `book_management/migrations/0002_book_total_copies_bookdetails_cover_image_and_more.py`: This migration adds inventory and detail fields.

### Book Management Templates

- `book_management/templates/book_management/index.html`: This file renders the librarian catalog page.
- `book_management/templates/book_management/member_books.html`: This file renders the member-facing catalog page.
- `book_management/templates/book_management/book_detail.html`: This file renders one book with borrow request form.
- `book_management/templates/book_management/profile.html`: This file renders profile and member borrow history.
- `book_management/templates/book_management/edit_profile.html`: This file renders the edit profile page.
- `book_management/templates/book_management/add.html`: This file renders the add new book form.
- `book_management/templates/book_management/edit.html`: This file renders the rewrite/edit book form.
- `book_management/templates/book_management/add_author.html`: This file renders add/delete author management.
- `book_management/templates/book_management/add_category.html`: This file renders add/delete category management.
- `book_management/templates/book_management/librarian_register.html`: This file renders librarian-only registration form.
- `book_management/templates/book_management/MemberBook.html`: This file stores an additional member book-related template.

### Shared Auth Templates

- `templates/book_management/login.html`: This file renders the login page.
- `templates/book_management/signup.html`: This file renders the signup page.

### Book Management Static CSS

- `book_management/static/book_management/css/Index_style.css`: This file styles catalog, profile, and dashboard screens.
- `book_management/static/book_management/css/Member_style.css`: This file styles member and borrow-related shared pages.
- `book_management/static/book_management/css/Add_style.css`: This file styles the add book form page.
- `book_management/static/book_management/css/Edit_style.css`: This file styles the edit/rewrite book form page.
- `book_management/static/book_management/css/Author_style.css`: This file styles auth and author-related card layouts.
- `book_management/static/book_management/css/Category_style.css`: This file styles category management page UI.

### Book Management Static JS

- `book_management/static/book_management/js/carousel.js`: This file powers carousel scrolling, arrows, and drag support.
- `book_management/static/book_management/js/search_suggestions.js`: This file powers live search suggestions while typing.

### Borrow App

- `borrow/apps.py`: This file defines app metadata for the borrow app.
- `borrow/models.py`: This file defines borrow request/record data structures.
- `borrow/forms.py`: This file defines borrow-related forms.
- `borrow/views.py`: This file contains borrow listing, detail, and status update logic.
- `borrow/urls.py`: This file maps borrow routes to view functions.
- `borrow/admin.py`: This file configures borrow models in admin.
- `borrow/tests.py`: This file is reserved for borrow app tests.
- `borrow/migrations/0001_initial.py`: This migration creates initial borrow tables.
- `borrow/migrations/0002_alter_borrowrecord_status.py`: This migration updates borrow status choices.
- `borrow/migrations/0003_alter_borrowrecord_status.py`: This migration further refines borrow status handling.
- `borrow/templates/borrow/index.html`: This file renders borrow records listing.
- `borrow/templates/borrow/request_detail.html`: This file renders one borrow request and status actions.
- `borrow/templates/borrow/add.html`: This file renders add borrow record form.

### Members App

- `members/apps.py`: This file defines app metadata for the members app.
- `members/models.py`: This file defines member profile/registry data.
- `members/forms.py`: This file defines member-related forms.
- `members/views.py`: This file contains member listing and management logic.
- `members/urls.py`: This file maps member routes to view functions.
- `members/admin.py`: This file configures member models in admin.
- `members/tests.py`: This file is reserved for members app tests.
- `members/migrations/0001_initial.py`: This migration creates initial members tables.
- `members/templates/members/index.html`: This file renders the member registry list.
- `members/templates/members/add.html`: This file renders add member form.
- `members/templates/members/edit.html`: This file renders edit member form.
- `members/templates/members/delete.html`: This file renders member delete confirmation.
- `members/templates/members/login.html`: This file renders member login form.
- `members/templates/members/register.html`: This file renders member register form.

