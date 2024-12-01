from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, login_manager
from app.database import register_user, get_user_by_email, check_password, get_chat_history
from app.models import User
from bson import ObjectId
from app import db


@login_manager.user_loader
def load_user(user_id):
    """Load the user from the database based on their ID."""
    user_data = db.users.find_one({"_id": ObjectId(user_id)})  # Query by ObjectId
    if user_data:
        return User.from_dict(user_data)
    return None


# --- Routes ---
@app.route('/')
def home():
    """Homepage with public chat."""
    print(f"Current user: {current_user}, Authenticated: {current_user.is_authenticated}")  # Debug print
    if current_user.is_authenticated:
        chat_history = get_chat_history()  # Fetch chat history from the database
        return render_template('index.html', username=current_user.username, chat_history=chat_history)
    return redirect(url_for('login'))  # Redirect to login if the user is not authenticated



@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Call the function to register the user
        result = register_user(username, email, password)

        # Flash the result message and print it
        if not result['success']:
            flash(result['message'], 'danger')
            print(f"Flash message: {result['message']}")  # Print message
            return redirect(url_for('login'))

        # Fetch the newly created user data and log them in
        user_data = get_user_by_email(email)
        if user_data:
            print(user_data)
            user = User.from_dict(user_data)
            login_user(user)

        flash('Registration successful!', 'success')
        print("Flash message: Registration successful!")  # Print message
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch the user data by email
        user_data = get_user_by_email(email)
        if user_data:
            # Check the password
            if check_password(user_data['password'], password):
                print(user_data)
                user = User.from_dict(user_data)
                print("here's the super importent print!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(user)
                login_user(user)
                flash('Login successful!', 'success')
                print("Flash message: Login successful!")  # Print message
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password.', 'danger')
                print("Flash message: Invalid email or password.")  # Print message
        else:
            flash('Invalid email or password.', 'danger')
            print("Flash message: Invalid email or password.")  # Print message

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Log the user out."""
    logout_user()
    flash('You have been logged out.', 'info')
    print("Flash message: You have been logged out.")  # Print message
    return redirect(url_for('login'))
