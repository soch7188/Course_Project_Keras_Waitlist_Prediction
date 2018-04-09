// 1st course
db.course.insert(
    {
        "code": "COMP1001",
        "semester": "2017-18 Spring",
        "title": "Exploring Multimedia and Internet Computing",
        "credits": 3.0,
        "attributes": "Common Core (S&T) for 2010 & 2011 3Y programs\tCommon Core (S&T) for 2012 3Y programs\tCommon Core (S&T) for 4Y programs",
        "exclusion": "ISOM 2010, any COMP courses of 2000-level or above",
        "description": "This course is an introduction to computers and computing tools. It introduces the organization and basic working mechanism of a computer system, including the development of the trend of modern computer system. It covers the fundamentals of computer hardware design and software application development. The course emphasizes the application of the state-of-the-art software tools to solve problems and present solutions via a range of skills related to multimedia and internet computing tools such as internet, e-mail, WWW, webpage design, computer animation, spread sheet charts/figures, presentations with graphics and animations, etc. The course also covers business, accessibility, and relevant security issues in the use of computers and Internet.",
        "sections": [
            {
                "recordTime": new Date("2018-01-26 14:00"),
                "sectionId": "L1",
                "offerings": [{
                    "dateAndTime": "Th 03:00PM - 04:50PM",
                    "room": "Rm 5620, Lift 31-32 (70)",
                    "instructors": ["LEUNG, Wai Ting"]
                }],
                "quota": 67,
                "enrol": 19,
                "wait": 0
            },
            {
                "recordTime": new Date("2018-01-26 14:00"),
                "sectionId": "LA1",
                "offerings": [{
                    "dateAndTime": "Tu 03:00PM - 04:50PM",
                    "room": "Rm 4210, Lift 19 (67)",
                    "instructors": ["LEUNG, Wai Ting"]
                }],
                "quota": 67,
                "enrol": 19,
                "wait": 0
            },
            {
                "recordTime": new Date("2018-02-01 11:30"),
                "sectionId": "L1",
                "offerings": [{
                    "dateAndTime": "Th 03:00PM - 04:50PM",
                    "room": "Rm 5620, Lift 31-32 (70)",
                    "instructors": ["LEUNG, Wai Ting"]
                }],
                "quota": 67,
                "enrol": 29,
                "wait": 0
            },
            {
                "recordTime": new Date("2018-02-01 11:30"),
                "sectionId": "LA1",
                "offerings": [{
                    "dateAndTime": "Tu 03:00PM - 04:50PM",
                    "room": "Rm 4210, Lift 19 (67)",
                    "instructors": ["LEUNG, Wai Ting"]
                }],
                "quota": 67,
                "enrol": 29,
                "wait": 0
            }
            // ...
        ],

        // ================================================
        // COMP1001 does not have the following attributes.
        // They are shown because some other courses have these attributes
        "alternateCodes": "CIVL 1170", // an example course: ENVR1170
        "colistWith": "RMBI 4310", // COMP4332
        "corequisite": "LANG 4016", // ENVS4964
        "intendedLearningOutcomes": "On successful completion of the course, students will be able to:   1.  Evaluate the air pollution problem, in particular that in Hong Kong and PRD, and the main contributing factors. 2.  Explain and use the basic concepts and terminology in atmospheric aerosols and particulate matter for communication and discussion. 3.  Identify the common aerosol parameters and atmospheric processes governing the changes of atmospheric aerosols. 4.  Apply the concepts and knowledge to analyze aerosol related air pollution issues.   5.  Work in a team to analyze and comment on an aerosols-related air pollution issue, like those reported in scientific papers, and present and communicate the findings to a group of audience.", // EVSM5280
        "prerequisite": "MATH 1003 OR MATH 1012 OR MATH 1013 OR MATH 1018 (prior to 2013-14) OR MATH 1020 OR MATH 1023", // ENVS2003
        "previousCode": "ENVS 3002", // ENVS2003
        "vector": "[3-0-0:3]" // EVSM5280
    }
)

