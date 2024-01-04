The main problem this project is designed to solve is the collection and updating of metadata for a _diverse_ dataset of URLs.

## Use as CLI

How do you use `minall` on our dataset from the command line?

### Set-up

Create and activate a virtual Python environment, using version 3.11. Then install `minall`.
```shell
$ pip install git+https://github.com/medialab/minall.git
```

For the purposes of this demonstration, create two files in your current working directory.

```
.
│
├── config.yml
│
└── data.csv
```

The first is a YAML [configuration file](https://github.com/medialab/minet/blob/master/docs/cli.md#minetrc-config-files), which contains API keys.

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

The second is the dataset of target URLs.

`data.csv`

|target_url|
|---|
|https://archive.fosdem.org/2020/schedule/event/open_research_web_mining/|
|https://www.youtube.com/watch?v=BTvfWbAjh1w|


### Run

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