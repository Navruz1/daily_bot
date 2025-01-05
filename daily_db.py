import sqlite3


def tools():
    conn = sqlite3.connect('daily.db')
    cursor = conn.cursor()
    return conn, cursor


def create_table(table_name):
    conn, cursor = tools()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            tg_id BIGINT UNIQUE, 
            name VARCHAR(255), 
            age INTEGER, 
            phone VARCHAR(32))''')
    conn.commit()


def save_info(tg_id, name, age, phone):
    conn, cursor = tools()
    t_name = "tasks"
    create_table(t_name)
    cursor.execute(f'''
        INSERT INTO {t_name} (tg_id, name, age, phone) 
        VALUES (?,?,?,?)
        ON CONFLICT (tg_id) DO UPDATE SET 
            name = excluded.name, 
            age = excluded.age,
            phone = excluded.phone
    ''', (tg_id, name, age, phone))
    conn.commit()


answers = {
    "wellcome": {
        "Русский": "Добро пожаловать!",
        "English": "Wellcome!",
    },
    "language": {
        "Русский": "Пожалуйста, выберите язык",
        "English": "Please choose a language",
    },
    "menu": {
        "Русский": "Главное меню",
        "English": "Main menu"
    }
}

#         "Русский": "",
#         "English": ""