from dataclasses import dataclass


@dataclass
class LinksConstants:
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
