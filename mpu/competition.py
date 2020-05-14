def get_neighbors(grid, pos):
    """
    Get all neighbors to pos within the grid.

    Parameters
    ----------
    grid : List[Any]
    pos : List[int]

    Returns
    -------
    neigbors : generator

    Examples
    --------
    >>> list(get_neighbors([1,2,3,4,5], [0]))
    [(1,)]
    >>> list(get_neighbors([1,2,3,4,5], [1]))
    [(0,), (2,)]

    >>> list(get_neighbors([[1,2], [3,4]], [0, 0]))
    [(1, 0), (0, 1)]
    >>> list(get_neighbors([[1,2], [3,4]], [1, 0]))
    [(0, 0), (1, 1)]
    """
    pos = tuple(pos)
    lengths = []
    part = grid
    for p in pos:
        lengths.append(len(part))
        part = part[p]
    for dimension in range(len(pos)):
        if pos[dimension] > 0:
            yield pos[:dimension] + (pos[dimension] - 1,) + pos[dimension + 1 :]
        if pos[dimension] < lengths[dimension] - 1:
            yield pos[:dimension] + (pos[dimension] + 1,) + pos[dimension + 1 :]
