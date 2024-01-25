# Task Manager
This is a simple Task Manager Application for Mediusware Job Task. I have created it using Django and Django REST Framework.

## Features
- Unauthenticated user can open an account, view task in short form.
- Authenticated user can login, logout, view profile, update profile information, change password, reset password, see details task, complete task.
- Superuser or admin or staff can do all what an Authenticated user can. Also can add task, edit task, delete task. Also have by default super power that django admin gives.
- token-based authentication system.


## Deployment

The first thing to do is to clone the repository:

```bash
  git clone https://github.com/tanzid64/task-manager-mediusware.git
  cd task-manager-mediusware
```
Create a virtual environment to install dependencies in and activate it:

```bash
  python -m venv .venv
  .venv\Scripts\activate
```
Then install the dependencies:

```bash
  pip install -r requirements.txt
```
Create a file name .env in project folder. Use Posgresql as database, and gmail account as email account. Setup your .env as per the requirements.

Apply migrations:

```bash
  python manage.py migrate
```
Create an admin account:

```bash
  python manage.py createsuperuser
```
Start the django application::

```bash
  python manage.py runserver
```

That's it! You should now be able to see the demo application.
Browse:
- HomePage:  localhost:8000/
- Admin Panel:  localhost:8000/admin
- API: localhost:8000/api


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`
`EMAIL_HOST_USER`
`EMAIL_HOST_PASSWORD`
`DB_NAME`
`DB_USER`
`DB_PASSWORD`
`DB_HOST`
`DB_PORT`



## API Reference

#### Get all Tasks

* [Authentication](#auth)
  * Signup ```localhost:8000/api/accounts/register/```
  * Login ```localhost:8000/api/accounts/login/```
  * Logout ```localhost:8000/api/accounts/logout/```
  * Profile ```localhost:8000/api/accounts/profile/```
  * Change Password ```localhost:8000/api/accounts/password/change/```
  * Reset Password ```localhost:8000/api/accounts/register/```
  
* [CRUD Operations](#crud)
  * All Tasks ```localhost:8000/api/all_tasks/```
  * Create Task (admin user only) ```localhost:8000/api/all_tasks/```
  * Retrieve specific task ```localhost:8000/api/all_tasks/id/```
  * Update Task (admin user only) ```localhost:8000/api/all_tasks/id/```
  * Delete Task (admin user only)```localhost:8000/api/all_tasks/id/```

* [Filter Tasks](#filter)
  * ALL Filter ```localhost:8000/api/all_tasks/?priority=${''}&due_date=${''}&created_at=${''}&search=${''}```
  * Priority ```localhost:8000/api/all_tasks/?priority=${''}```
  * Created Date ```localhost:8000/api/all_tasks/?created_at=${''}```
  * Due Date ```localhost:8000/api/all_tasks/?due_date=${''}```
  * Search(title, description) ```localhost:8000/api/all_tasks/?search=${''}```


