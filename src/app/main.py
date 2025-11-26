"""
CD Exercise - Main Flask Application

A simple Flask API for demonstrating continuous deployment concepts.
"""

import os
from flask import Flask, jsonify
from src.app.health import health_bp
from src.app import __version__


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration from environment
    app.config["ENV"] = os.getenv("FLASK_ENV", "development")
    app.config["VERSION"] = os.getenv("APP_VERSION", __version__)

    # Register blueprints
    app.register_blueprint(health_bp)

    @app.route("/")
    def index():
        """Root endpoint - welcome message."""
        return jsonify({
            "message": "Welcome to CD Exercise API",
            "version": app.config["VERSION"],
            "environment": app.config["ENV"]
        })

    @app.route("/api/version")
    def version():
        """Return application version information."""
        return jsonify({
            "version": app.config["VERSION"],
            "environment": app.config["ENV"],
            "python_version": os.popen("python --version").read().strip()
        })

    @app.route("/api/info")
    def info():
        """Return application information."""
        return jsonify({
            "name": "CD Exercise API",
            "description": "A Flask API for learning continuous deployment",
            "version": app.config["VERSION"],
            "endpoints": [
                {"path": "/", "method": "GET", "description": "Welcome message"},
                {"path": "/health", "method": "GET", "description": "Health check"},
                {"path": "/health/ready", "method": "GET", "description": "Readiness probe"},
                {"path": "/health/live", "method": "GET", "description": "Liveness probe"},
                {"path": "/api/version", "method": "GET", "description": "Version info"},
                {"path": "/api/info", "method": "GET", "description": "API information"}
            ]
        })

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
