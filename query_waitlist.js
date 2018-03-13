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