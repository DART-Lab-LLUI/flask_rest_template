# Flask RESTFUL template

This template provides a setup to easily develop RESTFUL servers.
It implements following features:

- Web based user management http://localhost:5000/ (https://flask-login.readthedocs.io/en/latest/)
- JWT based authorization for RESTFUL requests (https://flask-jwt-extended.readthedocs.io)
- Role-based access restrictions for REST and WEB with decorators
- Database migration (https://flask-migrate.readthedocs.io/en/latest/#)
- Schedules (https://viniciuschiele.github.io/flask-apscheduler/)
- Template application for Patient-Measurement data
- Template user-management as webpage (https://flask-wtf.readthedocs.io/en/1.2.x/)
- Simple client example to login and retrieve data from RESTFUL service


## Folder Structure

```
flask_rest_template
|   .flaskenv             # Environment variables
|   requirements.txt      # Libraries
|
+---server
    |   config.py         # Flask environment config loader
    |   extensions.py     # Globally accessable extension objects
    |   __init__.py       # Flask Factory (create_flask function)
    |
    +---auth              # Contains all files for JWT login
    |     decorator.py    # JWT role checker
    |     routes.py
    |     __init__.py     # Contains blueprint for auth
    |
    +---main              # Contains tempolate application routs
    |     appointment_routes.py
    |     measure_routes.py
    |     patient_routes.py
    |     __init__.py     # Contains blueprint for main
    |
    +---models            # Stores all flask-sqlalchemy models
    |     auth.py         # User Model for user-management & RESTFUL JWT Autehtification
    |     main.py         # Models for main application
    |     utils.py        # Helpful utils the easy RESTFUL develompment
    |     __init__.py
    |
    +---static            # Static files for Webpage
    |     style.css
    |
    +---templates         # Flask html templates. Contains Pages for user-management
    |     login.html      
    |     set_password.html
    |     user_management.html
    |
    +---user_mng          # Contains routes and decorators for user-management page
          decorator.py    
          routes.py
          __init__.py
```

## Usage

Install requirements

```shell
# Install libraries
$ pip install -r requirements.txt
# Install database
$ flask db ugrade
```

Start the application with

```shell
flask run
```

After successful starting of the server you have to initialize the database.
Use your broswer and request http://localhost:5000/init
The rest will handle flask.

## Using authorization

Enforce login for a RESTFUL request can be achieved with @jwt_required() decorator.
class Patient:
pass

````python
from flask_jwt_extended import jwt_required
from server.models.main import Patient
from server.main import bp


@jwt_required()
@bp.route('/appointment/<int:appointment_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return patient.to_dict()
````

The client has to login first with valid credentials.

````python
import requests

response = requests.post(
    'http://localhost:5000/api/auth/login',
    headers={"Content-Type": "application/json"},
    json={"username": "both", "password": "1234"}
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

response = requests.get('http://localhost:5000/api/patient/',
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

response = requests.get('http://localhost:5000/api/auth/refresh',
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

response = requests.delete('http://localhost:5000/api/auth/logout',
                        headers={"Authorization": "Bearer " + refresh_token, 
                                 "Content-Type": "application/json"})
````
## Using roles

With the decorator @role_required("role_name") requests can be restricted to roles of the user

````python
from flask_jwt_extended import jwt_required
from server.models.main import Patient
from server.main import bp
from server.auth.decorator import role_required


@jwt_required()
@role_required(["user"])
@bp.route('/appointment/<int:appointment_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return patient.to_dict()
````

The "role_name" corresponds to the column "name" in the table "role". Check out the class server.models.auth.Role.
Roles can be assigned to users in the user-management webpage when flask is started