from domain.entities.dish import Dish
import psycopg2

class PostgresRepo:
    def __init__(self, configuration):
        self.user = configuration['POSTGRES_USER']
        self.password = configuration['POSTGRES_PASSWORD']
        self.hostname = configuration['POSTGRES_HOSTNAME']
        self.port = configuration['POSTGRES_PORT']
        self.db = configuration['APPLICATION_DB']

    def execute_query(self, query, args=None):
        with psycopg2.connect(user=self.user, password=self.password, host=self.hostname, port=self.port, dbname=self.db) as conn:
            with conn.cursor() as cursor:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
    
    def _create_dish_object(self, results):
        return [
            Dish(
                id=result[0],
                name=result[1],
                description=result[2],
                price=result[3],
            )
            for result in results
        ]
    
    def list(self):
        query = "SELECT id, name, description, price FROM dishes;"
        results = self.execute_query(query)
        return self._create_dish_object(results)
    

    def get(self, id):
        query = "select id,name,description,price from dishes where dishes.id = {}".format(id)
        results = self.execute_query(query)
        return self._create_dish_object(results)
    
    def post(self, dish):
        query = """WITH inserted_dish AS (
    INSERT INTO dishes(id, name, description, price) 
    VALUES ({}, '{}', '{}', {})
    RETURNING id, name, description, price
)
SELECT id, name, description, price FROM inserted_dish;
""".format(dish['id'], dish['name'], dish['description'], dish['price'])
        results = self.execute_query(query)
        return self._create_dish_object(results)
    
    def put(self, updated_dish):
        query = """WITH updated_dish AS (
            UPDATE dishes 
            SET name = '{name}', description = '{description}', price = {price}
            WHERE id = {id}
            RETURNING id, name, description, price
        )
        SELECT id, name, description, price FROM updated_dish;
        """.format(id=updated_dish['id'], name=updated_dish['name'], description=updated_dish['description'], price=updated_dish['price'])
        
        results = self.execute_query(query)
        return self._create_dish_object(results)



    
    def delete(self, dish_id):
        query = """WITH deleted_dish AS (
            DELETE FROM dishes 
            WHERE id = {}
            RETURNING id, name, description, price
        )
        SELECT * FROM dishes;
        """.format(dish_id)
        
        results = self.execute_query(query)
        return self._create_dish_object(results)
    