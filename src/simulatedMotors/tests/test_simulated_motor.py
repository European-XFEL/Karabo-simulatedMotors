#############################################################################
# Author: schaffer
# Created on May, 2019, 10:37 AM
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
import pytest
import pytest_asyncio

from karabo.middlelayer import State
from karabo.middlelayer.testing import AsyncDeviceContext, create_instanceId

from ..SimulatedMotor import SimulatedMotor


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def simulated_motor_fixture():
    dev = SimulatedMotor({
        "classId": "SimulatedMotor",
        "deviceId": create_instanceId("TestSimulatedMotor"),
    })
    async with AsyncDeviceContext(dev=dev) as ctx:
        yield ctx


@pytest.mark.timeout(30)
@pytest.mark.asyncio(loop_scope="module")
async def test_instantiation(simulated_motor_fixture):
    dev = simulated_motor_fixture["dev"]
    assert dev.state == State.ON
