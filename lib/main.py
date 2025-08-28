import click
from crud import (
    create_author, delete_author, get_all_authors, find_author_by_id, find_author_by_name,
    create_publisher, delete_publisher, get_all_publishers, find_publisher_by_id, find_publisher_by_name,
    create_book, delete_book, get_all_books, find_book_by_id, find_book_by_title, get_books_by_author,
    get_books_by_publisher, get_book_relations
)
from models import Session

# Menu definitions
MAIN_MENU = [
    ("Manage Authors", "author"),
    ("Manage Publishers", "publisher"),
    ("Manage Books", "book"),
    ("Exit", "exit")
]

ENTITY_MENUS = {
    "author": [
        "Add new author",
        "List all authors",
        "Update author",
        "Delete author",
        "Find author by ID",
        "Find author by name",
        "List books by author",
        "Back"
    ],
    "publisher": [
        "Add new publisher",
        "List all publishers",
        "Update publisher",
        "Delete publisher",
        "Find publisher by ID",
        "Find publisher by name",
        "List books by publisher",
        "Back"
    ],
    "book": [
        "Add new book",
        "List all books",
        "Update book",
        "Delete book",
        "Find book by ID",
        "Find book by title",
        "View author and publisher",
        "Back"
    ]
}

# Field definitions for create/update prompts
ENTITY_FIELDS = {
    "author": [
        ("first_name", "First name", str, None),
        ("last_name", "Last name", str, None),
        ("birth_year", "Birth year", int, None),
        ("nationality", "Nationality", str, None)
    ],
    "publisher": [
        ("name", "Name", str, None),
        ("founded_year", "Founded year", int, None),
        ("location", "Location", str, None),
        ("website", "Website (optional)", str, None)
    ],
    "book": [
        ("title", "Title", str, None),
        ("publication_year", "Publication year", int, None),
        ("genre", "Genre", str, None),
        ("author_id", "Author ID", int, None),
        ("publisher_id", "Publisher ID", int, None)
    ]
}

# Entity-specific CRUD functions
ENTITY_CRUD = {
    "author": {
        "create": create_author,
        "delete": delete_author,
        "list": get_all_authors,
        "find_by_id": find_author_by_id,
        "find_by_name": find_author_by_name,
        "list_related": get_books_by_author
    },
    "publisher": {
        "create": create_publisher,
        "delete": delete_publisher,
        "list": get_all_publishers,
        "find_by_id": find_publisher_by_id,
        "find_by_name": find_publisher_by_name,
        "list_related": get_books_by_publisher
    },
    "book": {
        "create": create_book,
        "delete": delete_book,
        "list": get_all_books,
        "find_by_id": find_book_by_id,
        "find_by_name": find_book_by_title,
        "list_related": get_book_relations
    }
}