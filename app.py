from flask import Flask, request, redirect, render_template, current_app, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import NewUserForm, UserLoginForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

toolbar = DebugToolbarExtension(app)


# admin stuff
@app.route('/')
def home():
        # Home Page
    return redirect("/registar")


@app.errorhandler(404)
def error(e): 
    return render_template('error.html', user=session.get('username')), 404


# adding user

@app.route('/registar',  methods=["GET", "POST"])
def add_user():
        # add user post request
    if "username" in session: 
            return redirect(f"/users/{session['username']}")
    form = NewUserForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
            
        user = User.registar(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username
        return redirect("/users/<username>")
    else:
        return render_template("/users/new.html", form=form)

# login/out user
@app.route('/login',  methods=["GET", "POST"])
def login_user():
        # add user post request
    if "username" in session: 
        return redirect(f"/users/{session['username']}")
    
    form = UserLoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
         
        user = User.authenticate(username, password)        
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid Username or Password"]
            return render_template("/users/homelogin.html", form=form)
    
    return render_template("/users/homelogin.html", form=form)

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect("/login")


# specific user and capabilities
# special
@app.route('/users/<username>')
def user_inspect(username):
        # inspect user from directory - more info page
        if "username" not in session or username != session['username']:
             raise Unauthorized()
        
        user = User.query.get(username)
        form = DeleteForm()

        return render_template("/users/show.html", user=user, form=form)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
        # delete user post request
        if "username" not in session or username != session['username']:
             raise Unauthorized()
        
        user = User.query.get(username)
        
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
        return redirect("/login")


# feedback
@app.route('/users/<username>/feedback/new', methods=["GET", "POST"])
def new_Feedback(username):
     print("New Feedback")
     
     if "username" not in session or username != session['username']:
             raise Unauthorized()
     
     form=FeedbackForm()

     if form.validate_on_submit():
          title = form.title.data
          content = form.content.data

          feedback = Feedback(
               title = title,
               content = content,
               username = username
          )
          db.session.add(feedback)
          db.session.commit()

          return redirect(f"/users/{feedback.username}")
     else:
          return render_template("/feedback/newFeedback.html", form = form, user=session.get('username'))
     
@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_Feedback(feedback_id):
     
     feedback = Feedback.query.get(feedback_id)

     if "username" not in session or feedback.username != session['username']:
             raise Unauthorized()
     
     form=FeedbackForm(obj=feedback)

     if form.validate_on_submit():
          feedback.title = form.title.data
          feedback.content = form.content.data
   
          db.session.commit()

          return redirect(f"/users/{feedback.username}")
     return render_template("feedback/editFeedback.html", form=form, feedback=feedback, user=session.get('username'))

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_Feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
  
    if "username" not in session or feedback.username != session['username']:
             raise Unauthorized()
     
    form=DeleteForm()

    if form.validate_on_submit():
          db.session.delete(feedback)
          db.session.commit()

          return redirect(f"/users/{feedback.username}", user=session.get('username'))










