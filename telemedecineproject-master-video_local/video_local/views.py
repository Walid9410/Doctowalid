from app import app
from flask import Flask, render_template, url_for, request

# @app.route('/')
# def connexion():
# 	return render_template('pconnec.html')      #Remplacer page connection
#
# @app.route('/page1', methods=['GET','POST'])
# def page1():
#     return render_template("page1.html")        #Remplacer page consultation
#     #print("I'm here")
#
# @app.route('/pconnec')
# def deco():
#     return url_for('connexion')

@app.route('/')
def video():
	return render_template('index.html')

	# result=request.args
    # if request.method =="POST":
    #     user=request.form.get("login",None) #None permet de cache les parametre ds l'URL
    #     return render_template("page1.html") #redirect(url_for("user", a=user))
    # else :
    #     return render_template("pconnec.html")
		# (result['login'])
	# mdp=str(result['pass'])
	# return auth(user, mdp)

#def auth (login, pwd):
    # connection = mysql.connector.connect(host='104.197.145.19',database='sgame',user='root',password='vitrygtr')
    # #cmd = connection.(select Password from Joueur where User=login)
    # cmd = """SELECT Password FROM Joueur WHERE User= %s"""
    # cursor = connection.cursor()
    # cursor.execute(cmd, (login,))
    # passw = cursor.fetchone()
    # print(passw)
    # if (pwd==passw[0]) :
    #     print ('connection / ouverture du plateau')
    #     return render_template('mainpage.html')
    # else :
    #     print ('user or pwd false')
    # connection.commit()
    # cursor.close()
    # connection.close()
    #return render_template('mainpage.html',a=login)
