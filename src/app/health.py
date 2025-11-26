"""
Health Check Endpoints

Provides Kubernetes-style health check endpoints for container orchestration.
"""

from flask import Blueprint, jsonify
import time

health_bp = Blueprint("health", __name__, url_prefix="/health")

# Track application start time for uptime calculation
START_TIME = time.time()


@health_bp.route("")
@health_bp.route("/")
def health():
    """
    General health check endpoint.

    Returns basic health status of the application.
    """
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2)
    })


@health_bp.route("/ready")
def readiness():
    """
    Readiness probe for Kubernetes.

    Indicates if the application is ready to receive traffic.
    In a real application, this would check:
    - Database connections
    - External service availability
    - Cache connectivity
    """
    # Simulate readiness checks
    checks = {
        "database": True,  # Would check DB connection
        "cache": True,     # Would check cache connection
        "dependencies": True  # Would check external services
    }

    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503

    return jsonify({
        "status": "ready" if all_ready else "not_ready",
        "checks": checks
    }), status_code


@health_bp.route("/live")
def liveness():
    """
    Liveness probe for Kubernetes.

    Indicates if the application is alive and should not be restarted.
    A simple response indicates the process is running.
    """
    return jsonify({
        "status": "alive",
        "timestamp": time.time()
    })
