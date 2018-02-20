import os

DEFAULT_URL = 'http://course.cse.ust.hk/comp4332/index.html'

def run():
    # Welcome message
    print("(2) Data Crawling\n")

    choice = input("Enter a URL or a special keyword (e.g. default) >>  ")
    exec_menu(choice)


    # Main execution
    print("Data Crawling is successful and all data are inserted into the database")
    print("Warning: This is a stub.\n")

    return

def crawl(url):
    print("Crawling...")
    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()

    if ch == 'default':
        print("Crawl as default")
        crawl(DEFAULT_URL)
    else:
        try:
            print("Target: %s" % ch)
            crawl(ch)
        except:
            print("Please enter a valid URL.")

    return

