import sqlite3

DISTRICT_LIST=['Mokotów', 'Praga-Południe', 'Ursynów', 'Wola', 'Białołęka', 'Bielany', 'Bemowo', 'Targówek', 'Śródmieście', 'Ochota', 'Wawer', 'Praga-Północ', 'Ursus', 'Żoliborz', 'Włochy', 'Wilanów', 'Wesoła', 'Rembertów']

DATABASE='../database.db'
conn=sqlite3.connect(DATABASE)
c=conn.cursor()
# c.execute("""
# CREATE TABLE districts(
# name text
# )
# """)
# conn.commit()
for district in DISTRICT_LIST:
    c.execute('INSERT INTO districts values (?)', (district,))
    conn.commit()
conn.close()
