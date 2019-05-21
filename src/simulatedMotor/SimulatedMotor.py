#############################################################################
# Author: schaffer
# Created on May, 2019, 10:37 AM
# Copyright (C) European XFEL GmbH Hamburg. All rights reserved.
#############################################################################

from karabo.middlelayer import Device, Slot, String


class SimulatedMotor(Device):
    greeting = String()

    @Slot()
    async def hello(self):
        self.greeting = "Hello world!"

    def __init__(self, configuration):
        super(SimulatedMotor, self).__init__(configuration)

    async def onInitialization(self):
        """ This method will be called when the device starts.

            Define your actions to be executed after instantiation.
        """
