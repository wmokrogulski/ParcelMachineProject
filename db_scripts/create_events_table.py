import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
CREATE TABLE events(
parcel_machine_id integer,
event_type integer,
datetime text
)
""")
conn.commit()
