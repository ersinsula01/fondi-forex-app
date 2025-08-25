FondiForex - Transparency Platform
A complete full-stack application built to manage an investment fund (Forex) and provide complete transparency to investors. Users can register, view fund performance, invest amounts, and track the profit or loss of their investments in real time.

Key Features
User Authentication: Full registration and login system using JSON Web Tokens (JWT).

Public Fund Listing: All visitors can see active funds and their descriptions.

Personal Investor Dashboard: Logged in users can see a detailed list of their personal investments.

Profit/Loss Calculation: Automatic calculation of the current investment value and profit/loss based on the latest fund quota value.

Making Investments: Logged-in users can invest certain amounts in selected funds through a modal interface.

Modern Interface: Clean and responsive interface built with Bootstrap.

Powerful Backend: Secure and scalable API built with Django and the Django REST Framework.

Technologies Used
Backend:

Python

Django

Django REST Framework

djangorestframework-simplejwt (for JWT authentication)

Frontend:

HTML5

CSS3

JavaScript (Vanilla JS, ES6+)

Bootstrap 5

Database:

SQLite3 (for local development)

Installation and Local Usage
To run this project on your computer, follow these steps:

Clone the Repository:

Bash

git clone https://github.com/ersinsula01/fondi-forex-app.git

cd fondi-forex-app
Create and Activate the Virtual Environment:

Bash

python -m venv venv
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate
Install Required Libraries:

Bash

pip install -r requirements.txt
Apply Database Migrations:

Bash

python manage.py migrate
Create a Super User (Admin):

Bash

python manage.py createsuperuser
Start the Backend Server (Django):

Bash

python manage.py runserver
The backend will be active at http://127.0.0.1:8000/.

Start the Frontend Server:

Open a second terminal in the same folder and run:

Bash

python -m http.server 8001
The frontend will be active at http://127.0.0.1:8001/.

API Endpoints
Endpoint Method Description Requires Authentication?

POST /api/token/ Gets a JWT token by providing username/password. No
POST /api/registrohu/ Creates a new user. No
GET /api/fondet/ Lists all public funds. No
GET /api/investimet-e-mia/ Lists the user's personal investments. Yes
POST /api/invest/ Creates a new investment transaction. Yes

