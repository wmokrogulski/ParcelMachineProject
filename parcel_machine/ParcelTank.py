from dataclasses import dataclass, field
from enum import Enum


@dataclass
class ParcelTank:
    class ParcelTankSize(Enum):
        SMALL = 1
        MEDIUM = 2
        LARGE = 3

    tank_id: int
    size_type: int = field(repr=False)
    package_code: str
    size: ParcelTankSize = field(init=False)

    def __post_init__(self):
        self.size = ParcelTank.ParcelTankSize(self.size_type)
