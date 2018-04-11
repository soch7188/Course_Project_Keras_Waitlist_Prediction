
2. file list
3. file description
4. method of execution (e.g., “python main.py”)
5. known bugs of your system

README File for Phase 2
1. Group Information
    Group # 29
    1. Hu, Yao-Chieh (20216239)
    2. Kim, Ziwon    (20216497)

2. File List & Description

    FOLDER: 29_Phase4_JS        - Includes JS Script files for Phase 4
    FOLDER: 29_Phase4_PYTHON    - Includes PYTHON program files for Phase 4

    [JS script files]
    - insertions.js
        Insertion script for submission. Inserts multiple courses with sections into collection. Should have started up mongodb before insertion.
    - insertion_more.js
        Insertion script for extensive data. Use this file to show the differences in "Satisfied" field between sections.
    - query.js
        Query script for submission. Supports Query by Keyword, and Query by Waitlist Size. Should have inserted data with insertion.js before querying.
        *** INCLUDED "SATISFIED" FIELD FOR PHASE 4 ***

    [PYTHON files]
    - main.py
        Main execution file of the program. Can operate from the console.
        This file includes operations 1 and 2, which is for "DB initialization" and "Data crawling from the web" repectively.
    - menu_3.py
        This file is for querying the data. Includes "keyword search" and "waitlist size search".
    - scrapy.cfg & contents in the testCrawl folder
        Files needed for Crawling the data from the web. Most important file to note here is the "TrialPageSpider.py" file which has all the operations needed.
    - menu_4.py & menu_5.py
        Not used yet

3. Method of Execution
    [JS Scripts] (In terminal)
    (1) mongo insertion_more.js (You can use "mongo insertion.js", but this will not show any changes in the "SATISFIED" field. insertion_more.js is recommended for a more interesting result)
    (2) mongo query.js

    [PYTHON Program] (In terminal)
    (1) python main.py

4. Known bugs of your system
    None