# -*- coding: utf-8 -*-
"""
Created on Sun May  9 20:01:50 2021

@author: etudiant
"""

from flask.ext.bcrypt import Bcrypt
from flask import Flask
from flask.ext.bcrypt import generate_password_hash
from flask.ext.bcrypt import check_password_hash


app = Flask(__name__)
bcrypt = Bcrypt(app) 

password = 'hunter2'

pw_hash = generate_password_hash('hunter2', 10)
check_password_hash(pw_hash, 'hunter2')
print(pw_hash)


