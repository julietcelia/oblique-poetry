'''Class models for Sonnet Trace'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    '''A user.'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    user_comments = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))

    comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} user_name={self.user_name}>'

class Comment(db.Model):
    '''A comment.'''

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.poem_id'))

    user = db.relationship('User', back_populates='comments')
    poem = db.relationship('Poem', back_populates='comments')

    def __repr__(self):
        return f"<Comment comment_id={self.comment_id} user_id={self.user_id} poem_id={self.poem_id}>"

class Poem(db.Model):
    '''A poem.'''

    __tablename__ = 'poems'

    poem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    poem_title = db.Column(db.String)
    poem_type = db.Column(db.String)
    poem_text = db.Column(db.Text)
    poet = db.Column(db.Integer, db.ForeignKey('poets.poet_id'))
    comments = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))

    comments = db.relationship('Comment', back_populates='poem')
    poet = db.relationship('Poet', back_populates='poems')
    books = db.relationship('Book', secondary='books_poems', back_populates='poems')

    def __repr__(self):
        return f"<Poem poem_id={self.poem_id} poem_title={self.poem_title}>"

class BookPoem(db.Model):
    '''An anthology containing a specific poem.'''

    __tablename__ = 'books_poems'

    book_poem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.poem_id'), nullable=False)

class Book(db.Model):
    '''An anthology.'''

    __tablename__ = 'books'

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_title = db.Column(db.String)
    book_date = db.Column(db.Integer)
    book_cover = db.Column(db.String)
    book_link = db.Column(db.String)
    
    poems = db.relationship('Poem', secondary='books_poems', back_populates='books')

    def __repr__(self):
        return f"<Book book_id={self.book_id} book_title={self.book_title}>"

class Poet(db.Model):
    '''A poet.'''

    __tablename__ = 'poets'

    poet_id = db.Column(db.String, autoincrement=True, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    birthdate = db.Column(db.Integer)
    deathdate = db.Column(db.Integer)
    poems_by_poet = db.Column(db.Integer, db.ForeignKey('poems.poem_id'))

    poems = db.relationship('Poem', back_populates='poet')

    def __repr__(self):
        return f'<Poet poet_id={self.poet_id} fname={self.fname} lname={self.lname}>'

# def connect_to_db(flask_app, db_uri="postgresql:///", echo=False):
#     flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
#     flask_app.config["SQLALCHEMY_ECHO"] = echo
#     flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#     db.app = flask_app
#     db.init_app(flask_app)

#     print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)