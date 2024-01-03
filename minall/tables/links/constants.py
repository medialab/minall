# minall/tables/links/constants.py

from dataclasses import dataclass


@dataclass
class LinksConstants:
    """Dataclass to manage 'links' table.

    This dataclass manages the 'links' table's required column names and their data types. Being a dataclass, however, the instance of the class can also be subsequently modified to include other column names (and their data types) according to the input data.

    For example, if the input dataset's target URL column has a name other than 'url,' such as the name 'cleaned_urls,' this dataclass's `dtypes` and `col_names` attributes can be modified to preserve the data file's additional column names. However, the column 'url' must indicate the target URLs. If the input dataset does not have a 'url' column, one will be created. If it already has a 'url' column, that will be parsed and treated as the target URL column.

    Attributes:
        table_name (str): Name of the table. Default = "links".
        primary_key (str): Text string of primary key. Default = "url".
        pk_list (list): List of primary key columns. Default = ["url"]
        dtypes (dict): Key-value pairs of column names and SQLite data type descriptions.
        col_names (list): List of column names.
    """

    table_name: str = "links"
    primary_key: str = "url"
    pk_list = ["url"]
    dtypes = {
        "url": "TEXT",
        "domain": "TEXT",
        "work_type": "TEXT",
        "duration": "TEXT",
        "identifier": "TEXT",
        "date_published": "TEXT",
        "date_modified": "TEXT",
        "country_of_origin": "TEXT",
        "abstract": "TEXT",
        "keywords": "TEXT",
        "title": "TEXT",
        "text": "TEXT",
        "hashtags": "TEXT",
        "creator_type": "TEXT",
        "creator_date_created": "TEXT",
        "creator_location_created": "TEXT",
        "creator_identifier": "TEXT",
        "creator_facebook_follow": "INTEGER",
        "creator_facebook_subscribe": "INTEGER",
        "creator_twitter_follow": "INTEGER",
        "creator_youtube_subscribe": "INTEGER",
        "creator_create_video": "INTEGER",
        "creator_name": "TEXT",
        "creator_url": "TEXT",
        "facebook_comment": "INTEGER",
        "facebook_like": "INTEGER",
        "facebook_share": "INTEGER",
        "pinterest_share": "INTEGER",
        "twitter_share": "INTEGER",
        "tiktok_share": "INTEGER",
        "tiktok_comment": "INTEGER",
        "reddit_engagement": "INTEGER",
        "youtube_watch": "INTEGER",
        "youtube_comment": "INTEGER",
        "youtube_like": "INTEGER",
        "youtube_favorite": "INTEGER",
        "youtube_subscribe": "INTEGER",
        "create_video": "INTEGER",
    }
    col_names = dtypes.keys()
