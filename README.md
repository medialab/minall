# minall

CLI tool and Python library to apply a suite of Minet's data-mining tools on a heterogenous set of URLs.

![Tests](https://github.com/medialab/minall/actions/workflows/tests.yml/badge.svg)

---

## Description

[`minet`](https://github.com/medialab/minet) is a Python library, maintained by the [médialab at Sciences Po](https://github.com/medialab/), that provides a suite of Python classes and functions to scrape data from the web and make API calls to various platforms. Normally to use `minet`, you call one of its CLI commands on a specific data set, such as a set of YouTube video IDs or a set of URLs from Instagram. What `minall` does is take advantage of `minet`'s many platform-specific tools and applies them to a heterogenous set of URLs, without needing to manually specify which API should be called. `minall` parses the input URL, activates the appropriate `minet` tools, and returns a unified set of metadata common to all the input URLs, which allows for comparative analysis.

## Enrichment

```mermaid
graph TD
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

## Install CLI / library

1. Create and activate a virtual Python environment, >= 3.11
2. Install the tool with `pip`.
   ```shell
   pip install git+https://github.com/medialab/minall.git
   ```

## Use as a CLI tool

Quick example command for a CSV dataset `input.csv` with URLs in the column `url` :

```shell
minall --config minetrc.yml --output-dir ./output --links input.csv --url-col url
```

With the option `--config`, you provide a [Minet configuration file](https://github.com/medialab/minet/blob/master/docs/cli.md#minetrc), which contains the necessary API keys for the metadata collection.

`./config.yml`

```yml
---
buzzsumo:
  token: "TOKEN" # Used as --token for `minet bz` commands
crowdtangle:
  token: "TOKEN" # Used as --token for `minet ct` commands
  rate_limit: 10 # Used as --rate-limit for `minet ct` commands
youtube:
  key: "KEY" # Used as --key for `minet yt` commands
```

```shell
usage: Minall [-h] [--database DATABASE] [--config CONFIG] --output-dir OUTPUT_DIR --links LINKS_FILE --url-col URL_COL [--shared-content SHARED_CONTENT_FILE] [--buzzsumo-only]

options:
  -h, --help            show this help message and exit
  --database DATABASE   [Optional] Path to SQLite database. If not given, database written to memory.
  --config CONFIG       [Optional] Path to configuration file. If not given, environment variables are expected.
  --output-dir OUTPUT_DIR
                        [Required] Path to directory in which a links and shared_content file will be written.
  --links LINKS_FILE    [Required] Path to links file.
  --url-col URL_COL     [Required] Name of URL column in links file.
  --shared-content SHARED_CONTENT_FILE
                        [Optional] Path to shared_content file.
  --buzzsumo-only       [Optional] Flag indicating only Buzzsumo API will be called on links file.
```

A special feature of `minall` is that it creates an SQL database during the enrichment process and updates metadata provided at input without losing any data. For example, if you have already used `minall` on a set of URLs, you can update those metrics by inputting the files that minall previously produced. This is useful because, if a URL has been deleted or if an API no longer returns a response for it, `minall`'s result files will keep the old data, rather than overwriting it with null values.

### Output fields for enriched URLs file (`links.csv`)

- `url` : the URL that will be used for the metadata collection
- `domain` : the URL's domain name
- `work_type` : a [Schema.org](https://schema.org/CreativeWork) classification for the URL as a CreativeWork
- `duration` : if the URL is of a video, the video's duration
- `identifier` : the identifier given to the URL via a platform (i.e. YouTube ID, Twitter user ID)
- `date_published` : date (YYYY-MM-DD) when the URL's content was originally published
- `date_modified` : date (YYYY-MM-DD) when the URL's content was last updated
- `country_of_origin` : if the URL is of a YouTube channel, the channel's registered country
- `abstract` : abbreviated description of the URL's content
- `keywords` : keywords associated with the URL
- `title` : title given to the URL's content
- `text` : the URL's main textual content
- `hashtags` : hashtags associated with the URL
- `creator_type` : a [Schema.org](https://schema.org/creator) or [De Facto](https://github.com/AFP-Medialab/defacto-rss/blob/main/Defactor_rss.adoc) classification for the creator of the URL's content
- `creator_date_created` : if the URL's content was created by a social media account, the date of the account's creation on the site
- `creator_location_created` : if the URL's content was created by a social media account, the country in which the account is registered
- `creator_identifier` if the URL's content was created by a social media account, the social media platform's identifier for the account
- `creator_facebook_follow` : if the URL is a Facebook post, the number of Facebook followers the creator's account has
- `creator_facebook_subscribe` : if the URL is a Facebook post, the number of Facebook subscribers the creator's account has
- `creator_twitter_follow` : if the URL is a Tweet, the number of Twitter / X followers the creator's account has
- `creator_youtube_subscribe` : if the URL is a YouTube video, the number of YouTube channel subscribers the channel has
- `creator_create_video` : if the URL is a YouTube video, the number of videos the YouTube channel has created
- `creator_name` : the name of the creator of the URL's content
- `creator_url` : if the URL is a social media post, a link to the creator's account page on the platform
- `facebook_comment` : number of comments the URL has received on Facebook
- `facebook_like` : number of likes the URL has received on Facebook
- `facebook_share` : number of shares the URL has received on Facebook
- `pinterest_share` : number of shares the URL has received on Pinterest
- `twitter_share` : number of shares the URL has received on Twitter / X
- `tiktok_share` : number of shares the URL has received on TikTok
- `tiktok_comment` : number of comments the URL has received on TikTok
- `reddit_engagement` : metric engagement the URL has received on Reddit
- `youtube_watch` : number of views the URL has received on YouTube
- `youtube_comment` : number of comments the URL has received on YouTube
- `youtube_like` : number of likes the URL has received on YouTube
- `youtube_favorite` : number of favorite reactions the URL has received on YouTube
- `youtube_subscribe` : if the URL is of a YouTube channel, the channel's number of subscribers
- `create_video`: if the URL is of a YouTube channel, the number of videos the channel has created
