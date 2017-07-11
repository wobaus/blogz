from flask import Flask, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'somekindofsecretkey'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    title = ""
    body = ""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        new_posting = Blog(title, body)
        db.session.add(new_posting)
        db.session.commit()

    new_postings = Blog.query.all()
    return render_template('blog.html',page_title="Build a Blog", title=title, body=body )




@app.route('/newpost', methods=['POST','GET'])
def newpost():
    title = ""
    body = ""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        if title and body:
            new_posting = Blog(title, body)
            db.session.add(new_posting)
            db.session.commit()
            return redirect('/blog')
        
        else:
            flash('please fill contents','error')
    
    
    return render_template('newpost.html', page_title="Add a Blog Entry")

if __name__ == '__main__':
    app.run()
