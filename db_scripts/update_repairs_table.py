import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
alter table repairs rename column failure_id to parcel_machine_id
""")
conn.commit()
