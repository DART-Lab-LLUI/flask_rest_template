# Flask RESTFUL template

This template provides a setup to easily develop RESTFUL servers.
It implements following features:

### Security

- User Management Backend (http://localhost:5000)
    - Add, Delete, Password reset
    - Block authorization (Tokens)
    - https://flask.palletsprojects.com/en/3.0.x/
    - https://flask-login.readthedocs.io/en/latest/
- JWT Authorization
    - Is used to authorize clients with user credentials
    - https://flask-jwt-extended.readthedocs.io
- Role-based access restrictions
    - restricting access based on roles
    - using decorators
    - https://pythonbasics.org/decorators/
- Access-log
    - Needed for sensitive data
    - Every request will be logged with username and IP

### Database

- Object–relational mapping (ORM)
    - Helpful tool to use database table in objects
    - Mapping Classes to Data Table
    - https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
- Database migration
    - Easy set-up of databases
    - https://flask-migrate.readthedocs.io/en/latest/#

### Webservice

- Blueprints
    - Flasks method to split functionalities
    - https://flask.palletsprojects.com/en/3.0.x/blueprints/
- FlaskRESTful
    - Clean structure of functionalities
    - Parting / validation of input data
        - https://flask-restful.readthedocs.io/en/0.3.8/reqparse.html
    - Serialization of output data
        - https://flask-restful.readthedocs.io/en/0.3.8/fields.html
    - https://flask-restful.readthedocs.io/en/0.3.8/index.html

### Examples

- Simple example of storing Patient measurement data
    - can be found in server/main.py and server/models/main.py
- Simple example for a client
    - found in client/login.py

### Diverse

- Scheduling of tasks
    - Used to frequently clean-up database
    - https://github.com/furqonat/flask-scheduler

## Folder Structure

```
flask_rest_template
|   .flaskenv             # Environment variables
|   requirements.txt      # Librarie requirements
|
+---migrations            # set-up from flask-migrate
|   |   alembic.ini
|   |   env.py
|   |   README
|   |   script.py.macko
|   +----versions         # Migration scripts
|    
+---server
    |   config.py         # Flask environment config loader
    |   extensions.py     # Globally accessable extension objects
    |   utils.py          # Helpful functions
    |   __init__.py       # Flask Factory (create_flask function)
    |
    +---auth              # Contains all files for JWT login
    |     decorator.py    # JWT role checker
    |     routes.py       # login routes
    |     utils.py        # auth help functions
    |     __init__.py     # Contains blueprint for auth
    |
    +---main              # Contains tempolate application routs
    |     patient_routes.py
    |     __init__.py     # Contains blueprint for main
    |
    +---models            # Stores all flask-sqlalchemy models
    |     auth.py         # User Model for user-management & RESTFUL JWT Autehtification
    |     main.py         # Models for main application
    |     log.py          # Models for Access Log
    |     __init__.py
    |
    +---static            # Static files for Webpage
    |     style.css
    |
    +---templates         # Flask html templates. Contains Pages for user-management
    |     login.html      
    |     set_password.html
    |     tokens.html
    |     user_management.html
    |
    +---user_mng          # Contains routes and decorators for user-management page
          decorator.py    
          routes.py
          __init__.py
```

## Local Usage

Install requirements

```shell
# create venv
$ python -m venv venv
# activate venv
$ venv\Scripts\activate

# Install libraries
$ pip install -r requirements.txt
# Install database
$ flask db upgrade
```

Start the application with

```shell
$ flask run
```

## Docker usage
1 Install docker

2 Download source
````shell
$  git clone git@github.com:cereneo-foundation/flask_rest_template.git
````
3 Access folder
````shell
$ cd flask_rest_template/
````
4 Build docker artefact 
````shell
$ docker build -t flask-rest .
````
5 Run docker composition
````shell
$ docker compose up -d
````

## General development

After coping this template to your github you are ready to adapt this service to your needs.
The main functionalities of your application will be lying in two places.

1. server/models/main.py
    * Here you can add DataObjects for ORM
2. server/main
    * Here are your routes, utils and other functionalities store

### Adding Functionalities

For RESTFul Webservices it is important that you design your Applications concerning objects.
Lets imaging we have Patient which has frequent appointments.
We therefore have two objects "Patient" and "Appointment", and decide we only need to access Patient data
Lets create a new file server/main/ and call it "patient_routes.py"

````python
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from server.auth.decorator import role_required
from server.main import api_bp


class PatientApi(Resource):
    @jwt_required()
    @role_required(["user"])
    def get(self, user_id):
        return {"name": "Harald", "surname": "Meier"}

    @jwt_required()
    @role_required(["user"])
    def put(self, user_id):
        return {"name": "Harald", "surname": "Meier"}


api_bp.add_resource(PatientApi, '/patient/<user_id>')
````

@jwt_required() is necessary to enforce clients to be logged in.
With @roles_required we restrict access to users in the group "role"
The "role_name" corresponds to the column "name" in the table "role". Check out the class server.models.auth.Role.
Roles can be assigned to users in the user-management webpage when flask is started

with api_bp.add_resource(PatientApi, '/patient/<user_id>') we route all requests from <host>/api/patient/<Any> to the
Class
Next thing we need are DataObjects

### Adding DataObjects

Lets start to add database objects:

````python
from server.extensions import db


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Double)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68))
    surname = db.Column(db.String(68))
    appointments = db.relationship('Appointment', backref='patient')
````

Every Class inheriting db.Model will have a table object. This object will be used to define a table in the database and
manipulate it's data.
In class Appointment we defined the attribute patient_id with a foreign key to the table patient.
Further we defined the attribute appointments in Patient to easily access all the appointments which belongs to the
patient
use https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/ for explanations

