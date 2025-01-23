#Лабораторна робота N26. Завдання 1. Коритко Артур
import sqlite3
from contextlib import contextmanager

@contextmanager
def database_connection(db_name):
    connection = sqlite3.connect(db_name)
    try:
        yield connection
    finally:
        connection.commit()
        connection.close()

def create_books_table():
    with database_connection("books.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year_published INTEGER NOT NULL
            )
        ''')

def insert_books(books):
    with database_connection("books.db") as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO books (title, author, year_published)
            VALUES (?, ?, ?)
        ''', books)

def fetch_all_books():
    with database_connection("books.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()

def update_book_year(book_id, new_year):
    with database_connection("books.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE books
            SET year_published = ?
            WHERE id = ?
        ''', (new_year, book_id))

def delete_book(book_id):
    with database_connection("books.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))

def main():
    create_books_table()

    books = [
        ("Убить пересмешника", "Харпер Ли", 1960),
        ("1984", "Джордж Оруэлл", 1949),
        ("Великий Гэтсби", "Фрэнсис Скотт Фицджеральд", 1925)
    ]

    print("Добавляем записи...")
    insert_books(books)

    print("Все книги:")
    for book in fetch_all_books():
        print(book)

    print("Обновляем год издания книги с ID 2...")
    update_book_year(2, 1950)

    print("Все книги после обновления:")
    for book in fetch_all_books():
        print(book)

    print("Удаляем книгу с ID 3...")
    delete_book(3)

    print("Все книги после удаления:")
    for book in fetch_all_books():
        print(book)

if __name__ == "__main__":
    main()

    
#Лабораторна робота N26. Завдання 2. Коритко Артур
    
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import messagebox

Base = declarative_base()
DATABASE_URL = "sqlite:///products.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

def create_table():
    Base.metadata.create_all(engine)

def add_product(name, price, quantity):
    session = Session()
    new_product = Product(name=name, price=price, quantity=quantity)
    session.add(new_product)
    session.commit()
    session.close()

def get_all_products():
    session = Session()
    products = session.query(Product).all()
    session.close()
    return products

def update_product_quantity(product_id, new_quantity):
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.quantity = new_quantity
        session.commit()
    session.close()

def delete_product(product_id):
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        session.delete(product)
        session.commit()
    session.close()

def show_products():
    products = get_all_products()
    product_list = "\n".join([f"ID: {p.id}, Имя: {p.name}, Цена: {p.price}, Количество: {p.quantity}" for p in products])
    messagebox.showinfo("Продукты", product_list or "Нет доступных продуктов")

def add_product_window():
    def add():
        name = name_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        add_product(name, price, quantity)
        messagebox.showinfo("Успех", "Продукт успешно добавлен")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Добавить продукт")

    tk.Label(add_window, text="Имя:").grid(row=0, column=0)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Цена:").grid(row=1, column=0)
    price_entry = tk.Entry(add_window)
    price_entry.grid(row=1, column=1)

    tk.Label(add_window, text="Количество:").grid(row=2, column=0)
    quantity_entry = tk.Entry(add_window)
    quantity_entry.grid(row=2, column=1)

    tk.Button(add_window, text="Добавить", command=add).grid(row=3, column=0, columnspan=2)

def main_window():
    global root
    root = tk.Tk()
    root.title("Менеджер продуктов")

    tk.Button(root, text="Показать продукты", command=show_products).pack(pady=10)
    tk.Button(root, text="Добавить продукт", command=add_product_window).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_table()
    main_window()
