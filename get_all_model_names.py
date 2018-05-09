import pymongo
import collections
import datetime

host = "127.0.0.1"
database_name = "hkust"

# Connect to MongoDB
client = pymongo.MongoClient(host)
db = client[database_name]

print("Database Connected")

def arr(_in): return [x for x in _in]

# def mergeDict(x,y): return {**x, **y}


course = arr(db.courses.aggregate([
    {"$match": {"code": {"$regex": "RMBI.*|COMP1942|COMP42.*|COMP43.*"}}},
    {"$project": {"code":1, "_id":0, "sections.sectionId":1}},
    {"$unwind": "$sections"},
    {"$group": {
        "_id":{
            "code":"$code",
            "sectionId":"$sections.sectionId"
    }}} 
]))

# print(course)

courseList = [x["_id"] for x in arr(course)]
print(courseList)
