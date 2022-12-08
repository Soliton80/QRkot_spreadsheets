[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/) [![badge](https://img.shields.io/badge/-FastApi-008080)](https://fastapi.tiangolo.com) [![badge](https://img.shields.io/badge/-Alembic-008080)](https://pypi.org/project/alembic/) [![badge](https://img.shields.io/badge/-Pydantic-008080)](https://pydantic-docs.helpmanual.io) [![badge](https://img.shields.io/badge/-GoogleApi-008080)](https://developers.google.com/apis-explorer/)

# Training project yandex.practicum  - application QRKot. Google Sheets report



## Project profile

The project implemented Google API integration in QRKot donation collection application. The possibility of forming a report in a Google table has been added. The table generates a list of closed projects, sorted by the speed of fundraising - from those that closed the fastest to those that took a long time to collect the required amount.


Donations
A user can make a donation and accompany it with a comment. Donations are made to the fund, not to a specific project. Every donation received is automatically added to the first open project that has not yet reached the required amount. If a donation exceeds the required amount or if there are no open projects in the fund, the remaining money is waiting for the next project to open. When you create a new project all uninvested donations are automatically put into the new project.

Users

Examples of API queries, response options, and errors can be found in the project documentation, available at http://127.0.0.1:8000/docs.

Targeted projects are created by superuser .
Registered users can send donations and view a list of their donations.

## Startup instructions

Clone the repository to your computer:

```
git@github.com:yandex-praktikum/QRkot_spreadsheets.git
```

In the root folder, create a virtual environment

```
python -m venv venv
```

Launch virtual environment

```
. venv/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

create file  ```QRkot_spreadsheets/.env```

example of .env file:

```
APP_TITLE=App QRKot
APP_DESCRIPTION=**Donation collection service to support kitties.**
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db 
SECRET=NqyCP8-cGyGat-uJOt2o
TYPE=service_account
PROJECT_ID="opportune-lore-369911"
PRIVATE_KEY_ID="1b30aa142b6ef92c824edcf6536e81e8092daaa5"
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvAIT+YUw==\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL="service-account@opportune-lore-369911.iam.gserviceaccount.com"
CLIENT_ID="112473947934508090513"
AUTH_URI="https://accounts.google.com/o/oauth2/auth"
TOKEN_URI="https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/service-account%40opportune-lore-369911.iam.gserviceaccount.com"
EMAIL=email@gmail.com

```
## Connect the database, make migrations.

```
alembic init
alembic revision --autogenerate 
alembic upgrade head
```
## Create superuser.

To do this in any database manager, connect to the created database fastapi.db, change the status of the normal user is_superuser = 1

## Launch server

```
uvicorn app.main:app --reload 

```
### Author

- [Sukharev Kirill](https://github.com/Soliton80)
