# minall/enrichment/buzzsumo/__init__.py

"""Enrichment workflow's Buzzsumo data collection.

Modules exported by this package:

- `normalizer`: Dataclass to normlalize minet's Buzzsumo result object.
- `contexts`: Context manager for client's CSV writers, multi-threader, and progress bar.
- `get_data`: Function that runs all of the Buzzsumo enrichment process.
- `client`: Wrapper for minet's Buzzsumo API client that normalizes minet's result.
"""

from minall.enrichment.buzzsumo.get_data import get_buzzsumo_data
