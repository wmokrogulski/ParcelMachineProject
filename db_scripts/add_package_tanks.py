import sqlite3

DATABASE = '../database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
# c.execute("""
# CREATE TABLE parcel_tanks(
# parcel_machine_id integer,
# size integer,
# package_code text default ''
# )
# """)
# conn.commit()
# size = 1
# for i in range(16):
#     if i > 8:
#         size = 3
#     elif i > 4:
#         size = 2
#     c.execute('insert into parcel_tanks(parcel_machine_id,size,package_code) values (?,?,?)', [1, size, ''])
# conn.commit()
