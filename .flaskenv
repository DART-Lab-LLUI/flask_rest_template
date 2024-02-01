# Define name of python module to start
FLASK_APP=server

# change for production
FLASK_ENV=development
FLASK_DEBUG=1

# Define Secrets unique to your application (best to generate each)
FLASK_SECRET_KEY=superAmazingSecretKey
FLASK_JWT_SECRET_KEY=superAmazingJWTSecretKey

# How long an authorization is valid (in minutes)
FLASK_JWT_ACCESS_TOKEN_EXPIRES=0.3
# How login an refresh is valid (in days)
FLASK_JWT_REFRESH_TOKEN_EXPIRES=30

# Database uri
FLASK_SQLALCHEMY_DATABASE_URI=sqlite:///app.db