// 2nd course
db.course.insert(
    {
        "code": "COMP4332",
        "semester": "2017-18 Spring",
        "title": "Big Data Mining and Management",
        "credits": 3.0,
        "prerequisite": "COMP 4211 OR COMP 4331 OR ISOM 3360",
        "colistWith": "RMBI 4310",
        "description": "This course will expose students to new and practical issues of real world mining and managing big data. Data mining and management is to effectively support storage, retrieval, and extracting implicit, previously unknown, and potentially useful knowledge from data. This course will place emphasis on two parts. The first part is big data issues such as mining and managing on distributed data, sampling on big data and using some cloud computing techniques on big data. The second part is applications of the techniques learnt on areas such as business intelligence, science and engineering, which aims to uncover facts and patterns in large volumes of data for decision support. This course builds on basic knowledge gained in the introductory data-mining course, and explores how to more effectively mine and manage large volumes of real-world data and to tap into large quantities of data. Working on real world data sets, students will experience all steps of a data-mining and management project, beginning with problem definition and data selection, and continuing through data management, data exploration, data transformation, sampling, portioning, modeling, and assessment.",
        "sections": [
            {
                "recordTime": new Date("2018-01-26 14:00"),
                "sectionId": "L1",
                "offerings": [{
                    "dateAndTime": "WeFr 01:30PM - 02:50PM",
                    "room": "G010, CYT Bldg (140)",
                    "instructors": [
                        "WONG, Raymond Chi Wing"
                    ]
                }],
                "quota": 65,
                "enrol": 64,
                "wait": 4
            },
            {
                "recordTime": new Date("2018-01-26 14:00"),
                "sectionId": "T1",
                "offerings": [{
                    "dateAndTime": "Tu 06:00PM - 06:50PM",
                    "room": "Rm 4619, Lift 31-32 (126)",
                    "instructors": [
                        "WONG, Raymond Chi Wing"
                    ]
                }],
                "quota": 65,
                "enrol": 64,
                "wait": 4
            },
            {
                "recordTime": new Date("2018-02-01 11:30"),
                "sectionId": "L1",
                "offerings": [{
                    "dateAndTime": "WeFr 01:30PM - 02:50PM",
                    "room": "G010, CYT Bldg (140)",
                    "instructors": [
                        "WONG, Raymond Chi Wing"
                    ]
                }],
                "quota": 75,
                "enrol": 71,
                "wait": 3
            },
            {
                "recordTime": new Date("2018-02-01 11:30"),
                "sectionId": "T1",
                "offerings": [{
                    "dateAndTime": "Tu 06:00PM - 06:50PM",
                    "room": "Rm 4619, Lift 31-32 (126)",
                    "instructors": [
                        "WONG, Raymond Chi Wing"
                    ]
                }],
                "quota": 75,
                "enrol": 71,
                "wait": 3
            }
            // ...
        ],

        // ================================================
        // COMP4332 does not have the following attributes.
        // They are shown because some other courses have these attributes
        "attributes": "Common Core (S&T) for 2010 & 2011 3Y programs\tCommon Core (S&T) for 2012 3Y programs\tCommon Core (S&T) for 4Y programs", // example from COMP1001
        "alternateCodes": "CIVL 1170", // an example course: ENVR1170
        "corequisite": "LANG 4016", // ENVS4964
        "exclusion": "ISOM 2010, any COMP courses of 2000-level or above", // example from COMP1001
        "intendedLearningOutcomes": "On successful completion of the course, students will be able to:   1.  Evaluate the air pollution problem, in particular that in Hong Kong and PRD, and the main contributing factors. 2.  Explain and use the basic concepts and terminology in atmospheric aerosols and particulate matter for communication and discussion. 3.  Identify the common aerosol parameters and atmospheric processes governing the changes of atmospheric aerosols. 4.  Apply the concepts and knowledge to analyze aerosol related air pollution issues.   5.  Work in a team to analyze and comment on an aerosols-related air pollution issue, like those reported in scientific papers, and present and communicate the findings to a group of audience.", // EVSM5280
        "previousCode": "ENVS 3002", // ENVS2003
        "vector": "[3-0-0:3]" // EVSM5280
    }
)