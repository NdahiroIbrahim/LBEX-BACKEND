import os
from flask import Blueprint, request, jsonify, send_file
from app import db
from app.model import Waitlist, Business

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Welcome to LBEx Waitlist API!"

@main.route('/waitlist', methods=['POST'])
def add_to_waitlist():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Invalid input"}), 400

    new_entry = Waitlist(name=data['name'], email=data['email'])

    try:
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message" : "Succesfully added to the waitlist"}), 201
    except Exception  as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@main.route('/register-business', methods=['POST'])
def register_business():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Invalid input"}), 400

    new_business = Business(name=data['name'], email=data['email'], industry=data.get('industry'), location=data.get('location'))

    try:
        db.session.add(new_business)
        db.session.commit()
        return jsonify({"message": "Business successfully registered!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@main.route('/export-db', methods=['GET'])
def export_db():
    db_path = os.path.join(os.getcwd(), 'instance', 'app.db')
    
    if not os.path.exists(db_path):
        return jsonify({'message': 'Database file not found'}), 404

    return send_file(db_path, as_attachment=True)