from __future__ import annotations

from typing import TYPE_CHECKING

from moex_iss.services.bonds import BondService
from moex_iss.services.candles import CandleService
from moex_iss.services.history import HistoryService

if TYPE_CHECKING:
    from moex_iss.clients import ISSClient


class ServiceContainer:
    """Container for ISS services."""

    def __init__(
        self,
        client: ISSClient,
    ) -> None:

        self.history = HistoryService(client)

        self.candles = CandleService(client)

        self.bond = BondService(client)
