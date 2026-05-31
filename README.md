# AetherOS

AetherOS is an AI-native operating system blueprint for Debian 13/Fedora on x86_64,
with AI as the primary interaction layer.

## Repository Layout

```text
AetherOS/
│
├── ai-core/
├── desktop/
├── installer/
├── iso-builder/
├── system-services/
├── branding/
├── docs/
│
├── .github/
│   └── workflows/
│       └── build-iso.yml
│
└── README.md
```

## Core Components

- `installer/first_boot_setup.py`: first-boot flow with Gemini key capture + secure storage.
- `ai-core/aether_ai.py`: AI daemon logic, Gemini integration, local fallback, safe action proposal.
- `system-services/aether-ai.service`: systemd unit for the AI core daemon.
- `iso-builder/build_iso.sh`: Debian/Fedora ISO build entrypoint.
- `.github/workflows/build-iso.yml`: CI workflow for matrix ISO builds + artifact publishing.

## Security Guarantees

- No API key is bundled in source.
- Gemini API key is user-provided at first boot.
- Key storage uses Linux keyring, KDE Wallet, or encrypted storage fallback.
- AI-generated actions are only proposed, never auto-executed.
- Each proposed action includes a risk classification and requires user confirmation.

## Quick Validation

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```