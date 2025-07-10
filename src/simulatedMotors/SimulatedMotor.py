#############################################################################
# Author: schaffer
# Created on May, 2019, 10:37 AM
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
from asyncio import CancelledError

from karabo.middlelayer import (
    AccessMode, Bool, Device, Float, Int32, MetricPrefix, Slot, State, Unit,
    VectorString, background, sleep)

from ._version import version as deviceVersion


class SimulatedMotor(Device):
    # provide version for classVersion property
    __version__ = deviceVersion

    interfaces = VectorString(
        displayedName="Interfaces",
        description="Describes the interfaces for this device",
        defaultValue=["Motor"],
        accessMode=AccessMode.READONLY)

    actualPosition = Float(
        displayedName="Actual Position",
        description="Position of the simulated motor",
        defaultValue=0,
        accessMode=AccessMode.READONLY,
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI
    )

    targetPosition = Float(
        displayedName="Target Position",
        description="Target position of the simulated motor",
        defaultValue=0,
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI
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

    steps = Int32(
        displayedName="Steps",
        description="Steps for internal movement",
        defaultValue=2,
        minInc=1)

    updateRate = Float(
        displayedName="Update Rate",
        defaultValue=2,
        unitSymbol=Unit.HERTZ)

    def __init__(self, configuration):
        super().__init__(configuration)
        self.move_task = None

    async def onInitialization(self):
        """ This method will be called when the device starts.

            Define your actions to be executed after instantiation.
        """
        self.state = State.ON

    @Slot(
        displayedName="Move",
        description='Moves the simulated motor to the target position, in the '
                    'time defined by "Move Time"',
        allowedStates=[State.ON]
    )
    async def move(self):
        if self.targetPosition.value != self.actualPosition.value:
            self.state = State.MOVING
            self.move_task = background(self.move_action)

    async def move_action(self):
        try:
            distance = self.targetPosition - self.actualPosition
            step_size = distance / self.steps
            for _ in range(self.steps):
                if self.state == State.MOVING:
                    self.actualPosition += step_size
                    await sleep(1 / self.updateRate.value)
                else:
                    return
        except CancelledError:
            pass
        finally:
            self.state = State.ON

    @Slot(
        displayedName="Stop",
        description="Stops the simulated motor",
        allowedStates=[State.MOVING]
    )
    async def stop(self):
        self.move_task.cancel()
        self.state = State.ON
