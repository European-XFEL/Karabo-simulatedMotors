import pytest

from karabo.middlelayer.testing import KaraboTestLoopPolicy


@pytest.fixture(scope="session")
def event_loop_policy():
    return KaraboTestLoopPolicy()
