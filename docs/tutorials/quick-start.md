# Quick Start

Get your first Cocapn Fleet running in 5 minutes.

## Installation

```bash
git clone https://github.com/SuperInstance/cocapn-fleet-ultimate.git
cd cocapn-fleet-ultimate
pip install -e .
```

## First Fleet

```python
from cocapn_fleet import FleetCore, FleetConfig

# Create a fleet
fleet = FleetCore(FleetConfig(name="my-first-fleet", dim=128))

# Spawn agents
for i in range(5):
    fleet.spawn(name=f"explorer-{i}", room="harbor")

# Run one generation
result = fleet.tick()

print(f"Generation {result['generation']}: {result['stats']}")
```

## CLI

```bash
# Welcome message
cocapn-fleet welcome

# Interactive demo
cocapn-fleet demo

# Spawn an agent
cocapn-fleet spawn --name "my-agent" --room "forge"

# Run breeding cycle
cocapn-fleet tick

# Check status
cocapn-fleet status
```

## Next Steps

- Explore the [web demos](../web/demos/) — visual interactive guides
- Read [Architecture Deep Dive](architecture.md) — understand the A2A-first stack
- Study [Agent Breeding](breeding.md) — learn the lifecycle
- Dive into [FLUX Constraints](constraints.md) — formal verification

## Visual Demos

Open `web/landing/index.html` in your browser for an interactive tour.

| Demo | What It Shows |
|---|---|
| [Turbovec](demos/turbovec.html) | DNA memory compression and search |
| [FLUX](demos/flux.html) | Constraint checking pipeline |
| [PLATO](demos/plato.html) | Room system and spells |
| [Trinity](demos/trinity.html) | Fitness scoring and tournaments |
| [A2A](demos/a2a.html) | Agent-to-agent protocol |

## Architecture at a Glance

```
User → UI2A → A2A → Orchestrator → A2A → {Agent Mesh} → A2A → Hardware
                    ↓
              FLUX (constraint agent)
                    ↓
              Code (zerolang, generated on demand)
```

**The application is the architecture. Code is the evolving fallback.**

## Getting Help

- [GitHub Issues](https://github.com/SuperInstance/cocapn-fleet-ultimate/issues)
- [Fleet Overview Presentation](../presentations/fleet-overview.html)
- [Technical Specification](../presentations/technical-spec.html)

---

*Welcome to the fleet. 🔥*
