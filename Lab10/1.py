import psycopg2
import csv

import csv

def import_contacts_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    #with open(filename, newline='', encoding='utf-8') as csvfile:
      #  reader = csv.DictReader(csvfile)
       # for row in reader:
        #    name = row['name']
         #   phone = row['phone']
          #  cur.execute(
           #     "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            #    (name, phone)
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
        
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

def insert_user_console():
    first_name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")

    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (first_name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен!")


    

    
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

def query_users():
    print("Фильтр: 1 - все, 2 - по имени, 3 - по номеру")
    choice = input("Ваш выбор: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        name = input("Введите имя: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "3":
        phone = input("Введите номер: ")
        cur.execute("SELECT * FROM phonebook WHERE phone_number = %s", (phone,))
    else:
        print("Неверный выбор.")
        return

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_user():
    print("Удалить по: 1 - имени, 2 - номеру")
    choice = input("Ваш выбор: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Введите имя: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        phone = input("Введите номер: ")
        cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone,))
    else:
        print("Неверный выбор.")
        return

    conn.commit()
    cur.close()
    conn.close()
    print("Контакт удалён!")

def main():
    create_table()
    while True:
        print("\n--- Телефонная книга ---")
        print("1. Добавить контакт")
        print("2. Загрузить контакты из CSV")
        print("3. Обновить контакт")
        print("4. Найти контакт")
        print("5. Удалить контакт")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == "1":
            insert_user_console()
        elif choice == "2":
            filename = input("Введите путь к CSV-файлу: ")
            import_contacts_from_csv(filename)
        elif choice == "3":
            update_user()
        elif choice == "4":
            query_users()
        elif choice == "5":
            delete_user()
        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверная опция!")

if __name__ == "__main__":
    main()
