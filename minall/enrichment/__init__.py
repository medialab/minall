# minall/enrichment/__init__.py

"""Scripts to execute data collection.

Modules exported by this package:

- `enrichment`: Class that manages steps of data collection.
- `utils`: Module that provides helper functions for enrichment.
"""


import logging

logger = logging.getLogger("trafilatura")
logger.propagate = False

log_file = "minall.log"
logging.basicConfig(
    filename=log_file, filemode="w", encoding="utf-8", level=logging.INFO
)
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
