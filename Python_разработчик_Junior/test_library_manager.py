import unittest
from library_manager import Library, Book

class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        """Подготовка: сброс данных перед каждым тестом."""
        Library.save_data([])

    def test_add_book(self):
        Library.add_book("1984", "George Orwell", 1949)
        data = Library.load_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "1984")

    def test_delete_book(self):
        Library.add_book("1984", "George Orwell", 1949)
        book_id = Library.load_data()[0]["id"]
        Library.delete_book(book_id)
        data = Library.load_data()
        self.assertEqual(len(data), 0)

    def test_search_books(self):
        Library.add_book("1984", "George Orwell", 1949)
        Library.add_book("Animal Farm", "George Orwell", 1945)
        results = [book["title"] for book in Library.load_data() if book["author"] == "George Orwell"]
        self.assertIn("1984", results)
        self.assertIn("Animal Farm", results)

    def test_change_status(self):
        Library.add_book("1984", "George Orwell", 1949)
        book_id = Library.load_data()[0]["id"]
        Library.change_status(book_id, "выдана")
        status = Library.load_data()[0]["status"]
        self.assertEqual(status, "выдана")

if __name__ == "__main__":
    unittest.main()
