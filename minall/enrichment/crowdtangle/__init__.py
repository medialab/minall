# minall/enrichment/crowdtangle/__init__.py

"""Enrichment workflow's CrowdTangle data collection.

Modules exported by this package:

- `normalizer`: Dataclass to normlalize minet's CrowdTangle result object.
- `contexts`: Context manager for client's CSV writers, multi-threader, and progress bar.
- `get_data`: Function that runs all of the CrowdTangle enrichment process.
- `client`: Wrapper for minet's CrowdTangle API client that normalizes minet's result.
- `exceptions`: 
"""

from minall.enrichment.crowdtangle.get_data import get_facebook_post_data
