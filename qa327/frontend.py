from flask import Flask, render_template
import os

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

templates = os.path.join(
    package_dir, "templates"
)

app = Flask('this is a simple web application', template_folder=templates)


@app.route('/')
def hello_word():
    return render_template('login.html')
