from pymongo import MongoClient

mongo_url = "mongodb+srv://aditya:mongopass@cluster0.vjvcgdn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_url)
db = client.blog
