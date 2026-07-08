# ===================== app.py - VERSI SUPER LENGKAP =====================
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from flask_cors import CORS
from flask_mail import Mail, Message
import sqlite3
import json
import requests
import time
import random
import re
import os
import hashlib
import csv
import io
from datetime import datetime, timedelta
from functools import wraps
import threading
import logging
import threading

app = Flask(__name__)
app.secret_key = "davaofc_super_secret_key_2024_ultra_secure"
app.permanent_session_lifetime = timedelta(days=7)
CORS(app)

# ===================== LOGGING =====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===================== EMAIL CONFIG =====================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'davae5270@gmail.com'
app.config['MAIL_PASSWORD'] = 'iqyu ocic jgsb tzsz'
app.config['MAIL_DEFAULT_SENDER'] = 'davae5270@gmail.com'

mail = Mail(app)

# ===================== KONFIGURASI =====================
BOT_TOKEN = "8699257728:AAHYiE8d5iG75qfXN7xMtv2k3AFWhAQPzco"
OWNER_ID = 8737366854
OWNER_EMAIL = "owner@davaofc.com"
OWNER_USERNAME = "davaofc"
OWNER_PASSWORD = "davaofc123"
GROUP_CHAT_ID = -1003966392329
DB_PATH = 'exchange_bot.db'

