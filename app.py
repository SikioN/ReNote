from flask import Flask, render_template
from content import contents

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', contents=contents)


@app.route('/checkout')
def checkout():
    return render_template('content.html')


@app.route('/pers_acc')
def pers_acc():
    return render_template('personal_account.html')


@app.route('/notification')
def pers_acc_notifications():
    return render_template('pers_acc_notifications.html')


if __name__ == '__main__':
    app.run()
