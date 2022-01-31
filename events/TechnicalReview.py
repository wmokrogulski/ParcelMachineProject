import sqlite3
from dataclasses import dataclass

from parcel_machine import ParcelMachine
from users import User, get_user_by_id


@dataclass
class TechnicalReview:
    class ReviewState:
        Ordered = 1
        Accepted = 2
        Done = 3

    review_state: ReviewState
    serviceman: User
    parcel_machine: ParcelMachine
    review_id: int = None


def get_review_by_id(review_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('select rowid, review_state, serviceman_id, parcel_machine_id from technical_reviews where rowid=(?)',
              [review_id])
    row = c.fetchone()
    if row[2] is not None:
        review = TechnicalReview(row[1], get_user_by_id(row[2]), ParcelMachine(row[3]), row[0])
    else:
        review = TechnicalReview(row[1], None, ParcelMachine(row[3]), row[0])
    conn.close()
    return review
