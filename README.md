# viva-existential

An early-stage [process-bigraph](https://github.com/vivarium-collective/process-bigraph)
example modeling cell populations that grow, divide, and burst under viral
infection. The code lives in the `virus_burst` package.

Two submodels are currently implemented and run independently; composing them
into a single model is the next step (see [Status](#status)).

## What it provides

The `virus_burst` package defines two small process-bigraph models over a shared
`CELLS` schema (`{'_type': 'map', '_value': {'mass': 'float'}}`), where each cell
is tracked by id and carries a `mass`.

**Host cell growth and division** (`virus_burst/host.py`):

- `Grow` — a `Process` that increases each cell's mass at a rate proportional to
  its current mass.
- `Divide` — a `Step` that splits a cell into two daughters (each half the mass)
  once its mass reaches a threshold, using the schema's `_add` / `_remove`
  operations.
- `build_cell(growth_rate, division_mass)` — assembles a `Composite` seeded with
  a single cell.

**Viral replication and lysis** (`virus_burst/virus.py`):

- `ViralReplication` — a `Process` that grows an infected cell's viral mass at a
  constant rate.
- `Lyse` — a `Step` that removes (lyses) a cell once its viral mass reaches a
  critical threshold.
- `build_virus_sim(viral_rate, lytic_threshold)` — assembles a `Composite`
  seeded with a population of ten cells at randomized initial viral mass.

**Shared reporting** (`virus_burst/report.py`):

- `print_cells(t, cells)` — prints the per-cell and total mass at a time step.

## Install

The project pins its dependencies in `requirements.txt`:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Quick start

Each submodel is runnable on its own from the repository root. Both build a
`Composite` and step it forward, printing the cell population at each tick:

```bash
python -m virus_burst.host     # cells grow and divide as mass doubles
python -m virus_burst.virus    # cells accumulate viral mass and lyse at threshold
```

Or drive a model directly:

```python
from virus_burst.host import build_cell

composite = build_cell(growth_rate=0.1, division_mass=2.0)
for _ in range(16):
    composite.run(1.0)
print(composite.state['cells'])
```

## Status

`virus_burst/merged.py` is a placeholder for the combined model — at this stage
the host growth/division and viral replication/lysis models exist and run
separately, but have not yet been composed together.

## License

MIT. See [LICENSE](LICENSE).
