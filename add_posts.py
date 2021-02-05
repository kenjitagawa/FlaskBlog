from pyblog import db
from pyblog.models import User, Post
from flask_login import current_user


def new_post(n):
    user = User.query.filter_by(email='admin@kenji.com').first()
    for i in range(n):
        post = Post(title = f"Post {i}", content=f'This is a test post. It will post on the range of {n}. This is post numer: {i}', author=user)
        db.session.add(post)
        db.session.commit()
        print('Success!')

def delete_post():
    posts = Post().query.all()
    for post in posts:
        delt = Post.query.get(post.id)
        db.session.delete(delt)
        db.session.commit()
        print(f"Deleted post {delt.title}")

if __name__ == '__main__':
    pass
