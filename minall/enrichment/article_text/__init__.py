# minall/enrichment/article_text/__init__.py

"""Enrichment workflow's HTML scraping features.

Modules exported by this package:

- `normalizer`: Dataclass to normlalize minet's Trafilatura result object.
- `contexts`: Context manager for scraper's CSV writers, multi-threader, and progress bar.
- `get_data`: Function that runs all of the scraping process.
- `scraper`: Class and helper function for scraping HTML.
"""

from minall.enrichment.article_text.get_data import get_data as get_article_text
