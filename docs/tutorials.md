This tutorial will walk you through a real-life example of why and how to use `minall`.

## Example dataset

Let's say we have a list of URLs whose basic metadata and propagation online we want to study. We've stored those URLs in a CSV file under the column `target_url`. Both are about Guillaume Plique's presentation of `minet` at the FOSDEM conference in 2020. One of the URLs is of a web page from the conference's site and the other is a YouTube video, published by the conference organization.

|target_url|
|---|
|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/|
|https://www.youtube.com/watch?v=BTvfWbAjh1w|

If using `minet`, we'd need to run 2 different commands based on the type of URL, `minet yt` for the YouTube video and `minet fetch` / `minet extract` for the web page. When working with just 2 URLs, that's not such a problem. However, let's imagine our list of URLs is much bigger than these 2 rows and that we don't aleady know what type of content is in it. Plus, we want to be able to work with the collected data as a set, comparing identical attributes of both the web page and the YouTube video. `minet`'s commands write their results in data fields that are unique to each sub-command. This idiosyncracy complicates comparative analysis. What `minall` does, in one single command, is output fewer but harmonized data fields, which apply to all types of web content.

## Set up required files

For the purposes of this tutorial, let's create two files in our current working directory. One is the dataset described above (`data.csv`) and the second is a YAML configuation file, which is the [same as that used in `minet`](https://github.com/medialab/minet/blob/master/docs/cli.md#minetrc-config-files) (`config.yml`).

```
.
│
├── config.yml
│
└── data.csv
```

Because API keys are not always available, `minall` does not require them to function. However, the majority of its enrichments depend on various APIs and, if not using any, we might as well just use `minet`'s scraping commands directly.

Let's assume we only have a YouTube API key, which is free and can be [obtained from Google](https://developers.google.com/youtube/v3/getting-started) with a Gmail account. We'll set up the configuration file like so:

`config.yml`
```yaml
---
youtube:
  key: "XXXX"
```

### API keys

Technically, `minall` does not require a configuration file to function because it can skip over any enrichment methods that require API keys the user did not provide. Only the dataset file, which contains target URLs, is absolutley necessary. However, the purpose of using `minall` is to take advantage of `minet`'s many API clients in one single command. Thus, though not important for this tutorial, it's best if you can fill out the entire configuration file below:

  ```yaml
  ---
  buzzsumo:
    token: "XXXX" # Used as --token for `minet bz` commands
  crowdtangle:
    token: "XXXX" # Used as --token for `minet ct` commands
    rate_limit: 50 # Used as --rate-limit for `minet ct` commands
  youtube:
    key: "XXXX" # Used as --key for `minet yt` commands
  ```

- YouTube's API key can be [requested from Google](https://developers.google.com/youtube/v3/getting-started).
- CrowdTangle's API key can be [requested from Meta](https://help.crowdtangle.com/en/articles/4302208-crowdtangle-for-academics-and-researchers)
- Buzzsumo's API key can be [purchased from Buzzsumo](http://help.buzzsumo.com/en/articles/3883145-api-access-for-paid-web-app-subscriptions).

## Install `minall`

