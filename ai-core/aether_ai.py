#!/usr/bin/env python3
import json
import os
import platform
import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


GEMINI_MODEL = "gemini-2.0-flash"


@dataclass
class ActionProposal:
    user_request: str
    proposed_action: str
    risk_level: str
    requires_confirmation: bool = True


class GeminiClient:
    def __init__(self, api_key: Optional[str], timeout: int = 15) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return ""

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{GEMINI_MODEL}:generateContent?key={self.api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return ""

        candidates = data.get("candidates", [])
        if not candidates:
            return ""
        parts = candidates[0].get("content", {}).get("parts", [])
        return parts[0].get("text", "") if parts else ""


class AetherAI:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("AETHER_GEMINI_API_KEY")
        self.gemini = GeminiClient(self.api_key)
        self.package_manager = self._detect_package_manager()
        self.index_root = Path.home()

    @staticmethod
    def _detect_package_manager() -> str:
        os_release = Path("/etc/os-release")
        content = os_release.read_text(encoding="utf-8") if os_release.exists() else ""
        lowered = content.lower()
        if "fedora" in lowered:
            return "dnf"
        return "apt"

    def _local_action_from_text(self, text: str) -> ActionProposal:
        lowered = text.lower().strip()

        install_match = re.fullmatch(r"install\s+(.+)", lowered)
        if install_match:
            package = install_match.group(1).strip().replace(" ", "-")
            cmd = (
                f"sudo apt install -y {package}"
                if self.package_manager == "apt"
                else f"sudo dnf install -y {package}"
            )
            return ActionProposal(text, cmd, "medium")

        remove_match = re.fullmatch(r"remove\s+(.+)", lowered)
        if remove_match:
            package = remove_match.group(1).strip().replace(" ", "-")
            cmd = (
                f"sudo apt remove -y {package}"
                if self.package_manager == "apt"
                else f"sudo dnf remove -y {package}"
            )
            return ActionProposal(text, cmd, "high")

        if lowered in {"update system", "upgrade system", "update"}:
            cmd = (
                "sudo apt update && sudo apt upgrade -y"
                if self.package_manager == "apt"
                else "sudo dnf upgrade --refresh -y"
            )
            return ActionProposal(text, cmd, "high")

        if lowered == "enable dark mode":
            return ActionProposal(
                text,
                "plasma-apply-colorscheme BreezeDark",
                "low",
            )

        return ActionProposal(
            text,
            "No direct command generated. Open AI sidebar for guided workflow.",
            "low",
        )

    def propose_action(self, text: str) -> ActionProposal:
        local = self._local_action_from_text(text)
        if local.proposed_action.startswith("No direct command"):
            prompt = (
                "You are AetherOS AI. Convert request to one safe shell command only, "
                "no explanations. Request: "
                + text
            )
            gemini_command = self.gemini.generate(prompt).strip()
            if gemini_command:
                return ActionProposal(text, gemini_command, "medium")
        return local

    def desktop_assistant_create_python_project(self, project_name: str) -> list[str]:
        base = self.index_root / project_name
        commands = [
            f"mkdir -p {base}",
            f"python3 -m venv {base / '.venv'}",
            f"touch {base / 'main.py'} {base / 'README.md'}",
        ]
        return commands

    def offline_hint(self, text: str) -> str:
        return f"Offline mode active. Local suggestion: {self._local_action_from_text(text).proposed_action}"

    @staticmethod
    def system_awareness() -> dict:
        return {
            "hostname": platform.node(),
            "platform": platform.platform(),
            "machine": platform.machine(),
        }


def format_proposal_json(proposal: ActionProposal) -> str:
    return json.dumps(asdict(proposal), indent=2)
