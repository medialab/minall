import duckdb
from duckdb import DuckDBPyConnection
from ural.facebook import is_facebook_url
from ural.youtube import is_youtube_url

from minall.enrichment.article_text import get_article_text
from minall.enrichment.buzzsumo import get_buzzsumo_data
from minall.enrichment.buzzsumo.normalizer import get_domain
from minall.enrichment.crowdtangle import get_facebook_post_data
from minall.enrichment.other_social_media import add_type_data
from minall.enrichment.youtube import get_youtube_data
from minall.links.links_table import LinksTable
from minall.shared_content.shared_content_table import SharedContentTable
from minall.utils import parse_env_vars

bar = "\n===============\n"


def enrich_links(connection: DuckDBPyConnection):
    # Pull data
    data = [
        (url, link_id)
        for url, link_id in (
            duckdb.table("links", connection).select("url,link_id").fetchall()
        )
    ]

    # Parse environment variables
    env_vars = parse_env_vars()
    if not env_vars.outdir:
        raise KeyError
    results_file = env_vars.outdir.joinpath("links.csv")
    shared_content_file = env_vars.outdir.joinpath("shared_content.csv")

    # Prepare database's tables
    links_table = LinksTable(connection=connection)
    shared_content_table = SharedContentTable(connection=connection)

    if not env_vars.bz_only:
        youtube_links = [
            (url, link_id) for url, link_id in data if is_youtube_url(url=url)
        ]
        # ---- YOUTUBE VIDEOS AND CHANNELS --- #
        if len(env_vars.yt_keys) > 0 and len(youtube_links) > 0:
            print(f"{bar}Requesting data from YouTube API")
            # Add metadata from the YouTube API to the database's links that come from YouTube
            get_youtube_data(
                data=youtube_links,
                keys=env_vars.yt_keys,
                outfile=results_file,
            )
            links_table.insert(infile=results_file)

        # ---- FACEBOOK POSTS --- #
        facebook_links = [
            (url, link_id) for url, link_id in data if is_facebook_url(url=url)
        ]
        if (
            env_vars.ct_token is not None
            and env_vars.ct_rate_limit is not None
            and len(facebook_links) > 0
        ):
            # Add metadata from the CrowdTangle API to the database's links that come from Facebook
            print(f"{bar}Requesting data from CrowdTangle API")
            get_facebook_post_data(
                data=facebook_links,
                token=env_vars.ct_token,
                rate_limit=env_vars.ct_rate_limit,
                appearances_outfile=results_file,
                shared_content_outfile=shared_content_file,
            )
            links_table.insert(infile=results_file)
            shared_content_table.insert(infile=shared_content_file)

        # --- OTHER SOCIAL MEDIA -- #
        # Add 'SocialMediaPosting' if type value is null
        other_social_media = [
            (url, link_id)
            for url, link_id in data
            if get_domain(url=url)
            in [
                "facebook.com",
                "youtube.com",
                "tiktok.com",
                "instagram.com",
                "twitter.com",
                "snapchat.com",
            ]
        ]
        add_type_data(data=other_social_media, outfile=results_file)
        links_table.insert(infile=results_file)

        # --- ARTICLE TEXTS -- #
        print(f"{bar}Scrape article text")
        links_to_scrape = [
            (url, link_id)
            for url, link_id in data
            if get_domain(url=url)
            not in [
                "facebook.com",
                "youtube.com",
                "tiktok.com",
                "instagram.com",
                "twitter.com",
                "snapchat.com",
            ]
        ]
        get_article_text(data=links_to_scrape, outfile=results_file)  # type: ignore
        links_table.insert(infile=results_file)

    # ---- EVERYTHING --- #
    # Replace any remaining null values with metadata from Buzzsumo API to database's links
    if env_vars.bz_token:
        print(f"{bar}Requesting data from Buzzsumo API")
        get_buzzsumo_data(
            data=data,
            token=env_vars.bz_token,
            outfile=results_file,
        )
        links_table.insert(infile=results_file)
