import os

# API Settings
CRYPTOMESH_HOST  = os.environ.get("CRYPTOMESH_HOST", "0.0.0.0")
CRYPTOMESH_PORT = int(os.environ.get("CRYPTOMESH_PORT", "19000"))
CRYPTOMESH_TITLE = os.environ.get("CRYPTOMESH_TITLE", "CryptoMesh API")
CRYPTOMESH_API_PREFIX = os.environ.get("CRYPTOMESH_API_PREFIX", "/api/v1")
CRYPTOMESH_VERSION = os.environ.get("CRYPTOMESH_VERSION", "1.0.0")

# Debugging
CRYPTOMESH_DEBUG  = bool(int(os.environ.get("CRYPTOMESH_DEBUG ", "1")))

# Logging Configuration
CRYPTOMESH_LOG_PATH = os.environ.get("CRYPTOMESH_LOG_PATH", "./logs")
CRYPTOMESH_LOG_LEVEL = os.environ.get("CRYPTOMESH_LOG_LEVEL", "DEBUG")
CRYPTOMESH_LOG_ROTATION_WHEN = os.environ.get("CRYPTOMESH_LOG_ROTATION_WHEN", "m")
CRYPTOMESH_LOG_ROTATION_INTERVAL = int(os.environ.get("CRYPTOMESH_LOG_ROTATION_INTERVAL", "10"))
CRYPTOMESH_LOG_TO_FILE = bool(int(os.environ.get("CRYPTOMESH_LOG_TO_FILE", "1")))
CRYPTOMESH_LOG_ERROR_FILE = bool(int(os.environ.get("CRYPTOMESH_LOG_ERROR_FILE", "0")))
