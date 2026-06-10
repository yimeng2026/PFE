#!/usr/bin/env bash
# =============================================================================
# Sylva Formalization — CI Lake Adapter
# Called from within sylva_formalization/ during CI builds.
# Wraps lake build with Mega-specific telemetry and reporting.
# =============================================================================
# Usage (from repo root):
#   cd sylva_formalization && ./lakefile_ci_adapter.sh
# =============================================================================

set -euo pipefail

ADAPTER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_DIR="${ADAPTER_DIR}/.lake/build/reports"
mkdir -p "${REPORT_DIR}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${REPORT_DIR}/lake_build_${TIMESTAMP}.log"

echo "[lakefile-ci-adapter] Starting lake build..."
echo "[lakefile-ci-adapter] Working dir: $(pwd)"
echo "[lakefile-ci-adapter] Toolchain: $(cat lean-toolchain 2>/dev/null || echo 'unknown')"

# Check for lake
if ! command -v lake >/dev/null 2>&1; then
    echo "[lakefile-ci-adapter] ERROR: lake command not found"
    exit 1
fi

# Run lake build with all output captured
BUILD_START=$(date +%s)
set +e
lake build 2>&1 | tee "${LOG_FILE}"
BUILD_EXIT=${PIPESTATUS[0]}
set -e
BUILD_END=$(date +%s)
ELAPSED=$((BUILD_END - BUILD_START))

echo "[lakefile-ci-adapter] Build exit code: ${BUILD_EXIT}"
echo "[lakefile-ci-adapter] Elapsed: ${ELAPSED}s"
echo "[lakefile-ci-adapter] Log saved to: ${LOG_FILE}"

# If the Mega LeanBuildReporter is available, use it for rich reporting
MEGA_REPORTER="${ADAPTER_DIR}/../scripts/LeanBuildReporter.py"
if [[ -f "${MEGA_REPORTER}" ]]; then
    echo "[lakefile-ci-adapter] Invoking Mega LeanBuildReporter..."
    python3 "${MEGA_REPORTER}" \
        --lake-dir "${ADAPTER_DIR}" \
        --log "${LOG_FILE}" \
        --exit-code "${BUILD_EXIT}" \
        --elapsed "${ELAPSED}" \
        || echo "[lakefile-ci-adapter] Reporter failed (non-fatal)"
fi

exit ${BUILD_EXIT}
