"""
Vanaspati — Virtual Herbal Garden
Flask application factory
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "60 per hour"])


def create_app(config_name: str = None) -> Flask:
    """Application factory."""
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    # ── Configuration ──────────────────────────────────────────────
    env = config_name or os.getenv("FLASK_ENV", "development")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///vanaspati.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "")

    if env == "testing":
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    # ── Extensions ─────────────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # ── Blueprints ──────────────────────────────────────────────────
    from app.routes.plants import plants_bp
    from app.routes.tours import tours_bp
    from app.routes.users import users_bp
    from app.routes.ai import ai_bp
    from app.routes.health import health_bp

    app.register_blueprint(plants_bp, url_prefix="/api/plants")
    app.register_blueprint(tours_bp, url_prefix="/api/tours")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(health_bp, url_prefix="/api")

    # ── DB init ────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_if_empty()

    return app


def _seed_if_empty():
    """Seed database with plant and tour data if tables are empty."""
    from app.models.plant import Plant
    from app.models.tour import Tour
    from app.utils.seed_data import PLANT_SEED, TOUR_SEED

    if Plant.query.count() == 0:
        for data in PLANT_SEED:
            plant = Plant(**data)
            db.session.add(plant)
        db.session.commit()

    if Tour.query.count() == 0:
        from app.models.plant import Plant as P
        for data in TOUR_SEED:
            plant_ids = data.pop("plant_ids", [])
            tour = Tour(**data)
            tour.plants = [P.query.get(pid) for pid in plant_ids if P.query.get(pid)]
            db.session.add(tour)
        db.session.commit()
