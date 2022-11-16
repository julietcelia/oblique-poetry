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
    name = (poet["name"])
    db_poet = crud.create_poet(name)
    poets_in_db.append(db_poet)

model.db.session.add_all(poets_in_db)
model.db.session.commit()

with open("data/poems.json") as f:
    poem_data = json.loads(f.read())

poems_in_db = []
for poem in poem_data:
    poem_title, poet_id = (
        poem["poem_title"],
        poem["poet_id"]
    )

    db_poem = crud.create_poem(poem_title, poet_id)
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

for n in range(10):
    user_name = f"user{n}"
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(user_name, email, password)
    model.db.session.add(user)
    model.db.session.commit()