from flask import request, redirect, url_for, Blueprint
from qa327.models.User import User
from qa327 import db
from werkzeug.security import generate_password_hash, check_password_hash

backend = Blueprint('backend', __name__)


@backend.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(username=username).first()

    # if a user is found, we want to redirect back to signup page so user can try again
    if user and check_password_hash(user.password, password):
        return redirect(url_for('frontend.profile'))

    return redirect(url_for('frontend.hello_word'))


@backend.route('/register', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(username=username).first()

    # if a user is found, we want to redirect back to signup page so user can try again
    if user:
        return redirect(url_for('frontend.register'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    hashed_pw = generate_password_hash(password, method='sha256')
    new_user = User(username=username, name=name, password=hashed_pw)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('frontend.profile'))
