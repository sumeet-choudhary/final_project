from application import mongo


def find_user(email):
    result = mongo.db.UserCollection.find_one({"email": email})
    return result


def add_new_user(all_values):
    try:
        result = mongo.db.UserCollection.insert_one(all_values)
        return result
    except Exception as e:
        print(str(e))


def update_verify(email):
    try:
        result = mongo.db.UserCollection.update_one({"email": email}, {"$set": {"verified": True}})
        result = True if result.acknowledged else False
        return result
    except Exception as e:
        return str(e)
