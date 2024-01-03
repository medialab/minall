::: minall.tables
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 1

With SQLite, the module `minall/tables` manages the data during the enrichment process, from the data input at the start to the updated version exported at the end. The process relies on the following two tables:

1. The `links` table, which is the backbone of the enrichment, stores the target URLs and their enriched metadata.

2. The `shared_content` table, which is optional, stores URLs pointing to content shared via the target URLs' content.

As illustrated in the figure below, the two tables are related. The target URL (`url`) in the `links` table refers to the `post_url` in the `shared_content` table. A target URL (`url`) in the `links` table can share 0 or more items. Depending on the URLs dataset, it could be the case that no entities in the `links` table have shared any content. All entities in the `shared_content` must relate to at least one entity in the `links` table. Content in the `shared_content` table can have been shared by 1 or more URLs in the `links` table.

``` mermaid
erDiagram
    LINKS }|--o{ SHARED_CONTENT : shares
    LINKS {
        text url PK
        text domain
        text work_type
        text duration
        text identifier
        text date_published
        text date_modified
        text country_of_origin
        text abstract
        text keywords
        text title
        text text
        text hashtags
        text creator_type
        text creator_date_created
        text creator_identifier
        integer creator_facebook_follow
        integer creator_facebook_subscribe
        integer creator_twitter_follow
        integer creator_youtube_subscribe
        integer creator_create_video
        text creator_name
        text creator_url
        integer facebook_comment
        integer facebook_like
        integer facebook_share
        integer pinterest_share
        integer twitter_share
        integer tiktok_share
        integer tiktok_comment
        integer reddit_engagement
        integer youtube_watch
        integer youtube_comment
        integer youtube_like
        integer youtube_favorite
        integer youtube_subscribe
        integer create_video
    }
    SHARED_CONTENT {
        text post_url PK
        text content_url PK
        text media_type
        integer height
        integer width
    }
```

---

::: minall.tables.links
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: minall.tables.links.constants
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.tables.shared_content
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: minall.tables.shared_content.constants
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: minall.tables.base
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

::: minall.tables.utils
    handler: python
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2