To install the new objects into the database we need to use flask-migration in the terminal

````shell
$ flask db migrate -m "Add Appointments"
$ flask db upgrade
````

This will firstly create a new file in /migrations/versions and then update your local database.
To add initial data you can edit this file and reinstall the database.

### Marshalling

Now we can adapt the PatientApi to acces the database

````python
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from server.auth.decorator import role_required
from server.main import api_bp
from server.models.main import Patient


class PatientApi(Resource):
    @jwt_required()
    @role_required(["user"])
    def get(self, user_id):
        patient = Patient.query.get_or_404(user_id)
        return {"name": patient.name, "surname": patient.surname}

    @jwt_required()
    @role_required(["user"])
    def put(self, user_id):
        return {"name": "Harald", "surname": "Meier"}


api_bp.add_resource(PatientApi, '/patient/<user_id>')
````

Since it's quite annoying to mapp all the attributes into a dictionary we can add a description of the DataObject to
Patient

````python
from server.extensions import db
from flask_restful import fields


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Double)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    @classmethod
    def get_fields(cls) -> dict:
        return {
            'id': fields.Integer,
            'date': fields.Float,
        }


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68))
    surname = db.Column(db.String(68))
    appointments = db.relationship('Appointment', backref='patient')

    @classmethod
    def get_fields(cls) -> dict:
        return {
            'id': fields.Integer,
            'name': fields.String,
            'surname': fields.String,
            'appointments': fields.List(fields.Nested(Appointment.get_fields()))
        }
````

Fields are part of the flask-restful library to easify the mapping of response objects.
Lets incorporate them into our PatientApi
````python
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from server.auth.decorator import role_required
from server.main import api_bp
from server.models.main import Patient


class PatientApi(Resource):
    @jwt_required()
    @role_required(["user"])
    @marshal_with(Patient.get_fields())
    def get(self, user_id):
        patient = Patient.query.get_or_404(user_id)
        return patient

    @jwt_required()
    @role_required(["user"])
    def put(self, user_id):
        patient = Patient.query.get_or_404(user_id)
        return patient


api_bp.add_resource(PatientApi, '/patient/<user_id>')
````

With the @marshal_with decorator we define the fields of the class Patient to map into a Dictionary. So we now can
return patient objects directly.

### Request parsing

So last thing missing. We need to update patient in the database in the put request.
So ensure input data quality we now have to once again define the patient class.

````python
from server.extensions import db
from flask_restful import fields, reqparse


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Double)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    @classmethod
    def get_fields(cls) -> dict:
        return {
            'id': fields.Integer,
            'date': fields.Float,
        }


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68))
    surname = db.Column(db.String(68))
    appointments = db.relationship('Appointment', backref='patient')

    @classmethod
    def get_fields(cls) -> dict:
        return {
            'id': fields.Integer,
            'name': fields.String,
            'surname': fields.String,
            'appointments': fields.List(fields.Nested(Appointment.get_fields()))
        }

    @classmethod
    def get_parser(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        return parser
````

The request parser helps us to parse and check the data received from the client.
After parsing we will get a dictionary with all the data from the client and map it manually to the object. The parser
fails the client will receive an error message.

````python
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from server.auth.decorator import role_required
from server.main import api_bp
from server.models.main import Patient
from server.extensions import db


class PatientApi(Resource):
    @jwt_required()
    @role_required(["user"])
    @marshal_with(Patient.get_fields())
    def get(self, user_id):
        patient = Patient.query.get_or_404(user_id)
        return patient

    @jwt_required()
    @role_required(["user"])
    @marshal_with(Patient.get_fields())
    def put(self, user_id):
        parser = Patient.get_parser()
        args = parser.parse_args()
        patient = Patient.query.get_or_404(user_id)
        patient.name = args['name'] or patient.name
        patient.surname = args['surname'] or patient.surname
        patient.birthday = args['birthday'] or patient.birthday
        patient.comments = args['comments'] or patient.comments
        db.session.commit()
        return patient


api_bp.add_resource(PatientApi, '/patient/<user_id>')
````
Well done!

### Client authorization

The client has to login first with valid credentials.

````python
import requests

response = requests.post(
    'http://localhost:5000/api/auth/',
    headers={"Content-Type": "application/json"},
    json={"username": "client", "password": "123456"}
)
````

After successful login you will receive an access_token and a request_token which are valid for the configurated time
period.

````python
{'access_token': 'eyJhbGciOiJIUzI1NiIsInR5', 'refresh_token': 'erasdgafg'}
````

The access_token needs to be added in the header of every restricted request, to authorize the request.

````python
import requests

response = requests.get('http://localhost:5000/api/patient/1',
                        headers={"Authorization": "Bearer " + access_token,
                                 "Content-Type": "application/json"})
````

Please note the dictionary key has to be "Authorized" and the toke has to be prefixed with "Bearer ".

If the access_token is expired you will receive the status code 401 and following response.

````python 
{'msg': 'Token has expired'}
````

You can than refresh the authorization and receive a new access_token which will again be valid in the configured
time-period.

````python
import requests

response = requests.get('http://localhost:5000/api/auth/',
                        headers={"Authorization": "Bearer " + refresh_token,
                                 "Content-Type": "application/json"})
````

If the refresh_token is expired you will once again receive a message and have to login

````python 
{'msg': 'Token has expired'}
````

After business is done you can logout using the refresh_token

````python
import requests

response = requests.delete('http://localhost:5000/api/auth/',
                           headers={"Authorization": "Bearer " + refresh_token,
                                    "Content-Type": "application/json"})
````


