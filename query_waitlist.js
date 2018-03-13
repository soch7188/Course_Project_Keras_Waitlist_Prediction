// db = db.getSiblingDB("university")
//
//
// let num_f = 2;
// let start_ts = ISODate("2018-01-24T00:00:00.000Z");
// let end_ts = ISODate("2018-01-29T00:00:00.000Z");
//
// result = db.course.aggregate(
//     [
//
//         { $unwind: '$sectionList'},
//         { $match: {"sectionList.timeSlot": {
//             $gte: start_ts,
//             $lt: end_ts
//         }}},
//         // { $match: {$expr: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]}}},
//
//         // { $sort: {"sectionList.section": 1 } },
//         { $project : {
//             _id: 0,
//             cid: 1,
//             cname: 1,
//             "sectionList.satisfied": {
//                 $cond: {
//                     if: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]},
//                     then: 1,
//                     else: 0
//                 }
//             },
//             "sectionList.section": 1,
//             "sectionList.wait": 1,
//             "sectionList.timeSlot": 1,
//             "sectionList.enrol": 1 }
//         },
//         { $group: {
//             _id: {"cid": "$cid"},
//             // last: { $last: "$sectionList.timeSlot"},
//             matchedTimeSlots: {
//                 // $cond: {
//                 //     if: { $eq: ["sectionList.satisfied", 1]},
//                 //     then: { $push: "$sectionList.timeSlot"}
//                 // }
//                 $push: "$sectionList.timeSlot"
//
//                 // $cond: {
//                 //     if: { $eq: ["sectionList.satisfied", 1]},
//                 //     then: { $push: {"timeSlot": "$sectionList.timeSlot"}}
//                 // }
//             }
//
//
//         }}
//     ]
// )
//
// printjson(result.toArray());

// -------------------------------- Jeff's Code Above ----------------------------------- //

db = db.getSiblingDB("university")


num_f = 2;
start_ts = ISODate("2018-01-24T00:00:00.000Z");
end_ts = ISODate("2018-01-29T00:00:00.000Z");

latestTimeSlotResult = db.course.aggregate([
    { $unwind: '$sectionList'},
        { $match: {"sectionList.timeSlot": {
            $gte: start_ts,
            $lt: end_ts
        }}},
        { $match: {$expr: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]}}},
        // { $match: { $where:  function() { return $sectionList.wait < num_f * $sectionList.enrol }}},

        // { $sort: {"sectionList.section": 1 } },
        // { $project : { _id: 0, cid: 1, cname: 1, "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1, "sectionList.enrol": 1 } },
        // { $project : { _id: 0, "Course Code": '$cid', "Course Title": '$cname', "No of Units/Credits": "$credit", "Matched Time Slot": "", "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1 } },
        { $group: {
                "_id": "$cid",
                "LatestTimeSlot": {"$last": "$sectionList.timeSlot"},
            }
        },
])

latestTimeSlot = latestTimeSlotResult.toArray()[0].LatestTimeSlot

// printjson(latestTimeSlotResult.toArray())
// print(latestTimeSlot)

result = db.course.aggregate(
    [

        { $unwind: '$sectionList'},
        { $match: {"sectionList.timeSlot": {
            $gte: start_ts,
            $lt: end_ts
        }}},
        { $match: {$expr: {$gt: ["$sectionList.wait", {$multiply: ["$sectionList.enrol", num_f]}]}}},
        // { $match: { $where:  function() { return $sectionList.wait < num_f * $sectionList.enrol }}},

        // { $sort: {"sectionList.section": 1 } },
        // { $project : { _id: 0, cid: 1, cname: 1, "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1, "sectionList.enrol": 1 } },
        // { $project : { _id: 0, "Course Code": '$cid', "Course Title": '$cname', "No of Units/Credits": "$credit", "Matched Time Slot": "", "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1 } },
        // { $group: {
        //         "_id": "$cid",
        //         "Course Title": { "$first": "cname" },
        //         "Section List": {"$push": "$sectionList.timeSlot"},
        //         "LatestTimeSlot": {"$last": "$sectionList.timeSlot"},
        //     }
        // },
        // { $match: {"sectionList.timeSlot": latestTimeSlot}}
        // { $match: { "sectionList.timeSlot": {$eq: ["$sectionList.timeSLot" ,latestTimeSlot ] }}}
        { $match: { "sectionList.timeSlot": latestTimeSlot }},
        // { $eq: [ "$qty", 250 ] }
        {$group: {
            "_id": "$cid",
                "Section List": {"$push" :"$sectionList"},
        }}

    ]
)


printjson(result.toArray());
