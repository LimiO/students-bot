#!/usr/local/bin/python3.8
import os
import sys
import db

print('something')
users = db.get_users()
print(users)
for user in users:
    print(user.id)
    user.reset_limits()