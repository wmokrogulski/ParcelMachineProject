import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
CREATE TABLE repairs(
repair_state integer,
serviceman_id integer,
failure_id integer
)
""")
conn.commit()
