"""Flask app for notes"""
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from forms import AddUserForm


app = Flask(__name__)
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
        
    
