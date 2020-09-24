# CI-Python

[![](https://github.com/CISC-CMPE-327/CI-Python/workflows/Python%20application/badge.svg)](https://github.com/CISC-CMPE-327/CI-Python/actions)

### GitHub Actions CI Template for Selenium+Flask MVC


Folder structure:
```
.
│   .gitignore
│   LICENSE
│   README.md
│   requirements.txt ========> python dependencies, a MUST
│
├───.github
│   └───workflows
│           pythonapp.yml =======> CI workflow for python
│
├───qa327
│   │   app.py ===============> where we actually store the main function
│   │   __init__.py
│   └───__main__.py ==========> trigger by 'python -m qa327'
│   └───frontend.py ==========> defines frontend logic
│   └───backend.py  ==========> defines backend logic
│   └───models.py   ==========> defines all the models
│ 
│ 
└───qa327_test
    │   test_main_approach1.py
    │   test_main_approach2.py
    │   __init__.py
    │   
    └───r2
            terminal_input.txt
            terminal_output_tail.txt
            transaction_summary_file.txt
            valid_account_list_file.txt
```

First, clone this repo:
```
git clone https://github.com/CISC-CMPE-327/CI-Python
cd CI-Python 
```

To run the application (make sure you have a python environment of 3.5+)

```
$ pip install -r requirements.txt
$ python -m qa327
```

You can register, login, logout from the web application. Data will be saved to a `db.sqlite` file under your working directory.

To run all the test code:

```
$ pytest
```
You will see your browswer being controlled by the script automatically jumping around to test the website.


### Frontend

In order to understand every single bit of this template, first please try running it, registering a user, logging in, and logging out to develop a general sense of what is going on. 

Next, try to read the python code from the entry point, starting from `qa327.__main__` file. It imports a pre-configured flask application instance from `qa327.__init__.py`. In the init file, `SECRET_KEY` is used to encrypt the session data stored in the client's browser, so one cannot just tell by intercepting your traffice. Usually this shouldn't be hardcoded and read from environment variable during deployment. For the seak of convinience, we hard-code the secret key here as a demo.

When the user type the link `localhost:8081` in the browser, the browser will send a request to the server. The client can type different routes such as `localhost:8081\login` or `localhost:8081\register` with different request methods such as `GET` or `POST`. These different routes will be handled by different python code fragments. And those code fragments are all defined in the `qa327.frontend.py` file. For example:

```python
@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')
```

The first line here defines that if a client request `localhost:8081\register` with the 'GET' method, this fragment of code should handle that request and return the corresponding HTML code to be rendered at the client side. For example, if the user type `localhost:8081\register` on his/her browswer and hit enter, then the browser will send a GET request. The above fragment of code recieve the request, and the last line looks up for a HTMP template named `register.html` in the `qa327.templates` folder.
```html
{% extends 'base.html' %}

{% block header %}
<h1>{% block title %}Register{% endblock %}</h1>
{% endblock %}

{% block content %}
<h4>{{message}}</h4>
<form method="post">
  <div class="form-group">
    <label for="email">Email</label>
    <input class="form-control" name="email" id="email" required>
    <label for="name">Name</label>
    <input class="form-control" name="name" id="name" required>
    <label for="password">Password</label>
    <input class="form-control" type="password" name="password" id="password" required>
    <label for="password">Confirm Password</label>
    <input class="form-control" type="password" name="password2" id="password2" required>
    <input class="btn btn-primary" type="submit" value="Register">
  <a href='/login' class="btn btn-primary" id="btn-submit" >Login</a>
  </div>
</form>
{% endblock %}
```

Let's break this down. This is the [Jinja Templating format (full synatx documentation here)]{https://jinja.palletsprojects.com/en/2.11.x/templates/}. In contrast to React, Vue or other frameworks, it is a server-side rendering framework. It means that the job of filling the template with the required information is done on the server, and the final html will be sent to the client's browswer. Client side rendering is also becoming very popular, but it is very important to understand how different things work. 

The firstline calls a base template, if you open it, you will find a large chunk of html code. That is the base template for all webpages so we can share common HTML/CSS/JS code for all templates. In line ~127 of the base.html template, you can find something like:

```html
    <div class="col-lg-8">
        {% block content %}{% endblock %}
    </div>
```

It defines a block named `content`. This block can be replaced by any block definitions in other templates that use the base template. So in this example, `register.html` defines a block also named `content`, this block will replace the `content` block in the base template. So everything in the content block of `register.html` will be inserted into `base.html`. 

On `register.html` there is also a line: 

```html
<h4>{{message}}</h4>
```
This will be replaced by the same named parameter, in this case `message`, in the params of `render_template` function call. If we go back `frontend.py` python code ealier, we see:

```python
@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')
```

Here the message param is an empty string. So when rendering the template, `{{message}}` will be replaced by an empty string. 
Then completed the whole registration page will be returned to the browser. That will be the page you saw on the register URL.

Once the client got to the register page, he/she can submit the form with input information. The form by default, after the user clicked the submit button, will be `POST`ed to the same URL, so in this case, 'localhost:8081/register'. Now the server recieves the browswer's request, and need to find the corresponding code fragment to handle the request of route `/register` and method `POST`. It looks up the defined routes, and we have the following match in `frontend.py`:

```python
@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = bn.register_user(email, name, password, password2)
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')
```

So this fragment of code will read the data from the form, as you can tell from the first 4 lines of function `register_post`. Then, it calls a backend function to register the user. If there is any error, the backend will return an error message, describing what is the problem. If there is any error message, we will return the original `register.html` template to the client with the error message replaced the `{{message}}` snippet in the template.



### Backend

The backend portion controls the business logics, such as all associated actions to be done to finsih a transaction, and the interaction of data models. All the backend codes are included in the backend.py file. You can make it a module if there are too many logics involved in the single file, but for simplicity of this demo, we use a single file. Following the above registration example, if we take a look at what is inside the `register_user` function:

```python

def register_user(email, name, password, password2):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: an error message if there is any, or None if register succeeds
    """
    user = User.query.filter_by(email=email).first()

    if user:
        return "User existed"

    if password != password2:
        return "The passwords do not match"

    if len(email) < 1:
        return "Email format error"

    if len(password) < 1:
        return "Password not strong enough"

    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()
    return None


```

It takes user email, name (for dispaly purpsoe), user entered password, and user re-entered password. Frist, as a typical registration process, we need to check if anyone else has already used this email address before. So we use the User model, which we will explain later on, to find a user with the same email address. If we find a user, it means the email is already associated with a user, else, it means the email is available. 

So if user exists, we return "user existed" message. Then there are couple input checks that are very much self-explinatory. Before we storing the user data, we need to stored a hashed version of the password, rather than the original one. The reason is that, if your database gets hacked, all the plaintext passwords will be available to the hacker. Hashing is a one way function. It means that same passwords will yield the same hash. But with hash value only, the attacker cannot generate the original password. In this way, even if the database is leaked, the clients credentials are still safe. Then we create a user, and save it to the databae. 


### Models

When using a relational database, typically we interact with it using SQL language, which is not quite user friendly. Therefore we use another approach to avoid writing SQL language by defining objects that can be directly mapped into the database. In this example we use sqlite, which is simple file based database. By changing the application configuration in `__init__.py`, you can hood it up to other databases such as MySQL database. All these models we defined are in a single file `qa327.models.py`. Let's take a look at the user model:

```python
class User(db.Model):
    """
    A user model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
```

Just like any other python tasks, we define several attributes, as well as how they should be mapped into a column of the database. Here we also define the maximumn lenght of each individual field. 

To create a user:
```python
new_user = User(email=email, name=name, password=hashed_pw)
db.session.add(new_user)
db.session.commit()
```

To query a user:
```python
user = User.query.filter_by(email=email).first()
users = User.query.filter_by(name='steven')
```

To update a user:
```python
admin = User.query.filter_by(email=email).first()
admin.name = 'I changed my name'
db.session.commit()
```

To delete a user:
```python
User.query.filter_by(email=email).delete()
```

You can create any other classes following this example. 



### PyTest


TBA
