#############################################################################
# Author: schaffer
# Created on May, 2019, 10:37 AM
# Copyright (C) European XFEL GmbH Hamburg. All rights reserved.
#############################################################################
from contextlib import contextmanager
import unittest

from karabo.middlelayer_api.tests.eventloop import async_tst, DeviceTest

from ..SimulatedMotor import SimulatedMotor


conf = {
    "classId": "SimulatedMotor",
    "_deviceId_": "TestSimulatedMotor",
    "greeting": "buongiorno"
}


class TestSimulatedMotor(DeviceTest):
    @classmethod
    @contextmanager
    def lifetimeManager(cls):
        cls.dev = SimulatedMotor(conf)
        with cls.deviceManager(lead=cls.dev):
            yield

    @async_tst
    async def test_greet(self):
        for greet in ("Buongiorno", "Guten Tag", "Moin Moin"):
            self.dev.greeting = greet
            self.assertEqual(self.dev.greeting.value, greet)
            await self.dev.hello()
            self.assertEqual(self.dev.greeting.value, "Hello world!")
