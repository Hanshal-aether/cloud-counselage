# 🤖 CloudCounselage AI Support Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Railway](https://img.shields.io/badge/Deployed_on-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

**An AI-powered multi-channel student support chatbot for the CloudCounselage GPI Internship Program**

[🌐 Live Demo](https://cloud-counselage-production.up.railway.app/) &nbsp;·&nbsp; [✈️ Telegram Bot](https://t.me/ccgpi_bot) &nbsp;·&nbsp; [🐛 Report Bug](https://github.com/Hanshal-aether/cloud-counselage/issues)

</div>

---

## 📌 What is this?

This is an intelligent chatbot platform built for **CloudCounselage Pvt. Ltd.** to automatically handle student queries about the **Global Professional Internship (GPI)** program across multiple communication channels.

Students ask hundreds of questions every day — about onboarding, certificates, deadlines, domains, and more. This system answers them instantly, 24/7, without any manual intervention.

---

## ✨ Features

- 💬 **Web Chat Interface** — Clean, responsive chat UI accessible from any browser
- ✈️ **Telegram Bot** — Live bot that replies to student queries in real time  
- 🎨 **Platform Themes** — Switch between Web, Telegram, WhatsApp, Messenger, and Instagram UI themes
- 🎤 **Voice Input** — Click the mic and speak your question
- 🧠 **Smart FAQ Matching** — Fuzzy string matching finds the right answer even with typos
- 🤖 **Gemini AI Fallback** — Google Gemini handles questions outside the knowledge base
- 📋 **FAQ Admin Panel** — Add, edit, and delete FAQs without touching code
- 📊 **Analytics Dashboard** — Track conversations, query volumes, and resolution rates
- 🗄️ **Conversation Logging** — Every interaction stored in SQLite for review

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite |
| AI | Google Gemini 2.0 Flash |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js |
| Messaging | Telegram Bot API |
| Deployment | Railway.app |
| Version Control | GitHub |

---

## 🏗️ Project Structure

```
cloud-counselage/
├── main.py              # FastAPI server — all routes & webhook handlers
├── chatbot.py           # FAQ fuzzy matching engine
├── ai_service.py        # Gemini AI + keyword fallback responses
├── database.py          # SQLite setup, CRUD, analytics queries
├── faqs.json            # Knowledge base — 20 FAQ entries
├── requirements.txt     # Python dependencies
└── static/
    ├── index.html       # Single-page app
    ├── styles.css       # All styles + 5 platform themes
    └── app.js           # Frontend logic, API calls, voice input
```

---

## 🚀 How It Works

```
Student sends a message
        │
        ▼
  FAQ Fuzzy Matching
  (difflib SequenceMatcher + word overlap)
        │
        ├── Score ≥ 0.60 ──► Return verified FAQ answer
        │
        └── Score < 0.60 ──► Google Gemini AI
                                  │
                                  ├── API available ──► AI-generated response
                                  │
                                  └── Unavailable ──► Smart keyword fallback
                                            │
                                            ▼
                                  Log to SQLite → Send reply to user
```

---

## ⚙️ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Hanshal-aether/cloud-counselage.git
cd cloud-counselage
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file in the root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

Open **http://localhost:8000**

---

## 🔑 Getting API Keys

**Gemini API Key** (free)
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** → **Create API key**
3. Copy the key — it starts with `AIza...`

**Telegram Bot Token**
1. Open Telegram → search **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the bot token it gives you

---

## 🌍 Deploy on Railway

1. Fork this repo
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
3. Add environment variables: `GEMINI_API_KEY` and `TELEGRAM_BOT_TOKEN`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. After deploy, register the Telegram webhook by visiting:
```
https://your-app.railway.app/setup-telegram?url=https://your-app.railway.app
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Web chat message |
| `GET` | `/api/chat/history/{session_id}` | Conversation history |
| `POST` | `/webhook/telegram` | Telegram webhook receiver |
| `GET` | `/setup-telegram?url=` | Register Telegram webhook |
| `GET` | `/api/admin/faqs` | List all FAQs |
| `POST` | `/api/admin/faqs` | Add new FAQ |
| `PUT` | `/api/admin/faqs/{id}` | Update FAQ |
| `DELETE` | `/api/admin/faqs/{id}` | Delete FAQ |
| `GET` | `/api/admin/analytics` | Dashboard data |
| `GET` | `/health` | Health check |

---

## 🤝 About This Project

Built by **Hanshal Gajula** as part of the **CloudCounselage Global Professional Internship (GPI)** program.

| | |
|---|---|
| **Organization** | Cloud Counselage Pvt. Ltd. |
| **Program** | Global Professional Internship (GPI) — 120 Hours |
| **Domain** | Artificial Intelligence |
| **Duration** | April 2026 – July 2026 |
| **Mentor** | Marakand Jena |

---

<div align="center">
Made with ❤️ by <a href="https://github.com/Hanshal-aether">Hanshal Gajula</a>
</div>
