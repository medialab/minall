---
icon: material/folder-outline
---

# Enrichment tools

The enrichment workflow uses scraping and `minet`'s API clients to collect data about URLs in the SQLite database's `links` table. The collection method is dependent on the URL's domain name.

- URLs from Facebook -> `minall.enrichment.crowdtangle` -> **Normalized Facebook Post Data**
- URLs from YouTube -> `minall.enrichment.youtube` -> **Normalized YouTube Video Data**, **Normalized YouTube Channel Data**
- URLs from other social media platforms (because they cannot be scraped) -> `minall.enrichment.other_social_media`
- URLs not from social media platforms (they can be scraped) -> `minall.enrichment.article_text` -> **Normalized Scraped Web Page Data**
- all URLs -> `minall.enrichment.buzzsumo` -> **Normalized Buzzsumo Exact URL Data**

_Note: `creator_facebook_follow` and `hashtags` do not have any data field feeding to them. `hashtags` was fed by Twitter API, which has been depreciated. Still need to confirm `creator_facebook_follow` (Facebook account's `FollowAction` might be obsolete via `SubscribeAction`)._

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
