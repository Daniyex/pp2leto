import psycopg2
import csv

def import_contacts_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            phone = row['phone']
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Контакты успешно добавлены из CSV.")


def connect():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Dakota3012"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone_number VARCHAR(15) NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def upsert_user():
    name = input("Введите имя: ")
    phone = input("Введите номер: ")
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM phonebook WHERE first_name = %s", (name,))
    result = cur.fetchone()

    if result:
        cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (phone, name))
        print("Контакт обновлён!")
    else:
        cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
        print("Контакт добавлен!")

    conn.commit()
    cur.close()
    conn.close()




def bulk_insert_from_csv():
    filename = input("Введите имя CSV файла: ")
    names = []
    phones = []

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 2:
                names.append(row[0])
                phones.append(row[1])

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_users(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакты из CSV обработаны.")

def update_user():
    old_name = input("Введите текущее имя: ")
    new_name = input("Новое имя (оставьте пустым если не менять): ")
    new_phone = input("Новый номер телефона (оставьте пустым если не менять): ")

    conn = connect()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (new_phone, old_name))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт обновлён!")

def search_by_pattern():
    pattern = input("Введите шаблон (имя или номер): ")
    conn = connect()
    cur = conn.cursor()
    query = """
        SELECT * FROM phonebook
        WHERE first_name ILIKE %s OR phone_number ILIKE %s
    """
    cur.execute(query, (f'%{pattern}%', f'%{pattern}%'))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Ничего не найдено.")
    cur.close()
    conn.close()


def paginated_view():
    limit = int(input("Сколько записей выводить: "))
    offset = int(input("С какого смещения начинать: "))
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_user():
    key = input("Введите имя или номер для удаления: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM phonebook
        WHERE first_name = %s OR phone_number = %s
    """, (key, key))
    if cur.rowcount > 0:
        print("Контакт удалён!")
    else:
        print("Контакт не найден.")
    conn.commit()
    cur.close()
    conn.close()



def main():
    create_table()
    while True:
        print("\n--- Телефонная книга ---")
        print("1. Добавить или обновить контакт")
        print("2. Загрузить контакты из CSV")
        print("3. Обновить вручную (прямой UPDATE)")
        print("4. Поиск по шаблону")
        print("5. Постраничный просмотр")
        print("6. Удалить контакт по имени или номеру")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == "1":
            upsert_user()
        elif choice == "2":
            filename = input("Введите путь к CSV-файлу: ")
            import_contacts_from_csv(filename)
            

        elif choice == "3":
            update_user()
        elif choice == "4":
            search_by_pattern()
        elif choice == "5":
            paginated_view()
        elif choice == "6":
            delete_user()
        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверная опция!")

if __name__ == "__main__":
    main()
