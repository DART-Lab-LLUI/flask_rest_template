# Define name of python module to start
FLASK_APP=server

# change for production
#FLASK_ENV=development
#FLASK_DEBUG=1
#PROPAGATE_EXCEPTIONS=1

# Define Secrets unique to your application (best to generate each)
SECRET_KEY=superAmazingSecretKey
JWT_SECRET_KEY=superAmazingJWTSecretKey

# How long an authorization is valid (in minutes)
JWT_ACCESS_TOKEN_EXPIRES=0.3
# How login an refresh is valid (in days)
JWT_REFRESH_TOKEN_EXPIRES=30

# Database uri
SQLALCHEMY_DATABASE_URI=sqlite:///app.db