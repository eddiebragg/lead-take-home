# Wayhome Lead Engineer take home test

## Background

Wayhome's core product is gradual homeownership. Our customers partner with an institutional investor to purchase a home with as little as 5% initial contribution. The customer (residential member) can purchase more of the property from the investor (fund member) through a transaction we call "staircasing".

Customers can make staircasing payments whenever they want but there are some rules with regards to the amount they can staircase at any given time...
- Minimum purchase of £50
- Increase of ownership share can't exceed 5% in one anniversary year (annual cap)
- Annual cap doesn't rollover

### Annual cap example

A Customer moves into their home on 30th September 2021. The house was purchased for £250,000 and the customer started with a 5% ownership share. The customer can make as many staircasing payments as they like before 30th September 2022 but the total ammount staircased can't cause their ownership share to go above 10%. The annual cap doesn't rollover - if the customer in this example only staircased up to 9% ownership before 30th September 2022 then they can only staircase up to a 14% ownership share before 30th September 2023.

## The task

### Backend element

With the above information in mind we want you to write an HTTP API to satisfy the following features...

```
Given I'm a residential member in a Wayhome partnership
When I request a summary of my partnerships current situation
Then I see the property address
And I see the the property value
And I see my current ownership share in percentage terms
And I see my current ownership share in monetary terms

Given I'm a residential member in a Wayhome partnership
When I attempt make a staircasing payment with an acceptable amount
Then I see that my ownership share has increased accordingly

Given I'm a residential member in a Wayhome partnership
When I attempt make a staircasing payment with an unacceptable amount
Then I see an error message explaining why staircasing payment can't be accepted
```

The API should be written in python but you can use any framework you like. We'd like to see some form of data persistence and some test coverage.

### Frontend element

To demonstrate frontend ability we'd like to see a simple React app that consumes the endpoints implemented in the backend part of the task. The images below are rough guide for what we are looking for but you definitely shouldn't go to any effort to match the styles or make it look pretty.

![Main wireframe](/wireframes/1.png)
![Wireframe showing error](/wireframes/2.png)
![Wireframe showing success](/wireframes/3.png)

## Documentation & other instructions

Please append to this README any documentation you think appropriate. As a minimum we will need instructions on how we can run your API, frontend app and tests.


## Backend

The backend uses the Django Rest Framework and an SQLite database

### Dependecies

- Python (3.6, 3.7, 3.8, 3.9, 3.10)

### Install Virtual Env

To install the Virtual Env do the following commands

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Set up the DB

To set up the database with tables, superuser and fixtures.

```
cd homeownership
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/fixtures.json
```

### Run the Django dev server

`python manage.py runserver`

When running you will be able to see the API at http://localhost:8000/api/properties/1/

Use the Django Admin using your superuser login at
http://localhost:8000/admin

### Run tests

To run the tests

`python manage.py test api/tests`

## Frontend

The Frontend uses NextJS v14 and React v18

### Dependecies

- Node.js 18.17 or later.

## Running the NextJS server

```
cd frontend/homeownership
npm run dev
```

Go to http://localhost:3000/property/1 to view the page.
