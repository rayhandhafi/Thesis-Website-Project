from flask import Flask
from markupsafe import escape
from flask import url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)