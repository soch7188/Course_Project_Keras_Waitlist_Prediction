db = db.getSiblingDB("university")


num_f = 2;
start_ts = ISODate("2018-01-24T00:00:00.000Z");
end_ts = ISODate("2018-01-29T00:00:00.000Z");

latestTimeSlotResult = db.course.aggregate([
    { $unwind: '$sectionList'},
    { $match: {
        "sectionList.timeSlot": {
            $gte: start_ts,
            $lt: end_ts
        }
    }},
    // { $match: {$expr: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]}}},
    { $group: {
        "_id": "$cid",
        "LatestTimeSlot": {
            "$last": "$sectionList.timeSlot"
        }
    }}
]);

// printjson(latestTimeSlotResult.toArray())
latestTimeSlot = latestTimeSlotResult.toArray()[0].LatestTimeSlot

result = db.course.aggregate([
        { $unwind: '$sectionList'},
        { $match: {"sectionList.timeSlot": {
            $gte: start_ts,
            $lt: end_ts
        }}},
        // The filter that keeps the records that fulfill the condition that (waitlist size >= enrolment * f) // TODO: IMPLEMENT
        { $match: {$expr: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]}}},
        { $project : {
            _id: 0,
            cid: 1,
            cname: 1,
            credit: 1,
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
        { $sort: {"cid": -1, "sectionList.section": 1}},
        { $match: { "sectionList.timeSlot": latestTimeSlot }},
        { $group: {
            "_id": "$cid",
            "Course Code": {"$last": "$cid"},
            "Course Title": {"$last": "$cname"},
            "Number of Units/Credits": {"$last": "$credit"},
            "Matched Time Slot": {"$last": latestTimeSlot},
            "Section_List": {"$push" :"$sectionList"},
        }},
        {$project: {_id: 0}}
    ]
);


printjson(result.toArray());
