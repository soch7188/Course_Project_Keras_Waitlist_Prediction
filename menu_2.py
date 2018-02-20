import os

DEFAULT_URL = 'http://course.cse.ust.hk/comp4332/index.html'

def run():
    # Welcome message
    print("Hello Menu 2 !\n")

    print("Enter a URL or a special keyword (e.g. default):")
    choice = input(" >>  ")
    exec_menu(choice)


    # Main execution
    print("Collection dropping and empty collection creating are successful")
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

