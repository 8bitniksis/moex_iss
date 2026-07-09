from collections.abc import Iterator
from typing import Any

from .exceptions import ISSPaginationError


class ISSPaginator:
    def __init__(
        self,
        client: Any,
        chunk_size: int = 100,
    ) -> None:

        self.client = client
        self.chunk_size = chunk_size

    def iterate(
        self,
        url: str,
        block: str,
    ) -> Iterator[dict[str, Any]]:

        start = 0

        while True:
            separator = "&" if "?" in url else "?"

            request_url = url + separator + f"start={start}"

            response: dict[str, Any] = self.client.get_json(request_url)

            container = response.get(block)

            if not container:
                raise ISSPaginationError(f"Missing block {block}")

            rows = container.get("data", [])

            columns = container.get("columns", [])

            if not rows:
                break

            for row in rows:
                yield dict(
                    zip(
                        columns,
                        row,
                        strict=True,
                    )
                )

            start += len(rows)
