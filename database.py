import os
import json
import sqlite3
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT DEFAULT 'General',
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                keywords TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                channel TEXT NOT NULL,
                user_identifier TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                is_ai_generated INTEGER DEFAULT 0,
                matched_faq_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Seed FAQs if empty
        c.execute("SELECT COUNT(*) FROM faqs")
        if c.fetchone()[0] == 0:
            faq_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faqs.json")
            if os.path.exists(faq_path):
                with open(faq_path, "r", encoding="utf-8") as f:
                    faqs = json.load(f)
                c.executemany(
                    "INSERT INTO faqs (question, answer) VALUES (?, ?)",
                    [(faq["question"], faq["answer"]) for faq in faqs]
                )

def get_all_faqs(search_query=None):
    with get_db() as conn:
        c = conn.cursor()
        if search_query:
            q = f"%{search_query}%"
            c.execute("SELECT * FROM faqs WHERE question LIKE ? OR answer LIKE ? ORDER BY id DESC", (q, q))
        else:
            c.execute("SELECT * FROM faqs ORDER BY id DESC")
        return [dict(row) for row in c.fetchall()]

def get_faq_by_id(faq_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM faqs WHERE id = ?", (faq_id,))
        row = c.fetchone()
        return dict(row) if row else None

def create_faq(category, question, answer, keywords=""):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO faqs (category, question, answer, keywords) VALUES (?, ?, ?, ?)",
                  (category, question, answer, keywords))
        return c.lastrowid

def update_faq(faq_id, category, question, answer, keywords=""):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("UPDATE faqs SET category=?, question=?, answer=?, keywords=? WHERE id=?",
                  (category, question, answer, keywords, faq_id))
        return c.rowcount > 0

def delete_faq(faq_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
        return c.rowcount > 0

def get_or_create_conversation(conv_id, channel, user_id):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))
        if not c.fetchone():
            c.execute("INSERT INTO conversations (id, channel, user_identifier) VALUES (?, ?, ?)",
                      (conv_id, channel, user_id))

def save_message(conv_id, sender, text, is_ai=False, faq_id=None):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (conversation_id, sender, text, is_ai_generated, matched_faq_id) VALUES (?, ?, ?, ?, ?)",
                  (conv_id, sender, text, 1 if is_ai else 0, faq_id))

def get_conversation_history(conv_id, limit=15):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC LIMIT ?",
                  (conv_id, limit))
        return [dict(row) for row in c.fetchall()]

def get_dashboard_analytics():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM conversations"); total_conv = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM messages WHERE sender='user'"); total_queries = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM messages WHERE sender='bot' AND is_ai_generated=1"); ai_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM messages WHERE sender='bot' AND is_ai_generated=0"); faq_count = c.fetchone()[0]
        c.execute("SELECT channel, COUNT(*) as cnt FROM conversations GROUP BY channel")
        channels = {row["channel"]: row["cnt"] for row in c.fetchall()}
        for ch in ["web", "telegram", "whatsapp", "messenger", "instagram"]:
            channels.setdefault(ch, 0)
        c.execute("""
            SELECT f.question, COUNT(m.id) as cnt FROM messages m
            JOIN faqs f ON m.matched_faq_id = f.id
            WHERE m.sender='bot' GROUP BY m.matched_faq_id ORDER BY cnt DESC LIMIT 5
        """)
        top_faqs = [dict(row) for row in c.fetchall()]
        return {
            "total_conversations": total_conv,
            "total_queries": total_queries,
            "ai_resolved": ai_count,
            "faq_resolved": faq_count,
            "channels": channels,
            "top_faqs": top_faqs
        }
