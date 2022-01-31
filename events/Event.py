from datetime import datetime
import sqlite3
from dataclasses import dataclass
from enum import Enum

from parcel_machine import ParcelMachine

DATE_FORMAT='%d.%m.%Y %H:%M:%S'


@dataclass
class Event:
    class EventType(Enum):
        PackageSent = 1
        PackageReceived = 2
        TechnicalReviewOrder = 3
        TechnicalReviewAccepted = 4
        TechnicalReviewDone = 5
        RepairOrder = 6
        RepairAccepted = 7
        RepairDone = 8

    parcel_machine: ParcelMachine
    event_type: EventType
    event_datetime: datetime
    event_id: int = None


def get_event_by_id(event_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('select rowid, parcel_machine_id, event_type, datetime from events where rowid=(?)', [event_id])
    row = c.fetchone()
    event = Event(ParcelMachine(row[1]), Event.EventType(row[2]), datetime.strptime(row[3], DATE_FORMAT),
                  row[0])
    conn.close()
    return event
