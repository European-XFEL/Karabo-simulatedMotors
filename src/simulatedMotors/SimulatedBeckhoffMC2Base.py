#############################################################################
# Author: hickind
# Created on August 25, 2017, 23:25 PM
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
from asyncio import sleep

from karabo.middlelayer import (
    AccessMode, Bool, Configurable, Device, Double, Int32, MetricPrefix, Node,
    Overwrite, Slot, State, String, Unit, VectorString, background, isSet,
    unit, waitUntil)

from ._version import version as deviceVersion

motors = {}


class CouplingInterface(Configurable):

    def __init__(self, configuration):
        super().__init__(configuration=configuration)
        self.slaves = set()

    isConfigurableAsSlave = Bool(
        displayedName="Configurable as Slave",
        description="The motor is configurable as slave in a coordinated "
                    "motion.",
        accessMode=AccessMode.INITONLY,
        defaultValue=False)

    isMaster = Bool(
        displayedName="is Master",
        description="The motor is configured as master in a coordinated "
                    "motion.",
        accessMode=AccessMode.READONLY,
        defaultValue=False)

    isSlave = Bool(
        displayedName="is Slave",
        description="The motor is configured as slave in a coordinated "
                    "motion.",
        accessMode=AccessMode.READONLY,
        defaultValue=False)

    masterDevice = String(
        displayedName="Master Device",
        description="Name of the master device.",
        accessMode=AccessMode.INITONLY)

    numerator = Int32(
        displayedName="Ratio Numerator",
        description="This is the numerator of the coupling ratio. It is "
                    "valid only if this axis can be coupled.",
        defaultValue=0)

    denominator = Int32(
        displayedName="Ratio Denominator",
        description="This is the denominator of the coupling ratio. It is "
                    "valid only if this axis can be coupled.",
        defaultValue=1)

    @Slot(
        displayedName="Couple Axis",
        description="Configure the axis as a slave of the axis indicated in "
                    "the Master Motor property",
        allowedStates={State.ON})
    async def couple(self):
        if self.isConfigurableAsSlave:
            if self.masterDevice in motors:
                root = self.get_root()
                await sleep(2 * root.timeStep.value)
                master = motors[self.masterDevice]
                master.coupling.slaves.add(root.deviceId)
                master.coupling.isMaster = True
                self.isSlave = True
                root.state = State.DISABLED
                return
        raise RuntimeError('Coupling failed')

    @Slot(
        displayedName="Decouple Axis",
        description="Configure the axis as a slave of the axis indicated in "
                    "the Master Motor property",
        allowedStates={State.DISABLED})
    async def decouple(self):
        if self.isConfigurableAsSlave:
            root = self.get_root()
            await sleep(2 * root.timeStep.value)
            if self.isSlave:
                self.isSlave = False
            if self.masterDevice in motors:
                master = motors[self.masterDevice]
                if root.deviceId in master.coupling.slaves:
                    master.coupling.slaves.remove(root.deviceId)
                master.isMaster = bool(master.coupling.slaves)
            root.state = State.ON


class HwLimits(Configurable):
    cwLimit = Double(
        displayedName="CWLimit",
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI)

    ccwLimit = Double(
        displayedName="CCWLimit",
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI)

    enableCWLimit = Bool(
        displayedName="EnableCWLimit",
        defaultValue=False)

    enableCCWLimit = Bool(
        displayedName="EnableCCWLimit",
        defaultValue=False)


