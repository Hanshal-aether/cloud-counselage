# CloudCounselage Support Bot

## Folder Structure
```
project/
├── main.py
├── database.py
├── ai_service.py
├── chatbot.py
├── faqs.json
├── requirements.txt
├── vercel.json
├── .env
└── static/
    ├── index.html
    ├── styles.css
    └── app.js
```

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Open http://localhost:8000

## Deploy on Railway (Recommended for Telegram)
1. Push this folder to GitHub
2. Go to railway.app → New Project → Deploy from GitHub
3. Add environment variables: GEMINI_API_KEY and TELEGRAM_BOT_TOKEN
4. Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
5. After deploy, visit: https://yourapp.railway.app/setup-telegram?url=https://yourapp.railway.app

## Deploy on Vercel (Web only - Telegram won't work)
1. Push to GitHub
2. Go to vercel.com → New Project → Import repo
3. Add environment variables: GEMINI_API_KEY and TELEGRAM_BOT_TOKEN
4. Deploy

Note: Vercel does not support persistent webhooks needed for Telegram.
Use Railway for full Telegram support.
