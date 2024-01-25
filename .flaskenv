# Define name of python module to start
FLASK_APP=server

# change for production
FLASK_ENV=development
FLASK_DEBUG=True

# Define Secrets unique to your application (best to generate each)
SECRET_KEY=superAmazingSecretKey
JWT_SECRET_KEY=superAmazingJWTSecretKey

# How long an authorization is valid (in minutes)
JWT_ACCESS_TOKEN_EXPIRES=0.1
# How login an refresh is valid (in days)
JWT_REFRESH_TOKEN_EXPIRES=30

# Standard delay for job schedules (in seconds)
SCHEDULER_API_INTERVAL=1*24*60*60 # everday once

# Database uri
SQLALCHEMY_DATABASE_URI=sqlite:///app.db