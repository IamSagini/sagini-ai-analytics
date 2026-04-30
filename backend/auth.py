import sqlite3, os, uuid, bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt

DB_PATH = "/Users/enockabel/Documents/ai-analytics-dashboard/backend/sagini.db"
SECRET_KEY = "sagini-ai-analytics-secret-key-2026-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 30

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_seen TEXT,
            is_admin INTEGER DEFAULT 0,
            upload_count INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS uploads (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            rows INTEGER,
            cols INTEGER
        );
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password[:72].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password[:72].encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id):
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": user_id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def create_user(name, email, password):
    conn = get_db()
    try:
        user_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        conn.execute(
            "INSERT INTO users (id, name, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, email.lower().strip(), hash_password(password), now)
        )
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

def update_last_seen(user_id):
    conn = get_db()
    conn.execute("UPDATE users SET last_seen = ? WHERE id = ?", (datetime.utcnow().isoformat(), user_id))
    conn.commit()
    conn.close()

def log_upload(user_id, filename, rows, cols):
    conn = get_db()
    conn.execute(
        "INSERT INTO uploads (id, user_id, filename, uploaded_at, rows, cols) VALUES (?, ?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), user_id, filename, datetime.utcnow().isoformat(), rows, cols)
    )
    conn.execute("UPDATE users SET upload_count = upload_count + 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_admin_stats():
    conn = get_db()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_uploads = conn.execute("SELECT COUNT(*) FROM uploads").fetchone()[0]
    today = datetime.utcnow().date().isoformat()
    new_today = conn.execute("SELECT COUNT(*) FROM users WHERE created_at LIKE ?", (f"{today}%",)).fetchone()[0]
    active_7d = conn.execute(
        "SELECT COUNT(*) FROM users WHERE last_seen >= ?",
        ((datetime.utcnow() - timedelta(days=7)).isoformat(),)
    ).fetchone()[0]
    recent_users = conn.execute(
        "SELECT id, name, email, created_at, last_seen, upload_count FROM users ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    signups_by_day = conn.execute(
        "SELECT date(created_at) as day, COUNT(*) as count FROM users GROUP BY date(created_at) ORDER BY day DESC LIMIT 14"
    ).fetchall()
    uploads_by_day = conn.execute(
        "SELECT date(uploaded_at) as day, COUNT(*) as count FROM uploads GROUP BY date(uploaded_at) ORDER BY day DESC LIMIT 14"
    ).fetchall()
    conn.close()
    return {
        "total_users": total_users,
        "total_uploads": total_uploads,
        "new_today": new_today,
        "active_7d": active_7d,
        "recent_users": [dict(r) for r in recent_users],
        "signups_by_day": [dict(r) for r in signups_by_day],
        "uploads_by_day": [dict(r) for r in uploads_by_day],
    }

init_db()
