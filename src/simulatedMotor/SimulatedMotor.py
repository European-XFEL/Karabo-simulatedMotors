#############################################################################
# Author: schaffer
# Created on May, 2019, 10:37 AM
# Copyright (C) European XFEL GmbH Hamburg. All rights reserved.
#############################################################################

from karabo.middlelayer import (AccessMode, background, Bool, Device, Float,
                                sleep, Slot, State, VectorString)


class SimulatedMotor(Device):
    interfaces = VectorString(
        displayedName="Interfaces",
        description="Describes the interfaces for this device",
        defaultValue=["Motor"],
        accessMode=AccessMode.READONLY)

    actualPosition = Float(
        displayedName="Actual Position",
        description="Position of the simulated motor",
        defaultValue=0,
        accessMode=AccessMode.READONLY
    )

    targetPosition = Float(
        displayedName="Target Position",
        description="Target position of the simulated motor",
        defaultValue=0
    )

    isCWLimit = Bool(
        displayedName="Clockwise limit switch",
        defaultValue=False,
        accessMode=AccessMode.READONLY
    )

    isCCWLimit = Bool(
        displayedName="Counter-clockwise limit switch",
        defaultValue=False,
        accessMode=AccessMode.READONLY
    )

    isSWLimitLow = Bool(
        displayedName="Software lower limit",
        defaultValue=False,
        accessMode=AccessMode.READONLY
    )

    isSWLimitHigh = Bool(
        displayedName="Software upper limit",
        defaultValue=False,
        accessMode=AccessMode.READONLY
    )

    moveTime = Float(
        displayedName="Move time",
        description="Time (in seconds) for the simulated motor to make a "
                    "single move. This "
                    "can be adjusted to set the time between adjacent scan "
                    "points.",
        defaultValue=1
    )

    def __init__(self, configuration):
        super(SimulatedMotor, self).__init__(configuration)

    async def onInitialization(self):
        """ This method will be called when the device starts.

            Define your actions to be executed after instantiation.
        """
        self.state = State.ON
        self.stopped = False

    @Slot(
        displayedName="Move",
        description='Moves the simulated motor to the target position, in the '
                    'time defined by "Move Time"',
        allowedStates=[State.ON]
    )
    async def move(self):
        if self.targetPosition.value != self.actualPosition.value:
            self.state = State.MOVING
            background(self.moving_action)

    async def moving_action(self):
        starting_position = self.actualPosition.value
        velocity = (self.targetPosition - self.actualPosition) / self.moveTime
        for i in range(int(self.moveTime.value)):
            if self.stopped:
                break
            else:
                self.actualPosition = starting_position + velocity * i
                await sleep(1)

        if not self.stopped:
            await sleep(self.moveTime.value % 1)
            self.actualPosition = self.targetPosition.value
        self.stopped = False
        self.state = State.ON

    @Slot(
        displayedName="Stop",
        description="Stops the simulated motor",
        allowedStates=[State.MOVING]
    )
    async def stop(self):
        self.stopped = True
        self.state = State.ON
