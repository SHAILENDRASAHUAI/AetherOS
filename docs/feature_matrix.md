# AetherOS Feature Matrix

## Product and Platform

- Edition matrix (Desktop/Recovery/Developer): `release/targets.yaml`
- Platform matrix (x86_64/arm64 + desktop/laptop/server/vm/cloud): `release/targets.yaml`

## Boot / Kernel / Security

- GRUB template: `bootloader/grub/grub.cfg.template`
- Initramfs secure boot hook: `initramfs/hooks/aether-secureboot.sh`
- Kernel profiles: `kernel/configs/desktop.config`, `server.config`, `cloud.config`
- Firewall baseline: `security/firewall/nftables.conf`
- TPM policy baseline: `security/tpm/measurement-policy.json`
- Encryption baseline: `security/encryption/luks-layout.md`

## AI Platform

- AI proposal routing and safety policy: `ai-core/aether_ai.py`
- AI daemon transport: `ai-core/aether_daemon.py`
- First boot Gemini onboarding: `installer/first_boot_setup.py`
- AI memory policy modes: `ai-memory/memory_policy.yaml`
- AI terminal approval policy: `ai-terminal/safety_policy.yaml`

## Operations

- Matrix build orchestrator: `scripts/build.sh`
- Artifact checksums and manifest: `scripts/generate_manifest.py`
- ISO build entrypoint: `iso-builder/build_iso.sh`
- Update/recovery/health/telemetry services: `system-services/*.service`
