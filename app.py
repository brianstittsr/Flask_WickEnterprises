from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/brianstitt/Documents/GitHub/FlaskProjects/Connecxit/blog.db'

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    posted_by = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text, nullable=False)

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/contact') 
def contact():
    return render_template('contact.html')

@app.route('/heros') 
def heros():
    return render_template('/bootstrap_samples/heros.html')

@app.route('/features') 
def features():
    return render_template('/bootstrap_samples/features.html')

@app.route('/album') 
def album():
    return render_template('/bootstrap_samples/album.html')

@app.route('/product') 
def product():
    return render_template('/bootstrap_samples/product.html')

@app.route('/cover') 
def cover():
    return render_template('/bootstrap_samples/cover.html')

@app.route('/jumbotrons') 
def jumbotrons():
    return render_template('/bootstrap_samples/jumbotron.html')

@app.route('/signin') 
def signin():
    return render_template('/bootstrap_samples/signin.html')


@app.route('/sidebars') 
def sidebars():
    return render_template('/bootstrap_samples/sidebars.html')

@app.route('/dashboard') 
def dashboard():
    return render_template('/bootstrap_samples/dashboard.html')

@app.route('/strapblog') 
def strapblog():
    return render_template('/bootstrap_samples/strap_blog.html')

@app.route('/carousel') 
def carousel():
    return render_template('/bootstrap_samples/carousel.html')

@app.route('/pricing') 
def pricing():
    return render_template('/bootstrap_samples/pricing.html')

@app.route('/thumbtack') 
def thumbtack():
    return render_template('/thumbtack.html')

@app.route('/add') 
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST']) 
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, posted_by="BrianStitt", content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()