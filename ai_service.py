import os
import re
from dotenv import load_dotenv

load_dotenv()

# Try Gemini but don't depend on it
model = None
try:
    import google.generativeai as genai
    GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    if GEMINI_KEY and GEMINI_KEY != "your_gemini_api_key_here":
        genai.configure(api_key=GEMINI_KEY)
        for name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-pro"]:
            try:
                m = genai.GenerativeModel(name)
                r = m.generate_content("say hi")
                if r and r.text:
                    model = m
                    print(f"[AI] {name} ready.")
                    break
            except:
                continue
except Exception as e:
    print(f"[AI] Gemini unavailable: {e}")

SYSTEM = """You are a helpful, friendly AI support assistant for CloudCounselage Pvt. Ltd.
CloudCounselage runs the Global Professional Internship (GPI) — free internships for students.
Key facts: free/unpaid, 120 hours, 6 weeks-6 months, remote, 50+ domains, certificate on completion.
Respond naturally and helpfully in 2-3 sentences. For casual chat, be warm and conversational."""

def get_ai_response(query: str) -> str:
    # Try Gemini first
    if model:
        try:
            r = model.generate_content(f"{SYSTEM}\n\nUser: {query}\nAssistant:")
            if r and r.text and len(r.text.strip()) > 10:
                return r.text.strip()
        except Exception as e:
            print(f"[AI] Gemini error: {e}")

    return smart_fallback(query)


