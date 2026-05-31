#!/usr/bin/env python3
import json


def available_actions() -> dict:
    return {
        "snapshot_restore": True,
        "boot_repair": True,
        "network_repair": True,
        "password_reset": True,
    }


def main() -> int:
    print(json.dumps(available_actions()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
