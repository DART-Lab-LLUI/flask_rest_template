# Flask RESTFUL template 
This template provides a setup to easily develop RESTFUL servers. 
It implements following features:
- Webbased user management http://localhost:5000/ (https://flask-login.readthedocs.io/en/latest/)
- JWT based authorization for RESTFUL requests (https://flask-jwt-extended.readthedocs.io)
- Role-based access restrictions for REST and WEB with decorators
- Template application for Patient-Measurement data
- Template user-management as webpage (https://flask-wtf.readthedocs.io/en/1.2.x/)
- Simple client example to login and retrieve data from RESTFUL service

## Folder Structure
```
server
|   config.py         # Flask environment config storage
|   extension.py      # Globally accessable extension objects
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
pip install -r requirements.txt
```
Start the application with 
```shell
flask --app server run --debug
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
    'http://localhost:5000/api/auth/',
    headers={"Content-Type": "application/json"},
    json={"username": "both", "password": "1234"}
)
````
After successfull login you will receive a token which is valid for certain time period.
````python
{'access_token': 'eyJhbGciOiJIUzI1NiIsInR5'}
````
This token needs to be added in the header of every restricted request, to authorize the request.
````python
import requests

response = requests.get(
    'http://localhost:5000/api/patient/',
    headers={"Authorization": "Bearer " + json_response["access_token"], 
             "Content-Type": "application/json"}
)
````

Please note the dictionary key has to be "Authorized" and the toke has to be prefixed with "Bearer "

## Using roles
With the decorator @role_required("role_name") requests can be restricted to roles of the user
````python
from flask_jwt_extended import jwt_required
from server.models.main import Patient
from server.main import bp
from server.auth.decorator import role_required

@jwt_required()
@role_required("user")
@bp.route('/appointment/<int:appointment_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return patient.to_dict()
````

The "role_name" corresponds to the column "name" in the table "role". Check out the class server.models.auth.Role.
Roles can be assigned to users in the user-management webpage when flask is started