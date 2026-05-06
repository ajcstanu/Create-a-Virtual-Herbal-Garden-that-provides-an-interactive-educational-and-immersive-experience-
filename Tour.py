"""
Tour database model
"""

import json
from datetime import datetime
from app import db
from app.models.plant import tour_plants


class Tour(db.Model):
    __tablename__ = "tour"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(120))
    emoji = db.Column(db.String(8), default="🗺️")
    color = db.Column(db.String(200))
    desc = db.Column(db.Text)
    duration = db.Column(db.String(30))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many with Plant
    plants = db.relationship(
        "Plant",
        secondary=tour_plants,
        lazy="subquery",
        backref=db.backref("tours", lazy=True),
    )

    def to_dict(self, include_plants: bool = True) -> dict:
        d = {
            "id": self.id,
            "name": self.name,
            "theme": self.theme,
            "emoji": self.emoji,
            "color": self.color,
            "desc": self.desc,
            "duration": self.duration,
            "plant_count": len(self.plants),
        }
        if include_plants:
            d["plants"] = [p.to_dict(brief=True) for p in self.plants]
        return d

    def __repr__(self):
        return f"<Tour {self.id}: {self.name}>"
