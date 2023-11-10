import casanova


def check_csv_headers(table_name: str, infile: str, url_col: str) -> list:
    with casanova.reader(infile) as reader:
        columns = reader.fieldnames

    if not isinstance(columns, list):
        raise NoCSVHeaders()

    if table_name == "links":
        if url_col not in columns:
            raise NoURLColumn(url_col)

    elif table_name == "shared_content":
        if "post_url" not in columns:
            raise NoPrimaryKeyColumns("post_url")
        if "content_url" not in columns:
            raise NoPrimaryKeyColumns("content_url")
    return columns


class NoCSVHeaders(Exception):
    def __init__(self) -> None:
        # Call the base class constructor with the parameters it needs
        message = "No headers detected in CSV file."
        super().__init__(message)


class NoURLColumn(Exception):
    def __init__(self, url_col: str) -> None:
        # Call the base class constructor with the parameters it needs
        message = f"The declared URL column '{url_col}' is not a header in the given CSV file."
        super().__init__(message)


class NoPrimaryKeyColumns(Exception):
    def __init__(self, col: str) -> None:
        # Call the base class constructor with the parameters it needs
        message = f"Required primary key column '{col}' is not a header in the given CSV file."
        super().__init__(message)


class MissingAPIKey(Exception):
    def __init__(self, api: str) -> None:
        message = f"Credentials not found for {api} API."
        super().__init__(message)
