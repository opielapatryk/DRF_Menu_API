import pymongo


class MongoRepo:
    def __init__(self, configuration):
        client = pymongo.MongoClient(
            host=configuration["MONGODB_HOSTNAME"],
            port=int(configuration["MONGODB_PORT"]),
            username=configuration["MONGODB_USER"],
            password=configuration["MONGODB_PASSWORD"],
            authSource="admin",
        )

        self.db = client[configuration["APPLICATION_DB"]]

    def _create_dish_objects(self, dish_data):
        return {
            "_id": str(dish_data["_id"]),
            "id": dish_data["id"],
            "name": dish_data["name"],
            "description": dish_data["description"],
            "price": dish_data["price"],
        }

    def list(self):
        collection = self.db.dishes
        results = collection.find()
        dishes = [self._create_dish_objects(dish) for dish in results]
        return dishes
    
    def get(self,dish_id):
        collection = self.db.dishes
        dish = collection.find_one({'id': dish_id})
        if dish:
            result = self._create_dish_objects(dish)
            return result

    def post(self,dish):
        if dish['id'] > len(list(self.db.dishes.find())):
            self.db.dishes.insert_one(dish)
            return self.list()

    def put(self,dish):
        if dish['id'] <= len(list(self.db.dishes.find())):
            self.db.dishes.update_one(
                {"id": dish['id']},
                {"$set": dish}
            )

            return self.list()

    def patch(self, updated_fields,dish_id):
        if dish_id <= len(list(self.db.dishes.find())):
            update_query = {"$set": updated_fields}

            self.db.dishes.update_one(
                {"id": dish_id},
                update_query
            )

            return self.list()
        
    def delete(self,dish_id):
        if self.db.dishes.find_one({"id": dish_id}):
            self.db.dishes.delete_one({"id": dish_id})
            return self.list()
    