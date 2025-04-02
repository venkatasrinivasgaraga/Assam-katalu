import os
import logging
import threading
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-development")

# In-memory storage for the bot configuration
bot_config = {
    "getcpga_message": "Welcome to CPGA! This is the default message.",
    "admin_username": "admin",
    "admin_password": generate_password_hash("admin")  # Default password, change in production
}

# Import bot.py and start the bot in a separate thread
from bot import start_bot

# Start the bot in a separate thread
bot_thread = threading.Thread(target=start_bot, args=(bot_config,), daemon=True)
bot_thread.start()

# Routes
@app.route('/')
def index():
    return render_template('index.html', message=bot_config["getcpga_message"])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == bot_config["admin_username"] and check_password_hash(bot_config["admin_password"], password):
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_message = request.form.get('message')
        if new_message:
            bot_config["getcpga_message"] = new_message
            flash('CPGA message updated successfully!', 'success')
        
        # Check if password update form was submitted
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password:
            if new_password == confirm_password:
                bot_config["admin_password"] = generate_password_hash(new_password)
                flash('Password updated successfully!', 'success')
            else:
                flash('Passwords do not match!', 'danger')
    
    return render_template('admin.html', message=bot_config["getcpga_message"])

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))
