import pymongo
import bson
     
client = pymongo.MongoClient("mongodb://da1.eecs.utk.edu/")
db = client ['WoC']
coll = db['proj_metadata.R']
     
dataset = coll.find( { "NumAuthors": { "$gt": 1 } } , {"projectID" : 1} , no_cursor_timeout=True )

with open('./project_list', 'w') as f:
    for data in dataset:
	print >> f, data
    
dataset.close()
