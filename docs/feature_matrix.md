# AetherOS Feature Matrix

## AI-Native UX

- AI Sidebar (Super+Space): planned desktop integration point (`desktop/README.md`)
- Floating AI chat: planned desktop integration point (`desktop/README.md`)
- Voice wake phrase "Hey Aether": planned desktop integration point (`desktop/README.md`)
- Global AI search: planned desktop integration point (`desktop/README.md`)

## AI Core Capabilities

- AI terminal intent-to-command translation: `ai-core/aether_ai.py`
- AI desktop assistant Python project workflow: `ai-core/aether_ai.py`
- AI settings automation proposal example (dark mode): `ai-core/aether_ai.py`
- Offline local suggestion mode: `ai-core/aether_ai.py`
- System awareness snapshot: `ai-core/aether_ai.py`

## First Boot & Gemini Key Handling

- Welcome/internet/key/validation/enablement/account flow: `installer/first_boot_setup.py`
- Linux Keyring storage path: `installer/first_boot_setup.py`
- KDE Wallet storage path: `installer/first_boot_setup.py`
- Encrypted fallback storage path: `installer/first_boot_setup.py`

## Security

- Mandatory user confirmation and risk labels: `ai-core/aether_ai.py`
- AppArmor profile: `system-services/apparmor/aether-ai.profile`
- SELinux module stub: `system-services/selinux/aether_ai.te`
- Polkit policy: `system-services/polkit/org.aetheros.ai.policy`

## Service & Build

- `aether-ai.service`: `system-services/aether-ai.service`
- ISO build script: `iso-builder/build_iso.sh`
- GitHub Actions ISO workflow: `.github/workflows/build-iso.yml`
