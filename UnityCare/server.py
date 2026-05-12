#!/usr/bin/env python3
"""
UnityCare Full-Stack Server
- SQLite persistent database
- Real account creation + real login validation
- httpOnly signed sessions
- No demo users and no demo people
- OpenRouter-powered assistant answers typed user questions using saved UnityCare data
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import hmac
import json
import mimetypes
import os
import secrets
import sqlite3
import sys
import traceback
import urllib.error
import urllib.request
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

try:
    import bcrypt  # type: ignore
except Exception:  # pragma: no cover
    bcrypt = None

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "unitycare.db"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL_DEFAULT = "openai/gpt-4o-mini"



def load_env_file() -> None:
    """Load simple KEY=value lines from .env without requiring python-dotenv."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_env_file()

SESSION_COOKIE = "unitycare_session"
SESSION_DAYS_DEFAULT = 7
SESSION_DAYS_REMEMBER = 30
LOCKOUT_FAILED_LIMIT = 5
LOCKOUT_MINUTES = 15
SECRET = os.environ.get("UNITYCARE_SECRET", "dev-change-this-secret-before-deploying")
INTERNAL_PATHS = {
    "/dashboard", "/tasks", "/medications", "/appointments", "/family",
    "/journal", "/ai", "/notifications", "/settings", "/onboarding"
}


def utcnow() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def parse_iso(value: str) -> Optional[dt.datetime]:
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


def db() -> sqlite3.Connection:
    DATA_DIR.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def rows_to_dicts(rows) -> list[dict[str, Any]]:
    return [dict(r) for r in rows]


def one_to_dict(row) -> Optional[dict[str, Any]]:
    return dict(row) if row else None


def init_db() -> None:
    with db() as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                phone TEXT,
                password_hash TEXT NOT NULL,
                profile_photo TEXT,
                language TEXT NOT NULL DEFAULT 'en',
                onboarding_complete INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                device_hint TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL COLLATE NOCASE,
                attempted_at TEXT NOT NULL,
                success INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS care_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_by_user_id INTEGER NOT NULL,
                recipient_name TEXT NOT NULL,
                recipient_age INTEGER,
                recipient_photo TEXT,
                relationship TEXT,
                living_situation TEXT,
                location TEXT,
                gp_name TEXT,
                gp_phone TEXT,
                allergies TEXT,
                conditions TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(created_by_user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS family_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                care_profile_id INTEGER,
                name TEXT NOT NULL DEFAULT 'UnityCare group',
                created_by_user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(care_profile_id) REFERENCES care_profiles(id) ON DELETE SET NULL,
                FOREIGN KEY(created_by_user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS family_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                user_id INTEGER,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                notes TEXT,
                last_active TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
            );
            CREATE TABLE IF NOT EXISTS invites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                token_hash TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                accepted_at TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                care_profile_id INTEGER,
                name TEXT NOT NULL,
                dosage TEXT,
                frequency TEXT,
                purpose TEXT,
                prescribing_doctor TEXT,
                refill_date TEXT,
                notes TEXT,
                sort_order INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE,
                FOREIGN KEY(care_profile_id) REFERENCES care_profiles(id) ON DELETE SET NULL
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                care_profile_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                assigned_to_member_id INTEGER,
                due_date TEXT,
                status TEXT NOT NULL DEFAULT 'todo',
                category TEXT,
                priority TEXT DEFAULT 'normal',
                recurring TEXT DEFAULT 'none',
                created_by_user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                completed_at TEXT,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE,
                FOREIGN KEY(care_profile_id) REFERENCES care_profiles(id) ON DELETE SET NULL,
                FOREIGN KEY(assigned_to_member_id) REFERENCES family_members(id) ON DELETE SET NULL,
                FOREIGN KEY(created_by_user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                care_profile_id INTEGER,
                title TEXT NOT NULL,
                appointment_datetime TEXT,
                doctor_name TEXT,
                location TEXT,
                accompanied_by_member_id INTEGER,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE,
                FOREIGN KEY(care_profile_id) REFERENCES care_profiles(id) ON DELETE SET NULL,
                FOREIGN KEY(accompanied_by_member_id) REFERENCES family_members(id) ON DELETE SET NULL
            );
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                care_profile_id INTEGER,
                author_user_id INTEGER NOT NULL,
                entry_text TEXT NOT NULL,
                ai_flagged INTEGER NOT NULL DEFAULT 0,
                ai_flag_reason TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE,
                FOREIGN KEY(care_profile_id) REFERENCES care_profiles(id) ON DELETE SET NULL,
                FOREIGN KEY(author_user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                group_id INTEGER,
                type TEXT NOT NULL,
                message TEXT NOT NULL,
                read INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS ai_chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                group_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(group_id) REFERENCES family_groups(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                date_format TEXT DEFAULT 'DD/MM/YYYY',
                time_format TEXT DEFAULT '24h',
                email_notifications INTEGER DEFAULT 1,
                in_app_notifications INTEGER DEFAULT 1,
                quiet_hours_start TEXT,
                quiet_hours_end TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS dismissed_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                alert_key TEXT NOT NULL,
                dismissed_at TEXT NOT NULL,
                UNIQUE(user_id, alert_key),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )


def password_hash(password: str) -> str:
    if bcrypt is not None:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")
        return "bcrypt$" + hashed
    salt = secrets.token_bytes(16)
    iterations = 220_000
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2${}${}${}".format(iterations, base64.b64encode(salt).decode(), base64.b64encode(dk).decode())


def verify_password(password: str, stored: str) -> bool:
    try:
        if stored.startswith("bcrypt$") and bcrypt is not None:
            return bool(bcrypt.checkpw(password.encode("utf-8"), stored.split("$", 1)[1].encode("utf-8")))
        if stored.startswith("pbkdf2$"):
            _, iters, salt_b64, hash_b64 = stored.split("$", 3)
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(hash_b64)
            actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iters))
            return hmac.compare_digest(actual, expected)
    except Exception:
        return False
    return False


def session_hash(token: str) -> str:
    return hmac.new(SECRET.encode(), token.encode(), hashlib.sha256).hexdigest()


def make_session(con: sqlite3.Connection, user_id: int, remember: bool, device_hint: str) -> Tuple[str, str]:
    token = secrets.token_urlsafe(48)
    days = SESSION_DAYS_REMEMBER if remember else SESSION_DAYS_DEFAULT
    expires = (dt.datetime.utcnow() + dt.timedelta(days=days)).replace(microsecond=0).isoformat() + "Z"
    con.execute(
        "INSERT INTO sessions(user_id, token_hash, expires_at, created_at, device_hint) VALUES(?,?,?,?,?)",
        (user_id, session_hash(token), expires, utcnow(), device_hint[:160]),
    )
    return token, expires


