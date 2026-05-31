#!/usr/bin/env python3
import getpass
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional


def is_online() -> bool:
    try:
        with urllib.request.urlopen("https://clients3.google.com/generate_204", timeout=5):
            return True
    except urllib.error.URLError:
        return False


def validate_gemini_key(api_key: str) -> bool:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.status == 200
    except urllib.error.URLError:
        return False


def store_in_secret_tool(api_key: str) -> bool:
    if not shutil_which("secret-tool"):
        return False
    proc = subprocess.run(
        ["secret-tool", "store", "--label=AetherOS Gemini Key", "service", "aetheros", "account", "gemini"],
        input=api_key.encode("utf-8"),
        check=False,
    )
    return proc.returncode == 0


def store_in_kwallet(api_key: str) -> bool:
    if not shutil_which("kwallet-query"):
        return False
    cmd = [
        "kwallet-query",
        "-w",
        "gemini_api_key",
        "kdewallet",
        "-f",
        "aetheros",
    ]
    proc = subprocess.run(cmd, input=api_key.encode("utf-8"), check=False)
    return proc.returncode == 0


def store_encrypted_file(api_key: str, passphrase: str) -> bool:
    config_dir = Path.home() / ".config" / "aetheros"
    config_dir.mkdir(parents=True, exist_ok=True)
    output = config_dir / "gemini_api_key.enc"
    env = dict(os.environ)
    env["AETHER_ENCRYPTION_PASSPHRASE"] = passphrase
    proc = subprocess.run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-pbkdf2",
            "-salt",
            "-pass",
            "env:AETHER_ENCRYPTION_PASSPHRASE",
            "-out",
            str(output),
        ],
        env=env,
        input=api_key.encode("utf-8"),
        check=False,
    )
    if proc.returncode != 0:
        return False
    output.chmod(0o600)
    return True


def shutil_which(binary: str) -> Optional[str]:
    return subprocess.run(
        ["bash", "-lc", f"command -v {binary}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
        text=True,
    ).stdout.strip() or None


def first_boot() -> int:
    print("Welcome to AetherOS")
    print("Step 1/6: Welcome Screen")
    print("Step 2/6: Internet Connection Setup")
    if not is_online():
        print("No internet connection detected. Connect and re-run setup.")
        return 1

    print("Step 3/6: Gemini API Key Setup")
    api_key = getpass.getpass("Enter Gemini API key: ").strip()
    if not api_key:
        print("API key cannot be empty.")
        return 1

    print("Step 4/6: API Validation")
    if not validate_gemini_key(api_key):
        print("Gemini API key validation failed.")
        return 1

    print("Step 5/6: AI Feature Enablement")
    stored = store_in_secret_tool(api_key) or store_in_kwallet(api_key)
    if not stored:
        passphrase = getpass.getpass("Set encryption passphrase for local key storage: ").strip()
        if not passphrase:
            print("Passphrase required for encrypted storage fallback.")
            return 1
        stored = store_encrypted_file(api_key, passphrase)

    if not stored:
        print("Failed to securely store API key.")
        return 1

    setup_state = Path.home() / ".config" / "aetheros" / "setup_state.json"
    setup_state.parent.mkdir(parents=True, exist_ok=True)
    setup_state.write_text(json.dumps({"ai_enabled": True}), encoding="utf-8")

    print("Step 6/6: User Account Creation")
    print("Proceed with standard account creation in installer UI.")
    print("AetherOS setup complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(first_boot())
