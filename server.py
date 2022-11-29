from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db

from sys import argv
import json

import requests

import random

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


@app.route("/poems/<poem_id>")
def show_poem(poem_id):
    """Show details on a particular poem."""

    poem = crud.get_poem_by_id(poem_id)

    return render_template("poem_details.html", poem=poem)

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

@app.route("/email", methods=["POST"])
def change_email():
    """Process change of user email."""

    user = crud.get_user_by_email(session["user_email"])
    newemail = request.form.get("newemail")
    alreadyexists = crud.get_user_by_email(newemail)
    
    if alreadyexists:
        flash("This email already has an associated account.")
    else:
        crud.update_user_email(user, newemail)
        session.clear()
        flash("Email successfully updated, please log back in with new email.")

    return redirect("/")

@app.route("/password", methods=["POST"])
def change_password():
    """Process change of user password."""

    user = crud.get_user_by_email(session["user_email"])
    newpass = request.form.get("newpass")
    crud.update_user_password(user, newpass)
    session.clear()
    flash("Password successfully updated, please log back in with new password.")

    return redirect("/")

@app.route("/username", methods=["POST"])
def change_username():
    """Process change of username."""

    user = crud.get_user_by_email(session["user_email"])
    newname = request.form.get("newname")
    alreadyexists = crud.get_user_by_user_name(newname)
    
    if alreadyexists:
        flash("This username already has an associated account.")
    else:
        crud.update_user_name(user, newname)
        session.clear()
        flash("Username successfully updated, please log back in.")

    return redirect("/")

@app.route("/delete_account")
def delete_user():
    """Delete User Account."""

    user = crud.get_user_by_email(session["user_email"])
    db.session.delete(user)
    db.session.commit()
    session.clear()

    return redirect("/")

@app.route("/clear_session")
def clear_session():
    """For Debugging: Clears Session"""

    session.clear()

    return redirect("/")

def make_request():
    
    res = requests.get('https://poetrydb.org/random')

    print('response:', res)
    print('response.text:', res.text)
    print('response.status_code:', res.status_code)
    print('response.headers:', res.headers)

    if (res.status_code != 204
            and 'content-type' in res.headers
            and 'application/json' in res.headers['content-type']):
        parsed = res.json()
        print('parsed response:', parsed)
        return parsed
    else:
        print('conditions not met')
        return make_request()

@app.route("/add_random_poem")
def add_random_poem():
    '''Make GET request from PoetryDB API to grab random poem and add it to the database,'''
    '''and then send user to view that poem.'''
    
    # make the API request

    json_poem = make_request()
    print(json_poem)

    # check to see if poet is already in database, if not, create the poet
    poets_in_db = crud.get_poets()
    random_poet = json_poem[0]['author']
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
    random_poem = json_poem[0]["title"]
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
    new_poem_lines = json_poem[0]["lines"]
    print(new_poem_lines)

    # create line object for each line in list
    for line in new_poem_lines:
        new_line = crud.create_line(line, new_poem.poem_id)
        db.session.add(new_line)
        db.session.commit()
    
    # send user to poem_details template for newly created poem
    poem = new_poem

    return render_template("poem_details.html", poem=poem)

@app.route("/create_random_poem")
def randomize_poem():
    
    all_lines = crud.get_lines()

    random_poem = random.choice(all_lines)
    new_poem = crud.create_poem(random_poem.line_text, 1)
    db.session.add(new_poem)
    db.session.commit()

    # take poem text from JSON, split into list of line strings
    line_number = random.randint(4, 20)
    new_poem_lines = []
    i = 0
    while i < line_number:
        new_poem_lines.append(random.choice(all_lines))
        i = i + 1

    # create line object for each line in list
    for line in new_poem_lines:
        new_line = crud.create_line(line.line_text, new_poem.poem_id)
        db.session.add(new_line)
        db.session.commit()
    
    # send user to poem_details template for newly created poem
    poem = new_poem

    return render_template("poem_details.html", poem=poem)

@app.route("/prompts")
def view_prompts():
    """Displays prompt page."""
    
    return render_template("prompts.html")

@app.route("/show_prompt")
def show_prompts():
    """Reveals hidden prompt."""

    all_prompts = crud.get_prompts()
    prompt_texts = []
    for prompt in all_prompts:
        prompt_texts.append(prompt.prompt_text)
    return random.choice(prompt_texts)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
