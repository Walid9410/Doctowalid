# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:53:17 2021

@author: etudiant
"""

from flask import Flask
from flask_ngrok import run_with_ngrok
  
app = Flask(__name__)
run_with_ngrok(app)
  
@app.route("/")
def hello():
    return "Hello Geeks!! from Google Colab"
  
if __name__ == "__main__":
  app.run()