import os

ENV_VARS_CONFIG = {
    "buzzsumo": {"token": os.getenv("BUZZSUMO_TOKEN")},
    "crowdtangle": {
        "token": os.getenv("CROWDTANGLE_TOKEN"),
        "rate_limit": 10,
    },
    "youtube": {"key": os.getenv("YOUTUBE_KEY")},
}
