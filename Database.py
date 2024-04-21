import sqlite3


conn = sqlite3.connect('mydata.db')

cursor = conn.cursor()

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

def has_referrer(TG_ID):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE TG_ID = ?", (TG_ID,))
    row = cursor.fetchall()

    conn.commit()

    conn.close()
    print(row)
    if row:
        return False
    return True


def get_all_users():
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("SELECT TG_ID FROM users")
    tg_ids = [row[0] for row in cursor.fetchall()]

    conn.commit()

    conn.close()
    return tg_ids

def add_inv_ref(TGID_invaited,TGID_refowner):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("UPDATE users SET inv_referral = ? WHERE TG_ID = ?", (TGID_refowner,TGID_invaited))

    cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", (TGID_refowner,))
    row = cursor.fetchall()

    try:
        new_refs = " ".join(row[0]).split(", ")
        new_refs.append(TGID_invaited)
        new_refs = ", ".join(new_refs)
    except Exception:
        new_refs = f'{TGID_invaited}, '

    cursor.execute("UPDATE users SET referrals = ? WHERE TG_ID = ?", (new_refs, TGID_refowner))

    conn.commit()

    conn.close()


def add_user(TG_ID, name, inv_referral):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (TG_ID, name, referrals, inv_referral) VALUES (?, ?, ?, ?)", (TG_ID, name, '', inv_referral))

    conn.commit()

    conn.close()


def check_user_in_db(TG_ID):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE TG_ID = ?", (TG_ID,))
    row = cursor.fetchall()

    conn.commit()

    conn.close()
    if row:
        return True
    return False

# add_inv_ref('2424243','1040305807')

# print(has_referrer(2543535435))

# #Создание
# cursor.execute('''CREATE TABLE users
#                 (id INTEGER PRIMARY KEY, TG_ID TEXT, name TEXT, referrals TEXT, inv_referral TEXT)''')

# #Добавление
# cursor.execute("INSERT INTO users (TG_ID, name, referrals,inv_referral) VALUES (?, ?, ?, ?)", (1223, 'Yaroslav', '2313203213, 2313213555, 212122123112, 55425', ""))
# cursor.execute("INSERT INTO users (TG_ID, name, referrals, inv_referral) VALUES (?, ?, ?, ?)", (2424243, 'yarik', '', ""))

##Обновление данных
# cursor.execute("UPDATE users SET age = ? WHERE name = ?", (1488, "Alice"))

# cursor.execute("UPDATE users SET inv_referral = ? WHERE name = ?", ('', "yarik"))

# cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", ('1040305807',))
# row = cursor.fetchall()
# try:
#     new_refs = " ".join(row[0]).split(", ")
#     new_refs.append('2424243')
#     new_refs = ", ".join(new_refs)
#     print(new_refs)
# except Exception as ex:
#     new_refs = '2424243, '

# cursor.execute("SELECT TG_ID FROM users")
# tg_ids = [row[0] for row in cursor.fetchall()]
#
# print(tg_ids)

# cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", ('1040305807',))
# row = cursor.fetchall()
conn.commit()

conn.close()