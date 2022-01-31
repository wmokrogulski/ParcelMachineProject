import datetime
from dataclasses import dataclass
from enum import Enum

from parcel_machine import ParcelMachine


@dataclass
class Failure:
    class FailureType(Enum):
        TouchScreenFailure = 1
        DoorsFailure = 2
        CommunicationSystemFailure = 3

    failure_type: FailureType
    parcel_machine: ParcelMachine
    failure_datetime: datetime.datetime
    repair_datetime: datetime.datetime = None
    failure_id: int = None
