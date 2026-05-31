#!/usr/bin/env python3
import json
import socketserver
from pathlib import Path

from aether_ai import AetherAI


class AetherTCPHandler(socketserver.StreamRequestHandler):
    ai = AetherAI()

    def handle(self) -> None:
        raw = self.rfile.readline().decode("utf-8").strip()
        if not raw:
            return
        proposal = self.ai.propose_action(raw)
        payload = json.dumps(
            {
                "request": proposal.user_request,
                "proposed_action": proposal.proposed_action,
                "risk_level": proposal.risk_level,
                "requires_confirmation": proposal.requires_confirmation,
            }
        )
        self.wfile.write((payload + "\n").encode("utf-8"))


def main() -> int:
    socket_path = Path("/run/aetheros-ai.sock")
    if socket_path.exists():
        socket_path.unlink()
    with socketserver.UnixStreamServer(str(socket_path), AetherTCPHandler) as server:
        server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
