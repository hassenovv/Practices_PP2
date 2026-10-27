"""PhoneBook console application backed by PostgreSQL.

Features:
 1. Create table
 2. Insert contacts from a CSV file
 3. Insert a contact from the console
 4. Update a contact's first name or phone
 5. Query contacts with filters (all / name / phone prefix)
 6. Delete a contact by username (first name) or phone
"""
import csv
import os

import psycopg2
from connect import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS phonebook (
    id          SERIAL PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50),
    phone       VARCHAR(20)  NOT NULL UNIQUE
);
"""


# ---------- 1. Table design ----------
def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
    print("Table 'phonebook' is ready.")


# ---------- 2. Insert from CSV ----------
def insert_from_csv(path=os.path.join(BASE_DIR, "contacts.csv")):
    inserted, skipped = 0, 0
    with get_connection() as conn:
        with conn.cursor() as cur, open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    """INSERT INTO phonebook (first_name, last_name, phone)
                       VALUES (%s, %s, %s)
                       ON CONFLICT (phone) DO NOTHING""",
                    (row["first_name"].strip(), row["last_name"].strip(), row["phone"].strip()),
                )
                if cur.rowcount:
                    inserted += 1
                else:
                    skipped += 1
    print(f"CSV import done: {inserted} inserted, {skipped} skipped (duplicate phone).")


# ---------- 3. Insert from console ----------
def insert_from_console():
    first_name = input("First name (username): ").strip()
    last_name = input("Last name (optional): ").strip() or None
    phone = input("Phone: ").strip()

    if not first_name or not phone:
        print("First name and phone are required.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)",
                    (first_name, last_name, phone),
                )
        print("Contact added.")
    except psycopg2.errors.UniqueViolation:
        print("A contact with this phone already exists.")


# ---------- 4. Update ----------
def update_contact():
    phone = input("Enter the current phone of the contact to update: ").strip()
    print("What do you want to change?\n  1) First name\n  2) Phone")
    choice = input("> ").strip()

    if choice == "1":
        new_value = input("New first name: ").strip()
        sql = "UPDATE phonebook SET first_name = %s WHERE phone = %s"
    elif choice == "2":
        new_value = input("New phone: ").strip()
        sql = "UPDATE phonebook SET phone = %s WHERE phone = %s"
    else:
        print("Invalid choice.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_value, phone))
                if cur.rowcount:
                    print("Contact updated.")
                else:
                    print("No contact found with that phone.")
    except psycopg2.errors.UniqueViolation:
        print("That phone number is already used by another contact.")


# ---------- 5. Query with filters ----------
def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return
    print(f"{'ID':<4} {'First name':<15} {'Last name':<15} {'Phone':<15}")
    print("-" * 52)
    for r in rows:
        print(f"{r[0]:<4} {r[1]:<15} {(r[2] or ''):<15} {r[3]:<15}")


def query_contacts():
    print("Filter by:\n  1) Show all\n  2) Name (first or last, partial match)\n  3) Phone prefix")
    choice = input("> ").strip()

    base = "SELECT id, first_name, last_name, phone FROM phonebook"
    if choice == "1":
        sql, params = base + " ORDER BY first_name", ()
    elif choice == "2":
        name = input("Name contains: ").strip()
        sql = base + " WHERE first_name ILIKE %s OR last_name ILIKE %s ORDER BY first_name"
        params = (f"%{name}%", f"%{name}%")
    elif choice == "3":
        prefix = input("Phone starts with: ").strip()
        sql = base + " WHERE phone LIKE %s ORDER BY phone"
        params = (f"{prefix}%",)
    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            print_rows(cur.fetchall())


# ---------- 6. Delete ----------
def delete_contact():
    print("Delete by:\n  1) Username (first name)\n  2) Phone")
    choice = input("> ").strip()

    if choice == "1":
        value = input("First name: ").strip()
        sql = "DELETE FROM phonebook WHERE first_name = %s"
    elif choice == "2":
        value = input("Phone: ").strip()
        sql = "DELETE FROM phonebook WHERE phone = %s"
    else:
        print("Invalid choice.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (value,))
            print(f"Deleted {cur.rowcount} contact(s).")


# ---------- Menu ----------
MENU = """
===== PhoneBook =====
1. Insert contacts from CSV
2. Add contact from console
3. Update contact
4. Search contacts
5. Delete contact
0. Exit
"""


def main():
    create_table()
    actions = {
        "1": insert_from_csv,
        "2": insert_from_console,
        "3": update_contact,
        "4": query_contacts,
        "5": delete_contact,
    }
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Bye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except (psycopg2.DatabaseError, Exception) as error:
                print("Error:", error)
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
