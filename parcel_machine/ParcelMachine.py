import hashlib
import random
import sqlite3
from datetime import datetime

from events import Event
from parcel_machine import ParcelTank


class ParcelMachine:
    def __init__(self, pm_id):
        self.id = pm_id
        self.total_tanks = 0
        self.used_tanks = 0
        self.parcel_tanks: list[ParcelTank] = []
        self.free_parcel_tanks: list[ParcelTank] = []
        self.load_parcel_tanks()

    def load_parcel_tanks(self):
        self.parcel_tanks.clear()
        self.used_tanks=0
        self.total_tanks=0
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        for row in c.execute("select rowid, size, package_code from parcel_tanks where parcel_machine_id=(?)",
                             [self.id]):
            pt = ParcelTank(row[0], row[1], row[2])
            self.parcel_tanks.append(pt)
            if row[2] != '':
                self.used_tanks += 1
            else:
                self.free_parcel_tanks.append(pt)
            self.total_tanks += 1
        conn.close()

    def propose_free_tank(self, size: ParcelTank.ParcelTankSize=ParcelTank.ParcelTankSize.SMALL):
        proposal = None
        for tank in self.free_parcel_tanks:
            if tank.size == size:
                proposal = tank
                break
        return proposal

    def send_package(self, phone, tank: ParcelTank):
        if tank is None:
            message='Nie ma wolnej skrytki.'
            print(message)
            return message
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        while True:
            collection_code = f'{random.randint(0, 999999):06d}'
            c.execute('select * from package where phone=(?) and collection_code=(?)', [phone, collection_code])
            if c.fetchone() is None:
                break
        c.execute('select count(*) from package')
        package_id = c.fetchone()[0] + 1
        code = hashlib.md5(str(package_id).encode('utf-8')).hexdigest().upper()
        c.execute('insert into package(code, collection_code, phone) values (?,?,?)', [code, collection_code, phone])
        self.free_parcel_tanks.remove(tank)
        tank_id = tank.tank_id
        c.execute('update parcel_tanks set package_code=(?) where rowid=(?)', [code, tank_id])
        tank.package_code = code
        self.used_tanks += 1
        c.execute('update parcel_machines set tanks_used=(?) where rowid=(?)', [self.used_tanks, self.id])
        c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                  [self.id, Event.EventType.PackageSent.value,
                   datetime.now()])
        conn.commit()
        conn.close()
        message=f'Nadano przesyłkę. Numer telefonu {phone}, kod odbioru {collection_code}.'
        print(message)
        return message

    def receive_package(self, phone, collection_code):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('select code from package where phone=(?) and collection_code=(?)', [phone, collection_code])
        code = c.fetchone()
        package_tank = None
        if code is None:
            message='Podana paczka nie istnieje'
            print(message)
        else:
            code = code[0]
            for tank in self.parcel_tanks:
                if tank.package_code == code:
                    package_tank = tank
                    break
            else:
                message='Podana paczka znajduje się w innym paczkomacie.'
                print(message)
            if package_tank is not None:
                c.execute('delete from package where code=(?)', [code])
                c.execute('update parcel_tanks set package_code=(?) where rowid=(?)', ['', package_tank.tank_id])
                self.used_tanks -= 1
                self.free_parcel_tanks.append(package_tank)
                c.execute('update parcel_machines set tanks_used=(?) where rowid=(?)', [self.used_tanks, self.id])
                c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                          [self.id, Event.EventType.PackageReceived.value,
                           datetime.now()])
                message=f'Odebrano paczkę {code}'
                print(message)
                conn.commit()
        conn.close()
        return message
