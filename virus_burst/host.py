"""
The host cell submodel. Cells grow and divide when their mass doubles.
"""

from process_bigraph import Composite, Process, Step, allocate_core
from virus_burst.report import print_cells

# Schema
CELLS = {'_type' : 'map', '_value' : {'mass' : 'float'}}

# Processes

class Grow(Process):
    """
    Cell mass grows at a rate proportional to the cell mass.
    """
    config_schema = {"rate" : "float"}

    def inputs(self):
        return {'cells':CELLS}

    def outputs(self):
        return {'cells':CELLS}

    def update(self, state, interval):
        changes = {}
        for cell_id, cell in state['cells'].items():
            growth = cell['mass']*self.config['rate']*interval
            changes[cell_id] = {'mass' : growth}
        return {'cells' : changes}

class Divide(Step):
    """
    Cells divide to give two daughters when mass reaches a threshold.
    """
    config_schema = {"threshold" : "float"}

    def inputs(self):
        return {'cells':CELLS}

    def outputs(self):
        return {'cells':CELLS}

    def update(self, state):

        # A list of IDs for cells being removed
        removed_cells = []

        # Dictionary entries for new cells and their states
        added_cells = {}

        for cell_id, cell in state['cells'].items():
            if cell['mass'] >= self.config['threshold']:
                removed_cells.append(cell_id)
                for i in range(2):
                    added_cells[f'{cell_id}_{i}'] = {'mass':cell['mass']/2}
        if not removed_cells:
            return {'cells' : {}}
        return {'cells' : {'_remove':removed_cells, '_add':added_cells}}

# Assemble the model

def build_cell(growth_rate, division_mass):
    """
    Assemble the host submodel as a single initial cell.
    """
    core = allocate_core()
    core.register_link('Grow',Grow)
    core.register_link('Divide',Divide)

    state = {
        'cells' : {'c0':{'mass':1.0}},
        'grow' : {
            '_type':'process',
            'address':'local:Grow',
            'config':{'rate':growth_rate},
            'interval':1.0,
            'inputs':{'cells':['cells']},
            'outputs':{'cells':['cells']},
        },
        'divide' : {
            '_type':'step',
            'address':'local:Divide',
            'config':{'threshold':division_mass},
            'inputs':{'cells':['cells']},
            'outputs':{'cells':['cells']},
        },
             }
    return Composite({'schema':{'cells':CELLS},'state':state},core=core)


# Prepare simulation

def main():
    composite = build_cell(growth_rate=0.1, division_mass=2.0)
    print_cells(0, composite.state['cells'])
    for t in range(1, 17):
        composite.run(1.0)
        print_cells(t, composite.state['cells'])

# Run simulation

if __name__ == '__main__':
    main()