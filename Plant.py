"""
Plant database model
"""

import json
from datetime import datetime
from app import db


# Association table: tours ↔ plants (many-to-many)
tour_plants = db.Table(
    "tour_plants",
    db.Column("tour_id", db.Integer, db.ForeignKey("tour.id"), primary_key=True),
    db.Column("plant_id", db.Integer, db.ForeignKey("plant.id"), primary_key=True),
)


class Plant(db.Model):
    __tablename__ = "plant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    botanical = db.Column(db.String(180), nullable=False)
    emoji = db.Column(db.String(8), default="🌿")
    color = db.Column(db.String(20), default="#e8f5e9")

    # JSON-serialised lists / dicts stored as text
    _common_names = db.Column("common_names", db.Text, default="[]")
    _categories = db.Column("categories", db.Text, default="[]")
    _uses = db.Column("uses", db.Text, default="[]")
    _cultivation = db.Column("cultivation", db.Text, default="[]")

    region = db.Column(db.String(60), index=True)
    family = db.Column(db.String(120))
    ayurvedic_system = db.Column(db.String(120))
    taste = db.Column(db.String(120))
    part_used = db.Column(db.String(200))
    season = db.Column(db.String(60))

    desc = db.Column(db.Text)
    about = db.Column(db.Text)
    prep = db.Column(db.Text)
    compounds = db.Column(db.Text)
    habitat = db.Column(db.Text)

    # Media
    image_url = db.Column(db.String(500))
    model_3d_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    audio_url = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookmarks = db.relationship("Bookmark", back_populates="plant", cascade="all, delete-orphan")
    notes = db.relationship("Note", back_populates="plant", cascade="all, delete-orphan")

    # ── JSON helpers ────────────────────────────────────────────────
    @property
    def common_names(self):
        return json.loads(self._common_names or "[]")

    @common_names.setter
    def common_names(self, value):
        self._common_names = json.dumps(value or [])

    @property
    def categories(self):
        return json.loads(self._categories or "[]")

    @categories.setter
    def categories(self, value):
        self._categories = json.dumps(value or [])

    @property
    def uses(self):
        return json.loads(self._uses or "[]")

    @uses.setter
    def uses(self, value):
        self._uses = json.dumps(value or [])

    @property
    def cultivation(self):
        return json.loads(self._cultivation or "[]")

    @cultivation.setter
    def cultivation(self, value):
        self._cultivation = json.dumps(value or [])

    # ── Serialisation ───────────────────────────────────────────────
    def to_dict(self, brief: bool = False) -> dict:
        base = {
            "id": self.id,
            "name": self.name,
            "botanical": self.botanical,
            "emoji": self.emoji,
            "color": self.color,
            "common_names": self.common_names,
            "categories": self.categories,
            "region": self.region,
            "desc": self.desc,
            "image_url": self.image_url,
        }
        if not brief:
            base.update(
                {
                    "about": self.about,
                    "uses": self.uses,
                    "prep": self.prep,
                    "compounds": self.compounds,
                    "habitat": self.habitat,
                    "cultivation": self.cultivation,
                    "family": self.family,
                    "ayurvedic_system": self.ayurvedic_system,
                    "taste": self.taste,
                    "part_used": self.part_used,
                    "season": self.season,
                    "model_3d_url": self.model_3d_url,
                    "video_url": self.video_url,
                    "audio_url": self.audio_url,
                    "created_at": self.created_at.isoformat() if self.created_at else None,
                    "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                }
            )
        return base

    def __repr__(self):
        return f"<Plant {self.id}: {self.name}>"
