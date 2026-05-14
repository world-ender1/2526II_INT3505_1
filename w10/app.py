import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics


APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def configure_logging(app: Flask) -> None:
    os.makedirs(LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    app.logger.handlers.clear()
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    app.logger.propagate = False


def create_app() -> Flask:
    app = Flask(__name__)
    configure_logging(app)

    metrics = PrometheusMetrics(app)
    metrics.info("app_info", "Week 10 Demo API", version=APP_VERSION)

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["100 per 15 minutes"],
        storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
    )

    @app.get("/")
    def index():
        app.logger.info("Root endpoint accessed from %s", get_remote_address())
        return jsonify(
            {
                "message": "Week 10 API is running",
                "endpoints": ["/api/status", "/api/login", "/metrics"],
                "version": APP_VERSION,
            }
        )

    @app.get("/api/status")
    def status():
        app.logger.info("Status endpoint accessed from %s", get_remote_address())
        return jsonify(
            {
                "status": "OK",
                "message": "System is running normally",
                "version": APP_VERSION,
            }
        )

    @app.post("/api/login")
    @limiter.limit("5 per 15 minutes")
    def login():
        data = request.get_json(silent=True) or {}
        username = data.get("username", "")
        password = data.get("password", "")

        if username == "admin" and password == "123456":
            app.logger.info("User '%s' logged in successfully", username)
            return jsonify(
                {
                    "message": "Login successful",
                    "token": "demo-token-week10",
                }
            )

        app.logger.warning(
            "Failed login attempt from %s with username '%s'",
            get_remote_address(),
            username,
        )
        return jsonify({"error": "Invalid credentials"}), 401

    @app.errorhandler(429)
    def ratelimit_handler(error):
        app.logger.warning(
            "Rate limit triggered for %s: %s",
            get_remote_address(),
            error.description,
        )
        return (
            jsonify(
                {
                    "error": "Too Many Requests",
                    "message": "Request limit exceeded. Please try again later.",
                    "detail": error.description,
                }
            ),
            429,
        )

    @app.errorhandler(404)
    def not_found(_error):
        app.logger.warning("Not found: %s %s", request.method, request.path)
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Internal server error: %s", error)
        return jsonify({"error": "Internal Server Error"}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
