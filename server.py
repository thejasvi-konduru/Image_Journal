from flask import Flask, render_template,redirect,url_for,request
import model
import sqlite3 as sql
import hashlib

app = Flask(__name__)
model.create()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/signup')
def doit():
	return render_template('signup.html')

@app.route('/go')
def go():
	return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
	user = request.form['USERNAME']
	fposts=[]
	if model.checkuser(request) is not None :
		con = sql.connect("database.db")
		cur = con.cursor()
		query="select userid from userlist where username = '" + user + "';"
		cur.execute(query)
		idofuser=cur.fetchall()
		query="select friend_username from " + user +"friends;"
		cur.execute(query)
		p=cur.fetchall()
		cur.execute("select * from posts")
		l=cur.fetchall()
		a=""
		if l is not None:
			for i in l:
				a="("+str(i[2])+",)"
				for k in p:
					c=1
					if str(k) == a:
						fposts+=[dict(postid=i[0],likes=i[3],url=i[4],postedby=i[1],posted_by_id=i[2],follow=True)]
					if str(k) != a and c==1:
						c=0
						fposts+=[dict(postid=i[0],likes=i[3],url=i[4],postedby=i[1],posted_by_id=i[2],follow=False)]
				if p == []:
					fposts+=[dict(postid=i[0],likes=i[3],url=i[4],postedby=i[1],posted_by_id=i[2],follow=False)]
		con.commit()
		cur.close()
		con.close()			
		return render_template('friend.html',posts=fposts,username=user,userid=idofuser)
	else:
		return render_template('login.html')


@app.route('/register', methods=['POST'])
def signup():
	if model.addUser(request) is not None:
		return render_template('login.html')
	else:
		return render_template('signup.html')


@app.route('/logout',methods=['POST'])
def logout():
	return render_template('home.html')

@app.route('/index',methods=['POST'])
def do():
	user=request.form['username']
	posts=[]
	con = sql.connect("database.db")
	cur = con.cursor()
	query="select userid from userlist where username='"+user+"';"
	cur.execute(query)
	idofuser=cur.fetchone()
	query="select * from posts where username ='"+ user+"';"
	cur.execute(query)
	h=cur.fetchall()
	if h is not None:
		for k in h:
			cur.execute("select * from comments where post_id = "+str(k[0]))
			gh=cur.fetchall()
			i=[]
			if gh != []:
				posts+=[dict(postid=k[0],likes=k[3],url=i[2],whocommented=i[2],comment=i[2]+":"+i[3]) for i in gh]
			else:
				posts+=[dict(postid=k[0],likes=k[3],url=k[4],whocommented=None,comment=None)]
	return render_template('user.html',posts=posts,username=user,userid=idofuser[0])

@app.route('/clicklike',methods=['POST'])
def like():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("UPDATE posts SET likes='"+request.form['likes']+"'WHERE post_id = "+str(request.form['postid'])+";")
	con.commit()
	cur.close()
	con.close()
	return mustdo(request)

@app.route('/comment',methods=['POST'])
def comment():
	con = sql.connect("database.db")
	cur = con.cursor()
	con.execute("INSERT INTO comments(post_id,username,value) VALUES(?,?,?)",(request.form['postid'],request.form['username'],request.form['comment']))
	con.commit()
	cur.close()
	con.close()
	return mustdo(request)

def mustdo(request):
	con = sql.connect("database.db")
	cur = con.cursor()
	user = request.form['username']
	fposts=[]
	p=[]
	con = sql.connect("database.db")
	cur = con.cursor()
	query="select userid from userlist where username = '" + user + "';"
	cur.execute(query)
	idofuseri=cur.fetchone()
	query="select friend_userid from " + user +"friends;"
	cur.execute(query)
	p=cur.fetchall()
	cur.execute("select * from posts")
	l=cur.fetchall()
	a=""
	if l is not None:
		for i in l:
			a="("+str(i[2])+",)"
			for k in p:
				c=1
				if str(k) == a:
					fposts+=[dict(postid=i[0],likes=i[3],url=i[4],postedby=i[1],posted_by_id=i[2],follow=True)]
				if str(k) != a and c==1:
					c=0
					fposts+=[dict(postid=i[0],likes=i[3],url=i[4],postedby=i[1],posted_by_id=i[2],follow=False)]
		if p== []:
			fposts+=[dict(postid=i[0],likes=i[3],url=i[4],postedby=i[1],posted_by_id=i[2],follow=False)]
	con.commit()
	cur.close()
	con.close()
	return render_template('friend.html',posts=fposts,username=user,userid=idofuseri)

@app.route('/follow',methods=['POST'])
def follow():
	user=request.form['username']
	con = sql.connect("database.db")
	cur=con.cursor()
	query="select userid from userlist where username = '"+request.form['friendname']+"';"
	cur.execute(query)
	friendid=cur.fetchone()
	cur.execute("INSERT INTO " + user+"friends(friend_userid,friend_username) VALUES(?,?)",(friendid[0],request.form['friendname'],))
	con.commit()
	cur.close()
	con.close()
	return mustdo(request)

@app.route('/unfollow',methods=['POST'])
def unfollow():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("DELETE FROM "+request.form['username']+"friends WHERE friend_username='"+request.form['friendname']+"';")
	con.commit()
	cur.close()
	con.close()
	return mustdo(request)

@app.route('/addpost',methods=['POST'])
def add():
	con = sql.connect("database.db")
	cur = con.cursor()
	query="select userid from userlist where username='"+request.form['username']+"';"
	cur.execute(query)
	userid=cur.fetchone()
	cur.execute("INSERT INTO posts(username,posted_by_id,likes,filename) VALUES(?,?,?,?)",(request.form['username'],userid[0],0,request.form['url']))
	con.commit()
	cur.close()
	con.close()
	return mustdo(request)


if __name__ == '__main__':
	app.run(debug=True)
