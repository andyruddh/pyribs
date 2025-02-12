"""Tests for EvolutionStrategyEmitter."""
import numpy as np
import pytest

from ribs.archives import GridArchive
from ribs.emitters import EvolutionStrategyEmitter


def test_auto_batch_size():
    archive = GridArchive(10, [20, 20], [(-1.0, 1.0)] * 2)
    emitter = EvolutionStrategyEmitter(archive, np.zeros(10), 1.0, "obj")
    assert emitter.batch_size is not None
    assert isinstance(emitter.batch_size, int)


def test_list_as_initial_solution():
    archive = GridArchive(10, [20, 20], [(-1.0, 1.0)] * 2)
    emitter = EvolutionStrategyEmitter(archive, [0.0] * 10, 1.0, "obj")

    # The list was passed in but should be converted to a numpy array.
    assert isinstance(emitter.x0, np.ndarray)
    assert (emitter.x0 == np.zeros(10)).all()


@pytest.mark.parametrize("dtype", [np.float64, np.float32],
                         ids=["float64", "float32"])
def test_dtypes(dtype):
    archive = GridArchive(10, [20, 20], [(-1.0, 1.0)] * 2, dtype=dtype)
    emitter = EvolutionStrategyEmitter(archive, np.zeros(10), 1.0, "obj")
    assert emitter.x0.dtype == dtype

    # Try running with the negative sphere function for a few iterations.
    for _ in range(10):
        solution_batch = emitter.ask()
        objective_batch = -np.sum(np.square(solution_batch), axis=1)
        measures_batch = solution_batch[:, :2]

        status_batch, value_batch = archive.add(solution_batch, objective_batch,
                                                measures_batch)
        emitter.tell(solution_batch, objective_batch, measures_batch,
                     status_batch, value_batch)
