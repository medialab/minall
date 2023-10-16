from collections import namedtuple

CrowdTangleResult = namedtuple(
    "CrowdTangleResult",
    field_names=["link_id", "url", "FacebookPost"],
    defaults=[None for _ in range(3)],
)
