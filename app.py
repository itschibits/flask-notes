"""Flask app for notes"""
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from forms import AddUserForm
from project_secrets import FLASK_SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def homepage():
    """Redirect to /register"""
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """ Register user and shows registeration form"""
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """ Login user and shows log-in  form"""

    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors= ['Invalid username/password']
            return render_template("login.html", form=form)
        