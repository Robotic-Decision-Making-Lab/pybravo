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

import atexit
import socket
import sys
import threading
from typing import Callable
import logging

sys.path.append("..")

from protocol import Packet, PacketID  # noqa


class BravoDriver:
    """Low-level interface for sending and receiving serial data from the Bravo 7."""

    def __init__(self, ip: str = "192.168.2.3", port: int = 6789) -> None:
        """Create a new driver.

        Args:
            ip: The IP address of the Bravo 7. Defaults to "192.168.2.4".
            port: The port to connect with the Bravo 7 over. Defaults to 6789.
        """
        self.address = (ip, port)
        self.callbacks: dict[PacketID, list[Callable]] = {}
        self._running = False

        # Configure the logger
        logging.basicConfig()
        self._logger = logging.getLogger("BravoDriver")
        self._logger.setLevel(logging.INFO)

        # Configure a new socket with the Bravo
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)

        self.poll_t = threading.Thread(target=self._poll)
        self.poll_t.setDaemon(True)

        atexit.register(self.disconnect)

    def connect(self) -> None:
        """Connect the driver to the Bravo 7."""
        self._running = True
        self.poll_t.start()
        self._logger.info(
            "Successfully established a connection to the Reach Bravo 7 manipulator."
        )

    def disconnect(self) -> None:
        """Disconnect the driver from the Bravo 7."""
        self._running = False
        self.poll_t.join()
        self._logger.info(
            "Successfully shut down the connection to the Reach Bravo 7 manipulator."
        )

    def send(self, packet: Packet):
        """Send a packet to the Bravo 7.

        Args:
            packet: The serial packet to send.
        """
        self.sock.sendto(packet.encode(), self.address)

    def attach_callback(self, packet_id: PacketID, callback: Callable) -> None:
        """Bind a callback to the given packet type.

        Args:
            packet_id: The ID of the packet that, when received, should signal the
                callback.
            callback: The callback to execute when a packet with the given ID is
                received.
        """
        if packet_id not in self.callbacks:
            self.callbacks[packet_id] = []

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
                except Exception:
                    ...
                else:
                    try:
                        for func in self.callbacks[packet.packet_id]:
                            func(packet)
                    except Exception:
                        ...
