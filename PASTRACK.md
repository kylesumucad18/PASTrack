# PAStrack — CLAUDE.md

## What This System Does
PAStrack (Provincial Assessor's Office Tracking System) is a case management and document tracking web application built for the Local Government Units (LGUs) and the Provincial Assessor's Office in Cebu Province. 

It digitizes the workflow for real property document submissions. LGU Administrators use a wizard interface to submit cases and documents. Capitol Staff (Receivers, Examiners, Tax Mappers, Approvers, Numberers, and Releasers) process these cases through a strict, multi-step pipeline. Citizens can transparently check the real-time status of their transactions via a public tracking portal using a Tracking ID.

## Tech Stack
- **Backend Framework:** Django (v5.2.8) / Python (v3.11+)
- **Database:** Supabase (PostgreSQL) for production, SQLite for local development/testing.
- **Frontend UI:** Django Templates combined with React (v18.3.1) and Tailwind CSS (v3.4.17). React components are built using Vite.
- **APIs & Storage:** Django REST Framework, `django-storages` with boto3 (for AWS S3 / Supabase Storage), ConvertAPI (for document conversion).
- **Authentication & Security:** Argon2 password hashing, django-allauth, custom session timeouts and lockout middleware.

## Project Structure
- `core/`: Main Django application housing business logic, database models (`models.py`), views, forms, middleware, and Django templates.
- `frontend/`: Contains the React + Vite source code for interactive UI components.
- `legaltrack/`: The Django project configuration folder (contains `settings.py`, root `urls.py`, `wsgi.py`, `asgi.py`).
- `api/`: Django REST Framework endpoints.
- `media/`: Local directory for user-uploaded files and case documents (when not using S3).
- `staticfiles/` & `static/`: Static assets collected for deployment.
- `scripts/`: Utility and deployment scripts (`.bat` / `.ps1` files).

## User Roles & Workflows
- **Super Admin (`super_admin`)**: System administration, user management, analytics, and audit logs.
- **LGU Admin (`lgu_admin`)**: Submits transactions/cases on behalf of their municipality and tracks submissions.
- **Receiver (`capitol_receiving`)**: Receives incoming physical documents from LGUs and assigns them.
- **Examiner (`capitol_examiner`)**: Reviews case details, examines legal and technical documents, and requests revisions.
- **Tax Mapper (`capitol_taxmapper`)**: Assesses boundary and mapping specifics.
- **Approver (`capitol_approver`)**: Approves cases or returns them for correction.
- **Numberer (`capitol_numberer`)**: Assigns official case numbers and Tax Declaration numbers sequentially.
- **Releaser (`capitol_releaser`)**: Marks cases as released and ready for pickup/delivery.

## Database Models Overview
- `CustomUser`: Extends `AbstractUser`. Uses `email` as the login field. Contains fields for `role`, `lgu_municipality`, `account_status`, `staff_id`, and tracks failed login attempts and password reset codes.
- `Case`: The central transaction model. Key fields include `tracking_id`, `draft_id`, `status`, `ownership_type`, `client_name`, `case_type`, `lot_number`, area details, and timestamps for every stage of the workflow. Includes relations to users for each processing stage (e.g., `assigned_to`, `received_by`).
- `LGUTaxDeclarationSequence`: Critical model that tracks the current Tax Declaration sequence count for each LGU. Uses database locks to ensure strict sequential numbering.
- `AuditLog`: Polymorphic tracking of system actions, actors, and IP addresses.
- `PasswordResetRequest`: Tracks requested password reset flows.

## Key Views & URLs
Main routes are structured in `core/urls.py` and `legaltrack/urls.py`:
- **Public & Support:** `/` (Landing), `/track/` (Public Tracking), `/support/`
- **Dashboard:** `/dashboard/`, `/submissions/`, `/my-submissions/`
- **Case Management (Wizard):** `/case/<tracking_id>/step/<step>/`, `/submit/`, `/drafts/`
- **Case Pipeline Actions:** `/case/<tracking_id>/<action>/` (Actions include: `receive`, `assign`, `submit-for-approval`, `approve`, `assign-taxmapper`, `complete-taxmapping`, `assign-td-number`, `release`)
- **Admin/Analytics:** `/analytics/`, `/reports/`, `/audit-logs/`, `/users/`
- **Authentication:** `/login/`, `/logout/`, `/accounts/activate/<token>/`, `/accounts/password_reset/`

## Deployment & Environment
Deployed on **Render** (via `render.yaml`) and optionally **Vercel** (`vercel.json`).
**Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput 2>&1 || true`
**Start Command:** `python manage.py migrate --noinput && gunicorn legaltrack.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --graceful-timeout 30`

**Key Environment Variables:**
- Security: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
- Database: `LEGALTRACK_DB_PROVIDER` (`supabase` or `sqlite`), `DATABASE_URL`
- Storage: `SUPABASE_S3_ACCESS_KEY_ID`, `SUPABASE_S3_SECRET_ACCESS_KEY`, `SUPABASE_BUCKET_NAME`, `SUPABASE_S3_ENDPOINT_URL`
- Email: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `BREVO_API_KEY`
- Features: `LEGALTRACK_SEND_EMAILS`, `LEGALTRACK_FORCE_IPV4`

## Testing & CI/CD
### Testing
- **Test Suite:** There is a Django test suite located in `core/tests.py`, along with several standalone `test_*.py` files in the project root (e.g., `test_db_save.py`, `test_convert.py`).
- **Coverage:** The core `Case` workflow/pipeline is explicitly tested (e.g., `test_end_to_end_capitol_flow_to_release`, `test_approver_can_return_for_correction`), covering status transitions from `not_received` to `released`. However, the critical `LGUTaxDeclarationSequence.get_next_number()` concurrency method does **not** appear to have any test coverage.
- **Running Tests:** Tests are run locally using `py manage.py test`. Coverage can be generated with `coverage run --source='.' manage.py test`.

### CI/CD
- **No CI/CD pipeline currently configured.** There are no GitHub Actions (`.github/workflows/`), GitLab CI, or similar configurations in the repository.
- **Automation:** No automated tests, linting, or type checks run on push/PR.
- **Deployments:** Deployments to Render are either manual (via `.bat`/`.ps1` scripts like `deploy-render.bat`) or depend on Render's auto-deploy for connected branches, but there is no CI gate blocking failing code from deploying.

## Current Branch & Active Features
- **Current Branch:** `fintest`
- **Active Work:** Recent commits (`730 - 5`, `729 - 4`, etc.) indicate ongoing work related to final testing, financial, or minor iterative fixes.

## Known Issues & Pending Improvements
- **Tax Mapper Role:** The README notes that the Tax Mapper role (`capitol_taxmapper`) is "*(To be implemented)*", but the underlying implementation is actually largely complete. The `Case` model has `needs_taxmapping` fields, and the workflow is functional (views like `assign_taxmapper` and `complete_taxmapping` exist, alongside `core/dashboard_taxmapper.html`). It appears functionally integrated but may be pending final business review.
- **Database Connection Resolution:** Supabase (PostgreSQL) outbound networking on Render/Vercel can sometimes resolve to IPv6 and fail. `settings.py` includes a custom `LEGALTRACK_FORCE_IPV4` DNS resolution fallback to prevent timeouts.
- **Email in Dev:** Email activation links print to the console instead of sending when in development mode unless explicitly configured.

### Environments
- **No dedicated staging environment:** There is no explicitly configured staging or preview environment defined in the repository (e.g., no separate Render YAML service for staging). 
- **Active Branch (`fintest`):** The `fintest` (final testing) branch acts as the current active branch for testing/iterating. It appears to be a parallel testing branch rather than a true staging pipeline.
- **Local Testing:** There is no documented automated way to test changes in a live environment before they hit production, other than running the local development server.

## Coding Conventions
- **Django Standard:** Uses standard Django patterns (models, views, forms, templates).
- **Type Hinting:** Extensive use of Python type hinting (e.g., `ClassVar[list[tuple[str, str]]]`) in models.
- **Business Logic in Models:** Heavy reliance on `@property` methods in the `Case` model (e.g., `remaining_area`, `client_display_name`) and custom `save()` overrides (e.g., `CustomUser` generating its own `staff_id`).
- **Concurrency Control:** Utilizes Django's `transaction.atomic()` and `select_for_update()` for safe sequence generation.
- **Frontend Integration:** Uses Vite for building React components in the `frontend/` directory, while standard pages rely on Django template rendering and Tailwind.

## Do NOT Touch
- **`LGUTaxDeclarationSequence.get_next_number()`**: This uses strict database-level locking (`select_for_update()`) to generate sequential Tax Declaration numbers. Modifying this logic risks introducing duplicate IDs and breaking the core legal requirement of the system.
- **Database Resolution Fallback (`_database_from_url` in `settings.py`)**: The custom IPv4 DNS resolution logic is critical for Render/Vercel deployments connecting to Supabase.
- **Authentication & Middleware**: The `CustomUser` model relies on email for login instead of username. `core.middleware` handles forced password changes and session lockouts. Modifying these without extreme care can lock users out of the system.
- **Workflow Status Pipeline**: The strict progression of `Case.status` choices (from `draft` -> `received` -> `to_examine` -> `for_approval` -> etc.). Altering state transitions will break the pipeline for Capitol Staff.
