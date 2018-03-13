db = db.getSiblingDB("university")

// INDEX BASED SEARCH
indexResult = db.course.find({$text: {$search: "Multimedia asdfasdf"}},
    // Project
    {
        _id: 0,
        cid: 1,
        cname: 1,
        credit: 1,
        sectionList: 1
    }
).sort({'timeRecord':1})

printjson(indexResult.toArray());

result = db.course.aggregate(
    [
        {$match: {$text: {$search: 'Exploring asdasdf'}}},
        { $unwind: '$sectionList'},
        { $sort: {"sectionList.section": 1 } },
        { $project : { _id: 0, cid: 1, cname: 1, credit: 1, "sectionList.section": 1, "sectionList.dateTime": 1, "sectionList.quota": 1, "sectionList.enrol": 1, "sectionList.avail": 1, "sectionList.wait": 1 } },
    ]
)

printjson(result.toArray());