from model import db, User, Comment, Poem, Line, BookPoem, Book, Poet, connect_to_db


def create_user(user_name, email, password):
    """Create and return a new user."""

    user = User(user_name=user_name, email=email, password=password)

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_user_name(user_name):
    """Return a user by username."""

    return User.query.filter(User.user_name == user_name).first()

def create_poem(poem_title, poem_type, poet_id):
    """Create and return a new poem."""

    poem = Poem(
        poem_title=poem_title,
        poem_type=poem_type,
        poet_id=poet_id,
    )

    return poem

def get_poems():
    """Return all poems."""

    return Poem.query.all()

def get_poem_by_id(poem_id):
    """Return a poem by primary key."""

    return Poem.query.get(poem_id)

def create_book(book_title, book_date, book_cover, book_link):
    """Create and return a poetry anthology."""

    book = Book(
        book_title=book_title,
        book_date=book_date,
        book_cover=book_cover,
        book_link=book_link
    )

    return book

def get_books():
    """Return all poetry anthologies."""

    return Book.query.all()

def get_book_by_id(book_id):
    """Return a poetry anthology by primary key."""

    return Book.query.get(book_id)

def create_poet(fname, lname, birthdate="0", deathdate="0"):
    """Create and return a poet."""

    poet = Poet(
        fname=fname,
        lname=lname,
        birthdate=birthdate,
        deathdate=deathdate
    )

    return poet

def get_poets():
    """Return all poets."""

    return Poet.query.all()

def get_poet_by_id(poet_id):
    """Return a poet by primary key."""

    return Poet.query.get(poet_id)

def get_poet_by_last_name(lname):
    """Return a poet by last name."""

    return Poet.query.get(lname)

def create_comment(comment_text, user_id, poem_id):
    """Create and return a new comment."""

    comment = Comment(
        comment_text = comment_text,
        user_id = user_id,
        poem_id = poem_id
    )

    return comment

def update_comment(comment_id, new_text):
    """ Update a rating given rating_id and the updated score. """
    comment = Comment.query.get(comment_id)
    comment.comment_text = new_text

if __name__ == "__main__":
    from server import app

    connect_to_db(app)