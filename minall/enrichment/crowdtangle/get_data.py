from pathlib import Path

from minall.enrichment.crowdtangle.client import FacebookPostCommand, parse_rate_limit
from minall.enrichment.crowdtangle.contexts import ContextManager
from minall.enrichment.crowdtangle.normalizer import (
    parse_facebook_post,
    parse_shared_content,
)


def get_facebook_post_data(
    data: list[str],
    token: str,
    rate_limit: int | str | None,
    links_outfile: Path,
    shared_content_outfile: Path,
):
    rate_limit = parse_rate_limit(rate_limit)

    client = FacebookPostCommand(token=token, rate_limit=rate_limit)

    with ContextManager(links_outfile, shared_content_outfile) as contexts:
        links_writer, shared_content_writer, executor, progress = contexts

        t = progress.add_task(
            description="[bold blue]Querying Facebook posts", total=len(data)
        )

        for url, result in executor.map(client, data):
            for shared_content in parse_shared_content(url, result):
                if shared_content:
                    shared_content_writer.writerow(shared_content)
            facebook_post = parse_facebook_post(url, result)
            if facebook_post:
                links_writer.writerow(facebook_post)
            progress.advance(t)
