# Copyright (c) 2023 Evan Palmer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Demonstrates how to poll the Bravo joint positions.

This example demonstrates how to implement an asynchronous interface for interacting
with the Bravo. An example callback function is implemented to demonstrate how
to design and register callbacks.
"""

import atexit
import struct
import sys
import threading
import time

from pybravo import BravoDriver, DeviceID, Packet, PacketID


class JointReader:
    """Demonstrates how to request position messages from the Bravo."""

    def __init__(self) -> None:
        """Create a new joint position interface."""
        self._bravo = BravoDriver()
        self._running = False
        self.joint_positions = [0.0] * 7

        self._bravo.attach_callback(PacketID.POSITION, self.read_joint_position_cb)

        # Create a new thread to poll the joint angles
        self.poll_t = threading.Thread(target=self.poll_joint_angles)
        self.poll_t.daemon = True

        # Make sure that we shutdown the interface when we exit
        atexit.register(self.stop)

    def start(self) -> None:
        """Start the joint position reader."""
        self._running = True
        self.poll_t.start()

    def stop(self) -> None:
        """Stop the joint position reader."""
        self._running = False
        self.poll_t.join()

    def poll_joint_angles(self) -> None:
        """Request the current joint positions at a rate of 100 Hz."""
        while self._running:
            request = Packet(
                DeviceID.ALL_JOINTS, PacketID.REQUEST, bytes([PacketID.POSITION.value])
            )
            self._bravo.send(request)
            time.sleep(0.01)

    def read_joint_position_cb(self, packet: Packet) -> None:
        """Handle the joint position reading.

        Args:
            packet: A packet with a joint position measurement.
        """
        position: float = struct.unpack("<f", packet.data)[0]

        # The jaws are a linear joint; convert from mm to m
        if packet.device_id == DeviceID.LINEAR_JAWS:
            position *= 0.001

        # Save the joint positions at the same index as their ID
        self.joint_positions[packet.device_id.value - 1] = position


if __name__ == "__main__":
    reader = JointReader()

    reader.start()

    while True:
        try:
            print(f"The current joint positions are: {reader.joint_positions}")
            time.sleep(0.1)
        except KeyboardInterrupt:
            reader.stop()
            sys.exit()
