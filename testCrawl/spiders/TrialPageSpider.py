#!/usr/bin/python
#
#  The program was written by Ziwon KIM, based on the code by Raymond WONG.
#
import datetime

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
                colist_with = course_attributes.xpath(".//tr[th = 'CO - LIST WITH']/td/text()").extract_first()
                corequisite = course_attributes.xpath(".//tr[th = 'CO-REQUISITE']/td/text()").extract_first()
                intended_learning_outcomes_raw = course_attributes.xpath(".//tr//table//text()").extract()
                intended_learning_outcomes = ''.join(intended_learning_outcomes_raw)
                prerequisite = course_attributes.xpath(".//tr[th = 'PRE-REQUISITE']/td/text()").extract_first()
                previous_code = course_attributes.xpath(".//tr[th = 'PREVIOUS CODE']/td/text()").extract_first()
                vector = course_attributes.xpath(".//tr[th = 'VECTOR']/td/text()").extract_first()

                # Upsert course info
                db.course.update(
                    {
                        "code": course_code
                    },
                    {
                        "$set": {
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
                            "intendedLearningOutcomes": intended_learning_outcomes,
                            "prerequisite": prerequisite,
                            "previousCode": previous_code,
                            "vector": vector,
                        },

                    },
                    upsert=True,
                )

                record_time = course_page_title[-2] + "T" + course_page_title[-1] + " +0800"
                list_of_sections = course.xpath("./table//tr")
                is_first = True
                curr_section_id = ""

                for section in list_of_sections:
                    # Skip first "tr" - only have headings no meaningful data to store
                    if is_first:
                        is_first = False
                        continue

                    section_tr_class = section.xpath("./@class").extract_first()

                    if "newsect" in section_tr_class:
                        section_id = section.xpath("./td[1]/text()").extract_first()
                        curr_section_id = section_id
                        offerings_date_and_time_raw = section.xpath("./td[2]/text()").extract()
                        offerings_date_and_time = ' '.join(offerings_date_and_time_raw)
                        offerings_room = section.xpath("./td[3]/text()").extract_first()
                        offerings_instructors = section.xpath("./td[4]/text()").extract() # This is list
                        quota = (section.xpath("./td[5]//text()").extract_first())
                        enrol = (section.xpath("./td[6]//text()").extract_first())
                        wait = (section.xpath("./td[8]//text()").extract_first())

                        # Add Sections to course info
                        db.course.update(
                            {
                                "code": course_code,
                                # "sections.recordTime": datetime.datetime.strptime(record_time, "%Y-%m-%dT%H:%M"),
                            },
                            {
                                "$push": {
                                    "sections": {
                                        "recordTime": datetime.datetime.strptime(record_time, "%Y-%m-%dT%H:%M %z"),
                                        "sectionId": section_id,
                                        "offerings": [{
                                            "dateAndTime": offerings_date_and_time,
                                            "room": offerings_room,
                                            "instructors": offerings_instructors,
                                        }],
                                        "quota": quota,
                                        "enrol": enrol,
                                        "wait": wait
                                    }
                                }
                            },
                            # upsert=True,
                        )

                    # section is not newsect. Add new "offering" to previous section
                    else:
                        offerings_date_and_time_raw = section.xpath("./td[1]/text()").extract()
                        offerings_date_and_time = ' '.join(offerings_date_and_time_raw)
                        offerings_room = section.xpath("./td[2]/text()").extract_first()
                        offerings_instructors = section.xpath("./td[3]/text()").extract()  # This is list

                        db.course.update(
                            {
                                "code": course_code,
                                "sections.recordTime": datetime.datetime.strptime(record_time, "%Y-%m-%dT%H:%M %z"),
                                "sections.sectionId": curr_section_id
                            },
                            {
                                "$push": {
                                    "sections.$.offerings": {
                                        "dateAndTime": offerings_date_and_time,
                                        "room": offerings_room,
                                        "instructors": offerings_instructors,
                                    }
                                }
                            },
                            # upsert=True,
                        )



                    # Sample Document Insert Script for Nested Sections Part
                    # "sections": [
                    #     {
                    #         "recordTime": new Date("2018-01-26 14:00"),
                    #     "sectionId": "L1",
                    #     "offerings": [{
                    #           "dateAndTime": "Th 03:00PM - 04:50PM",
                    #           "room": "Rm 5620, Lift 31-32 (70)",
                    #           "instructors": ["LEUNG, Wai Ting"]
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
