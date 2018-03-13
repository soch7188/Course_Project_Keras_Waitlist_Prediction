db = db.getSiblingDB("university")

printjson( db.course.find().toArray() );