# ===================== DATABASE =====================

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
# Users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        email TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT,
        full_name TEXT,
        phone TEXT,
        avatar TEXT,
        balance REAL DEFAULT 0,
        is_verified INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0,
        is_owner INTEGER DEFAULT 0,
        referrer_id INTEGER DEFAULT NULL,
        ip_address TEXT,
        banned_at TIMESTAMP,
        ban_reason TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        email_verified_at TIMESTAMP
    )''')
    
    # OTP
    cursor.execute('''CREATE TABLE IF NOT EXISTS otp_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        code TEXT,
        expires_at TIMESTAMP,
        is_used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Orders
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE,
        user_id INTEGER,
        username TEXT,
        full_name TEXT,
        bank_name TEXT,
        account_number TEXT,
        amount_usd REAL,
        amount_idr REAL,
        fee_idr REAL DEFAULT 0,
        tx_hash TEXT,
        photo_id TEXT,
        crypto_type TEXT DEFAULT 'USDT BEP-20',
        status TEXT DEFAULT 'pending',
        transfer_status TEXT DEFAULT 'pending',
        transferred_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        approved_at TIMESTAMP
    )''')
    
    # Deposits
    cursor.execute('''CREATE TABLE IF NOT EXISTS deposits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dep_number TEXT UNIQUE,
        user_id INTEGER,
        username TEXT,
        full_name TEXT,
        amount REAL,
        method TEXT DEFAULT 'DANA',
        destination TEXT,
        photo_id TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        approved_at TIMESTAMP
    )''')
    
    # Withdrawals
    cursor.execute('''CREATE TABLE IF NOT EXISTS withdrawals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wd_number TEXT UNIQUE,
        user_id INTEGER,
        username TEXT,
        full_name TEXT,
        destination TEXT,
        amount REAL,
        fee REAL DEFAULT 0,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        approved_at TIMESTAMP
    )''')
    
    # Referrals
    cursor.execute('''CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        referred_id INTEGER,
        commission REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Reviews
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        full_name TEXT,
        rating INTEGER,
        review_text TEXT,
        is_approved INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        approved_at TIMESTAMP
    )''')
    
    # Arisan
    cursor.execute('''CREATE TABLE IF NOT EXISTS arisan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_slots INTEGER,
        price REAL,
        currency TEXT DEFAULT 'IDR',
        owner_profit_percent REAL DEFAULT 10.0,
        status TEXT DEFAULT 'active',
        winner_id INTEGER,
        winner_name TEXT,
        winner_wallet_info TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP
    )''')
    
    # Arisan Participants
    cursor.execute('''CREATE TABLE IF NOT EXISTS arisan_participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arisan_id INTEGER,
        user_id INTEGER,
        username TEXT,
        full_name TEXT,
        wallet_info TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Investasi
    cursor.execute('''CREATE TABLE IF NOT EXISTS investasi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        full_name TEXT,
        modal REAL,
        profit REAL DEFAULT 0,
        total_return REAL DEFAULT 0,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP,
        status TEXT DEFAULT 'active',
        last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Investasi Settings
    cursor.execute('''CREATE TABLE IF NOT EXISTS investasi_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        min_invest INTEGER DEFAULT 50000,
        max_invest INTEGER DEFAULT 10000000,
        profit_percent INTEGER DEFAULT 50,
        duration_hours INTEGER DEFAULT 24,
        interest_per_second REAL DEFAULT 1,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Slot History
    cursor.execute('''CREATE TABLE IF NOT EXISTS slot_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        full_name TEXT,
        bet_amount REAL,
        win_amount REAL,
        symbols TEXT,
        game_type TEXT DEFAULT 'classic',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Settings
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')
    
    # Fee Settings
    cursor.execute('''CREATE TABLE IF NOT EXISTS fee_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        min_amount REAL,
        max_amount REAL,
        fee REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Maintenance Settings
    cursor.execute('''CREATE TABLE IF NOT EXISTS maintenance_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feature TEXT UNIQUE,
        is_active INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Wallet Settings (DITINGKATKAN DENGAN RATE)
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallet_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token_name TEXT UNIQUE NOT NULL,
        address TEXT NOT NULL,
        rate REAL DEFAULT 15500,
        is_active INTEGER DEFAULT 1,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Transaction Log
    cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        description TEXT,
        reference_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # ===== INSERT DEFAULT WALLETS =====
    default_wallets = {
        'USDT BEP-20': ('0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', 15500),
        'USDT TRC-20': ('TXYZ...', 15500),
        'USDT ERC-20': ('0x...', 15500),
        'BTC': ('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 650000000),
        'ETH': ('0x...', 35000000),
        'BNB': ('0x...', 5000000),
        'SOL': ('So111...', 2000000),
        'DOGE': ('DDoGE...', 2000)
    }
    for token, (address, rate) in default_wallets.items():
        cursor.execute('''INSERT OR IGNORE INTO wallet_settings (token_name, address, rate) 
                         VALUES (?, ?, ?)''', (token, address, rate))
    
    # ===== INSERT DEFAULT FEES =====
    check_fee = cursor.execute('SELECT COUNT(*) FROM fee_settings').fetchone()[0]
    if check_fee == 0:
        default_fees = [
            (0, 100000, 5000),
            (100001, 500000, 10000),
            (500001, 1000000, 20000),
            (1000001, 999999999, 50000)
        ]
        for min_a, max_a, fee in default_fees:
            cursor.execute('''INSERT INTO fee_settings (min_amount, max_amount, fee) 
                            VALUES (?, ?, ?)''', (min_a, max_a, fee))
    
    # ===== INSERT DEFAULT SETTINGS =====
    default_settings = [
        ('site_name', 'DavaOFC'),
        ('site_description', 'Crypto Exchange & Slot Games'),
        ('min_deposit', '10000'),
        ('min_withdraw', '50000'),
        ('withdraw_fee', '5000'),
        ('profit_rate', '5'),
        ('profit_interval', '300'),
        ('maintenance', '0'),
        ('owner_email', OWNER_EMAIL),
        ('owner_username', OWNER_USERNAME),
        ('owner_password', hashlib.sha256(OWNER_PASSWORD.encode()).hexdigest()),
        ('slot_min_bet', '400'),
        ('slot_max_bet', '204800'),
        ('slot_jackpot', '10000'),
        ('investasi_status', 'active'),
        ('referral_bonus', '400'),
        ('transaction_fee', '5000'),
        ('usd_rate', '15500'),
        ('usd_rate_auto_update', '1'),
        ('auto_approve_orders', '0'),
        ('telegram_notifications', '1'),
        ('email_notifications', '1')
    ]
    for key, value in default_settings:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))
    
    # ===== INSERT DEFAULT MAINTENANCE =====
    features = ['convert', 'deposit', 'withdraw', 'slot', 'arisan', 'investasi', 'referral', 'reviews', 'register']
    for feature in features:
        cursor.execute('''INSERT OR IGNORE INTO maintenance_settings (feature, is_active) 
                         VALUES (?, 0)''', (feature,))
    
    # ===== INSERT DEFAULT INVESTASI SETTINGS =====
    cursor.execute('''INSERT OR IGNORE INTO investasi_settings 
                     (id, min_invest, max_invest, profit_percent, duration_hours, interest_per_second, is_active) 
                     VALUES (1, 50000, 10000000, 50, 24, 1, 1)''')
    
    # ===== CREATE OWNER ACCOUNT =====
    owner = cursor.execute('SELECT * FROM users WHERE email = ?', (OWNER_EMAIL,)).fetchone()
    if not owner:
        cursor.execute('''
            INSERT INTO users (email, username, full_name, password, is_verified, is_owner, balance)
            VALUES (?, ?, ?, ?, 1, 1, 999999999)
        ''', (OWNER_EMAIL, OWNER_USERNAME, 'DavaOFC Owner', hashlib.sha256(OWNER_PASSWORD.encode()).hexdigest()))
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized successfully with dynamic rates & fees")

init_db()

# ===================== HELPER FUNCTIONS =====================

def execute_query(query, params=(), fetch_one=False, fetch_all=False):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp():
    return str(random.randint(100000, 999999))

def format_rupiah(amount):
    if amount is None:
        return "Rp 0"
    return f"Rp {int(amount):,}".replace(",", ".")

def format_usd(amount):
    if amount is None:
        return "$0.00"
    return f"${amount:.2f}"

def get_setting(key, default=None):
    try:
        row = execute_query('SELECT value FROM settings WHERE key = ?', (key,), fetch_one=True)
        return row['value'] if row else default
    except:
        return default

def update_setting(key, value):
    execute_query('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))

def send_telegram_message(chat_id, text):
    if not chat_id:
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Telegram send error: {e}")
        return False

def send_telegram_photo(chat_id, photo_data, caption=""):
    if not chat_id or not photo_data:
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        if photo_data.startswith('data:image'):
            import base64
            photo_data = photo_data.split(',')[1]
            files = {'photo': ('image.jpg', base64.b64decode(photo_data), 'image/jpeg')}
            data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'HTML'}
            response = requests.post(url, data=data, files=files, timeout=30)
        else:
            response = requests.post(url, json={
                "chat_id": chat_id,
                "photo": photo_data,
                "caption": caption,
                "parse_mode": "HTML"
            }, timeout=30)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Telegram photo error: {e}")
        return False

def send_otp_email(email, otp):
    try:
        msg = Message(
            subject='🔐 Verifikasi Akun DavaOFC',
            recipients=[email],
            body=f"""
Halo!

Terima kasih telah mendaftar di DavaOFC.

Kode verifikasi Anda adalah:

🔑 {otp}

Kode ini berlaku selama 5 menit.

Jika Anda tidak merasa mendaftar, abaikan email ini.

━━━━━━━━━━━━━━━━━━━━
🚀 DavaOFC - Crypto Exchange & Slot Games
"""
        )
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Email send error: {e}")
        return False

def is_owner(user_id):
    try:
        user = execute_query('SELECT is_owner FROM users WHERE id = ?', (user_id,), fetch_one=True)
        return user and user['is_owner'] == 1
    except:
        return False

def get_user_balance(user_id):
    try:
        user = execute_query('SELECT balance FROM users WHERE id = ?', (user_id,), fetch_one=True)
        return user['balance'] if user else 0
    except:
        return 0

def log_transaction(user_id, type, amount, description, reference_id=None):
    try:
        execute_query('''
            INSERT INTO transaction_logs (user_id, type, amount, description, reference_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, type, amount, description, reference_id))
    except Exception as e:
        logger.error(f"Log transaction error: {e}")

def is_maintenance_active(feature):
    try:
        row = execute_query('SELECT is_active FROM maintenance_settings WHERE feature = ?', (feature,), fetch_one=True)
        return row and row['is_active'] == 1
    except:
        return False

# ===================== AUTH DECORATOR =====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu!', 'warning')
            return redirect(url_for('login'))
        
        # Cek maintenance untuk fitur register/login
        if is_maintenance_active('register'):
            flash('Fitur login sedang dalam maintenance. Silakan coba lagi nanti.', 'danger')
            return redirect(url_for('logout'))
        
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu!', 'warning')
            return redirect(url_for('login'))
        
        if not is_owner(session['user_id']):
            flash('Akses ditolak! Anda bukan owner.', 'danger')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def maintenance_check(feature):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if is_maintenance_active(feature):
                return jsonify({
                    'success': False,
                    'error': f'Fitur {feature} sedang dalam maintenance. Silakan coba lagi nanti.'
                }), 503
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ===================== ROUTES =====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

# ============================================================
# LOGIN PAGE
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            return render_template('login.html', error='Email dan password wajib diisi!')
        
        user = execute_query('SELECT * FROM users WHERE email = ? OR username = ?', (email, email), fetch_one=True)
        
        if not user:
            return render_template('login.html', error='Akun tidak ditemukan!')
        
        if user['is_banned'] == 1:
            return render_template('login.html', error='Akun telah diblokir!')
        
        if user['password'] != hash_password(password):
            return render_template('login.html', error='Password salah!')
        
        # SET SESSION
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['email'] = user['email']
        session['full_name'] = user['full_name']
        session['is_owner'] = user.get('is_owner', 0)
        session.permanent = True
        
        # DEBUG - CEK SESSION
        print(f"✅ Login berhasil! Session: {dict(session)}")
        print(f"🔍 user_id: {session.get('user_id')}")
        print(f"🔍 is_owner: {session.get('is_owner')}")
        
        # Update last_login
        execute_query('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')
    
# ============================================================
# FUNGSI KIRIM EMAIL ASYNC
# ============================================================
def send_otp_async(email, otp):
    """Kirim OTP di background thread - TIDAK MEMBLOKIR RESPONSE"""
    try:
        send_otp_email(email, otp)
        logger.info(f"✅ OTP sent to {email}")
    except Exception as e:
        logger.error(f"❌ Send OTP async error: {e}")

# ============================================================
# API REGISTER - FIXED (TANPA DELAY + OTP TERKIRIM)
# ============================================================
@app.route('/api/register', methods=['POST'])
def api_register():
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        full_name = data.get('full_name', '').strip()
        password = data.get('password', '')
        phone = data.get('phone', '').strip()
        referral_code = data.get('referral_code', '').strip()
        
        # Validasi
        if not all([email, username, full_name, password]):
            return jsonify({'success': False, 'error': 'Semua field harus diisi!'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password minimal 6 karakter!'}), 400
        
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return jsonify({'success': False, 'error': 'Email tidak valid!'}), 400
        
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return jsonify({'success': False, 'error': 'Username harus 3-20 karakter (huruf, angka, underscore)'}), 400
        
        # Cek existing
        existing = execute_query(
            'SELECT id FROM users WHERE email = ? OR username = ?', 
            (email, username), 
            fetch_one=True
        )
        if existing:
            return jsonify({'success': False, 'error': 'Email atau Username sudah terdaftar!'}), 400
        
        # ⚡ GENERATE OTP
        otp = generate_otp()
        
        # ⚡ SIMPAN OTP KE DATABASE
        execute_query('''
            INSERT INTO otp_codes (email, code, expires_at)
            VALUES (?, ?, datetime('now', '+5 minutes'))
        ''', (email, otp))
        
        # ⚡ KIRIM EMAIL DI BACKGROUND (PAKAI THREAD)
        # TAPI KITA PASTIKAN THREADNYA JALAN
        def send_email_task():
            try:
                print(f"📧 Mengirim OTP ke {email}...")
                send_otp_email(email, otp)
                print(f"✅ OTP berhasil dikirim ke {email}")
            except Exception as e:
                print(f"❌ Gagal kirim email: {e}")
                # Kalau gagal, simpan di session
                session['dev_otp'] = otp
                session['dev_email'] = email
        
        # Start thread
        import threading
        thread = threading.Thread(target=send_email_task)
        thread.daemon = True
        thread.start()
        
        # ⚡ KASIH WAKTU SEDIKIT AGAR THREAD JALAN
        time.sleep(0.1)  # Hanya 0.1 detik, ga kerasa
        
        # ⚡ HASH PASSWORD
        hashed_password = hash_password(password)
        
        # Simpan data registrasi ke session
        session['register_data'] = {
            'email': email,
            'username': username,
            'full_name': full_name,
            'password': hashed_password,
            'phone': phone,
            'referral_code': referral_code
        }
        
        # Simpan OTP di session untuk fallback
        session['dev_otp'] = otp
        session['dev_email'] = email
        
        # Log waktu
        elapsed = time.time() - start_time
        print(f"⚡ Register API response time: {elapsed:.2f}s")
        
        # ⚡ RESPONSE CEPAT
        return jsonify({
            'success': True, 
            'message': 'Kode OTP telah dikirim ke email Anda!',
            'email': email,
            'otp': otp if app.debug else None  # Tampilkan OTP di response
        })
        
    except Exception as e:
        print(f"❌ API Register error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
        
# ============================================================
# API VERIFY OTP - FINAL (DENGAN PERBAIKAN KECIL)
# ============================================================
@app.route('/api/verify_otp', methods=['POST'])
def api_verify_otp():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
        
        if not email or not otp:
            return jsonify({'success': False, 'error': 'Email dan OTP wajib diisi!'}), 400
        
        # ⚡ CEK OTP (1 query)
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM otp_codes 
            WHERE email = ? AND code = ? AND is_used = 0 AND expires_at > datetime('now')
            ORDER BY id DESC LIMIT 1
        ''', (email, otp))
        row = cursor.fetchone()
        
        # Fallback: development mode
        if not row and session.get('dev_otp') == otp and session.get('dev_email') == email:
            row = (0,)
        
        if not row:
            conn.close()
            return jsonify({'success': False, 'error': 'Kode OTP tidak valid atau sudah kadaluarsa!'}), 400
        
        # ⚡ UPDATE OTP (1 query)
        if row[0] != 0:
            cursor.execute('UPDATE otp_codes SET is_used = 1 WHERE id = ?', (row[0],))
        
        # Ambil data registrasi dari session
        register_data = session.get('register_data')
        if not register_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Sesi registrasi tidak ditemukan! Silakan daftar ulang.'}), 400
        
        # ⚡ CEK USER + INSERT (dalam 1 transaksi)
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            session.pop('register_data', None)
            return jsonify({'success': False, 'error': 'Email sudah terdaftar! Silakan login.'}), 400
        
        # INSERT USER
        cursor.execute('''
            INSERT INTO users (email, username, full_name, password, is_verified)
            VALUES (?, ?, ?, ?, 1)
        ''', (
            email, 
            register_data.get('username'), 
            register_data.get('full_name'), 
            register_data.get('password')
        ))
        user_id = cursor.lastrowid
        
        # ⚡ HANDLE REFERRAL (dioptimasi)
        if register_data.get('referral_code'):
            try:
                referrer_id = int(register_data['referral_code'])
                if referrer_id != user_id:
                    # Insert referral
                    cursor.execute(
                        'INSERT INTO referrals (user_id, referred_id) VALUES (?, ?)', 
                        (referrer_id, user_id)
                    )
                    
                    # Get bonus (pakai default 400)
                    cursor.execute('SELECT value FROM settings WHERE key = ?', ('referral_bonus',))
                    row = cursor.fetchone()
                    bonus = float(row[0]) if row else 400.0
                    
                    # Update balance
                    cursor.execute(
                        'UPDATE users SET balance = balance + ? WHERE id = ?', 
                        (bonus, referrer_id)
                    )
                    
                    # Log transaction
                    cursor.execute('''
                        INSERT INTO transactions (user_id, type, amount, description)
                        VALUES (?, ?, ?, ?)
                    ''', (referrer_id, 'referral', bonus, f'Bonus referral dari {register_data.get("username")}'))
                    
            except Exception as e:
                print(f"⚠️ Referral error: {e}")  # Pakai print biar ga perlu logger
        
        conn.commit()
        
        # ⚡ AMBIL USER DATA (1 query)
        cursor.execute('''
            SELECT id, username, email, full_name, is_owner, balance 
            FROM users WHERE id = ?
        ''', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        # Hapus session
        session.pop('register_data', None)
        session.pop('dev_otp', None)
        session.pop('dev_email', None)
        
        # ⚡ AUTO LOGIN
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            session['full_name'] = user[3]
            session['is_owner'] = user[4] if len(user) > 4 else 0
            session.permanent = True
            
            # ⚡ UPDATE LAST_LOGIN (background)
            def update_last_login():
                try:
                    execute_query('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
                except Exception as e:
                    print(f"⚠️ Update last_login error: {e}")
            
            threading.Thread(target=update_last_login, daemon=True).start()
        
        # ⚡ KIRIM NOTIF TELEGRAM (background)
        def send_telegram_notification():
            try:
                send_telegram_message(
                    OWNER_ID,
                    f"📝 *REGISTER BARU!*\n\n"
                    f"👤 Nama: {register_data.get('full_name')}\n"
                    f"📧 Email: {email}\n"
                    f"📝 Username: @{register_data.get('username')}\n"
                    f"🆔 ID: {user_id}"
                )
            except Exception as e:
                print(f"⚠️ Telegram error: {e}")
        
        threading.Thread(target=send_telegram_notification, daemon=True).start()
        
        return jsonify({
            'success': True,
            'message': 'Akun berhasil dibuat! Selamat datang!',
            'redirect': '/dashboard'
        })
        
    except Exception as e:
        print(f"❌ API Verify OTP error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# API RESEND OTP - FINAL
# ============================================================
@app.route('/api/resend_otp', methods=['POST'])
def api_resend_otp():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'success': False, 'error': 'Email wajib diisi!'}), 400
        
        # ⚡ CEK APAKAH EMAIL ADA DI SESSION REGISTER
        register_data = session.get('register_data')
        if not register_data or register_data.get('email') != email:
            return jsonify({'success': False, 'error': 'Sesi tidak ditemukan! Silakan daftar ulang.'}), 400
        
        # ⚡ KOMBINASI UPDATE + INSERT DALAM 1 TRANSAKSI
        conn = get_db()
        cursor = conn.cursor()
        
        # Nonaktifkan OTP lama
        cursor.execute('UPDATE otp_codes SET is_used = 1 WHERE email = ? AND is_used = 0', (email,))
        
        # Generate OTP baru
        otp = generate_otp()
        cursor.execute('''
            INSERT INTO otp_codes (email, code, expires_at)
            VALUES (?, ?, datetime('now', '+5 minutes'))
        ''', (email, otp))
        
        conn.commit()
        conn.close()
        
        # ⚡ UPDATE SESSION DENGAN OTP BARU
        session['dev_otp'] = otp
        session['dev_email'] = email
        
        # ⚡ KIRIM EMAIL DI BACKGROUND (TIDAK NUNGGU)
        def send_email_task():
            try:
                send_otp_email(email, otp)
                print(f"✅ OTP baru terkirim ke {email}")
            except Exception as e:
                print(f"❌ Gagal kirim OTP baru: {e}")
                # Kalau gagal, OTP tetap ada di session
        
        thread = threading.Thread(target=send_email_task)
        thread.daemon = True
        thread.start()
        
        # ⚡ RESPONSE CEPAT
        return jsonify({
            'success': True,
            'message': 'Kode OTP baru telah dikirim ke email Anda!',
            'email': email,
            'otp': otp if app.debug else None  # Tampilkan OTP di response (development)
        })
        
    except Exception as e:
        print(f"❌ Resend OTP error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# REGISTER PAGE (TEMPLATE) - SUDAH BAGUS
# ============================================================
@app.route('/register', methods=['GET'])
def register_page():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

# ============================================================
# DASHBOARD PAGE
# ============================================================
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        # ===== STATISTIK LENGKAP =====
        # Orders
        total_orders = execute_query('SELECT COUNT(*) as count FROM orders WHERE user_id = ?', (user_id,), fetch_one=True)
        pending_orders = execute_query('SELECT COUNT(*) as count FROM orders WHERE user_id = ? AND status = "pending"', (user_id,), fetch_one=True)
        
        # Deposits
        total_deposit = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM deposits WHERE user_id = ? AND status = "approved"', (user_id,), fetch_one=True)
        
        # Withdraws
        total_withdraw = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM withdrawals WHERE user_id = ? AND status = "approved"', (user_id,), fetch_one=True)
        
        # Slot
        total_spins = execute_query('SELECT COUNT(*) as count FROM slot_history WHERE user_id = ?', (user_id,), fetch_one=True)
        total_wins = execute_query('SELECT COALESCE(SUM(win_amount), 0) as total FROM slot_history WHERE user_id = ? AND win_amount > 0', (user_id,), fetch_one=True)
        
        # Recent Orders (5 terakhir)
        recent_orders = execute_query('''
            SELECT * FROM orders 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 5
        ''', (user_id,), fetch_all=True) or []
        
        return render_template('dashboard.html',
            user=user,
            balance=user['balance'] if user else 0,
            total_orders=total_orders['count'] if total_orders else 0,
            pending_orders=pending_orders['count'] if pending_orders else 0,
            total_deposit=total_deposit['total'] if total_deposit else 0,
            total_withdraw=total_withdraw['total'] if total_withdraw else 0,
            total_spins=total_spins['count'] if total_spins else 0,
            total_wins=total_wins['total'] if total_wins else 0,
            orders=recent_orders,
            is_owner=user['is_owner'] if user else 0
        )
        
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('dashboard.html', 
            user=None, 
            balance=0,
            total_orders=0,
            pending_orders=0,
            total_deposit=0,
            total_withdraw=0,
            total_spins=0,
            total_wins=0,
            orders=[],
            is_owner=0,
            error='Gagal memuat dashboard'
        )

@app.route('/convert')
@login_required
def convert():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        # Get wallets
        wallets = execute_query('SELECT token_name, address, rate FROM wallet_settings WHERE is_active = 1 ORDER BY token_name', fetch_all=True) or []
        cryptos = [w['token_name'] for w in wallets] if wallets else ['USDT BEP-20', 'USDT TRC-20', 'USDT ERC-20', 'BTC', 'ETH', 'BNB', 'SOL', 'DOGE']
        banks = ['DANA', 'GOPAY', 'OVO', 'ShopeePay', 'BCA', 'BRI', 'BNI', 'Mandiri', 'SeaBank']
        
        # Get rate
        usd_rate = float(get_setting('usd_rate', 15500))
        
        return render_template('convert.html', 
            user=user,
            balance=user['balance'] if user else 0,
            cryptos=cryptos,
            banks=banks,
            usd_rate=usd_rate
        )
    except Exception as e:
        logger.error(f"Convert page error: {e}")
        return render_template('convert.html', error='Gagal memuat halaman convert')

@app.route('/api/convert', methods=['POST'])
@login_required
@maintenance_check('convert')
def api_convert():
    try:
        data = request.get_json()
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        crypto = data.get('crypto', 'USDT BEP-20')
        receive_type = data.get('receive_type', 'IDR')
        bank = data.get('bank', '')
        full_name = data.get('full_name', user['full_name'] or user['username'])
        account = data.get('account', '')
        amount_usd = float(data.get('amount_usd', 0))
        proof = data.get('proof', '')
        
        # ===== VALIDASI INPUT =====
        if not full_name:
            return jsonify({'success': False, 'error': 'Nama lengkap wajib diisi!'}), 400
        
        if not account:
            return jsonify({'success': False, 'error': 'Nomor rekening wajib diisi!'}), 400
        
        if not proof or not proof.startswith('data:image'):
            return jsonify({'success': False, 'error': 'Upload bukti transfer terlebih dahulu!'}), 400
        
        if len(proof) > 2_500_000:
            return jsonify({'success': False, 'error': 'Ukuran foto terlalu besar! Maksimal 2MB'}), 400
        
        if amount_usd < 0.1:
            return jsonify({'success': False, 'error': 'Minimal $0.1 USD'}), 400
        
        # ===== AMBIL RATE =====
        usd_rate = float(get_setting('usd_rate', 15500))
        
        # Cek wallet_settings
        try:
            wallet = execute_query('SELECT rate FROM wallet_settings WHERE token_name = ? AND is_active = 1', (crypto,), fetch_one=True)
            token_rate = wallet['rate'] if wallet else usd_rate
        except Exception as e:
            logger.error(f"Wallet rate error: {e}")
            token_rate = usd_rate
        
        # ===== AMBIL FEE =====
        try:
            fee_row = execute_query('''
                SELECT fee FROM fee_settings 
                WHERE ? >= min_amount AND ? <= max_amount 
                ORDER BY min_amount LIMIT 1
            ''', (amount_usd, amount_usd), fetch_one=True)
            
            if fee_row:
                fee_idr = float(fee_row['fee'])
            else:
                fee_idr = float(get_setting('withdraw_fee', 5000))
        except Exception as e:
            logger.error(f"Fee settings error: {e}")
            fee_idr = float(get_setting('withdraw_fee', 5000))
        
        # ===== HITUNG TOTAL =====
        total_idr = amount_usd * token_rate
        amount_idr = total_idr - fee_idr
        
        # ===== VALIDASI MINIMAL =====
        min_deposit = float(get_setting('min_deposit', 10000))
        if amount_idr < min_deposit:
            return jsonify({
                'success': False, 
                'error': f'Minimal penerimaan Rp {format_rupiah(min_deposit)}'
            }), 400
        
        if amount_idr <= 0:
            return jsonify({'success': False, 'error': 'Jumlah terlalu kecil setelah dipotong fee'}), 400
        
        # ===== GENERATE ORDER =====
        import random
        order_number = f"INV{random.randint(100000, 999999)}"
        
        # ===== SIMPAN ORDER =====
        try:
            execute_query('''
                INSERT INTO orders (
                    order_number, user_id, username, full_name, bank_name, 
                    account_number, amount_usd, amount_idr, fee_idr, 
                    photo_id, crypto_type, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            ''', (order_number, user_id, user['username'], full_name, bank, 
                  account, amount_usd, amount_idr, fee_idr, proof, crypto))
        except Exception as e:
            logger.error(f"Insert order error: {e}")
            return jsonify({'success': False, 'error': f'Gagal menyimpan order: {str(e)}'}), 500
        
        # ===== LOG =====
        log_transaction(user_id, 'order', amount_idr, f'Order {order_number} - {crypto}', order_number)
        
        # ===== NOTIFY OWNER =====
        try:
            owner_msg = (
                f"🆕 *ORDER BARU DARI WEB*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 ID: `{order_number}`\n"
                f"👤 User: @{user['username']} (ID: {user_id})\n"
                f"📛 Nama: {full_name}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💳 Detail Transaksi:\n"
                f"🪙 Crypto: {crypto}\n"
                f"💰 USD: ${amount_usd:.2f}\n"
                f"💵 Rate: Rp {token_rate:,.0f}/USD\n"
                f"💵 Total IDR: {format_rupiah(total_idr)}\n"
                f"📊 Fee Admin: {format_rupiah(fee_idr)}\n"
                f"💵 Total Diterima: {format_rupiah(amount_idr)}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🏦 Bank: {bank}\n"
                f"📱 Rekening: `{account}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⏳ Status: Menunggu konfirmasi owner"
            )
            
            # Kirim foto ke Telegram
            if proof and proof.startswith('data:image'):
                try:
                    send_telegram_photo(OWNER_ID, proof, owner_msg)
                except Exception as e:
                    logger.error(f"Telegram photo error: {e}")
                    send_telegram_message(OWNER_ID, owner_msg + "\n\n⚠️ Foto tidak terkirim!")
            else:
                send_telegram_message(OWNER_ID, owner_msg)
        except Exception as e:
            logger.error(f"Telegram notification error: {e}")
        
        # ===== NOTIFY GROUP =====
        try:
            group_msg = (
                f"🆕 *ORDER MASUK!*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 ID: `{order_number}`\n"
                f"👤 User: @{user['username']}\n"
                f"💰 Jumlah: {format_rupiah(amount_idr)}\n"
                f"🏦 Bank: {bank}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"⏳ Status: Menunggu konfirmasi"
            )
            send_telegram_message(GROUP_CHAT_ID, group_msg)
        except:
            pass
        
        # ===== RESPONSE =====
        return jsonify({
            'success': True,
            'order_number': order_number,
            'amount_idr': amount_idr,
            'fee_idr': fee_idr,
            'amount_usd': amount_usd,
            'total_idr': total_idr,
            'crypto': crypto,
            'receive_type': receive_type,
            'bank': bank,
            'full_name': full_name,
            'account': account,
            'rate': token_rate,
            'usd_rate': usd_rate
        })
        
    except Exception as e:
        logger.error(f"Convert API error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# API DEPOSIT - LENGKAP
# ============================================================

@app.route('/api/deposit', methods=['POST'])
@login_required
@maintenance_check('deposit')
def api_deposit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Data tidak ditemukan'}), 400
            
        user_id = session['user_id']
        
        # Ambil data user
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User tidak ditemukan'}), 404
        
        # Ambil data dari request
        amount = float(data.get('amount', 0))
        proof = data.get('proof', '')
        method = data.get('method', 'DANA')
        
        # Validasi amount
        if amount <= 0:
            return jsonify({'success': False, 'error': 'Nominal deposit harus lebih dari 0'}), 400
        
        # Validasi minimal deposit
        min_deposit = float(get_setting('min_deposit', 10000))
        if amount < min_deposit:
            return jsonify({
                'success': False, 
                'error': f'Minimal deposit {format_rupiah(min_deposit)}'
            }), 400
        
        # Validasi bukti transfer
        if not proof:
            return jsonify({
                'success': False, 
                'error': 'Upload bukti transfer terlebih dahulu!'
            }), 400
            
        if not proof.startswith('data:image'):
            return jsonify({
                'success': False, 
                'error': 'Format bukti transfer tidak valid!'
            }), 400
        
        # Validasi ukuran foto (maks 2MB)
        if len(proof) > 2_500_000:
            return jsonify({
                'success': False, 
                'error': 'Ukuran foto terlalu besar! Maksimal 2MB'
            }), 400
        
        # Generate nomor deposit
        import random
        from datetime import datetime
        dep_number = f"DEP{random.randint(100000, 999999)}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Simpan ke database
        execute_query('''
            INSERT INTO deposits (
                dep_number, user_id, username, full_name, 
                amount, method, photo_id, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        ''', (
            dep_number, 
            user_id, 
            user['username'], 
            user['full_name'], 
            amount, 
            method, 
            proof,
            timestamp
        ))
        
        # Log transaksi
        log_transaction(user_id, 'deposit', amount, f'Deposit {dep_number}', dep_number)
        
        # Kirim notifikasi Telegram (dengan foto)
        try:
            send_telegram_photo(
                OWNER_ID,
                proof,
                f"📥 *DEPOSIT BARU*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 ID: {dep_number}\n"
                f"👤 User: @{user['username']}\n"
                f"👤 Nama: {user['full_name']}\n"
                f"💰 Nominal: {format_rupiah(amount)}\n"
                f"📱 Metode: {method}\n"
                f"🕐 Waktu: {timestamp}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"⏳ Status: Menunggu konfirmasi"
            )
        except Exception as e:
            logger.error(f"Telegram notif error: {e}")
        
        return jsonify({
            'success': True, 
            'dep_number': dep_number,
            'message': 'Deposit berhasil diajukan!'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False, 
            'error': 'Nominal deposit tidak valid'
        }), 400
    except Exception as e:
        logger.error(f"Deposit API error: {e}")
        return jsonify({
            'success': False, 
            'error': 'Terjadi kesalahan pada server'
        }), 500 

@app.route('/api/withdraw', methods=['POST'])
@login_required
@maintenance_check('withdraw')
def api_withdraw():
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Ambil data user
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User tidak ditemukan'}), 404
        
        # Ambil data dari request
        amount = float(data.get('amount', 0))
        method = data.get('method', 'DANA')
        full_name = data.get('full_name', '').strip()
        destination = data.get('destination', '').strip()
        note = data.get('note', '').strip()
        fee = float(data.get('fee', 5000))
        
        # Validasi nominal
        if amount <= 0:
            return jsonify({'success': False, 'error': 'Nominal withdraw harus lebih dari 0'}), 400
        
        min_withdraw = float(get_setting('min_withdraw', 50000))
        if amount < min_withdraw:
            return jsonify({
                'success': False, 
                'error': f'Minimal withdraw {format_rupiah(min_withdraw)}'
            }), 400
        
        if not full_name or len(full_name) < 3:
            return jsonify({'success': False, 'error': 'Nama penerima wajib diisi (minimal 3 karakter)'}), 400
        
        if not destination or len(destination) < 5:
            return jsonify({'success': False, 'error': 'Nomor tujuan wajib diisi (minimal 5 karakter)'}), 400
        
        total_deduct = amount + fee
        if total_deduct > user['balance']:
            return jsonify({
                'success': False, 
                'error': f'Saldo tidak cukup! Saldo: {format_rupiah(user["balance"])}'
            }), 400
        
        # Generate nomor withdraw
        import random
        from datetime import datetime
        wd_number = f"WD{random.randint(100000, 999999)}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Kurangi saldo user
        execute_query('UPDATE users SET balance = balance - ? WHERE id = ?', (total_deduct, user_id))
        
        # Simpan ke database
        execute_query('''
            INSERT INTO withdrawals (
                wd_number, user_id, username, full_name, 
                destination, amount, fee, method, note, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        ''', (
            wd_number,
            user_id,
            user['username'],
            full_name,
            destination,
            amount,
            fee,
            method,
            note,
            timestamp
        ))
        
        # Log transaksi
        log_transaction(user_id, 'withdraw', amount, f'Withdraw {wd_number} - {method}', wd_number)
        
        # Kirim notifikasi Telegram
        try:
            msg = (
                f"📤 *WITHDRAW BARU DARI WEB*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 ID: `{wd_number}`\n"
                f"👤 User: @{user['username']} (ID: {user_id})\n"
                f"📛 Nama: {full_name}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💳 Detail Transaksi:\n"
                f"💰 Nominal: {format_rupiah(amount)}\n"
                f"📊 Fee Admin: {format_rupiah(fee)}\n"
                f"💵 Total Diterima: {format_rupiah(amount - fee)}\n"
                f"📱 Metode: {method}\n"
                f"📱 Tujuan: `{destination}`\n"
                f"📝 Catatan: {note or '-'}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⏳ Status: Menunggu konfirmasi owner"
            )
            send_telegram_message(OWNER_ID, msg)
        except Exception as e:
            logger.error(f"Telegram notif error: {e}")
        
        return jsonify({
            'success': True,
            'wd_number': wd_number,
            'message': 'Withdraw berhasil diajukan!'
        })
        
    except Exception as e:
        logger.error(f"Withdraw API error: {e}")
        return jsonify({
            'success': False,
            'error': 'Terjadi kesalahan pada server'
        }), 500

# ============================================================
# SLOT GAMES PAGE
# ============================================================
@app.route('/slot')
@login_required
def slot():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        # Statistik Slot
        total_spins = execute_query('SELECT COUNT(*) as count FROM slot_games WHERE user_id = ?', (user_id,), fetch_one=True)['count'] or 0
        total_wins = execute_query('SELECT COALESCE(SUM(win), 0) as total FROM slot_games WHERE user_id = ?', (user_id,), fetch_one=True)['total'] or 0
        total_bets = execute_query('SELECT COALESCE(SUM(bet), 0) as total FROM slot_games WHERE user_id = ?', (user_id,), fetch_one=True)['total'] or 0
        total_losses = execute_query('SELECT COALESCE(SUM(bet - win), 0) as total FROM slot_games WHERE user_id = ? AND win < bet', (user_id,), fetch_one=True)['total'] or 0
        win_rate = round((total_wins / total_bets * 100) if total_bets > 0 else 0, 2)
        
        # Riwayat Slot Terbaru
        recent_games = execute_query('''
            SELECT * FROM slot_games 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 10
        ''', (user_id,), fetch_all=True)
        
        # Game Populer
        popular_games = execute_query('''
            SELECT game_name, COUNT(*) as plays, SUM(bet) as total_bet, SUM(win) as total_win
            FROM slot_games 
            WHERE user_id = ?
            GROUP BY game_name 
            ORDER BY plays DESC 
            LIMIT 5
        ''', (user_id,), fetch_all=True)
        
        return render_template('slot.html',
            user=user,
            balance=user['balance'] if user else 0,
            total_spins=total_spins,
            total_wins=total_wins,
            total_bets=total_bets,
            total_losses=total_losses,
            win_rate=win_rate,
            recent_games=recent_games,
            popular_games=popular_games
        )
    except Exception as e:
        logger.error(f"Slot page error: {e}")
        return render_template('slot.html', 
            user=None, 
            balance=0,
            total_spins=0,
            total_wins=0,
            total_bets=0,
            total_losses=0,
            win_rate=0,
            recent_games=[],
            popular_games=[],
            error='Gagal memuat halaman Slot'
        )

# ============================================================
# API SLOT - SPIN
# ============================================================
@app.route('/api/slot/spin', methods=['POST'])
@login_required
def api_slot_spin():
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        game_name = data.get('game_name', 'Classic Slot')
        bet = float(data.get('bet', 0))
        
        # Validasi
        if bet <= 0:
            return jsonify({'success': False, 'error': 'Bet harus lebih dari 0!'}), 400
        
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User tidak ditemukan!'}), 404
        
        if user['balance'] < bet:
            return jsonify({'success': False, 'error': 'Saldo tidak mencukupi!'}), 400
        
        # Random hasil spin
        import random
        symbols = ['🍒', '🍋', '🍊', '🍇', '🔔', '💎', '7️⃣', '⭐']
        
        # Hitung win (random dengan RTP ~85%)
        win = 0
        result = []
        is_win = False
        
        # Generate 3 simbol
        for i in range(3):
            result.append(random.choice(symbols))
        
        # Cek kombinasi menang
        if result[0] == result[1] == result[2]:
            # Jackpot!
            multiplier = 10 if result[0] == '7️⃣' else 5 if result[0] == '💎' else 3
            win = bet * multiplier
            is_win = True
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            # 2 sama
            win = bet * 1.5
            is_win = True
        else:
            # Kalah
            win = 0
            is_win = False
        
        # Bonus random (5% chance)
        if random.random() < 0.05 and not is_win:
            win = bet * 2
            is_win = True
        
        # Update saldo user
        new_balance = user['balance'] - bet + win
        execute_query('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
        
        # Simpan ke database
        execute_query('''
            INSERT INTO slot_games (user_id, username, game_name, bet, win, result, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, user['username'], game_name, bet, win, ' | '.join(result), 'approved' if is_win else 'lost'))
        
        # Log transaksi
        if is_win:
            log_transaction(user_id, 'slot_win', win, f'Menang slot {game_name}', f'SLOT-{random.randint(100000, 999999)}')
        else:
            log_transaction(user_id, 'slot_loss', bet, f'Kalah slot {game_name}', f'SLOT-{random.randint(100000, 999999)}')
        
        return jsonify({
            'success': True,
            'data': {
                'result': result,
                'win': win,
                'is_win': is_win,
                'bet': bet,
                'new_balance': new_balance,
                'game_name': game_name
            }
        })
        
    except Exception as e:
        logger.error(f"Slot spin error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# API SLOT - HISTORY
# ============================================================
@app.route('/api/slot/history')
@login_required
def api_slot_history():
    try:
        user_id = session['user_id']
        limit = request.args.get('limit', 20, type=int)
        
        history = execute_query('''
            SELECT * FROM slot_games 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit), fetch_all=True)
        
        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        logger.error(f"Slot history error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# API SLOT - STATS
# ============================================================
@app.route('/api/slot/stats')
@login_required
def api_slot_stats():
    try:
        user_id = session['user_id']
        
        total_spins = execute_query('SELECT COUNT(*) as count FROM slot_games WHERE user_id = ?', (user_id,), fetch_one=True)['count'] or 0
        total_wins = execute_query('SELECT COALESCE(SUM(win), 0) as total FROM slot_games WHERE user_id = ?', (user_id,), fetch_one=True)['total'] or 0
        total_bets = execute_query('SELECT COALESCE(SUM(bet), 0) as total FROM slot_games WHERE user_id = ?', (user_id,), fetch_one=True)['total'] or 0
        win_count = execute_query('SELECT COUNT(*) as count FROM slot_games WHERE user_id = ? AND win > 0', (user_id,), fetch_one=True)['count'] or 0
        win_rate = round((win_count / total_spins * 100) if total_spins > 0 else 0, 2)
        
        # Game paling sering dimainkan
        top_games = execute_query('''
            SELECT game_name, COUNT(*) as plays, SUM(win) as total_win
            FROM slot_games 
            WHERE user_id = ?
            GROUP BY game_name 
            ORDER BY plays DESC 
            LIMIT 3
        ''', (user_id,), fetch_all=True)
        
        return jsonify({
            'success': True,
            'data': {
                'total_spins': total_spins,
                'total_wins': total_wins,
                'total_bets': total_bets,
                'win_count': win_count,
                'win_rate': win_rate,
                'top_games': top_games
            }
        })
    except Exception as e:
        logger.error(f"Slot stats error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# API SLOT - LEADERBOARD
# ============================================================
@app.route('/api/slot/leaderboard')
def api_slot_leaderboard():
    try:
        leaderboard = execute_query('''
            SELECT 
                u.username,
                u.full_name,
                COUNT(s.id) as total_spins,
                SUM(s.win) as total_wins,
                SUM(s.bet) as total_bets,
                ROUND((SUM(s.win) / NULLIF(SUM(s.bet), 0) * 100), 2) as win_rate
            FROM slot_games s
            JOIN users u ON s.user_id = u.id
            WHERE s.status = 'approved'
            GROUP BY s.user_id
            ORDER BY total_wins DESC
            LIMIT 10
        ''', fetch_all=True)
        
        return jsonify({
            'success': True,
            'data': leaderboard
        })
    except Exception as e:
        logger.error(f"Slot leaderboard error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# INVESTASI PAGE ROUTE - OPTIMIZED
# ============================================================

@app.route('/investasi')
@login_required
def investasi():
    try:
        user_id = session['user_id']
        
        # ===== 1. AMBIL USER (1 QUERY) =====
        user = execute_query('SELECT id, username, full_name, balance FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        if not user:
            flash('User tidak ditemukan!', 'danger')
            return redirect(url_for('logout'))
        
        # ===== 2. AMBIL SETTINGS (PAKAI get_setting DENGAN DEFAULT) =====
        min_invest = float(get_setting('investasi_min', 50000))
        max_invest = float(get_setting('investasi_max', 10000000))
        profit_percent = float(get_setting('investasi_profit', 50))
        duration_hours = float(get_setting('investasi_duration', 24))
        is_active = int(get_setting('investasi_is_active', 1))
        
        # ===== 3. AMBIL INVESTASI AKTIF (1 QUERY) =====
        active_investasi = execute_query('''
            SELECT id, modal, profit, total_return, profit_percent,
                   duration_hours, start_time, end_time, status
            FROM investasi 
            WHERE user_id = ? AND status = 'active'
            ORDER BY id DESC LIMIT 1
        ''', (user_id,), fetch_one=True)
        
        # ===== 4. CEK APAKAH INVESTASI SUDAH SELESAI =====
        from datetime import datetime
        
        if active_investasi and active_investasi.get('end_time'):
            try:
                end_time = datetime.strptime(active_investasi['end_time'], '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                
                if now >= end_time:
                    # Complete investasi (1 transaksi)
                    execute_query('''
                        UPDATE investasi 
                        SET status = 'completed', last_update = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    ''', (active_investasi['id'],))
                    
                    execute_query('''
                        UPDATE users SET balance = balance + ? 
                        WHERE id = ?
                    ''', (active_investasi['total_return'], user_id))
                    
                    log_transaction(
                        user_id, 
                        'investasi_return', 
                        active_investasi['total_return'], 
                        f'Investasi return {active_investasi["id"]}'
                    )
                    
                    active_investasi = None
            except Exception as e:
                logger.error(f"Investasi check error: {e}")
                active_investasi = None
        
        # ===== 5. AMBIL HISTORY (1 QUERY) =====
        history = execute_query('''
            SELECT id, modal, profit, total_return, profit_percent,
                   duration_hours, start_time, end_time, status
            FROM investasi 
            WHERE user_id = ? 
            ORDER BY id DESC 
            LIMIT 20
        ''', (user_id,), fetch_all=True) or []
        
        # ===== 6. HITUNG STATISTIK (1 QUERY) =====
        stats = execute_query('''
            SELECT 
                COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
                COALESCE(SUM(CASE WHEN status = 'completed' THEN profit ELSE 0 END), 0) as total_profit
            FROM investasi 
            WHERE user_id = ?
        ''', (user_id,), fetch_one=True)
        
        active_count = stats['active_count'] if stats else 0
        total_profit = stats['total_profit'] if stats else 0
        
        # ===== 7. DATA UNTUK JAVASCRIPT =====
        active_investasi_data = None
        if active_investasi:
            active_investasi_data = {
                'id': active_investasi['id'],
                'modal': active_investasi['modal'],
                'profit': active_investasi['profit'],
                'total_return': active_investasi['total_return'],
                'profit_percent': active_investasi.get('profit_percent', profit_percent),
                'duration_hours': active_investasi.get('duration_hours', duration_hours),
                'start_time': active_investasi.get('start_time'),
                'end_time': active_investasi.get('end_time'),
                'status': active_investasi.get('status')
            }
        
        # ===== 8. SETTINGS UNTUK TEMPLATE =====
        settings = {
            'min_invest': min_invest,
            'max_invest': max_invest,
            'profit_percent': profit_percent,
            'duration_hours': duration_hours,
            'is_active': is_active
        }
        
        return render_template('investasi.html',
            user=user,
            balance=user['balance'] if user else 0,
            settings=settings,
            active_investasi=active_investasi,
            active_investasi_data=active_investasi_data,
            investasi_list=history,
            active_count=active_count,
            total_profit=total_profit,
            min_invest=min_invest,
            max_invest=max_invest,
            profit_percent=profit_percent,
            duration_hours=duration_hours,
            is_active=is_active
        )
        
    except Exception as e:
        logger.error(f"Investasi page error: {e}")
        import traceback
        traceback.print_exc()
        
        # Default settings
        default_settings = {
            'min_invest': 50000,
            'max_invest': 10000000,
            'profit_percent': 50,
            'duration_hours': 24,
            'is_active': 1
        }
        
        return render_template('investasi.html',
            error='Gagal memuat halaman investasi',
            user=None,
            balance=0,
            settings=default_settings,
            active_investasi=None,
            active_investasi_data=None,
            investasi_list=[],
            active_count=0,
            total_profit=0,
            min_invest=50000,
            max_invest=10000000,
            profit_percent=50,
            duration_hours=24,
            is_active=1
        )


# ============================================================
# API INVESTASI START - OPTIMIZED
# ============================================================

@app.route('/api/investasi/start', methods=['POST'])
@login_required
@maintenance_check('investasi')
def api_investasi_start():
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Ambil user
        user = execute_query('SELECT id, username, full_name, balance FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        amount = float(data.get('amount', 0))
        
        # Ambil settings
        min_invest = float(get_setting('investasi_min', 50000))
        max_invest = float(get_setting('investasi_max', 10000000))
        profit_percent = float(get_setting('investasi_profit', 50))
        duration = float(get_setting('investasi_duration', 24))
        is_active = int(get_setting('investasi_is_active', 1))
        
        # Validasi
        if is_active == 0:
            return jsonify({'success': False, 'error': 'Fitur investasi sedang tidak aktif!'}), 400
        
        if amount < min_invest:
            return jsonify({
                'success': False, 
                'error': f'Minimal investasi {format_rupiah(min_invest)}'
            }), 400
        
        if amount > max_invest:
            return jsonify({
                'success': False, 
                'error': f'Maksimal investasi {format_rupiah(max_invest)}'
            }), 400
        
        if user['balance'] < amount:
            return jsonify({
                'success': False, 
                'error': f'Saldo tidak cukup! Saldo: {format_rupiah(user["balance"])}'
            }), 400
        
        # Cek investasi aktif
        active = execute_query('''
            SELECT id FROM investasi 
            WHERE user_id = ? AND status = 'active'
        ''', (user_id,), fetch_one=True)
        
        if active:
            return jsonify({
                'success': False, 
                'error': 'Anda memiliki investasi aktif! Tunggu hingga selesai.'
            }), 400
        
        # Hitung
        profit = amount * profit_percent / 100
        total_return = amount + profit
        
        # ===== INSERT DENGAN SEMUA KOLOM =====
        execute_query('''
            INSERT INTO investasi (
                user_id, username, full_name, 
                modal, profit, total_return, 
                profit_percent, duration_hours,
                start_time, end_time, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now', '+' || ? || ' hours'), 'active')
        ''', (
            user_id, user['username'], user['full_name'], 
            amount, profit, total_return,
            profit_percent, duration,
            duration
        ))
        
        # Kurangi saldo
        execute_query('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
        
        # Log
        log_transaction(user_id, 'investasi_start', amount, f'Investasi {amount} ({profit_percent}%)', 'investasi')
        
        return jsonify({
            'success': True,
            'message': f'Investasi berhasil dimulai! Profit {profit_percent}% dalam {duration} jam.',
            'profit': profit,
            'total_return': total_return,
            'duration': duration,
            'profit_percent': profit_percent
        })
        
    except Exception as e:
        logger.error(f"Investasi start error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# API INVESTASI STATUS - OPTIMIZED
# ============================================================

@app.route('/api/investasi/status')
@login_required
def api_investasi_status():
    try:
        user_id = session['user_id']
        
        investasi = execute_query('''
            SELECT id, modal, profit, total_return, profit_percent,
                   duration_hours, start_time, end_time, status
            FROM investasi 
            WHERE user_id = ? AND status = 'active'
            ORDER BY id DESC LIMIT 1
        ''', (user_id,), fetch_one=True)
        
        if not investasi:
            return jsonify({'success': True, 'active': False, 'completed': False})
        
        from datetime import datetime
        
        # Cek jika end_time NULL
        if not investasi.get('end_time'):
            return jsonify({
                'success': True,
                'active': True,
                'id': investasi['id'],
                'modal': investasi['modal'],
                'profit': investasi['profit'],
                'total_return': investasi['total_return'],
                'progress': 0,
                'duration_hours': investasi.get('duration_hours', 24)
            })
        
        end_time = datetime.strptime(investasi['end_time'], '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        
        # Cek selesai
        if now >= end_time:
            execute_query('''
                UPDATE investasi 
                SET status = 'completed', last_update = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (investasi['id'],))
            
            execute_query('''
                UPDATE users SET balance = balance + ? 
                WHERE id = ?
            ''', (investasi['total_return'], user_id))
            
            log_transaction(
                user_id, 
                'investasi_return', 
                investasi['total_return'], 
                f'Investasi return {investasi["id"]}'
            )
            
            return jsonify({
                'success': True,
                'active': False,
                'completed': True,
                'total_return': investasi['total_return']
            })
        
        # Hitung progress
        start_time = datetime.strptime(investasi['start_time'], '%Y-%m-%d %H:%M:%S')
        total_duration = (end_time - start_time).total_seconds()
        elapsed = (now - start_time).total_seconds()
        progress = min(100, (elapsed / total_duration) * 100) if total_duration > 0 else 0
        
        current_profit = (progress / 100) * investasi['profit']
        
        return jsonify({
            'success': True,
            'active': True,
            'id': investasi['id'],
            'modal': investasi['modal'],
            'profit': investasi['profit'],
            'current_profit': round(current_profit, 2),
            'total_return': investasi['total_return'],
            'current_return': investasi['modal'] + round(current_profit, 2),
            'progress': round(progress, 1),
            'end_time': investasi['end_time'],
            'start_time': investasi['start_time'],
            'duration_hours': investasi.get('duration_hours', 24)
        })
        
    except Exception as e:
        logger.error(f"Investasi status error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
# API INVESTASI HISTORY - TAMBAHAN
# ============================================================

@app.route('/api/investasi/history')
@login_required
def api_investasi_history():
    try:
        user_id = session['user_id']
        
        history = execute_query('''
            SELECT id, modal, profit, total_return, profit_percent,
                   status, start_time, end_time
            FROM investasi 
            WHERE user_id = ? 
            ORDER BY id DESC 
            LIMIT 20
        ''', (user_id,), fetch_all=True) or []
        
        total_invested = execute_query('''
            SELECT COALESCE(SUM(modal), 0) as total 
            FROM investasi 
            WHERE user_id = ? AND status = 'completed'
        ''', (user_id,), fetch_one=True)
        
        total_profit = execute_query('''
            SELECT COALESCE(SUM(profit), 0) as total 
            FROM investasi 
            WHERE user_id = ? AND status = 'completed'
        ''', (user_id,), fetch_one=True)
        
        return jsonify({
            'success': True,
            'history': history,
            'total_invested': total_invested['total'] if total_invested else 0,
            'total_profit': total_profit['total'] if total_profit else 0
        })
        
    except Exception as e:
        logger.error(f"Investasi history error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/referral')
@login_required
def referral():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        if not user:
            return redirect(url_for('login'))
        
        referrals = execute_query('''
            SELECT r.*, u.username, u.full_name, u.joined_at 
            FROM referrals r 
            JOIN users u ON r.referred_id = u.id 
            WHERE r.user_id = ?
            ORDER BY r.created_at DESC
        ''', (user_id,), fetch_all=True) or []
        
        ref_count = len(referrals)
        ref_earnings = sum(r['commission'] for r in referrals) if referrals else 0
        
        referral_code = user['id']
        referral_bonus = float(get_setting('referral_bonus', 400))
        
        return render_template('referral.html',
            user=user,
            referral_code=referral_code,
            ref_count=ref_count,
            ref_earnings=ref_earnings,
            referred_users=referrals,
            referral_bonus=referral_bonus,
            balance=user['balance'] if user else 0
        )
    except Exception as e:
        logger.error(f"Referral page error: {e}")
        return render_template('referral.html', error='Gagal memuat halaman referral')

@app.route('/claim-referral-bonus', methods=['POST'])
@login_required
def claim_referral_bonus():
    try:
        user_id = session['user_id']
        
        referrals = execute_query('''
            SELECT COALESCE(SUM(commission), 0) as total 
            FROM referrals 
            WHERE user_id = ?
        ''', (user_id,), fetch_one=True)
        
        total = referrals['total'] if referrals else 0
        
        if total < 10000:
            return jsonify({'success': False, 'message': 'Minimal bonus Rp 10.000'})
        
        execute_query('UPDATE users SET balance = balance + ? WHERE id = ?', (total, user_id))
        execute_query('UPDATE referrals SET commission = 0 WHERE user_id = ?', (user_id,))
        
        # Log
        log_transaction(user_id, 'referral_claim', total, 'Claim referral bonus')
        
        return jsonify({'success': True, 'message': f'Bonus {format_rupiah(total)} berhasil diklaim!'})
        
    except Exception as e:
        logger.error(f"Claim referral error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/history')
@login_required
def history():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        # Get all transactions
        orders = execute_query('''
            SELECT 'order' as type, order_number as ref_id, amount_idr as amount, 
                   status, created_at, crypto_type as description, amount_usd
            FROM orders WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 50
        ''', (user_id,), fetch_all=True) or []
        
        deposits = execute_query('''
            SELECT 'deposit' as type, dep_number as ref_id, amount, 
                   status, created_at, method as description
            FROM deposits WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 50
        ''', (user_id,), fetch_all=True) or []
        
        withdrawals = execute_query('''
            SELECT 'withdraw' as type, wd_number as ref_id, amount, 
                   status, created_at, destination as description
            FROM withdrawals WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 50
        ''', (user_id,), fetch_all=True) or []
        
        slots = execute_query('''
            SELECT 'slot' as type, id as ref_id, bet_amount as amount, 
                   'completed' as status, created_at, 
                   CASE WHEN win_amount > 0 THEN 'Menang' ELSE 'Kalah' END as description
            FROM slot_history WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 50
        ''', (user_id,), fetch_all=True) or []
        
        # Combine and sort
        transactions = orders + deposits + withdrawals + slots
        transactions.sort(key=lambda x: x['created_at'], reverse=True)
        
        status_map = {
            'pending': '⏳ Pending',
            'approved': '✅ Selesai',
            'completed': '✅ Selesai',
            'rejected': '❌ Ditolak',
            'cancelled': '❌ Dibatalkan',
            'processing': '🔄 Diproses'
        }
        
        return render_template('history.html',
            user=user,
            transactions=transactions[:20],
            status_map=status_map,
            balance=user['balance'] if user else 0
        )
    except Exception as e:
        logger.error(f"History page error: {e}")
        return render_template('history.html', error='Gagal memuat history')

@app.route('/reviews')
@login_required
def reviews():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        approved_reviews = execute_query('''
            SELECT * FROM reviews WHERE is_approved = 1 
            ORDER BY created_at DESC LIMIT 50
        ''', fetch_all=True) or []
        
        user_review = execute_query('SELECT * FROM reviews WHERE user_id = ?', (user_id,), fetch_one=True)
        
        return render_template('reviews.html',
            user=user,
            reviews=approved_reviews,
            user_review=user_review,
            balance=user['balance'] if user else 0
        )
    except Exception as e:
        logger.error(f"Reviews page error: {e}")
        return render_template('reviews.html', error='Gagal memuat reviews')

@app.route('/api/reviews/submit', methods=['POST'])
@login_required
@maintenance_check('reviews')
def api_submit_review():
    try:
        data = request.get_json()
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        rating = data.get('rating')
        review_text = data.get('review_text', '').strip()
        
        if not rating or not review_text:
            return jsonify({'success': False, 'error': 'Rating dan ulasan wajib diisi!'})
        
        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'error': 'Rating harus 1-5!'})
        
        if len(review_text) < 10:
            return jsonify({'success': False, 'error': 'Ulasan minimal 10 karakter!'})
        
        existing = execute_query('SELECT * FROM reviews WHERE user_id = ?', (user_id,), fetch_one=True)
        if existing:
            return jsonify({'success': False, 'error': 'Anda sudah memberikan review!'})
        
        execute_query('''
            INSERT INTO reviews (user_id, username, full_name, rating, review_text, is_approved)
            VALUES (?, ?, ?, ?, ?, 0)
        ''', (user_id, user['username'], user['full_name'], rating, review_text))
        
        # Notify
        send_telegram_message(
            OWNER_ID,
            f"⭐ *REVIEW BARU!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 User: @{user['username']}\n"
            f"📝 Rating: {'⭐' * rating} ({rating}/5)\n"
            f"💬 Ulasan: {review_text[:100]}...\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏳ Menunggu approval owner"
        )
        
        return jsonify({'success': True, 'message': 'Review berhasil dikirim! Tunggu approval owner.'})
        
    except Exception as e:
        logger.error(f"Submit review error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/user')
@login_required
def get_user():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT id, username, email, full_name, balance, is_owner FROM users WHERE id = ?', (user_id,), fetch_one=True)
        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'balance': user['balance'] or 0,
            'is_owner': user['is_owner'] or 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings')
@login_required
def get_settings():
    try:
        settings = execute_query('SELECT * FROM settings', fetch_all=True) or []
        return jsonify({row['key']: row['value'] for row in settings})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/stats')
@login_required
def api_dashboard_stats():
    try:
        user_id = session['user_id']
        
        total_orders = execute_query('SELECT COUNT(*) as count FROM orders WHERE user_id = ?', (user_id,), fetch_one=True)
        pending_orders = execute_query('SELECT COUNT(*) as count FROM orders WHERE user_id = ? AND status = "pending"', (user_id,), fetch_one=True)
        total_deposit = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM deposits WHERE user_id = ? AND status = "approved"', (user_id,), fetch_one=True)
        total_withdraw = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM withdrawals WHERE user_id = ? AND status = "approved"', (user_id,), fetch_one=True)
        total_spins = execute_query('SELECT COUNT(*) as count FROM slot_history WHERE user_id = ?', (user_id,), fetch_one=True)
        total_wins = execute_query('SELECT COALESCE(SUM(win_amount), 0) as total FROM slot_history WHERE user_id = ? AND win_amount > 0', (user_id,), fetch_one=True)
        
        return jsonify({
            'total_orders': total_orders['count'] if total_orders else 0,
            'pending_orders': pending_orders['count'] if pending_orders else 0,
            'total_deposit': total_deposit['total'] if total_deposit else 0,
            'total_withdraw': total_withdraw['total'] if total_withdraw else 0,
            'total_spins': total_spins['count'] if total_spins else 0,
            'total_wins': total_wins['total'] if total_wins else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
@owner_required
def admin_panel():
    try:
        user_id = session.get('user_id')
        print(f"🔍 Admin panel: user_id={user_id}")
        
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        print(f"🔍 User data: {user}")
        
        if not user:
            flash('User tidak ditemukan!', 'danger')
            return redirect(url_for('logout'))
        
        # Stats
        total_users = execute_query('SELECT COUNT(*) as count FROM users', fetch_one=True)
        total_orders = execute_query('SELECT COUNT(*) as count FROM orders', fetch_one=True)
        pending_orders = execute_query('SELECT COUNT(*) as count FROM orders WHERE status = "pending"', fetch_one=True)
        total_deposits = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM deposits WHERE status = "approved"', fetch_one=True)
        total_withdraws = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM withdrawals WHERE status = "approved"', fetch_one=True)
        total_reviews = execute_query('SELECT COUNT(*) as count FROM reviews WHERE is_approved = 1', fetch_one=True)
        total_slots = execute_query('SELECT COUNT(*) as count FROM slot_history', fetch_one=True)
        
        # Recent data
        recent_orders = execute_query('''
            SELECT o.*, u.username, u.full_name 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            ORDER BY o.created_at DESC LIMIT 20
        ''', fetch_all=True) or []
        
        recent_deposits = execute_query('''
            SELECT d.*, u.username, u.full_name 
            FROM deposits d 
            JOIN users u ON d.user_id = u.id 
            WHERE d.status = 'pending' 
            ORDER BY d.created_at DESC LIMIT 20
        ''', fetch_all=True) or []
        
        recent_withdraws = execute_query('''
            SELECT w.*, u.username, u.full_name 
            FROM withdrawals w 
            JOIN users u ON w.user_id = u.id 
            WHERE w.status = 'pending' 
            ORDER BY w.created_at DESC LIMIT 20
        ''', fetch_all=True) or []
        
        pending_reviews = execute_query('''
            SELECT r.*, u.username, u.full_name 
            FROM reviews r 
            JOIN users u ON r.user_id = u.id 
            WHERE r.is_approved = 0 
            ORDER BY r.created_at DESC LIMIT 20
        ''', fetch_all=True) or []
        
        # Settings
        settings = execute_query('SELECT * FROM settings', fetch_all=True) or []
        settings_dict = {row['key']: row['value'] for row in settings}
        
        # Wallets
        wallets = execute_query('SELECT * FROM wallet_settings ORDER BY token_name', fetch_all=True) or []
        
        # Fees
        fees = execute_query('SELECT * FROM fee_settings ORDER BY min_amount', fetch_all=True) or []
        
        # Maintenance
        maintenance = execute_query('SELECT * FROM maintenance_settings ORDER BY feature', fetch_all=True) or []
        
        return render_template('admin.html',
            user=user,
            total_users=total_users['count'] if total_users else 0,
            total_orders=total_orders['count'] if total_orders else 0,
            pending_orders=pending_orders['count'] if pending_orders else 0,
            total_deposits=total_deposits['total'] if total_deposits else 0,
            total_withdraws=total_withdraws['total'] if total_withdraws else 0,
            total_reviews=total_reviews['count'] if total_reviews else 0,
            total_slots=total_slots['count'] if total_slots else 0,
            recent_orders=recent_orders,
            recent_deposits=recent_deposits,
            recent_withdraws=recent_withdraws,
            pending_reviews=pending_reviews,
            settings=settings_dict,
            wallets=wallets,
            fees=fees,
            maintenance=maintenance,
            balance=user['balance'] if user else 0
        )
    except Exception as e:
        logger.error(f"Admin panel error: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

# ===== ADMIN API ROUTES =====

@app.route('/api/admin/settings', methods=['POST'])
@login_required
@owner_required
def api_admin_settings():
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        for key, value in data.items():
            execute_query('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
        
        logger.info(f"Settings updated by admin {session.get('username')}")
        return jsonify({'success': True, 'message': 'Settings updated!'})
    except Exception as e:
        logger.error(f"Admin settings error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/stats')
@login_required
@owner_required
def api_admin_stats():
    try:
        total_users = execute_query('SELECT COUNT(*) as count FROM users', fetch_one=True)
        total_orders = execute_query('SELECT COUNT(*) as count FROM orders', fetch_one=True)
        pending_orders = execute_query('SELECT COUNT(*) as count FROM orders WHERE status = "pending"', fetch_one=True)
        total_deposits = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM deposits WHERE status = "approved"', fetch_one=True)
        total_withdraws = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM withdrawals WHERE status = "approved"', fetch_one=True)
        total_reviews = execute_query('SELECT COUNT(*) as count FROM reviews WHERE is_approved = 1', fetch_one=True)
        total_slots = execute_query('SELECT COUNT(*) as count FROM slot_history', fetch_one=True)
        
        return jsonify({
            'total_users': total_users['count'] if total_users else 0,
            'total_orders': total_orders['count'] if total_orders else 0,
            'pending_orders': pending_orders['count'] if pending_orders else 0,
            'total_deposits': total_deposits['total'] if total_deposits else 0,
            'total_withdraws': total_withdraws['total'] if total_withdraws else 0,
            'total_reviews': total_reviews['count'] if total_reviews else 0,
            'total_slots': total_slots['count'] if total_slots else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# FIX: WALLET SETTINGS API (OVERWRITE)
# ============================================================

@app.route('/api/admin/wallets', methods=['GET'])
@login_required
@owner_required
def api_admin_get_wallets_fix():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, token_name, address, COALESCE(rate, 15700) as rate, COALESCE(is_active, 1) as is_active
            FROM wallet_settings 
            ORDER BY token_name
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'token_name': row[1],
                'address': row[2],
                'rate': float(row[3]) if row[3] else 15700,
                'is_active': row[4] if row[4] else 1
            })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Get wallets error: {e}")
        return jsonify([]), 200

@app.route('/api/admin/wallets/add', methods=['POST'])
@login_required
@owner_required
def api_admin_add_wallet_fix():
    try:
        data = request.get_json()
        token = data.get('token_name', '').strip()
        address = data.get('address', '').strip()
        rate = float(data.get('rate', 15700))
        
        if not token or not address:
            return jsonify({'success': False, 'error': 'Token dan Address wajib diisi'}), 400
        
        if len(address) < 10:
            return jsonify({'success': False, 'error': 'Address tidak valid (minimal 10 karakter)'}), 400
        
        if rate <= 0:
            return jsonify({'success': False, 'error': 'Rate harus lebih dari 0'}), 400
        
        execute_query('''
            INSERT OR REPLACE INTO wallet_settings (token_name, address, rate, is_active, updated_at)
            VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
        ''', (token, address, rate))
        
        return jsonify({'success': True, 'message': f'✅ Wallet {token} berhasil ditambahkan!'})
    except Exception as e:
        logger.error(f"Add wallet error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/wallets/update', methods=['POST'])
@login_required
@owner_required
def api_admin_update_wallet_fix():
    try:
        data = request.get_json()
        wallet_id = data.get('id')
        address = data.get('address', '').strip()
        rate = float(data.get('rate', 15700))
        is_active = data.get('is_active', 1)
        
        if not wallet_id:
            return jsonify({'success': False, 'error': 'ID wallet required'}), 400
        
        if not address or len(address) < 10:
            return jsonify({'success': False, 'error': 'Address tidak valid'}), 400
        
        if rate <= 0:
            return jsonify({'success': False, 'error': 'Rate harus lebih dari 0'}), 400
        
        execute_query('''
            UPDATE wallet_settings 
            SET address = ?, rate = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (address, rate, is_active, wallet_id))
        
        return jsonify({'success': True, 'message': '✅ Wallet berhasil diupdate!'})
    except Exception as e:
        logger.error(f"Update wallet error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/wallets/delete', methods=['POST'])
@login_required
@owner_required
def api_admin_delete_wallet_fix():
    try:
        data = request.get_json()
        wallet_id = data.get('wallet_id')
        
        if not wallet_id:
            return jsonify({'success': False, 'error': 'ID wallet required'}), 400
        
        wallet = execute_query('SELECT token_name FROM wallet_settings WHERE id = ?', (wallet_id,), fetch_one=True)
        if not wallet:
            return jsonify({'success': False, 'error': 'Wallet not found'}), 404
        
        execute_query('DELETE FROM wallet_settings WHERE id = ?', (wallet_id,))
        
        return jsonify({'success': True, 'message': f'✅ Wallet {wallet["token_name"]} berhasil dihapus!'})
    except Exception as e:
        logger.error(f"Delete wallet error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN USD RATE ROUTES =====

@app.route('/api/admin/usd-rate', methods=['GET'])
@login_required
@owner_required
def api_admin_get_usd_rate():
    try:
        usd_rate = float(get_setting('usd_rate', 15500))
        return jsonify({'success': True, 'usd_rate': usd_rate})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/usd-rate/update', methods=['POST'])
@login_required
@owner_required
def api_admin_update_usd_rate():
    try:
        data = request.json
        usd_rate = data.get('usd_rate')
        
        if usd_rate is None or float(usd_rate) <= 0:
            return jsonify({'success': False, 'error': 'Harga USD harus lebih dari 0'}), 400
        
        update_setting('usd_rate', str(usd_rate))
        
        logger.info(f"USD rate updated to {usd_rate} by admin")
        return jsonify({'success': True, 'message': f'Harga USD berhasil diupdate menjadi Rp {float(usd_rate):,.0f}'})
    except Exception as e:
        logger.error(f"Update USD rate error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN FEE ROUTES =====

@app.route('/api/admin/fees', methods=['GET'])
@login_required
@owner_required
def api_admin_get_fees():
    try:
        fees = execute_query('SELECT * FROM fee_settings ORDER BY min_amount', fetch_all=True) or []
        return jsonify([dict(f) for f in fees])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/fees/add', methods=['POST'])
@login_required
@owner_required
def api_admin_add_fee():
    try:
        data = request.json
        min_amount = float(data.get('min_amount', 0))
        max_amount = float(data.get('max_amount', 0))
        fee = float(data.get('fee', 0))
        
        if min_amount < 0 or max_amount <= min_amount or fee < 0:
            return jsonify({'success': False, 'error': 'Invalid fee settings'}), 400
        
        execute_query('''
            INSERT INTO fee_settings (min_amount, max_amount, fee)
            VALUES (?, ?, ?)
        ''', (min_amount, max_amount, fee))
        
        return jsonify({'success': True, 'message': 'Fee added!'})
    except Exception as e:
        logger.error(f"Add fee error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/fees/delete', methods=['POST'])
@login_required
@owner_required
def api_admin_delete_fee():
    try:
        data = request.json
        fee_id = data.get('fee_id')
        
        if not fee_id:
            return jsonify({'success': False, 'error': 'Fee ID required'}), 400
        
        execute_query('DELETE FROM fee_settings WHERE id = ?', (fee_id,))
        
        return jsonify({'success': True, 'message': 'Fee deleted!'})
    except Exception as e:
        logger.error(f"Delete fee error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN MAINTENANCE ROUTES =====

@app.route('/api/admin/maintenance', methods=['GET'])
@login_required
@owner_required
def api_admin_get_maintenance():
    try:
        maintenance = execute_query('SELECT * FROM maintenance_settings ORDER BY feature', fetch_all=True) or []
        return jsonify([dict(m) for m in maintenance])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/maintenance/toggle', methods=['POST'])
@login_required
@owner_required
def api_admin_toggle_maintenance():
    try:
        data = request.json
        feature = data.get('feature')
        is_active = data.get('is_active', 0)
        
        if not feature:
            return jsonify({'success': False, 'error': 'Feature required'}), 400
        
        execute_query('''
            INSERT OR REPLACE INTO maintenance_settings (feature, is_active, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (feature, is_active))
        
        status = 'aktif' if is_active else 'nonaktif'
        logger.info(f"Maintenance {feature} set to {status} by admin")
        return jsonify({'success': True, 'message': f'Maintenance {feature} {status}!'})
    except Exception as e:
        logger.error(f"Toggle maintenance error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN ORDER ROUTES =====

@app.route('/api/admin/order/approve', methods=['POST'])
@login_required
@owner_required
def api_admin_approve_order():
    try:
        data = request.json
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({'success': False, 'error': 'Order ID required'}), 400
        
        order = execute_query('SELECT * FROM orders WHERE order_number = ?', (order_id,), fetch_one=True)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        if order['status'] != 'pending':
            return jsonify({'success': False, 'error': f'Order already {order["status"]}'}), 400
        
        execute_query('UPDATE orders SET status = "approved", approved_at = CURRENT_TIMESTAMP WHERE order_number = ?', (order_id,))
        
        # Notify user
        send_telegram_message(
            order['user_id'],
            f"✅ *Order {order_id} DISETUJUI!*\n\n"
            f"💰 Jumlah: {format_rupiah(order['amount_idr'])}\n"
            f"📅 Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"⏳ Owner akan segera transfer ke rekening Anda."
        )
        
        # Notify group
        try:
            send_telegram_message(
                GROUP_CHAT_ID,
                f"✅ *Order {order_id} disetujui!*\n"
                f"👤 User: @{order['username']}\n"
                f"💰 Jumlah: {format_rupiah(order['amount_idr'])}"
            )
        except:
            pass
        
        logger.info(f"Order {order_id} approved by admin")
        return jsonify({'success': True, 'message': 'Order approved!'})
    except Exception as e:
        logger.error(f"Approve order error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/order/reject', methods=['POST'])
@login_required
@owner_required
def api_admin_reject_order():
    try:
        data = request.json
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({'success': False, 'error': 'Order ID required'}), 400
        
        order = execute_query('SELECT * FROM orders WHERE order_number = ?', (order_id,), fetch_one=True)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        if order['status'] != 'pending':
            return jsonify({'success': False, 'error': f'Order already {order["status"]}'}), 400
        
        execute_query('UPDATE orders SET status = "rejected" WHERE order_number = ?', (order_id,))
        
        # Notify user
        send_telegram_message(
            order['user_id'],
            f"❌ *Order {order_id} DITOLAK!*\n\n"
            f"Mohon maaf, order Anda tidak dapat diproses.\n"
            f"Silakan coba lagi dengan data yang valid."
        )
        
        logger.info(f"Order {order_id} rejected by admin")
        return jsonify({'success': True, 'message': 'Order rejected!'})
    except Exception as e:
        logger.error(f"Reject order error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN DEPOSIT ROUTES =====

@app.route('/api/admin/deposit/approve', methods=['POST'])
@login_required
@owner_required
def api_admin_approve_deposit():
    try:
        data = request.json
        deposit_id = data.get('deposit_id')
        
        if not deposit_id:
            return jsonify({'success': False, 'error': 'Deposit ID required'}), 400
        
        deposit = execute_query('SELECT * FROM deposits WHERE dep_number = ?', (deposit_id,), fetch_one=True)
        if not deposit:
            return jsonify({'success': False, 'error': 'Deposit not found'}), 404
        
        if deposit['status'] != 'pending':
            return jsonify({'success': False, 'error': f'Deposit already {deposit["status"]}'}), 400
        
        execute_query('UPDATE deposits SET status = "approved", approved_at = CURRENT_TIMESTAMP WHERE dep_number = ?', (deposit_id,))
        execute_query('UPDATE users SET balance = balance + ? WHERE id = ?', (deposit['amount'], deposit['user_id']))
        
        # Log
        log_transaction(deposit['user_id'], 'deposit_approved', deposit['amount'], f'Deposit {deposit_id} approved')
        
        # Notify user
        send_telegram_message(
            deposit['user_id'],
            f"✅ *Deposit {deposit_id} DISETUJUI!*\n\n"
            f"💰 Jumlah: {format_rupiah(deposit['amount'])}\n"
            f"Saldo Anda telah bertambah!"
        )
        
        logger.info(f"Deposit {deposit_id} approved by admin")
        return jsonify({'success': True, 'message': 'Deposit approved!'})
    except Exception as e:
        logger.error(f"Approve deposit error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/deposit/reject', methods=['POST'])
@login_required
@owner_required
def api_admin_reject_deposit():
    try:
        data = request.json
        deposit_id = data.get('deposit_id')
        
        if not deposit_id:
            return jsonify({'success': False, 'error': 'Deposit ID required'}), 400
        
        deposit = execute_query('SELECT * FROM deposits WHERE dep_number = ?', (deposit_id,), fetch_one=True)
        if not deposit:
            return jsonify({'success': False, 'error': 'Deposit not found'}), 404
        
        if deposit['status'] != 'pending':
            return jsonify({'success': False, 'error': f'Deposit already {deposit["status"]}'}), 400
        
        execute_query('UPDATE deposits SET status = "rejected" WHERE dep_number = ?', (deposit_id,))
        
        # Notify user
        send_telegram_message(
            deposit['user_id'],
            f"❌ *Deposit {deposit_id} DITOLAK!*\n\n"
            f"Mohon maaf, bukti transfer Anda tidak valid.\n"
            f"Silakan coba lagi dengan bukti yang jelas."
        )
        
        logger.info(f"Deposit {deposit_id} rejected by admin")
        return jsonify({'success': True, 'message': 'Deposit rejected!'})
    except Exception as e:
        logger.error(f"Reject deposit error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN WITHDRAW ROUTES =====

@app.route('/api/admin/withdraw/approve', methods=['POST'])
@login_required
@owner_required
def api_admin_approve_withdraw():
    try:
        data = request.json
        withdraw_id = data.get('withdraw_id')
        
        if not withdraw_id:
            return jsonify({'success': False, 'error': 'Withdraw ID required'}), 400
        
        withdraw = execute_query('SELECT * FROM withdrawals WHERE wd_number = ?', (withdraw_id,), fetch_one=True)
        if not withdraw:
            return jsonify({'success': False, 'error': 'Withdraw not found'}), 404
        
        if withdraw['status'] != 'pending':
            return jsonify({'success': False, 'error': f'Withdraw already {withdraw["status"]}'}), 400
        
        execute_query('UPDATE withdrawals SET status = "approved", approved_at = CURRENT_TIMESTAMP WHERE wd_number = ?', (withdraw_id,))
        
        # Log
        log_transaction(withdraw['user_id'], 'withdraw_approved', withdraw['amount'], f'Withdraw {withdraw_id} approved')
        
        # Notify user
        send_telegram_message(
            withdraw['user_id'],
            f"✅ *Withdraw {withdraw_id} DISETUJUI!*\n\n"
            f"💰 Jumlah: {format_rupiah(withdraw['amount'])}\n"
            f"📱 Tujuan: {withdraw['destination']}\n\n"
            f"Dana akan segera dikirim ke rekening Anda."
        )
        
        logger.info(f"Withdraw {withdraw_id} approved by admin")
        return jsonify({'success': True, 'message': 'Withdraw approved!'})
    except Exception as e:
        logger.error(f"Approve withdraw error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/withdraw/reject', methods=['POST'])
@login_required
@owner_required
def api_admin_reject_withdraw():
    try:
        data = request.json
        withdraw_id = data.get('withdraw_id')
        
        if not withdraw_id:
            return jsonify({'success': False, 'error': 'Withdraw ID required'}), 400
        
        withdraw = execute_query('SELECT * FROM withdrawals WHERE wd_number = ?', (withdraw_id,), fetch_one=True)
        if not withdraw:
            return jsonify({'success': False, 'error': 'Withdraw not found'}), 404
        
        if withdraw['status'] != 'pending':
            return jsonify({'success': False, 'error': f'Withdraw already {withdraw["status"]}'}), 400
        
        # Return funds
        total_return = withdraw['amount'] + (withdraw['fee'] or 0)
        execute_query('UPDATE users SET balance = balance + ? WHERE id = ?', (total_return, withdraw['user_id']))
        execute_query('UPDATE withdrawals SET status = "rejected" WHERE wd_number = ?', (withdraw_id,))
        
        # Notify user
        send_telegram_message(
            withdraw['user_id'],
            f"❌ *Withdraw {withdraw_id} DITOLAK!*\n\n"
            f"Mohon maaf, withdraw Anda tidak dapat diproses.\n"
            f"Saldo Anda telah dikembalikan."
        )
        
        logger.info(f"Withdraw {withdraw_id} rejected by admin")
        return jsonify({'success': True, 'message': 'Withdraw rejected!'})
    except Exception as e:
        logger.error(f"Reject withdraw error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN REVIEW ROUTES =====

@app.route('/api/admin/review/approve', methods=['POST'])
@login_required
@owner_required
def api_admin_approve_review():
    try:
        data = request.json
        review_id = data.get('review_id')
        
        if not review_id:
            return jsonify({'success': False, 'error': 'Review ID required'}), 400
        
        review = execute_query('SELECT * FROM reviews WHERE id = ?', (review_id,), fetch_one=True)
        if not review:
            return jsonify({'success': False, 'error': 'Review not found'}), 404
        
        execute_query('UPDATE reviews SET is_approved = 1, approved_at = CURRENT_TIMESTAMP WHERE id = ?', (review_id,))
        
        logger.info(f"Review {review_id} approved by admin")
        return jsonify({'success': True, 'message': 'Review approved!'})
    except Exception as e:
        logger.error(f"Approve review error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/review/reject', methods=['POST'])
@login_required
@owner_required
def api_admin_reject_review():
    try:
        data = request.json
        review_id = data.get('review_id')
        
        if not review_id:
            return jsonify({'success': False, 'error': 'Review ID required'}), 400
        
        review = execute_query('SELECT * FROM reviews WHERE id = ?', (review_id,), fetch_one=True)
        if not review:
            return jsonify({'success': False, 'error': 'Review not found'}), 404
        
        execute_query('DELETE FROM reviews WHERE id = ?', (review_id,))
        
        logger.info(f"Review {review_id} rejected by admin")
        return jsonify({'success': True, 'message': 'Review rejected!'})
    except Exception as e:
        logger.error(f"Reject review error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN NOTIFY =====

@app.route('/api/admin/notify', methods=['POST'])
@login_required
@owner_required
def api_admin_notify():
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'error': 'Message required'}), 400
        
        users = execute_query('SELECT telegram_id, id FROM users WHERE telegram_id IS NOT NULL', fetch_all=True) or []
        
        success_count = 0
        for user in users:
            try:
                if send_telegram_message(user['telegram_id'], f"📢 *Pengumuman*\n\n{message}"):
                    success_count += 1
                time.sleep(0.05)
            except:
                pass
        
        logger.info(f"Notification sent to {success_count} users by admin")
        return jsonify({'success': True, 'sent': success_count, 'total': len(users)})
    except Exception as e:
        logger.error(f"Notify error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN USER MANAGEMENT =====

@app.route('/api/admin/users')
@login_required
@owner_required
def api_admin_users():
    try:
        users = execute_query('''
            SELECT id, username, full_name, email, balance, is_verified, is_banned, 
                   joined_at, last_login, is_owner 
            FROM users 
            ORDER BY id DESC LIMIT 100
        ''', fetch_all=True) or []
        return jsonify([dict(u) for u in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/user/<int:user_id>')
@login_required
@owner_required
def api_admin_user_detail(user_id):
    try:
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        return jsonify(dict(user))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/user/<int:user_id>/ban', methods=['POST'])
@login_required
@owner_required
def api_admin_ban_user(user_id):
    try:
        data = request.json
        reason = data.get('reason', 'Melanggar aturan')
        
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        execute_query('''
            UPDATE users 
            SET is_banned = 1, ban_reason = ?, banned_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (reason, user_id))
        
        # Notify
        send_telegram_message(
            user.get('telegram_id') or user_id,
            f"🚫 *AKUN DIBLOKIR!*\n\n"
            f"Alasan: {reason}\n"
            f"Hubungi owner untuk informasi lebih lanjut."
        )
        
        logger.info(f"User {user['username']} banned by admin")
        return jsonify({'success': True, 'message': 'User banned!'})
    except Exception as e:
        logger.error(f"Ban user error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/user/<int:user_id>/unban', methods=['POST'])
@login_required
@owner_required
def api_admin_unban_user(user_id):
    try:
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        execute_query('''
            UPDATE users 
            SET is_banned = 0, ban_reason = NULL, banned_at = NULL 
            WHERE id = ?
        ''', (user_id,))
        
        # Notify
        send_telegram_message(
            user.get('telegram_id') or user_id,
            f"✅ *AKUN DIBUKA!*\n\n"
            f"Anda sudah bisa menggunakan layanan kembali."
        )
        
        logger.info(f"User {user['username']} unbanned by admin")
        return jsonify({'success': True, 'message': 'User unbanned!'})
    except Exception as e:
        logger.error(f"Unban user error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/user/<int:user_id>/balance', methods=['POST'])
@login_required
@owner_required
def api_admin_user_balance(user_id):
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        action = data.get('action', 'add')
        
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        if action == 'add':
            execute_query('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
            msg = f"💰 Admin menambahkan {format_rupiah(amount)} ke saldo Anda."
        else:
            if user['balance'] < amount:
                return jsonify({'success': False, 'error': 'Saldo tidak cukup!'}), 400
            execute_query('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, user_id))
            msg = f"💰 Admin mengurangi {format_rupiah(amount)} dari saldo Anda."
        
        # Log
        log_transaction(user_id, 'admin_balance', amount, f'Admin {action} balance')
        
        # Notify
        new_balance = get_user_balance(user_id)
        send_telegram_message(
            user.get('telegram_id') or user_id,
            f"ℹ️ *Update Saldo*\n\n{msg}\n\nSaldo terbaru: {format_rupiah(new_balance)}"
        )
        
        logger.info(f"User {user['username']} balance {action} {amount} by admin")
        return jsonify({'success': True, 'message': 'Balance updated!', 'new_balance': new_balance})
    except Exception as e:
        logger.error(f"Update balance error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ADMIN EXPORT =====

@app.route('/admin/export/orders')
@login_required
@owner_required
def admin_export_orders():
    try:
        orders = execute_query('''
            SELECT o.*, u.username, u.full_name 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            ORDER BY o.created_at DESC
        ''', fetch_all=True) or []
        
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerow(['Order Number', 'User', 'Full Name', 'Bank', 'Account', 'Amount USD', 'Amount IDR', 'Fee', 'Status', 'Created At'])
        
        for order in orders:
            writer.writerow([
                order['order_number'],
                order['username'],
                order['full_name'],
                order['bank_name'] or '-',
                order['account_number'] or '-',
                order['amount_usd'] or 0,
                order['amount_idr'] or 0,
                order['fee_idr'] or 0,
                order['status'],
                order['created_at']
            ])
        
        output = io.BytesIO()
        output.write(si.getvalue().encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output, 
            mimetype='text/csv', 
            as_attachment=True, 
            download_name=f'orders_export_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        logger.error(f"Export orders error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_estimate', methods=['GET'])
@login_required
def api_get_estimate():
    try:
        crypto = request.args.get('crypto', 'USDT BEP-20')
        amount = float(request.args.get('amount', 0))
        
        if amount < 0.1:
            return jsonify({'success': False, 'error': 'Minimal $0.1'}), 400
        
        usd_rate = float(get_setting('usd_rate', 15500))
        wallet = execute_query('SELECT rate FROM wallet_settings WHERE token_name = ?', (crypto,), fetch_one=True)
        token_rate = wallet['rate'] if wallet else usd_rate
        
        # ===== AMBIL FEE BERDASARKAN AMOUNT USD =====
        fee_row = execute_query('''
            SELECT fee FROM fee_settings 
            WHERE ? >= min_amount AND ? <= max_amount 
            ORDER BY min_amount LIMIT 1
        ''', (amount, amount), fetch_one=True)

        if fee_row:
            fee_idr = float(fee_row['fee'])
        else:
            fee_idr = float(get_setting('withdraw_fee', 5000))
        
        total_idr = amount * token_rate
        amount_idr = total_idr - fee_idr
        
        return jsonify({
            'success': True,
            'total_idr': total_idr,
            'amount_idr': amount_idr,
            'fee_idr': fee_idr,
            'rate': token_rate,
            'usd_rate': usd_rate
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
        
@app.route('/api/wallets', methods=['GET'])
@login_required
def api_get_wallets_for_convert():
    try:
        wallets = execute_query('SELECT token_name, address, rate FROM wallet_settings WHERE is_active = 1 ORDER BY token_name', fetch_all=True)
        result = []
        if wallets:
            for w in wallets:
                result.append({
                    'token_name': w['token_name'],
                    'address': w['address'],
                    'rate': w['rate'] if w['rate'] else 15500
                })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500        
        
@app.route('/deposit')
@login_required
def deposit():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        return render_template('deposit.html', user=user, balance=user['balance'] if user else 0)
    except Exception as e:
        logger.error(f"Deposit page error: {e}")
        return render_template('deposit.html', user=None, balance=0, error='Gagal memuat halaman deposit')
        
@app.route('/withdraw')
@login_required
def withdraw():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        # Ambil fee withdraw dari settings
        withdraw_fee = float(get_setting('withdraw_fee', 5000))
        min_withdraw = float(get_setting('min_withdraw', 50000))
        
        return render_template('withdraw.html', 
            user=user, 
            balance=user['balance'] if user else 0,
            withdraw_fee=withdraw_fee,
            min_withdraw=min_withdraw
        )
    except Exception as e:
        logger.error(f"Withdraw page error: {e}")
        return render_template('withdraw.html', 
            user=None, 
            balance=0, 
            withdraw_fee=5000,
            min_withdraw=50000,
            error='Gagal memuat halaman withdraw'
        )       
            
@app.route('/arisan')
@login_required
def arisan():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        # ===== AMBIL DATA ARISAN =====
        # Ambil semua arisan yang aktif
        arisan_list = execute_query('''
            SELECT 
                a.*,
                COUNT(ap.id) as participant_count,
                (SELECT COUNT(*) FROM arisan_participants WHERE arisan_id = a.id AND user_id = ?) as user_joined
            FROM arisan a
            LEFT JOIN arisan_participants ap ON a.id = ap.arisan_id
            WHERE a.status = 'active'
            GROUP BY a.id
            ORDER BY a.created_at DESC
        ''', (user_id,), fetch_all=True) or []
        
        # Format data untuk tampilan
        formatted_arisan = []
        for a in arisan_list:
            formatted_arisan.append({
                'id': a['id'],
                'total_slots': a['total_slots'],
                'price': a['price'],
                'price_display': format_rupiah(a['price']),
                'prize_display': format_rupiah(a['price'] * (a['total_slots'] - 1)),
                'participant_count': a['participant_count'] or 0,
                'owner_profit_percent': a['owner_profit_percent'] or 10,
                'created_at': a['created_at'],
                'status': a['status'],
                'user_joined': a['user_joined'] or 0,
                'winner_name': a['winner_name'],
                'winner_wallet_info': a['winner_wallet_info']
            })
        
        # ===== STATS =====
        active_count = execute_query('''
            SELECT COUNT(*) as count FROM arisan WHERE status = 'active'
        ''', fetch_one=True)['count'] or 0
        
        total_participants = execute_query('''
            SELECT COUNT(*) as count FROM arisan_participants
        ''', fetch_one=True)['count'] or 0
        
        won_count = execute_query('''
            SELECT COUNT(*) as count FROM arisan WHERE winner_id IS NOT NULL
        ''', fetch_one=True)['count'] or 0
        
        return render_template('arisan.html',
            user=user,
            arisan_list=formatted_arisan,
            active_count=active_count,
            total_participants=total_participants,
            won_count=won_count,
            balance=user['balance'] if user else 0
        )
        
    except Exception as e:
        logger.error(f"Arisan page error: {e}")
        return render_template('arisan.html',
            user=None,
            arisan_list=[],
            active_count=0,
            total_participants=0,
            won_count=0,
            balance=0,
            error='Gagal memuat halaman arisan'
        )
        
# ============================================================
# PROFILE PAGE
# ============================================================

@app.route('/profile')
@login_required
def profile():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT * FROM users WHERE id = ?', (user_id,), fetch_one=True)
        
        total_orders = execute_query('SELECT COUNT(*) as count FROM orders WHERE user_id = ?', (user_id,), fetch_one=True)['count'] or 0
        total_deposits = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM deposits WHERE user_id = ? AND status = "approved"', (user_id,), fetch_one=True)['total'] or 0
        total_withdraws = execute_query('SELECT COALESCE(SUM(amount), 0) as total FROM withdrawals WHERE user_id = ? AND status = "approved"', (user_id,), fetch_one=True)['total'] or 0
        total_referrals = execute_query('SELECT COUNT(*) as count FROM referrals WHERE user_id = ?', (user_id,), fetch_one=True)['count'] or 0
        
        return render_template('profile.html',
            user=user,
            balance=user['balance'] if user else 0,
            total_orders=total_orders,
            total_deposits=total_deposits,
            total_withdraws=total_withdraws,
            total_referrals=total_referrals
        )
    except Exception as e:
        logger.error(f"Profile page error: {e}")
        return render_template('profile.html', 
            user=None, 
            balance=0,
            total_orders=0,
            total_deposits=0,
            total_withdraws=0,
            total_referrals=0,
            error='Gagal memuat halaman profil'
        )


# ============================================================
# API PROFILE
# ============================================================

@app.route('/api/profile', methods=['GET'])
@login_required
def api_get_profile():
    try:
        user_id = session['user_id']
        user = execute_query('SELECT id, username, email, full_name, balance, is_verified, is_owner, joined_at, last_login FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        return jsonify({'success': True, 'user': dict(user)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/update', methods=['POST'])
@login_required
def api_update_profile():
    try:
        data = request.get_json()
        user_id = session['user_id']
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        
        if not full_name or len(full_name) < 3:
            return jsonify({'success': False, 'error': 'Nama lengkap minimal 3 karakter'}), 400
        if not email or '@' not in email:
            return jsonify({'success': False, 'error': 'Email tidak valid'}), 400
        if not username or len(username) < 3:
            return jsonify({'success': False, 'error': 'Username minimal 3 karakter'}), 400
        
        existing = execute_query('SELECT id FROM users WHERE (email = ? OR username = ?) AND id != ?', (email, username, user_id), fetch_one=True)
        if existing:
            return jsonify({'success': False, 'error': 'Email atau Username sudah digunakan'}), 400
        
        execute_query('UPDATE users SET full_name = ?, email = ?, username = ? WHERE id = ?', (full_name, email, username, user_id))
        session['username'] = username
        session['full_name'] = full_name
        session['email'] = email
        
        return jsonify({'success': True, 'message': 'Profil berhasil diupdate!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/change-password', methods=['POST'])
@login_required
def api_change_password():
    try:
        data = request.get_json()
        user_id = session['user_id']
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        if not current_password or not new_password or not confirm_password:
            return jsonify({'success': False, 'error': 'Semua field harus diisi'}), 400
        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'Password baru minimal 6 karakter'}), 400
        if new_password != confirm_password:
            return jsonify({'success': False, 'error': 'Password baru tidak cocok'}), 400
        
        user = execute_query('SELECT password FROM users WHERE id = ?', (user_id,), fetch_one=True)
        if not user or user['password'] != hash_password(current_password):
            return jsonify({'success': False, 'error': 'Password saat ini salah'}), 400
        
        execute_query('UPDATE users SET password = ? WHERE id = ?', (hash_password(new_password), user_id))
        return jsonify({'success': True, 'message': 'Password berhasil diubah!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/profile/avatar', methods=['POST'])
@login_required
def api_update_avatar():
    try:
        data = request.get_json()
        user_id = session['user_id']
        avatar = data.get('avatar', '')
        
        if not avatar or not avatar.startswith('data:image'):
            return jsonify({'success': False, 'error': 'Format avatar tidak valid'}), 400
        if len(avatar) > 500_000:
            return jsonify({'success': False, 'error': 'Ukuran avatar maksimal 500KB'}), 400
        
        execute_query('UPDATE users SET avatar = ? WHERE id = ?', (avatar, user_id))
        return jsonify({'success': True, 'message': 'Avatar berhasil diupdate!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
        
# ============================================================
# ===== RUN APP =====
# ============================================================

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("=" * 70)
    print("🚀 DAVAOFC WEB - VERSI SUPER LENGKAP")
    print("=" * 70)
    print(f"📱 Open: http://139.162.24.234:5000")
    print(f"👑 Owner Login: {OWNER_EMAIL} / {OWNER_PASSWORD}")
    print("=" * 70)
    print("✅ Semua fitur terhubung dengan benar!")
    print("✅ Admin panel lengkap!")
    print("✅ Wallet management dengan rate!")
    print("✅ Fee management!")
    print("✅ Maintenance management!")
    print("✅ User management!")
    print("=" * 70)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)