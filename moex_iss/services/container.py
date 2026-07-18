from __future__ import annotations

from typing import TYPE_CHECKING

from .candles import CandleService
from .history import HistoryService

if TYPE_CHECKING:
    from ..client import ISSClient


class ServiceContainer:
    """Container for ISS services."""

    def __init__(
        self,
        client: ISSClient,
    ) -> None:

        self.history = HistoryService(client)

        self.candles = CandleService(client)