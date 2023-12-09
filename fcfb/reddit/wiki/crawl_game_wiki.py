import re

from fcfb.utils.setup import setup
from fcfb.utils.exception_handling import async_exception_handler, RedditAPIError

config_data, r, logger = setup()
subreddit = r.subreddit(config_data['reddit']['subreddit'])
wiki_page = subreddit.wiki["games"]


@async_exception_handler()
async def get_ongoing_games():
    try:
        # Exclude header and footer
        table_rows = wiki_page.content_md.split('\n')[3:-2]

        # Define the column names
        columns = ["Away", "Home", "Score", "Quarter", "Time", "Playclock", "Deadline", "Status", "Thread", "Admin"]

        # Create a list to store the dictionaries
        data_list = []

        # Patterns to filter out
        exclude_patterns = ["**FBS**", "**FCS**", "***", ":-:"]

        # Regex pattern for extracting text outside of []
        text_outside_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        # Regex patterns for extracting desired information
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        # Iterate through each row and extract data
        for row in table_rows:
            row_data = [item.strip() for item in row.split('|')]

            # Skip empty rows
            if not any(row_data) or row_data == columns:
                continue

            # Skip rows containing specific patterns
            if any(pattern in row for pattern in exclude_patterns):
                continue

            data_dict = dict(zip(columns, row_data))

            # Remove the "Admin" key from the dictionary
            data_dict.pop("Admin", None)
            data_dict.pop("Status", None)

            # Extract information from the markdown hyperlinks
            for key in ["Away", "Home"]:
                match = text_outside_pattern.search(data_dict[key])
                if match:
                    data_dict[key] = match.group(1)

            for key in ["Playclock", "Deadline", "Thread"]:
                match = link_pattern.search(data_dict[key])
                if match and key != "Thread":
                    data_dict[key] = match.group(1)
                if key == "Thread":
                    data_dict[key] = match.group(2)

            data_list.append(data_dict)

        return data_list
    except RedditAPIError as e:
        raise RedditAPIError(e)