class SimulatedBeckhoffMC2Base(Device):

    # provide version for classVersion property
    __version__ = deviceVersion

    state = Overwrite(
        displayedName="State",
        defaultValue=State.ON)

    interfaces = VectorString(
        displayedName="Interfaces",
        description="The names of the interfaces the device complies with",
        defaultValue=["Motor"],
        accessMode=AccessMode.READONLY)

    actualPosition = Double(
        displayedName="Actual Position",
        defaultValue=0,
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI,
        accessMode=AccessMode.READONLY)

    targetPosition = Double(
        displayedName="Target Position",
        defaultValue=0,
        unitSymbol=Unit.METER,
        metricPrefixSymbol=MetricPrefix.MILLI,
        allowedStates={State.OFF, State.ON, State.MOVING})

    isOnTarget = Bool(
        displayedName="isOnTarget",
        defaultValue=True,
        accessMode=AccessMode.READONLY)

    isCWLimit = Bool(
        displayedName="isCWLimit",
        defaultValue=False,
        accessMode=AccessMode.READONLY)

    isCCWLimit = Bool(
        displayedName="isCCWLimit",
        defaultValue=False,
        accessMode=AccessMode.READONLY)

    isSWLimitHigh = Bool(
        displayedName="isSWLimitHigh",
        defaultValue=False)

    isSWLimitLow = Bool(
        displayedName="isSWLimitLow",
        defaultValue=False,
        accessMode=AccessMode.READONLY)

    @Double(
        displayedName="Target Velocity",
        defaultValue=0.1,
        allowedStates={State.OFF, State.ON, State.MOVING})
    def targetVelocity(self, value):
        self.targetVelocity = value
        if isSet(value) and isSet(self.timeStep):
            targetVelocity = self.targetVelocity * unit.mm / unit.s
            self.max_step = targetVelocity * self.timeStep

    coupling = Node(
        CouplingInterface,
        displayedName="Coupling Interface"
    )

    hwLimits = Node(
        HwLimits,
        displayedName="Hardware Limits"
    )

    timeStep = Double(
        displayedName="Time Step",
        defaultValue=0.1,
        unitSymbol=Unit.SECOND,
        accessMode=AccessMode.INITONLY)

    def __init__(self, configuration):
        super().__init__(configuration=configuration)
        self.move_task = None

    async def onInitialization(self):
        motors[self.deviceId] = self
        await super().onInitialization()
        self.actualTargetPosition = self.actualPosition
        targetVelocity = self.targetVelocity * unit.mm / unit.s
        self.max_step = targetVelocity * self.timeStep

    async def onDestruction(self):
        motors.pop(self.deviceId, None)
        await super().onDestruction()

    async def reset(self):
        if self.move_task is not None:
            self.move_task.cancel()
            await waitUntil(lambda: self.move_task is None)
            self.state = State.ON
        self.max_step = self.targetVelocity * self.timeStep
        self.actualPosition = 0
        self.actualTargetPosition = self.actualPosition
        self.targetPosition = 0
        self.coupling.isSlave = False

    def dump(self):
        print('\ndump\n')
        print('{}'.format(self.deviceId))
        print('state: {}'.format(self.state))
        print('iOT: {}'.format(self.isOnTarget))
        print('eP: {}'.format(self.actualPosition))
        print('tP: {}'.format(self.targetPosition))
        print('step: {}'.format(self.max_step))
        print()

    @Slot(
        displayedName="Off",
        allowedStates={State.ON})
    async def off(self):
        self.state = State.OFF

    @Slot(
        displayedName="On",
        allowedStates={State.OFF})
    async def on(self):
        self.state = State.ON

    @Slot(
        displayedName="Move",
        allowedStates={State.ON})
    async def move(self):
        self.actualTargetPosition = QuantityValue(
            self.targetPosition,
            timestamp=get_timestamp())
        if self.coupling.isSlave:
            return
        if not self.move_task:
            if self.targetPosition != self.actualPosition:
                self.move_task = background(self.move_action())
                self.state = State.MOVING
            else:
                self.state = State.ON

    async def move_action(self):
        try:
            distance = self.targetPosition - self.actualPosition
            hwOk = True
            while hwOk and abs(distance) > self.max_step:
                hwOk = self.checkHwLimits()
                slave_motors = [
                    motors[slave] for slave in self.coupling.slaves]
                if any([not motor.checkHwLimits() for motor in slave_motors]):
                    hwOk = False

                if distance.value > 0:
                    step = self.max_step
                else:
                    step = -self.max_step
                self.actualPosition += step
                for slave in self.coupling.slaves:
                    slaveDev = motors[slave]
                    coupling = slaveDev.coupling
                    ratio = coupling.numerator / coupling.denominator
                    slaveDev.actualPosition += step * ratio

                if self.isOnTarget:
                    self.isOnTarget = False
                for slave in self.coupling.slaves:
                    slaveDev = motors[slave]
                    slaveDev.isOnTarget = False

                await sleep(self.timeStep.value)

                distance = self.targetPosition - self.actualPosition

            hwOk = self.checkHwLimits()
            if hwOk:
                for slave in self.coupling.slaves:
                    slaveDev = motors[slave]
                    coupling = slaveDev.coupling
                    ratio = coupling.numerator / coupling.denominator
                    step = self.targetPosition - self.actualPosition
                    slaveDev.actualPosition += step * ratio
                self.actualPosition = self.targetPosition

                if not self.isOnTarget:
                    self.isOnTarget = True
                for slave in self.coupling.slaves:
                    slaveDev = motors[slave]
                    slaveDev.isOnTarget = True

                await sleep(self.timeStep.value)

        finally:
            self.state = State.ON
            self.move_task = None

    @Slot(
        displayedName="Stop",
        allowedStates={State.MOVING})
    async def stop(self):
        if self.move_task is not None:
            self.move_task.cancel()
        await waitUntil(lambda: self.state == State.ON)

    def checkHwLimits(self):
        hwLimits = self.hwLimits
        isCWLimit = hwLimits.enableCWLimit and isSet(hwLimits.cwLimit) and \
            self.actualPosition >= hwLimits.cwLimit

        isCCWLimit = hwLimits.enableCCWLimit and isSet(hwLimits.ccwLimit) and \
            self.actualPosition <= hwLimits.ccwLimit

        inc = self.state == State.MOVING and \
            self.actualTargetPosition > self.actualPosition

        dec = self.state == State.MOVING and \
            self.actualTargetPosition < self.actualPosition

        if self.isCWLimit != isCWLimit:
            self.isCWLimit = isCWLimit

        if self.isCCWLimit != isCCWLimit:
            self.isCCWLimit = isCCWLimit

        return not ((inc and isCWLimit) or (dec and isCCWLimit))
