from collections import namedtuple
from datetime import datetime

BEGINDATE = int(datetime.strptime("2020-01-01", "%Y-%m-%d").timestamp())

ENDDATE = int(
    datetime.strptime(
        datetime.utcnow().isoformat().split("T")[0], "%Y-%m-%d"
    ).timestamp()
)

BuzzsumoResult = namedtuple(
    "MinetResult", field_names=["link_id", "url", "BuzzsumoExactURL"]
)
