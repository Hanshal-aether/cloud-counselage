import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()
model = None

SYSTEM_PROMPT = """You are a helpful support assistant for CloudCounselage Pvt. Ltd., an Indian IT company that runs free internship programs for students.

About CloudCounselage & GPI:
- GPI = Global Professional Internship — free, unpaid, work from home, 120 hours, 6 weeks to 6 months
- 50+ domains: Python, AI/ML, Data Science, Web Dev, Digital Marketing, HR, Finance etc
- Students get Experience Certificate on completion, LOR for top performers
- Onboarding: Register on IAC portal → complete modules → fill New Joinee Form → Appointment Letter in 5-7 days
- Submit: code/project files + project report + demo video
- Contact: welcome@cloudcounselage.com (general), hr@cloudcounselage.com (HR/certificates)
- IAC community: 5 lakh+ members, 40+ countries
- Office: Mumbai, BKC and Vikhroli

Rules:
- Answer any question a student asks, not just about internships
- If someone says their name or asks casual questions, respond naturally and friendly
- Keep answers to 2-3 sentences
- Never say you don't know basic things
- If truly unsure, say email welcome@cloudcounselage.com"""

if GEMINI_KEY and GEMINI_KEY != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=GEMINI_KEY)
        # gemini-2.0-flash is the latest free model
        for model_name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_PROMPT
                )
                # Quick test
                test = model.generate_content("say ok")
                if test and test.text:
                    print(f"[AI] {model_name} ready.")
                    break
            except Exception as e:
                print(f"[AI] {model_name} failed: {e}")
                model = None
                continue
    except Exception as e:
        print(f"[AI] Gemini init failed: {e}")
        model = None
else:
    print("[AI] No Gemini key. Using keyword fallback.")

