from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #pin
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #

        HOST="nv-desktop-services.apporto.com"
        PORT=31017
        DB="acc"
        COL="animals"

                        
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,int(PORT)))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Create method
    def create(self, data):
        if data is not None:
            find_animal = self.database.animals.find_one({ "name": data['name']})
            
            if find_animal is not None:
                raise Exception(f"Nothing to create, because {data['name']} already exists")
            else:
                insert_animal = self.database.animals.insert_one(data) 
                
                if insert_animal is not None:
                    print(f"{data['name']} was successfully created!")
                    return True
                else:
                    raise Exception("There was an issue creating a new animal.")

# Read method
    def read(self, value):
        if value is not None:
            animals = self.database.animals.find(value)
            animal_list = list(animals)

            return animal_list


            # if animal_list:
            #     for animal in animal_list:
            #         for key in animal:
            #             print(key,": ", animal[key])
            #     print("\n")
            # else:
            #     raise Exception(f"Cannot find an animal with the key {key} and {value}")

        else:
            raise Exception(f"Cannot find {value} to read")

# Update method
    def update(self, key, value, update_data):
        if key is not None and value is not None and update_data is not None:
            find_animal = self.database.animals.find({ key: value })
            
            if find_animal is not None:
                update_animal = self.collection.update_one({key: value}, {'$set': update_data})

                if update_animal.modified_count == 1:
                    print(f"modified_count: {update_animal.modified_count}")
                else:
                    raise Exception(f"There was an error updating {key} {value}")
            else:
                raise Exception(f"There isn't a {key} {value} document found in collection. Please create it.")
        else:
            raise Exception(f"Cannot find {key} {value} to update or no update_data was set.")

# Delete method
    def delete(self, key, value):
        deleted_animal = self.collection.delete_one({key: value})
        
        if deleted_animal.deleted_count == 1:
            print(f"deleted.deleted_count: {deleted_animal.deleted_count}")
        else:
            raise Exception(f"Cannot find {key} {value} to delete")

   
