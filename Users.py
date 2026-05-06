"""
User API routes
POST /api/users/register      - register
POST /api/users/login         - login → JWT token
GET  /api/users/me            - profile (JWT required)

GET  /api/users/bookmarks     - list bookmarks (JWT)
POST /api/users/bookmarks     - add bookmark (JWT)
DELETE /api/users/bookmarks/<plant_id> - remove bookmark (JWT)

GET  /api/users/notes         - list notes (JWT)
POST /api/users/notes         - save/update note (JWT)
DELETE /api/users/notes/<plant_id> - delete note (JWT)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from app import db
from app.models.user import User, Bookmark, Note
from app.models.plant import Plant

users_bp = Blueprint("users", __name__)


def _ok(data, **kw):
    return jsonify({"success": True, "data": data, **kw})


def _err(msg, code=400):
    return jsonify({"success": False, "error": msg}), code


# ── Auth ──────────────────────────────────────────────────────────────────────

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return _err("JSON body required")

    for f in ["username", "email", "password"]:
        if not data.get(f):
            return _err(f"'{f}' is required")

    if User.query.filter_by(email=data["email"]).first():
        return _err("Email already registered", 409)
    if User.query.filter_by(username=data["username"]).first():
        return _err("Username already taken", 409)

    user = User(username=data["username"], email=data["email"])
    user.password = data["password"]
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return _ok({"user": user.to_dict(), "access_token": token}), 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return _err("JSON body required")

    user = User.query.filter_by(email=data.get("email", "")).first()
    if not user or not user.check_password(data.get("password", "")):
        return _err("Invalid email or password", 401)
    if not user.is_active:
        return _err("Account is inactive", 403)

    token = create_access_token(identity=str(user.id))
    return _ok({"user": user.to_dict(), "access_token": token})


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def profile():
    uid  = int(get_jwt_identity())
    user = User.query.get_or_404(uid)
    return _ok(user.to_dict())


# ── Bookmarks ─────────────────────────────────────────────────────────────────

@users_bp.route("/bookmarks", methods=["GET"])
@jwt_required()
def list_bookmarks():
    uid  = int(get_jwt_identity())
    bks  = Bookmark.query.filter_by(user_id=uid).order_by(Bookmark.created_at.desc()).all()
    return _ok([b.to_dict() for b in bks], total=len(bks))


@users_bp.route("/bookmarks", methods=["POST"])
@jwt_required()
def add_bookmark():
    uid  = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    pid  = data.get("plant_id")
    if not pid:
        return _err("'plant_id' is required")

    plant = Plant.query.get(pid)
    if not plant:
        return _err("Plant not found", 404)

    existing = Bookmark.query.filter_by(user_id=uid, plant_id=pid).first()
    if existing:
        return _err("Already bookmarked", 409)

    bk = Bookmark(user_id=uid, plant_id=pid)
    db.session.add(bk)
    db.session.commit()
    return _ok(bk.to_dict()), 201


@users_bp.route("/bookmarks/<int:plant_id>", methods=["DELETE"])
@jwt_required()
def remove_bookmark(plant_id):
    uid = int(get_jwt_identity())
    bk  = Bookmark.query.filter_by(user_id=uid, plant_id=plant_id).first()
    if not bk:
        return _err("Bookmark not found", 404)
    db.session.delete(bk)
    db.session.commit()
    return _ok({"removed": plant_id})


# ── Notes ─────────────────────────────────────────────────────────────────────

@users_bp.route("/notes", methods=["GET"])
@jwt_required()
def list_notes():
    uid   = int(get_jwt_identity())
    notes = Note.query.filter_by(user_id=uid).order_by(Note.updated_at.desc()).all()
    return _ok([n.to_dict() for n in notes], total=len(notes))


@users_bp.route("/notes", methods=["POST"])
@jwt_required()
def save_note():
    uid  = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    pid  = data.get("plant_id")
    content = data.get("content", "").strip()

    if not pid:
        return _err("'plant_id' is required")
    if not content:
        return _err("'content' is required")

    plant = Plant.query.get(pid)
    if not plant:
        return _err("Plant not found", 404)

    note = Note.query.filter_by(user_id=uid, plant_id=pid).first()
    if note:
        note.content = content
    else:
        note = Note(user_id=uid, plant_id=pid, content=content)
        db.session.add(note)

    db.session.commit()
    return _ok(note.to_dict()), 201


@users_bp.route("/notes/<int:plant_id>", methods=["DELETE"])
@jwt_required()
def delete_note(plant_id):
    uid  = int(get_jwt_identity())
    note = Note.query.filter_by(user_id=uid, plant_id=plant_id).first()
    if not note:
        return _err("Note not found", 404)
    db.session.delete(note)
    db.session.commit()
    return _ok({"removed": plant_id})
