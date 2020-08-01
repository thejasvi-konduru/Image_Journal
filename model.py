import sqlite3 as sql
import hashlib
import requests

def create():
	con = sql.connect("database.db")
	con.execute("CREATE TABLE IF NOT EXISTS userlist(userid INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL,password_h TEXT NOT NULL,emailid TEXT NOT NULL)")
	con.execute("CREATE TABLE IF NOT EXISTS posts(post_id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL,posted_by_id INT NOT NULL,likes INT,filename NOT NULL)")
	con.execute("CREATE TABLE IF NOT EXISTS comments(ID INTEGER PRIMARY KEY AUTOINCREMENT,post_id INT NOT NULL,username TEXT NOT NULL,value TEXT NOT NULL)")
	con.commit()
	con.close()

def addUser(request):
	emailid = request.form['EMAIL']
	username = request.form['USERNAME']
	password = request.form['PASSWORD']
	check_password = request.form['RETYPEPASSWORD']
	emailid = request.form['EMAIL']
	if password!=check_password:
		return None
	con = sql.connect("database.db")
	cur = con.cursor()
	sqlQuery="SELECT username from userlist where username='"+ username + "';"
	cur.execute(sqlQuery)
	row = cur.fetchone()
	if row:
		return None
	else:
		password = hashlib.md5(password.encode()).hexdigest()
		cur.execute("INSERT INTO userlist(username,password_h,emailid) VALUES (?,?,?)",(username,password,emailid,))
		name = username + "friends"
		con.execute("CREATE TABLE IF NOT EXISTS "+ name +"(id INTEGER PRIMARY KEY AUTOINCREMENT,friend_userid INTEGER NOT NULL,friend_username TEXT NOT NULL)")
		con.commit()
		cur.close()
		con.close()
	return name

def checkuser(request):
	try:
		username = request.form['USERNAME']
		password = request.form['PASSWORD']
		con = sql.connect("database.db")
		cur = con.cursor()
		sqlQuery="SELECT password_h from userlist where username='"+ username + "';"
		cur.execute(sqlQuery)
		ch_password =  hashlib.md5(password.encode()).hexdigest()
		userpass=cur.fetchone()
		if ch_password != userpass[0]:
			return None
		else:
			return username
	except:
		return None
