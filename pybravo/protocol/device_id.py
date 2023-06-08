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

"""An enum wrapper that provides an abstraction for the ID of a device.

The DeviceID provides an abstraction for each of the device IDs supported by the Reach
serial protocol.

Examples:
    >>> DeviceID.LINEAR_JAWS.value
    0x01
    >>> DeviceID(1)
    DeviceID.LINEAR_JAWS
"""

from enum import Enum


class DeviceID(Enum):
    """The ID of a device on the Reach Bravo 7."""

    LINEAR_JAWS = 0x01
    ROTATE_END_EFFECTOR = 0x02
    BEND_FOREARM = 0x03
    ROTATE_ELBOW = 0x04
    BEND_ELBOW = 0x05
    BEND_SHOULDER = 0x06
    ROTATE_BASE = 0x07
    ALL_JOINTS = 0xFF
    FORCE_TORQUE_SENSOR = 0x0D
