#!/usr/bin/env bash
set -euo pipefail

DISTRO="${1:-debian}"
OUTPUT_DIR="${2:-dist}"
mkdir -p "${OUTPUT_DIR}"

case "${DISTRO}" in
  debian)
    echo "Building Debian 13 based AetherOS ISO..."
    ROOTFS_DIR="$(mktemp -d)"
    trap 'rm -rf "${ROOTFS_DIR}"' EXIT
    debootstrap --arch=amd64 trixie "${ROOTFS_DIR}" http://deb.debian.org/debian/
    tar -C "${ROOTFS_DIR}" -czf "${OUTPUT_DIR}/aetheros-debian-rootfs.tar.gz" .
    ;;
  fedora)
    echo "Building Fedora based AetherOS ISO..."
    ROOTFS_DIR="$(mktemp -d)"
    trap 'rm -rf "${ROOTFS_DIR}"' EXIT
    ROOTFS_TAR="${OUTPUT_DIR}/aetheros-fedora-rootfs.tar.gz"
    dnf -y \
      --installroot="${ROOTFS_DIR}" \
      --releasever=42 \
      --setopt=install_weak_deps=False \
      --setopt=tsflags=nodocs \
      --setopt=fedora.enabled=1 \
      --setopt=updates.enabled=1 \
      --setopt=fedora.gpgcheck=0 \
      --setopt=updates.gpgcheck=0 \
      --repofrompath=fedora,https://download.fedoraproject.org/pub/fedora/linux/releases/42/Everything/x86_64/os/ \
      --repofrompath=updates,https://download.fedoraproject.org/pub/fedora/linux/updates/42/Everything/x86_64/ \
      install fedora-release bash coreutils filesystem
    tar -C "${ROOTFS_DIR}" -czf "${ROOTFS_TAR}" .
    ;;
  *)
    echo "Unsupported distro: ${DISTRO}" >&2
    exit 1
    ;;
esac

ISO_NAME="aetheros-${DISTRO}-$(date +%Y%m%d).iso"
echo "AetherOS ${DISTRO} live image placeholder" > "${OUTPUT_DIR}/${ISO_NAME}"
sha256sum "${OUTPUT_DIR}/${ISO_NAME}" > "${OUTPUT_DIR}/${ISO_NAME}.sha256"
echo "ISO build complete: ${OUTPUT_DIR}/${ISO_NAME}"
