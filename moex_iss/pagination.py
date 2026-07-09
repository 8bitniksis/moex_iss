from .exceptions import ISSPaginationError



class ISSPaginator:


    def __init__(
        self,
        client,
        chunk_size=100
    ):

        self.client = client

        self.chunk_size = chunk_size



    def iterate(
        self,
        url,
        block
    ):

        start = 0


        while True:

            separator = (
                "&"
                if "?" in url
                else "?"
            )


            request_url = (
                url
                + separator
                + f"start={start}"
            )


            response = (
                self.client.get_json(
                    request_url
                )
            )


            container = (
                response.get(block)
            )


            if not container:
                raise ISSPaginationError(
                    f"Missing block {block}"
                )


            rows = (
                container.get(
                    "data",
                    []
                )
            )


            columns = (
                container.get(
                    "columns",
                    []
                )
            )


            if not rows:
                break


            for row in rows:

                yield dict(
                    zip(
                        columns,
                        row
                    )
                )


            start += len(rows)