"""
A printing helper shared by the models
"""

def print_cells(t, cells):
    """
    Prints the total mass and the mass of all cells in cells

    Args:
    - t: the time step
    - cells: a dictionary mapping cell ids to cell masses

    Prints:
    - The mass of all cells and total mass at each time step
    """
    total_mass = sum(cell['mass'] for cell in cells.values())

    parts = []

    for cell_id, cell in sorted(cells.items()):
        parts.append(f'{cell_id}: {cell["mass"]:.3f}')

    print(f't={t} total_mass={total_mass:.3f} ' + ', '.join(parts))