Because `minall` is written entirely in Python, we need to [have Python installed](https://docs.python-guide.org/starting/installation/), specifically version 3.11-something. We also need to create a ["virtual" Python environment](https://docs.python-guide.org/dev/virtualenvs/).

In a shell with the virtual Python environment activated, install `minall` from GitHub.

```shell
$ pip install git+https://github.com/medialab/minall.git
```

Let's check that we installed it correctly by entering the command `minall --help`. The following should show up in the console:

```shell
usage: Minall [-h] [--database DATABASE] [--config CONFIG] --output-dir
              OUTPUT_DIR --links LINKS_FILE --url-col URL_COL
              [--shared-content SHARED_CONTENT_FILE] [--buzzsumo-only]

options:
  -h, --help            show this help message and exit
  --database DATABASE   [Optional] Path to SQLite database. If not given,
                        database written to memory.
  --config CONFIG       [Optional] Path to configuration file. If not
                        given, environment variables are expected.
  --output-dir OUTPUT_DIR
                        [Required] Path to directory in which a links and
                        shared_content file will be written.
  --links LINKS_FILE    [Required] Path to links file.
  --url-col URL_COL     [Required] Name of URL column in links file.
  --shared-content SHARED_CONTENT_FILE
                        [Optional] Path to shared_content file.
  --buzzsumo-only       [Optional] Flag indicating only Buzzsumo API will
                        be called on links file.
```

## Run

Now we're ready to run `minall` on our dataset of URLs about Guillaume Plique's FOSDEM presentation. The `minall` command will produce 2 new CSV files, one has all of the dataset's URLs and their newly collected metadata (`links.csv`), the other has URLs pointing to media content that was embedded inside the target URL's web content (`shared_content.csv`).

> _Note: Currently, `minall` only records the URLS of embedded media content when it's shared inside a Facebook post. This feature, however, should be expanded to include media (images, videos) shared inside articles._

We'll ask `minall` to write the 2 new files to a directory named `output`, which will eventually (at the end of the workflow) change our current working directory like so:

```
.
│
├── config.yml
│
├── data.csv
│
└── output/
    ├── links.csv
    └── shared_content.csv
```

To run `minall`, we'll call the command with the following options:

- `--config` : Path to the YAML configuration file, `./config.yml`
- `--links` : Path to the dataset of target URLs, `./data.csv`
- `--url-col`: Name of the column in the dataset file with the target URLs. `target_url`
- `--output-dir`: Path to where `minall` will export its results. `./output/`

```shell
$ minall --config config.yml --output-dir output/ --links data.csv --url-col target_url
```

While `minall` is running, we'll see the following commands proceed:

```
Querying YouTube videos   1/1 0:00:00
Querying YouTube channels   1/1 0:00:00
Scraping webpage   1/1 0:00:00
```

Had our dataset included URLs from Facebook and had we provided a CrowdTangle API key, `minall` would have also called the CrowdTangle API. But because our dataset only included the URL of a web page and of a YouTube video, it ran through only its YouTube API and scraping utilities. Had we provided a Buzzsumo API key, it would have also called the Buzzsumo API twice, searching for both the web page's URL and the YouTube video's URL in Buzzsumo's database.

## Understanding the results

A portion of the `output/links.csv` file that `minall` created is shown below.

|target_url|url|domain|work_type|duration|identifier|date_published|...|title|
|--|--|--|--|--|--|--|--|--|
|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/|fosdem.org|WebPage|||2020-02-01|...|FOSDEM 2020 - Empowering social scientists with web mining tools|
|https://www.youtube.com/watch?v=BTvfWbAjh1w|https://www.youtube.com/watch?v=BTvfWbAjh1w|youtube.com|VideoObject|1431|BTvfWbAjh1w|2021-07-12T06:53:30|...|Empowering social scientists with web mining tools Why and how to enable researchers to perform com…|

We see that `minall` read the columns in our data file, specifically `target_url`, conserved the original column, and appended the enrichment's additional columns to the right.

We also see that FOSDEM published the announcement of Guillaume Plique's presentation about `minet` on their website just before the conference, on 1 February 2020. However, FOSDEM uploaded a video of the presentation to YouTube over a year later, on 12 July 2021. Though we have no way of knowing how many people viewed the web page, YouTube's API allows us know how many people viewed, commented on, and liked the video.

|target_url|...|reddit_engagement|youtube_watch|youtube_comment|youtube_like|
|--|--|--|--|--|--|
|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/||||||
|https://www.youtube.com/watch?v=BTvfWbAjh1w|||69|0|3|


### Buzzsumo

Because we didn't provide `minall` with a Buzzsumo API key, it was unable to ask Buzzsumo if the database had cached metadata about either of our dataset's URLs. Had we included Buzzsumo in our configuration file, `minall` would have told us that Buzzsumo does have information about the FOSDEM video on YouTube; however, it does not have any information about the web page on FOSDEM's site.

We know when Buzzsumo has stored information about one of our target URLs because certain data fields in the `links.csv` file will have a value. For example, if we were to run `minall` again with a Buzzsumo API key in the configuration file, we would know Buzzsumo cached our dataset's YouTube video because we see values in data fields that are beyond the scope of YouTube's API, specifically `facebook_comment`, `pinterest_share`, and `twitter_share`. It is normal that some of Buzzsumo's data fields, such as `tiktok_share`, are empty even though Buzzsumo found an exact match of our target URL in its database. The fact that none of the data fields for our dataset's web page have any value means that Buzzsumo did not find the FOSDEM URL.

|target_url|...|facebook_comment|facebook_like|pinterest_share|twitter_share|tiktok_share|
|--|--|--|--|--|--|--|
|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/|||||||
|https://www.youtube.com/watch?v=BTvfWbAjh1w||0||0|0||


