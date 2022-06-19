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

        1. Run all functions (default) [1]
        2. Run only the scraper [2]
        3. Run only the post and story generator [3]
        4. Create only post images from existing scraped posts [4]
        5. Create only story images from existing scraped posts [5]
        6. Post post images and story images [6]
        7. Post only post images [7]
        8. Post only story images [8]
        9. Post only carousel images [9]
        10. Clear all posts and stories [10]
        11. Exit [11]

        What would you like to do?

    """)
    return int(input())
    