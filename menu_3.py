import datetime
import os
from pymongo import MongoClient, collation
import pymongo
from bson.son import SON
import pprint


try:
    # Making a DB connection
    print("Making a MongoDB connection...")
    client = MongoClient("mongodb://localhost:27017")

    # Getting a Database named "university"
    print("Getting a database named \"hkust\"")
    db = client["hkust"]

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
    keyword = keyword.replace(",", "")
    keyword = keyword.replace(";", "")
    keyword = keyword.replace(".", "")
    keyword = keyword.replace(":", "")
    keyword = keyword.replace("-", " ")
    print("Course Search by Keyword: %s" % keyword)


    # Uncomment the two lines below when data is first crawled and this function is called for the first time.
    # db.courses.drop_indexes()
    # db.courses.create_index([("code", pymongo.TEXT), ("title", pymongo.TEXT), ("description", pymongo.TEXT)])

    pipeline = [
        {"$match": {"$text": {"$search": keyword, "$caseSensitive": True}}},
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
        {"$project": {"code": "$code", "credits": "$credits", "title": "$title",
                      "sections.SectionId": "$sections.sectionId",
                      "sections.Enrol": "$sections.enrol",
                      "sections.Quota": "$sections.quota",
                      "sections.Wait": "$sections.wait",
                      "sections.Avail": {"$subtract": ["$sections.quota", "$sections.enrol"]},
                      "sections.Date&Time": "$sections.offerings.dateAndTime",
                      "lastRecordTime": "$lastRecordTime",
                      "isLastRecordTime": {"$eq": ["$sections.recordTime", "$lastRecordTime"]}}},
        # {"$project": {"code": "$code", "credits": "$credits", "title": "$title",
        #               "sections": "$sections", "lastRecordTime": "$lastRecordTime",
        #               "isLastRecordTime": {"$eq": ["$sections.recordTime", "$lastRecordTime"]}}},
        # {"$group": {"_id": "$_id",
        #             "sections.avail": {"$subtract": ["$sections.quota", "$sections.avail"]}}},
        {"$match": {"isLastRecordTime": True}},
        {"$group": {"_id": "$_id",
                    "code": {"$last": "$code"},
                    "sections": {"$push": "$sections"},
                    "title": {"$last": "$title"},
                    "credits": {"$last": "$credits"},
                    }},
        {"$sort": {"code": 1, "sections.sectionId": 1}},
        {"$project": {"_id": 0, "code": 1, "title": 1, "credits": 1,
                      "sections.SectionId": 1,"sections.Enrol": 1, "sections.Quota": 1,
                      "sections.Wait": 1, "sections.Avail": 1,
                      "sections.Date&Time": 1,
                      # "sections.offerings[0].dateAndTime": 1
                      }
         },
        {"$project": {"_id": 0, "Course Code": "$code", "Course Title": "$title",
                      "Number of Units/Credits": "$credits", "Sections": "$sections"}}
    ]

    indexAggregateSortedResult = list(
        db.courses.aggregate(pipeline=pipeline, allowDiskUse=True)
    )

    pp = pprint.PrettyPrinter(indent=0)
    pp.pprint(indexAggregateSortedResult)

    print("Course Search by Keyword complete")

    return


def searchByWaitingListSize():
    print("(3)[2] Course Search by Waiting List Size")
    num_f = input("Please enter the f value >>  ")
    num_f = int(num_f)
    # Required timestamp format: 2018-01-28 10:00
    start_ts_input = input("Please enter the starting timestamp >>  ")
    end_ts_input = input("Please enter the ending timestamp >>  ")
    start_ts_input = start_ts_input.split(' ')
    end_ts_input = end_ts_input.split(' ')
    start_ts = datetime.datetime.strptime(start_ts_input[0] + 'T' + start_ts_input[1] + ' +0800', "%Y-%m-%dT%H:%M %z")
    end_ts = datetime.datetime.strptime(end_ts_input[0] + 'T' + end_ts_input[1] + ' +0800', "%Y-%m-%dT%H:%M %z")

    print("Course Search by num_f: %s" % num_f)

    pipeline = [
        {"$match": {"sections.sectionId": {"$in": ["L1"]}}},
        {"$unwind": '$sections'},
        {"$match": {"sections.recordTime": {
            "$gte": start_ts,
            "$lt": end_ts
        }}},
        {"$project": {
            "_id": 0,
            "code": 1,
            "title": 1,
            "credits": 1,
            "sections.Satisfied": {
                "$cond": {
                    # "if": {"$gt": ["$sections.wait", {"$multiply": ["$sections.enrol", num_f]}]},
                    "if": {"$gte": ["$sections.wait", {"$multiply": ["$sections.enrol", num_f]}]},
                    "then": True,
                    "else": False
                }
            },
            "sections.sectionId": 1,
            # "sections.offerings": 1,
            "sections.Date&Time": "$sections.offerings.dateAndTime",
            "sections.quota": 1,
            "sections.enrol": 1,
            "sections.avail": 1,
            "sections.wait": 1,
            "sections.recordTime": 1,
            }
        },
        {"$match": {"sections.Satisfied": True}},

        {"$sort": {"code": 1, "sections.sectionId": 1}},
        {"$group": {"_id": "$code",
                    "code": {"$last": "$code"},
                    "sections": {"$push": "$sections"},
                    "lastRecordTime": {"$last": "$sections.recordTime"},
                    "title": {"$last": "$title"},
                    "credits": {"$last": "$credits"},
                    }},

        {"$unwind": "$sections"},
        {"$project": {"code": 1, "credits": 1, "title": 1, "sections": 1,
                      "lastRecordTime": 1,
                      "isLastRecordTime": {"$eq": ["$sections.recordTime", "$lastRecordTime"]}}},

        {"$match": {"isLastRecordTime": True}},

        {"$group": {"_id": "$_id",
                    "code": {"$last": "$code"},
                    "sections": {"$push": "$sections"},
                    "title": {"$last": "$title"},
                    "credits": {"$last": "$credits"},
                    }},
        {"$sort": {"code": 1, "sections.sectionId": 1}},
        {"$project": {"_id": 0, "code": 1, "title": 1, "credits": 1, "sections": 1}},
        {"$project": {"_id": 0, "Course Code": "$code", "Course Title": "$title", "Number of Units/Credits": "$credits",
                      "Sections": "$sections"}}
    ]


    sizeAggregateSortedResult = list(db.courses.aggregate(pipeline=pipeline))

    pp = pprint.PrettyPrinter(indent=0)
    pp.pprint(sizeAggregateSortedResult)

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
