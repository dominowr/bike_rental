
# Motorcycle Rental & Workshop Application

This is a fully functional web application which allows Users to book motorcycles and schedule appointments at the motorcycle workshop.   
Users can create accounts, browse all motorcycles with filtering, make reservations and manage their data.

## Features

- User account creation and data management
- Motorcycle reservations
- Scheduling appointments at the motorcycle workshop
- Filtering:
  - Intuitive motorcycle filtering options for Users to find the perfect motorcycles, based on their type (sport/enduro/etc.) and engine capacity
- Date and time availability:
  - A user-friendly date picker to check availability of chosen motorcycle and workshop appointments. Unavailable dates are blocked in picker.
-Automated email notifications:
  - Users receive account activation link after registrations
  - User receive detailed confirmation emails after making or updating a reservations, containing all relevant information
  - Automated email notifications are sent to admin email account when users modify or delete their reservation



## Tech Stack

- Django (Python)
- PostgreSQL
- Django REST framework
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



## API Reference

### Open Endpoints:
Open endpoints require no Authentication:



### * User Registration:   

   
Used to register a new User.

URL: ```/api/users/registration/```.  
Method: ```POST```.  
   
Data example:
```json
{
    "username": "theKing",
    "first_name": "Aragorn",
    "last_name": "SonOfArathorn"
    "email": "aragorn@minastirith.com",
    "password": "Anduril!1",
    "password2": "Anduril!1",
}
```
Optional fields:
```json
{
    "last_name": ,
    "phone_no":
}
```
Example usage:
```
http POST http://127.0.0.1:8000/api/users/registration/ \
  username=theKing \
  first_name=Aragorn \
  last_name=SonOfArathorn \
  email=aragorn@minastirith.com \
  password='Anduril!1' \
  password2='Anduril!1'
```
#### Success Response:
Code: ```201 CREATED```   

Content example:   
```json
{
    "email": "aragorn@minastirith.com",
    "first_name": "Aragorn",
    "last_name": "SonOfArathorn",
    "phone_no": null,
    "username": "theKing"
}

```

#### Error Response   
Condition: If 'username' or 'email' are not unique.   
Code: ```400 BAD REQUEST```


Content example:
```json
{
    "email": [
        "user with this email already exists."
    ],
    "username": [
        "A user with that username already exists."
    ]
}

```

Condition: If 'password' not equal 'password2'.   
Code: ```400 BAD REQUEST```


Content example:
```json
{
    "non_field_errors": [
        "The two password fields did not match."
    ]
}

```
___
### * Show list of all Motorcycles:   

   
Endpoint returns list of all motorcycles that are available for rent with all information.

URL: ```/api/motorcycles/```  
Method: ```GET```  

   
#### Success Response:
Code: ```200 OK```   
Content example:
```json
{
    "capacity": 750,
    "category": "Enduro",
    "description": "Yamaha SuperTener beautiful motorcycle.",
    "engine": "parallel twin",
    "fuel_capacity": 23,
    "id": 3,
    "image": "http://127.0.0.1:8000/media/images/rental/yamaha-supertenere.jpeg",
    "model": "Yamaha XTZ750 Super Ténéré",
    "rental_price": "250.00",
    "slug": "yamaha-xtz750-super-tenere",
    "top_speed": 180,
    "torque": 89,
    "wet_weight": 190,
    "year": 1989
}


```
___
### * Show list of all Services:   

   
Endpoint returns list of all services provides by workshop.

URL: ```/api/services/```  
Method: ```GET```  

   
#### Success Response:
Code: ```200 OK```   
Content example:
```json
{
    "description": "Carburetors cleaning, beautiful carburetors. Lorem ipsum.",
    "id": 1,
    "name": "Carburetors cleaning",
    "price": 100
}
```

### SuperUser Authentication Endpoints:
Endpoints that required superuser permission:

### * Show list of all registered Users:   

   
Used to collect a list of all registered Users with motorcycles and services reservation lists.

URL: ```/api/users/```  
Method: ```GET```  
Authorization: __SuperUser__  
Example usage:
```
http GET http://127.0.0.1:8000/api/users/ 'Authorization: Token YourSecretTokenMrBaggins'
```
#### Success Response:
Code: ```200 OK```   

Content example:   
```json
 {
    "email": "frodo@baggins.com",
    "first_name": "Frodo",
    "id": 2,
    "motorcyclereservation_set": [
        1
    ],
    "servicereservation_set": [],
    "username": "frodo"
}

```

#### Error Response   
Condition: If User don't have a SuperUser role.   
Code: ```403 FORBIDDEN```


Content example:
```json
{
    "detail": "You do not have permission to perform this action."
}

```
Condition: If User is not authenticated.   
Code: ```401 UNAUTHORIZED```


Content example:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

___


### * Add New Motorcycle:
Used to add a new motorcycle to the rental.

URL: ```/api/motorcycles/add/```  
Method: ```POST```
Authorization: __SuperUser__   
Code: ```201 CREATED```

Data constraints:
```json
{
    "capacity": 750,
    "category": "Enduro",
    "description": "Yamaha SuperTener beautiful motorcycle.",
    "engine": "parallel twin",
    "fuel_capacity": 23,
    "image": "http://127.0.0.1:8000/media/images/rental/tenere750_x1HEUaD.png",
    "model": "Yamaha XTZ750 Super Ténéré",
    "rental_price": "250.00",
    "slug": "yamaha-xtz750-super-tenere",
    "top_speed": 180,
    "torque": 89,
    "wet_weight": 190,
    "year": 1989
}
```
Example usage:
```
http -form POST http://127.0.0.1:8000/api/motorcycles/add/ 'Authorization: Token YourSecretTokenMrBaggins' \
  capacity=750 \
  category=Enduro \
  description="Yamaha SuperTener beautiful motorcycle." \
  engine="parallel twin" \
  fuel_capacity=23 \
  image@/Users/gandalf/Desktop/supertenere-750.jpeg \
  model="Yamaha XTZ750 Super Ténéré" \
  rental_price="250.00" \
  slug="yamaha-xtz750-super-tenere" \
  top_speed=180 \
  torque=89 \
  wet_weight=190 \
  year=1989
```
TBC

___
Endpoints for user authentication will be continued: 
### * User Login:   

   
Used to collect a Token for registered User.

URL: ```/api/api-token-auth/```.  
Method: ```POST```.  
   

#### Success Response:
Code: ```200 OK```   

Content example:   
```
http POST http://127.0.0.1:8000/api/api-token-auth/ \
  username=classic_boromir \
  password=SonOfDenethor
```

#### Error Response   
Condition: If 'username' or 'password' combination is wrong.   
Code: ```400 BAD REQUEST```


Content example:
```json
{
    "non_field_errors": [
        "Unable to login with provided credentials."
    ]
}
```

## Authors

- [@dominowr](https://www.github.com/dominowr)

