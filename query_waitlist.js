db = db.getSiblingDB("university")

// INDEX BASED SEARCH
// indexResult = db.course.find({$text: {$search: "Multimedia asdfasdf"}},
//     // Project
//     {
//         _id: 0,
//         cid: 1,
//         cname: 1,
//         credit: 1,
//         sectionList: 1
//     }
// ).sort({'timeRecord':1})

// printjson(indexResult.toArray());

result = db.course.aggregate(
    [
        
        { $unwind: '$sectionList'},
        { $match: {"sectionList.timeSlot": {
            $gte: ISODate("2018-01-26T00:00:00.000Z"),
            $lt: ISODate("2018-01-27T00:00:00.000Z")
        }}},
        // { $sort: {"sectionList.section": 1 } },
        { $project : { _id: 0, cid: 1, cname: 1, "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1 } },
    ]
)

printjson(result.toArray());