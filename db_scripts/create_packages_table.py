import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
CREATE TABLE package(
code text,
collection_code text,
phone text
)
""")
conn.commit()
