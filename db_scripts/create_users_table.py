import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
CREATE TABLE users(
username text,
password text,
first_name text,
last_name text
)
""")
conn.commit()
