from application import mongo


def find_user(email):
    result = mongo.db.my_collection.find_one({"email": email})
    return result


def add_new_user(all_values):
    result = mongo.db.my_collection.insert_one(all_values)
    return result


def update_verification(email):
    result = mongo.db.my_collection.update_one({"email": email}, {"$set": {"verified": True}})
    return result


def update_new_pass(email, new_password):
    result = mongo.db.my_collection.update_one({"email": email}, {"$set": {"password": new_password}})
    return result


# This is used to completely delete user info from our database but we can also soft delete which is used below to maintain the info
# def delete_user(email):
#     result = mongo.db.my_collection.delete_one({"email": email})
#     result = True if result.acknowledged else False
#     return result


def soft_delete(email):
    result = mongo.db.my_collection.update_one({"email": email}, {"$set": {"verified": False}})
    return result