def get_ai_response(query: str) -> str:
    if model:
        try:
            response = model.generate_content(query)
            if response and response.text and len(response.text.strip()) > 5:
                return response.text.strip()
        except Exception as e:
            print(f"[AI] Gemini call error: {e}")

    # Smart keyword fallback
    q = query.lower()

    # Greetings and casual
    if any(w in q for w in ["hello", "hi ", "hey", "good morning", "good evening", "hii", "helo"]):
        return "Hello! I'm the CloudCounselage Support Bot. Ask me anything about the GPI internship — onboarding, certificates, deadlines, domains, and more!"

    if "name" in q and any(w in q for w in ["my", "i am", "i'm", "call me", "is"]):
        name = query.strip().split()[-1] if query.strip() else "there"
        return f"Nice to meet you! I'm the CloudCounselage Support Bot. How can I help you with the GPI internship today?"

    if any(w in q for w in ["who built", "who made", "who created", "who developed", "built this"]):
        return "This platform was built by Hanshal Gajula as part of the CloudCounselage GPI internship project — an AI-powered multi-channel student support system."

    if any(w in q for w in ["what is this", "what are you", "what can you do", "tell me about"]):
        return "I'm an AI support bot for CloudCounselage's GPI internship program. I can answer questions about joining, certificates, deadlines, domains, onboarding, and anything else about the internship!"

    if any(w in q for w in ["how many", "number of", "programs", "types", "list", "available", "option", "which"]):
        return "CloudCounselage offers internships in 50+ domains including Python, AI/ML, Data Science, Web Development, Digital Marketing, HR, Business Operations, Finance, and many more!"

    if any(w in q for w in ["duration", "long", "weeks", "months", "hours", "time", "period", "days", "how long"]):
        return "The GPI internship runs for 6 weeks to 6 months and requires around 120 hours of self-paced work. It's fully flexible so you can balance it with college."

    if any(w in q for w in ["paid", "stipend", "salary", "money", "payment", "free", "cost", "fee", "charge"]):
        return "The internship is 100% free and unpaid — no fees to join, no stipend. You get real project experience, mentor support, and an official Experience Certificate."

    if any(w in q for w in ["certificate", "experience letter", "completion", "credential"]):
        return "Yes! You receive an official Experience Certificate from CloudCounselage after completing all tasks, submitting deliverables, and passing the evaluation."

    if any(w in q for w in ["lor", "recommendation", "letter of recommendation"]):
        return "Letters of Recommendation are given to top-performing interns who finish tasks early, add advanced features, and actively support peers in community groups."

    if any(w in q for w in ["apply", "join", "register", "how to start", "onboard", "enroll", "get started", "begin"]):
        return "To join: 1) Register on the IAC portal, 2) Complete the preparation modules, 3) Fill the New Joinee Form. Your Appointment Letter arrives by email in 5-7 business days."

    if any(w in q for w in ["appointment", "offer letter", "joining letter"]):
        return "Your Appointment Letter is issued within 5-7 business days after the HR team verifies your submitted onboarding documents."

    if any(w in q for w in ["domain", "field", "subject", "python", "data science", "web", "ai", "ml", "marketing", "hr", "finance"]):
        return "CloudCounselage offers 50+ internship domains: Python, AI/ML, Data Science, Web Development, Digital Marketing, HR, Business Operations, Finance, and more!"

    if any(w in q for w in ["remote", "wfh", "work from home", "online", "location", "office", "where"]):
        return "All GPI internships are 100% remote and work-from-home. Work from anywhere as long as you meet weekly milestones."

    if any(w in q for w in ["submit", "deliverable", "submission", "project report", "video", "what to submit"]):
        return "Submit: 1) Your completed project code, 2) A project report covering tools and methodology, 3) A short demo video — all through the IAC portal."

    if any(w in q for w in ["deadline", "extension", "late", "miss", "delay", "last date"]):
        return "If you need more time, request an extension in writing to your project manager before the deadline. Late submissions without approval may delay your certificate."

    if any(w in q for w in ["contact", "email", "support", "reach", "help", "talk to"]):
        return "General queries: welcome@cloudcounselage.com\nHR/certificates: hr@cloudcounselage.com\nTechnical help: post in your domain's Telegram or WhatsApp group."

    if any(w in q for w in ["meeting", "weekly", "check in", "review", "attendance", "webinar"]):
        return "Yes, interns attend weekly virtual check-in meetings to review progress, solve blockers, and confirm milestones are on track."

    if any(w in q for w in ["mentor", "communicate", "whatsapp", "telegram", "group", "community", "peer"]):
        return "Communication is through official domain-specific WhatsApp and Telegram groups. Use these to ask questions and get mentor feedback."

    if any(w in q for w in ["genuine", "real", "fraud", "scam", "legit", "fake", "trust", "safe", "verify"]):
        return "CloudCounselage is a legitimate registered company. All programs are completely free — we never ask for payment. Trust only emails from @cloudcounselage.com."

    if any(w in q for w in ["iac", "industry academia", "community", "about cloudcounselage", "what is cloud"]):
        return "CloudCounselage is an IT company with a mission to make students job-ready. Their IAC (Industry Academia Community) has 5 lakh+ members across 40+ countries."

    if any(w in q for w in ["evaluate", "grading", "marks", "score", "criteria", "pass", "fail", "assessment"]):
        return "Your project is evaluated on functionality, code quality, documentation, and demo video. A minimum passing score is required to receive the certificate."

    if any(w in q for w in ["mumbai", "bkc", "vikhroli", "address", "headquarters", "location of office"]):
        return "CloudCounselage is based in Mumbai. BKC: 91 Springboard, Kagalwala House, BKC Kalina, Mumbai 400098. Vikhroli: 91 Springboard, Godrej & Boyce Estate, Vikhroli West."

    if any(w in q for w in ["thank", "thanks", "great", "awesome", "nice", "good", "perfect", "helpful"]):
        return "You're welcome! Feel free to ask if you have more questions about the internship. Good luck! 🎉"

    if any(w in q for w in ["bye", "goodbye", "see you", "take care", "ciao"]):
        return "Goodbye! Best of luck with your internship. Feel free to come back anytime you have questions!"

    return "That's a great question! For the most accurate answer, please email welcome@cloudcounselage.com or ask in your domain's Telegram/WhatsApp group. You can also rephrase your question and I'll do my best!"
