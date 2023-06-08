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

"""Provides an interface to the Reach Bravo 7 manipulator.

The ``BravoDriver`` provides an interface for sending and receiving serial data from the
Reach Bravo 7 manipulator.

Examples:
    >>> bravo = BravoDriver()
    >>> bravo.connect()
    >>> packet = Packet(
            DeviceID.LINEAR_JAWS, PacketID.REQUEST, bytes([PacketID.POSITION.value])
        )
    >>> bravo.send(packet)
"""

import atexit
import logging
import socket
import threading
from typing import Callable

from pybravo.protocol import Packet, PacketID


class BravoDriver:
    """Low-level interface for sending and receiving serial data from the Bravo 7."""

    def __init__(self) -> None:
        """Create a new driver."""
        self.callbacks: dict[PacketID, list[Callable]] = {}

        # Leave this private because we don't want anyone to accidentally disable the
        # polling thread
        self._running = False

        # Set the address to none during configuration to enable changing the address
        # when the connection happens
        self.address: tuple[str, int] | None = None

        # Configure the logger
        logging.basicConfig()
        self._logger = logging.getLogger("BravoDriver")
        self._logger.setLevel(logging.INFO)

        # Create a thread to poll for incoming packets
        self._poll_t = threading.Thread(target=self._poll)
        self._poll_t.setDaemon(True)

        # Shutdown the connection on exit
        atexit.register(self.disconnect)

    def connect(self, ip: str = "192.168.2.3", port: int = 6789) -> None:
        """Establish a connection between the Bravo 7 and the driver.

        Args:
            ip: The IP address of the Bravo 7. Defaults to "192.168.2.4".
            port: The port to connect with the Bravo 7 over. Defaults to 6789.
        """
        self.address = (ip, port)

        # Configure a new socket with the Bravo
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)

        self._running = True
        self._poll_t.start()
        self._logger.info(
            "Successfully established a connection to the Reach Bravo 7 manipulator."
        )

    def disconnect(self) -> None:
        """Disconnect the driver from the Bravo 7."""
        # Reset the address for future connections
        self.address = None

        # Stop the thread
        self._running = False
        self._poll_t.join()
        self._logger.info(
            "Successfully shut down the connection to the Reach Bravo 7 manipulator."
        )

    def send(self, packet: Packet) -> None:
        """Send a packet to the Bravo 7.

        Args:
            packet: The serial packet to send.
        """
        if self.address is None:
            raise RuntimeError(
                "Packets can't be sent without first establishing a connection!"
            )

        self.sock.sendto(packet.encode(), self.address)

    def attach_callback(self, packet_id: PacketID, callback: Callable) -> None:
        """Bind a callback to the given packet type.

        Args:
            packet_id: The ID of the packet that, when received, should signal the
                callback.
            callback: The callback to execute when a packet with the given ID is
                received.
        """
        # We want to allow multiple callbacks to be attached to one packet ID
        if packet_id not in self.callbacks:
            self.callbacks[packet_id] = []

        # Don't allow duplicate callbacks to be added to the list. This would result
        # In the callback being run multiple times when a packet is received.
        if callback not in self.callbacks[packet_id]:
            self.callbacks[packet_id].append(callback)

    def _poll(self) -> None:
        """Poll the socket for new data and call the registered callbacks."""
        while self._running:
            try:
                read_data, _ = self.sock.recvfrom(256)
            except BaseException:
                ...
            else:
                if read_data == b"":
                    continue

                try:
                    packet = Packet.decode(read_data)
                except Exception as e:
                    self._logger.debug(
                        "An error occurred while attempting to decode the"
                        f" data: {read_data!r}",
                        e,
                    )
                else:
                    try:
                        for cb in self.callbacks[packet.packet_id]:
                            cb(packet)
                    except Exception as e:
                        self._logger.warning(
                            "An exception occurred while trying to execute a callback"
                            f" for the packet {packet}.",
                            e,
                        )
