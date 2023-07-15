from application import mongo


def find_user(email):
    result = mongo.db.UserCollection.find_one({"email": email})
    return result


def add_new_user(all_values):
    result = mongo.db.UserCollection.insert_one(all_values)
    return result


def update_verify(email):
    result = mongo.db.UserCollection.update_one(
        {"email": email}, {"$set": {"verified": True}}
    )
    result = True if result.acknowledged else False
    return result


def update_new_pass(email, new_password):
    result = mongo.db.UserCollection.update_one(
        {"email": email}, {"$set": {"new_password": new_password}}
    )
    return result


def delete_user(email):
    result = mongo.db.UserCollection.delete_one({"email": email})
    return result
