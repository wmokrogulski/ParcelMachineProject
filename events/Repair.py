import sqlite3
from dataclasses import dataclass
from enum import Enum

from parcel_machine import ParcelMachine
from users import User, get_user_by_id


@dataclass
class Repair:
    class RepairState(Enum):
        Ordered = 1
        Accepted = 2
        Done = 3

    repair_state: RepairState
    parcel_machine: ParcelMachine
    repair_id: int = None
    serviceman: User = None


def get_repair_by_id(repair_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('select rowid, repair_state, parcel_machine_id, serviceman_id from repairs where rowid=(?)', [repair_id])
    row = c.fetchone()
    if row[3] is not None:
        repair = Repair(row[1], ParcelMachine(row[2]), row[1],
                        get_user_by_id(row[3]))
    else:
        repair = Repair(row[1], ParcelMachine(row[2]), row[1],
                        None)
    conn.close()
    return repair
