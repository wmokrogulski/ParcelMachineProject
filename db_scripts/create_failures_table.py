import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
CREATE TABLE failures(
parcel_machine_id integer,
failure_code integer,
failure_datetime text,
repair_datetime text
)
""")
conn.commit()
