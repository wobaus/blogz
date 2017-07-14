from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    #created_date = db.Column(db.DateTime) 
                 

    def __init__(self, title, body):
   
        self.title = title
        self.body = body

@app.route('/blog')
def blog():

    if not request.args:

        title = request.form.get("title")
        body = request.form.get("body")

        new_posting = Blog(title, body)
        postings = Blog.query.all()
        #time = Blog.query.get(created_date)

        return render_template('blog.html',page_title="Build a Blog", title=title, body=body, new_posting=new_posting, postings=postings)
  
    else: 
        posting_id = request.args.get('id') 
        current_page = Blog.query.filter_by(id=posting_id).first()
        return render_template('posting_page.html',current_page=current_page)

 
  


@app.route('/newpost', methods=['POST','GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

    
        if title and body:
            new_posting = Blog(title, body)
            db.session.add(new_posting)
            db.session.commit()

            return render_template('posting_page.html', current_page=new_posting)

        if not title:
                flash ('Please type title','error')
        if not body:
                flash ('Please type blog','body_error')
                    
    return render_template('/newpost.html',page_title="Add a blog Entry")




@app.route('/posting_page')
def posting_page():
    title = request.form.get("title")
    body = request.form.get("body")
    blog_id = request.form.get("id")


    current_posting = Blog.query.get(posting_id)
    return render_template('/blog.html', page_title=title, page_body=body)

    #return render_template('/posting_page.html', page_title=title,posting_body=body )




@app.route('/')
def index():
    return redirect(url_for('blog'))




if __name__ == '__main__':
    app.run()
