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
    user_bio = db.Column(db.Text)

    user_comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} user_name={self.user_name}>'

class Comment(db.Model):
    '''A comment.'''

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.poem_id'), nullable=False)

    user = db.relationship('User', back_populates='user_comments')
    poem = db.relationship('Poem', back_populates='poem_comments')

    def __repr__(self):
        return f"<Comment comment_id={self.comment_id} user_id={self.user_id} poem_id={self.poem_id}>"

class Poem(db.Model):
    '''A poem.'''

    __tablename__ = 'poems'

    poem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    poem_title = db.Column(db.String)
    poet_id = db.Column(db.Integer, db.ForeignKey('poets.poet_id'), nullable=False)

    poem_comments = db.relationship('Comment', back_populates='poem')
    poet = db.relationship('Poet', back_populates='poems')
    lines = db.relationship('Line', back_populates='poem')

    def __repr__(self):
        return f"<Poem poem_id={self.poem_id} poem_title={self.poem_title}>"

class Line(db.Model):
    '''A line of poetry.'''

    __tablename__ = 'lines'

    line_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    line_text = db.Column(db.Text)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.poem_id'), nullable=False)

    poem = db.relationship('Poem', back_populates='lines')

    def __repr__(self):
        return f"<Line line_id={self.line_id} line_text={self.line_text}>"

class Poet(db.Model):
    '''A poet.'''

    __tablename__ = 'poets'

    poet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)

    poems = db.relationship('Poem', back_populates='poet')

    def __repr__(self):
        return f'<Poet poet_id={self.poet_id} fname={self.fname} lname={self.lname}>'

def connect_to_db(flask_app, db_uri="postgresql:///sonnettrace", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)