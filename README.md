# GitHub Actions CI Template for Selenium+Flask MVC

[![](https://github.com/CISC-CMPE-327/CI-Python/workflows/Python%20application/badge.svg)](https://github.com/CISC-CMPE-327/CI-Python/actions)

## Instructions: 

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


## How does it work?

Folder structure:
```
.
├── LICENSE
├── README.md
├── .github
│   └── workflows
│       └── pythonapp.yml ======> CI workflow for python (trigger test for commits/pull-requests)
│
├── qa327
│   ├── __init__.py.  ==========> we define our flask app instance here
│   ├── __main__.py   ==========> trigger by 'python -m qa327'
│   ├── backend.py    ==========> defines backend logic
│   ├── frontend.py   ==========> defines frontend logic
│   ├── models.py.    ==========> defines all the data models
│   └── templates
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       └── register.html
├── qa327_test
│   ├── __init__.py
│   ├── backend
│   ├── conftest.py
│   ├── frontend
│   │   ├── test_connection.py
│   │   └── test_registraion.py
│   └── integration
│       └── test_registration.py
└── requirements.txt  ====================> python dependencies, a MUST
```

qa327 is the module that contains the application, and qa327_test is the module that contains the testing code for qa327

![image](https://user-images.githubusercontent.com/8474647/94135588-ad25a700-fe31-11ea-8839-59699a9608db.png)

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
    
    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()
    return None


```

It takes user email, name (for dispaly purpsoe), user entered password, and user re-entered password. Before we storing the user data, we need to stored a hashed version of the password, rather than the original one. The reason is that, if your database gets hacked, all the plaintext passwords will be available to the hacker. Hashing is a one way function. It means that same passwords will yield the same hash. But with hash value only, the attacker cannot generate the original password. In this way, even if the database is leaked, the clients credentials are still safe. Then we create a user using the data model (will talk about this below), and save it to the databae. 


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

The testing will contain three parts (frontend testing, backend testing and integration testing). For now we include the examples for frontend testing and integration testing. Backend testing (unit testing in our case) is straightforward (will be covered in the lecture), so we didn't include them for now.

Let's take a look at the file structure:

````
├── qa327_test
│   ├── __init__.py
│   ├── conftest.py  ===================> defines fixture (run the web server)
│   ├── frontend                ========> testing the front-end (without backend, using mocking)
│   │   ├── test_connection.py  ========> testing if we can connect
│   │   └── test_registraion.py ========> testing the login page and home page (without backend, using mocking)
│   └── integration             ========> integration testing (running both frontend and the backend)
│       └── test_registration.py =======> testing the registration process (actually storing/reading data from database)
````

conftest.py defines the fixtures for the test cases. These fixtures are resources that are needed to setup and shared between different test cases. In order to test the services and the web interface, we need to run the web server first. If we take a look at what is inside conftest.py (you are not supposed to understand every single line of this part):

```python
class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', FLASK_PORT, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


@pytest.fixture(scope="module", autouse=True)
def server():
    on_win = os.name == 'nt'
    with tempfile.TemporaryDirectory() as tmp_folder:
        # create a live server for testing
        # with a temporary file as database
        db = os.path.join(tmp_folder, 'db.sqlite')
        server = ServerThread()
        server.start()
        time.sleep(5)
        yield
        server.shutdown()
        time.sleep(2)
```

We create a new thread that run the web service. There is a yield statement, where this function will return to run the actual test cases. Once all the test cases are finished, we return back to the yield statement, and continue executing the rest of the code to terminate the thread. Again, for this course, you don't need to change this for your course project.

Next, let's take a look at **integration testing** first, the `test_registration.py` file under `integration_test` folder:

```
│   └── integration             ========> integration testing (running both frontend and the backend)
│       └── test_registration.py =======> testing the registration process (actually storing/reading data from database)
````

```python

@pytest.mark.usefixtures('server')
class Registered(BaseCase):

    def register(self):
        """register new user"""
        self.open(base_url + '/register')
        self.type("#email", "test0")
        self.type("#name", "test0")
        self.type("#password", "test0")
        self.type("#password2", "test0")
        self.click('input[type="submit"]')

    def login(self):
        """ Login to Swag Labs and verify that login was successful. """
        self.open(base_url + '/login')
        self.type("#email", "test0")
        self.type("#password", "test0")
        self.click('input[type="submit"]')

    def test_register_login(self):
        """ This test checks the implemented login/logout feature """
        self.register()
        self.login()
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test0", "#welcome-header")

```
This one uses SeleniumBase API to control chrome browser. First we defined a class inherited from the BaseCase class, with the @pytest.mark.usefixtures('server') decoration (yes we need a live server running for this test case). Then all the test_xxx functions will be executed as a test case under this class. For this one, we have a test_register_login function. It means that we are going to test the registeration function. It first calls a register function, where the test case automatically fills in emails, passwords, and names into corresponding HTML elements using CSS selector. In this case, just using an ID selector. For #email it will look for element that has an attribute id="email". self.type means typing into. Then, the test case clicks the submit button. After registeration, it tries to login using the same credential, and verifies if the weclome header is correctly displayed.

This test case runs both the frontend and the backend at the same time, as you can tell from the qa327 folder, the registration backend has been implemented. This is what we suppose to do in the **last assignment**. But before that, we will be only **testing the frontend and backend separately**.

Lets take a look at the frontend testing code, where we are supposed to run the frontend **without the backend**. How can we do it? We use a method called mocking. Lets take a look at the file `test_registraion.py` under the `qa327_test/frontend` folder:

```
│   ├── frontend                ========> testing the front-end (without backend, using mocking)
│   │   └── test_registraion.py ========> testing the login page and home page (without backend, using mocking)
```

```python
# Moch a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]

```
First, this file define a user object and a list of tickets object. Since we don't run the actual backend, we need to create faked object to test the frontend. This process is called mocking. So we need to patch the backend to have its certain functions returning the mocked object. After creating the faked objects, we can start our test cases: (in the same file `test_registration.py` for frontend)

```python

class FrontEndHomePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "test_frontend")
        # click enter button
        self.click('input[type="submit"]')
        
        # after clicking on the browser (the line above)
        # the front-end code is activated 
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value. However, here we only want to test the
        # front-end, without running the backend logics. 
        # so we patch the backend to return a specific user instance, 
        # rather than running that program. (see @ annotations above)
        
        
        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_failed(self, *_):
        """ Login and verify if the tickets are correctly listed."""
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "wrong_password")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("login failed", "#message")

```
This is very similar to the above selenium example for integration testing, except that we put annotation on the testing functions. 
These annotation will patch the program in the scope of current test case. 
The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

```python
@patch('qa327.backend.get_user', return_value=test_user)
```

Will patch the backend `get_user` function (within the scope of the current test case)
so that it return `test_user` instance below rather than actually reading the user data from the database. 
