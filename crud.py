from model import db, User, Poem, Line, Poet, connect_to_db


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

def update_user_name(user, newname):
    """Update user's username."""

    user.user_name = newname
    db.session.commit()
    

def update_user_email(user, newemail):
    """Update user's email."""

    user.email = newemail
    db.session.commit()

def update_user_password(user, newpass):
    """Update user's password."""

    user.password = newpass
    db.session.commit()

def create_poem(poem_title, poet_id):
    """Create and return a new poem."""

    poem = Poem(
        poem_title=poem_title,
        poet_id=poet_id
    )

    return poem

def get_poems():
    """Return all poems."""

    return Poem.query.all()

def get_poem_by_id(poem_id):
    """Return a poem by primary key."""

    return Poem.query.get(poem_id)

def create_poet(name):
    """Create and return a poet."""

    poet = Poet(name=name)

    return poet

def get_poets():
    """Return all poets."""

    return Poet.query.all()

def get_poet_by_id(poet_id):
    """Return a poet by primary key."""

    return Poet.query.get(poet_id)

def get_poet_by_name(name):
    """Return a poet by name."""

    return Poet.query.filter(Poet.name == name).first()

def create_line(line_text, poem_id):
    """Create and return a new line of poetry."""

    line = Line(
        line_text = line_text,
        poem_id = poem_id
    )

    return line

def get_lines():
    """Return all lines."""

    return Line.query.all()

def get_lines_by_poem(poem_id):
    """Return lines in a poem by poem's primary key."""

    return Line.query.filter(Line.poem_id == poem_id).all()

def get_line_by_line_id(line_id):
    """Return a line of poetry by primary key."""

    return Line.query.get(line_id)

def update_line(line_id, new_text):
    """Update a line of poetry given primary key and new line text."""
    
    line = Line.query.get(line_id)
    line.line_text = new_text

if __name__ == "__main__":
    from server import app

    connect_to_db(app)