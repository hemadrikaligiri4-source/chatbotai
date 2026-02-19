import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from models import db, User, ChatHistory
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
# Use a static secret key from environment or generate a random one for local development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
# Support for Render Postgres (DATABASE_URL) or fallback to local SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///hemadri.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hemadrik2006@gmail.com'
app.config['MAIL_PASSWORD'] = 'hthw hlpj zotl fozw'
app.config['MAIL_DEFAULT_SENDER'] = 'hemadrik2006@gmail.com'

db.init_app(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not all([full_name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        print(f"Registration failed: Email {email} already exists")
        return jsonify({"error": "Email already exists"}), 400

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(full_name=full_name, email=email, password=hashed_password, is_verified=False)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(f"Database error during registration: {e}")
        return jsonify({"error": "Database error occurred. Please try again."}), 500

    # Send verification email
    token = s.dumps(email, salt='email-confirm')
    link = url_for('verify_email', token=token, _external=True)
    msg = Message('Confirm Your Email - Hemadri Chatbot', recipients=[email])
    msg.body = f'Hi {full_name},\n\nThank you for joining Hemadri Chatbot Educational! Please click the link below to verify your email address:\n\n{link}\n\nHappy Learning!'
    
    try:
        # Check if auto-verification is enabled for testing
        if os.environ.get('AUTO_VERIFY') == 'true':
            new_user.is_verified = True
            db.session.commit()
            return jsonify({"message": "User registered and automatically verified (Debug Mode). You can now login."}), 201
        
        mail.send(msg)
        return jsonify({"message": "User registered successfully. Please check your email to verify your account."}), 201
    except Exception as e:
        print(f"Error sending email or auto-verifying: {e}")
        return jsonify({"message": "User registered, but failed to send verification email. (Error: " + str(e) + ")"}), 201

@app.route('/verify-email/<token>')
def verify_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600) # 1 hour expiry
    except:
        return "<h1>The verification link is invalid or has expired.</h1>", 400
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        return "<h1>Email already verified. You can now login.</h1>"
    
    user.is_verified = True
    db.session.commit()
    return "<h1>Email verified successfully! You can now login to Hemadri Chatbot.</h1>"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember', False)

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        if not user.is_verified:
            print(f"Login attempt for unverified email: {email}")
            return jsonify({"error": "Please verify your email before logging in."}), 403
        
        login_user(user, remember=remember)
        print(f"User logged in: {email}")
        return jsonify({"message": "Logged in successfully", "user": {"full_name": user.full_name, "email": user.email}}), 200
    
    print(f"Login failed for email: {email}")
    return jsonify({"error": "Invalid email or password"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

# --- Chat Routes ---

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Mock AI Response Logic (Replace with OpenAI/Gemini API)
    ai_response = generate_mock_response(user_message)

    # Save to history
    new_chat = ChatHistory(user_id=current_user.id, message=user_message, response=ai_response)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"response": ai_response})

@app.route('/history', methods=['GET'])
@login_required
def history():
    chats = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp.asc()).all()
    history = [{"message": chat.message, "response": chat.response, "timestamp": chat.timestamp} for chat in chats]
    return jsonify(history)

@app.route('/clear_chat', methods=['POST'])
@login_required
def clear_chat():
    ChatHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"message": "Chat history cleared"})

import requests
import json

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "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")

def generate_mock_response(message):
    try:
        print(f"Sending message to OpenRouter (Gemini 2.0 Flash): {message[:50]}...")
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Hemadri Chatbot Professional",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-001",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are Hemadri, a highly sophisticated and professional AI Learning Assistant. Your goal is to provide elite-level educational guidance to students and professionals. Be precise, encouraging, and provide depth in your explanations, especially for programming and career growth. Use markdown for better readability."
                    },
                    {"role": "user", "content": message}
                ],
            })
        )
        print(f"OpenRouter Status: {response.status_code}")
        response_json = response.json()
        
        if response.status_code == 200:
            if "choices" in response_json and len(response_json["choices"]) > 0:
                return response_json["choices"][0]["message"]["content"]
            else:
                print(f"Unexpected JSON structure: {response_json}")
                return "I received an unexpected response from the AI. Please try again."
        else:
            print(f"OpenRouter Error Content: {response_json}")
            error_data = response_json.get('error', {})
            error_msg = error_data.get('message', 'Unknown error')
            return f"AI Service Error: {error_msg}"
            
    except Exception as e:
        print(f"Critical Error calling OpenRouter: {e}")
        return "Oops! Something went wrong while connecting to my AI brain. Please check your connection."

@app.route('/debug/status', methods=['GET'])
def debug_status():
    try:
        user_count = User.query.count()
        return jsonify({
            "status": "online",
            "database": "connected",
            "user_count": user_count,
            "db_uri": app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] # Hide credentials
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/debug/verify_all', methods=['GET'])
def verify_all_users():
    try:
        users = User.query.filter_by(is_verified=False).all()
        for user in users:
            user.is_verified = True
        db.session.commit()
        return jsonify({"message": f"Successfully verified {len(users)} users!"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
