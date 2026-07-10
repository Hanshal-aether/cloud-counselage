import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
model = None

if GEMINI_KEY and GEMINI_KEY != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("[AI] Gemini ready.")
    except Exception as e:
        print(f"[AI] Gemini setup failed: {e}")
else:
    print("[AI] No Gemini key. Using fallback responses.")

def get_ai_response(query: str) -> str:
    if model:
        try:
            prompt = (
                "You are a helpful support assistant for CloudCounselage Pvt. Ltd., "
                "an Indian IT company running free internship programs for students under the GPI program. "
                "Answer the student's question in 2-3 clear sentences. Be friendly and helpful.\n\n"
                f"Student question: {query}"
            )
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[AI] Gemini error: {e}")

    # Keyword fallback
    q = query.lower()
    if any(w in q for w in ["certificate", "letter", "credential"]):
        return "Experience Certificates are awarded to interns who complete all tasks and submit their deliverables. For verification, email hr@cloudcounselage.com with your certificate ID."
    if any(w in q for w in ["paid", "stipend", "salary", "fee", "cost"]):
        return "The internship is 100% free and unpaid. There are no charges or stipends — the focus is on learning and gaining real project experience."
    if any(w in q for w in ["apply", "join", "register", "onboard"]):
        return "Register on the IAC portal, complete the preparation modules, and fill out the New Joinee Form. Your Appointment Letter will be emailed after document verification."
    if any(w in q for w in ["contact", "email", "support", "help"]):
        return "For general queries email welcome@cloudcounselage.com. For HR or certificate issues email hr@cloudcounselage.com."
    if any(w in q for w in ["hello", "hi", "hey"]):
        return "Hello! I'm the CloudCounselage Support Bot. Ask me anything about the GPI internship program — onboarding, certificates, deadlines, or general support."

    return (
        "I'm not fully sure about that specific query. "
        "Please email welcome@cloudcounselage.com or ask in your domain's Telegram/WhatsApp group for accurate help."
    )
