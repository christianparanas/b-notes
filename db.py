import sqlite3 as sql

#connect to SQLite
con = sql.connect('notes.db')

#Create a Connection
cur = con.cursor()

#Drop users table if already exsist.
cur.execute("DROP TABLE IF EXISTS notes")

#Create users table  in db_web database
sql ='''CREATE TABLE "notes" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"title"	TEXT,
	"content"	TEXT,
	"subject" TEXT
)'''
cur.execute(sql)

#commit changes
con.commit()

#close the connection
con.close()