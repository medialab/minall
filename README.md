# minall

CLI tool and Python library to apply a suite of Minet's data-mining tools on a heterogenous set of URLs.

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

To enrich a set of URLs in CSV `input.csv` and to write the results in directory `output/` in your current working directory, run the following command:

```shell
minall --input-links input.csv --config-file config.json --output-dir ./output
```

The input CSV file needs to have the columns `link_id` and `url`. (Future development: allow user to specify column names)

| link_id  | url         |
| -------- | ----------- |
| ID/12345 | example.com |

With the option `--config-file`, you will need to provide a JSON-formatted configuration file, which contains the necessary API keys for the metadata collection.

`./config.json`

```json
{
  "buzzsumo": {
    "token": "MY_BZ_TOKEN"
  },
  "crowdtangle": {
    "token": "MY_CT_TOKEN",
    "rate_limit": 10
  },
  "youtube": {
    "key": "MY_YT_API_KEY"
  }
}
```

A special feature of `minall` is that it creates an in-memory SQL database during the enrichment process and updates any metadata provided at input without losing any data. For example, if you have already used `minall` on a set of URLs, you can update those metrics by inputting the previous run's out-files. This is useful because, if a URL has been deleted or an API no longer returns a response for it, `minall`'s result files will keep the old data, rather than overwriting it with null values.

### Data fields for enriched URLs file

- `link_id` : some kind of unique identifier, which can refer to the URL or to some other entity to which the URL relates
- `url` : the URL that will be used for the metadata collection
- `domain` : the URL's domain name
- `type` : a [Schema.org](https://schema.org/CreativeWork) classification for the URL as a CreativeWork
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
