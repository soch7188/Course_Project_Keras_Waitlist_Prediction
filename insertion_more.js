db = db.getSiblingDB("university")

db.course.insert(
{
    cid: "COMP 1001",
    cname: "Exploring Multimedia and Internet Computing",
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
            wait: 25,
            remarks: "",
            timeSlot: new Date("2018-01-25T09:00:00")
        },
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
            wait: 35,
            remarks: "",
            timeSlot: new Date("2018-01-26T09:00:00") //YYYY-mm-ddTHH:MM:ss
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
            wait: 36,
            remarks: "",
            timeSlot: new Date("2018-01-26T09:00:00")
        },
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
            wait: 136,
            remarks: "",
            timeSlot: new Date("2018-01-27T19:00:00") //YYYY-mm-ddTHH:MM:ss
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
            wait: 135,
            remarks: "",
            timeSlot: new Date("2018-01-27T19:00:00")
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
            wait: 9,
            remarks: "",
            timeSlot: new Date("2018-01-25T09:00:00")
        },
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
            wait: 8,
            remarks: "",
            timeSlot: new Date("2018-01-27T19:00:00") //YYYY-mm-ddTHH:MM:ss
        },
        {
            section: "L2",
            sectionNumber: 1758,
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
            wait: 9,
            remarks: "",
            timeSlot: new Date("2018-01-27T19:00:00") //YYYY-mm-ddTHH:MM:ss
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
            wait: 6,
            remarks: "",
            timeSlot: new Date("2018-01-27T19:00:00")
        }
    ]
});
