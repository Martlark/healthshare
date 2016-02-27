from flask import render_template, flash, redirect, session, url_for, request, g, abort, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, PostForm, AnswerForm
from .models import User, Post, Answer
import datetime

@lm.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.timestamp = datetime.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    print 'login',g.user
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.authenticated = True
            user.timestamp = datetime.datetime.utcnow()
            db.session.add(user)
            db.session.commit()

            login_user(user,remember=True)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            # create the user
            user = User(email=form.email.data,timestamp=datetime.datetime.utcnow(),previous_timestamp=datetime.datetime.utcnow())
            db.session.add(user)
            db.session.commit()
            flash('new user account created')
            login_user(user,remember=True)
            return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, timestamp=datetime.datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your question is now live!')
        return redirect(url_for('index'))

    user = g.user
    previous_timestamp=user.previous_timestamp
    user.previous_timestamp = datetime.datetime.utcnow()
    db.session.add(user)
    db.session.commit()

    posts = Post.query.all()
    for post in posts:
        votes = 0
        for answer in post.answers:
            votes += answer.up_vote
            votes -= answer.down_vote
        post.votes = votes

    posts = sorted(posts, key=lambda post: post.votes, reverse=True)
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts,
                           previous_timestamp=previous_timestamp,
                           form=form)


@app.route('/api/answer/<id>/vote/<direction>')
@login_required
def api_answer_vote(id, direction):
    answer = Answer.query.get(id)
    if answer:
        if not answer.up_vote:
            answer.up_vote = 0

        if not answer.down_vote:
            answer.down_vote = 0

        if direction == 'up':
            answer.up_vote += 1
        elif direction == 'down':
            answer.down_vote += 1
        else:
            return jsonify( {'result':'error','message':'invalid direction'})

        db.session.add(answer)
        db.session.commit()
        return jsonify( {'result':'ok','message':answer.up_vote-answer.down_vote})


    return jsonify( {'result':'error','message':'answer not found'})



@app.route('/question/<id>', methods=['GET', 'POST'])
@login_required
def question(id):
    question = Post.query.get(id)
    if question:
        question_form = PostForm()
        answer_form = AnswerForm()

        if question_form.validate_on_submit():
            question.body = question_form.body.data
            question.title = question_form.title.data
            db.session.add(question)
            db.session.commit()
            flash('Question updated!')
            return redirect(url_for('question',id=id))

        if answer_form.validate_on_submit():
            answer = Answer(body=answer_form.body.data, timestamp=datetime.datetime.utcnow(), up_vote=0, down_vote=0, author=g.user, question=question)
            db.session.add(answer)
            db.session.commit()
            flash('Your answer is now live!')
            return redirect(url_for('question',id=id))

        user = g.user
        return render_template("question.html",
                               title='Question',
                               user=user,
                               question=question,
                               question_form=question_form,
                               answer_form=answer_form,
                               )
    else:
        abort(404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<email>')
@login_required
def user(email):
    user = User.query.filter_by(email=email).first()

    if user == None:
        flash('User %s not found.' % email)
        return redirect(url_for('index'))

    previous_timestamp=user.previous_timestamp
    return render_template('user.html',
                           user=user,
                           previous_timestamp=previous_timestamp)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
