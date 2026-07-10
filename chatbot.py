import difflib
from database import get_all_faqs, get_or_create_conversation, save_message, get_conversation_history
from ai_service import get_ai_response

THRESHOLD = 0.45

def clean(text: str) -> str:
    text = text.lower().strip()
    for ch in ["?", "!", ".", ",", ";", ":", "-", "_", "(", ")", "'"]:
        text = text.replace(ch, "")
    return " ".join(text.split())

def find_faq(query: str, faqs: list):
    cq = clean(query)
    best, score = None, 0.0
    for faq in faqs:
        cf = clean(faq["question"])
        # Sequence ratio
        seq = difflib.SequenceMatcher(None, cq, cf).ratio()
        # Word overlap
        qw, fw = set(cq.split()), set(cf.split())
        overlap = len(qw & fw) / max(len(qw), len(fw)) if qw and fw else 0
        s = max(seq, overlap)
        if cq in cf or cf in cq:
            s = max(s, 0.8)
        if s > score:
            score, best = s, faq
    return (best, score) if score >= THRESHOLD else (None, score)

def handle_user_query(conversation_id: str, channel: str, user_identifier: str, query: str) -> dict:
    get_or_create_conversation(conversation_id, channel, user_identifier)
    save_message(conversation_id, "user", query)

    faqs = get_all_faqs()
    faq_match, score = find_faq(query, faqs)

    if faq_match:
        reply = faq_match["answer"]
        is_ai = False
        faq_id = faq_match["id"]
    else:
        reply = get_ai_response(query)
        is_ai = True
        faq_id = None

    save_message(conversation_id, "bot", reply, is_ai=is_ai, faq_id=faq_id)

    return {
        "conversation_id": conversation_id,
        "response": reply,
        "is_ai_generated": is_ai,
        "match_score": round(score, 2)
    }
