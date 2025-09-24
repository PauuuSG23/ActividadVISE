from enum import Enum
from typing import Literal

class CardType(str, Enum):
    Classic="Classic"
    Gold="Gold"
    Platinum="Platinum"
    Black="Black"
    White="White"

Currency=Literal["USD"]