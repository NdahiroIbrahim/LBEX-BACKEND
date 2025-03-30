import os
from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'waitlist.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"Database Path: {app.config['SQLALCHEMY_DATABASE_URI']}")

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)
class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/')
def home():
    return "Welcome to the LBEx Waitlist API!"

@app.route('/waitlist', methods=['OPTIONS'])
def options():
    response = jsonify({})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
@app.route('/waitlist', methods=['GET','POST'])
def waitlist():
    data = request.json
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    new_entry = Waitlist(name=name, email=email)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Successfully added to the waitlist!"})

@app.route('/export-db', methods=['GET'])
def export_db():
    try:
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'waitlist.db')

        if not os.path.exists(db_path):
            return jsonify({"error": f"Database file not found at {db_path}"}), 500

        return send_file(db_path, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
