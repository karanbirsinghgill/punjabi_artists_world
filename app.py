from flask import Flask, render_template, url_for,request, redirect
from form import blog_post
from flask_sqlalchemy import SQLAlchemy
#from model import *
from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Manager
from datetime import datetime
from flask_bootstrap import Bootstrap 
import pdb


app = Flask(__name__)

app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://karan:gill@localhost:3306/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('runserver', Server(

	use_debugger = True,
	use_reloader = True,
	host = '0.0.0.0',
	port = 5000
	))

manager.add_command("dbase", MigrateCommand)

class blog_model(db.Model):
	post_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False)
	post = db.Column(db.Text, nullable=False)
	author = db.Column(db.String(15))
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __init__ (self, title, post, author):

		self.title = title
		self.post = post 
		self.author = author

	def __repr__(self):

		return 'blog_model ' +str(self.post_id)

@app.route('/')
@app.route('/home')
def home():

	return render_template('index.html')



@app.route('/posts')
def view_posts():

	#view_posts = blog_model.query.order_by(blog_model.date_created.desc()).all()
	view_posts = blog_model.query.all()
	print('Posts = {}'.format(view_posts))
	return render_template('view.html', blogs = view_posts)

@app.route('/posts/new', methods =['GET', 'POST'])
def add_post():

	form = blog_post()

	if request.method == 'POST':

		title = form.title.data 
		post = form.post.data 
		author = form.author.data 

		blog = blog_model(title, post, author)
		db.session.add(blog)
		db.session.commit()

		return redirect (url_for('view_posts'))
	

	return render_template('add.html', form = form)


@app.route('/delete/<int:post_id>')

def delete_post(post_id):

	post = blog_model.query.get_or_404(post_id)
	
	db.session.delete(post)
	db.session.commit()

	return redirect (url_for('view_posts'))


@app.route('/edit/<int:post_id>', methods=['POST','GET'])
def edit_post(post_id):
	
	blog = blog_model.query.get_or_404(post_id)
	form = blog_post(obj = blog)
	if request.method == 'POST':

		blog.title = form.title.data 
		blog.post = form.post.data 
		blog.author = form.author.data 
		db.session.commit()
		return redirect(url_for('view_posts'))

	return render_template('edit.html', form = form, blog = blog)

# @app.route('/register', methods=['POST','GET'])

# def registration():
# 	form = registration_form()
# 	if request.method == 'POST':
# 		email = form.email.data
# 		password = form.password.data
# 		name = form.name.data
# 		DOB = form.DOB.data
# 		address = form.address.data
# 		new_author = author(email,password,name,DOB,address)
# 		db.session.add(new_author)
# 		db.session.commit()
# 		return redirect(url_for('login'))
# 	else:

# 		return render_template('registration.html', form = form)

		 

if __name__ == '__main__':
	
	manager.run()
