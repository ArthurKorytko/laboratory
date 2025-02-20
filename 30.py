import sqlite3


def create_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_book(title, author, year, genre):
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)",
                       (title, author, year, genre))
        conn.commit()
        print(f"✅ Книга '{title}' добавлена в библиотеку!")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при добавлении книги: {e}")
    finally:
        conn.close()


def show_all_books():
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        conn.close()

        if books:
            print("\n📚 Все книги в библиотеке:")
            for book in books:
                print(
                    f"{book[0]}. {book[1]} - {book[2]} ({book[3]}) [{book[4]}]")
        else:
            print("⚠️ Библиотека пуста!")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при получении книг: {e}")


def show_books_by_genre():
    genre = input("Введите жанр книги: ").strip()
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE genre = ?", (genre,))
        books = cursor.fetchall()
        conn.close()

        if books:
            print(f"\n📚 Книги в жанре '{genre}':")
            for book in books:
                print(f"{book[1]} - {book[2]} ({book[3]})")
        else:
            print(f"⚠️ Нет книг в жанре '{genre}'.")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при поиске книг: {e}")


def update_book_year():
    title = input(
        "Введите название книги для обновления года издания: ").strip()
    new_year = input("Введите новый год издания: ").strip()

    try:
        new_year = int(new_year)
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET year = ? WHERE title = ?", (new_year, title))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Год издания книги '{title}' обновлен до {new_year}!")
        else:
            print(f"⚠️ Книга '{title}' не найдена в библиотеке.")
    except ValueError:
        print("❌ Ошибка: год должен быть числом!")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при обновлении книги: {e}")
    finally:
        conn.close()


def delete_book():
    title = input("Введите название книги, которую хотите удалить: ").strip()
    try:
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"🗑 Книга '{title}' удалена!")
        else:
            print(f"⚠️ Книга '{title}' не найдена.")
    except sqlite3.Error as e:
        print(f"❌ Ошибка при удалении книги: {e}")
    finally:
        conn.close()


def menu():
    create_database()

    while True:
        print("\n📖 Меню библиотеки:")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги по жанру")
        print("4. Обновить год издания книги")
        print("5. Удалить книгу")
        print("6. Выйти")

        choice = input("Выберите действие (1-6): ").strip()

        if choice == "1":
            title = input("Название книги: ").strip()
            author = input("Автор: ").strip()
            year = input("Год издания: ").strip()
            genre = input("Жанр: ").strip()
            try:
                year = int(year)
                add_book(title, author, year, genre)
            except ValueError:
                print("❌ Ошибка: год должен быть числом!")
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            show_books_by_genre()
        elif choice == "4":
            update_book_year()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("👋 Выход из программы.")
            break
        else:
            print("⚠️ Неизвестная команда, попробуйте еще раз.")


if __name__ == "__main__":
    menu()
