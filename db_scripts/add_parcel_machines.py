import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
# c.execute("""
# CREATE TABLE parcel_machines(
# tanks_number integer,
# tanks_used integer
# )
# """)
# conn.commit()

c.execute('insert into parcel_machines(tanks_number, tanks_used) values (?,?)', [16,0])
conn.commit()
