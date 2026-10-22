"""
The merged virus and host cell models. Only imports and wiring, nothing changed from the
two models individually.
"""

import numpy as np
# Importing the host and virus
from virus_burst import host as h
from virus_burst import virus as v
from process_bigraph import Composite, Process, Step, allocate_core
from virus_burst.report import print_cells


# Schema
CELLS = h.CELLS

# Processes

Grow = h.Grow

Divide = h.Divide

Lyse = v.Lyse

ViralReplication = v.ViralReplication

# Build Simulation

def build_sim (growth_rate, division_mass, viral_rate, lytic_threshold):
    """
    Constructing the merged simulation
    """
    core = allocate_core()
    core.register_link('Grow', Grow)
    core.register_link('Divide', Divide)
    core.register_link('Lyse', Lyse)
    core.register_link('ViralReplication', ViralReplication)

    rng = np.random.default_rng(0)

    state = {
        # Create a population of ten cells with a mass in the range of (0.0,1.0)
        'cells': {f'c{i}': {'mass': rng.uniform(0.0, 1.0)} for i in range(10)},
        'viralreplication': {
            '_type': 'process',
            'address': 'local:ViralReplication',
            'config': {'rate': viral_rate},
            'interval': 1.0,
            'inputs': {'cells': ['cells']},
            'outputs': {'cells': ['cells']}
        },
        'lyse': {
            '_type': 'step',
            'address': 'local:Lyse',
            'config': {'threshold': lytic_threshold},
            'inputs': {'cells': ['cells']},
            'outputs': {'cells': ['cells']},
        },
        'grow': {
            '_type': 'process',
            'address': 'local:Grow',
            'config': {'rate': growth_rate},
            'interval': 1.0,
            'inputs': {'cells': ['cells']},
            'outputs': {'cells': ['cells']},
        },
        'divide': {
            '_type': 'step',
            'address': 'local:Divide',
            'config': {'threshold': division_mass},
            'inputs': {'cells': ['cells']},
            'outputs': {'cells': ['cells']},
        },
    }

    return Composite({'schema': {'cells': CELLS}, 'state': state}, core=core)

# Prepare simulation

def main():
    composite = build_sim(growth_rate=0.1, division_mass=2.0,viral_rate=0.125, lytic_threshold=2.5)
    print_cells(0,composite.state['cells'])
    for t in range(1, 30):
        composite.run(1.0)
        print_cells(t,composite.state['cells'])

# Run Simulation
if __name__ == '__main__':
    main()



