from os import environ

#TG Credentials
API_ID = int(environ.get('API_ID', '1379638'))
API_HASH = environ.get('API_HASH', '4eba7cf1672380503a8a3cd94e102980')
BOT_TOKEN = environ.get('BOT_TOKEN', '1643063196:AAGC6GEMLlBGA7eQa2k-EujWgaBd5N3Nq20')
FORCESUB = environ.get('FORCESUB', '-1001313593468')
SUPPORT = environ.get('SUPPORT', '@drwhitexbot') #USERNAME OF SUPPORT BOT/CONTACT BOT/SUPPORT GROUP FOR EX:- @SUPPORTBOT
ADMINS = environ.get("ADMINS", "1111214141,1646672520").split(",")
ADMIN_IDS = [int(admin.strip()) for admin in ADMINS]

#Database
DB_URI = environ.get('DB_URI', 'mongodb+srv://ForwardBot:NQ7uGG5pDDntRmB9@testbot0586.0n9hhr6.mongodb.net/?retryWrites=true&w=majority&appName=testbot0586')
DB_NAME = environ.get('DB_NAME', 'Pastes')