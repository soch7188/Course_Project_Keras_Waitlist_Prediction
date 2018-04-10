import os
from pymongo import MongoClient
import pymongo
from bson.son import SON
import pprint


try:
    # Making a DB connection
    print("Making a MongoDB connection...")
    client = MongoClient("mongodb://localhost:27017")

    # Getting a Database named "university"
    print("Getting a database named \"university\"")
    db = client["university"]

    # print(db.getCollectionNames())

except pymongo.errors.ConnectionFailure as error:
    print("DB Connection Failed! Error Message: \"{}\"".format(error))

def run():
    # Welcome message
    print("(3) Course Search\n")

    print("Please choose the menu you want to start by entering the number")
    print("[1] Course Search by Keyword")
    print("[2] Course Search by Waiting List Size")
    choice = input(" >>  ")
    exec_menu(choice)

    client.close()

    return


def searchByKeyword():

    print("(3)[1] Course Search by Keyword")
    keyword = input("Please enter the keyword >>  ")
    print("Course Search by Keyword: %s" % keyword)

    db.course.drop_indexes()
    db.course.create_index([("title", pymongo.TEXT), ("description", pymongo.TEXT), ("sections.remarks", pymongo.TEXT)])

    pipeline = [
        {"$match": {"$text": {"$search": keyword}}},
        {"$sort": {"code": 1, "sections.recordTime": 1}},
        {"$unwind": "$sections"},
        {"$sort": {"sections.recordTime": 1}},
        {"$group": {"_id": "$_id",
                    "code": {"$last": "$code"},
                    "sections": {"$push": "$sections"},
                    "lastRecordTime": {"$last": "$sections.recordTime"},
                    "title": {"$last": "$title"},
                    "credits": {"$last": "$credits"},
                    }},
        {"$unwind": "$sections"},
        {"$project": {"code": "$code", "credits": "$credits", "title": "$title", "sections": "$sections", "lastRecordTime": "$lastRecordTime", "isLastRecordTime": {"$eq": ["$sections.recordTime", "$lastRecordTime"]}}},
        {"$match": {"isLastRecordTime": True}},
        {"$group": {"_id": "$_id",
                    "code": {"$last": "$code"},
                    "sections": {"$push": "$sections"},
                    "title": {"$last": "$title"},
                    "credits": {"$last": "$credits"},
                    }},
        {"$sort": {"code": 1, "sections.sectionId": 1}},
        {"$project": {"_id": 0, "code": 1, "title": 1, "credits": 1, "sections": 1}},
        {"$project": {"_id": 0, "Course Code": "$code", "Course Title": "$title", "Number of Units/Credits": "$credits", "Sections": "$sections"}}
    ]

    indexAggregateSortedResult = list(db.course.aggregate(pipeline=pipeline))

    pp = pprint.PrettyPrinter(indent=0)
    pp.pprint(indexAggregateSortedResult)

    print("Course Search by Keyword complete")

    return


def searchByWaitingListSize():
    print("(3)[2] Course Search by Waiting List Size")
    size = input("Please enter the size >>  ")
    print("Course Search by Waiting List Size: %s" % size)

    








    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()

    if ch == '1':
        searchByKeyword()
    elif ch == '2':
        searchByWaitingListSize()
    else:
        print("Please retry.")

    return
