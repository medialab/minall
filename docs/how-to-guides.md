## Using `minall` from the command line

### Context

Let's say we have a set of 2 URLs, one is a web page and the other is a YouTube video.

`data.csv`

|target_url|
|---|
|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/|
|https://www.youtube.com/watch?v=BTvfWbAjh1w|

And we've stored the data file in our current working directory under the name `data.csv`.

```
.
│
└── data.csv
```

### Set up files

For the purposes of this demonstration, we'll need to create an additional file, `config.yml`.

```
.
│
├── config.yml
│
└── data.csv
```

This YAML file is a configuration file [in the same format as that used in `minet`](https://github.com/medialab/minet/blob/master/docs/cli.md#minetrc-config-files), and it contains API keys.

`config.yml`
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

### Set up `minall`

Now we'll install `minall`. Create and activate a virtual Python environment, using version 3.11. Then install the tool with pip.

```shell
$ pip install git+https://github.com/medialab/minall.git
```

### Run

Finally, let's run the workflow on our dataset. We'll set the parameters as follows:

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
Calling Buzzsumo API   2/2 0:00:05
```

### Results

The results will be written to files in the directory whose path was given to the parameter `--output-dir`.

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