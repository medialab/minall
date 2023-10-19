from minall.enrichment.youtube.constants import YoutubeResults


class YoutubeNormalizer:
    def __init__(self) -> None:
        pass

    def parse_type(self, data: YoutubeResults) -> str | None:
        if data.video is None and data.channel is not None:
            return "WebPage"
        elif data.video is not None and data.channel is not None:
            return "VideoObject"

    def __call__(self, data: YoutubeResults) -> dict:
        media_type = self.parse_type(data)
        keep = {}

        # Channel
        if media_type == "WebPage":
            keep = {
                "link_id": data.link_id,
                "url": data.url,
                "domain": "youtube.com",
                "type": media_type,
                "identifier": getattr(data.channel, "id"),
                "date_published": getattr(data.channel, "published_at"),
                "country_of_origin": getattr(data.channel, "country"),
                "abstract": getattr(data.channel, "description"),
                "keywords": getattr(data.channel, "keywords"),
                "title": getattr(data.channel, "title"),
                "youtube_subscribe": getattr(data.channel, "subscriber_count"),
                "create_video": getattr(data.channel, "video_count"),
            }

        elif media_type == "VideoObject":
            keep = {
                "link_id": data.link_id,
                "url": data.url,
                "domain": "youtube.com",
                "type": media_type,
                "identifier": getattr(data.video, "video_id"),
                "date_published": getattr(data.video, "published_at"),
                "duration": getattr(data.video, "duration"),
                "title": getattr(data.video, "title"),
                "abstract": getattr(data.video, "description"),
                "youtube_watch": getattr(data.video, "view_count"),
                "youtube_comment": getattr(data.video, "comment_count"),
                "youtube_like": getattr(data.video, "like_count"),
                "creator_type": "WebPage",
                "creator_date_created": getattr(data.channel, "published_at"),
                "creator_location_created": getattr(data.channel, "country"),
                "creator_identifier": getattr(data.video, "channel_id"),
                "creator_youtube_subscribe": getattr(data.channel, "subscriber_count"),
                "creator_create_video": getattr(data.channel, "video_count"),
                "creator_name": getattr(data.channel, "title"),
            }

        return keep
