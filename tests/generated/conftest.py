"""
pytest configuration for AI-generated tests.
Framework-specific setup with minimal dependencies.
"""

import os
import sys
import pytest
import warnings

# Suppress deprecation warnings during testing
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

# Set testing environment
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("LOG_LEVEL", "ERROR")

# Add target project to Python path
TARGET_ROOT = os.environ.get("TARGET_ROOT", "/home/runner/work/test-low-coverage-repo/test-low-coverage-repo/pipeline/target_repo")
if TARGET_ROOT and TARGET_ROOT not in sys.path:
    sys.path.insert(0, TARGET_ROOT)

# Also add current directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============== UNIVERSAL PYTHON CONFIGURATION ==============

import types
from unittest.mock import Mock

# Try to detect and import any application
_app = None
_framework = None

# Try Flask
try:
    for module_name in ['app', 'application', 'main', 'server']:
        try:
            mod = __import__(module_name)
            if hasattr(mod, 'app'):
                _app = mod.app
                if hasattr(_app, 'test_client'):
                    _framework = 'flask'
                break
        except ImportError:
            continue
except Exception:
    pass

# Try FastAPI if Flask not found
if _app is None:
    try:
        for module_name in ['main', 'app', 'api']:
            try:
                mod = __import__(module_name)
                if hasattr(mod, 'app'):
                    _app = mod.app
                    _framework = 'fastapi'
                    break
            except ImportError:
                continue
    except Exception:
        pass


@pytest.fixture(scope="session")
def app():
    """Universal application fixture."""
    if _app is None:
        pytest.skip("No application found")

    if _framework == 'flask':
        _app.config['TESTING'] = True
        ctx = _app.app_context()
        ctx.push()
        yield _app
        ctx.pop()
    else:
        yield _app


@pytest.fixture
def client(app):
    """Universal test client fixture."""
    if _framework == 'flask':
        return app.test_client()
    elif _framework == 'fastapi':
        try:
            from fastapi.testclient import TestClient
            return TestClient(app)
        except ImportError:
            pass
    pytest.skip("No test client available")


@pytest.fixture
def sample_data():
    """Universal sample test data."""
    return {
        "id": 1,
        "name": "Test Item",
        "title": "Test Title",
        "description": "Test Description",
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "is_active": True,
        "data": {"key": "value"},
    }


@pytest.fixture
def mock_request():
    """Universal mock request object."""
    request = types.SimpleNamespace()
    request.method = "GET"
    request.path = "/test"
    request.data = {}
    request.args = {}
    request.headers = {}
    request.json = lambda: {}
    return request


@pytest.fixture
def authenticated_user():
    """Universal authenticated user mock."""
    user = types.SimpleNamespace()
    user.id = 1
    user.username = "testuser"
    user.email = "test@example.com"
    user.is_authenticated = True
    user.is_active = True
    return user
