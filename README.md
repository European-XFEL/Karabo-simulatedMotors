# SimulatedMotors Library (MiddleLayer)

## Description

The simulatedMotors library contains the following simulated motors, which can
easily be used in the GUI, unit tests, and similar contexts:

- SimulatedMotor
- SimulatedBeckhoffMC2Base
- SimulatedMultiAxisMotor
- SimulatedX2TimerML

## Testing

Every Karabo device in Python is shipped as a regular Python package. To make
the device visible to any device server, install the package in Karabo's own
Python environment.

From the directory containing `pyproject.toml`, run:

```bash
pip install -e .
```

Alternatively, use the `karabo` utility script:

```bash
karabo develop simulatedMotors
```

## Running

To manually start a server using these devices, run:

```bash
karabo-middlelayerserver serverId=middleLayerServer/1 \\
    deviceClasses=SimulatedMotor,SimulatedBeckhoffMC2Base,SimulatedMultiAxisMotor,SimulatedX2TimerML
```

Or use a properly configured:

```bash
karabo-start
```
