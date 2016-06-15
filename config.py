# define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# defines the database we are working with
SQLALCHEMY_DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DB_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# CSRF
CSRF_ENABLED = True
CSRF_SESSION_KEY = 'supersecretkey'

# Cookie signing key

SECRET_KEY = "evenmoresecret"