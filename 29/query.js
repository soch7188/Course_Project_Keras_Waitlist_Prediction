// Retrieve "university" database without modifying the db variable in the shell environment.
db = db.getSiblingDB("university")

// ------------------ Query by Keyword --------------------- //
print(" -------------- Query by Keyword --------------- ")


// Creating a text index for all fields.
// db.course.createIndex({"$**": "text"})

// Creating a text index for "cname" field. It can speed up keyword search.
db.course.createIndex({"cname": "text"})

// INDEX BASED SEARCH
indexAggregateSortedResult = db.course.aggregate(                       // Aggregation Pipeline that handles multiple mongo executions and returns a single result
    [
        { $match: {$text: {$search: 'Exploring something'}}},           // MATCH: Filter out non-satisfied records and keep the records that contain the searched word (e.g. either "Exploring" or "something") 
        { $unwind: '$sectionList'},                                     // UNWIND: Based on sectionList, unroll all the elements inside the sectionList as stand-alone records with all the corresponding fields and values as originals
        { $sort: {"cid": -1, "sectionList.section": 1}},                // SORT: Order the records by field "cid" decendingly first, and by field "sectionList.section" ascendingly afterward
        { $project : { _id: 0, cid: 1, cname: 1, credit: 1, "sectionList.section": 1, "sectionList.dateTime": 1, "sectionList.quota": 1, "sectionList.enrol": 1, "sectionList.avail": 1, "sectionList.wait": 1 } },     // PROJECT: Discard _id and keep all the following fields shown, if denoted as 1
        { $group: {                                                     // GROUP: Group the records by cid, and reorganize the fields as following
            "_id": "$cid",                                              // cid is the pivot for grouping
            "Course Code": {"$last": "$cid"},                           // Find the latest
            "Course Title": {"$last": "$cname"},                        // Find the latest
            "Number of Units/Credits": {"$last": "$credit"},            // Find the latest
            "Section_List": {"$push" :"$sectionList"},                  // Push all the records to sectionList that turns out to be an array
        }},
        {$project: {_id: 0}}                                            // Discard _id
    ]
);

// REGEX BASED SEARCH
// indexResult = db.course.find({"cname": {$regex: /Multimedi/}})

printjson(indexAggregateSortedResult.toArray());                        // Show the query result in the format of JSON






// -------------- Query by Waitlist Size --------------- //
print("\n\n\n -------------- Query by Waitlist Size --------------- ")

num_f = 2;                                          // The number 'f' as requested
start_ts = ISODate("2018-01-24T00:00:00.000Z");     // The starting timestamp
end_ts = ISODate("2018-01-29T00:00:00.000Z");       // The ending timestamp

latestTimeSlotResult = db.course.aggregate([
    { $unwind: '$sectionList'},                     // UNWIND: unroll all the elements in sectionList, and each of which become a stand-alone records with all the corresponding fields and values as originals
    { $match: {                                     // MATCH: Filter out all the unsatisfied records and keep the records that locate within the given time span ranging from start_ts to end_ts
        "sectionList.timeSlot": {
            $gte: start_ts,
            $lt: end_ts
        }
    }},
    // The filter that keeps the records that fulfill the condition that (waitlist size >= enrolment * f)
    // { $match: {$expr: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]}}},
    { $group: {                                     // GROUP: using cid as the pivot, find out the latest timestamp of each course
        "_id": "$cid",
        "LatestTimeSlot": {
            "$last": "$sectionList.timeSlot"
        }
    }}
]);

// Collect all the latest time slot for proceeding executions
// printjson(latestTimeSlotResult.toArray())
latestTimeSlot = latestTimeSlotResult.toArray()[0].LatestTimeSlot

result = db.course.aggregate([
        { $unwind: '$sectionList'},                 // UNWIND: unroll all the elements in sectionList, and each of which become a stand-alone records with all the corresponding fields and values as originals
        { $match: {"sectionList.timeSlot": {        // MATCH: Filter out all the unsatisfied records and keep the records that locate within the given time span ranging from start_ts to end_ts
            $gte: start_ts,
            $lt: end_ts
        }}},
        // The filter that keeps the records that fulfill the condition that (waitlist size >= enrolment * f)
        // { $match: {$expr: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]}}},
        { $project : {                              // Discard _id and keep the following fields if denoted as 1
            _id: 0,
            cid: 1,
            cname: 1,
            credit: 1,
            // The conditional statement to generate the value "Satisfied" for each section (not included in phase 2)
            // "sectionList.Satisfied": {
            //     $cond: {
            //         if: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]},
            //         then: "Yes",
            //         else: "No"
            //     }
            // },
            "sectionList.section": 1,
            "sectionList.dateTime": 1,
            "sectionList.quota": 1,
            "sectionList.enrol": 1,
            "sectionList.avail": 1,
            "sectionList.wait": 1,
            "sectionList.timeSlot": 1,
            }
        },
        { $sort: {"cid": -1, "sectionList.section": 1}},            // SORT: Order the cid decendingly and then section title ascendingly
        { $match: { "sectionList.timeSlot": latestTimeSlot }},      // MATCH: Filter that capture the latest timeslot for each section
        { $group: {                                                 // GROUP: Use _id as pivot to group each course and show the additional fields as following
            "_id": "$cid",
            "Course Code": {"$last": "$cid"},                       // Find the latest
            "Course Title": {"$last": "$cname"},                    // Find the latest
            "Number of Units/Credits": {"$last": "$credit"},        // Find the latest
            "Matched Time Slot": {"$last": latestTimeSlot},         // Find the latest
            "Section_List": {"$push" :"$sectionList"},              // Push all the records to sectionList that turns out to be an array
        }},
        {$project: {_id: 0}}                                        // Discard _id
    ]
);


printjson(result.toArray());                                        // Show the query result in the format of JSON

