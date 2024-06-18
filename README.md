# NOVA

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)

## Prerequisites

Ensure you have the following installed before proceeding:

- Python 3.x
- Django (specified version, e.g., Django 4.0.2)
- Other dependencies as listed in `requirements.txt`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Anbazhagan4281/Nova_backend.git
   cd your-repository


2. **Set up a virtual environment:**
	```bash
	python -m venv venv
	source venv/bin/activate

3. **Install dependencies:**
	```bash
	pip install -r requirements.txt

4. **Database Setup:**
	Configure your database settings in settings.py. Example for PostgreSQL:
	```bash 
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': 'your_database_name',
			'USER': 'your_database_user',
			'PASSWORD': 'your_database_password',
			'HOST': 'localhost',
			'PORT': '5432',
		}
	}

Replace with your actual database details.

5. **Create Migrations:**
	```bash 
	python manage.py makemigrations

6. **Apply Migrations:**

	Apply the migrations to your database:

	```bash
	python manage.py migrate

7. **Run the development server:**
	```bash 
	python manage.py runserver
