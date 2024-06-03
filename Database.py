import sqlite3

conn = sqlite3.connect('mydata.db')

cursor = conn.cursor()


def get_referrals_count(TG_ID):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()
    cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", (TG_ID,))
    row = cursor.fetchall()[0][0]

    conn.commit()

    conn.close()
    if row:
        return len(row.split(","))
    else:
        return 0


def has_referrer(TG_ID):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE TG_ID = ?", (TG_ID,))
    row = cursor.fetchall()

    conn.commit()

    conn.close()
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


def add_inv_ref(TGID_invaited, TGID_refowner):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("UPDATE users SET inv_referral = ? WHERE TG_ID = ?", (TGID_refowner, TGID_invaited))

    cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", (TGID_refowner,))
    row = cursor.fetchall()
    print(row)
    try:
        if row[0][0]:
            new_refs = f'{row[0][0]},{TGID_invaited}'
        else:
            new_refs = f'{TGID_invaited}'
    except Exception as ex:
        print(ex)
        pass



    cursor.execute("UPDATE users SET referrals = ? WHERE TG_ID = ?", (new_refs, TGID_refowner))

    conn.commit()

    conn.close()

# add_inv_ref('849778335','1040305807' )


def add_user(TG_ID, name, inv_referral):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (TG_ID, name, referrals, inv_referral, balance) VALUES (?, ?, ?, ?, ?)",
                   (TG_ID, name, '', inv_referral, 0))

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


def get_name(TG_ID):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()

    cursor.execute("SELECT inv_referral FROM users WHERE TG_ID = ?", (TG_ID,))
    TG_ID_invaited = "".join(cursor.fetchall()[0])
    cursor.execute("SELECT name FROM users WHERE TG_ID = ?", (TG_ID_invaited,))
    row = cursor.fetchall()

    conn.commit()

    conn.close()
    if row:
        return "".join(row[0])
    return "None"


def get_referrals_names(TG_ID):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()
    cursor.execute("SELECT referrals FROM users WHERE TG_ID = ?", (TG_ID,))
    row = cursor.fetchall()[0][0].split(',')
    s = []
    for num, id in enumerate(row):
        cursor.execute("SELECT name FROM users WHERE TG_ID = ?", (str(id),))
        s.append(f'{num + 1}. {cursor.fetchall()[0][0]}')

    conn.commit()

    conn.close()
    return "\n".join(s)


def update_balance(TG_ID, amount):
    conn = sqlite3.connect('mydata.db')

    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE TG_ID = ?", (TG_ID,))
    now_balance = cursor.fetchall()[0][0] + amount
    cursor.execute("UPDATE users SET balance = ? WHERE TG_ID = ?", (now_balance, TG_ID))

    conn.commit()

    conn.close()


# update_balance('1040305807', 200)

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
