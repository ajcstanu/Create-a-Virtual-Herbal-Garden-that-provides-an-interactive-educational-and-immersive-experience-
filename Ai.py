"""
AI Herb Guide route
POST /api/ai/chat   - chat with Vanaspati AI (uses Anthropic API)
GET  /api/ai/suggest - get plant suggestions for a symptom/condition
"""

import os
from flask import Blueprint, request, jsonify, current_app
from app.models.plant import Plant

ai_bp = Blueprint("ai", __name__)


SYSTEM_PROMPT = """You are Vanaspati, a knowledgeable and warm AI guide specialising in Ayurvedic \
medicinal plants, herbs, and the AYUSH system of traditional Indian medicine. Your role is to \
educate users about medicinal plants, their uses, preparation methods, and Ayurvedic wisdom.

Guidelines:
- Be accurate, educational, and friendly
- Keep responses concise (2–5 sentences) unless deeper explanation is requested
- Use simple language accessible to students and enthusiasts
- Reference specific plants from the Vanaspati garden when relevant
- ALWAYS remind users to consult a qualified Ayurvedic practitioner or healthcare professional \
  before using any herb medicinally, especially if they have existing health conditions
- Never diagnose medical conditions or replace professional medical advice
- Use emojis sparingly to add warmth (🌿🌱)

You have knowledge of these plants in the Vanaspati garden:
{plant_list}
"""


def _build_system_prompt() -> str:
    plants = Plant.query.order_by(Plant.name).all()
    lines  = [f"• {p.name} ({p.botanical}): {', '.join(p.uses[:3])}" for p in plants]
    return SYSTEM_PROMPT.format(plant_list="\n".join(lines))


def _ok(data, **kw):
    return jsonify({"success": True, "data": data, **kw})


def _err(msg, code=400):
    return jsonify({"success": False, "error": msg}), code


@ai_bp.route("/chat", methods=["POST"])
def chat():
    """
    Body: { "message": "...", "history": [{"role": "user"|"assistant", "content": "..."}] }
    """
    data    = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return _err("'message' is required")

    history = data.get("history", [])
    # Validate history structure
    valid_history = [
        {"role": h["role"], "content": h["content"]}
        for h in history
        if isinstance(h, dict) and h.get("role") in ("user", "assistant") and h.get("content")
    ]

    api_key = current_app.config.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        # Fallback: return a helpful static response
        return _ok({
            "reply": (
                "Namaste! 🌿 I'm your Vanaspati herb guide. "
                "The AI service is not configured — please set ANTHROPIC_API_KEY in your .env file. "
                "In the meantime, explore the garden to learn about each plant's detailed uses!"
            )
        })

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        messages = valid_history + [{"role": "user", "content": message}]

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            system=_build_system_prompt(),
            messages=messages,
        )

        reply = response.content[0].text if response.content else "I couldn't process that. Please try again."
        return _ok({"reply": reply})

    except Exception as exc:
        current_app.logger.error(f"AI chat error: {exc}")
        return _err("AI service temporarily unavailable. Please try again later.", 503)


@ai_bp.route("/suggest", methods=["GET"])
def suggest():
    """
    Query: ?condition=headache  → returns matching plants
    """
    condition = request.args.get("condition", "").strip().lower()
    if not condition:
        return _err("'condition' query parameter is required")

    like  = f"%{condition}%"
    plants = (
        Plant.query
        .filter(
            db.or_(
                Plant._uses.ilike(like),
                Plant.desc.ilike(like),
                Plant.about.ilike(like),
            )
        )
        .limit(6)
        .all()
    )

    # Import here to avoid circular imports
    from app import db

    return _ok([p.to_dict(brief=True) for p in plants])
