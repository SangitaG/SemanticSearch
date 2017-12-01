import pymongo

def mongoDB_create_collection(db_name, collection_name, collection_lst):
    
    # Instantiate client to our Mongo Server
    client = pymongo.MongoClient('35.163.170.219', 27016)

    # Handle to  database
    db_ref = client[db_name]
    
    # If collection exists, remove it and rewrite it.
    if (collection_name in db_ref.collection_names()):
        db_ref[collection_name].remove()

    # Create a reference to a collection
    coll_ref = db_ref[collection_name]
        
    # Use the collection reference to insert the ML_page_contents
    for doc in tqdm(collection_lst):
        coll_ref.insert_one(doc)

def mongoDB_read_collection(db_name, collection_name):
    
    # Instantiate client to our Mongo Server
    client = pymongo.MongoClient('35.163.170.219', 27016)

    # Make a new database
    db_ref = client[db_name]

    # Create a reference to my_collection
    coll_ref = db_ref[collection_name] 
    
    # Read collection into a list.
    coll_lst = list(coll_ref.find())
    
    return(coll_lst)

def mongoDB_read_unique_pages_collection(db_name, collection_name):
    
    # Instantiate client to our Mongo Server
    client = pymongo.MongoClient('35.163.170.219', 27016)

    # Make a new database
    db_ref = client[db_name]

    # Create a reference to my_collection
    coll_ref = db_ref[collection_name] 
    
    
    # Read collection into a list.
    unique_pgeid_lst = coll_ref.distinct( "pageid" )
    
    # Read collection into a list.
    coll_lst = list(coll_ref.find())
    
    unique_pg_lst=[]
    for p_entry in coll_lst:
        if(len(unique_pgeid_lst) != 0):
            if p_entry['pageid'] in unique_pgeid_lst:
                unique_pg_lst.append(p_entry)
                unique_pgeid_lst.remove(p_entry['pageid'])
        else:
            break
    
    return(unique_pg_lst)
    
def mongoDB_get_DBnames():  
    
    # Instantiate client to our Mongo Server
    client = pymongo.MongoClient('35.163.170.219', 27016)    
    
    # Databases on our MongoDB Server.
    names = client.database_names()
    
    return(names)

def mongoDB_get_collection_names(db_name):
    
    # Instantiate client to our Mongo Server
    client = pymongo.MongoClient('35.163.170.219', 27016)    
    
    # Make a new database
    db_ref = client[db_name]
    
    names = db_ref.collection_names()
    
    return(names)