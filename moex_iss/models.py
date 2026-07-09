from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ISSBlock:
    name: str

    columns: list[str]

    data: list[list[Any]]

    metadata: dict

    def rows(self):

        for row in self.data:
            yield dict(
                zip(
                    self.columns,
                    row,
                    strict=True,
                )
            )
