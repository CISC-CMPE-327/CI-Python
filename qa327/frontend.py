from flask import render_template, Blueprint


frontend = Blueprint('frontend', __name__)


@frontend.route('/login')
def hello_word():
    return render_template('login.html')


@frontend.route('/')
def profile():
    return render_template('profile.html')


@frontend.route('/register')
def register():
    return render_template('register.html')
