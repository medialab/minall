# minall/tables/shared_content/constants.py


from dataclasses import dataclass

from minall.tables.links.constants import LinksConstants


@dataclass
class ShareContentConstants:
    """Dataclass to manage 'shared_content' table.

    This dataclass manages the 'shared_content' table's required column names and their data types. Being a dataclass, however, the instance of the class can also be subsequently modified to include other column names (and their data types) according to the input data. The 'shared_content' table is meant to relate to the 'links' table, wherein the former's 'post_url' column refers to the latter's 'url' column.

    Contrary to the 'links' table, whose primary key column can be derived from any declared target URL column in the input data, the 'shared_content' table requires the input data has the two columns that jointly compose its primary key, 'post_url' and 'content_url.'

    Attributes:
        table_name (str): Name of the table. Default = "shared_content".
        primary_key (str): Text string of composite primary key. Default = "post_url,content_url".
        pk_list (list): List of comosite primary key columns. Default = ["post_url", "content_url]
        dtypes (dict): Key-value pairs of column names and SQLite data type descriptions.
        col_names (list): List of column names.
    """

    table_name = "shared_content"
    primary_key = "post_url,content_url"
    pk_list = ["post_url", "content_url"]
    dtypes = {
        "post_url": f"TEXT REFERENCES {LinksConstants.table_name}(url) ON UPDATE CASCADE",
        "media_type": "TEXT",
        "content_url": "TEXT",
        "height": "INTEGER",
        "width": "INTEGER",
    }
    col_names = dtypes.keys()
