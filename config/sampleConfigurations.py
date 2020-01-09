from datetime import timedelta
# Database Configurations
HOST = ####
USER = ####
PASSWORD = ####
DATABASE = ####
CHARSET = ####
TIMEOUT = ####

# Secret Key
SECRET = ####

# JWT
JWT_URL = #### e.g. '/login' default URL is '/auth'
JWT_USERNAME_KEY = #### e.g. 'email' if you wish to use email key instead of username
JWT_EXPIRATION_TIME = #### e.g. timedelta(seconds=60*60*1) for 1 Hour