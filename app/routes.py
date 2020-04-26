from flask import request, jsonify, g, abort
from sqlalchemy import desc
from datetime import date, timedelta

from app import app, db, auth
from app.models import Mood, User


@auth.verify_password
def verify_password(username, password):
    user =  User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True


@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': username})


@app.route('/moods', methods=['POST'])
@auth.login_required
def set_mood():
    # Check to see if this user currently has a streak, if so, increment it
    today = date.today()
    yesterday = today - timedelta(days=1)
    streak_mood = Mood.query.filter_by(owner=g.user).filter(Mood.timestamp.between(yesterday, today)).first()
    if streak_mood:
        mood = Mood(value=request.json['mood'], owner=g.user, streak=streak_mood.streak+1)
        # Check to see if this is a new longest streak
        g.user.longest_streak = max(g.user.longest_streak, mood.streak)
    else:
        mood = Mood(value=request.json['mood'], owner=g.user)
    db.session.add(mood)
    db.session.commit()
    return jsonify(mood.as_dict())


@app.route('/moods', methods=['GET'])
@auth.login_required
def get_mood():
    moods = Mood.query.filter_by(owner=g.user).order_by(desc('id')).all()
    # If the user doesn't have any moods left, don't fail out, give default message
    if not moods:
        return jsonify({'moods': '', 'streak': 0})
    most_recent_mood = moods[0]

    # Check where this user's streak lays amidst other users
    users = User.query.order_by('longest_streak').all()
    index = users.index(g.user)
    # Index is zero-offset, so need to add 1
    percentile = int((index+1) / len(users) * 100)

    if percentile >= 50:
        return jsonify({'moods': [mood.as_dict() for mood in moods], 'streak': most_recent_mood.streak, 'percentile': percentile})
    else:
        return jsonify({'moods': [mood.as_dict() for mood in moods], 'streak': most_recent_mood.streak})

