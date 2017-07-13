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

    def __init__(self, title, body):
   
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    
    title = ""
    body = ""
    new_posting = ""
    postings = ""


    title = request.form.get("title")
    body = request.form.get("body")
    #blog_id = request.form.get("blog-id")


    new_posting = Blog(title, body)
    postings = Blog.query.all()
    #blog_link = Blog.query.get(blog_id)
  
    #blog_id = int(request.form.get('blog-id'))
    #blog_query_id = Blog.query.get(blog_id)


    return render_template('blog.html',page_title="Build a Blog", title=title, body=body, new_posting=new_posting, postings=postings)
  

@app.route('/newpost', methods=['POST','GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

    
        if title and body:
            new_posting = Blog(title, body)
            db.session.add(new_posting)
            db.session.commit()
            return render_template('/posting_page.html',page_title=title, posting_body=body)
        
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

    if id == 
    current_posting = Blog.query.get(posting_id)
    return render_template('/blog.html', page_title=title, page_body=body)

    #return render_template('/posting_page.html', page_title=title,posting_body=body )




@app.route('/')
def index():
    return redirect('/blog')




if __name__ == '__main__':
    app.run()
