import re

from fcfb.utils.setup import setup
from fcfb.utils.exception_handling import async_exception_handler, RedditAPIError

config_data, r, logger = setup()
subreddit = r.subreddit(config_data['reddit']['subreddit'])
wiki_page = subreddit.wiki["games"]


@async_exception_handler()
def crawl():
    try:
        # Parse the table using regular expressions
        table_pattern = re.compile(r'\|(.+?)\|')
        table_rows = wiki_page.content_md.split('\n')[3:-2]  # Exclude header and footer

        # Define the column names
        columns = ["Away", "Home", "Score", "Quarter", "Time", "Playclock", "Deadline", "Status", "Thread", "Admin"]

        # Create a list to store the dictionaries
        data_list = []

        # Iterate through each row and extract data
        for row in table_rows:
            row_data = table_pattern.findall(row)
            data_dict = dict(zip(columns, row_data))
            if data_dict
            data_list.append(data_dict)

        # Print the result
        for entry in data_list:
            print(entry)
    except RedditAPIError as e:
        raise RedditAPIError(e)
