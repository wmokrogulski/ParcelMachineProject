import sqlite3
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    username: str
    first_name: str
    last_name: str


def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('select rowid, username, first_name, last_name from users where rowid=(?)', [user_id])
    row = c.fetchone()
    user = User(row[0], row[1], row[2], row[3])
    conn.close()
    return user
