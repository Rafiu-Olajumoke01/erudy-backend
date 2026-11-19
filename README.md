# Erudy Backend

Erudy (schoolHub) is a multi-tenant school management platform: one system serving many schools, with each school's data completely isolated from every other school's. This repository is its backend, built with Django and Django REST Framework and consumed by a Next.js frontend.

## Highlights

- **Tenant isolation:** every record carries a school, every queryset is scoped by it, and serializers reject cross-school references
- **Role-based access:** four roles (Platform Owner, School Admin, Tutor, Student) with permissions per role and token authentication
- **Enrollment pipeline:** public application, admin approval, payment, then automatic student account creation and cohort assignment
- **Payments:** manual bank-transfer flow with promo codes, server-side amount calculation (the client never sets the price), and an admin review step
- **Academics:** class sessions, notes, assignments, capstone guidelines, bulk attendance, exams and results with score-integrity checks, and certificates
- **Communications:** role-scoped announcements and threaded messaging

## Tech stack

- Python
- Django and Django REST Framework
- Token authentication
- 12 Django apps

## Design principles

- Business rules live on the server, never only in the UI
- Isolation and permissions are designed in from day one
- Pricing and scores are validated on the backend, not trusted from the client

## Author

Built by **Jummy**, a backend-focused software engineer working with Python, Django, Celery, Redis, and PostgreSQL.

GitHub: [Rafiu-Olajumoke01](https://github.com/Rafiu-Olajumoke01)
