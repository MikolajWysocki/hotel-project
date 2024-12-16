from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS
from cryptography.fernet import Fernet
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (useful for API communication)
app.secret_key = 'supersecretkey'  # Change this to a secure and unpredictable value

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Encryption key setup and utility functions
def load_key():
    """Load the encryption key or generate a new one if it doesn't exist."""
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()  # Generate a new key
        with open("secret.key", "wb") as key_file:
            key_file.write(key)  # Save the key to a file
    return open("secret.key", "rb").read()  # Read the key from the file

# Initialize the encryption object
fernet = Fernet(load_key())

def encrypt_data(data):
    """Encrypt data using Fernet."""
    if isinstance(data, str):  # For strings, encode and encrypt
        return fernet.encrypt(data.encode()).decode()
    elif isinstance(data, int):  # Convert integers to strings before encryption
        return fernet.encrypt(str(data).encode()).decode()
    elif isinstance(data, datetime):  # Convert datetime objects to ISO format strings
        return fernet.encrypt(data.isoformat().encode()).decode()
    else:
        raise ValueError("Unsupported data type for encryption")

def decrypt_data(data):
    """Decrypt data using Fernet."""
    try:
        return fernet.decrypt(data.encode()).decode()  # Decrypt and decode the data
    except Exception as e:
        raise ValueError("Decryption failed") from e

# User model
class User(db.Model):
    """Model to store user details."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), nullable=False, unique=True)  # Unique username
    password = db.Column(db.String(500), nullable=False)  # Store hashed password

# Reservation model
class Reservation(db.Model):
    """Model to store reservation details."""
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(500), nullable=False)  # Encrypted guest name
    guest_age = db.Column(db.String(300), nullable=False)  # Encrypted guest age
    room_type = db.Column(db.String(300), nullable=False)  # Encrypted room type
    start_date = db.Column(db.String(500), nullable=False)  # Encrypted start date
    end_date = db.Column(db.String(500), nullable=False)  # Encrypted end date
    created_at = db.Column(db.String(500), nullable=False, default=lambda: encrypt_data(datetime.utcnow()))  # Timestamp

# Home route
@app.route('/')
def home():
    """Homepage with options to login or register."""
    if 'user_id' in session:  # Check if user is logged in
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login</a> or <a href='/register'>Register</a>"

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Route to handle user registration."""
    if request.method == 'POST':  # Handle form submission
        username = request.form['username']
        password = request.form['password']
        encrypted_username = encrypt_data(username)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Hash the password

        existing_user = User.query.filter_by(username=username).first()  # Check if username exists
        if existing_user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=encrypted_username, password=hashed_password)  # Create a new user
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route to handle user login."""
    if request.method == 'POST':  # Handle login form submission
        username = request.form['username']
        password = request.form['password']

        # Pobierz wszystkich użytkowników i porównaj odszyfrowane username
        users = User.query.all()
        user = next((u for u in users if decrypt_data(u.username) == username), None)

        if user and check_password_hash(user.password, password):  # Validate credentials
            session['user_id'] = user.id  # Store user ID in session
            session['username'] = username  # Store username in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password!', 'danger')

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Route for the user dashboard."""
    if 'user_id' not in session:  # Check if user is logged in
        flash('You need to log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))
    return render_template('userdashboard.html', username=session['username'])

# API endpoint for creating reservations
@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    """API endpoint to create a reservation."""
    if 'user_id' not in session:  # Ensure the user is authenticated
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    try:
        # Encrypt all reservation details
        guest_name = encrypt_data(data['guest_name'])
        guest_age = encrypt_data(str(data['guest_age']))
        room_type = encrypt_data("Single" if data['room_type'] == 1 else "Double")
        start_date = encrypt_data(data['start_date'])
        end_date = encrypt_data(data['end_date'])

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

# Logout route
@app.route('/logout')
def logout():
    """Route to log out the user."""
    session.clear()  # Clear the session data
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)  
