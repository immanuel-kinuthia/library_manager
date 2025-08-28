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

def list_entity(session, entity_type):
    """List all entities of a given type."""
    entities = ENTITY_CRUD[entity_type]["list"](session)
    if not entities:
        click.echo(f"No {entity_type}s found.")
        return
    click.echo(f"\n--- All {entity_type.title()}s ---")
    for e in entities:
        if entity_type == "author":
            click.echo(f"{e.id}. {e.full_name} - Birth Year: {e.birth_year}, Nationality: {e.nationality}")
        elif entity_type == "publisher":
            click.echo(f"{e.id}. {e.name} - Founded: {e.founded_year}, Location: {e.location}, Website: {e.website or 'N/A'}")
        else:  # book
            author = find_author_by_id(session, e.author_id)
            publisher = find_publisher_by_id(session, e.publisher_id)
            click.echo(f"{e.id}. {e.title} - Year: {e.publication_year}, Genre: {e.genre}, "
                       f"Author: {author.full_name if author else 'Unknown'}, Publisher: {publisher.name if publisher else 'Unknown'}")

def run_menu(session, menu_type, menu_options, entity_type=None):
    """Generic menu handler for main or entity menus."""
    while True:
        click.echo(f"\n--- {menu_type} ---")
        for i, (option, _) in enumerate(menu_options, 1):
            click.echo(f"{i}. {option}")
        choice = click.prompt("Enter choice", type=click.Choice([str(i) for i in range(1, len(menu_options) + 1)]), show_choices=False)
        choice = int(choice) - 1
        if menu_options[choice][1] == "exit":
            return "exit"
        elif menu_options[choice][1] == "back":
            return None
        elif entity_type:
            handle_entity_action(session, entity_type, choice)
        else:
            return menu_options[choice][1]

def handle_entity_action(session, entity_type, choice):
    """Handle entity-specific actions based on menu choice."""
    if choice == 0:  # Add new
        fields = {f[0]: click.prompt(f[1], type=f[2], default=f[3]) for f in ENTITY_FIELDS[entity_type]}
        try:
            if entity_type == "book":
                list_entity(session, "author")
                list_entity(session, "publisher")
            entity = ENTITY_CRUD[entity_type]["create"](session, **fields)
            click.echo(f"{entity_type.title()} '{getattr(entity, 'full_name', getattr(entity, 'name', entity.title))}' added successfully!")
        except ValueError as e:
            click.echo(f"Error: {e}")
    elif choice == 1:  # List all
        list_entity(session, entity_type)
    elif choice == 2:  # Update
        list_entity(session, entity_type)
        entity_id = click.prompt(f"Enter {entity_type.title()} ID to update", type=int)
        entity = ENTITY_CRUD[entity_type]["find_by_id"](session, entity_id)
        if not entity:
            click.echo(f"{entity_type.title()} not found.")
            return
        fields = {f[0]: click.prompt(f"{f[1]} [{getattr(entity, f[0], 'N/A')}]", type=f[2], default=getattr(entity, f[0])) for f in ENTITY_FIELDS[entity_type]}
        try:
            if entity_type == "book":
                list_entity(session, "author")
                list_entity(session, "publisher")
            for key, value in fields.items():
                setattr(entity, key, value)
            session.commit()
            click.echo(f"{entity_type.title()} '{getattr(entity, 'full_name', getattr(entity, 'name', entity.title))}' updated successfully!")
        except ValueError as e:
            click.echo(f"Error: {e}")
     elif choice == 3:  # Delete
        list_entity(session, entity_type)
        entity_id = click.prompt(f"Enter {entity_type.title()} ID to delete", type=int)
        if ENTITY_CRUD[entity_type]["delete"](session, entity_id):
            click.echo(f"{entity_type.title()} deleted successfully!")
        else:
            click.echo(f"{entity_type.title()} not found.")