from app import db
from datetime import datetime

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
	

class author()