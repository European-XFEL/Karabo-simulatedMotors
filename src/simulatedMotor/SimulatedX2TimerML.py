#############################################################################
# Author: samadlia
#
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
from asyncio import CancelledError

from karabo.middlelayer import (
    Device, Float, Int32, MetricPrefix, Overwrite, QuantityValue, Slot, State,
    Unit, background, sleep, unit)

max_step = QuantityValue(0.001, unit.meter)


class SimulatedX2TimerML(Device):
    state = Overwrite(
        displayedName="State",
        defaultValue=State.ON)

    actualPosition = Float(
        displayedName="actualPosition",
        defaultValue=0,
        unitSymbol=Unit.SECOND,
        metricPrefixSymbol=MetricPrefix.NANO)

    targetPosition = Float(
        displayedName="targetPosition",
        defaultValue=0,
        unitSymbol=Unit.SECOND,
        metricPrefixSymbol=MetricPrefix.NANO)

    steps = Int32(
        displayedName="steps",
        description="Steps for internal movement",
        defaultValue=2,
        minInc=1)

    updateRate = Float(
        displayedName="Update Rate",
        defaultValue=2,
        unitSymbol=Unit.HERTZ)

    def __init__(self, configuration):
        super().__init__(configuration=configuration)
        self.move_task = None

    @Slot(displayedName="Move", allowedStates=[State.ON])
    async def move(self):
        if not self.move_task:
            self.move_task = background(self.move_action())
            self.state = State.MOVING

    async def move_action(self):
        try:
            await sleep(1 / self.updateRate.value)
            self.actualPosition = self.targetPosition
        except CancelledError:
            pass
        finally:
            self.state = State.ON
            self.move_task = None

    @Slot(displayedName="Stop", allowedStates=[State.MOVING])
    async def stop(self):
        if self.move_task:
            self.move_task.cancel()
            self.move_task = None
