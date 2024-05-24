from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from .bot import get_bot_posts

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.String(500))
    datecreated = db.Column(db.DateTime, defualt=datetime.now(datetime.UTC))
    
with app.app_context():
    db.create_all()
    contents = get_bot_posts()
    try:
        for content in contents:
            post_obj = Post(title=content.topic, content=content.post)
            db.session.add(post_obj)
            db.session.commit()
    except:
        pass
    
@app.route('/', methods=['GET','POST'])
def index():
    post = Post.query.get_or_404(1)
    data = {
        "title": post.title,
        "content":post.content
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)