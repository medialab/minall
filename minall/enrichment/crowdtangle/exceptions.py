class NoPostID(Exception):
    def __init__(self, error, url):
        # Call the base class constructor with the parameters it needs
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
