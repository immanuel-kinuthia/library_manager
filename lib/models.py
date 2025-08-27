from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

ENGINE = create_engine('sqlite:///lib/db/library.db')
Base = declarative_base()
Session = sessionmaker(bind=ENGINE)

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)
    nationality = Column(String, nullable=False)
    
    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @full_name.setter
    def full_name(self, value):
        parts = value.split()
        if len(parts) < 2:
            raise ValueError("Full name must include first and last name.")
        self.first_name, self.last_name = parts[0], ' '.join(parts[1:])
    
    def __repr__(self):
        return f"Author(id={self.id}, name='{self.full_name}', birth_year={self.birth_year}, nationality='{self.nationality}')"

class Publisher(Base):
    __tablename__ = 'publishers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    founded_year = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    website = Column(String)
    
    books = relationship('Book', back_populates='publisher', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"Publisher(id={self.id}, name='{self.name}', founded_year={self.founded_year}, location='{self.location}')"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    publication_year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)
    
    author = relationship('Author', back_populates='books')
    publisher = relationship('Publisher', back_populates='books')
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', year={self.publication_year}, genre='{self.genre}', author_id={self.author_id}, publisher_id={self.publisher_id})"