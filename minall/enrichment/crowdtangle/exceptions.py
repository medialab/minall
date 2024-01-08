# minall/enrichment/crowdtangle/exceptions.py

"""Exceptions raised during data collection from CrowdTangle API.

This module contains exceptions raised during data collection from CrowdTangle API. The module contains the following exceptions:

- `NoPostID` - Neither minet nor minall's adhoc parser successfully recovered the Facebook post's ID.
- `PostNotfound` - CrowdTangle did not return a post matching the given post ID.
"""


class NoPostID(Exception):
    def __init__(self, error, url):
        message = "Unable to parse the post ID from url: {url}. Encountered error: {error}".format(
            url=url, error=error
        )
        super().__init__(message)


class PostNotFound(Exception):
    def __init__(self, url, error) -> None:
        message = "CrowdTangle does not have data about the post at this url: {url}. The CrowdTangle API's response is: \n{data}\n".format(
            url=url, data=error.data
        )
        super().__init__(message)
