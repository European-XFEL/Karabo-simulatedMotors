#############################################################################
# Author: samadlia
#
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
from asyncio import CancelledError, sleep

from karabo.middlelayer import (
    AccessMode, Configurable, Device, Float, MetricPrefix, Node, QuantityValue,
    Slot, State, Unit, VectorString, background, unit)

DEFAULT_MAX_STEP = QuantityValue(0.001, unit.meter)


class LinearAxis(Configurable):
    updateRate = Float(
        displayedName="Update Rate",
        defaultValue=2,
        unitSymbol=Unit.HERTZ)

    @Slot(displayedName="Stop", allowedStates=[State.MOVING])
    async def stop(self):
        if self.move_task:
            self.move_task.cancel()
            self.move_task = None

    @Slot(displayedName="Move", allowedStates=[State.ON, State.MOVING])
    async def move(self):
        if not self.move_task:
            self.move_task = background(self.move_action())
            self.parent.updateState()

    async def move_action(self):
        try:
            distance = self.targetPosition - self.actualPosition
            while abs(distance) > self.max_step:
                if distance.value > 0:
                    self.actualPosition += self.max_step
                else:
                    self.actualPosition -= self.max_step
                distance = self.targetPosition - self.actualPosition
                await sleep(1 / self.updateRate.value)
            self.actualPosition = self.targetPosition
            await sleep(1 / self.updateRate.value)
        except CancelledError:
            pass
        finally:
            self.move_task = None
            self.parent.updateState()

    actualPosition = Float(
        displayedName="Actual Position",
        defaultValue=0.0,
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI,
        accessMode=AccessMode.READONLY)

    targetPosition = Float(
        displayedName="Target Position",
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI)


class SimulatedMultiAxisMotor(Device):
    axes = VectorString(
        displayedName="Motor Axes",
        accessMode=AccessMode.READONLY)

    axis1 = Node(
        LinearAxis,
        displayedName="Axis 1")

    axis2 = Node(
        LinearAxis,
        displayedName="Axis 2")

    interfaces = VectorString(
        displayedName="Interfaces",
        defaultValue=["MultiAxisMotor"],
        accessMode=AccessMode.READONLY)

    @Slot(displayedName="Move", allowedStates=[State.ON])
    async def move(self):
        axes = [getattr(self, axis) for axis in self.axes]
        for axis in axes:
            if not axis.move_task:
                axis.move()

    @Slot(displayedName="Stop", allowedStates=[State.MOVING])
    async def stop(self):
        axes = [getattr(self, axis) for axis in self.axes]
        for axis in axes:
            axis.stop()

    async def onInitialization(self):
        self.axes = ["axis1", "axis2"]
        self.state = State.ON
        self.move_task = None
        for axisName in self.axes:
            axis = getattr(self, axisName)
            axis.parent = self
            axis.move_task = None
            axis.max_step = DEFAULT_MAX_STEP

    def updateState(self):
        axes = [getattr(self, axis) for axis in self.axes]
        is_moving = any([axis.move_task for axis in axes])
        state = State.MOVING if is_moving else State.ON
        if self.state != state:
            self.state = state
