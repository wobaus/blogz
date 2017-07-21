#Check : test add & commit database

from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'somekindofsecretkey'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
             


    def __init__(self, title, body, owner):
   
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.username


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

        
@app.route('/login', methods = ['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            flash ('User password incorrect, or user does not exist')
            return render_template('login.html', page_title="Log In!")
    
    return render_template('login.html', page_title="Log In!")

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        verifypassword = request.form['verifypassword']
        

        # TODO - style validation error 

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            if len(username) < 3 or len(username) > 20 or " " in username:
                flash('This is not a valid username.','error_user')

            if len(password) < 3 or len(password) > 20 or " " in password:
                flash('Password is not valid.')
            
            if password != verifypassword:
                flash('Password dont match')
            
                return render_template('signup.html', page_title="SIGN UP!")

        
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')


    return render_template('signup.html', page_title="SIGN UP!")



@app.route('/blog')
def blog():
    
    posting_id = request.args.get('id')
    author = request.args.get('username')
    
    # TODO: display and create link for posting username
    if posting_id: #grab posting id to display individual post
        current_page = Blog.query.get(posting_id)
        #current_user = User.query.filter_by(id=current_page.owner_id).first()
        #current_user = User.query.get(current_page.owner_id)
        #page_author = (User.query.filter_by(id=current_page.owner_id)).username
        #get User class info of what current_page owner_id = User id

        return render_template('singleuser.html',current_page=current_page, author=author)

   
    # if author: #get username to display all posts from this user
    #     user = User.query.filter_by(username=author).first() #get selected user 
        
    #     current_owner_post = Blog.query.filter_by(owner_id=user.id).all() #try to get all data that matches owner_id in Blog class and id in user
    #     return render_template('blog.html', user=user)

    else:


        postings = Blog.query.all()

        return render_template('blog.html',page_title="All Postings",postings=postings)

    


@app.route('/newpost', methods=['POST','GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title and body:
            
            auther = User.query.filter_by(username=session['username']).first()
            
            new_posting = Blog(title, body, auther)
            db.session.add(new_posting)
            db.session.commit()
            
            postings = Blog.query.all()
            
            return render_template('/singleuser.html', current_page=new_posting)

        else: #TODO: style flash message
            flash ('Please POST!')
            return render_template('/newpost.html',page_title="Add a blog Entry")
                    
    return render_template('/newpost.html',page_title="Add a blog Entry")




@app.route('/')
def index():


    all_user = User.query.all()

    return render_template('index.html', page_title="All users", all_user=all_user )

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

   




if __name__ == '__main__':
    app.run()
