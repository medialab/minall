# minall/enrichment/youtube/__init__.py

"""Enrichment workflow's YouTube data collection.

Modules exported by this package:

- `normalizer`: Dataclass to normlalize minet's YouTube result objects.
- `context`: Context manager for client's CSV writer and progress bar.
- `get_data`: Function that runs all of the YouTube enrichment process.
"""

from minall.enrichment.youtube.get_data import get_youtube_data
