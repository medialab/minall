---
icon: material/folder-outline
---

# Enrichment tools

```mermaid
graph
A("What is the nature of the URL?")
B("Is the URL of a video?")
C["Call YouTube API for video metadata, including channel ID."]
D("Is the URL of a channel?")
E["Call YouTube API for channel metadata"]

F("Is the URL of a Facebook post?")
G["Call CrowdTangle API for post metadata"]

H("Is the URL from a media platform other than YouTube or Facebook?")
I["Assign '@type' = 'SocialMediaPosting'."]

J("Is the URL not from a social media platform?")
K["Scrape text and metadata."]

L["Call Buzzsumo API for metadata."]

A==YouTube==>B
B==Y==>C
B==N==>D
C---E
D---E
A==Facebook==>F
F---G
A==Other Social Media==>H
H---I
A==Article==>J
J---K
E---L
G---L
I---L
K---L
```

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

::: minall.enrichment.article_text
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 2

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

::: minall.enrichment.article_text.constants
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
