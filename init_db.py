import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
            ('First_user', 'First_Pwd')
            )

cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
            ('Second_user', 'Snd_Pwd')
            )

connection.commit()
connection.close()
