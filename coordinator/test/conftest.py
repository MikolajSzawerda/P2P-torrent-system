import pytest

from coordinator.src.coordinator import Coordinator


@pytest.fixture
def coordinator() -> Coordinator:
    return Coordinator()
