import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE schedule (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  start_day TEXT NOT NULL,
                  groupname TEXT NOT NULL,
                  start_time TEXT NOT NULL,
                  end_time TEXT NOT NULL,
                  lessonname TEXT NOT NULL,
                  auditory TEXT NOT NULL,
                  teachername TEXT NOT NULL,
                  date TEXT NULL,
                  course TEXT NOT NULL,
                  comment_to_day TEXT,
                  pod_groups TEXT
             )''')

c.execute('''CREATE TABLE users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tblogin TEXT NOT NULL,
                  tbpassword TEXT NOT NULL
             )''')

conn.commit()
conn.close()
