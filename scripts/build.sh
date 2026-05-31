#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-${ROOT_DIR}/dist}"
mkdir -p "${OUTPUT_DIR}"

DISTROS=(debian fedora)
ARCHES=(x86_64 arm64)
EDITIONS=(Desktop Recovery Developer)

for distro in "${DISTROS[@]}"; do
  for arch in "${ARCHES[@]}"; do
    for edition in "${EDITIONS[@]}"; do
      "${ROOT_DIR}/iso-builder/build_iso.sh" "${distro}" "${arch}" "${edition}" "${OUTPUT_DIR}"
    done
  done
done

cp "${OUTPUT_DIR}/AetherOS-Desktop-x86_64.iso" "${OUTPUT_DIR}/AetherOS-Desktop.iso"
cp "${OUTPUT_DIR}/AetherOS-Recovery-x86_64.iso" "${OUTPUT_DIR}/AetherOS-Recovery.iso"
cp "${OUTPUT_DIR}/AetherOS-Developer-x86_64.iso" "${OUTPUT_DIR}/AetherOS-Developer.iso"

python3 "${ROOT_DIR}/scripts/generate_manifest.py" "${OUTPUT_DIR}"

echo "Build outputs available in ${OUTPUT_DIR}"
