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

from __future__ import annotations

import struct

from cobs import cobs
from crc import Calculator, Configuration

from pybravo.protocol.device_id import DeviceID
from pybravo.protocol.packet_id import PacketID


class Packet:
    """A serial packet defined using the Reach serial specification."""

    _crc_calculator = Calculator(
        Configuration(
            width=8,
            polynomial=0x4D,
            init_value=0x00,
            final_xor_value=0xFF,
            reverse_input=True,
            reverse_output=True,
        )
    )

    def __init__(self, device_id: DeviceID, packet_id: PacketID, data: bytes) -> None:
        """Create a new serial packet.

        Args:
            device_id: The device ID that the packet is targeting.
            packet_id: The ID of the packet.
            data: The packet value.
        """
        self.device_id = device_id
        self.packet_id = packet_id
        self.data = data

    def __str__(self) -> str:
        """Print the packet as a string.

        Returns:
            A string description of the packet.
        """
        return (
            f"Packet(Packet ID: {self.packet_id}, Device ID: {self.device_id},"
            f" Data: {self.data!r})"
        )

    def encode(self) -> bytes:
        """Encode the serial data using the COBS encoding algorithm.

        Returns:
            The encoded serial data.
        """
        data = self.data
        data += struct.pack(
            ">BBB",
            self.packet_id.value,
            self.device_id.value,
            len(self.data) + 4,
        )
        data += struct.pack(">B", self._crc_calculator.checksum(data))

        return cobs.encode(data) + b"\x00"

    @classmethod
    def decode(cls, data: bytes) -> Packet:
        """Decode the provided serial data.

        Args:
            data: The encoded serial data to decode.

        Raises:
            ValueError: Invalid CRC value
            ValueError: The actual payload is not equal to the specified payload
            ValueError: The provided data is empty

        Returns:
            A packet with decoded serial data.
        """
        if len(data) <= 0:
            raise ValueError("Cannot decode an empty byte array!")

        if data[-1] == 0:
            decoded = bytearray(cobs.decode(data[:-1]))
        else:
            decoded = bytearray(cobs.decode(data))

        actual_crc = decoded.pop()

        if not cls._crc_calculator.verify(decoded, actual_crc):
            raise ValueError("The expected and actual CRC values do not match.")

        length = decoded.pop()

        if len(decoded) + 2 != length:
            raise ValueError(
                "The specified payload size is not equal to the actual payload size."
            )

        device_id = decoded.pop()
        packet_id = decoded.pop()

        return Packet(DeviceID(device_id), PacketID(packet_id), bytes(decoded))
