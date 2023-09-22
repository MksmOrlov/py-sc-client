from dataclasses import dataclass
from typing import Callable, Optional

from sc_client.constants.common import ScEventType
from sc_client.models.sc_addr import ScAddr

ScEventCallback = Callable[[ScAddr, ScAddr, ScAddr], None]


@dataclass
class ScEventParams:
    addr: ScAddr
    event_type: ScEventType
    callback: ScEventCallback


@dataclass
class ScEvent:
    id: int
    event_type: Optional[ScEventType] = None
    callback: Optional[ScEventCallback] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, event_type={self.event_type})"
