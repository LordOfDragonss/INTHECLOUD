from pymongo_get_database import get_database
dbname = get_database()

collection_name = dbname["user_1_items"]

item_details = collection_name.find()
for item in item_details:
    print(item['item_name'], item['category'])