import json


class Book:
    def __init__(self, title, author, pages, status="unread"):
        self.title = title
        self.author = author
        self.pages = pages
        self.status = status

    def mark_finished(self):
        self.status = "finished"

    def __str__(self):
        return f"{self.title} by {self.author} - {self.pages} pages - {self.status}"

    def __repr__(self):
        return (
            f"Book(title={self.title!r}, author={self.author!r}, "
            f"pages={self.pages!r}, status={self.status!r})"
        )


class EBook(Book):
    def __init__(self, title, author, pages, file_format, status="unread"):
        super().__init__(title, author, pages, status)
        self.file_format = file_format

    def __str__(self):
        return f"{super().__str__()} - Format: {self.file_format}"

    def __repr__(self):
        return (
            f"EBook(title={self.title!r}, author={self.author!r}, "
            f"pages={self.pages!r}, file_format={self.file_format!r}, "
            f"status={self.status!r})"
        )


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def mark_finished(self, title):
        for book in self.books:
            if book.title == title:
                book.mark_finished()
                print(f'"{title}" has been marked as finished.')
                return

        print(f'Book "{title}" was not found in the library.')

    def get_books_by_status(self, status):
        return [book for book in self.books if book.status == status]

    def total_pages_read(self):
        return sum(
            book.pages
            for book in self.books
            if book.status == "finished"
        )

    def save_to_json(self, filename):
        data = []

        for book in self.books:
            book_data = {
                "type": "ebook" if isinstance(book, EBook) else "book",
                "title": book.title,
                "author": book.author,
                "pages": book.pages,
                "status": book.status
            }

            if isinstance(book, EBook):
                book_data["file_format"] = book.file_format

            data.append(book_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Library saved to {filename}.")

    def load_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self.books = []

            for item in data:
                if item["type"] == "ebook":
                    book = EBook(
                        item["title"],
                        item["author"],
                        item["pages"],
                        item["file_format"],
                        item["status"]
                    )
                else:
                    book = Book(
                        item["title"],
                        item["author"],
                        item["pages"],
                        item["status"]
                    )

                self.books.append(book)

            print(f"Library loaded from {filename}.")

        except FileNotFoundError:
            print(
                f'Could not load library: "{filename}" does not exist.'
            )

    def __str__(self):
        if not self.books:
            return "Library is empty."

        return "\n".join(str(book) for book in self.books)


# -------------------------
# Example usage
# -------------------------

library = Library()

book1 = Book(
    "Atomic Habits",
    "James Clear",
    320
)

book2 = Book(
    "The Alchemist",
    "Paulo Coelho",
    208,
    "reading"
)

ebook1 = EBook(
    "Python Crash Course",
    "Eric Matthes",
    544,
    "PDF"
)

library.add_book(book1)
library.add_book(book2)
library.add_book(ebook1)

print("All books:")
print(library)

print("\nMarking a book as finished:")
library.mark_finished("Atomic Habits")

print("\nFinished books:")
for book in library.get_books_by_status("finished"):
    print(book)

print("\nTotal pages read:")
print(library.total_pages_read())

print("\nSaving library:")
library.save_to_json("library.json")

print("\nTrying to load a missing file:")
new_library = Library()
new_library.load_from_json("does_not_exist.json")

print("\nLoading saved library:")
new_library.load_from_json("library.json")
print(new_library)