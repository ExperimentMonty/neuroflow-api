from flask import request, jsonify, g, abort
from sqlalchemy import desc

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
    mood = Mood(value=request.json['mood'])
    db.session.add(mood)
    db.session.commit()
    return jsonify(mood.as_dict())


@app.route('/moods', methods=['GET'])
@auth.login_required
def get_mood():
    moods = Mood.query.order_by(desc('id')).all()
    return jsonify([mood.as_dict() for mood in moods])
