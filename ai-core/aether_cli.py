#!/usr/bin/env python3
import argparse

from aether_ai import AetherAI, format_proposal_json


def main() -> int:
    parser = argparse.ArgumentParser(description="AetherOS AI proposal CLI")
    parser.add_argument("request", help="Natural language request")
    parser.add_argument("--offline", action="store_true", help="Use local offline mode")
    args = parser.parse_args()

    ai = AetherAI()
    if args.offline:
        print(ai.offline_hint(args.request))
        return 0

    proposal = ai.propose_action(args.request)
    print(format_proposal_json(proposal))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
