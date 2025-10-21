#!/usr/bin/env bash
set -euo pipefail

# ===========================================
#  MictlanX Router - Deploy + Health-check
# ===========================================
# Vars configurables (puedes exportarlas antes de llamar el script):
#   ROUTER_COMPOSE_FILE : archivo compose del router (default: mictlanx-router.yml)
#   ROUTER_HOST         : host del API (default: localhost)
#   ROUTER_PORT         : puerto del API (default: 60666)
#   ROUTER_PATH         : path de stats (default: /api/v4/peers/stats)
#   ROUTER_TIMEOUT      : segundos de espera total (default: 180)
#   ROUTER_SLEEP        : segundos entre intentos (default: 2)
#   REQUIRE_PEERS       : "true" para fallar si no hay peers en el timeout; "false" por defecto
#   SILENT_CURL         : "true" para suprimir errores de curl (default: true)

ROUTER_COMPOSE_FILE="${ROUTER_COMPOSE_FILE:-mictlanx-router.yml}"
ROUTER_HOST="${ROUTER_HOST:-localhost}"
ROUTER_PORT="${ROUTER_PORT:-60666}"
ROUTER_PATH="${ROUTER_PATH:-/api/v4/peers/stats}"
ROUTER_TIMEOUT="${ROUTER_TIMEOUT:-180}"
ROUTER_SLEEP="${ROUTER_SLEEP:-2}"
REQUIRE_PEERS="${REQUIRE_PEERS:-false}"
SILENT_CURL="${SILENT_CURL:-true}"

API="http://${ROUTER_HOST}:${ROUTER_PORT}${ROUTER_PATH}"

# Colores (#89CA78 ≈ 38;5;114)
C_MINT="\e[38;5;114m"; C_RESET="\e[0m"
info(){ echo -e "${C_MINT}ℹ️  $*${C_RESET}"; }
ok(){ echo -e "${C_MINT}✅ $*${C_RESET}"; }
warn(){ echo -e "⚠️  $*"; }
err(){ echo -e "❌ $*" >&2; }

echo "Removing existing routers"
docker compose -f "${ROUTER_COMPOSE_FILE}" down || true

echo "Starting a new MictlanX Cluster"
docker compose -f "${ROUTER_COMPOSE_FILE}" up -d

# -------------------------------
# Healthcheck: wait for API/peers
# -------------------------------
deadline=$((SECONDS + ROUTER_TIMEOUT))
info "Waiting for peers at ${API} (timeout ${ROUTER_TIMEOUT}s)…"

# helpers para contar peers
count_peers() {
  # lee JSON de stdin y devuelve un entero
  if command -v jq >/dev/null 2>&1; then
    jq -r 'length' 2>/dev/null || echo 0
  elif command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY' 2>/dev/null || echo 0
import sys, json
try:
    data = json.load(sys.stdin)
    print(len(data))
except Exception:
    print(0)
PY
  else
    # fallback muy básico: cuenta '[' ']' para arrays vacíos/no vacíos
    # si detecta "[]" → 0, si ve al menos una coma → >=2, si ve "}" o "{" dentro → heurística
    buf="$(cat)"
    if echo "$buf" | grep -q '^\s*\[\s*\]\s*$'; then
      echo 0
    elif echo "$buf" | grep -q ','; then
      # aproximación burda (al menos 2)
      echo 2
    else
      echo 1
    fi
  fi
}

curl_flags=( -fsS --retry 3 --retry-delay 1 --max-time 3 )
# --retry-connrefused acelera en algunas curl recientes; si falla, ignoramos
curl --help 2>&1 | grep -q -- '--retry-connrefused' && curl_flags+=( --retry-connrefused )

while true; do
  if [[ "${SILENT_CURL}" == "true" ]]; then
    http="$(curl "${curl_flags[@]}" "${API}" 2>/dev/null || true)"
  else
    http="$(curl "${curl_flags[@]}" "${API}" || true)"
  fi

  if [[ -n "${http}" ]]; then
    n="$(printf '%s' "${http}" | count_peers)"
    if [[ "${n}" =~ ^[0-9]+$ ]] && [ "${n}" -gt 0 ]; then
      ok "MictlanX cluster is healthy (peers: ${n})"
      break
    else
      echo "⏳ No peers yet (length=${n})"
    fi
  else
    echo "⏳ API not ready yet (curl returned empty)"
  fi

  if [ ${SECONDS} -ge ${deadline} ]; then
    if [[ "${REQUIRE_PEERS}" == "true" ]]; then
      err "Timed out waiting for peers at ${API} (REQUIRE_PEERS=true)"
      exit 1
    else
      warn "Timed out waiting for peers at ${API}, but continuing (REQUIRE_PEERS=false)"
      exit 0
    fi
  fi

  sleep "${ROUTER_SLEEP}"
done

exit 0
