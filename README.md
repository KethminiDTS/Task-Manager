📋 Task Manager Web Application

A role-based daily task management system for employees and a centralized dashboard for managers — built with Django, Bootstrap, and SQLite.

🚀 Features

👩‍💼 For Employees:
Submit daily task updates via a clean web form
View, edit, and delete their own tasks
Form supports features like:
  Date picker
  Status options (WIP, DONE, HOLD)

🧑‍💼 For Manager:

View all submitted employee tasks in a dashboard
Filter tasks by:
  Date
  Employee
Export:
  All tasks
  Filtered tasks (CSV)
View, edit, or delete any registered employee
Single manager login allowed

⚙️ Technologies Used

Backend: Django (Python 3.10+)
Frontend: HTML, CSS, Bootstrap 5
Database: SQLite (default)
CSV Export: Built-in Django StreamingHttpResponse

🛠️ How to Run Locally

Clone the repository:
  git clone https://github.com/yourusername/task-manager.git
  cd task-manager

Create and activate virtual environment:
  python3 -m venv venv
  source venv/bin/activate

Install dependencies:
  pip install -r requirements.txt

Apply migrations:
  python manage.py migrate

Run the development server:
  python manage.py runserver 8001

Access the app:
  Open in your browser: http://127.0.0.1:8001/


📌 Future Enhancements

Email reminders for employees
Weekly task summaries
Multi-manager support
Role-based permissions using Django Groups

🧑‍💻 Author
Kethmini Rupasinghe
