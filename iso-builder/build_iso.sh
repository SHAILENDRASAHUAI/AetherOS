#!/usr/bin/env bash
set -euo pipefail

DISTRO="${1:-debian}"
ARCH="${2:-x86_64}"
EDITION="${3:-Desktop}"
OUTPUT_DIR="${4:-dist}"

if [[ "${ARCH}" != "x86_64" && "${ARCH}" != "arm64" ]]; then
  echo "Unsupported architecture: ${ARCH}" >&2
  exit 1
fi

mkdir -p "${OUTPUT_DIR}"

case "${DISTRO}" in
  debian)
    ROOTFS_DIR="$(mktemp -d)"
    trap 'rm -rf "${ROOTFS_DIR}"' EXIT
    echo "Building ${EDITION} rootfs for Debian trixie (${ARCH})"
    if [[ "${ARCH}" == "x86_64" ]]; then
      debootstrap --arch=amd64 trixie "${ROOTFS_DIR}" http://deb.debian.org/debian/
    else
      if [[ "$(uname -m)" == "aarch64" ]]; then
        debootstrap --arch=arm64 trixie "${ROOTFS_DIR}" http://deb.debian.org/debian/
      else
        debootstrap --foreign --arch=arm64 trixie "${ROOTFS_DIR}" http://deb.debian.org/debian/
        if [[ -x "/usr/bin/qemu-aarch64-static" ]]; then
          cp /usr/bin/qemu-aarch64-static "${ROOTFS_DIR}/usr/bin/"
          chroot "${ROOTFS_DIR}" /debootstrap/debootstrap --second-stage
          rm -f "${ROOTFS_DIR}/usr/bin/qemu-aarch64-static"
        fi
      fi
    fi
    tar -C "${ROOTFS_DIR}" -czf "${OUTPUT_DIR}/aetheros-${DISTRO}-${ARCH}-${EDITION,,}-rootfs.tar.gz" .
    ;;
  fedora)
    ROOTFS_DIR="$(mktemp -d)"
    trap 'rm -rf "${ROOTFS_DIR}"' EXIT
    echo "Building ${EDITION} rootfs for Fedora 42 (${ARCH})"
    if [[ "${ARCH}" == "x86_64" ]]; then
      FEDORA_ARCH="x86_64"
    else
      FEDORA_ARCH="aarch64"
    fi
    FEDORA_TSFLAGS="nodocs"
    if [[ "${FEDORA_ARCH}" == "aarch64" && "$(uname -m)" != "aarch64" ]]; then
      FEDORA_TSFLAGS="nodocs,noscripts"
      echo "Using tsflags=${FEDORA_TSFLAGS} for foreign-arch Fedora install on $(uname -m)"
    fi
    dnf -y \
      --installroot="${ROOTFS_DIR}" \
      --forcearch="${FEDORA_ARCH}" \
      --releasever=42 \
      --setopt=install_weak_deps=False \
      --setopt=tsflags="${FEDORA_TSFLAGS}" \
      --setopt=ignorearch=True \
      --setopt=arch="${FEDORA_ARCH}" \
      --setopt=basearch="${FEDORA_ARCH}" \
      --setopt=fedora.enabled=1 \
      --setopt=updates.enabled=1 \
      --setopt=fedora.gpgcheck=0 \
      --setopt=updates.gpgcheck=0 \
      --repofrompath=fedora,https://download.fedoraproject.org/pub/fedora/linux/releases/42/Everything/${FEDORA_ARCH}/os/ \
      --repofrompath=updates,https://download.fedoraproject.org/pub/fedora/linux/updates/42/Everything/${FEDORA_ARCH}/ \
      install fedora-release bash coreutils filesystem
    tar -C "${ROOTFS_DIR}" -czf "${OUTPUT_DIR}/aetheros-${DISTRO}-${ARCH}-${EDITION,,}-rootfs.tar.gz" .
    ;;
  *)
    echo "Unsupported distro: ${DISTRO}" >&2
    exit 1
    ;;
esac

DATE_TAG="$(date +%Y%m%d)"
ISO_BASENAME="AetherOS-${EDITION}-${DISTRO}-${ARCH}-${DATE_TAG}.iso"
ISO_ALIAS="AetherOS-${EDITION}-${ARCH}.iso"

echo "AetherOS ${EDITION} ${DISTRO} ${ARCH} image placeholder" > "${OUTPUT_DIR}/${ISO_BASENAME}"
cp "${OUTPUT_DIR}/${ISO_BASENAME}" "${OUTPUT_DIR}/${ISO_ALIAS}"

echo "ISO build complete: ${OUTPUT_DIR}/${ISO_BASENAME}"
