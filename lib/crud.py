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