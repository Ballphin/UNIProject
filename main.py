from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, PostForm
from models import db, User, Post, Like, Comment  # Ensure Like model is imported

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    return render_template('index.html')

#Main Page
@app.route('/main', methods=['GET', 'POST'])
@login_required
def main_page():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main_page'))
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main.html', posts=posts, form=form)

#Register and Login
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = RegistrationForm()


    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_page'))
        
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

#Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#Post Route
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main_page'))

#Like Post Route
@app.route("/like_post/<int:post_id>", methods=['POST'])
@login_required
def like_post(post_id):
    major = request.args.get('major', None)
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if like:
        # If like exists, unlike the post
        db.session.delete(like)
        flash('Post unliked!', 'info')
    else:
        # Like the post
        new_like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        flash('Post liked!', 'success')

    db.session.commit()

    # Redirect to the specific forum page if major is known, otherwise to the main forum
    if major:
        return redirect(url_for('forum', major=major))
    else:
        return redirect(url_for('main_page'))


#Main Post Route
@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


#Comment Post
@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    major = request.args.get('major', None)
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    if content:
        comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')

    else:
        flash('There was an error with your comment.', 'danger')

    #Redirecting to Correct Major Post
    if major:
        return redirect(url_for('forum', major=major))
    else:
        return redirect(url_for('main_page'))

# Deleting Comment
@app.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    major = request.args.get('major', None)
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)  # Forbidden access if the current user isn't the comment's author
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    
    if major:
        return redirect(url_for('forum', major=major))
    else:
        return redirect(url_for('main_page'))


#Profile Page, Updating NickName
#Display the profile page where users can see their nickname, email, and posts. 
#Additionally, we'll implement a form for changing the nickname.
class ProfileForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    submit = SubmitField('Update Nickname')

#Profile Route
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    user = User.query.get_or_404(current_user.id)
    if form.validate_on_submit():
        user.username = form.nickname.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.nickname.data = current_user.username
    return render_template('profile.html', title='Profile', form=form, user=user)

#Different Forums 
@app.route('/forum/<major>', methods=['GET', 'POST'])
@login_required
def forum(major):
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # You might want to add an additional field to the Post model for major
        new_post.major = major
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('forum', major=major))
    # You would filter posts by major here
    posts = Post.query.filter_by(major=major).order_by(Post.date_posted.desc()).all()
    return render_template('forum.html', major=major, posts=posts, form=form)




##########################################################################################

if __name__ == '__main__':
    app.run(debug=True)
