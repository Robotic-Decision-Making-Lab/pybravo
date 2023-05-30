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

import sys

import pytest  # noqa

sys.path.append("..")

from protocol import DeviceID, Packet, PacketID  # noqa


def test_packet_encoding() -> None:
    """Test that the packet encoding properly encodes serial data."""
    expected_encoding = bytes([0x06, 0x03, 0x60, 0x01, 0x05, 0x52, 0x00])

    packet = Packet(
        DeviceID.LINEAR_JAWS, PacketID.REQUEST, bytes([PacketID.POSITION.value])
    )

    assert expected_encoding == packet.encode()


def test_data_decoding() -> None:
    """Test that the serial data decoding properly decodes the serial data."""
    encoded_data = bytes([0x09, 0x01, 0x02, 0x03, 0x04, 0x01, 0xFF, 0x08, 0x5D, 0x00])
    decoded_data = bytes([0x01, 0x02, 0x03, 0x04])

    assert decoded_data == Packet.decode(encoded_data).data
