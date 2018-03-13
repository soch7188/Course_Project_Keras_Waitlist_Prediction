db = db.getSiblingDB("university")


let num_f = 2;
let start_ts = ISODate("2018-01-24T00:00:00.000Z");
let end_ts = ISODate("2018-01-29T00:00:00.000Z");

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
        { $project : { _id: 0, cid: 1, cname: 1, "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1, "sectionList.enrol": 1 } },
    ]
)

printjson(result.toArray());

// db = db.getSiblingDB("university")
//
// // Given inputs
// num_f = 100;
// start_ts = ISODate("2018-01-26T00:00:00.000Z")
// end_ts = ISODate("2018-01-28T00:00:00.000Z")
//
// // DB Query
// result = db.course.aggregate(
//     [
//         { $unwind: '$sectionList'},
//         { $match:
//             {
//                 "sectionList.timeSlot": {
//                     $gte: start_ts,
//                     $lt: end_ts
//                 }
//             }
//         },
//         { $match:
//             {
//                 $expr:{$gt:["$sectionList.wait", num_f]}
//             }
//         },
//         {$project: {"sectionList.wait": 1}}
//         // { $match: {$expr:  function() { return "sectionList.wait" < "sectionList.enrol" }}},
//         // { $sort: {"sectionList.section": 1 } },
//         // { $project : { _id: 0, "Course Code": '$cid', "Course Title": '$cname', "No of Units/Credits": "$credit", "Matched Time Slot": "", "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1 } },
//         // { $group: {_id: "$cid"}}
//     ]
// )
//
// // Print out result
// printjson(result.toArray());