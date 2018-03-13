db = db.getSiblingDB("university")

// db.course.createIndex({"$**": "text"})
db.course.createIndex({"cname": "text"})

// INDEX BASED SEARCH
indexResult = db.course.find({$text: {$search: "\'Multimedi\'"}}, {}).sort({'timeRecord':1})

// REGEX BASED SEARCH
// indexResult = db.course.find({"cname": {$regex: /Multimedi/}})

printjson(indexResult.toArray());