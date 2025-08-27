from sqlalchemy.exc import IntegrityError
from models import Author, Publisher, Book

def create_author(session, first_name, last_name, birth_year, nationality):
    if birth_year < 0:
        raise ValueError("Birth year must be positive.")
    if not all([first_name, last_name, nationality]):
        raise ValueError("All fields are required.")
    author = Author(first_name=first_name, last_name=last_name, birth_year=birth_year, nationality=nationality)
    session.add(author)
    session.commit()
    return author

def delete_author(session, id):
    author = find_author_by_id(session, id)
    if author:
        session.delete(author)
        session.commit()
        return True
    return False

def get_all_authors(session):
    return session.query(Author).all()

def find_author_by_id(session, id):
    return session.query(Author).filter_by(id=id).first()

def find_author_by_name(session, full_name):
    parts = full_name.split()
    first_name = parts[0]
    last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    return session.query(Author).filter_by(first_name=first_name, last_name=last_name).first()

def get_books_by_author(session, author_id):
    author = find_author_by_id(session, author_id)
    if author:
        return author.books
    return []

def create_publisher(session, name, founded_year, location, website):
    if founded_year < 0:
        raise ValueError("Founded year must be positive.")
    if not all([name, location]):
        raise ValueError("Name and location are required.")
    publisher = Publisher(name=name, founded_year=founded_year, location=location, website=website)
    try:
        session.add(publisher)
        session.commit()
        return publisher
    except IntegrityError:
        session.rollback()
        raise ValueError("Publisher name must be unique.")

def delete_publisher(session, id):
    publisher = find_publisher_by_id(session, id)
    if publisher:
        session.delete(publisher)
        session.commit()
        return True
    return False

def get_all_publishers(session):
    return session.query(Publisher).all()

def find_publisher_by_id(session, id):
    return session.query(Publisher).filter_by(id=id).first()

def find_publisher_by_name(session, name):
    return session.query(Publisher).filter_by(name=name).first()

def get_books_by_publisher(session, publisher_id):
    publisher = find_publisher_by_id(session, publisher_id)
    if publisher:
        return publisher.books
    return []

def create_book(session, title, publication_year, genre, author_id, publisher_id):
    if publication_year < 0:
        raise ValueError("Publication year must be positive.")
    if not all([title, genre, author_id, publisher_id]):
        raise ValueError("All fields are required.")
    if not find_author_by_id(session, author_id):
        raise ValueError("Author not found.")
    if not find_publisher_by_id(session, publisher_id):
        raise ValueError("Publisher not found.")
    book = Book(title=title, publication_year=publication_year, genre=genre, author_id=author_id, publisher_id=publisher_id)
    try:
        session.add(book)
        session.commit()
        return book
    except IntegrityError:
        session.rollback()
        raise ValueError("Book title must be unique.")

def delete_book(session, id):
    book = find_book_by_id(session, id)
    if book:
        session.delete(book)
        session.commit()
        return True
    return False

def get_all_books(session):
    return session.query(Book).all()

def find_book_by_id(session, id):
    return session.query(Book).filter_by(id=id).first()

def find_book_by_title(session, title):
    return session.query(Book).filter_by(title=title).first()

def get_book_relations(session, book_id):
    book = find_book_by_id(session, book_id)
    if book:
        return book.author, book.publisher
    return None, None