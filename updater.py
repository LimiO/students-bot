#!/usr/local/bin/python3.8
import db

users = db.get_users()
for user in users:
    user.reset_limits()
