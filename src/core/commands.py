import sys

import bcrypt

from core.resources.database import client


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_dummy_users_command():
    """Create dummy users in MongoDB"""

    db = client.db
    collection = db.users

    users_exist = collection.count_documents({})
    if users_exist:
        sys.stdout.write("create_dummy_users(): Users already exist \n")
        return

    users = [
        {
            "firstname": "John",
            "lastname": "Doe",
            "email": "johndoe@example.com",
            "password": hash_password("TestPassword"),
        },
        {
            "firstname": "Jane",
            "lastname": "Doe",
            "email": "janedoe@example.com",
            "password": hash_password("TestPassword"),
        },
    ]

    for user in users:
        collection.insert_one(user)

    sys.stdout.write("create_dummy_users(): Users created \n")
