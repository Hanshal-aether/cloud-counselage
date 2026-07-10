import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
model = None

if GEMINI_KEY and GEMINI_KEY.strip() and GEMINI_KEY != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=GEMINI_KEY.strip())
        # Try flash first, fall back to pro
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            # Test it works
            model.generate_content("hi")
            print("[AI] Gemini 1.5 Flash ready.")
        except Exception:
            model = genai.GenerativeModel("gemini-pro")
            print("[AI] Gemini Pro ready.")
    except Exception as e:
        print(f"[AI] Gemini setup failed: {e}")
        model = None
else:
    print("[AI] No Gemini key found. Using keyword fallback.")

SYSTEM_PROMPT = """You are a helpful support assistant for CloudCounselage Pvt. Ltd., an Indian IT company.
CloudCounselage runs the Global Professional Internship (GPI) program — free internships for students.
Key facts:
- Internship is 100% free, no fees, no stipend
- Duration: 6 weeks to 6 months, 120 hours total, self-paced
- 50+ domains: Python, AI/ML, Data Science, Web Dev, Marketing, HR, Finance etc
- Fully remote / work from home
- Students get Experience Certificate on completion
- LOR given to top performers
- Contact: welcome@cloudcounselage.com (general), hr@cloudcounselage.com (HR/certificates)
- Onboarding: Register on IAC portal → complete modules → fill New Joinee Form → get Appointment Letter in 5-7 days
- Deliverables: code/project files + project report + demo video
- IAC community has 5 lakh+ members across 40+ countries

Answer the student question in 2-4 sentences. Be friendly, clear and direct. Do not make up information."""

def get_ai_response(query: str) -> str:
    if model:
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\nStudent question: {query}\nAnswer:"
            response = model.generate_content(full_prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"[AI] Gemini call failed: {e}")

    # Keyword fallback — covers most common questions
    q = query.lower()

    if any(w in q for w in ["hello", "hi", "hey", "start"]):
        return "Hello! I'm the CloudCounselage Support Bot. Ask me anything about the GPI internship — onboarding, certificates, deadlines, domains, and more!"

    if any(w in q for w in ["how many", "number of", "programs", "types", "list", "available", "option"]):
        return "CloudCounselage offers internships in 50+ domains including Python Development, AI/ML, Data Science, Web Development (HTML/CSS/React), Digital Marketing, HR Management, Business Operations, Finance, and many more."

    if any(w in q for w in ["duration", "long", "weeks", "months", "hours", "time", "period", "days"]):
        return "The GPI internship typically runs for 6 weeks to 6 months and requires around 120 hours of self-paced work. It is fully flexible so you can balance it with your college schedule."

    if any(w in q for w in ["paid", "stipend", "salary", "money", "payment", "free", "cost", "fee", "charge"]):
        return "The internship is 100% free and unpaid. There are no fees to join and no stipend is offered. You get real project experience, mentor guidance, and an official Experience Certificate."

    if any(w in q for w in ["certificate", "experience letter", "completion", "credential"]):
        return "Yes! You receive an official Experience Certificate from CloudCounselage Pvt. Ltd. after completing all tasks, submitting deliverables, and passing the evaluation."

    if any(w in q for w in ["lor", "recommendation", "letter of recommendation"]):
        return "Letters of Recommendation are given to top-performing interns who complete tasks early, add advanced features, and actively help peers in community groups."

    if any(w in q for w in ["apply", "join", "register", "how to start", "onboard", "enroll", "get started"]):
        return "To join: 1) Register on the IAC portal, 2) Complete the preparation modules, 3) Fill the New Joinee Form with your documents. Your Appointment Letter will be emailed within 5-7 business days."

    if any(w in q for w in ["appointment", "offer letter", "joining letter"]):
        return "Your Appointment Letter is issued within 5-7 business days after submitting the onboarding form and document verification by HR."

    if any(w in q for w in ["domain", "field", "subject", "branch", "python", "data science", "web", "ai", "ml", "marketing", "hr", "finance"]):
        return "CloudCounselage offers 50+ domains including Python, AI/ML, Data Science, Web Development, Digital Marketing, HR, Business Operations, Finance, and more."

    if any(w in q for w in ["remote", "wfh", "work from home", "online", "location", "office"]):
        return "All GPI internships are 100% remote and work-from-home. You can work from anywhere as long as you meet weekly milestones."

    if any(w in q for w in ["submit", "deliverable", "submission", "project report", "video", "what to submit"]):
        return "You need to submit: 1) Completed project code or files, 2) A project report covering tools and methodology, 3) A short demo video. All via the IAC portal."

    if any(w in q for w in ["deadline", "extension", "late", "miss", "delay"]):
        return "If you need more time, request an extension in writing to your project manager before the deadline. Unauthorized late submissions may delay your certificate."

    if any(w in q for w in ["contact", "email", "support", "reach", "help"]):
        return "For general queries: welcome@cloudcounselage.com\nFor HR/certificate issues: hr@cloudcounselage.com\nFor technical help: post in your domain Telegram/WhatsApp group."

    if any(w in q for w in ["meeting", "weekly", "check in", "review", "attendance"]):
        return "Yes, interns must attend weekly virtual check-in meetings to review progress, discuss blockers, and confirm milestones are on track."

    if any(w in q for w in ["mentor", "communicate", "whatsapp", "telegram", "group", "community"]):
        return "Communication is through official domain-specific WhatsApp and Telegram groups. Use these to ask questions, get feedback, and connect with your mentor."

    if any(w in q for w in ["genuine", "real", "fraud", "scam", "legit", "fake", "trust", "safe"]):
        return "CloudCounselage is a legitimate registered company. All programs are completely free — we never ask for payment. Only trust emails from @cloudcounselage.com."

    if any(w in q for w in ["iac", "industry academia", "community", "about", "what is"]):
        return "CloudCounselage is an IT company with a social mission to make students job-ready. The IAC (Industry Academia Community) is their free platform connecting 5 lakh+ students across 40+ countries with industry mentors."

    if any(w in q for w in ["evaluate", "grading", "marks", "score", "criteria", "pass", "fail"]):
        return "Your project is evaluated by industry mentors based on functionality, code quality, documentation, and your demo video. A minimum passing score is required to receive the certificate."

    if any(w in q for w in ["mumbai", "bkc", "vikhroli", "address", "headquarters"]):
        return "CloudCounselage is based in Mumbai, India. BKC office: 91 Springboard, Kagalwala House, BKC Kalina, Mumbai 400098."

    return "I'm not fully sure about that. Please email welcome@cloudcounselage.com or ask in your domain's Telegram/WhatsApp group. You can also rephrase your question and I'll try again!"
