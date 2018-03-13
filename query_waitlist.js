db = db.getSiblingDB("university")

start_ts = ISODate("2018-01-26T00:00:00.000Z")
end_ts = ISODate("2018-01-28T00:00:00.000Z")

result = db.course.aggregate(
    [
        { $unwind: '$sectionList'},
        { $match: {"sectionList.timeSlot": {
            $gte: start_ts,
            $lt: end_ts
        }}},
        // { $sort: {"sectionList.section": 1 } },
        { $project : { _id: 0, cid: 1, cname: 1, "sectionList.section": 1, "sectionList.wait": 1, "sectionList.timeSlot": 1 } },
    ]
)

printjson(result.toArray());