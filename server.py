from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db
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

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    session["user_email"] = None
    flash(f"Goodbye, {user.user_name}!")

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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
