# minall/enrichment/other_social_media/add_data.py

"""Module contains function to write web content ontological subtype information to CSV.

The module contains a function that write the ontological subtype "SocialMediaPosting" and the related target URL to a CSV, which will be inserted into the 'links' SQL table.
"""


import csv
from pathlib import Path
from typing import List

from minall.tables.links import LinksConstants


def add_data(data: List[str], outfile: Path):
    """For the set of target URLs, write the URL and the category "SocialMediaPosting" to a CSV row for insert into the 'links' SQL table.

    Args:
        data (List[str]): Target URLs.
        outfile (Path): Path to CSV file for links.
    """
    with open(outfile, "w") as f:
        writer = csv.DictWriter(f, fieldnames=LinksConstants.col_names)
        writer.writeheader()
        [
            writer.writerow({"url": url, "work_type": "SocialMediaPosting"})
            for url in data
        ]
