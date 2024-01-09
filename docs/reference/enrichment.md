---
icon: material/folder-outline
---

# Enrichment tools

The enrichment workflow uses scraping and `minet`'s API clients to collect data about URLs and associated shared content in the SQLite database's `links` table and `shared_content` table, respectively. The collection method that `minall` deploys is dependent on the URL's domain name.

The URLs in the SQLite database's `links` table are parsed using the [`ural`](https://github.com/medialab/ural) Python library and grouped in the following subsets:

Subsets of URLs

|subset|dataclass|module|
|--|--|--|
|URLs from Facebook|**Normalized Facebook Post Data**|`minall.enrichment.crowdtangle.get_data`|
|URLs from YouTube|**Normalized YouTube Video Data**, **Normalized YouTube Channel Data**|`minall.enrichment.youtube.get_data`|
URLs from other social media platforms (because they cannot be scraped)|NA|`minall.enrichment.other_social_media.add_data`|
|URLs not from social media platforms (they can be scraped)|**Normalized Scraped Web Page Data**|`minall.enrichment.article_text.get_data`|

If the user has a Buzzsumo API token, all URLs, regardless of grouping by domain name, are searched in the Buzzsumo database.

All URLs

|subset|dataclass|module|
|--|--|--|
all URLs|**Normalized Buzzsumo Exact URL Data**|`minall.enrichment.buzzsumo.get_data`|

Due to the diversity of data available for different types of URLs and provided by different data sources, an important step in all the enrichment procedures is normalizing the data. Each target URL's metadata, regardless of its domain name, must conform to the SQLite database's `links` table. Such harmonization of data fields constitutes an important feature of the `minall` workflow and is not (yet) something replicated in `minet`.

The following table illustrates which of each data source's data fields are matched to which column in the database's `links` table.

|`links` SQL table|Normalized Scraped Web Page Data|Normalized Buzzsumo Exact URL Data|Normalized Facebook Post Data|Normalized YouTube Video Data|Normalized YouTube Channel Data|
|--|--|--|--|--|--|
|url (TEXT)|X|X|X|X|X|
|domain (TEXT)||X|X ("facebook.com")|X ("youtube.com")|X ("youtube.com")|
|work_type (TEXT)|X ("WebPage")|X ("WebPage", "Article", "VideoObject")|X ("SocialMediaPosting", "ImageObject", "VideoObject")|X ("VideoObject")|X ("WebPage")|
|duration (TEXT)||X|X|X||
|identifier (TEXT)|||X|X|X|
|date_published (TEXT)|X|X|X|X|X|
|date_modified (TEXT)|||X|||
|country_of_origin (TEXT)|||||X|
|abstract (TEXT)|||X|X|X|
|keywords (TEXT)||||X|X|
|title (TEXT)|X|X|X|X|X|
|text (TEXT)|X||X|||
|hashtags (TEXT)||||||
|creator_type (TEXT)|||X ("defacto:SocialMediaAccount")|X ("WebPgae")||
|creator_date_created (TEXT)||||X||
|creator_location_created (TEXT)|||X|X||
|creator_identifier (TEXT)||X|X|X||
|creator_facebook_follow (INTEGER)|||||
|creator_facebook_subscribe (INTEGER)|||X||
|creator_twitter_follow (INTEGER)|||||
|creator_youtube_subscribe (INTEGER)||||X||
|creator_create_video (INTEGER)||||X||
|creator_name (TEXT)||X|X|X||
|creator_url (TEXT)|||X|||
|facebook_comment (INTEGER)||X|X|||
|facebook_like (INTEGER)|||X|||
|facebook_share (INTEGER)||X|X|||
|pinterest_share (INTEGER)||X||||
|twitter_share (INTEGER)||X||||
|tiktok_share (INTEGER)||X||||
|tiktok_comment (INTEGER)||X||||
|reddit_engagement (INTEGER)||X||||
|youtube_watch (INTEGER)||X||X||
|youtube_comment (INTEGER)||||X||
|youtube_like (INTEGER)||X||X||
|youtube_favorite (INTEGER)||||||
|youtube_subscribe (INTEGER)|||||X|
|create_video (INTEGER)|||||X|

_Note: `creator_facebook_follow` and `hashtags` do not have any data field feeding to them. `hashtags` was fed by the Twitter API, which has been depreciated. I still need to confirm the use of `creator_facebook_follow` (Facebook accounts' `FollowAction` might have been made redundant by the `SubscribeAction`)._

---

::: minall.enrichment.enrichment
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: minall.enrichment.utils
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: minall.enrichment.buzzsumo
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 2

::: minall.enrichment.buzzsumo.normalizer
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.buzzsumo.client
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.buzzsumo.get_data
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.buzzsumo.contexts
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.crowdtangle
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 2

::: minall.enrichment.crowdtangle.normalizer
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.crowdtangle.client
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.crowdtangle.get_data
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.crowdtangle.contexts
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.crowdtangle.exceptions
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.youtube
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 2

::: minall.enrichment.youtube.normalizer
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.youtube.get_data
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.youtube.context
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.other_social_media
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 2

::: minall.enrichment.other_social_media.add_data
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.article_text
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 2

::: minall.enrichment.article_text.normalizer
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.article_text.scraper
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.article_text.get_data
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.enrichment.article_text.contexts
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3
