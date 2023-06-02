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

"""An enum wrapper that provides an abstraction for the ID of a Packet.

The PacketID provides an abstraction for each of the packet IDs supported by the Reach
serial protocol.

Usage:
    ```
    # Create a packet ID from an integer
    packet_id = PacketID(1)

    # Get the hex value assigned to the packet ID
    value = PacketID.POSITION.value
    ```
"""

from enum import Enum


class PacketID(Enum):
    """The ID of a packet."""

    MODE = 0x01
    VELOCITY = 0x02
    POSITION = 0x03
    CURRENT = 0x05
    RELATIVE_POSITION = 0x0E
    INDEXED_POSITION = 0x0D
    REQUEST = 0x60
    SERIAL_NUMBER = 0x61
    MODEL_NUMBER = 0x62
    TEMPERATURE = 0x66
    SOFTWARE_VERSION = 0x6C
    KM_END_POS = 0xA1
    KM_END_VEL = 0xA2
    KM_END_VEL_LOCAL = 0xCB
    KM_BOX_OBSTACLE_02 = 0xA5
    KM_BOX_OBSTACLE_03 = 0xA6
    KM_BOX_OBSTACLE_04 = 0xA7
    KM_BOX_OBSTACLE_05 = 0xA8
    KM_CYLINDER_OBSTACLE_02 = 0xAB
    KM_CYLINDER_OBSTACLE_03 = 0xAC
    KM_CYLINDER_OBSTACLE_04 = 0xAD
    KM_CYLINDER_OBSTACLE_05 = 0xAE
    VOLTAGE = 0x90
    SAVE = 0x50
    HEARTBEAT_FREQUENCY = 0x92
    HEARTBEAT_SET = 0x91
    POSITION_LIMITS = 0x10
    VELOCITY_LIMITS = 0x11
    CURRENT_LIMITS = 0x12
    ATI_FT_READING = 0xD8
    BOOTLOADER = 0xFF
    VOLTAGE_THRESHOLD_PARAMETERS = 0x99
