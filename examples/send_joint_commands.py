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

"""Demonstrates how to set the joint positions of the Bravo.

This example is inspired by the `joint_control_eth.py` example from the official
Reach Robotics SDK (see the link below), and demonstrates how this package improves the
usability of the official interface.

Usage:
    `python3 send_joint_commands.py`
"""

import struct

from pybravo import BravoDriver, DeviceID, Packet, PacketID

if __name__ == "__main__":
    bravo = BravoDriver()

    # Start the bravo connection
    bravo.connect()

    # Specify the desird positions
    desired_positions = [10.0, 0.5, 1.5707, 1.5707, 1.5707, 2.8, 3.14159]

    # Create the packets and send them to the Bravo
    for i, position in enumerate(desired_positions):
        packet = Packet(DeviceID(i), PacketID.POSITION, struct.pack(">f", position))
        bravo.send(packet)
