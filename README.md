# AetherOS

AetherOS is an AI-native operating system engineering repository targeting Debian 13 and Fedora 42 with x86_64 and arm64 support.

## Release Targets

- **Desktop**: AI-first workstation image
- **Recovery**: snapshot and boot repair image
- **Developer**: SDK + container/virtualization enabled image

Defined in: `release/targets.yaml`

## Repository Layout

```text
AetherOS/
├── kernel/
├── bootloader/
├── initramfs/
├── security/
├── networking/
├── desktop/
├── ai-core/
├── ai-memory/
├── ai-terminal/
├── ai-filemanager/
├── ai-assistant/
├── browser/
├── appstore/
├── installer/
├── updater/
├── recovery/
├── drivers/
├── sdk/
├── docs/
├── tests/
├── branding/
├── scripts/
├── iso-builder/
└── .github/workflows/
```

## Build Matrix

Use:

```bash
./scripts/build.sh
```

Builds Debian/Fedora, x86_64/arm64, and Desktop/Recovery/Developer placeholders, then emits:

- `AetherOS-Desktop.iso`
- `AetherOS-Recovery.iso`
- `AetherOS-Developer.iso`
- `manifest.json` and SHA256 files in `dist/`

## Security Guarantees

- Gemini API key is user provided at first boot.
- Key storage uses secret-tool, KDE Wallet, or encrypted fallback.
- AI actions are proposals requiring user confirmation.
- AI-generated unsafe commands are rejected by safety policy.

## Quick Validation

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
