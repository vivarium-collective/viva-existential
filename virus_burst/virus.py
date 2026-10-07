"""
The virus module. When the cell's viral mass
reaches a critical value, it bursts and replaces the cell with nothing.
"""

from process_bigraph import Composite, Process, Step, allocate_core
from virus_burst.report import print_cells
import numpy as np

# Schema

CELLS = {'_type' : 'map', '_value' : {'mass' : 'float'}}


# Processes

class ViralReplication(Process):
    """
    The amount of virus in an infected cell grows at a constant rate.
    """
    config_schema = {
        'rate' : "float"
    }

    def inputs(self):
        return {'cells' : CELLS}

    def outputs(self):
        return {'cells' : CELLS}

    def update(self, state, interval):
        """
        Every infected cell's viral mass increases by a constant rate.
        """
        # Prepare a dictionary to record changes
        changes = {}
        for cell_id, cell in state['cells'].items():
            if cell['mass']>0.0:
                changes[cell_id] = {'mass': self.config['rate']*interval}
            else:
                changes[cell_id] = {'mass': 0.0}

        return {'cells':changes}

class Lyse(Step):
    """
    A cell is erased when the (viral) mass reaches a critical threshold.
    """
    config_schema = {'threshold' : "float"}

    def inputs(self):
        return {'cells' : CELLS}

    def outputs(self):
        return {'cells' : CELLS}

    def update(self, state):

        # A list for cells being removed
        lysing_cells = []

        for cell_id, cell in state['cells'].items():
            if cell['mass']>=self.config['threshold']:
                lysing_cells.append(cell_id)

        if not lysing_cells:
            return {'cells' : {}}

        return {'cells': {'_remove': lysing_cells}}

# Preparing the model. A population of ten cells will be generated,
# each with a randomized amount of viral mass in the range (0,1.0].

def initialize_population(viral_rate, lytic_threshold):
    """
    Assemble the population of cells with a randomized amount of viral mass.
    """
    core = allocate_core()
    core.register_link('ViralReplication',ViralReplication)
    core.register_link('Lyse',Lyse)

    rng = np.random.default_rng(0)

    state = {
        # Create a population of ten cells with a mass in the range of (0.0,1.0)
        'cells': {f'c{i}': {'mass': rng.uniform(0.0, 1.0)} for i in range(10)},
        'viralreplication' : {
            '_type':'process',
            'address':'local:ViralReplication',
            'config':{'rate':viral_rate},
            'interval':1.0,
            'inputs':{'cells':['cells']},
            'outputs':{'cells':['cells']}
        },
        'lyse' : {
            '_type':'step',
            'address':'local:Lyse',
            'config':{'threshold':lytic_threshold},
            'inputs':{'cells':['cells']},
            'outputs':{'cells':['cells']},
        },

    }


    return Composite({'schema':{'cells':CELLS},'state':state},core=core)

# Prepare simulation

def main():
    composite = initialize_population(viral_rate=0.125, lytic_threshold=2.5)
    print_cells(0,composite.state['cells'])
    for t in range(1, 30):
        composite.run(1.0)
        print_cells(t,composite.state['cells'])

# Run Simulation
if __name__ == '__main__':
    main()

