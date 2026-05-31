# AetherOS Architecture

## Base System

- Target distros: Debian 13 (trixie) and Fedora
- Architecture: x86_64
- Desktop: KDE Plasma customization with Wayland, UEFI, Secure Boot intent
- Delivery: Live ISO builds via `iso-builder/` and GitHub Actions

## AI Core (`aether-ai.service`)

`aether-ai.service` launches `ai-core/aether_daemon.py` and exposes a local UNIX
socket for desktop components.

Core responsibilities implemented in `ai-core/aether_ai.py`:

- Gemini API communication with user-provided API key
- Local fallback mode for offline functionality
- Intent-to-command conversion for package operations
- Desktop automation proposal generation
- System awareness data collection

## Safety Model

- AI actions are always returned as **proposals**
- Every proposal includes `risk_level`
- `requires_confirmation` is always true
- No auto execution path exists in AI core

## First Boot Sequence

Implemented by `installer/first_boot_setup.py`:

1. Welcome
2. Internet check
3. Gemini API key collection
4. API validation
5. AI feature enablement + secure key storage
6. User account creation handoff

## Secure Key Storage

Storage priority:

1. Linux Keyring (`secret-tool`)
2. KDE Wallet (`kwallet-query`)
3. Encrypted local fallback (`openssl` AES-256)

No plaintext API key file is written.
