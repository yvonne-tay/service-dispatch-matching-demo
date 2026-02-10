# service-dispatch-matching-demo

A simplified, fictional demo of a dispatch / matching engine for a multi-location services platform.

This project focuses on workflow structure, decision logic, and documentation — suitable for showcasing systems thinking in operations and AI/data project delivery.

---

## Example scenario (marketplace-style matching)

This demo can be mapped to a two-sided dispatch system (e.g., ride-hailing, deliveries, home services, appointment-based services):

- Customers create requests (tasks).
- Providers (agents) have skills, availability, and a location zone.
- The matching engine assigns each task using:
  - constraints (skill match + availability)
  - fairness (queue-based assignment)
  - planned reservations (round-robin distribution)

---

## Project structure & Quickstart

```text
service-dispatch-matching-demo/
├─ src/
│  ├─ dispatch_demo.py
│  └─ sample_data/
│     ├─ agents.csv
│     ├─ tasks.csv
│     └─ sample_output.csv
├─ requirements.txt
└─ README.md

# Quickstart

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

python src/dispatch_demo.py --out src/sample_data/sample_output.csv
