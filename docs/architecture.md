# AetherOS Architecture

## Platform Baseline

- Distros: Debian 13 (trixie), Fedora 42
- Architectures: x86_64, arm64
- Editions: Desktop, Recovery, Developer
- Boot target: UEFI + GRUB2 + Linux LTS + initramfs + systemd

## Boot Path

UEFI -> GRUB -> Kernel -> Initramfs -> systemd -> Desktop -> AI Core

Artifacts:
- `bootloader/grub/grub.cfg.template`
- `initramfs/hooks/aether-secureboot.sh`
- `kernel/configs/*.config`

## AI Core

`aether-ai.service` starts `ai-core/aether_daemon.py`, which delegates intent routing to `ai-core/aether_ai.py`.

Capabilities:
- intent-to-command mapping for package operations
- Gemini-backed fallback command generation
- command safety filtering for destructive patterns
- offline local recommendation mode

## Security Model

- Secure boot intent + TPM measurement policy (`security/tpm/measurement-policy.json`)
- SELinux + AppArmor scaffolding (`system-services/selinux`, `system-services/apparmor`)
- firewall baseline (`security/firewall/nftables.conf`)
- encryption baseline (`security/encryption/luks-layout.md`)

## Service Topology

- `aether-ai.service`: AI routing daemon
- `aether-update.service`: update orchestration
- `aether-recovery.service`: recovery actions
- `aether-health.service`: health monitoring
- `aether-telemetry.service`: local telemetry collector

## Build and Release

- `iso-builder/build_iso.sh`: distro/arch/edition image entrypoint
- `scripts/build.sh`: matrix build orchestrator
- `scripts/generate_manifest.py`: checksums + manifest metadata
- `release/targets.yaml`: product baseline and release target declaration
