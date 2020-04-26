from flask import request, jsonify
from sqlalchemy import desc

from app import app, db
from app.models import Mood


@app.route('/mood', methods=['POST'])
def set_mood():
    mood = Mood(value=request.json['mood'])
    db.session.add(mood)
    db.session.commit()
    return jsonify(mood.as_dict())


@app.route('/mood', methods=['GET'])
def get_mood():
    moods = Mood.query.order_by(desc('id')).all()
    return jsonify([mood.as_dict() for mood in moods])
