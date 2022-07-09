import pyfiglet

def progress_bar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#'):
    """
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def print_progress_bar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print('{} |{}| {}% {}'.format(prefix, bar, percent, suffix), end='\r')

    # Initial Call
    print_progress_bar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        print_progress_bar(i + 1)
    print()


def start_message():
    ascii_banner = pyfiglet.figlet_format("shkence.bot")
    print(ascii_banner)
    print("""
    Version: 2.1

    Welcome admin!
    Share your news posts directly to Instagram with ease.
    
    You can choose to:

    1.  Full run
    2.  Scraper
    3.  Generate posts and stories
    4.  Generate only posts
    5.  Generate only stories
    6.  Post posts and stories
    7.  Post only posts
    8.  Post only stories
    9.  Clear workspace
    10. Update
    11. Login
    12. Exit

    What would you like to do?

    """)
    return int(input())
    