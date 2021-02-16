from flask import Flask, render_template
from content import contents


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', contents=contents)


if __name__ == '__main__':
    app.run()