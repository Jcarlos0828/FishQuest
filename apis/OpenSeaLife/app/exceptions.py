class OSLError(Exception):
    """Base for OpenSeaLife domain errors mapped to HTTP responses."""


class InvalidVersionError(OSLError):
    def __init__(self, version: str, server: str, available: list[str]) -> None:
        self.version = version
        self.server = server
        self.available = available
        super().__init__(f"Version '{version}' is not available for server '{server}'.")


class TableNotFoundError(OSLError):
    def __init__(self, table: str, server: str, version: str) -> None:
        self.table = table
        self.server = server
        self.version = version
        super().__init__(f"Table '{table}' is not available for {server} {version}.")


class DataSourceError(OSLError):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)
