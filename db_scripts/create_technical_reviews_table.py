import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("""
CREATE TABLE technical_reviews(
review_state integer,
serviceman_id integer,
parcel_machine_id integer
)
""")
conn.commit()
