db = db.getSiblingDB("university")

result = db.course.aggregate(
    [
        {
            $lookup: {
                localField: 'section_id',
                from: 'section',
                foreignField: 'section_id',
                as: 'lecture_section'
            }
        },
        {
            $project: {
                _id: 1,
                'Course Code': '$course_code',
                'Course Title': '$title',
                'No.ofUnits/Credits': '$credits',
                'lecture_section.code': 1,
                'lecture_section.datetime': 1,
                'lecture_section.quota': 1,
                'lecture_section.enrol': 1,
                'lecture_section.avail': 1,
                'lecture_section.wait': 1
            }
        },
        {
            $sort: {'course_code': 1, 'lecture_section.section_id': 1}
        }
    ]
)

printjson(result.toArray());


printjson( db.course.find( {description: { $regex: "course"} } ).toArray() );

// db.course.find( {description: { $regex: "course"} } );
//
// cursor = db.course.find( {description: { $regex: "course"} } );
// while ( cursor.hasNext() ) {
//    print( cursor.next() )
// }
