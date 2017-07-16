#Check : test add & commit database

from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

#@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
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
            return '<h1> Incorrect username or password </h1>'
            #flash ('User password incorrect, or user does not exist')
            #TODO specify each error message
            
    return render_template('login.html', page_title="Log In!")

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        verifypassword = request.form['verifypassword']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

        #TODO: flash or render each case's error message. invalid email, password, verifypassword.
        else:
            return "<h1>Duplicate user</h1>" 

    return render_template('signup.html', page_title="SIGN UP!")



@app.route('/blog')
def blog():
     

    if not request.args:
        
        title = request.args.get("title")
        body = request.args.get("body")
        
        
        owner = User.query.filter_by(username=username).first()

        new_posting = Blog(title,body,owner)
        
        current_owner = User.query.filter_by(id=new_posting.owner_id).first()
        
        postings = Blog.query.all()


        # TODO: need to get username from User class that matches Blog's owner_id

        return render_template('blog.html',page_title="All Postings",new_posting=new_posting, postings=postings, current_owner=current_owner)
  
    else:
        posting_id = request.args.get('id') 
        current_page = Blog.query.filter_by(id=posting_id).first()
        return render_template('singleuser.html',current_page=current_page)
    

    return render_template('singleuser.html',current_page=current_page,new_posting=new_posting, postings=postings)
    


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

        else:
           #flash ('Please POST!')
            return '<h1> Please POST! </h1>'
                    
    return render_template('/newpost.html',page_title="Add a blog Entry")




@app.route('/')
def index():
    #getting all user and displays as ul

    all_user = User.query.all()

    return render_template('index.html', page_title="All users", all_user=all_user )

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

   




if __name__ == '__main__':
    app.run()
