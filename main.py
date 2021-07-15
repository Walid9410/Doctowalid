# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:52:54 2021

@author: etudiant
"""

from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import json as JSON
from flask_socketio import SocketIO

from flask.ext.bcrypt import generate_password_hash

#from flask_ngrok import run_with_ngrok



app = Flask(__name__)
#run_with_ngrok(app) 


##########
PHOTO_FOLDER = os.path.join('static', 'photo')
app.config['UPLOAD_FOLDER'] = PHOTO_FOLDER
###############

app.config["DEBUG"]=True

app.config["user"]=os.getcwd()+"/fhir/user"


##################################################################
'''
@app.route('/testjson', methods=['GET','POST'])
def json():
    global user
    user=str(request.args.get('username'))
    print('user')
    mdp=str(request.args.get('password'))
    fichier="fhir/user/"+user+".json"
    print(fichier)
    var=open(fichier)
    charge=JSON.load(var)
    var.close()
    
    if mdp == charge["mdp"]:
        return render_template("home.html",charge=charge)
    return render_template("index.html",charge=charge)
 '''   

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'vitrygtr'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vitrygtr'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)
@app.route("/")
def acc():
    return render_template('acc.html')
    
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    global user
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        print(password)
        pw_hash = generate_password_hash(password, 10)
        print('Mots de passe hache de ',password,'est',pw_hash)
        
#        user=str(request.form['username'])
#        print('user')
#        mdp=str(request.form['password'])
#        fichier="fhir/user/"+user+".json"
#        print(fichier)
#        var=open(fichier)
#        charge=JSON.load(var)
#        var.close()
#        if mdp == charge["test"]:
#            return render_template("home.html",charge=charge)
    
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        #cursor.execute('SELECT * FROM doctor WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        
        
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrecte login/motsdepasse!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

socketio = SocketIO(app,cor_allowed_origins="*")
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)



#####################################################################################################"
   ### Cote patient

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    
    
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone=request.form['phone']
        
        print(password)
        pw_hash = generate_password_hash(password, 10)
        print('Mots de passe hache de ',password,'est',pw_hash) ####mots de passe hache
        #######creation json
        
        Utilisateur=request.form['username']
        mdp = request.form['password']
        mail = request.form['email']
        tel=request.form['phone']
    
    
        data = { 
             "id":15,   
            	"ressourceType":"Patient",
            "Username": Utilisateur,
            "password":mdp,
            "mail":mail,
            "phone":tel,
	"organization": "/fhir/Organization?_id=15"
            
            }
        with open ("15.json","w") as f_write:
            JSON.dump(data,f_write,indent=1)
    
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        
  
        
        # If account exists show error and validation checks
        if account:
            msg = 'Un compte existe déjà!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Adresse mail invalide ! Veuillez rentrer mail de la forme test@mail.com'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Veuillez remplir le formulaire !'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s,%s,%s)', (username, password, email,phone,pw_hash))
            mysql.connection.commit()
            msg = 'Vous êtes enrengistrer!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Veuillez remplir le formulaire !'
    # Show registration form with message (if any)
    
    return render_template('register.html', msg=msg)
'''
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def json1():
    
    L=[]
    Utilisateur=request.form['username']
    mdp = request.form['password']
    mail = request.form['email']
    tel=request.form['phone']
    
    data = { 
            	"ressourceType":"patient",
            "Username": Utilisateur,
            "password":mdp,
            "mail":mail,
            "phone":tel,
	"organization": "/fhir/Organization?_id=1"
            
            }
    with open (Utilisateur+".json","w") as f_write:
        json.dump(data,f_write,indent=1)
        print(L)
        return str(L)
'''

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/inter_med_agenda')
def agenda():
    # Check if user is loggedin
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'note.png')
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('inter_med_agenda.html',image=full_filename, username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/tele')
def tele():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('tele.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/pconsult')
def redirection():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('pconsult.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#######################################################
    ############""cote docteur
    
@app.route('/ConnexionMedecin/', methods=['GET', 'POST'])
def login2():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home2'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrecte login/motsdepasse!'
    # Show the login form with message (if any)
    return render_template('index2.html', msg=msg)    


@app.route('/ConnexionMedecin/home2')
def home2():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home2.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/ConnexionMedecin/profile2')
def profile2():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile2.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/ConnexionMedecin/inter_med_agenda2')
def agenda2():
    # Check if user is loggedin
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'note.png')
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('inter_med_agenda2.html',image=full_filename, username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/ConnexionMedecin/tele2')
def tele2():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('tele2.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
    
    
    
    
    
@app.route('/ConnexionMedecin/register2', methods=['GET', 'POST'])
def register2():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form and 'specialiste' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone=request.form['phone']
        specialiste=request.form['specialiste']
        
        print(password)
        pw_hash = generate_password_hash(password, 10)
        print('Mots de passe hache de ',password,'est',pw_hash)
        
        ##############################creation json
        
        Utilisateur=request.form['username']
        mdp = request.form['password']
        mail = request.form['email']
        tel=request.form['phone']
        Specialiste=request.form['specialiste']
        
    
    
        data = { 
             "id": 10,   
            	"ressourceType":"Practicor",
            "Username": Utilisateur,
            "password":mdp,
            "mail":mail,
            "phone":tel,
            "specialiste":Specialiste,
            "organization": "/fhir/Organization?_id=10"
            
            }
        with open ("10.json","w") as f_write:
            JSON.dump(data,f_write,indent=1)
       
        
        
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Un compte existe déjà!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Adresse mail invalide ! Veuillez rentrer mail de la forme test@mail.com'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Veuillez remplir le formulaire !'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO doctor VALUES (NULL, %s, %s, %s,%s,%s,%s)', (username, password, email,phone,specialiste,pw_hash))
            mysql.connection.commit()
            msg = 'Vous êtes enrengistrer!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Veuillez remplir le formulaire !'
    # Show registration form with message (if any)
    return render_template('register2.html', msg=msg)

if __name__ == "__main__":
  socketio.run(app)

