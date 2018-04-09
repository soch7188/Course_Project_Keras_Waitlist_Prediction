#!/usr/bin/python
#
#  The program was written by Ziwon KIM, based on the code by Raymond WONG.
#
import scrapy
from pymongo import MongoClient
import pymongo

try:
    # Making a DB connection
    print("Making a MongoDB connection...")
    client = MongoClient("mongodb://localhost:27017")

    # Getting a Database named "university"
    print("Getting a database named \"university\"")
    db = client["university"]

    # print(db.getCollectionNames())

except pymongo.errors.ConnectionFailure as error:
    print("DB Connection Failed! Error Message: \"{}\"".format(error))


class TrialPageSpider(scrapy.Spider):
    name = "TrialPage"
    start_urls = []
    time_slots = []
    departments = []

    # Constructor (which is called at the beginning)
    def __init__(self, domain = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("TrialPageSpider domain: " + domain)
        self.start_urls.append(domain)  # Domain given by call parameter.
        print("This is called at the beginning.")

    # Closed (which is called at the end)
    def closed(self, reason):
        print("This is called at the end.")

    def parse(self, response):
        # print("TrialPageSpider Parse called.")

        # Step 1: If at the top directory (timeSlot Page),
        #         find a list of all links found in "href" of the "a" HTML tags
        if len(self.time_slots) == 0:
            list_of_time_slot_link = response.xpath("//a[@href]/@href").extract()

            # Step 2: Perform data crawling on the web page of each of the links
            #          where each link contains keyword "Table.html"
            for link in list_of_time_slot_link:
                self.time_slots.append(link)
                yield response.follow(link, callback=self.parse)

        # # Step 3: For all sub pages (inside the time slot page), extract list of subjects to search
        elif len(response.xpath("//div[contains(@id, 'classes')]").extract()) >= 1:

            list_of_courses = response.xpath("/html/body/div[@id='classes']/div[@class='course']")

            course_page_title = response.xpath("/html/head/title/text()").extract_first().split()  # Ex) 2017-18 Spring ACCT: Snapshot taken at 2018-01-26 14:00
            semester = course_page_title[0] + ' ' + course_page_title[1]

            for course in list_of_courses:
                course_code = course.xpath("./div[@class='courseanchor']/a/@name").extract_first()
                course_title = course.xpath("./h2/text()").extract_first()
                unit_pos = course_title.find(' unit')  # Let a whitespace in front of 'unit' in order to avoid unexpected finds such as "comm-unit-y"
                title = course_title[:(unit_pos-3)]
                credits = int(course_title[unit_pos-1])

                course_attributes = course.xpath("./div[@class='courseinfo']/div[contains(@class,'courseattr')]/div[@class='popupdetail']/table")
                attributes_raw = course_attributes.xpath(".//tr[th = 'ATTRIBUTES']/td/text()").extract()
                attributes = ''
                for attribute in attributes_raw:
                    if len(attributes) != 0:
                        attributes = attributes + '\t'
                    attributes = attributes + attribute
                if attributes == '':
                    attributes = None

                exclusion = course_attributes.xpath(".//tr[th = 'EXCLUSION']/td/text()").extract_first()
                description = course_attributes.xpath(".//tr[th = 'DESCRIPTION']/td/text()").extract_first()



                # Uncommon attributes
                alternate_codes = course_attributes.xpath(".//tr[th = 'ALTERNATE CODE(S)']/td/text()").extract_first()
                colist_with =course_attributes.xpath(".//tr[th = 'CO - LIST WITH']/td/text()").extract_first()
                corequisite =course_attributes.xpath(".//tr[th = 'CO-REQUISITE']/td/text()").extract_first()
                intendedLearningOutcomes =course_attributes.xpath(".//tr//table//text()").extract_first() # TODO: CHECK IF THIS WORKS PROPERLY on EVSM5280
                prerequisite =course_attributes.xpath(".//tr[th = 'PRE-REQUISITE']/td/text()").extract_first()
                previousCode =course_attributes.xpath(".//tr[th = 'PREVIOUS CODE']/td/text()").extract_first()
                vector =course_attributes.xpath(".//tr[th = 'VECTOR']/td/text()").extract_first()


                # Upsert course info
                db.course.update(
                    {
                        "code": course_code
                    },
                    {
                        "code": course_code,
                        "semester": semester,
                        "title": title,
                        "credits": credits,
                        "attributes": attributes,
                        "exclusion": exclusion,
                        "description": description,

                        "alternateCodes": alternate_codes,
                        "colistWith": colist_with,
                        "corequisite": corequisite,
                        "intendedLearningOutcomes": intendedLearningOutcomes,
                        "prerequisite": prerequisite,
                        "previousCode": previousCode,
                        "vector": vector,

                    },
                    upsert=True,
                )


                # Add Sections to course info
                db.collection.update(
                    {
                        "code": course_code,
                        # "sections.recordTime": ,
                    },
                    {
                        "$push": {
                            "sections": {
                                "recordTime": "",
                                "sectionId": "",
                                "offerings": [],
                                "quota": "",
                                "enrol": '',
                                "wait": ''
                            }
                        }
                    }
                )

                # Sample Document Insert Script for Nested Sections Part
                # "sections": [
                #     {
                #         "recordTime": new Date("2018-01-26 14:00"),
                #     "sectionId": "L1",
                #                  "offerings": [{
                #     "dateAndTime": "Th 03:00PM - 04:50PM",
                #     "room": "Rm 5620, Lift 31-32 (70)",
                #     "instructors": ["LEUNG, Wai Ting"]
                # }],
                # "quota": 67,
                # "enrol": 19,
                # "wait": 0
                # },
                # {
                #     "recordTime": new Date("2018-01-26 14:00"),
                # "sectionId": "LA1",
                # "offerings": [{
                #     "dateAndTime": "Tu 03:00PM - 04:50PM",
                #     "room": "Rm 4210, Lift 19 (67)",
                #     "instructors": ["LEUNG, Wai Ting"]
                # }],
                # "quota": 67,
                # "enrol": 19,
                # "wait": 0
                # },
                # {
                #     "recordTime": new Date("2018-02-01 11:30"),
                # "sectionId": "L1",
                # "offerings": [{
                #     "dateAndTime": "Th 03:00PM - 04:50PM",
                #     "room": "Rm 5620, Lift 31-32 (70)",
                #     "instructors": ["LEUNG, Wai Ting"]
                # }],
                # "quota": 67,
                # "enrol": 29,
                # "wait": 0
                # },

        else:
            list_of_departments = response.xpath("//a[@href]/@href").extract()
            for link in list_of_departments:
                self.departments.append(link)
                yield response.follow(link, callback=self.parse)


        # elif len(self.departments) == 0:
        #     list_of_departments = response.xpath("//a[@href]/@href").extract()
        #     for link in list_of_departments:
        #         self.departments.append(link)
        #         yield response.follow(link, callback=self.parse)
        #
        # elif self.at_dept_page:
        #     list_of_subjects_link = response.xpath("//a[@href]/@href").extract()
        #
        #     for link in list_of_subjects_link:
        #         yield response.follow(link, callback=self.parse)

#
# class DeptPageSpider(scrapy.Spider):
#     name = "DeptPage"
#     start_urls = []
#     departments = []
#
#     # Constructor (which is called at the beginning)
#     def __init__(self, domain='', *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         print("DeptPageSpider domain: " + domain)
#         self.start_urls.append(domain)  # Domain given by call parameter.
#         print("This is called at the beginning.")
#
#     # Closed (which is called at the end)
#     def closed(self, reason):
#         print("This is called at the end.")
#
#     def parse(self, response):
#         print("DeptPageSpider Parse called.")
#
#         list_of_departments = response.xpath("//a[@href]/@href").extract()
#         for link in list_of_departments:
#             self.departments.append(link)
#             yield response.follow(link, callback=CoursePageSpider.parse)
#
#
# class CoursePageSpider(scrapy.Spider):
#     name = "CoursePage"
#     start_urls = []
#
#     # Constructor (which is called at the beginning)
#     def __init__(self, domain='', *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         print("CoursePage domain: " + domain)
#         self.start_urls.append(domain)  # Domain given by call parameter.
#         print("This is called at the beginning.")
#
#     # Closed (which is called at the end)
#     def closed(self, reason):
#         print("This is called at the end.")
#
#     def parse(self, response):
#         print("CoursePageSpider Parse called.")
#
#         # Insert into DB.
#         list_of_courses = response.xpath("//div[contains(@class, 'course')]").extract()
#
#         for course in list_of_courses:
#             course_code = course.xpath("//div[contains(@class, 'courseanchor')]/a[@name]/@name")
#             db.course.insert(
#                 {
#                     "code": course_code,
#                     "semester": "test_semester",
#                     "title": "test_title"
#                 })