from pymongo import MongoClient, collection

# client = MongoClient("mongodb://localhost:27017/Users")
# print(client)
# client.db.my_db.my_collection.insert_one({"Name": "Sumeet"})
# mongodb://localhost:27017/Users/UserCollection/insertOne({"Name": "Sumeet"})

my_document = client.db.UserCollection.insert_one({"Name": "ff"})
# print(a)
# def insert_in_colllection(email,etc):
#     find=find_email()


def add_new_user(email, password, verified, role):
    try:
        print(email, "l")
        result = mongo.db.my_collection.insert_one({"email": email, "password": password, "role": role, "verified": verified})
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))

