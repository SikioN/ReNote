import datetime
from threading import Thread
from time import sleep

from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_mail import Mail, Message
from flask_migrate import Migrate

from forms import TextArea, SignUpForm, LoginForm, NotificationForm, ResetPasswordRequestForm, ResetPasswordForm
from models import db, Summary, User, Notification

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?check_same_thread=False'
app.config['SECRET_KEY'] = 'NeverGonnaGiveYouUP'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'maxshlyahtin@gmail.com'
app.config['MAIL_PASSWORD'] = 'Pp485221'
app.config['MAIL_PORT'] = 587
app.config['ADMINS'] = 'mrekkhub@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'mrekkhub@gmail.com'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/main')
def main():
    summary = Summary.query.filter_by(user=current_user).all()
    return render_template('main.html', summary=summary)


# @app.route('/notification')
# @login_required
# def notification():
#     user = current_user.last_notification_read_time = datetime.utcnow()

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = ResetPasswordRequestForm()
    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset.html',
                           title='Reset Password', form=form)


@app.route('/n')
def new_pers_acc():
    return render_template('pers_acc_new.html')


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[ReNote] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               html_body=render_template('msg_to_user.html',
                                         user=user, token=token))


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('checkout'))
    form = ResetPasswordForm()
    if form.is_submitted():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('new_pass.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is None or user.check_password(password) is False:
            abort(400)
        login_user(user)
        return redirect(url_for("main"))
    return render_template("en/base_dark.html", form=form)


# @app.route('/', methods=["GET", "POST"])
# @login_required
# def activate_notification():


@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    form = SignUpForm()
    if form.is_submitted():
        nickname = form.nickname.data
        email = form.email.data
        password = form.password.data
        country = form.country.data
        existing_user = User.query.filter(User.nickname.like(nickname) | User.email.like(email)).first()
        if existing_user is not None:
            abort(400)
        user = User(nickname=nickname, email=email, country=country)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('new_summary'))
    return render_template('en/checkout_dark.html', form=form)
#
#
# @app.route('/summary/<int:summary_id>', methods=["GET", "POST"])
# def get_summary(summary_id):
#     summary = Summary.query.filter_by(id=summary_id).all()
#     return render_template('main.html', summary=summary)


@app.route('/new_summary', methods=["GET", "POST"])
@login_required
def new_summary():
    form = TextArea()
    if form.is_submitted():
        title = form.title.data
        text = form.text.data
        summary = Summary(title=title,text=text, user=current_user)
        db.session.add(summary)
        db.session.commit()
        return redirect(url_for('main', summary_id=summary.id))
    return render_template('pers_acc_new.html', form=form)


@app.route('/articles/<int:article_id>/edit', methods=["GET", "POST"])
@login_required
def edit_summary(summary_id):
    summary = Summary.query.filter_by(id=summary_id).first()
    form = TextArea()
    if form.validate_on_submit():
        summary.title = form.title.data
        summary.body = form.body.data
        db.session.add(summary)
        db.session.commit()
        return redirect(url_for("get_summary", summary_id=summary.id))
    else:
        form.title.data = summary.title
        form.body.data = summary.body
        return render_template('edit_article.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/notification')
@login_required
def pers_acc_notifications():
    form = NotificationForm()
    return render_template('pers_acc_notifications.html', form=form)


@app.route('/note', methods=["GET", "POST"])
@login_required
def create_notification():
    global reminding_time, note
    form = NotificationForm()
    note = form.note.data
    reminding_time = form.datetime.data
    if form.is_submitted():
        notification = Notification(note=note, reminding_time=reminding_time, user=current_user)
        db.session.add(notification)
        db.session.commit()
        # Thread(target=alarm, args=(current_user,)).start()
        alarm(current_user)
        return redirect(url_for('main'))
    return render_template('pers_acc_notifications.html', form=form)


def alarm(user):
    current_time = datetime.datetime.now().timestamp()
    alarm_time = reminding_time.timestamp()
    sleep(alarm_time - current_time)
    send_email('[ReNote] Notification',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               html_body=render_template('reminder.html',
                                         user=user))


if __name__ == '__main__':
    app.run()
