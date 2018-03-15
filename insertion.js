// Retrieve "university" database without modifying the db variable in the shell environment.
db = db.getSiblingDB("university")

// ################ Insertion ################ //
db.course.insert(
{
    cid: "COMP 1001",   // Course ID (STRING)
    cname: "Exploring Multimedia and Internet Computing",   // Course Name (STRING)
    category: "COMP",   // Course Category (STRING): To speed up catogorized query in future usage
    credit: 3,          // Credit Unit (INTEGER)
    courseInfo:         // Course Information (Embedded Document): Stratified multiple items
    {
        attributes:     // Common Core Attributes (Array of STRING): Can be empty
        [
            "Common Core (S&T) for 2010 & 2011 3Y programs",
            "Common Core (S&T) for 2012 3Y programs",
            "Common Core (S&T) for 4Y programs"
        ],
        exclusion: "ISOM 2010, any COMP courses of 2000-level or above",    // Exclusion and Description (STRING)
        description: "This course is an introduction to computers and computing tools. It introduces the organization and basic working mechanism of a computer system, including the development of the trend of modern computer system. It covers the fundamentals of computer hardware design and software application development. The course emphasizes the application of the state-of-the-art software tools to solve problems and present solutions via a range of skills related to multimedia and internet computing tools such as internet, e-mail, WWW, webpage design, computer animation, spread sheet charts/figures, presentations with graphics and animations, etc. The course also covers business, accessibility, and relevant security issues in the use of computers and Internet."
    },
    sectionList:        // Sections belonged to the course (Array of Embedded Document): Each section can have different section title (e.g. "L1", "LA1") and different timeSlot.
    [
        {
            section: "L1",                      // Section Title (STRING)
            sectionNumber: 1756,                // Section Number (INTEGER)
            dateTime:                           // Day and Time (Embedded Document): Contains info about weekly schedule
            {

                weekDay: "Thursday",            // Weekday (STRING)
                startTime: "03:00PM",           // Start Time (STRING)
                endTime: "04:50PM",             // End TIme (STRING)
            },
            room: "Rm 5620, Lift 31-32 (70)",   // Venue (STRING)
            instructor: "LEUNG, Wai Ting",      // Instructor (STRING): Can vary among sections within one course
            quota: 67,                          // Quota Number (INTEGER)
            enrol: 4,                           // Enroll Number (INTEGER)
            avail: 63,                          // Available Number (INTEGER)
            wait: 0,                            // Waitlist Number (INTEGER)
            remarks: "",                        // Additional Remarks about enrollment (STRING)
            timeSlot: new Date("2018-01-25T09:00:00")   // Timeslot of the snapshot (ISODATE): In the format of YYYY-mm-ddTHH:MM:ss
        },
        {
            section: "LA1",
            sectionNumber: 1757,
            dateTime:
            {

                weekDay: "Tuesday",
                startTime: "03:00PM",
                endTime: "04:50PM",

            },
            room: "Rm 4210, Lift 19 (67)",
            instructor: "LEUNG, Wai Ting",
            quota: 67,
            enrol: 4,
            avail: 63,
            wait: 0,
            remarks: "",
            timeSlot: new Date("2018-01-25T09:00:00")
        }
    ]
});


db.course.insert(
{
    cid: "COMP 4332",
    cname: "Big Data Mining and Management",
    category: "COMP",
    credit: 3,
    courseInfo:
    {
        attributes:
        [
            "Common Core (S&T) for 2010 & 2011 3Y programs",
            "Common Core (S&T) for 2012 3Y programs",
            "Common Core (S&T) for 4Y programs"
        ],
        exclusion: "ISOM 2010, any COMP courses of 2000-level or above",
        description: "This course is an introduction to computers and computing tools. It introduces the organization and basic working mechanism of a computer system, including the development of the trend of modern computer system. It covers the fundamentals of computer hardware design and software application development. The course emphasizes the application of the state-of-the-art software tools to solve problems and present solutions via a range of skills related to multimedia and internet computing tools such as internet, e-mail, WWW, webpage design, computer animation, spread sheet charts/figures, presentations with graphics and animations, etc. The course also covers business, accessibility, and relevant security issues in the use of computers and Internet."
    },
    sectionList:
    [
        {
            section: "L1",
            sectionNumber: 1756,
            dateTime:
            {

                weekDay: "Thursday",
                startTime: "03:00PM",
                endTime: "04:50PM",
            },
            room: "Rm 5620, Lift 31-32 (70)",
            instructor: "LEUNG, Wai Ting",
            quota: 67,
            enrol: 4,
            avail: 63,
            wait: 0,
            remarks: "",
            timeSlot: new Date("2018-01-25T09:00:00") //YYYY-mm-ddTHH:MM:ss
        },
        {
            section: "LA1",
            sectionNumber: 1757,
            dateTime:
            {

                weekDay: "Tuesday",
                startTime: "03:00PM",
                endTime: "04:50PM",

            },
            room: "Rm 4210, Lift 19 (67)",
            instructor: "LEUNG, Wai Ting",
            quota: 67,
            enrol: 4,
            avail: 63,
            wait: 0,
            remarks: "",
            timeSlot: new Date("2018-01-25T09:00:00")
        }
    ]
});
