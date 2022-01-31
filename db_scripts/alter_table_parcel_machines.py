import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
alter table parcel_machines column failure_state;
""")
conn.commit()
