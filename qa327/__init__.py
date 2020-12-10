from flask import Flask
import os

"""
This file defines global variables and config values
"""


package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

templates = os.path.join(
    package_dir, "templates"
)

app = Flask('this is a simple web application', template_folder=templates)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '69cae04b04756f65eabcd2c5a11c8c24'
# if the user supplies a database file name, we use
# that instead, and it should an absolute path
# for windows user, C:\ is the root directory, so it
# should not be included. e.g. Users/xxx/Document/db.sqlite
db_name = os.getenv('DB_NAME')
db_string = os.getenv('db_string')
if db_name:
    database_url = "sqlite:////" + db_name
elif db_string:
    database_url = db_string
else:
    # default:
    # db.sqlite at the working directory
    database_url = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
