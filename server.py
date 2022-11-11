from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db

from sys import argv
from pprint import pprint
import json

import requests

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.app_context().push()
app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/user_settings")
def user_settings():
    """View User Settings."""

    user = crud.get_user_by_email(session["user_email"])

    return render_template("user_settings.html", user=user)

@app.route("/poems")
def all_poems():
    """View all poems."""

    poems = crud.get_poems()

    return render_template("all_poems.html", poems=poems)


@app.route("/poems/<poem_id>")
def show_poem(poem_id):
    """Show details on a particular poem."""

    poem = crud.get_poem_by_id(poem_id)

    return render_template("poem_details.html", poem=poem)

@app.route("/poets")
def all_poets():
    """View all poets."""

    poets = crud.get_poets()

    return render_template("all_poets.html", poets=poets)


@app.route("/poets/<poet_id>")
def show_poet(poet_id):
    """Show details on a particular poet."""

    poet = crud.get_poet_by_id(poet_id)

    return render_template("poet_details.html", poet=poet)


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    user_name = request.form.get("username")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    user1 = crud.get_user_by_user_name(user_name)
    if user:
        flash("Cannot create an account with that email. Try again.")
    elif user1:
        flash("Cannot create an account with that username. Try again.")
    else:
        user = crud.create_user(user_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.user_name}!")

    return redirect("/")

@app.route("/logout")
def process_logout():
    """Process user logout."""

    user = crud.get_user_by_email(session["user_email"])
    user_name = user.user_name
    session.clear()
    flash(f"Goodbye, {user_name}!")

    return redirect("/")

@app.route("/delete_account")
def delete_user():
    """Delete User Account."""

    user = crud.get_user_by_email(session["user_email"])
    for comment in user.user_comments:
        db.session.delete(comment)
    db.session.delete(user)
    db.session.commit()
    session.clear()

    return redirect("/")

@app.route("/clear_session")
def clear_session():
    """For Debugging: Clears Session"""

    session.clear()

    return redirect("/")

@app.route("/update_comment", methods=["POST"])
def update_comment():
    """Update the text of a user comment."""
    comment_id = request.json["comment_id"]
    updated_comment = request.json["updated_comment"]
    crud.update_comment(comment_id, updated_comment)
    db.session.commit()

    return "Success"

@app.route("/poems/<poem_id>/comments", methods=["POST"])
def create_comment(poem_id):
    """Create a new comment for the poem."""

    logged_in_email = session.get("user_email")
    comment_text = request.form.get("comment")

    if logged_in_email is None:
        flash("You must log in to comment on a poem.")
    elif not comment_text:
        flash("Error: you didn't write anything for your comment.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        user_id = user.user_id
        poem = crud.get_poem_by_id(poem_id)
        poem_title = poem.poem_title

        comment = crud.create_comment(comment_text, user_id, poem_id)
        db.session.add(comment)
        db.session.commit()

        flash(f"You successfully left a comment on {poem_title}.")

    return redirect(f"/poems/{poem_id}")

@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    """Delete User Comment."""

    comment = crud.get_comment_by_comment_id(comment_id)
    user = comment.user
    db.session.delete(comment)
    db.session.commit()

    return redirect(f"/users/{user.user_id}")

@app.route("/users/<user_id>/bio", methods=["POST"])
def create_bio(user_id):
    """Create a user bio for the logged-in user."""

    logged_in_email = session.get("user_email")
    bio_text = request.form.get("bio")

    if logged_in_email is None:
        flash("You must log in to write a user bio.")
    elif not bio_text:
        flash("Error: you didn't write anything for your bio.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        user_id = user.user_id
        user_name = user.user_name

        crud.update_bio(user_id, bio_text)
        db.session.commit()

        flash(f"You successfully wrote a bio for yourself, {user_name}!")

    return redirect(f"/users/{user_id}")

@app.route("/add_random_poem")
def add_random_poem():
    '''Make GET request from Poemist API to grab random poem and add it to the database,'''
    '''and then send user to view that poem.'''
    
    # make the API request
    res = requests.get('https://www.poemist.com/api/v1/randompoems')
    poemist_poem = res.json()
    print(poemist_poem)

    # check to see if poet is already in database, if not, create the poet
    poets_in_db = crud.get_poets()
    random_poet = poemist_poem[0]['poet']['name']
    new_poem_poet = ""
    for poet in poets_in_db:
        if poet.name == random_poet:
            new_poem_poet = crud.get_poet_by_name(random_poet)
    if not new_poem_poet:
        new_poem_poet = crud.create_poet(random_poet)
        db.session.add(new_poem_poet)
        db.session.commit()

    # check to see if poem is already in database, if not, create the poem
    poems_by_poet = new_poem_poet.poems
    random_poem = poemist_poem[0]["title"]
    poem_in_poets = False

    for poem in poems_by_poet:
        if poem.poem_title == random_poem:
            poem_in_poets = True
            flash('Poem already in database; please try again!')
    if not poem_in_poets:
        new_poem = crud.create_poem(random_poem, new_poem_poet.poet_id)
        db.session.add(new_poem)
        db.session.commit()

    # take poem text from JSON, split into list of line strings
    new_poem_text = poemist_poem[0]["content"]
    new_poem_lines = new_poem_text.split('\n')
    print(new_poem_lines)

    # create line object for each line in list
    for line in new_poem_lines:
        new_line = crud.create_line(line, new_poem.poem_id)
        db.session.add(new_line)
        db.session.commit()
    
    # send user to poem_details template for newly created poem
    poem = new_poem

    return render_template("poem_details.html", poem=poem)





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
