import os
from dotenv import load_dotenv
CRYPTOMESH_ENV_FILE = os.environ.get("CRYPTOMESH_ENV_FILE",".env")
exists = os.path.exists(CRYPTOMESH_ENV_FILE)
if exists:
    load_dotenv(CRYPTOMESH_ENV_FILE)
# Base Configuration for CryptoMesh

# MongoDB Settings
CRYPTOMESH_MONGODB_URI          = os.environ.get("CRYPTOMESH_MONGODB_URI", "mongodb://localhost:27017/cryptomesh")
CRYPTOMESH_MONGO_DATABASE_NAME  = os.environ.get("CRYPTOMESH_MONGO_DATABASE_NAME", "cryptomesh")

# API Settings
CRYPTOMESH_HOST                       = os.environ.get("CRYPTOMESH_HOST", "0.0.0.0")
CRYPTOMESH_PORT                       = int(os.environ.get("CRYPTOMESH_PORT", "19000"))
CRYPTOMESH_TITLE                      = os.environ.get("CRYPTOMESH_TITLE", "CryptoMesh API")
CRYPTOMESH_API_PREFIX                 = os.environ.get("CRYPTOMESH_API_PREFIX", "/api/v1")
CRYPTOMESH_VERSION                    = os.environ.get("CRYPTOMESH_VERSION", "1.0.0")
CRYPTOMESH_ENDPOINT_REQ_RES_BASE_PORT = int(os.environ.get("CRYPTOMESH_ENDPOINT_REQ_RES_BASE_PORT", "40000"))
CRYPTOMESH_ENDPOINT_PUBSUB_BASE_PORT  = int(os.environ.get("CRYPTOMESH_ENDPOINT_PUBSUB_BASE_PORT", "50000"))
CRYPTOMESH_DEBUG                      = bool(int(os.environ.get("CRYPTOMESH_DEBUG", "1")))
CRYPTOMESH_CORS_ORIGINS               = os.environ.get("CRYPTOMESH_CORS_ORIGINS","https://muyal.tamps.cinvestav.mx").split(",")
CRYPTOMESH_CORS_ALLOW_CREDENTIALS     = bool(int(os.environ.get("CRYPTOMESH_CORS_ALLOW_CREDENTIALS","1")))
CRYPTOMESH_MAX_DEPLOYED_ENDPOINTS     = int(os.getenv("CRYPTOMESH_MAX_DEPLOYED_ENDPOINTS", "5"))

SHIELDX_API_PREFIX = os.environ.get("SHIELDX_API_PREFIX", "/api/v1")
SHIELDX_HOST       = os.environ.get("SHIELDX_HOST", "localhost")
SHIELDX_PORT       = int(os.environ.get("SHIELDX_PORT", "20000"))

# ========================
# Configuración de ShieldX Client
# ========================
SHIELDX_CLIENT_BASE_URL = os.environ.get(
    "SHIELDX_CLIENT_BASE_URL",
    f"http://{SHIELDX_HOST}:{SHIELDX_PORT}{SHIELDX_API_PREFIX}"
)



# Logging Configuration
CRYPTOMESH_LOG_PATH              = os.environ.get("CRYPTOMESH_LOG_PATH", "./logs")
CRYPTOMESH_LOG_LEVEL             = os.environ.get("CRYPTOMESH_LOG_LEVEL", "DEBUG")
CRYPTOMESH_LOG_ROTATION_WHEN     = os.environ.get("CRYPTOMESH_LOG_ROTATION_WHEN", "m")
CRYPTOMESH_LOG_ROTATION_INTERVAL = int(os.environ.get("CRYPTOMESH_LOG_ROTATION_INTERVAL", "10"))
CRYPTOMESH_LOG_TO_FILE           = bool(int(os.environ.get("CRYPTOMESH_LOG_TO_FILE", "1")))
CRYPTOMESH_LOG_ERROR_FILE        = bool(int(os.environ.get("CRYPTOMESH_LOG_ERROR_FILE", "0")))
