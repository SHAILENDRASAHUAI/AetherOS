#!/usr/bin/env python3
import json
from dataclasses import dataclass


@dataclass
class UpdatePlan:
    channel: str
    strategy: str
    requires_snapshot: bool = True


def build_default_plan() -> UpdatePlan:
    return UpdatePlan(channel="stable", strategy="delta")


def main() -> int:
    print(json.dumps(build_default_plan().__dict__))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
