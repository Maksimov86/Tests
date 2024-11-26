import os
import json
from typing import List, Dict, Union

DATA_FILE = "data.json"

class Book:
    def __init__(self, title: str, author: str, year: int):
        self.id = self.generate_id()
        self.title = title.strip()
        self.author = author.strip()
        self.year = year
        self.status = "в наличии"

    @staticmethod
    def generate_id() -> int:
        """Генерирует уникальный идентификатор книги."""
        data = Library.load_data()
        if data:
            return max(book["id"] for book in data) + 1
        return 1

    def to_dict(self) -> Dict:
        """Преобразует объект книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Book':
        """Создает объект книги из словаря."""
        book = Book(data["title"], data["author"], data["year"])
        book.id = data["id"]
        book.status = data["status"]
        return book


class Library:
    @staticmethod
    def load_data() -> List[Dict]:
        """Загружает данные из JSON-файла."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    @staticmethod
    def save_data(data: List[Dict]):
        """Сохраняет данные в JSON-файл."""
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def add_book(title: str, author: str, year: Union[str, int]):
        """Добавляет книгу в библиотеку."""
        try:
            year = int(year)
            if year < 0:
                raise ValueError("Год не может быть отрицательным.")
        except ValueError as e:
            print(f"Ошибка: {e}")
            return
        book = Book(title, author, year)
        data = Library.load_data()
        data.append(book.to_dict())
        Library.save_data(data)
        print(f"Книга '{title}' успешно добавлена.")

    @staticmethod
    def delete_book(book_id: Union[str, int]):
        """Удаляет книгу по id."""
        try:
            book_id = int(book_id)
        except ValueError:
            print("Ошибка: id должен быть числом.")
            return
        data = Library.load_data()
        filtered_data = [book for book in data if book["id"] != book_id]
        if len(data) == len(filtered_data):
            print(f"Книга с id {book_id} не найдена.")
        else:
            Library.save_data(filtered_data)
            print(f"Книга с id {book_id} успешно удалена.")

    @staticmethod
    def search_books(query: str):
        """Ищет книги по названию, автору или году, поддерживает частичные совпадения."""
        data = Library.load_data()
        query = query.lower()
        results = [
            book for book in data
            if query in book["title"].lower() or 
               query in book["author"].lower() or 
               query in str(book["year"])
        ]
        if results:
            Library.display_books(results)
        else:
            print(f"Книги по запросу '{query}' не найдены.")

    @staticmethod
    def display_books(data: Union[None, List[Dict]] = None):
        """Отображает список всех книг или переданный список."""
        if data is None:
            data = Library.load_data()
        if not data:
            print("Библиотека пуста.")
        else:
            print("Список книг:")
            for book in data:
                print(f"[{book['id']}] {book['title']} - {book['author']} ({book['year']}), статус: {book['status']}")

    @staticmethod
    def change_status(book_id: Union[str, int], status: str):
        """Изменяет статус книги."""
        if status not in ["в наличии", "выдана"]:
            print("Ошибка: некорректный статус. Доступные статусы: 'в наличии', 'выдана'.")
            return
        try:
            book_id = int(book_id)
        except ValueError:
            print("Ошибка: id должен быть числом.")
            return
        data = Library.load_data()
        for book in data:
            if book["id"] == book_id:
                book["status"] = status
                Library.save_data(data)
                print(f"Статус книги с id {book_id} успешно изменен на '{status}'.")
                return
        print(f"Книга с id {book_id} не найдена.")


def main():
    while True:
        print("\n--- Меню ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ").strip()
            year = input("Введите год издания: ").strip()
            Library.add_book(title, author, year)
        elif choice == "2":
            book_id = input("Введите id книги: ").strip()
            Library.delete_book(book_id)
        elif choice == "3":
            query = input("Введите имя автора, название книги или год: ").strip()
            Library.search_books(query)
        elif choice == "4":
            Library.display_books()
        elif choice == "5":
            book_id = input("Введите id книги: ").strip()
            status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
            Library.change_status(book_id, status)
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
