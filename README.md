# pybravo :mechanical_arm:

pybravo is a Python interface for interacting with the [Reach Bravo 7
manipulator](https://reachrobotics.com/products/manipulators/reach-bravo/).

## :warning: Disclaimer :warning:

This is an independent project, and is not affiliated with or maintained by
Reach Robotics. Please refer to the [Reach Robotics
SDK](https://github.com/Reach-Robotics/reach_robotics_sdk/tree/master)
for all official software.

## Main features

The main features of pybravo include:

- An easy-to-use interface for sending and receiving packets from the
  Bravo arm
- Implements the Reach Serial protocol
- Attach callbacks for asynchronous packet handling

## Quick start

Refer to the following code snippet for a simple example showing how to get
started with pybravo. Additional examples may be found in the project examples.

```python
import struct
import time

from bravo import BravoDriver, PacketID, DeviceID, Packet


def example_joint_positions_cb(packet: Packet) -> None:
    """Read the joint positions from the Bravo 7.

    Args:
        packet: The joint position packet.
    """
    position: float = struct.unpack("<f", packet.data)[0]
    print(
        f"The current joint position of joint {packet.device_id} is {position}"
    )


if __name__ == "__main__":
    bravo = BravoDriver()

    # Attempt to establish a connection with the Bravo
    bravo.connect()

    # Attach a callback to be executed when a packet with the POSITION ID is
    # received
    bravo.attach_callback(PacketID.POSITION, example_joint_positions_cb)

    # Create a request for the current joint positions
    request = Packet(
        DeviceID.ALL_JOINTS, PacketID.REQUEST, bytes([PacketID.POSITION])
    )

    # Send the request
    bravo.send(request)

    # Wait a second for the Bravo to respond to the request
    time.sleep(1.0)

    bravo.disconnect()
```
