# Service Desk Ticket Management & SLA Analytics System

Academic project starter for MSc Computer Applications (Semester 3). Built with Python, Django, SQLite, Bootstrap and Chart.js.

## Features
- Authentication using Django's built-in user system
- Ticket create/read/update/delete (CRUD)
- Priority, status, category, requester and assignee fields
- SLA due-time calculation based on priority
- Dashboard with ticket status, priority and category charts
- Search/filter and CSV export
- Ticket comments/update notes
- Django admin and automated tests

## SLA rules used in this academic prototype
- Critical: 4 hours
- High: 8 hours
- Medium: 24 hours
- Low: 72 hours

These are illustrative project rules, not an industry standard. The prototype measures elapsed clock hours, not business hours or contractual SLA rules.

## Setup (Windows PowerShell)
1. Install Python 3.11+ from python.org and tick **Add Python to PATH**.
2. Extract the ZIP and open this folder in VS Code.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```
4. Install Django:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Create database tables:
   ```powershell
   python manage.py makemigrations tickets
   python manage.py migrate
   ```
6. Create an administrator:
   ```powershell
   python manage.py createsuperuser
   ```
7. Start the site:
   ```powershell
   python manage.py runserver
   ```
8. Visit `http://127.0.0.1:8000/`, sign in with your superuser account, and create sample tickets.
9. Admin interface: `http://127.0.0.1:8000/admin/`.

## Run tests
```powershell
python manage.py test
```

## Important implementation notes
- The first user who creates a ticket becomes its requester.
- Any active user can be selected as an assignee in this academic starter. Add role-based permissions before real deployment.
- Dashboard and export show all records to authenticated users. Restrict data by role before using with real organizational data.
- SLA logic is intentionally simple. If a ticket's priority changes after creation, the original due date remains; implement an explicit SLA recalculation policy if required.
- Do not use real employee, customer, payroll, or confidential support data in the academic demo.
- Before public deployment: set `DEBUG=False`, use environment variables for `SECRET_KEY`, configure allowed hosts, HTTPS, secure cookies, production database, backups and access controls.

## Suggested GitHub repository description
A Django web application for service request management, SLA tracking, operational dashboards, and CSV reporting.
