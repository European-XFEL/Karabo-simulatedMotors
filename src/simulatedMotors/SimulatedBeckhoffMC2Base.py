#############################################################################
# Author: samadlia
#
# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
#############################################################################
from asyncio import CancelledError

from karabo.middlelayer import Float, State, Unit, sleep

from ._version import version as deviceVersion
from .SimulatedMotor import SimulatedMotor


class SimulatedBeckhoffMC2Base(SimulatedMotor):
    # provide version for classVersion property
    __version__ = deviceVersion

    targetVelocity = Float(
        displayedName="Target Velocity",
        defaultValue=10.0,
        minInc=0.001)

    guiUpdateRate = Float(
        displayedName="GUI Update Rate",
        description="GUI Update Rate shows how often GUI should show"
                    "the updates of actualPosition."
                    "NOTE: GUI can handle max 2Hz update frequency.",
        defaultValue=2,
        unitSymbol=Unit.HERTZ,
        minInc=0.1,
        maxInc=2)

    async def move_action(self):
        try:
            if self.targetPosition < self.actualPosition:
                direction = -1
            else:
                direction = 1

            distance = abs(self.targetPosition - self.actualPosition)
            # GUI can show updates at max 2 Hz frequency
            # show (t * guiUpdateRate) updates
            # steps = t * guiUpdateRate, where t = distance / velocity
            time_to_reach_target = distance.value / self.targetVelocity.value
            self.steps = int(time_to_reach_target * self.guiUpdateRate.value)
            for _ in range(self.steps):
                if self.state == State.MOVING:
                    await sleep(1.0 / self.guiUpdateRate.value)
                    self.actualPosition = (
                        self.actualPosition.value +
                        self.targetVelocity.value * direction /
                        self.guiUpdateRate.value)
                else:
                    break
        except CancelledError:
            pass
        finally:
            if (self.actualPosition != self.targetPosition and
                    self.state == State.MOVING):
                # Calculate how many mm distance left to target
                distance_left = (
                    distance.value -
                    self.steps.value * self.targetVelocity.value /
                    self.guiUpdateRate.value)
                # Calculate exactly how many seconds it will take
                # to cover the distance left
                await sleep(distance_left / self.targetVelocity.value)
                self.actualPosition = self.targetPosition

            self.state = State.ON
