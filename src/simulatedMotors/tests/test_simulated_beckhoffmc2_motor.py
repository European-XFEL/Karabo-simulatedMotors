#############################################################################
# Author: schaffer
# Created on May, 2019, 10:37 AM
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
import pytest
import pytest_asyncio

from karabo.middlelayer import State, connectDevice, waitUntil
from karabo.middlelayer.testing import AsyncDeviceContext, create_instanceId

from ..SimulatedBeckhoffMC2Base import SimulatedBeckhoffMC2Base


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def simulated_motor_fixture():
    dev = SimulatedBeckhoffMC2Base({
        "classId": "SimulatedMC2BaseMotor",
        "deviceId": create_instanceId("DUT"),
        "targetVelocity": 1.
    })
    async with AsyncDeviceContext(dev=dev) as ctx:
        yield ctx


@pytest.mark.timeout(30)
@pytest.mark.asyncio(loop_scope="module")
async def test_instantiation(simulated_motor_fixture):
    dev = simulated_motor_fixture["dev"]
    assert dev.state == State.ON


@pytest.mark.timeout(30)
@pytest.mark.asyncio(loop_scope="module")
async def test_move(simulated_motor_fixture):
    dev = simulated_motor_fixture["dev"]
    assert dev.state == State.ON
    proxy = await connectDevice(dev.deviceId)

    for tgt in (1.234, 4.321):
        proxy.targetPosition = tgt
        await proxy.move()
        assert dev.state == State.MOVING
        await waitUntil(lambda: proxy.state != State.MOVING)
        assert dev.state == State.ON
        assert pytest.approx(proxy.actualPosition.value) == tgt


@pytest.mark.timeout(30)
@pytest.mark.asyncio(loop_scope="module")
async def test_stop(simulated_motor_fixture):
    dev = simulated_motor_fixture["dev"]
    assert dev.state == State.ON
    proxy = await connectDevice(dev.deviceId)
    start_pos = dev.actualPosition.value
    tgt = start_pos + 100.
    proxy.targetPosition = tgt
    await proxy.move()
    assert dev.state == State.MOVING
    await proxy.stop()
    await waitUntil(lambda: proxy.state != State.STOPPING)
    assert dev.state == State.ON
    assert start_pos < proxy.actualPosition.value < tgt


@pytest.mark.timeout(30)
@pytest.mark.asyncio(loop_scope="module")
async def test_step(simulated_motor_fixture):
    dev = simulated_motor_fixture["dev"]
    assert dev.state == State.ON
    proxy = await connectDevice(dev.deviceId)
    step_size = 1.234
    proxy.stepSize = step_size
    start_pos = dev.actualPosition.value

    await proxy.stepUp()
    assert dev.state == State.MOVING
    await waitUntil(lambda: proxy.state != State.MOVING)
    assert dev.state == State.ON
    assert pytest.approx(proxy.actualPosition.value) == start_pos + step_size

    await proxy.stepDown()
    assert dev.state == State.MOVING
    await waitUntil(lambda: proxy.state != State.MOVING)
    assert dev.state == State.ON
    assert pytest.approx(proxy.actualPosition) == start_pos
