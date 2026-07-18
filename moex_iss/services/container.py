from __future__ import annotations

from typing import TYPE_CHECKING

from moex_iss.services.candles import CandleService
from moex_iss.services.history import HistoryService
from moex_iss.services.bonds import BondService


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

        self.bond = BondService(client)