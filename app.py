"""Flask app for notes"""
from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User
from forms import AddUserForm, LogInForm
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
        return redirect(f"/users/{user.username}")
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
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


@app.route('/users/<username>')
def show_user(username):
    """Show user page"""
    if "username" not in session or session["username"] != username:
        flash("You must be logged in to view!")
        return redirect("/")
    else:
        user = User.query.get_or_404(username)
        return render_template("user.html", user=user)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username", None)

    return redirect("/")
