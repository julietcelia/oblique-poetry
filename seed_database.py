import os
import json
from random import choice, randint

import crud
import model
import server

os.system("dropdb sonnettrace")
os.system("createdb sonnettrace")

model.connect_to_db(server.app)
model.db.create_all()

with open("data/poets.json") as f:
    poet_data = json.loads(f.read())

poets_in_db = []
for poet in poet_data:
    fname, lname, birthdate, deathdate = (
        poet["fname"],
        poet["lname"],
        poet["birthdate"],
        poet["deathdate"]
    )

    db_poet = crud.create_poet(fname, lname, birthdate, deathdate)
    poets_in_db.append(db_poet)

model.db.session.add_all(poets_in_db)
model.db.session.commit()

with open("data/poems.json") as f:
    poem_data = json.loads(f.read())

poems_in_db = []
for poem in poem_data:
    poem_title, poem_type, poet_id = (
        poem["poem_title"],
        poem["poem_type"],
        poem["poet_id"]
    )

    db_poem = crud.create_poem(poem_title, poem_type, poet_id)
    poems_in_db.append(db_poem)

model.db.session.add_all(poems_in_db)
model.db.session.commit()

with open("data/lines.json") as f:
    line_data = json.loads(f.read())

lines_in_db = []
for line in line_data:
    line_text, poem_id = (
        line["line_text"],
        line["poem_id"]
    )

    db_line = crud.create_line(line_text, poem_id)
    lines_in_db.append(db_line)

model.db.session.add_all(lines_in_db)
model.db.session.commit()

test_comments = [
    "Beautiful!",
    "Wow!",
    "Interesting...",
    "Intriguing.",
    "What does it mean?",
    "Literally me.",
    "This is a favorite.",
    "I don't understand this one.",
    "So pretty...",
    "I have to read more!",
    "This one gets me",
    "So powerful!",
]

for n in range(10):
    user_name = f"user{n}"
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(user_name, email, password)
    model.db.session.add(user)
    model.db.session.commit()

users_in_db = crud.get_users()
for user in users_in_db:
    for n in range(10):
        random_poem = choice(poems_in_db)
        comment_text = choice(test_comments)

        comment = crud.create_comment(comment_text, user.user_id, random_poem.poem_id)
        model.db.session.add(comment)
        model.db.session.commit()