def get_cookie(header: str | None, name: str) -> Optional[str]:
    if not header:
        return None
    cookie = SimpleCookie()
    try:
        cookie.load(header)
    except Exception:
        return None
    morsel = cookie.get(name)
    return morsel.value if morsel else None


def clean_text(value: Any, max_len: int = 5000) -> str:
    if value is None:
        return ""
    text = str(value).replace("\x00", "").strip()
    return text[:max_len]


def require_fields(data: Dict[str, Any], fields: list[str]) -> Optional[str]:
    missing = [f for f in fields if not clean_text(data.get(f))]
    if missing:
        return "Missing required field: " + ", ".join(missing)
    return None


class UnityCareHandler(BaseHTTPRequestHandler):
    server_version = "UnityCare/8.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def send_json(self, status: int, payload: Dict[str, Any], cookie: str | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def redirect(self, where: str) -> None:
        self.send_response(302)
        self.send_header("Location", where)
        self.end_headers()

    def read_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length > 2_000_000:
            raise ValueError("Request body too large")
        raw = self.rfile.read(length) if length else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def current_user(self) -> Optional[Dict[str, Any]]:
        token = get_cookie(self.headers.get("Cookie"), SESSION_COOKIE)
        if not token:
            return None
        th = session_hash(token)
        with db() as con:
            row = con.execute(
                """
                SELECT users.* FROM sessions
                JOIN users ON users.id = sessions.user_id
                WHERE sessions.token_hash=? AND sessions.expires_at > ?
                """,
                (th, utcnow()),
            ).fetchone()
            return one_to_dict(row)

    def user_group_id(self, con: sqlite3.Connection, user_id: int) -> int:
        group = con.execute("SELECT id FROM family_groups WHERE created_by_user_id=? ORDER BY id LIMIT 1", (user_id,)).fetchone()
        if group:
            return int(group["id"])
        cur = con.execute("INSERT INTO family_groups(name, created_by_user_id, created_at) VALUES(?,?,?)", ("UnityCare group", user_id, utcnow()))
        return int(cur.lastrowid)

    def care_profile_id(self, con: sqlite3.Connection, group_id: int) -> Optional[int]:
        row = con.execute("SELECT care_profile_id FROM family_groups WHERE id=?", (group_id,)).fetchone()
        return int(row["care_profile_id"]) if row and row["care_profile_id"] else None

    def do_GET(self) -> None:
        try:
            path = self.path.split("?", 1)[0]
            if path.startswith("/api/"):
                self.route_api_get(path)
                return
            if path in INTERNAL_PATHS and not self.current_user():
                self.redirect("/")
                return
            self.serve_static(path)
        except Exception as exc:
            traceback.print_exc()
            if self.path.startswith("/api/"):
                self.send_json(500, {"ok": False, "error": "Server error. Please try again."})
            else:
                self.send_error(500, "Server error")

    def do_POST(self) -> None:
        try:
            self.route_api_post(self.path.split("?", 1)[0])
        except Exception as exc:
            traceback.print_exc()
            self.send_json(500, {"ok": False, "error": "Server error. Please try again."})

    def do_PUT(self) -> None:
        try:
            self.route_api_put(self.path.split("?", 1)[0])
        except Exception:
            traceback.print_exc()
            self.send_json(500, {"ok": False, "error": "Server error. Please try again."})

    def do_DELETE(self) -> None:
        try:
            self.route_api_delete(self.path.split("?", 1)[0])
        except Exception:
            traceback.print_exc()
            self.send_json(500, {"ok": False, "error": "Server error. Please try again."})

    def serve_static(self, path: str) -> None:
        if path == "/" or path == "":
            file_path = STATIC_DIR / "index.html"
        else:
            clean = path.lstrip("/")
            file_path = STATIC_DIR / clean
            if not file_path.exists() and path in INTERNAL_PATHS:
                file_path = STATIC_DIR / "index.html"
        if not file_path.exists() or not file_path.resolve().is_relative_to(STATIC_DIR.resolve()):
            self.send_error(404, "Not found")
            return
        ctype = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def auth_or_401(self) -> Optional[Dict[str, Any]]:
        user = self.current_user()
        if not user:
            self.send_json(401, {"ok": False, "error": "Authentication required"})
            return None
        return user

    def route_api_get(self, path: str) -> None:
        if path == "/api/auth/me":
            user = self.current_user()
            if not user:
                self.send_json(200, {"ok": True, "user": None})
                return
            with db() as con:
                group_id = self.user_group_id(con, user["id"])
            self.send_json(200, {"ok": True, "user": self.public_user(user), "groupId": group_id})
            return

        user = self.auth_or_401()
        if not user:
            return
        with db() as con:
            group_id = self.user_group_id(con, user["id"])
            if path == "/api/dashboard":
                self.send_json(200, {"ok": True, "data": self.collect_context(con, user, group_id)})
            elif path == "/api/care-recipient":
                self.send_json(200, {"ok": True, "profile": self.get_profile(con, group_id)})
            elif path == "/api/members":
                self.send_json(200, {"ok": True, "members": rows_to_dicts(con.execute("SELECT * FROM family_members WHERE group_id=? ORDER BY created_at DESC", (group_id,)).fetchall())})
            elif path == "/api/medications":
                self.send_json(200, {"ok": True, "medications": rows_to_dicts(con.execute("SELECT * FROM medications WHERE group_id=? ORDER BY sort_order, id DESC", (group_id,)).fetchall())})
            elif path == "/api/tasks":
                self.send_json(200, {"ok": True, "tasks": rows_to_dicts(con.execute("SELECT tasks.*, family_members.name AS assigned_name FROM tasks LEFT JOIN family_members ON family_members.id=tasks.assigned_to_member_id WHERE tasks.group_id=? ORDER BY tasks.created_at DESC", (group_id,)).fetchall())})
            elif path == "/api/appointments":
                self.send_json(200, {"ok": True, "appointments": rows_to_dicts(con.execute("SELECT appointments.*, family_members.name AS accompanied_by_name FROM appointments LEFT JOIN family_members ON family_members.id=appointments.accompanied_by_member_id WHERE appointments.group_id=? ORDER BY appointments.appointment_datetime", (group_id,)).fetchall())})
            elif path == "/api/journal":
                self.send_json(200, {"ok": True, "entries": rows_to_dicts(con.execute("SELECT journal_entries.*, users.full_name AS author_name FROM journal_entries JOIN users ON users.id=journal_entries.author_user_id WHERE journal_entries.group_id=? ORDER BY journal_entries.created_at DESC", (group_id,)).fetchall())})
            elif path == "/api/notifications":
                self.send_json(200, {"ok": True, "notifications": rows_to_dicts(con.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC", (user["id"],)).fetchall())})
            elif path == "/api/ai/messages":
                self.send_json(200, {"ok": True, "messages": rows_to_dicts(con.execute("SELECT role, content, created_at FROM ai_chat_messages WHERE user_id=? AND group_id=? ORDER BY id ASC LIMIT 200", (user["id"], group_id)).fetchall())})
            else:
                self.send_json(404, {"ok": False, "error": "API route not found"})

    def route_api_post(self, path: str) -> None:
        data = self.read_json()
        if path == "/api/auth/signup":
            self.signup(data)
            return
        if path == "/api/auth/login":
            self.login(data)
            return
        if path == "/api/auth/logout":
            self.logout()
            return

        user = self.auth_or_401()
        if not user:
            return
        with db() as con:
            group_id = self.user_group_id(con, user["id"])
            cp_id = self.care_profile_id(con, group_id)
            if path == "/api/care-recipient":
                err = require_fields(data, ["recipientName"])
                if err:
                    self.send_json(400, {"ok": False, "error": err}); return
                existing = self.get_profile(con, group_id)
                payload = (
                    clean_text(data.get("recipientName"), 160), self.as_int(data.get("recipientAge")), clean_text(data.get("relationship"), 80),
                    clean_text(data.get("livingSituation"), 120), clean_text(data.get("location"), 160), clean_text(data.get("gpName"), 160),
                    clean_text(data.get("gpPhone"), 80), clean_text(data.get("allergies"), 500), clean_text(data.get("conditions"), 1000)
                )
                if existing:
                    con.execute("UPDATE care_profiles SET recipient_name=?, recipient_age=?, relationship=?, living_situation=?, location=?, gp_name=?, gp_phone=?, allergies=?, conditions=? WHERE id=?", (*payload, existing["id"]))
                    profile_id = existing["id"]
                else:
                    cur = con.execute("INSERT INTO care_profiles(created_by_user_id, recipient_name, recipient_age, relationship, living_situation, location, gp_name, gp_phone, allergies, conditions, created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (user["id"], *payload, utcnow()))
                    profile_id = cur.lastrowid
                    con.execute("UPDATE family_groups SET care_profile_id=? WHERE id=?", (profile_id, group_id))
                con.execute("UPDATE users SET onboarding_complete=1 WHERE id=?", (user["id"],))
                self.send_json(200, {"ok": True, "profile": self.get_profile(con, group_id)})
            elif path == "/api/members":
                err = require_fields(data, ["name", "email", "role"])
                if err:
                    self.send_json(400, {"ok": False, "error": err}); return
                cur = con.execute("INSERT INTO family_members(group_id, name, email, phone, role, notes, last_active, created_at) VALUES(?,?,?,?,?,?,?,?)", (group_id, clean_text(data.get("name"), 160), clean_text(data.get("email"), 160), clean_text(data.get("phone"), 80), clean_text(data.get("role"), 80), clean_text(data.get("notes"), 1000), "Just added", utcnow()))
                self.send_json(201, {"ok": True, "member": one_to_dict(con.execute("SELECT * FROM family_members WHERE id=?", (cur.lastrowid,)).fetchone())})
            elif path == "/api/medications":
                err = require_fields(data, ["name"])
                if err:
                    self.send_json(400, {"ok": False, "error": err}); return
                cur = con.execute("INSERT INTO medications(group_id, care_profile_id, name, dosage, frequency, purpose, prescribing_doctor, refill_date, notes, sort_order, created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (group_id, cp_id, clean_text(data.get("name"), 160), clean_text(data.get("dosage"), 120), clean_text(data.get("frequency"), 120), clean_text(data.get("purpose"), 240), clean_text(data.get("prescribingDoctor"), 160), clean_text(data.get("refillDate"), 40), clean_text(data.get("notes"), 1000), 0, utcnow()))
                self.send_json(201, {"ok": True, "medication": one_to_dict(con.execute("SELECT * FROM medications WHERE id=?", (cur.lastrowid,)).fetchone())})
            elif path == "/api/tasks":
                err = require_fields(data, ["title"])
                if err:
                    self.send_json(400, {"ok": False, "error": err}); return
                priority = clean_text(data.get("priority"), 40) or self.local_priority(data)
                assigned = self.as_int(data.get("assignedToMemberId"))
                cur = con.execute("INSERT INTO tasks(group_id, care_profile_id, title, description, assigned_to_member_id, due_date, status, category, priority, recurring, created_by_user_id, created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (group_id, cp_id, clean_text(data.get("title"), 180), clean_text(data.get("description"), 1200), assigned, clean_text(data.get("dueDate"), 40), clean_text(data.get("status"), 30) or "todo", clean_text(data.get("category"), 80), priority, clean_text(data.get("recurring"), 40) or "none", user["id"], utcnow()))
                self.send_json(201, {"ok": True, "task": one_to_dict(con.execute("SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)).fetchone())})
            elif path == "/api/appointments":
                err = require_fields(data, ["title"])
                if err:
                    self.send_json(400, {"ok": False, "error": err}); return
                cur = con.execute("INSERT INTO appointments(group_id, care_profile_id, title, appointment_datetime, doctor_name, location, accompanied_by_member_id, notes, created_at) VALUES(?,?,?,?,?,?,?,?,?)", (group_id, cp_id, clean_text(data.get("title"), 180), clean_text(data.get("appointmentDateTime"), 80), clean_text(data.get("doctorName"), 160), clean_text(data.get("location"), 200), self.as_int(data.get("accompaniedByMemberId")), clean_text(data.get("notes"), 1200), utcnow()))
                self.send_json(201, {"ok": True, "appointment": one_to_dict(con.execute("SELECT * FROM appointments WHERE id=?", (cur.lastrowid,)).fetchone())})
            elif path == "/api/journal":
                err = require_fields(data, ["entryText"])
                if err:
                    self.send_json(400, {"ok": False, "error": err}); return
                cur = con.execute("INSERT INTO journal_entries(group_id, care_profile_id, author_user_id, entry_text, created_at) VALUES(?,?,?,?,?)", (group_id, cp_id, user["id"], clean_text(data.get("entryText"), 5000), utcnow()))
                self.send_json(201, {"ok": True, "entry": one_to_dict(con.execute("SELECT * FROM journal_entries WHERE id=?", (cur.lastrowid,)).fetchone())})
            elif path == "/api/ai/chat":
                self.ai_chat(con, user, group_id, clean_text(data.get("message"), 4000))
            elif path == "/api/ai/clear":
                con.execute("DELETE FROM ai_chat_messages WHERE user_id=? AND group_id=?", (user["id"], group_id))
                self.send_json(200, {"ok": True})
            elif path == "/api/notifications/read-all":
                con.execute("UPDATE notifications SET read=1 WHERE user_id=?", (user["id"],))
                self.send_json(200, {"ok": True})
            else:
                self.send_json(404, {"ok": False, "error": "API route not found"})

    def route_api_put(self, path: str) -> None:
        user = self.auth_or_401()
        if not user:
            return
        data = self.read_json()
        parts = path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "api":
            self.send_json(404, {"ok": False, "error": "API route not found"}); return
        table_key, item_id = parts[1], self.as_int(parts[2])
        if not item_id:
            self.send_json(400, {"ok": False, "error": "Invalid id"}); return
        with db() as con:
            group_id = self.user_group_id(con, user["id"])
            if table_key == "members":
                con.execute("UPDATE family_members SET name=?, email=?, phone=?, role=?, notes=? WHERE id=? AND group_id=?", (clean_text(data.get("name"),160), clean_text(data.get("email"),160), clean_text(data.get("phone"),80), clean_text(data.get("role"),80), clean_text(data.get("notes"),1000), item_id, group_id))
            elif table_key == "medications":
                con.execute("UPDATE medications SET name=?, dosage=?, frequency=?, purpose=?, prescribing_doctor=?, refill_date=?, notes=? WHERE id=? AND group_id=?", (clean_text(data.get("name"),160), clean_text(data.get("dosage"),120), clean_text(data.get("frequency"),120), clean_text(data.get("purpose"),240), clean_text(data.get("prescribingDoctor"),160), clean_text(data.get("refillDate"),40), clean_text(data.get("notes"),1000), item_id, group_id))
            elif table_key == "tasks":
                con.execute("UPDATE tasks SET title=?, description=?, assigned_to_member_id=?, due_date=?, status=?, category=?, priority=?, recurring=? WHERE id=? AND group_id=?", (clean_text(data.get("title"),180), clean_text(data.get("description"),1200), self.as_int(data.get("assignedToMemberId")), clean_text(data.get("dueDate"),40), clean_text(data.get("status"),30) or "todo", clean_text(data.get("category"),80), clean_text(data.get("priority"),40), clean_text(data.get("recurring"),40), item_id, group_id))
            elif table_key == "appointments":
                con.execute("UPDATE appointments SET title=?, appointment_datetime=?, doctor_name=?, location=?, accompanied_by_member_id=?, notes=? WHERE id=? AND group_id=?", (clean_text(data.get("title"),180), clean_text(data.get("appointmentDateTime"),80), clean_text(data.get("doctorName"),160), clean_text(data.get("location"),200), self.as_int(data.get("accompaniedByMemberId")), clean_text(data.get("notes"),1200), item_id, group_id))
            elif table_key == "notifications":
                con.execute("UPDATE notifications SET read=1 WHERE id=? AND user_id=?", (item_id, user["id"]))
            else:
                self.send_json(404, {"ok": False, "error": "Unknown collection"}); return
            self.send_json(200, {"ok": True})

    def route_api_delete(self, path: str) -> None:
        user = self.auth_or_401()
        if not user:
            return
        parts = path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "api":
            self.send_json(404, {"ok": False, "error": "API route not found"}); return
        table_key, item_id = parts[1], self.as_int(parts[2])
        if not item_id:
            self.send_json(400, {"ok": False, "error": "Invalid id"}); return
        allowed = {"members": "family_members", "medications": "medications", "tasks": "tasks", "appointments": "appointments", "journal": "journal_entries", "notifications": "notifications"}
        table = allowed.get(table_key)
        if not table:
            self.send_json(404, {"ok": False, "error": "Unknown collection"}); return
        with db() as con:
            group_id = self.user_group_id(con, user["id"])
            if table == "notifications":
                con.execute(f"DELETE FROM {table} WHERE id=? AND user_id=?", (item_id, user["id"]))
            else:
                con.execute(f"DELETE FROM {table} WHERE id=? AND group_id=?", (item_id, group_id))
            self.send_json(200, {"ok": True})

    def signup(self, data: Dict[str, Any]) -> None:
        err = require_fields(data, ["fullName", "email", "password"])
        if err:
            self.send_json(400, {"ok": False, "error": err}); return
        email = clean_text(data.get("email"), 180).lower()
        password = clean_text(data.get("password"), 512)
        if len(password) < 8:
            self.send_json(400, {"ok": False, "error": "Password must be at least 8 characters."}); return
        with db() as con:
            existing = con.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
            if existing:
                self.send_json(409, {"ok": False, "error": "An account with this email already exists. Log in instead."}); return
            cur = con.execute("INSERT INTO users(full_name, email, phone, password_hash, language, created_at) VALUES(?,?,?,?,?,?)", (clean_text(data.get("fullName"), 160), email, clean_text(data.get("phone"), 80), password_hash(password), clean_text(data.get("language"), 8) or "en", utcnow()))
            user_id = int(cur.lastrowid)
            con.execute("INSERT INTO family_groups(name, created_by_user_id, created_at) VALUES(?,?,?)", ("UnityCare group", user_id, utcnow()))
            con.execute("INSERT INTO user_settings(user_id) VALUES(?)", (user_id,))
            token, expires = make_session(con, user_id, True, self.headers.get("User-Agent", "unknown"))
            user = con.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        cookie = f"{SESSION_COOKIE}={token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={SESSION_DAYS_REMEMBER*24*3600}"
        self.send_json(201, {"ok": True, "user": self.public_user(dict(user)), "expiresAt": expires}, cookie)

    def login(self, data: Dict[str, Any]) -> None:
        email = clean_text(data.get("email"), 180).lower()
        password = clean_text(data.get("password"), 512)
        remember = bool(data.get("remember"))
        if not email or not password:
            self.send_json(400, {"ok": False, "error": "Incorrect email or password. Please try again."}); return
        with db() as con:
            lock = self.lockout_remaining(con, email)
            if lock > 0:
                self.send_json(429, {"ok": False, "error": "Too many failed attempts. Try again when the countdown ends.", "lockoutSeconds": lock}); return
            user = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            valid = bool(user and verify_password(password, user["password_hash"]))
            con.execute("INSERT INTO login_attempts(email, attempted_at, success) VALUES(?,?,?)", (email, utcnow(), 1 if valid else 0))
            if not valid:
                self.send_json(401, {"ok": False, "error": "Incorrect email or password. Please try again."}); return
            token, expires = make_session(con, int(user["id"]), remember, self.headers.get("User-Agent", "unknown"))
        max_age = (SESSION_DAYS_REMEMBER if remember else SESSION_DAYS_DEFAULT) * 24 * 3600
        cookie = f"{SESSION_COOKIE}={token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={max_age}"
        self.send_json(200, {"ok": True, "user": self.public_user(dict(user)), "expiresAt": expires}, cookie)

    def logout(self) -> None:
        token = get_cookie(self.headers.get("Cookie"), SESSION_COOKIE)
        if token:
            with db() as con:
                con.execute("DELETE FROM sessions WHERE token_hash=?", (session_hash(token),))
        cookie = f"{SESSION_COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0"
        self.send_json(200, {"ok": True}, cookie)

    def lockout_remaining(self, con: sqlite3.Connection, email: str) -> int:
        cutoff = (dt.datetime.utcnow() - dt.timedelta(minutes=LOCKOUT_MINUTES)).replace(microsecond=0).isoformat() + "Z"
        rows = con.execute("SELECT attempted_at FROM login_attempts WHERE email=? AND success=0 AND attempted_at>? ORDER BY attempted_at ASC", (email, cutoff)).fetchall()
        if len(rows) < LOCKOUT_FAILED_LIMIT:
            return 0
        oldest = parse_iso(rows[0]["attempted_at"])
        if not oldest:
            return 0
        unlock = oldest + dt.timedelta(minutes=LOCKOUT_MINUTES)
        return max(0, int((unlock - dt.datetime.utcnow()).total_seconds()))

    def ai_chat(self, con: sqlite3.Connection, user: Dict[str, Any], group_id: int, message: str) -> None:
        if not message:
            self.send_json(400, {"ok": False, "error": "Message is required."}); return
        con.execute("INSERT INTO ai_chat_messages(user_id, group_id, role, content, created_at) VALUES(?,?,?,?,?)", (user["id"], group_id, "user", message, utcnow()))
        context = self.collect_context(con, user, group_id)
        try:
            reply = self.openrouter_care_assistant_reply(message, context, user)
        except Exception as exc:
            reply = str(exc) or "The assistant could not answer right now. Check the server OpenRouter settings and try again."
        created = utcnow()
        con.execute("INSERT INTO ai_chat_messages(user_id, group_id, role, content, created_at) VALUES(?,?,?,?,?)", (user["id"], group_id, "assistant", reply, created))
        self.send_json(200, {"ok": True, "reply": reply, "createdAt": created})

    def openrouter_care_assistant_reply(self, message: str, context: Dict[str, Any], user: Dict[str, Any]) -> str:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OpenRouter is not configured on the server. Add OPENROUTER_API_KEY in your environment variables and redeploy.")

        language = "Arabic" if user.get("language") == "ar" else "English"
        system_prompt = (
            "You are UnityCare Assistant, a calm family care coordinator inside a web app. "
            "The user can type any care-related question. Answer using the saved UnityCare data provided as JSON. "
            "Do not invent family members, medications, appointments, diagnoses, or facts that are not in the data. "
            "If information is missing, clearly say what is missing and what the user should add next. "
            "You are not a doctor. Do not diagnose, do not tell users to start or stop medication, and do not replace a doctor or pharmacist. "
            "For medication and health concerns, advise confirming with a doctor or pharmacist. "
            f"Reply only in {language}. Keep the answer helpful, structured, and easy to present."
        )
        safe_context = json.dumps(context, ensure_ascii=False, indent=2, default=str)
        payload = {
            "model": os.environ.get("OPENROUTER_MODEL", OPENROUTER_MODEL_DEFAULT),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Saved UnityCare data for this logged-in user/group:\n" + safe_context},
                {"role": "user", "content": message},
            ],
            "temperature": 0.25,
            "max_tokens": 900,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.environ.get("OPENROUTER_SITE_URL", "https://unitycare.local"),
            "X-Title": os.environ.get("OPENROUTER_SITE_NAME", "UnityCare"),
        }
        request = urllib.request.Request(
            OPENROUTER_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as err:
            detail = ""
            try:
                body = err.read().decode("utf-8")
                parsed = json.loads(body)
                detail = parsed.get("error", {}).get("message") or parsed.get("message") or body[:240]
            except Exception:
                detail = getattr(err, "reason", "") or "OpenRouter request failed"
            raise RuntimeError(f"OpenRouter error: {detail}")
        except Exception as err:
            raise RuntimeError("Could not reach OpenRouter. Check internet access, key, model, and credits.") from err

        try:
            parsed = json.loads(raw)
            content = parsed["choices"][0]["message"]["content"]
            if isinstance(content, list):
                content = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
            content = clean_text(content, 6000)
            if not content:
                raise ValueError("Empty assistant response")
            return content
        except Exception as err:
            raise RuntimeError("OpenRouter returned an unreadable response. Try a different OPENROUTER_MODEL.") from err

    def local_care_assistant_reply(self, message: str, context: Dict[str, Any], user: Dict[str, Any]) -> str:
        ar = (user.get("language") == "ar")
        msg = message.lower()
        profile = context.get("careRecipient") or {}
        members = context.get("familyMembers") or []
        meds = context.get("medications") or []
        tasks = context.get("tasks") or []
        appts = context.get("appointments") or []
        journal = context.get("journalEntries") or []
        name = profile.get("recipient_name") or ("المستفيد من الرعاية" if ar else "the care recipient")

        def none(text_en: str, text_ar: str) -> str:
            return text_ar if ar else text_en

        def bullet(lines: list[str]) -> str:
            return "\n".join([f"• {x}" for x in lines if x])

        def parse_date(value: Any) -> Optional[dt.date]:
            if not value:
                return None
            try:
                return dt.date.fromisoformat(str(value)[:10])
            except Exception:
                return None

        def member_name(member_id: Any) -> str:
            for m in members:
                if str(m.get("id")) == str(member_id):
                    return m.get("name") or none("Unnamed member", "عضو بدون اسم")
            return none("Unassigned", "غير معيّن")

        def short_date(value: Any) -> str:
            d = parse_date(value)
            return str(d) if d else none("No date", "لا يوجد تاريخ")

        today = dt.date.today()
        overdue, due_soon = [], []
        for task in tasks:
            d = parse_date(task.get("due_date"))
            if task.get("status") != "done" and d and d < today:
                overdue.append(task)
            elif task.get("status") != "done" and d and d <= today + dt.timedelta(days=3):
                due_soon.append(task)

        upcoming = []
        for appt in appts:
            d = parse_date(appt.get("appointment_datetime"))
            if d and d >= today:
                upcoming.append(appt)
        upcoming = sorted(upcoming, key=lambda a: str(a.get("appointment_datetime") or ""))

        refill_soon, missing_med_details = [], []
        for med in meds:
            d = parse_date(med.get("refill_date"))
            if d and today <= d <= today + dt.timedelta(days=7):
                refill_soon.append(med)
            missing = [label for key, label in [
                ("dosage", none("dosage", "الجرعة")),
                ("frequency", none("frequency", "التكرار")),
                ("purpose", none("purpose", "الهدف")),
                ("refill_date", none("refill date", "تاريخ التعبئة")),
            ] if not med.get(key)]
            if missing:
                missing_med_details.append((med, missing))

        if any(x in msg for x in ["first", "add first", "أضيف أول", "ابدأ"]):
            steps = []
            if not profile:
                steps.append(none("Add the care recipient profile: name, age, relationship, location, GP phone, allergies, and conditions.", "أضف ملف المستفيد من الرعاية: الاسم، العمر، صلة القرابة، الموقع، رقم الطبيب، الحساسية، والحالات الصحية."))
            if not members:
                steps.append(none("Add at least one family member so tasks and appointments can be assigned clearly.", "أضف فرداً واحداً على الأقل من العائلة حتى يمكن توزيع المهام والمواعيد بوضوح."))
            if not meds:
                steps.append(none("Add medications with dosage, frequency, purpose, and refill date.", "أضف الأدوية مع الجرعة، التكرار، الهدف، وتاريخ إعادة التعبئة."))
            if not tasks:
                steps.append(none("Create the first care task, such as a check-in call, medication pickup, transport, or grocery task.", "أنشئ أول مهمة رعاية، مثل اتصال للاطمئنان أو استلام دواء أو توصيل أو شراء احتياجات."))
            if not appts:
                steps.append(none("Add the next medical or family appointment if one exists.", "أضف الموعد الطبي أو العائلي القادم إن وجد."))
            if not journal:
                steps.append(none("Write the first journal note so the family has a history of observations.", "اكتب أول ملاحظة في سجل الرعاية حتى يكون للعائلة تاريخ للملاحظات."))
            if not steps:
                steps.append(none("Your basic setup looks good. Next, keep tasks updated and add journal notes regularly.", "الإعداد الأساسي يبدو جيداً. الخطوة التالية هي تحديث المهام وإضافة ملاحظات السجل بانتظام."))
            return none("Start with these items:\n", "ابدأ بهذه الأشياء:\n") + bullet(steps)

        if any(x in msg for x in ["summarise", "summarize", "current care", "لخص", "ملخص"]):
            lines = [
                none(f"Care recipient: {name}" + (f", age {profile.get('recipient_age')}" if profile.get("recipient_age") else ""), f"المستفيد من الرعاية: {name}" + (f"، العمر {profile.get('recipient_age')}" if profile.get("recipient_age") else "")),
                none(f"Family members added: {len(members)}", f"عدد أفراد العائلة المضافين: {len(members)}"),
                none(f"Medications saved: {len(meds)}", f"عدد الأدوية المحفوظة: {len(meds)}"),
                none(f"Open tasks: {len([t for t in tasks if t.get('status') != 'done'])}", f"المهام المفتوحة: {len([t for t in tasks if t.get('status') != 'done'])}"),
                none(f"Upcoming appointments: {len(upcoming)}", f"المواعيد القادمة: {len(upcoming)}"),
                none(f"Journal notes: {len(journal)}", f"ملاحظات السجل: {len(journal)}"),
            ]
            if profile.get("conditions"):
                lines.append(none(f"Known conditions: {profile.get('conditions')}", f"الحالات الصحية: {profile.get('conditions')}"))
            return none("UnityCare summary from saved data:\n", "ملخص UnityCare من البيانات المحفوظة:\n") + bullet(lines)

        if any(x in msg for x in ["attention today", "needs attention", "today", "انتباه", "اليوم"]):
            lines = []
            if overdue:
                lines.append(none(f"{len(overdue)} task(s) are overdue.", f"هناك {len(overdue)} مهمة متأخرة."))
            if due_soon:
                lines.append(none(f"{len(due_soon)} task(s) are due within 3 days.", f"هناك {len(due_soon)} مهمة خلال 3 أيام."))
            if refill_soon:
                lines.append(none(f"{len(refill_soon)} medication refill(s) are due within 7 days.", f"هناك {len(refill_soon)} تعبئة دواء خلال 7 أيام."))
            if upcoming[:1]:
                a = upcoming[0]
                lines.append(none(f"Next appointment: {a.get('title')} on {short_date(a.get('appointment_datetime'))}.", f"الموعد القادم: {a.get('title')} بتاريخ {short_date(a.get('appointment_datetime'))}."))
            if missing_med_details:
                lines.append(none("Some medications are missing important details.", "بعض الأدوية ناقصة معلومات مهمة."))
            if not lines:
                lines.append(none("Nothing urgent is visible from the saved data. Keep adding tasks, medication details, appointments, and journal notes.", "لا يظهر شيء عاجل من البيانات المحفوظة. استمر في إضافة المهام وتفاصيل الأدوية والمواعيد وملاحظات السجل."))
            return none("What needs attention:\n", "الأشياء التي تحتاج انتباه:\n") + bullet(lines)

        if any(x in msg for x in ["overdue", "important", "priority", "رتب", "متأخرة", "مهمة"]):
            selected = overdue or [t for t in tasks if t.get("status") != "done"]
            if not selected:
                return none("There are no open tasks saved yet. Add a task first, then I can help rank it.", "لا توجد مهام مفتوحة محفوظة حالياً. أضف مهمة أولاً ثم أستطيع ترتيبها.")
            priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
            selected = sorted(selected, key=lambda t: (priority_order.get(str(t.get("priority") or "normal"), 2), str(t.get("due_date") or "9999-12-31")))[:6]
            lines = [none(f"{x.get('title')} — {x.get('priority') or 'normal'}, due {short_date(x.get('due_date'))}, assigned to {x.get('assigned_name') or member_name(x.get('assigned_to_member_id'))}.", f"{x.get('title')} — الأولوية {x.get('priority') or 'normal'}، التاريخ {short_date(x.get('due_date'))}، المسؤول {x.get('assigned_name') or member_name(x.get('assigned_to_member_id'))}.") for x in selected]
            return none("Task priority list:\n", "ترتيب أولوية المهام:\n") + bullet(lines)

        if "suggest one" in msg or "suggest a task" in msg or "اقترح" in msg:
            if refill_soon:
                med = refill_soon[0]
                return none(f"Suggested task: Pick up or confirm refill for {med.get('name')} before {short_date(med.get('refill_date'))}. Assign it to the family member who is available soonest.", f"مهمة مقترحة: استلام أو تأكيد تعبئة دواء {med.get('name')} قبل {short_date(med.get('refill_date'))}. عيّنها للفرد المتاح قريباً.")
            if upcoming:
                a = upcoming[0]
                return none(f"Suggested task: Prepare for {a.get('title')} on {short_date(a.get('appointment_datetime'))}: confirm transport, write questions, and bring medication list.", f"مهمة مقترحة: التجهيز لموعد {a.get('title')} بتاريخ {short_date(a.get('appointment_datetime'))}: تأكيد التوصيل، كتابة الأسئلة، وإحضار قائمة الأدوية.")
            if meds:
                return none("Suggested task: Review medication details and make sure every medication has dosage, frequency, purpose, and refill date.", "مهمة مقترحة: راجع تفاصيل الأدوية وتأكد أن كل دواء له جرعة وتكرار وهدف وتاريخ إعادة تعبئة.")
            return none("Suggested task: Add a daily check-in call for the care recipient and assign it to a family member.", "مهمة مقترحة: أضف اتصال اطمئنان يومي للمستفيد من الرعاية وعيّنه لأحد أفراد العائلة.")

        if any(x in msg for x in ["medication", "medications", "أدوية", "دواء"]):
            if "missing" in msg or "ناقصة" in msg:
                if not missing_med_details:
                    return none("All saved medications have the main details filled in.", "كل الأدوية المحفوظة فيها المعلومات الأساسية.")
                lines = [none(f"{m.get('name')}: missing {', '.join(miss)}.", f"{m.get('name')}: ناقص {', '.join(miss)}.") for m, miss in missing_med_details]
                return none("Medication details to complete:\n", "تفاصيل الأدوية التي تحتاج إكمال:\n") + bullet(lines)
            if "doctor" in msg or "pharmacist" in msg or "طبيب" in msg or "صيدلي" in msg:
                lines = [none("What is the correct dose and best time of day for each medication?", "ما الجرعة الصحيحة وأفضل وقت في اليوم لكل دواء؟"), none("Are any medications unsafe to combine with over-the-counter painkillers or supplements?", "هل توجد أدوية لا يجب جمعها مع مسكنات أو مكملات بدون وصفة؟"), none("Which medications need refills soon?", "أي أدوية تحتاج إعادة تعبئة قريباً؟")]
                return none("Questions to ask the doctor or pharmacist:\n", "أسئلة للطبيب أو الصيدلي:\n") + bullet(lines)
            if not meds:
                return none("No medications are saved yet. Add each medication manually with name, dosage, frequency, purpose, doctor, refill date, and notes.", "لا توجد أدوية محفوظة حالياً. أضف كل دواء يدوياً مع الاسم والجرعة والتكرار والهدف والطبيب وتاريخ التعبئة والملاحظات.")
            lines = [none(f"{m.get('name')} — {m.get('dosage') or 'dosage missing'}, {m.get('frequency') or 'frequency missing'}, purpose: {m.get('purpose') or 'not added'}.", f"{m.get('name')} — {m.get('dosage') or 'الجرعة ناقصة'}، {m.get('frequency') or 'التكرار ناقص'}، الهدف: {m.get('purpose') or 'غير مضاف'}." ) for m in meds]
            return none("Medication summary:\n", "ملخص الأدوية:\n") + bullet(lines) + "\n\n" + none("This is not medical advice. Confirm medication questions with a doctor or pharmacist.", "هذه ليست نصيحة طبية. تأكد من أسئلة الأدوية مع الطبيب أو الصيدلي.")

        if any(x in msg for x in ["appointment", "appointments", "موعد", "مواعيد"]):
            if not upcoming:
                return none("No upcoming appointments are saved yet. Add appointments manually with date/time, doctor, location, and who is taking the care recipient.", "لا توجد مواعيد قادمة محفوظة حالياً. أضف المواعيد يدوياً مع التاريخ والوقت والطبيب والموقع ومن سيرافق المستفيد.")
            lines = [none(f"{a.get('title')} — {short_date(a.get('appointment_datetime'))}, doctor/location: {a.get('doctor_name') or a.get('location') or 'not added'}, accompanied by {a.get('accompanied_by_name') or member_name(a.get('accompanied_by_member_id'))}.", f"{a.get('title')} — {short_date(a.get('appointment_datetime'))}، الطبيب/الموقع: {a.get('doctor_name') or a.get('location') or 'غير مضاف'}، المرافق {a.get('accompanied_by_name') or member_name(a.get('accompanied_by_member_id'))}.") for a in upcoming[:5]]
            return none("Upcoming appointment preparation:\n", "التحضير للمواعيد القادمة:\n") + bullet(lines) + "\n" + bullet([none("Prepare medication list and questions before the visit.", "جهز قائمة الأدوية والأسئلة قبل الموعد."), none("Confirm transport and arrival time with the assigned family member.", "أكد التوصيل ووقت الوصول مع فرد العائلة المسؤول.")])

        if any(x in msg for x in ["balanced", "care load", "rebalance", "توزيع", "متوازن"]):
            if not members:
                return none("No family members are added yet, so care load cannot be balanced. Add members first.", "لا يوجد أفراد عائلة مضافون حالياً، لذلك لا يمكن تقييم توزيع الرعاية. أضف الأفراد أولاً.")
            counts = {m["id"]: 0 for m in members}
            for task in tasks:
                if task.get("assigned_to_member_id") in counts:
                    counts[task.get("assigned_to_member_id")] += 1
            total = sum(counts.values())
            if total == 0:
                return none("Members are added, but no tasks are assigned yet. Assign tasks to see care-load balance.", "الأفراد مضافون، لكن لا توجد مهام معينة لهم. عيّن المهام حتى يظهر توازن الرعاية.")
            lines = [f"{m.get('name')}: {counts.get(m.get('id'),0)} ({round(counts.get(m.get('id'),0)*100/total)}%)" for m in members]
            return none("Care-load distribution from assigned tasks:\n", "توزيع الرعاية حسب المهام المعينة:\n") + bullet(lines) + "\n" + none("If one person has most tasks, consider moving a low-risk task to another available member.", "إذا كان شخص واحد يحمل معظم المهام، انقل مهمة بسيطة إلى فرد آخر متاح.")

        if any(x in msg for x in ["journal", "notes", "patterns", "سجل", "ملاحظات", "أنماط"]):
            if not journal:
                return none("No journal entries are saved yet. Add short notes after calls, visits, incidents, or mood changes.", "لا توجد ملاحظات في السجل حالياً. أضف ملاحظات قصيرة بعد المكالمات أو الزيارات أو الحوادث أو تغير المزاج.")
            latest = journal[:5]
            lines = [none(f"{j.get('created_at')}: {str(j.get('entry_text') or '')[:180]}", f"{j.get('created_at')}: {str(j.get('entry_text') or '')[:180]}") for j in latest]
            text_all = " ".join(str(j.get("entry_text") or "").lower() for j in journal[:20])
            flags = []
            for word, label_en, label_ar in [("confus", "confusion/memory", "ارتباك/ذاكرة"), ("forget", "forgetfulness", "نسيان"), ("fall", "falls", "سقوط"), ("pain", "pain", "ألم"), ("lonely", "loneliness", "وحدة"), ("tired", "tiredness", "تعب")]:
                if text_all.count(word) >= 2:
                    flags.append(label_ar if ar else label_en)
            out = none("Latest journal notes:\n", "آخر ملاحظات السجل:\n") + bullet(lines)
            if flags:
                out += "\n" + none("Repeated words noticed: ", "كلمات متكررة ملاحظة: ") + ", ".join(flags) + ". " + none("Mention repeated concerns to a GP if they continue.", "إذا استمرت هذه الملاحظات، اذكرها للطبيب.")
            return out

        if any(x in msg for x in ["emergency", "طوارئ"]):
            lines = [
                none(f"Name: {name}", f"الاسم: {name}"),
                none(f"Age: {profile.get('recipient_age') or 'not added'}", f"العمر: {profile.get('recipient_age') or 'غير مضاف'}"),
                none(f"Location: {profile.get('location') or 'not added'}", f"الموقع: {profile.get('location') or 'غير مضاف'}"),
                none(f"Conditions: {profile.get('conditions') or 'not added'}", f"الحالات الصحية: {profile.get('conditions') or 'غير مضافة'}"),
                none(f"Allergies: {profile.get('allergies') or 'not added'}", f"الحساسية: {profile.get('allergies') or 'غير مضافة'}"),
                none(f"GP/doctor: {profile.get('gp_name') or 'not added'} — {profile.get('gp_phone') or 'no phone'}", f"الطبيب: {profile.get('gp_name') or 'غير مضاف'} — {profile.get('gp_phone') or 'لا يوجد رقم'}"),
                none("Medications: " + (", ".join([m.get('name') for m in meds if m.get('name')]) or "none saved"), "الأدوية: " + (", ".join([m.get('name') for m in meds if m.get('name')]) or "لا توجد أدوية محفوظة")),
                none("Family contacts: " + (", ".join([f"{m.get('name')} ({m.get('phone') or m.get('email')})" for m in members]) or "none saved"), "جهات تواصل العائلة: " + (", ".join([f"{m.get('name')} ({m.get('phone') or m.get('email')})" for m in members]) or "لا توجد جهات محفوظة")),
            ]
            return none("Emergency card from saved data:\n", "بطاقة الطوارئ من البيانات المحفوظة:\n") + bullet(lines)

        if any(x in msg for x in ["draft", "message to", "رسالة", "اكتب"]):
            target = None
            for m in members:
                mname = (m.get("name") or "").lower()
                first = mname.split()[0] if mname.split() else ""
                if first and (first in msg or mname in msg):
                    target = m
                    break
            target_name = (target or {}).get("name") or none("the family", "العائلة")
            if ar:
                return f"رسالة مقترحة إلى {target_name}:\nمرحباً {target_name}، نحتاج نرتب رعاية {name} هذا الأسبوع بهدوء. هل تستطيع المساعدة في مهمة أو موعد مناسب لك؟ سأضيف التفاصيل في UnityCare حتى يكون كل شيء واضح للجميع. شكراً لك."
            return f"Suggested message to {target_name}:\nHi {target_name}, I’d like us to rebalance {name}’s care this week so everything is clear and fair. Could you help with one task or appointment that fits your schedule? I’ll keep the details updated in UnityCare. Thank you."

        return none("I can answer from the data saved in UnityCare. Type a question about the care summary, overdue tasks, medications, appointments, family balance, journal notes, or emergency card.", "أستطيع الإجابة من البيانات المحفوظة في UnityCare. اكتب سؤالاً عن ملخص الرعاية، المهام المتأخرة، الأدوية، المواعيد، توازن العائلة، ملاحظات السجل، أو بطاقة الطوارئ.")

    def collect_context(self, con: sqlite3.Connection, user: Dict[str, Any], group_id: int) -> Dict[str, Any]:
        profile = self.get_profile(con, group_id)
        members = rows_to_dicts(con.execute("SELECT * FROM family_members WHERE group_id=? ORDER BY created_at DESC", (group_id,)).fetchall())
        meds = rows_to_dicts(con.execute("SELECT * FROM medications WHERE group_id=? ORDER BY sort_order, id DESC", (group_id,)).fetchall())
        tasks = rows_to_dicts(con.execute("SELECT tasks.*, family_members.name AS assigned_name FROM tasks LEFT JOIN family_members ON family_members.id=tasks.assigned_to_member_id WHERE tasks.group_id=? ORDER BY tasks.created_at DESC", (group_id,)).fetchall())
        appointments = rows_to_dicts(con.execute("SELECT appointments.*, family_members.name AS accompanied_by_name FROM appointments LEFT JOIN family_members ON family_members.id=appointments.accompanied_by_member_id WHERE appointments.group_id=? ORDER BY appointments.appointment_datetime", (group_id,)).fetchall())
        journal = rows_to_dicts(con.execute("SELECT journal_entries.*, users.full_name AS author_name FROM journal_entries JOIN users ON users.id=journal_entries.author_user_id WHERE journal_entries.group_id=? ORDER BY journal_entries.created_at DESC LIMIT 20", (group_id,)).fetchall())
        notifications = rows_to_dicts(con.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 20", (user["id"],)).fetchall())
        return {
            "user": self.public_user(user),
            "careRecipient": profile,
            "familyMembers": members,
            "medications": meds,
            "tasks": tasks,
            "appointments": appointments,
            "journalEntries": journal,
            "notifications": notifications,
            "counts": {
                "openTasks": len([t for t in tasks if t.get("status") != "done"]),
                "familyMembers": len(members),
                "medications": len(meds),
                "appointments": len(appointments),
                "unreadNotifications": len([n for n in notifications if not n.get("read")]),
            }
        }

    def get_profile(self, con: sqlite3.Connection, group_id: int) -> Optional[Dict[str, Any]]:
        return one_to_dict(con.execute("SELECT care_profiles.* FROM family_groups JOIN care_profiles ON care_profiles.id=family_groups.care_profile_id WHERE family_groups.id=?", (group_id,)).fetchone())

    @staticmethod
    def public_user(user: Dict[str, Any]) -> Dict[str, Any]:
        return {"id": user["id"], "fullName": user["full_name"], "email": user["email"], "phone": user.get("phone"), "language": user.get("language", "en"), "onboardingComplete": bool(user.get("onboarding_complete"))}

    @staticmethod
    def as_int(value: Any) -> Optional[int]:
        try:
            if value in (None, ""):
                return None
            return int(value)
        except Exception:
            return None

    @staticmethod
    def local_priority(data: Dict[str, Any]) -> str:
        due = clean_text(data.get("dueDate"), 40)
        category = clean_text(data.get("category"), 80).lower()
        if "medical" in category:
            return "high"
        if due:
            try:
                d = dt.date.fromisoformat(due[:10])
                if d <= dt.date.today():
                    return "urgent"
            except Exception:
                pass
        return "normal"


def main() -> None:
    init_db()
    port = int(os.environ.get("PORT", "8787"))
    host = os.environ.get("HOST", "0.0.0.0")
    print("UnityCare v9 Typed OpenRouter assistant server")
    print(f"Local:   http://localhost:{port}")
    print(f"Network: http://YOUR-PC-IP:{port}")
    print(f"Database: {DB_PATH}")
    print("Assistant: OpenRouter typed chat enabled")
    ThreadingHTTPServer((host, port), UnityCareHandler).serve_forever()


if __name__ == "__main__":
    main()
