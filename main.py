import os
import uuid
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from database import init_db, get_all_faqs, create_faq, update_faq, delete_faq, get_dashboard_analytics, get_conversation_history
from chatbot import handle_user_query

load_dotenv()

app = FastAPI(title="CloudCounselage Support Chatbot")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.on_event("startup")
def on_startup():
    init_db()
    print("[Server] Database ready.")

STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC), name="static")

@app.get("/")
def index():
    f = os.path.join(STATIC, "index.html")
    if os.path.exists(f):
        return FileResponse(f)
    return {"message": "CloudCounselage Chatbot API running."}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = ""
    channel: Optional[str] = "web"
    user_id: Optional[str] = "web_user"

class FAQBody(BaseModel):
    category: Optional[str] = "General"
    question: str
    answer: str
    keywords: Optional[str] = ""

@app.post("/api/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(400, "Message cannot be empty.")
    sid = req.session_id or str(uuid.uuid4())
    return handle_user_query(sid, req.channel, req.user_id, req.message.strip())

@app.get("/api/chat/history/{session_id}")
def history(session_id: str):
    return {"messages": get_conversation_history(session_id)}

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(400, "Bad JSON")
    msg = data.get("message") or data.get("edited_message")
    if not msg:
        return {"ok": True}
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "").strip()
    user_id = str(msg.get("from", {}).get("id", "unknown"))
    username = msg.get("from", {}).get("username", user_id)
    if not chat_id or not text:
        return {"ok": True}
    if text.startswith("/start"):
        await tg_send(chat_id,
            "👋 Hi! I'm the *CloudCounselage Support Bot*.\n\n"
            "I can help you with:\n"
            "• GPI Internship details\n"
            "• Onboarding & Appointment Letters\n"
            "• Certificates & LOR\n"
            "• Deadlines & Deliverables\n\n"
            "Just type your question! 🚀")
        return {"ok": True}
    result = handle_user_query(f"tg_{chat_id}", "telegram", username, text)
    await tg_send(chat_id, result["response"])
    return {"ok": True}

async def tg_send(chat_id, text):
    if not TELEGRAM_TOKEN:
        return
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{TELEGRAM_URL}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=10)
    except Exception as e:
        print(f"[Telegram] Error: {e}")

@app.get("/setup-telegram")
async def setup_telegram(url: str):
    if not TELEGRAM_TOKEN:
        return {"error": "TELEGRAM_BOT_TOKEN not set"}
    webhook = f"{url}/webhook/telegram"
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{TELEGRAM_URL}/setWebhook", params={"url": webhook})
    return r.json()

@app.post("/api/webhooks/{channel}")
async def channel_webhook(channel: str, request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(400, "Bad JSON")
    text = data.get("message") or data.get("text") or data.get("Body") or ""
    user = str(data.get("user_id") or data.get("From") or "unknown")
    if not text:
        return {"ok": True}
    sid = f"{channel}_{user}_{str(uuid.uuid4())[:6]}"
    result = handle_user_query(sid, channel, user, str(text).strip())
    return {"ok": True, "response": result["response"]}

@app.get("/api/admin/faqs")
def list_faqs(search: Optional[str] = None):
    faqs = get_all_faqs(search)
    return {"faqs": faqs, "total": len(faqs)}

@app.post("/api/admin/faqs")
def add_faq(body: FAQBody):
    new_id = create_faq(body.category, body.question, body.answer, body.keywords)
    return {"id": new_id, "message": "FAQ created."}

@app.put("/api/admin/faqs/{faq_id}")
def edit_faq(faq_id: int, body: FAQBody):
    ok = update_faq(faq_id, body.category, body.question, body.answer, body.keywords)
    if not ok:
        raise HTTPException(404, "FAQ not found.")
    return {"message": "FAQ updated."}

@app.delete("/api/admin/faqs/{faq_id}")
def remove_faq(faq_id: int):
    ok = delete_faq(faq_id)
    if not ok:
        raise HTTPException(404, "FAQ not found.")
    return {"message": "FAQ deleted."}

@app.get("/api/admin/analytics")
def analytics():
    return get_dashboard_analytics()

@app.get("/health")
def health():
    return {"status": "ok"}
