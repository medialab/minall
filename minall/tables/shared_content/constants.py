from dataclasses import dataclass

from minall.tables.links.constants import LinksConstants


@dataclass
class ShareContentConstants:
    table_name = "shared_content"
    primary_key = "post_url,content_url"
    pk_list = ["post_url", "content_url"]
    dtypes = {
        "post_url": f"VARCHAR REFERENCES {LinksConstants.table_name}(url) ON UPDATE CASCADE",
        "media_type": "VARCHAR",
        "content_url": "VARCHAR",
        "height": "INTEGER",
        "width": "INTEGER",
    }
    col_names = dtypes.keys()
