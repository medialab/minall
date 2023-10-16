from minet.extraction import TrafilaturaResult


class ArticleNormalizer:
    def __init__(self) -> None:
        pass

    def __call__(self, result: TrafilaturaResult, url: str, link_id: str) -> dict:
        keep = {
            "link_id": link_id,
            "url": url,
            "title": result.title,
            "type": "WebPage",
            "text": result.content,
            "date_published": result.date,
        }

        return keep
