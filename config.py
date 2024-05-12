from os import environ

#TG Credentials
API_ID = int(environ.get('API_ID', ''))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')
FORCESUB = environ.get('FORCESUB', '')
SUPPORT = environ.get('SUPPORT', '@drwhitexbot') #USERNAME OF SUPPORT BOT/CONTACT BOT/SUPPORT GROUP FOR EX:- @SUPPORTBOT
ADMINS = environ.get("ADMINS", "1111214141,1646672520").split(",")
ADMIN_IDS = [int(admin.strip()) for admin in ADMINS]

#Database
DB_URI = environ.get('DB_URI', '')
DB_NAME = environ.get('DB_NAME', 'Pastes')
