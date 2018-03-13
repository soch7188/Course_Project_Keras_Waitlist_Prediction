db.course.aggregate(
    [
        {
            $lookup: {
                localField: “section_id”,
                from: “section”,
                foreignField: “section_id”,
                as: “lecture_sections”
            }
        },
        {
            $project: {
                _id: 0,
                “Course Code”: “$course_code”,
                “Course Title”: “$title”,
                “No. of Units/Credits”: “$credits”,
                “lecture_section.code”: 1,
                “lecture_section.datetime”: 1,
                “lecture_section.quota”: 1,
                “lecture_section.enrol”: 1,
                “lecture_section.avail”: 1,
                “lecture_section.wait”: 1
            }
        },
        {
            $sort: {“course_code”: 1, “lecture_section.section_id”: 1}
        }
    ]
)

db.course.find( {description: { $regex: "keyword(s)"} } );
