This part of the project documentation focuses on an
**understanding-oriented** approach. You'll get a
chance to read about the background of the project,
as well as reasoning about how it was implemented.

> **Note:** Expand this section by considering the
> following points:

- Give context and background on your library
- Explain why you created it
- Provide multiple examples and approaches of how
  to work with it
- Help the reader make connections
- Avoid writing instructions or technical descriptions
  here

## Data fields

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

Example from [https://realpython.com/python-project-documentation-with-mkdocs/](https://realpython.com/python-project-documentation-with-mkdocs/)
