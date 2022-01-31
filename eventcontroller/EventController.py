from datetime import datetime, timedelta
import sqlite3

from events import Failure, Repair, Event, TechnicalReview, DATE_FORMAT
from parcel_machine import ParcelMachine
from users import User



class EventController:
    @staticmethod
    def add_failure(failure: Failure):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('insert into failures(failure_code, parcel_machine_id, failure_datetime) values (?,?,?)',
                  [failure.failure_type.value, failure.parcel_machine.id,
                   failure.failure_datetime.strftime(DATE_FORMAT)])
        c.execute('update parcel_machines set failure_state=1, error_code=(?) where rowid=(?)',
                  [failure.failure_type.value, failure.parcel_machine.id])
        conn.commit()
        conn.close()

    @staticmethod
    def order_repair(parcel_machine: ParcelMachine):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('insert into repairs(repair_state, parcel_machine_id) values (?,?)',
                  [Repair.RepairState.Ordered.value, parcel_machine.id])
        c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                  [parcel_machine.id, Event.EventType.RepairOrder.value, datetime.now().strftime(DATE_FORMAT)])
        conn.commit()
        conn.close()

    @staticmethod
    def accept_repair(repair: Repair, serviceman: User):
        if repair.repair_state == Repair.RepairState.Done:
            print('Naprawa została już wykonana')
            return
        if repair.repair_state == Repair.RepairState.Accepted:
            print('Naprawa została już zaakceptowana')
            return
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('update repairs set repair_state=(?), serviceman_id=(?) where rowid=(?)',
                  [Repair.RepairState.Accepted.value, serviceman.user_id, repair.repair_id])
        c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                  [repair.parcel_machine.id, Event.EventType.RepairAccepted.value, datetime.now().strftime(DATE_FORMAT)])
        conn.commit()
        conn.close()

    @staticmethod
    def do_repair(repair: Repair, serviceman: User):
        if repair.repair_state == Repair.RepairState.Done:
            print('Naprawa została już wykonana')
            return
        if repair.repair_state != Repair.RepairState.Accepted:
            print('Naprawa nie została zaakceptowana')
            return
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('update repairs set repair_state=(?), serviceman_id=(?) where rowid=(?)',
                  [Repair.RepairState.Done.value, serviceman.user_id, repair.repair_id])
        c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                  [repair.parcel_machine.id, Event.EventType.RepairDone.value, datetime.now()])
        c.execute('update failures set repair_datetime=(?) where parcel_machine_id=(?)',
                  [datetime.now(), repair.parcel_machine.id])
        c.execute('update parcel_machines set failure_state=0, error_code=null where rowid=(?)',
                  [repair.parcel_machine.id])
        conn.commit()
        conn.close()

    @staticmethod
    def order_review(parcel_machine: ParcelMachine):

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('insert into technical_reviews(review_state, parcel_machine_id) values (?,?)',
                  [TechnicalReview.ReviewState.Ordered.value, parcel_machine.id])
        c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                  [parcel_machine.id, Event.EventType.TechnicalReviewOrder.value, datetime.now().strftime(DATE_FORMAT)])
        conn.commit()
        conn.close()

    @staticmethod
    def accept_review(review:TechnicalReview, serviceman: User):
        if review.review_state == TechnicalReview.ReviewState.Done:
            print('Przegląd został już wykonany')
            return
        if review.review_state == TechnicalReview.ReviewState.Accepted:
            print('Przegląd został już zaakceptowany')
            return
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('update technical_reviews set review_state=(?), serviceman_id=(?) where rowid=(?)',
                  [Repair.RepairState.Accepted, serviceman.user_id, review.review_id])
        c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                  [review.parcel_machine.id, Event.EventType.TechnicalReviewAccepted.value, datetime.now().strftime(DATE_FORMAT)])
        conn.commit()
        conn.close()

    @staticmethod
    def do_review(review: TechnicalReview, serviceman: User):
        if review.review_state == TechnicalReview.ReviewState.Done:
            print('Przegląd został już wykonany')
            return
        if review.review_state != TechnicalReview.ReviewState.Accepted:
            print('Przegląd nie zaakceptowany')
            return
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('update technical_reviews set review_state=(?), serviceman_id=(?) where rowid=(?)',
                  [TechnicalReview.ReviewState.Done, serviceman.user_id, review.review_id])
        c.execute('insert into events(parcel_machine_id, event_type, datetime) values (?,?,?)',
                  [review.parcel_machine.id, Event.EventType.TechnicalReviewDone.value, datetime.now()])
        c.execute('update parcel_machines set next_inspection_date=(?) where rowid=(?)',
                  [(datetime.now() + timedelta(days=30)).strftime(DATE_FORMAT), review.parcel_machine.id])
        conn.commit()
        conn.close()
