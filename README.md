
# Motorcycle Rental & Workshop Application

The application allows users to book motorcycles and schedule appointments at the motorcycle workshop. Users can create accounts, browse available motorcycles, make reservations, and manage their data.

## Features

- User account creation and management
- Role division: super admin, rental admin, rental worker, workshop admin, 
  workshop worker, user
- Motorcycle reservations
- Scheduling appointments at the motorcycle workshop


## Tech Stack

- Django (Python)
- PostgreSQL
- Docker
- HTML, CSS, JavaScript

## Running

### Requirements

- Installed Docker
- Installed Docker Compose

### Instructions

1. Clone this repository: `git clone https://github.com/dominowr/bike_rental.git`
2. Navigate to the project directory: `cd bike_rental`
3. Copy the `.env.example` file to `.env` and adjust the configuration as needed
4. Run Docker Compose: `docker compose up -d`
5. The application will be available at [http://localhost:8000/](http://localhost:8000/)

### Database Migrations

After the first run, perform database migrations:

```
docker compose exec web python manage.py migrate
```

### Create Superuser(optional)

If you want to create a superuser account (admin), use the following command and follow the instructions:

```
docker compose exec web python manage.py createsuperuser
```

## Authors

- [@dominowr](https://www.github.com/dominowr)

