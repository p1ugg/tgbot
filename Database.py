import sqlite3


conn = sqlite3.connect('mydata.db')

cursor = conn.cursor()

# #Создание
# cursor.execute('''CREATE TABLE users
#                 (id INTEGER PRIMARY KEY, TG_ID INTEGER, name TEXT, referrals TEXT)''')
#
# #Добавление
# cursor.execute("INSERT INTO users (TG_ID, name, referrals) VALUES (?, ?, ?)", (1040305807, 'Yaroslav', '2313203213, 2313213555, 212122123112, 55425'))
# cursor.execute("INSERT INTO users (TG_ID, name, referrals) VALUES (?, ?, ?)", (2424243, 'yarik', ''))

##Обновление данных
# cursor.execute("UPDATE users SET age = ? WHERE name = ?", (1488, "Alice"))

# cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", ('1040305807',))
# row = cursor.fetchall()

def get_referrals_count(TG_ID):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()
    cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", (TG_ID,))
    row = cursor.fetchall()
    conn.commit()

    conn.close()
    try:
        return len(" ".join(row[0]).split(", "))
    except Exception as ex:
        return 0