def smart_fallback(query: str) -> str:
    q = query.lower().strip()

    # ── Casual / Small talk ───────────────────────────────────
    if re.search(r'\b(hi|hello|hey|hii|helo|howdy|sup|wassup)\b', q):
        return "Hey! 👋 I'm the CloudCounselage Support Bot. I'm here to help with anything about the GPI internship — onboarding, certificates, deadlines, domains, or general questions. What would you like to know?"

    if re.search(r'\bhow are you\b', q):
        return "I'm doing great, thanks for asking! 😊 I'm always ready to help. What can I do for you today?"

    if re.search(r'\bwho are you\b', q):
        return "I'm the CloudCounselage AI Support Bot! I help students with questions about the GPI internship program — onboarding, certificates, project submissions, and more. Ask me anything!"

    if re.search(r'\b(who built|who made|who created|who developed|built this|made this)\b', q):
        return "This platform was built by Hanshal Gajula as part of the CloudCounselage GPI Internship project — a multi-channel AI-powered student support system."

    if re.search(r'\b(what is this|what are you|what can you do|your purpose|your role)\b', q):
        return "I'm an AI support assistant for CloudCounselage's GPI internship program. I can answer your questions about joining, certificates, deadlines, domains, onboarding, and anything else related to the internship!"

    if re.search(r'\b(thank|thanks|thank you|ty|thx|appreciate)\b', q):
        return "You're welcome! 😊 Feel free to ask if you have more questions. Good luck with your internship journey!"

    if re.search(r'\b(bye|goodbye|see you|take care|later|ciao)\b', q):
        return "Goodbye! 👋 Best of luck with your internship. Come back anytime you have questions!"

    if re.search(r'\bsorry\b', q):
        return "No worries at all! How can I help you today?"

    if re.search(r'\b(ok|okay|got it|understood|sure|alright|fine)\b', q):
        return "Great! Let me know if there's anything else you'd like to know about the internship. I'm here to help!"

    if re.search(r'(fuck|shit|damn|ass|stupid|idiot|hate|suck|crap)', q):
        return "I understand the frustration! Let me know what's bothering you and I'll do my best to help you out. 😊"

    if re.search(r'\b(my name is|i am|i\'m|call me)\b', q):
        words = q.split()
        name = words[-1].capitalize() if words else "there"
        return f"Nice to meet you, {name}! 😊 I'm the CloudCounselage Support Bot. How can I help you with the GPI internship today?"

    # ── Internship Core ───────────────────────────────────────
    if re.search(r'\b(what is gpi|what is the gpi|global professional|about gpi|about the internship|what is cloudcounselage|about cloud counselage)\b', q):
        return "The Global Professional Internship (GPI) by CloudCounselage is a free, structured internship program where students work on live projects under mentor guidance. It's 120 hours, fully remote, and available in 50+ domains — with a certificate on completion!"

    if re.search(r'\b(how many|number of|50\+|list of|available|which domain|what domain|all domain)\b', q) and re.search(r'\b(domain|program|field|course|internship|option)\b', q):
        return "CloudCounselage offers internships in 50+ domains! Popular ones include Python Development, AI/ML, Data Science, Web Development, Digital Marketing, HR Management, Business Operations, Finance, Cloud Computing, and many more."

    if re.search(r'\b(duration|how long|weeks|months|120 hours|time period|period|days|deadline)\b', q) and not re.search(r'\b(submission|project|task)\b', q):
        return "The GPI internship runs for 6 weeks to 6 months and requires around 120 hours of self-paced work. It's fully flexible — you can balance it easily with your college schedule!"

    if re.search(r'\b(paid|stipend|salary|money|payment|cost|fee|free|charge|unpaid)\b', q):
        return "The GPI internship is completely free and unpaid — no registration fees, no hidden charges, no stipend. What you gain is real project experience, mentor support, and an official Experience Certificate from CloudCounselage!"

    if re.search(r'\b(certificate|experience letter|completion letter|credential|certification)\b', q):
        return "Yes! 🎉 All interns who complete their tasks, submit deliverables, and pass the evaluation receive an official Experience Certificate from CloudCounselage Pvt. Ltd. It's a great addition to your resume!"

    if re.search(r'\b(lor|letter of recommendation|recommendation letter)\b', q):
        return "Letters of Recommendation (LOR) are awarded to top-performing interns who complete tasks early, implement advanced features, and actively support their peers in the community groups. Aim high and you'll get one!"

    if re.search(r'\b(apply|how to join|how to apply|join|register|enroll|get started|start the internship|how do i start|onboard)\b', q):
        return "To join the GPI internship: 1) Register on the IAC portal, 2) Complete the preparation and training modules, 3) Fill out the New Joinee Form with your documents. Your Appointment Letter will be emailed within 5-7 business days. It's that simple!"

    if re.search(r'\b(appointment letter|offer letter|joining letter|when will i get|letter status)\b', q):
        return "Your Appointment Letter is issued within 5-7 business days after you submit the onboarding form and your documents are verified by the HR team. Check your email regularly!"

    if re.search(r'\b(remote|work from home|wfh|online|offline|where do i work|location|from home)\b', q):
        return "Yes! All GPI internships are 100% remote and work-from-home. You can work from anywhere in the world as long as you meet the weekly milestones and attend check-in meetings."

    if re.search(r'\b(submit|submission|deliverable|what to submit|project report|demo video|how to submit)\b', q):
        return "To complete the internship, you need to submit: 1) Your completed project code or files, 2) A detailed project report covering tools, methodology, and outcomes, 3) A short demo video showcasing your project. All through the IAC portal!"

    if re.search(r'\b(miss|late|extension|delay|deadline extension|more time)\b', q):
        return "If you need more time, contact your project manager in writing and request an extension before the deadline. Late submissions without prior approval may delay your certificate issuance."

    if re.search(r'\b(contact|email|reach out|support|helpdesk|help desk|how to contact|get in touch)\b', q):
        return "You can reach CloudCounselage at:\n📧 General: welcome@cloudcounselage.com\n📧 HR/Certificates: hr@cloudcounselage.com\n💬 Technical: Post in your domain's Telegram or WhatsApp group!"

    if re.search(r'\b(meeting|weekly meeting|check.?in|review session|attendance|webinar|session)\b', q):
        return "Yes, interns are required to attend weekly virtual check-in meetings. These sessions help review progress, resolve blockers, and ensure you're on track with your milestones."

    if re.search(r'\b(mentor|communicate|whatsapp group|telegram group|community|peer|batch)\b', q):
        return "All communication happens through official domain-specific WhatsApp and Telegram groups. Your mentor will be available there to guide you, answer questions, and give feedback on your work."

    if re.search(r'\b(fake|fraud|scam|genuine|legit|real|safe|trust|verify|authentic)\b', q):
        return "CloudCounselage is a legitimate, registered IT company based in Mumbai. All programs are 100% free — they will never ask for payment or bank details. Only trust communications from @cloudcounselage.com email IDs."

    if re.search(r'\b(iac|industry academia|community|about cc|cloudcounselage)\b', q):
        return "CloudCounselage operates the Industry Academia Community (IAC) — a free platform with 5 lakh+ members across 40+ countries. It connects students, colleges, and industry professionals for internships, mentorship, and job opportunities."

    if re.search(r'\b(evaluate|evaluation|grading|marks|score|how am i judged|criteria|pass|fail|assessment)\b', q):
        return "Your project is evaluated by industry mentors based on: functionality of your project, code quality, documentation accuracy, and your demo video. A minimum passing score is required to receive the certificate."

    if re.search(r'\b(mumbai|bkc|vikhroli|address|office|headquarters)\b', q):
        return "CloudCounselage has offices in Mumbai:\n🏢 BKC: 91 Springboard, Kagalwala House, BKC Kalina, Mumbai 400098\n🏢 Vikhroli: 91 Springboard, Godrej & Boyce Estate, Vikhroli West, Mumbai 400079"

    if re.search(r'\b(task|assignment|work|project|what do i do|what should i do|my work)\b', q):
        return "As a GPI intern, you'll work on a live project assigned to you based on your domain. You attend weekly webinars, complete tasks, document your progress, and submit your final project with a report and demo video."

    if re.search(r'\b(IAC portal|portal|dashboard|platform|website|where to submit)\b', q):
        return "The IAC portal is the main platform where you register, access training modules, submit your work, and track your internship progress. You'll receive the portal link during onboarding."

    # ── Default ───────────────────────────────────────────────
    return (
        "Thanks for your question! 😊 I'm focused on the CloudCounselage GPI internship program. "
        "For more specific queries, feel free to email welcome@cloudcounselage.com "
        "or ask your question in your domain's Telegram/WhatsApp group where mentors are active!"
    )
