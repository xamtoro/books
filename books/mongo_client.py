from pymongo import MongoClient
from django.conf import settings

# Initialize the MongoDB client using the URI from Django settings
client = MongoClient(settings.MONGO_URI)

# Access the specific database configured in Django settings
db = client[settings.MONGO_DB_NAME]
users_collection = db['users']