from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Database model for reservations
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(150), nullable=False)
    guest_age = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login</a> or <a href='/register'>Register</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password!', 'danger')

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))
    return render_template('userdashboard.html', username=session['username'])

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
#    if 'user_id' not in session:
 #       return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    try:
        guest_name = data['guest_name']
        guest_age = int(data['guest_age'])
        room_type = "Single" if data['room_type'] == 1 else "Double"
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

        # Validation
        if start_date >= end_date:
            return jsonify({"message": "End date must be after start date"}), 400

        # Create and save reservation
        new_reservation = Reservation(
            guest_name=guest_name,
            guest_age=guest_age,
            room_type=room_type,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({"message": "Reservation created successfully!", "confirmation_number": new_reservation.id}), 201

    except (KeyError, ValueError) as e:
        return jsonify({"message": "Invalid data", "error": str(e)}), 400

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
