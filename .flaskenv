FLASK_APP=server

# change for production
FLASK_ENV=development
FLASK_DEBUG=True

# Define Secrets unique to your application (best to generate each)
SECRET_KEY=superAmazingSecretKey
JWT_SECRET_KEY=superAmazingJWTSecretKey
SALT=superAmazingSalt

# How long an authorization is valid (in minutes)
JWT_ACCESS_TOKEN_EXPIRES=30
# How login an refresh is valid (in days)
JWT_REFRESH_TOKEN_EXPIRES=30

# Database uri
SQLALCHEMY_DATABASE_URI=sqlite:///../app.db