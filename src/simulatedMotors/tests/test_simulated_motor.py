#############################################################################
# Author: schaffer
# Created on May, 2019, 10:37 AM
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
from contextlib import contextmanager

from karabo.middlelayer import State
from karabo.middlelayer.testing import DeviceTest, async_tst

from ..SimulatedMotor import SimulatedMotor

conf = {
    "classId": "SimulatedMotor",
    "deviceId": "TestSimulatedMotor",
}


class TestSimulatedMotor(DeviceTest):
    @classmethod
    @contextmanager
    def lifetimeManager(cls):
        cls.dev = SimulatedMotor(conf)
        with cls.deviceManager(lead=cls.dev):
            yield

    @async_tst
    async def test_instantiation(self):
        self.assertEqual(self.dev.state, State.ON)
