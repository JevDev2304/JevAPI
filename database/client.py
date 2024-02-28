from pymongo import MongoClient
# Create a new client and connect to the server
db_client = MongoClient("mongodb+srv://admin:admin@cluster0.iguozyd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test
