"""
Dispatch / Matching Demo (Fictional & Sanitized)

- Confirmed tasks: assigned by top-of-queue among eligible agents (fairness).
- Planned tasks: assigned by round-robin among eligible agents.

All data is synthetic and generic.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import List, Optional, Set

import pandas as pd


@dataclass
class Agent:
    agent_id: str
    skills: Set[str]
    zone: str
    is_available: bool
    queue_rank: int


def parse_skills(raw: str) -> Set[str]:
    return {s.strip() for s in raw.split(";") if s.strip()}


def load_agents(path: str) -> List[Agent]:
    df = pd.read_csv(path)
    agents: List[Agent] = []
    for _, r in df.iterrows():
        agents.append(
            Agent(
                agent_id=str(r["agent_id"]),
                skills=parse_skills(str(r["skills"])),
                zone=str(r["zone"]),
                is_available=str(r["is_available"]).upper() == "TRUE",
                queue_rank=int(r["queue_rank"]),
            )
        )
    agents.sort(key=lambda a: a.queue_rank)
    return agents


def eligible_agents(agents: List[Agent], required_skill: str, zone: str) -> List[Agent]:
    return [a for a in agents if a.is_available and required_skill in a.skills and a.zone == zone]


def pick_by_queue(candidates: List[Agent]) -> Optional[Agent]:
    return candidates[0] if candidates else None


def round_robin_pick(candidates: List[Agent], rr_index: int) -> Optional[Agent]:
    if not candidates:
        return None
    return candidates[rr_index % len(candidates)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fictional dispatch/matching demo (sanitized).")
    parser.add_argument("--agents", default="src/sample_data/agents.csv", help="Path to agents.csv")
    parser.add_argument("--tasks", default="src/sample_data/tasks.csv", help="Path to tasks.csv")
    parser.add_argument("--out", default="src/sample_data/sample_output.csv", help="Output CSV path")
    args = parser.parse_args()

    agents = load_agents(args.agents)
    tasks = pd.read_csv(args.tasks)

    confirmed = tasks[tasks["is_confirmed"] == True].copy()
    planned = tasks[tasks["is_confirmed"] == False].copy()

    results = []

    # 1) Confirmed tasks: assign by top-of-queue
    for _, t in confirmed.iterrows():
        zone = str(t["zone"])
        required_skill = str(t["required_skill"])
        candidates = eligible_agents(agents, required_skill, zone)
        chosen = pick_by_queue(candidates)

        if chosen is None:
            results.append(
                {
                    "task_id": t["task_id"],
                    "task_type": t["task_type"],
                    "required_skill": required_skill,
                    "zone": zone,
                    "assigned_agent": "",
                    "decision_reason": "no eligible agent available in same zone",
                }
            )
            continue

        chosen.is_available = False  # toy simulation
        results.append(
            {
                "task_id": t["task_id"],
                "task_type": t["task_type"],
                "required_skill": required_skill,
                "zone": zone,
                "assigned_agent": chosen.agent_id,
                "decision_reason": "confirmed task assigned by top-of-queue (fairness)",
            }
        )

    # 2) Planned tasks: assign by round-robin
    rr_index = 0
    for _, t in planned.iterrows():
        zone = str(t["zone"])
        required_skill = str(t["required_skill"])
        candidates = eligible_agents(agents, required_skill, zone)
        chosen = round_robin_pick(candidates, rr_index)
        rr_index += 1

        if chosen is None:
            results.append(
                {
                    "task_id": t["task_id"],
                    "task_type": t["task_type"],
                    "required_skill": required_skill,
                    "zone": zone,
                    "assigned_agent": "",
                    "decision_reason": "no eligible agent available in same zone",
                }
            )
            continue

        results.append(
            {
                "task_id": t["task_id"],
                "task_type": t["task_type"],
                "required_skill": required_skill,
                "zone": zone,
                "assigned_agent": chosen.agent_id,
                "decision_reason": "planned task assigned by round-robin (fair distribution)",
            }
        )

    out_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    out_df.to_csv(args.out, index=False)

    print(f"Saved output to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
