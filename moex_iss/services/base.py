from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import ISSClient


class BaseService:
    """Base class for all ISS services."""

    def __init__(
        self,
        client: ISSClient,
    ) -> None:
        self._client = client