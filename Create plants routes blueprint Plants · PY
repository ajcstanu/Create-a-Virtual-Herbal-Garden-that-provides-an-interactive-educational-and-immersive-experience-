"""
Plants API routes
GET  /api/plants/           - list all (search, filter, paginate)
GET  /api/plants/<id>       - detail
POST /api/plants/           - create (admin)
PUT  /api/plants/<id>       - update (admin)
DELETE /api/plants/<id>     - delete (admin)
GET  /api/plants/categories - list categories
GET  /api/plants/regions    - list regions
GET  /api/plants/<id>/related - related plants
"""

from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.plant import Plant

plants_bp = Blueprint("plants", __name__)


# ── helpers ──────────────────────────────────────────────────────────────────

def _paginate_args():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 50)
    return page, per_page


def _ok(data, **kwargs):
    return jsonify({"success": True, "data": data, **kwargs})


def _err(msg, code=400):
    return jsonify({"success": False, "error": msg}), code


# ── routes ───────────────────────────────────────────────────────────────────

@plants_bp.route("/", methods=["GET"])
def list_plants():
    """
    Query params:
        q        - full-text search (name / botanical / common_names / uses)
        category - filter by category slug
        region   - filter by region slug
        page     - page number (default 1)
        per_page - results per page (default 12, max 50)
        brief    - if '1' return compact representation
    """
    q        = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    region   = request.args.get("region", "").strip().lower()
    brief    = request.args.get("brief", "0") == "1"
    page, per_page = _paginate_args()

    query = Plant.query

    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                Plant.name.ilike(like),
                Plant.botanical.ilike(like),
                Plant._common_names.ilike(like),
                Plant._uses.ilike(like),
                Plant.desc.ilike(like),
            )
        )

    if category:
        query = query.filter(Plant._categories.ilike(f"%{category}%"))

    if region:
        query = query.filter(Plant.region == region)

    total    = query.count()
    plants   = query.order_by(Plant.name).paginate(page=page, per_page=per_page, error_out=False)

    return _ok(
        [p.to_dict(brief=brief) for p in plants.items],
        total=total,
        page=page,
        per_page=per_page,
        pages=plants.pages,
    )


@plants_bp.route("/<int:plant_id>", methods=["GET"])
def get_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id, description=f"Plant {plant_id} not found")
    return _ok(plant.to_dict())


@plants_bp.route("/", methods=["POST"])
def create_plant():
    data = request.get_json(silent=True)
    if not data:
        return _err("JSON body required")

    required = ["name", "botanical"]
    for field in required:
        if not data.get(field):
            return _err(f"'{field}' is required")

    if Plant.query.filter_by(botanical=data["botanical"]).first():
        return _err("A plant with this botanical name already exists", 409)

    plant = Plant(
        name=data["name"],
        botanical=data["botanical"],
        emoji=data.get("emoji", "🌿"),
        color=data.get("color", "#e8f5e9"),
        region=data.get("region"),
        family=data.get("family"),
        ayurvedic_system=data.get("ayurvedic_system"),
        taste=data.get("taste"),
        part_used=data.get("part_used"),
        season=data.get("season"),
        desc=data.get("desc"),
        about=data.get("about"),
        prep=data.get("prep"),
        compounds=data.get("compounds"),
        habitat=data.get("habitat"),
        image_url=data.get("image_url"),
        model_3d_url=data.get("model_3d_url"),
        video_url=data.get("video_url"),
        audio_url=data.get("audio_url"),
    )
    plant.common_names = data.get("common_names", [])
    plant.categories   = data.get("categories", [])
    plant.uses         = data.get("uses", [])
    plant.cultivation  = data.get("cultivation", [])

    db.session.add(plant)
    db.session.commit()
    return _ok(plant.to_dict()), 201


@plants_bp.route("/<int:plant_id>", methods=["PUT"])
def update_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    data  = request.get_json(silent=True) or {}

    str_fields = [
        "name", "botanical", "emoji", "color", "region", "family",
        "ayurvedic_system", "taste", "part_used", "season",
        "desc", "about", "prep", "compounds", "habitat",
        "image_url", "model_3d_url", "video_url", "audio_url",
    ]
    for f in str_fields:
        if f in data:
            setattr(plant, f, data[f])

    list_fields = ["common_names", "categories", "uses", "cultivation"]
    for f in list_fields:
        if f in data:
            setattr(plant, f, data[f])

    db.session.commit()
    return _ok(plant.to_dict())


@plants_bp.route("/<int:plant_id>", methods=["DELETE"])
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    return _ok({"deleted": plant_id})


@plants_bp.route("/categories", methods=["GET"])
def list_categories():
    categories = [
        {"slug": "digest",      "label": "Digestive Health",  "emoji": "🫁"},
        {"slug": "immunity",    "label": "Immunity",           "emoji": "🛡️"},
        {"slug": "skin",        "label": "Skin Care",          "emoji": "✨"},
        {"slug": "stress",      "label": "Stress & Mind",      "emoji": "🧠"},
        {"slug": "pain",        "label": "Pain Relief",        "emoji": "💪"},
        {"slug": "respiratory", "label": "Respiratory Health", "emoji": "🌬️"},
    ]
    return _ok(categories)


@plants_bp.route("/regions", methods=["GET"])
def list_regions():
    regions = [
        {"slug": "himalayan",  "label": "Himalayan"},
        {"slug": "tropical",   "label": "Tropical India"},
        {"slug": "deccan",     "label": "Deccan Plateau"},
        {"slug": "coastal",    "label": "Coastal"},
        {"slug": "pan-india",  "label": "Pan-India"},
    ]
    return _ok(regions)


@plants_bp.route("/<int:plant_id>/related", methods=["GET"])
def related_plants(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    cats  = plant.categories
    if not cats:
        return _ok([])

    related = (
        Plant.query
        .filter(Plant.id != plant_id)
        .filter(
            db.or_(*[Plant._categories.ilike(f"%{c}%") for c in cats])
        )
        .limit(4)
        .all()
    )
    return _ok([p.to_dict(brief=True) for p in related])
